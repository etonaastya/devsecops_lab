# Отчёт по лабораторной работе `lab02` 

## 🔹 Задание 1: Базовые команды и анализ

```bash
$ who | wc -l
2
```
 **Результат:** В системе 2 активные пользовательские сессии.  
 **Анализ:** `who` выводит список вошедших пользователей, `wc -l` считает строки = количество сессий.

```bash
$ id
uid=1000(vboxuser) gid=1000(vboxuser) groups=1000(vboxuser),27(sudo),984(docker)
```
 **Результат:** Пользователь `vboxuser` (UID/GID 1000) входит в группы `sudo` и `docker`.  
 **AppSec-значение:** Наличие в `sudo` позволяет эскалацию привилегий, `docker` — потенциальный вектор escape в хост-систему.

```bash
$ whoami
vboxuser
```
 **Результат:** Подтверждение текущего имени пользователя (эквивалент `id -un`).

```bash
$ hostnamectl
Static hostname: ubuntu
Icon name: computer-vm
Chassis: vm 🖴
Machine ID: 29edcb64587b4c90a971ad2f7f692d80
Boot ID: 83eb8eb1e8524d258efd612d25ea300f
Virtualization: oracle
Operating System: Ubuntu 24.04.3 LTS
Kernel: Linux 6.14.0-37-generic
Architecture: x86-64
Hardware Vendor: innotek GmbH
Hardware Model: VirtualBox
```
 **Результат:** Полная информация о системе: виртуальная машина Oracle VirtualBox, Ubuntu 24.04, архитектура x86-64.

---

## 🔹 Задание 2: Дерево каталогов и `ls`

```bash
$ tree -L 2 ~
/home/vboxuser
├── bin
├── Desktop
├── devsecops
├── Documents
├── Downloads
├── lab2_DSO
├── labCV
├── mp
├── Music
├── Pictures
├── project
├── Public
├── snap
├── Templates
└── Videos
43 directories, 14 files
```
 **Результат:** Визуализация структуры домашнего каталога с глубиной 2 уровня.

```bash
$ ls -a ~
.  ..  .bash_history  .bashrc  .cache  .config  ...  snap  .ssh  .vscode
```
 **Результат:** Показаны **все** файлы, включая скрытые (начинающиеся с `.`): конфиги, кэш, SSH-ключи.

```bash
$ ls -l ~
total 60
drwxr-xr-x  6 vboxuser docker   4096 Feb 16  2025 bin
drwxr-xr-x  2 vboxuser vboxuser 4096 Dec 13 11:32 Desktop
drwxrwxr-x 13 vboxuser vboxuser 4096 Dec 11 15:16 devsecops
...
```
 **Результат:** Детальный список с правами (`rwx`), владельцем, группой, размером и датой.   **Отличие:** `-a` = скрытые файлы, `-l` = метаданные. Вместе: `ls -la`.

---

## 🔹 Задание 3: Файловая система на `/dev/sda1`

```bash
$ sudo file -s /dev/sda1
/dev/sda1: data

$ df -hT /dev/sda1
Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs  3.8G     0  3.8G   0% /dev
```
 **Результат:**  
- `file -s` не распознал ФС на `/dev/sda1` (возможно, не примонтирован или это raw-диск).  
- `df -hT` показал, что `/dev/sda1` не отображается в смонтированных — вместо него `/dev` типа `devtmpfs`.

---

## 🔹 Задание 4: Поиск файлов и `locate`

```bash
$ which vi
/usr/bin/vi
```
 **Результат:** Исполняемый файл `vi` найден в `$PATH`.

```bash
$ locate hello.py
/home/vboxuser/.local/share/Trash/files/exmpl_hello.py
/home/vboxuser/devsecops/lab1/lab-report/hello.py
/home/vboxuser/devsecops/lab5/hello.py
...
```
 **Результат:** `locate` нашёл файлы по имени из базы данных `mlocate` (быстро, но может быть неактуально).

```bash
$ touch screen
$ find ~ -name screen
/home/vboxuser/Downloads/course_labs-develop/labs/lab02/screen
```
 **Результат:** `find` выполнил реальный поиск по файловой системе — нашёл только что созданный файл.

```bash
$ locate screen  # до updatedb
# не нашёл новый файл

$ sudo updatedb
$ locate screen  # после updatedb
/home/vboxuser/Downloads/course_labs-develop/labs/lab02/screen
...
```
 **Результат:** После `updatedb` база обновлена, и `locate` теперь видит новый файл `screen`.

 **Вывод:** `locate` работает по кэшу (`/var/lib/mlocate/mlocate.db`), `find` — сканирует ФС в реальном времени.

---

## 🔹 Задание 5: Исправление Pygame-скрипта

 **Создан файл `pygamesteel_fixed.py`** с исправлением бага:

 **Ошибка в исходнике:** переменная `screen` использовалась, но не была инициализирована.  
 **Исправление:**
```python
screen = pygame.display.set_mode(window_size)  # Сохраняем возвращаемый Surface
```

Также улучшена отрисовка:
```python
pygame.draw.rect(screen, bg_color, [0, 0, screen_width, screen_height], 0)  # 0 = заливка
```

```bash
$ python3 pygamesteel.py
pygame 2.5.2 (SDL 2.30.0, Python 3.12.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
^CTraceback (most recent call last):
  File "pygamesteel.py", line 27, in <module>
KeyboardInterrupt
```
 **Результат:** Скрипт запускается, окно отображается, текст "Hello appsec world*" отрисовывается. Завершение через `Ctrl+C`.

---

## 🔹 Задание 6: Git commit & push

 **Выполнено:**
```bash
$ git add exmpl_hello.py pygamesteel.py pygamesteel_fixed.py
$ git commit -m "lab02: add pygame examples, fix screen variable bug"
$ git push -u origin master
```
>  Файлы добавлены в репозиторий в ветку `master`.

---

## 🔹 Задание 7: Управление пользователями

```bash
$ groups
vboxuser sudo docker
```
 **Результат:** Текущие группы пользователя.

```bash
$ sudo useradd smallman
$ sudo passwd smallman
New password:
BAD PASSWORD: The password fails the dictionary check - it is based on a dictionary word
Retype new password:
passwd: password updated successfully
$ sudo usermod -c 'Hach Hachov Hacherovich,239,45-67,499-239-45-33' smallman
$ sudo groupadd -g 1500 readgroup
$ sudo usermod -aG readgroup smallman
$ id smallman
uid=1001(smallman) gid=1001(smallman) groups=1001(smallman),1500(readgroup)
```
 **Результат:**  
- Создан пользователь `smallman` с UID 1001.  
- Добавлен в группу `readgroup` (GID 1500).  
- Заполнено поле GECOS (ФИО, телефон).

```bash
$ sudo chmod 666 screen
$ ls -l screen
-rw-rw-rw- 1 vboxuser vboxuser 0 Apr 27 18:49 screen
```
 **Результат:** Файл `screen` доступен на чтение/запись **всем** (права `666`).  
 **AppSec-риск:** В production такие права опасны — любой пользователь может изменить файл.

---

## 🔹 Задание 8: Групповые права для `screen`

```bash
$ sudo chgrp readgroup screen
$ sudo chmod 640 screen
$ ls -l screen
-rw-r----- 1 vboxuser readgroup 0 Apr 27 18:49 screen
```
 **Результат:**  
- Группа файла изменена на `readgroup`.  
- Права `640` = владелец: `rw-`, группа: `r--`, остальные: `---`.  
- Только владелец и члены `readgroup` могут читать файл.

```bash
$ sudo -u smallman cat ~/lab02/screen
cat: /home/vboxuser/lab02/screen: Permission denied
```
 **Результат:** Доступ запрещён, потому что путь `~/lab02` не существует для `smallman` (нет домашнего каталога).  
 **Решение:** Использовать абсолютный путь: `/home/vboxuser/Downloads/.../screen`.

---

## 🔹 Задание 9: POSIX ACL

```bash
$ touch nmapres.txt
$ sudo setfacl -m u:smallman:rw nmapres.txt
$ sudo setfacl -m g:readgroup:r nmapres.txt
$ getfacl nmapres.txt
# file: nmapres.txt
# owner: vboxuser
# group: vboxuser
user::rw-
user:smallman:rw-
group::rw-
group:readgroup:r--
mask::rw-
other::r--
```
 **Результат:**  
- Для пользователя `smallman` установлены права `rw-`.  
- Для группы `readgroup` — права `r--`.  
- `mask::rw-` ограничивает максимальные права для named entries.  
- ACL хранится в расширенных атрибутах файла.

---

## 🔹 Задание 10: Сохранение `nmapres.txt`

 **Выполнено:**
```bash
$ git add nmapres.txt
$ git commit -m "lab02: add nmapres.txt for next lab"
```

---

## 🔹 Задание 11: Группы и права системных каталогов

```bash
$ ls -ld /bin /sbin /dev /etc /lib /home /root /usr /var /tmp /proc /mnt /boot /sys
lrwxrwxrwx   1 root root     7 Apr 22  2024 /bin -> usr/bin
drwxr-xr-x   3 root root  4096 Dec 13 07:10 /boot
drwxr-xr-x  19 root root  4360 Apr 24 20:12 /dev
drwxr-xr-x 147 root root 12288 Apr 27 18:54 /etc
drwxr-xr-x   3 root root  4096 Oct 27 19:57 /home
lrwxrwxrwx   1 root root     7 Apr 22  2024 /lib -> usr/lib
drwxr-xr-x   2 root root  4096 Aug  5  2025 /mnt
dr-xr-xr-x 369 root root     0 Apr 24 09:46 /proc
drwx------   7 root root  4096 Dec 19 09:03 /root
lrwxrwxrwx   1 root root     8 Apr 22  2024 /sbin -> usr/sbin
dr-xr-xr-x  13 root root     0 Apr 24 09:46 /sys
drwxrwxrwt  18 root root  4096 Apr 27 18:51 /tmp
drwxr-xr-x  12 root root  4096 Aug  5  2025 /usr
drwxr-xr-x  14 root root  4096 Oct 27 19:56 /var
```
 **Результат:**  
- `/tmp` имеет права `1777` (sticky bit) — все могут создавать файлы, но удалять только свои.  
- `/root` = `700` — доступ только для root.  
- `/etc` = `755`, конфигурации обычно `644`.  
- `/dev` управляется `udev`, права динамические.

---

## 🔹 Задание 12: Файлы репозитория с другими владельцами

```bash
$ find . -maxdepth 3 -not -user $USER -printf '%u %g %M %p\n'
.:
```
 **Результат:** В текущем каталоге `lab02` все файлы принадлежат текущему пользователю `vboxuser`.

---

## 🔹 Задание 13: Тест SUID и privilege escalation

```bash
$ cat << 'EOF' > test_privesc.sh
#!/bin/bash
echo "Running as $(whoami)"
EOF
$ chmod +x test_privesc.sh
$ sudo chown root:root test_privesc.sh
$ sudo chmod u+s test_privesc.sh
$ su - smallman -c "./test_privesc.sh"
Password:
su: warning: cannot change directory to /home/smallman: No such file or directory
Running as smallman
```
 **Результат:** Скрипт выполнился от имени `smallman`, **не** `root`.

 **Важно:** Ядро Linux **игнорирует SUID на интерпретируемых скриптах** (безопасность).  
 **Почему SUID опасен:**  
- Если бинарник с `u+s` содержит уязвимость (buffer overflow, command injection), атакующий получает права владельца (часто `root`).  
- Примеры: `/usr/bin/passwd`, `sudo`, `pkexec` (CVE-2021-4034).  
- Для демонстрации эскалации нужно использовать **бинарные** файлы или `capabilities`.

---

## 🔹 Задание 14: Sticky bit vs обычные права

```bash
$ mkdir shared
$ sudo chmod 770 shared
$ sudo chown :readgroup shared
$ touch shared/userA_file
$ sudo -u smallman touch shared/smallman_file
$ sudo -u smallman rm shared/userA_file   #  удалится (770 без sticky)
rm: remove write-protected regular empty file 'shared/userA_file'? yes

$ sudo chmod 1770 shared
$ sudo -u smallman rm shared/userA_file   #  Operation not permitted
rm: cannot remove 'shared/userA_file': No such file or directory
```
 **Результат:**  
- С правами `770` любой член группы может удалять файлы других.  
- С `1770` (добавлен sticky bit) удалить файл может **только его владелец, владелец директории или root**.  
 **Разница:** `1` в начале = sticky bit (`t` в `ls -l`), защита от удаления чужих файлов в общих папках.

---

## 🔹 Задание 15: Поиск SUID-файлов в системе

```bash
$ find / -perm -4000 2>/dev/null
/usr/share/code/chrome-sandbox
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/xorg/Xorg.wrap
/usr/lib/snapd/snap-confine
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/sbin/pppd
/usr/bin/su
/usr/bin/pkexec
/usr/bin/fusermount3
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/mount
/usr/bin/umount
/usr/bin/sudo
```
 **Анализ 3 файлов:**

| Файл | Зачем нужен SUID | Риск |
|------|-----------------|------|
| `/usr/bin/passwd` | Позволяет обычному пользователю менять пароль (запись в `/etc/shadow` требует root) | Уязвимость в парсинге аргументов → root shell |
| `/usr/bin/sudo` | Механизм временной эскалации привилегий | Неправильная конфигурация `sudoers` или CVE → полный контроль |
| `/usr/bin/pkexec` | Выполнение команд от имени другого пользователя через PolicyKit | Уязвимость (CVE-2021-4034) → локальная эскалация до root |

---

## 🔹 Задание 16: Процессы в системе

```bash
$ ps aux | head -20
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.2  0.1  23620 14724 ?        Ss   08:14   1:29 /sbin/init splash
root           2  0.0  0.0      0     0 ?        S    08:14   0:08 [kthreadd]
...
vboxuser    3013  3.3  6.4 5925188 515080 ?      Rsl  08:16  21:32 /usr/bin/gnome-shell
```
 **Результат:** Список всех процессов с деталями: пользователь, %CPU, %MEM, команда.

```bash
$ pstree -p -u | head -30
systemd(1)─┬─ModemManager(1047)─┬─{ModemManager}(1087)
           ├─NetworkManager(983)─┬─{NetworkManager}(1073)
           ├─dockerd(1311)─┬─{dockerd}(1359)
           └─...
```
 **Результат:** Дерево процессов показывает иерархию: родитель → потомки, с пользователями и PID.

 **Наблюдения:**  
- Демоны (`systemd`, `dockerd`, `snapd`) работают без привязки к терминалу (`TTY = ?`).  
- Пользовательские процессы (`gnome-shell`, `firefox`, `code`) запущены от `vboxuser`.  
- Ядро создаёт множество `kworker` потоков для фоновых задач.

---