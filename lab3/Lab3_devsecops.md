 
 Данная лабораторная работа посвещена изучению `nmap` и как с ним работать. Лабораторная работа - подпорка для старта в выявлении и определении уязвимостей на уровне сканера портов, что бы освоить базовые методы сканирования.

  **Структура проекта:** 
  ```bash 
├── lab3
│   ├── Lab3_devsecops.md
│   └── reports
│       ├── nmapres_new.html
│       ├── nmapres_new.txt
│       ├── nmapres_new.xml
│       └── nmapres.txt

  ```
---
## Теория: 

**Nmap** — open-source утилита для разведки и анализа сетей. Основная цель — выявление:
- активных устройств,
- открытых портов,
- работающих сервисов и их версий,
- ОС (через fingerprinting),
- характеристик сети (фаерволы, фрагментация и др.).

Фактически — «виртуальная сетевая карта».
### Методы сканирования
- **TCP Connect** (`-sT`)  
- **TCP SYN (Stealth)** (`-sS`)  
- **UDP Scan** (`-sU`)  
- **FIN / NULL / Xmas** (`-sF`, `-sN`, `-sX`) — обход фаерволов  
- **ACK Scan** (`-sA`) — анализ фильтрации  
- **Idle (Zombie) Scan** (`-sI`) — анонимное сканирование  
- **ICMP Ping** (`-PE`)  
- **TCP/UDP Ping** (`-PS`, `-PA`, `-PU`)  
- **FTP Bounce**, **SCTP**, и др.
###  Ключевые возможности
- **OS fingerprinting** — определение ОС по отпечатку TCP/IP-стека  
- **Service/version detection** (`-sV`) — баннеры, версии ПО  
- **NSE (Nmap Scripting Engine)** — автоматизация поиска уязвимостей (SQLi, CVE и др.)  
- **Обход обнаружения**: фрагментация (`-f`), ложные IP (`-D`), изменение темпа (`-T[0-5]`)  
- **Гибкое управление DNS, трассировкой, интерфейсами**  
- Поддержка массового сканирования (`-iL`, CIDR)
### Основные флаги
| Флаг            | Назначение                                   |
| --------------- | -------------------------------------------- |
| `-sn`           | Ping scan (без портов)                       |
| `-Pn`           | Считать все хосты онлайн                     |
| `-sL`           | List scan (без отправки пакетов)             |
| `-A`            | Агрессивный режим: `-O -sV -sC --traceroute` |
| `-O`            | Определение ОС                               |
| `-sV`           | Версии сервисов                              |
| `--script=vuln` | Поиск уязвимостей через NSE                  |
### Распространённые порты
| Порт | Сервис | Протокол |
|------|--------|----------|
| 20/21 | FTP | TCP |
| 22    | SSH | TCP |
| 23    | Telnet | TCP |
| 25    | SMTP | TCP |
| 53    | DNS | TCP/UDP |
| 67/68 | DHCP | UDP |
| 69    | TFTP | UDP |
| 80    | HTTP | TCP |
| 110   | POP3 | TCP |
| 443   | HTTPS | TCP |
| 3306  | MySQL | TCP |

---

## Задание
1. Опишите используемые методы по их назначению, как они функционируют и какие результаты могут дать для оценки. Используйте сноску из материалов выше по флагам команд.
 2. Выведите на терминале и проанализируйте следующие команды консоли
```bash
$ nmap localhost
$ nmap -sC localhost

$ nmap -p localhost
$ nmap -O localhost

$ nmap -p 80 localhost
$ nmap -p 443 localhost
$ nmap -p 8443 localhost
$ nmap -p "*" localhost
$ nmap -sV -p 22,8080 localhost

$ nmap -sP 192.168.1.0/24
$ nmap --open 192.168.1.1
$ nmap --packet-trace 192.168.1.1
$ nmap --packet-trace scanme.nmap.org 
$ nmap --iflist

$ nmap -iL scanme.nmap.org 
$ nmap -A -iL scanme.nmap.org 
$ nmap -sA scanme.nmap.org
$ nmap -PN scanme.nmap.org 

$ nmap --script=vuln IP_addr -vv
$ nmap -sV --script vuln -oN nmapres_new.txt localhost
$ cat > ./nmapres_new.txt # сделать подобный пример файлу exmp_targets.txt
$ grep "VULNERABLE" nmapres_new.txt

$ mkdir -p ~/project/reports
$ nmap -sV -p 8080 --script vuln -oN ~/project/reports/nmapres_new.txt -oX ~/project/reports/nmapres_new.xml localhost
$ xsltproc ~/project/reports/nmapres_new.xml -o ~/project/reports/nmapres_new.html
```
3. Используйте команду `tree` и выведите все вложенные файлы по директориям.
 4. Найдите IP сетевой карты `Ethernet`, которая соответствует вашей виртуальной машине используя `ifconfig` и выполните команду

```shell
$ nmap -sP inet_addr
```

5. Определите ОС, данные ssh, telnet  с помощью `nmap` и выведитео них информацию.
6. Результаты из `nmapres_new.txt` надо перенести в `nmapres.txt` и оставить оба файла рядом в локальном репозитории. Желательно использовать `cp` в консоли через редактор.
7. Оформить `README.md` по аналогии и использовать `shield`, etc.
8. Составить `gist` отчет и отправить ссылку личным сообщением
----
## Выполнение задания:
- [x]  1. Опишите используемые методы по их назначению, как они функционируют и какие результаты могут дать для оценки. Используйте сноску из материалов выше по флагам команд.

 - [x]  2. Выведите на терминале и проанализируйте следующие команды консоли
```bash

# Базовое сканирование localhost
$ nmap localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 14:54 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000032s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
Not shown: 999 closed tcp ports (conn-refused)
PORT    STATE SERVICE
631/tcp open  ipp
Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds

# Сканирование с запуском default-скриптов
$ nmap -sC localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:02 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000033s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
Not shown: 999 closed tcp ports (conn-refused)
PORT    STATE SERVICE
631/tcp open  ipp
|_ssl-date: TLS randomness does not represent time
| http-robots.txt: 1 disallowed entry 
|_/
| ssl-cert: Subject: commonName=ubuntu/organizationName=ubuntu/stateOrProvinceName=Unknown/countryName=US
| Subject Alternative Name: DNS:ubuntu, DNS:ubuntu.local, DNS:localhost
| Not valid before: 2025-12-11T15:02:29
|_Not valid after:  2035-12-09T15:02:29
|_http-title: Home - CUPS 2.4.7
Nmap done: 1 IP address (1 host up) scanned in 1.67 seconds

# Нет порта — ошибка
$ nmap -p localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:03 UTC
Found no matches for the service mask 'localhost' and your specified protocols
QUITTING!

# Определение ОС
$ nmap -O localhost

# Сканирование конкретных портов
$ nmap -p 80 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:05 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000046s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
PORT   STATE  SERVICE
80/tcp closed http
Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds


$ nmap -p 443 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:05 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0010s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
PORT    STATE  SERVICE
443/tcp closed https
Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds

$ nmap -p 8443 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:06 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00018s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
PORT     STATE  SERVICE
8443/tcp closed https-alt
Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds


# Сканирование ВСЕХ портов (1–65535)
$ nmap -p "*" localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:06 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00011s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain
Not shown: 8376 closed tcp ports (conn-refused)
PORT    STATE SERVICE
631/tcp open  ipp
Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds


# Сканирование версий на портах 22 и 8080
$ nmap -sV -p 22,8080 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:06 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00013s latency).
Other addresses for localhost (not scanned): ::1
rDNS record for 127.0.0.1: localhost.localdomain

PORT     STATE  SERVICE    VERSION
22/tcp   closed ssh
8080/tcp closed http-proxy

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.12 seconds


#Ping-scan всей подсети
$ nmap -sP 192.168.1.0/24

# Показать ТОЛЬКО открытые порты у хоста
$ nmap --open 192.168.1.1

# трассировка пакетов
$ nmap --packet-trace 192.168.1.1
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:07 UTC
CONN (0.0188s) TCP localhost > 192.168.1.1:80 => Operation now in progress
CONN (0.0190s) TCP localhost > 192.168.1.1:443 => Operation now in progress
CONN (2.0225s) TCP localhost > 192.168.1.1:443 => Operation now in progress
CONN (2.0228s) TCP localhost > 192.168.1.1:80 => Operation now in progress


$ nmap --packet-trace scanme.nmap.org 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:07 UTC
CONN (0.0230s) TCP localhost > 45.33.32.156:80 => Operation now in progress
CONN (0.0231s) TCP localhost > 45.33.32.156:443 => Operation now in progress
CONN (0.1974s) TCP localhost > 45.33.32.156:80 => Connected
NSOCK INFO [0.1970s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.1970s] nsock_connect_udp(): UDP connection requested to 127.0.0.53:53 (IOD #1) EID 8
NSOCK INFO [0.1970s] nsock_read(): Read request from IOD #1 [127.0.0.53:53] (timeout: -1ms) EID 18
NSOCK INFO [0.1970s] nsock_write(): Write request for 43 bytes to IOD #1 EID 27 [127.0.0.53:53]


# Показать доступные сетевые интерфейсы
$ nmap --iflist


# `-iL` требует файла, а не домена
$ nmap -iL scanme.nmap.org
$ nmap -A -iL scanme.nmap.org 


# ACK-сканирование scanme.nmap.org (проверка фаервола) 
$ nmap -sA scanme.nmap.org

# Считать хост онлайн, игнорируя ping //-Pn
$ nmap -PN scanme.nmap.org 

# Поиск уязвимостей на IP
$ nmap --script=vuln IP_addr -vv

# Сканирование localhost с выводом в файлы
$ nmap -sV --script vuln -oN nmapres_new.txt localhost

# Анализ результата + сделать подобный пример файлу exmp_targets.txt
$ cat > ./nmapres_new.txt 
$ grep "VULNERABLE" nmapres_new.txt

$ mkdir -p ~/project/reports
$ nmap -sV -p 8080 --script vuln -oN ~/project/reports/nmapres_new.txt -oX ~/project/reports/nmapres_new.xml localhost
$ xsltproc ~/project/reports/nmapres_new.xml -o ~/project/reports/nmapres_new.html
```

3. Используйте команду `tree` и выведите все вложенные файлы по директориям.
```bash 
$ tree 
.
└── reports
    ├── nmapres_new.html
    ├── nmapres_new.txt
    └── nmapres_new.xml

2 directories, 3 files

```

 4. Найдите IP сетевой карты `Ethernet`, которая соответствует вашей виртуальной машине используя `ifconfig` и выполните команду
 ```bash
 $ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:1e:04:b5 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 69329sec preferred_lft 69329sec
    inet6 fd17:625c:f037:2:9dd7:8315:bd98:b526/64 scope global temporary dynamic 
       valid_lft 86295sec preferred_lft 14295sec
    inet6 fd17:625c:f037:2:a00:27ff:fe1e:4b5/64 scope global dynamic mngtmpaddr 
       valid_lft 86295sec preferred_lft 14295sec
    inet6 fe80::a00:27ff:fe1e:4b5/64 scope link 
       valid_lft forever preferred_lft forever


$ nmap -sP 10.0.2.0/24
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:25 UTC
Nmap scan report for ubuntu (10.0.2.15)
Host is up (0.0045s latency).
Nmap done: 256 IP addresses (1 host up) scanned in 2.78 seconds

 ```

5. Определите ОС, данные ssh, telnet  с помощью `nmap` и выведитео них информацию.

```bash 
$ nmap -sT -sV -p 22,23 127.0.0.1
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-11 15:26 UTC
Nmap scan report for localhost.localdomain (127.0.0.1)
Host is up (0.000064s latency).

PORT   STATE  SERVICE VERSION
22/tcp closed ssh
23/tcp closed telnet

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds

```
Результат:  
    Порт 22/tcp (SSH) — закрыт  
    Порт 23/tcp (Telnet) — закрыт  
    На localhost не запущены SSH- и Telnet-серверы.  
    ОС не определена — ограничение среды (отсутствие raw-socket доступа). 
    
- [x]  6. Результаты из `nmapres_new.txt` надо перенести в `nmapres.txt` и оставить оба файла рядом в локальном репозитории. Желательно использовать `cp` в консоли через редактор.
 ```shell 
 $ cp ~/devsecops/lab3/reports/nmapres_new.txt ~/devsecops/lab3/reports/nmapres.txt

 $ ls -la ~/devsecops/lab3/reports/
total 32
drwxrwxr-x 2 vboxuser vboxuser 4096 Dec 11 15:30 .
drwxrwxr-x 3 vboxuser vboxuser 4096 Dec 11 15:16 ..
-rw-rw-r-- 1 vboxuser vboxuser 8792 Dec 11 15:20 nmapres_new.html
-rw-rw-r-- 1 vboxuser vboxuser  601 Dec 11 15:16 nmapres_new.txt
-rw-rw-r-- 1 vboxuser vboxuser 1662 Dec 11 15:16 nmapres_new.xml
-rw-rw-r-- 1 vboxuser vboxuser  601 Dec 11 15:30 nmapres.txt

 ```
- [x]  7. Оформить `README.md` по аналогии и использовать `shield`, etc.
- [x]  8. Составить `gist` отчет и отправить ссылку личным сообщением
