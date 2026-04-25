## Задание

- [ ]  1. Поставьте `Docker` и `buildkit`

```shell
$ brew install buildkit
$ brew install docker
```

- [ ]  2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```shell
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker run --rm -it hello-appsec-world

$ docker save -o hello.tar hello-appsec-world
$ docker load -i hello.tar
$ docker load -i image.tar
```

- [ ]  3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
- [ ]  4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`.

> Пример анализа по текущему `Dockerfile` в репозитории

```dockerfile
# Этап 1: сборка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /hello
# Копируем файл с зависимостями
COPY requirements.txt . 
# Устанавливаем зависимости в отдельную директорию wheelhouse для кеширования
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# Этап 2: запускаемый образ
FROM python:3.11-slim
WORKDIR /hello
# Копируем файл с зависимостями
COPY --from=builder /wheels /wheels # Копируем собранные wheel-пакеты
COPY requirements.txt . 
# Устанавливаем зависимости из wheel-пакетов
RUN pip install --no-index --find-links=/wheels -r requirements.txt
# Копируем исходный код приложения
COPY hello.py .

# Переменные окружения для улучшенной работы Python
ENV PYTHONUNBUFFERED=1
# Запускаем приложение
CMD ["python", "hello.py"] 
```

- [ ]  5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```shell
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker save -o hello_ypur_project.tar hello-appsec-world

$ docker load -i hello_ypur_project.tar
$ docker run hello-appsec-world

$ docker load -i image.tar
$ docker run hello-appsec-world
```

- [ ]  6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате:

```
flask==2.2.3
requests==2.28.1
```

- [ ]  7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.
- [ ]  8. Выведите на терминале и проанализируйте следующие команды консоли

```shell
$ docker login
$ docker tag hello-appsec-world yourusername/hello-appsec-world
$ docker push yourusername/hello-appsec-world
$ docker inspect yourusername/hello-appsec-world
$ docker container create --name first hello-appsec-world # выпишите id контейнера

$ docker image pull geminishkv/hello-appsec-world
$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world

```

- [ ]  9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```shell
 $ docker container run -it ubuntu /bin/bash
```

- [ ]  10. Выведите оба контейнера first и second на терминал
- [ ]  11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```shell
$ docker-compose up --build
```

- [ ]  12. Откройте соседнее окно терминала и и выведите на терминале

```shell
$ open -a "Google Chrome" http://localhost:8000
```

- [ ]  13. Остановите работу `docker-compose`.

```shell
$ docker ps -a
$ docker ps -q
$ docker images

$ docker ps -q | xargs docker stop
$ docker-compose down
```

- [ ]  14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
- [ ]  15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`

## Выполнение задания:
Процесс установки докера :
```bash 
# 1. Обновитт систему
sudo apt update

# 2. Установитт зависимости
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. Добавить официальный GPG-ключ Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Добавьте репозиторий
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Обновить пакеты и установите Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# Добавьте текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Примените изменения (выйдите и зайдите заново, или:)
newgrp docker

$ docker --version
Docker version 29.1.2, build 890dcca
```

Вывод содержимого файла hello.py

```bash
$ nano hello.py
print("Hello, AppSec World! 🐳")
  ```

Создание Dockerfile
```bash
$ nano Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]

```

**Процесс сборки и тестирования образа:** 
```bash 
$ docker buildx build -t hello-appsec-world .
[+] Building 10.6s (8/8) FINISHED                                docker:default
 => [internal] load build definition from Dockerfile                       0.1s
 => => transferring dockerfile: 117B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        1.9s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/3] FROM docker.io/library/python:3.11-slim@sha256:7cd0079a9bd8800c  6.8s
 => => resolve docker.io/library/python:3.11-slim@sha256:7cd0079a9bd8800c  0.1s
 => => sha256:3f0cdbca744e7bd0ce0ff6da73b9148829b043099259929 249B / 249B  0.4s
 => => sha256:4d55cfecf3663813d03c369bcd532b89f41cf07b6 14.36MB / 14.36MB  2.2s
 => => sha256:72cf4c3b83019e176aba979aba419d35f56576bbcfc 1.29MB / 1.29MB  1.0s
 => => sha256:1733a4cd59540b3470ff7a90963bcdea5b543279d 29.78MB / 29.78MB  4.7s
 => => extracting sha256:1733a4cd59540b3470ff7a90963bcdea5b543279dd6bdaf0  1.1s
 => => extracting sha256:72cf4c3b83019e176aba979aba419d35f56576bbcfc4f724  0.1s
 => => extracting sha256:4d55cfecf3663813d03c369bcd532b89f41cf07b65d95887  0.6s
 => => extracting sha256:3f0cdbca744e7bd0ce0ff6da73b9148829b0430992599295  0.0s
 => [internal] load build context                                          0.1s
 => => transferring context: 72B                                           0.0s
 => [2/3] WORKDIR /app                                                     1.0s
 => [3/3] COPY hello.py .                                                  0.1s
 => exporting to image                                                     0.4s
 => => exporting layers                                                    0.2s
 => => exporting manifest sha256:bff92fe7a4e9edfd4d947dd6c9ea9aad1fd86161  0.0s
 => => exporting config sha256:8842fd86de7a786e93867eab9a779889ba8d448998  0.0s
 => => exporting attestation manifest sha256:9491310467d4d6a9dd9dd287fd92  0.0s
 => => exporting manifest list sha256:c72e613629d41c660fe98f1cfb813cc832a  0.0s
 => => naming to docker.io/library/hello-appsec-world:latest               0.0s
 => => unpacking to docker.io/library/hello-appsec-world:latest            0.1s
 

# `buildx` — современный билдер (поддержка кэширования, multi-arch)
# `-t hello-appsec-world` — тег образа
# `.` — контекст сборки (текущая директория)

# 2. Запуск контейнера (однократно)
$ docker run hello-appsec-world
Hello, AppSec World! 🐳
# Вывод: Hello, AppSec World! 🐳
# Контейнер остаётся в состоянии «Exited» 

# 3. Интерактивный запуск с автоматической очисткой
docker run --rm -it hello-appsec-world
# То же самое, но:
# `--rm` — удалить контейнер после завершения
# `-it` — интерактивный режим (для Python print — не обязателен, но безопаснее)

# 4. Сохранение образа в архив
docker save -o hello.tar hello-appsec-world
$ docker save -o hello.tar hello-appsec-world
vboxuser@ubuntu:~/devsecops/lab5$ ls
Dockerfile  hello.py  hello.tar
# • Формат: tar-архив со всеми слоями и метаданными

# 5. Загрузка обратно (проверка целостности)
$ docker load -i hello.tar
Loaded image: hello-appsec-world:latest
# Вывод: Loaded image: hello-appsec-world:latest

$ docker load -i image.tar
open image.tar: no such file or directory

```
## **Анализ Dockerfile**
| Проблема                             | Риск                             | Рекомендация                                  |
| ------------------------------------ | -------------------------------- | --------------------------------------------- |
| Запуск от `root`                     | Высокий                          | Добавить `USER non-root`                      |
| Минимальный контроль зависимостей    | Средний                          | Добавить `requirements.txt`, даже если пустой |
| Нет `EXPOSE`, `HEALTHCHECK`, `LABEL` | Низкий                           | Для production — добавить                     |
| Нет многоэтапной сборки              | Средний (для больших приложений) | Не критично для hello.py, но нужно для Flask  |
### Обновление `Dockerfile`
``` dockerfile 
FROM python:3.11-slim AS builder


RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt


FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 1001 appgroup && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos '' appuser

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY hello.py .

USER appuser

ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["python", "hello.py"]
```

| Улучшение                              | Эффект                                                                        |
| -------------------------------------- | ----------------------------------------------------------------------------- |
| `--no-cache-dir`, `rm -rf /var/lib...` | ↓ размер образа (~50–100 МБ экономии)                                         |
| `adduser` + `USER appuser`             | ❌ Нет запуска от root                                                         |
| `--no-index --find-links`              | ↑ безопасность: зависимости только из `/wheels` (не из интернета при запуске) |
| `EXPOSE 8000`                          | Явное указание порта                                                          |
| `PYTHONDONTWRITEBYTECODE=1`            | Защита от записи `.pyc` в volume                                              |
```bash 

# Сборка нового образа

$ docker buildx build -t hello-appsec-world .
[+] Building 14.3s (16/16) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 807B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        1.1s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => CACHED [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:7  0.1s
 => => resolve docker.io/library/python:3.11-slim@sha256:7cd0079a9bd8800c  0.1s
 => [internal] load build context                                          0.0s
 => => transferring context: 508B                                          0.0s
 => CACHED [builder 2/4] WORKDIR /app                                      0.0s
 => [stage-1 2/8] RUN apt-get update &&     apt-get install -y --no-insta  4.9s
 => [builder 3/4] COPY requirements.txt .                                  0.4s
 => [builder 4/4] RUN pip install --user --no-cache-dir --upgrade pip      7.3s
 => [stage-1 3/8] RUN addgroup --gid 1001 appgroup &&     adduser --uid 1  0.7s
 => [stage-1 4/8] WORKDIR /app                                             0.1s
 => [stage-1 5/8] COPY --from=builder /wheels /wheels                      0.2s 
 => [stage-1 6/8] COPY requirements.txt .                                  0.1s 
 => [stage-1 7/8] RUN pip install --no-cache-dir --no-index --find-links=  2.6s 
 => [stage-1 8/8] COPY hello2.py .                                         0.1s 
 => exporting to image                                                     1.8s 
 => => exporting layers                                                    1.2s 
 => => exporting manifest sha256:532e54a118a346629cd233aa732a5ec9d2c05820  0.0s 
 => => exporting config sha256:1c529506843b4dad63cdef371c07ca3b26a8062995  0.0s
 => => exporting attestation manifest sha256:23b2aa5ee1f8fcb22034fc265a05  0.0s
 => => exporting manifest list sha256:d69bf3541347242ebb06925c008b599417e  0.0s
 => => naming to docker.io/library/hello-appsec-world:latest               0.0s
 => => unpacking to docker.io/library/hello-appsec-world:latest            0.5s


vboxuser@ubuntu:~/devsecops/lab5$ docker run -d --name test-app -p 8000:8000 hello-appsec-world
13575ba5d3a92ba746fd2dcd3af51c21f9259c1fe36e893fc93f117dc5b9185a


vboxuser@ubuntu:~/devsecops/lab5$ docker stop test-app && docker rm test-app

test-app



vboxuser@ubuntu:~/devsecops/lab5$ docker buildx build -t hello-appsec-world .
[+] Building 13.9s (16/16) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 807B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        1.0s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:7cd0079a  0.1s
 => => resolve docker.io/library/python:3.11-slim@sha256:7cd0079a9bd8800c  0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 107B                                          0.0s
 => CACHED [builder 2/4] WORKDIR /app                                      0.0s
 => [builder 3/4] COPY requirements.txt .                                  0.1s
 => [builder 4/4] RUN pip install --user --no-cache-dir --upgrade pip      7.1s
 => CACHED [stage-1 2/8] RUN apt-get update &&     apt-get install -y --n  0.0s 
 => CACHED [stage-1 3/8] RUN addgroup --gid 1001 appgroup &&     adduser   0.0s 
 => CACHED [stage-1 4/8] WORKDIR /app                                      0.0s 
 => [stage-1 5/8] COPY --from=builder /wheels /wheels                      0.1s 
 => [stage-1 6/8] COPY requirements.txt .                                  0.1s 
 => [stage-1 7/8] RUN pip install --no-cache-dir --no-index --find-links=  2.7s 
 => [stage-1 8/8] COPY hello2.py .                                         0.2s 
 => exporting to image                                                     2.2s 
 => => exporting layers                                                    1.6s 
 => => exporting manifest sha256:2046ba64b58a2fb5c8b5cebbc3d4469ca31beee1  0.0s 
 => => exporting config sha256:d29eca6521fdbadd5f5c0bf6d3c91c779fd0be249b  0.0s
 => => exporting attestation manifest sha256:fee739a2f0a0063d57ae238d954d  0.0s
 => => exporting manifest list sha256:ed41fd05a59a3b14fb7aaa170119b2d1f61  0.0s
 => => naming to docker.io/library/hello-appsec-world:latest               0.0s
 => => unpacking to docker.io/library/hello-appsec-world:latest            0.4s

vboxuser@ubuntu:~/devsecops/lab5$ docker save -o hello_final.tar hello-appsec-world
vboxuser@ubuntu:~/devsecops/lab5$ git add hello_final.tar
vboxuser@ubuntu:~/devsecops/lab5$ git commit -m "build: final image with requests"
[main c2ba06b] build: final image with requests
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 lab5/hello_final.tar

vboxuser@ubuntu:~/devsecops/lab5$ docker inspect etonastya/hello-appsec-world:lab05 | jq -r '.[0].Config.User'
appuser

#значает, что  образ `etonastya/hello-appsec-world:lab05` настроен правильно с точки зрения безопасности. Внутри контейнера процессы будут работать от имени пользователя `appuser`, а не `root`. Это значительно снижает риски при возможной эксплуатации уязвимостей (например, RCE): злоумышленник не получит root-доступ к хосту.

vboxuser@ubuntu:~/devsecops/lab5$ docker container create --name first hello-appsec-world
4c259b4319f6bfca03a5bca44b178d03697d0a668975b4f4797345ec18ae7c9d

vboxuser@ubuntu:~/devsecops/lab5$ CONTAINER_FIRST=$(docker container inspect -f '{{.4c259b4319f6bfca03a5bca44b178d03697d0a668975b4f4797345ec18ae7c9d}}' first)
template parsing error: template: :1: bad number syntax: ".4c"

vboxuser@ubuntu:~/devsecops/lab5$ CONTAINER_FIRST=$(docker container inspect -f '{{.Id}}' first)

vboxuser@ubuntu:~/devsecops/lab5$ CONTAINER_FIRST=$(docker container inspect -f '{{.Id}}' first)

vboxuser@ubuntu:~/devsecops/lab5$ echo $CONTAINER_FIRST
4c259b4319f6bfca03a5bca44b178d03697d0a668975b4f4797345ec18ae7c9d


vboxuser@ubuntu:~/devsecops/lab5$ docker run -it --rm ubuntu /bin/bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
20043066d3d5: Pull complete 
Digest: sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54
Status: Downloaded newer image for ubuntu:latest
root@23c998029733:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.0   4588  3928 pts/0    Ss   22:04   0:00 /bin/bash
root           9  0.0  0.0   7888  4224 pts/0    R+   22:04   0:00 ps aux
root@23c998029733:/# id 
uid=0(root) gid=0(root) groups=0(root)
root@23c998029733:/# exit
exit

```

Далее были выведены на терминал и проанализированы в консоли процессы, которые запущены.

```shell
 $ docker container run -it ubuntu /bin/bash
 
# немного не верная команда, ниже написана верная. 
 
vboxuser@ubuntu:~/devsecops/lab5$ docker run -it --rm --entrypoint /bin/sh etonastya/hello-appsec-world:lab05
Unable to find image 'etonastya/hello-appsec-world:lab05' locally
lab05: Pulling from etonastya/hello-appsec-world
1733a4cd5954: Pull complete 
72cf4c3b8301: Pull complete 
4d55cfecf366: Pull complete 
3f0cdbca744e: Pull complete 
054c50ce3d06: Pull complete 
fe04e219170c: Pull complete 
57472376a1c9: Pull complete 
1212342b5c2d: Pull complete 
7a93f042c2cb: Pull complete 
ed0606b1c5c0: Pull complete 
30fa13526ccd: Pull complete 
Digest: sha256:ed41fd05a59a3b14fb7aaa170119b2d1f612da94d58372d65be2c6d16c1c20bc
Status: Downloaded newer image for etonastya/hello-appsec-world:lab05
$ ps aux
/bin/sh: 1: ps: not found
$ id 
/bin/sh: 2: шid: not found
$ id
uid=1001(appuser) gid=1001(appgroup) groups=1001(appgroup),100(users)

vboxuser@ubuntu:~/devsecops/lab5$ docker-compose up --build
Creating network "lab5_app_net" with the default driver
Building server
[+] Building 24.4s (14/14) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.1s
 => => transferring dockerfile: 419B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        2.1s
 => [auth] library/python:pull token for registry-1.docker.io              0.0s
 => [internal] load .dockerignore                                          0.2s
 => => transferring context: 2B                                            0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e  0.5s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd7  0.2s
 => => sha256:158caf0e080e2cd74ef2879ed3c4e697792ee6525 10.37kB / 10.37kB  0.0s
 => => sha256:26fe52250f1b8012f5061c8f7228e6fca4f100aa3f9 1.75kB / 1.75kB  0.0s
 => => sha256:cb352e69d7b69f39dbc2cc35ecc34d01ca14439abc5 5.48kB / 5.48kB  0.0s
 => [internal] load build context                                          0.3s
 => => transferring context: 842B                                          0.1s
 => [builder 2/4] WORKDIR /app                                             0.1s
 => [builder 3/4] COPY requirements.txt .                                  0.2s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir  17.2s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                      0.0s 
 => [stage-1 4/6] COPY requirements.txt .                                  0.1s 
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requ  3.1s 
 => [stage-1 6/6] COPY app.py .                                            0.1s 
 => exporting to image                                                     0.2s 
 => => exporting layers                                                    0.2s 
 => => writing image sha256:0f5cebc9fa053a2390b06335444a74d9c2d78fabef169  0.0s
 => => naming to docker.io/library/lab5_server                             0.0s
Building client
[+] Building 14.7s (13/13) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 425B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        0.2s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 576B                                          0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e  0.0s
 => CACHED [builder 2/4] WORKDIR /app                                      0.0s
 => [builder 3/4] COPY requirements.txt .                                  0.1s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=  9.0s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                      0.0s 
 => [stage-1 4/6] COPY requirements.txt .                                  0.1s 
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requ  4.0s 
 => [stage-1 6/6] COPY client.py .                                         0.2s 
 => exporting to image                                                     0.4s 
 => => exporting layers                                                    0.4s 
 => => writing image sha256:f68fb603eddfdfc9771a4adf55391bd22db88e4d86ca4  0.0s 
 => => naming to docker.io/library/lab5_client                             0.0s 
Creating lab5_server_1 ... done
Creating lab5_client_1 ... done
Attaching to lab5_server_1, lab5_client_1
server_1  |  * Serving Flask app 'app'
server_1  |  * Debug mode: off
server_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
server_1  |  * Running on all addresses (0.0.0.0)
server_1  |  * Running on http://127.0.0.1:8000
server_1  |  * Running on http://172.19.0.2:8000
server_1  | Press CTRL+C to quit
server_1  | 172.19.0.3 - - [12/Dec/2025 22:15:19] "GET / HTTP/1.1" 200 -
client_1  | 
client_1  |     <html>
client_1  |     <head><title>Colorful Output</title></head>
client_1  |     <body style="font-family: monospace; font-size: 24px;">
client_1  |     <span style="color:red">h</span><span style="color:green">e</span><span style="color:yellow">l</span><span style="color:blue">l</span><span style="color:purple">o</span><span style="color:red"> </span><span style="color:green">a</span><span style="color:yellow">p</span><span style="color:blue">p</span><span style="color:purple">s</span><span style="color:red">e</span><span style="color:green">c</span><span style="color:yellow"> </span><span style="color:blue">w</span><span style="color:purple">o</span><span style="color:red">r</span><span style="color:green">l</span><span style="color:yellow">d</span>
client_1  |     </body>
client_1  |     </html>
client_1  |     
lab5_client_1 exited with code 0
```

![[img5.png]]


```bash 
# Проверка эндпоинтов

vboxuser@ubuntu:~$ curl http://localhost:8000/health
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
vboxuser@ubuntu:~$ curl http://localhost:8000/info
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>


# Просмотр всех контейнеров
vboxuser@ubuntu:~/devsecops/lab5$ docker ps -a
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                        PORTS                                         NAMES
da52ee36023d   lab5_client          "python client.py"       5 minutes ago    Exited (0) 2 minutes ago                                                    lab5_client_1
46abaf5950dc   lab5_server          "python app.py"          5 minutes ago    Exited (137) 12 seconds ago                                                 lab5_server_1
9ac4c5fd6256   nginx:alpine         "/docker-entrypoint.…"   11 minutes ago   Exited (255) 3 minutes ago                                                  9ac4c5fd6256_vulnerable-nginx
03221533c363   python:3.11-alpine   "python app.py"          11 minutes ago   Exited (2) 3 minutes ago                                                    vulnerable-app
3d55d54b29a1   postgres:16-alpine   "docker-entrypoint.s…"   11 minutes ago   Up 5 minutes                  0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   insecure-db

# Просмотр только ID запущенных
vboxuser@ubuntu:~/devsecops/lab5$ docker ps -q
3d55d54b29a1

# Остановка ВСЕХ контейнеров 
vboxuser@ubuntu:~/devsecops/lab5$ docker ps -q | xargs docker stop 2>/dev/null || true
3d55d54b29a1


vboxuser@ubuntu:~/devsecops/lab5$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# Удаление остановленных
vboxuser@ubuntu:~/devsecops/lab5$ docker-compose down --rmi local -v --remove-orphans
Removing lab5_client_1 ... done
Removing lab5_server_1 ... done
Removing network lab5_app_net
Removing image lab5_server
Removing image lab5_client

# Просмотр образов
vboxuser@ubuntu:~/devsecops/lab5$ docker images
                                                            i Info →   U  In Use
IMAGE                           ID             DISK USAGE   CONTENT SIZE   EXTRA
alpine:latest                   7acffee03fe8       8.44MB             0B        
etonastya/hello-appsec-world:lab05
                                d29eca6521fd        144MB             0B        
nginx:alpine                    a236f84b9d5d       53.7MB             0B    U   
nginx:latest                    576306625d79        152MB             0B        
postgres:16-alpine              52f87503b2fe        276MB             0B    U   
python:3.11-alpine              33146c594cc9       54.3MB             0B    U   
ubuntu:latest                   c3a134f2ace4       78.1MB             0B        
vboxuser@ubuntu:~/devsecops/lab5$ 

```

Доработка docker-compose.yml:

```bash 
version: '3.8'

services:
  web:
    build:
      context: ./source
      dockerfile: Dockerfile
    image: hello-appsec-world:local
    container_name: hello-web
    ports:
      - "8000:8000"          # host:container
    # Безопасные настройки:
    user: "1001:1001"      # явное указание UID:GID 
    read_only: true        # ФС только для чтения (кроме /tmp)
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL                # Убираем все capabilities
    restart: unless-stopped

```


**Вывод:**
```bash 
vboxuser@ubuntu:~/devsecops/lab5$ docker-compose up --build
Creating network "lab5_default" with the default driver
Building web
[+] Building 11.3s (14/14) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 429B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        0.9s
 => [auth] library/python:pull token for registry-1.docker.io              0.0s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [internal] load build context                                          0.1s
 => => transferring context: 477B                                          0.0s
 => CACHED [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:1  0.0s
 => [builder 2/4] WORKDIR /hello                                           0.1s
 => [builder 3/4] COPY requirements.txt .                                  0.1s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=  6.1s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                      0.1s 
 => [stage-1 4/6] COPY requirements.txt .                                  0.1s 
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requ  2.9s 
 => [stage-1 6/6] COPY hello.py .                                          0.2s 
 => exporting to image                                                     0.3s 
 => => exporting layers                                                    0.2s 
 => => writing image sha256:49f6e34e288f78b867e4fbe639c51e11ddf7775e297c4  0.0s 
 => => naming to docker.io/library/hello-appsec-world:local                0.0s 
Creating hello-web ... done
Attaching to hello-web
hello-web | exec /usr/local/bin/python: operation not permitted
vboxuser@ubuntu:~/devsecops/lab5$ 

```
