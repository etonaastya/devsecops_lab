## Задание

- [ ]  1. Необходимо установить `Docker Engine` для Linux

```shell
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo usermod -aG docker "$USER"

$ sudo systemctl start docker
$ docker pull docker/docker-bench-security
```

- [ ]  2. Проверьте работу докера и сделать скрипт `audit.sh` исполняемым
- [ ]  3. Развернуть уязвимое приложение как отдельные стенды

```shell
$ docker compose up -d # основной web, app, postgres
$ docker-compose -f dvulnerable-app.yml up -d # поверх для vulnerable-web, debug-shell
    -f # file
    up # создает и поднимает файлы из compose
    -d # фоновый режим
```

- [ ]  4. Запустите скрипт из `venv` и проанализируйте то, что вывело на терминале и что вывело при конвертировании

```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install openpyxl odfpy
$ ./audit.sh
$ deactivate # или $ deactivate 2>/dev/null || true
```

- [ ]  5. Проведите анализ уязвимостей, опишите их причину возникновения
- [ ]  6. Опишите влияния уязвимостей, их сценарий атаки
- [ ]  7. Оцените риски ИБ и предложите меры для их снижения:

> - Следует разобрать `.yaml` описав, что в них считается не безопасным и почему
> - Опишите сценарии реализации рисков CR, DL
> - Предложили исправленные `.yaml`

- [ ]  8. Сделайте анализ уязвимостей из сгенерированных файлов .odt, .xslx и опишите их в отчете. Файлы конвертируются в эти директории

```shell
"├── json/          (Trivy JSON outputs)"
"├── text/          (CIS audit text outputs)"
"├── xlsx/          (Excel spreadsheets)"
"└── odt/           (OpenDocument Text files)"
```

- [ ]  9. Подготовьте отчет `gist`.
- [ ]  10. Почистите кеш от `venv` и остановите уязвимостей приложение, почистите контейнера

```shell
$ rm -rf venv
$ docker-compose -f demo-vulnerable-app.yml down
$ docker system prune -f
```

#### **Установка Docker и подготовка инструментов**
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker "$USER"
sudo systemctl start docker
docker pull docker/docker-bench-security


sudo snap install docker & sudo apt  install docker-compose

```
 **Вывод:** установлен Docker Engine, добавлен пользователь в группу `docker`, запущен демон, загружен образ `docker-bench-security`

Сдели исполняемым скрипт `audit.sh` с помощью команды: 
```bash 
chmod +x audit.sh
```
#### **Развертывание уязвимого приложения**

Ошибка в команде docker-compose -f dvulnerable-app.yml up -d , а также остановка развертывания компонента:
```
vboxuser@ubuntu:~/devsecops/lab6$ docker-compose -f dvulnerable-app.yml up -d
ERROR: .FileNotFoundError: [Errno 2] No such file or directory: './dvulnerable-app.yml'
vboxuser@ubuntu:~/devsecops/lab6$ ls
app  audit.sh  config  db  docker-compose.yml  README.md  vulnerable-app.yml
vboxuser@ubuntu:~/devsecops/lab6$ docker-compose -f vulnerable-app.yml up -d
WARNING: Found orphan containers (insecure-db, vulnerable-app) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Recreating 9ac4c5fd6256_vulnerable-nginx ... 
Creating debug-shell                     ... 

ERROR: for debug-shell  "host" network_mode is incompatible with port_bindings

ERROR: for 9ac4c5fd6256_vulnerable-nginx  'ContainerConfig'

ERROR: for debug-shell  "host" network_mode is incompatible with port_bindings

ERROR: for vulnerable-web  'ContainerConfig'
Traceback (most recent call last):
  File "/usr/bin/docker-compose", line 33, in <module>
    sys.exit(load_entry_point('docker-compose==1.29.2', 'console_scripts', 'docker-compose')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/cli/main.py", line 81, in main
    command_func()
  File "/usr/lib/python3/dist-packages/compose/cli/main.py", line 203, in perform_command
    handler(command, command_options)
  File "/usr/lib/python3/dist-packages/compose/metrics/decorator.py", line 18, in wrapper
    result = fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/cli/main.py", line 1186, in up
    to_attach = up(False)
                ^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/cli/main.py", line 1166, in up
    return self.project.up(
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/project.py", line 697, in up
    results, errors = parallel.parallel_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/parallel.py", line 108, in parallel_execute
    raise error_to_reraise
  File "/usr/lib/python3/dist-packages/compose/parallel.py", line 206, in producer
    result = func(obj)
             ^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/project.py", line 679, in do
    return service.execute_convergence_plan(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 579, in execute_convergence_plan
    return self._execute_convergence_recreate(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 499, in _execute_convergence_recreate
    containers, errors = parallel_execute(
                         ^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/parallel.py", line 108, in parallel_execute
    raise error_to_reraise
  File "/usr/lib/python3/dist-packages/compose/parallel.py", line 206, in producer
    result = func(obj)
             ^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 494, in recreate
    return self.recreate_container(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 612, in recreate_container
    new_container = self.create_container(
                    ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 330, in create_container
    container_options = self._get_container_create_options(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 921, in _get_container_create_options
    container_options, override_options = self._build_container_volume_options(
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 960, in _build_container_volume_options
    binds, affinity = merge_volume_bindings(
                      ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 1548, in merge_volume_bindings
    old_volumes, old_mounts = get_container_data_volumes(
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/compose/service.py", line 1579, in get_container_data_volumes
    container.image_config['ContainerConfig'].get('Volumes') or {}
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
KeyError: 'ContainerConfig'

```

#### Запуск скрипта в venv и генерация отчетов

```bash 

vboxuser@ubuntu:~/devsecops/lab6$ python3 -m venv venv
vboxuser@ubuntu:~/devsecops/lab6$ source venv/bin/activate
(venv) vboxuser@ubuntu:~/devsecops/lab6$ pip install openpyxl odfpy
.......
(venv) vboxuser@ubuntu:~/devsecops/lab6$ ls
app       config  docker-compose.yml  venv
audit.sh  db      README.md           vulnerable-app.yml
(venv) vboxuser@ubuntu:~/devsecops/lab6$ ./audit.sh 
Starting Docker CIS & Image Security Audit
==========================================
Detected platform: Linux
Using docker-bench-security image: docker/docker-bench-security:latest
Reports will be saved to: ./audit_reports/

Bench image docker/docker-bench-security:latest not found locally.
Pulling it explicitly...
latest: Pulling from docker/docker-bench-security
cd784148e348: Pull complete 
48fe0d48816d: Pull complete 
164e5e0f48c5: Pull complete 
378ed37ea5ff: Pull complete 
Digest: sha256:ddbdf4f86af4405da4a8a7b7cc62bb63bfeb75e85bf22d2ece70c204d7cfabb8
Status: Downloaded newer image for docker/docker-bench-security:latest
docker.io/docker/docker-bench-security:latest

Trivy not found, skipping image vulnerability scan for docker/docker-bench-security:latest

Trivy not found, skipping lab images scan

Linux host detected – configuring mounts for CIS Docker Benchmark coverage

Mounting /usr/bin/containerd
Mounting /usr/bin/runc
Mounting /usr/lib/systemd
Mounting /etc/docker
Mounting /var/log
Running Docker Bench Security container (CIS host audit)

docker: Error response from daemon: error while creating mount source path '/usr/bin/containerd': mkdir /usr/bin/containerd: read-only file system

Run 'docker run --help' for more information
(venv) vboxuser@ubuntu:~/devsecops/lab6$ deactivate 
vboxuser@ubuntu:~/devsecops/lab6$ 
```
##### **Анализ уязвимостей и их причины**
Файл docker-compose.yml:

|Уязвимость|Причина|
|---|---|
|**Hardcoded `POSTGRES_PASSWORD=root`**|Предсказуемый пароль → easy RCE/дамп БД|
|**`APP_SECRET_KEY=hardcoded-in-env`**|Секрет в открытом виде — если приложение использует Flask/Django, возможна подделка сессий|
|**`DEBUG=true`**|Вывод стек-трейсов, переменных окружения, путей → утечка инфы|
|**`volumes: - ./app:/app:rw`**|Запись в код приложения → можно внедрить веб-шелл (`echo "<?php system(\$_GET['c']);?>" > app/shell.php`)|
|**`user: "nginx"` — хорошо**, но в `app` нет `user` → Python-контейнер запускается от `root`||
Файл vulnerable-app.yml: 

|Уязвимость|Причина|
|---|---|
|**`privileged: true`**|Даёт контейнеру **все capabilities ядра**, включая `CAP_SYS_ADMIN` → полный контроль над хостом|
|**`network_mode: host` + `pid: host`**|Контейнер работает в **пространстве процессов и сети хоста** — видит все процессы, порты, может перехватывать трафик|
|**`user: "0:0"` (root)**|Все процессы запускаются от `root` внутри контейнера → проще эскалация|
|**`volumes: - /:/hostroot:rw`**|Полный **read-write доступ ко всей файловой системе хоста**|
|**`/var/run/docker.sock` примонтирован**|Возможность запуска **новых контейнеров от имени хоста** → container breakout, DoS, RCE на хосте|
|**Hardcoded credentials в `environment`**:<br>`ADMIN_PASSWORD=admin123`, `SSH_PASSWORD=password`, `DB_PASSWORD=root`, `FLAG=...`|Утечка секретов → прямой вход без брутфорса|
|**`cap_add: ALL` + `seccomp:unconfined` + `apparmor:unconfined`**|Полное отключение всех механизмов изоляции ядра|
|**SSH-сервер в `debug-shell` с `PermitRootLogin=yes`**|Прямой root-доступ по SSH на порт 22 хоста (!)|
##### **Сценарии атаки и влияние**

###### **Сценарий: Эскалация до root на хосте через `debug-shell`**

1. Атакующий подключается по SSH:  
    `ssh root@ваш_хост -p 22` → пароль `password`
2. Получает **полный root-доступ к хосту** (не к контейнеру!)
3. Может:
    - Прочитать `/etc/shadow`, `/home/vboxuser/.ssh/id_rsa`
    - Запустить `docker run -v /:/host alpine chroot /host /bin/sh`
    - Установить бэкдор, keylogger, майнер
    - Удалить все данные: `rm -rf /home /var/lib/docker`

→ **Влияние**: **CR + IA + DL** (полная компрометация)

##### **Оценка рисков ИБ и меры снижения**

| Риск                                                          | Мера снижения                                                                                                            |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Компрометация хоста** (через `privileged` + `/`)            | **ЗАПРЕТИТЬ `privileged: true`**, убрать `volumes: /:/hostroot`, ограничить `cap_drop: ALL`, использовать `userns-remap` |
| **Утечка секретов** (`ADMIN_PASSWORD`, `FLAG`, `DB_PASSWORD`) | Использовать **Docker secrets** или **HashiCorp Vault**, убрать из `environment`, использовать `.env` + `.gitignore`     |
| **Доступ к `docker.sock`**                                    | **Не монтировать `/var/run/docker.sock`**, если не требуется (а здесь — не требуется!)                                   |
| **Открытый SSH-доступ** (`debug-shell`)                       | Удалить `debug-shell`, или заменить на `docker exec -it ...` + строгие ACL                                               |
| **Запуск от root** (`user: "0:0"` без `USER` в Dockerfile)    | Добавить `user: "1001:1001"` и `non-root` пользователя в образах                                                         |
| **Отсутствие Trivy**                                          | Установить `trivy` → внедрить в CI/CD: `trivy config .`, `trivy image ...`                                               |
 Исправленный `vulnerable-app.yml:
```bash

version: "3.8"

services:
  vulnerable-web-demo:
    image: nginx:alpine
    container_name: vulnerable-web-demo
    # УБРАНО: privileged, host network, pid:host, cap_add:ALL
    # Добавлены ограничения:
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
      - apparmor:docker-default
    user: "101:101"  # nginx UID/GID
    restart: "no"  # не "always"
    ports:
      - "8081:80"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      # УБРАНО: /:/hostroot, /var/run/docker.sock
    # УБРАНО: environment с паролями и флагом

  # УДАЛЁН debug-shell — он не нужен в проде, а в лабе — временно и под строгим контролем
```

Отчеты получились не полными. Исправление - установка **Trivy**.
```bash 
sudo apt install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo gpg --dearmor -o /usr/share/keyrings/trivy.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install trivy

#ручное сканирование

# Сканирование конфигов compose
trivy config .

# Сканирование образов
trivy image nginx:alpine
trivy image postgres:16-alpine
trivy image python:3.11-alpine

#Вывод:
vboxuser@ubuntu:~/devsecops/lab6$ trivy config .
2025-12-12T23:05:37Z	INFO	Misconfiguration scanning is enabled
2025-12-12T23:05:37Z	INFO	Need to update the built-in policies
2025-12-12T23:05:37Z	INFO	Downloading the built-in policies...
74.86 KiB / 74.86 KiB [------------------------------------] 100.00% ? p/s 100ms
2025-12-12T23:05:38Z	INFO	Detected config files	num=0

#Данный  вывод обоснован установкой не актуальной версии trivy (0.20). Далее была установлена версия 0.50
```

Чистка кеша от `venv` и остановка уязвимого приложения (ошибка в названии я yaml  файла):
```bash vboxuser@ubuntu:~/devsecops/lab6$ rm -rf venv/
vboxuser@ubuntu:~/devsecops/lab6$ docker-compose -f demo-vulnerable-app.yml down
ERROR: .FileNotFoundError: [Errno 2] No such file or directory: './demo-vulnerable-app.yml'
vboxuser@ubuntu:~/devsecops/lab6$ ls
app            audit.sh  db                  README.md
audit_reports  config    docker-compose.yml  vulnerable-app.yml
vboxuser@ubuntu:~/devsecops/lab6$ docker-compose -f vulnerable-app.yml down
WARNING: Found orphan containers (vulnerable-app, insecure-db) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Removing 9ac4c5fd6256_vulnerable-nginx ... done
vboxuser@ubuntu:~/devsecops/lab6$ docker system prune -f
Deleted Containers:
03221533c3633a4f0d8e26be93bfe3e3dc78c13cc80c813a692a1d23fcf574f7

Deleted Networks:
lab5_default

Deleted build cache objects:
9d9g741t676hgoq2rq1kjptyn
3l92c7fb1j1gaz0wwr6jtgi3t
010g4bok3g1fw8yjj7368261f
rfgkqewp9z10gkauh7czqumjn
a6shcxlcb65dzi2f7je0arkdm
p168jlsn8gr2i59mbk2pfgrsp
jk2rdfi55pu7tiv4hytx4lwg7
2yw7qth00xdncfna6f49qg6ac
a9laxc02tbv2aeb3wtu6tcht9
a81u6dhk7fsymwtokmeow9axd
0xkcde0evig3n4edwpd6g7fws
451x82zf8g9lymamw7rovel9t
xol7smjyyjm4zg8mobwi838zm
7axxcrkx47ianj5s9x83ebulg
p2hrcif7ko58mo09w6i1aic3l
zeopd3byy3mxbjh25kks56bv0
m49lnbbxl21tap8x36ra7s5vi
l8gk6thpmmr8bconh1qf3kai8
wzlkyihraw903c3ozzbpgc4ln
lpo8o5ttm2nu8x87wzet7fvg3
ysfbriecslvy0cvfu79cngiek
k7dnqh592igzhplnhxb3cskrl
extfv7at4safaw34n1h5ivmgv
5vwnjcrlj5bxfc2acv110l8o0

Total reclaimed space: 85.8MB

```