soar默认是以字符型排序的，要按数字排序使用参数-n
---
``` shell
richard@rich:~$ sort test.log 

-10
-1.5
21
212
35343434
43
54
6
-65
8.5
9999
richard@rich:~$ sort -n test.log 
-65
-10
-1.5

6
8.5
21
43
54
212
9999
35343434
```
``` shell
-b  排序时忽略前面的空格
-M  --month-sort 按月份排序
-n  --numeric-sort 按数值排序
-r  --reverse 反转排序
-f  --ignore-case忽略大小写
-t  --field-separator=SEP 指定区分关键位置的字符
-k  --key=POS1,[POS2]根据POS1位置排序，并在POS2结束
```
示例
---
``` shell
richard@rich:~$ sort -t ':' -k 3 -n /etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
```
``` shell
richard@rich:~$ du -sh * |sort -nr
748K	test
208K	python
12K	examples.desktop
4.0K	Videos
4.0K	test.log
4.0K	Templates
4.0K	sources.list
4.0K	Public
4.0K	Pictures
4.0K	Music
4.0K	Downloads
4.0K	Documents
4.0K	Desktop
4.0K	apt.conf
```