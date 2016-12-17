NTP工作模式
1. Broadcast/Multicast
2. Client/Server
3. Broadcast

use UDP协议，使用123号端口
国内NTP服务器地址
1. time.buptnet.edu.cn
2. slb.time.edu.cn
3. slc.time.edu.cn
4. sld.time.edu.cn

1、安装、相关配置文件
---
``` shell
# yum -y install ntp
```
``` shell
# cat /etc/ntp.conf   //NTP的主要配置文件
# By default, exchange time with everybody, but don't allow configuration.
restrict -4 default kod notrap nomodify nopeer noquery limited
restrict -6 default kod notrap nomodify nopeer noquery limited

# Local users may interrogate the ntp server more closely.
restrict 127.0.0.1
restrict ::1

# Needed for adding pool entries
restrict source notrap nomodify noquery

# Clients from this (example!) subnet have unlimited access, but only if
# cryptographically authenticated.
#restrict 192.168.123.0 mask 255.255.255.0 notrust


# If you want to provide time to your local subnet, change the next line.
# (Again, the address is an example only.)
#broadcast 192.168.123.255
```
``` shell
# cat /usr/share/zoneinfo/     //目录，规定了主要时区的配置文件
Africa/            Egypt              Hongkong           Mexico/            ROC
Antarctica/        EST                Iceland            MST7MDT            Singapore
Asia/              Etc/               Iran               NZ                 Turkey
Atlantic/          Europe/            iso3166.tab        NZ-CHAT            UCT
Brazil/            GB                 Jamaica            Poland             US/
Canada/            GB-Eire            Japan              Portugal           UTC
```
``` shell
系统默认是没有这个文件，需要创建
# cat /etc/sysconfig/clock
```
``` shell
# cat /etc/localtime   //本地系统时间配置文件。如果clock文件规定了时间为/usr/share/zoneinfo/Asia/Shanghai 则系统会将Shanhai这个文件复制一份到/etc/localtime,系统时间会以Shanhai为准
```
2.NTP服务器端配置文件/etc/ntp.conf
---
``` shell
restrict IP地址mask子网掩码参数    //restrict提供权限

1. ignore 关闭所有联机服务。    
2.nomodify客户端不能更改服务器端时间参数，只可校对。  
3.notrust 客户端要通过认证   
4.noquery 不提供查询
不设置，表示该IP地址、子网没有任何限制
``` shell
server IP地址或域名[prefer]     //使用server参数设置上级时间服务器
```
3、配置示例
---
``` shell
restrict 192.168.100.0 mask 255.255.255.0    #允许192.168.100.0/24网段访问
restrict 10.0.0.0 mask 255.0.0.0 nomodify    #添加10.0.0.0/8网段，不可更改服务器时间参数

server 202.112.128.33 prefer
server 202.112.10.60

driftfile /var/lib/ntp/drift
keys /etc/ntp/keys        #给客户端设置认证信息，不修改
```
4. 开机启动
---
``` shell
# systemctl start ntp
# systemctl enable ntp
```
5.打开iptables和防火墙123端口
---
```
# iptables -A INPUT -p UDP -i eth0 -s 192.168.0.0/24 --dport 123 -j ACCEPT
```
``` shell
Either long or short options are allowed.
  --append  -A chain		Append to chain
  --check   -C chain		Check for the existence of a rule
  --delete  -D chain		Delete matching rule from chain
  --delete  -D chain rulenum
				Delete rule rulenum (1 = first) from chain
  --insert  -I chain [rulenum]
				Insert in chain as rulenum (default 1=first)
  --replace -R chain rulenum
				Replace rule rulenum (1 = first) in chain
  --list    -L [chain [rulenum]]
				List the rules in a chain or all chains
  --list-rules -S [chain [rulenum]]
				Print the rules in a chain or all chains
  --flush   -F [chain]		Delete all rules in  chain or all chains
  --zero    -Z [chain [rulenum]]
				Zero counters in chain or all chains
  --new     -N chain		Create a new user-defined chain
  --delete-chain
            -X [chain]		Delete a user-defined chain
  --policy  -P chain target
				Change policy on chain to target
  --rename-chain
            -E old-chain new-chain
				Change chain name, (moving any references)
Options:
    --ipv4	-4		Nothing (line is ignored by ip6tables-restore)
    --ipv6	-6		Error (line is ignored by iptables-restore)
[!] --protocol	-p proto	protocol: by number or name, eg. `tcp'
[!] --source	-s address[/mask][...]
				source specification
[!] --destination -d address[/mask][...]
				destination specification
[!] --in-interface -i input name[+]
				network interface name ([+] for wildcard)
 --jump	-j target
				target for rule (may load target extension)
  --goto      -g chain
                              jump to chain with no return
  --match	-m match
```
``` shell
防火墙设置允许ntp 服务，并重启
# firewall-cmd --add-service=ntp --permanent
success
# firewall-cmd --reload
success
```
``` shell
selinux 设置
# setsebool -P ntpd_disable_trans 1

# vi /etc/sysconfig/ntpd
SYNC_HWCLOCK=yes     #允许BIOS与系统时间同步

# vi /etc/ntp/step-tickers
192.168.0.254     #当ntp 服务启动时，会自动与该文件记录的上层ntp服务器进行时间校正
```
5. 查看ntp服务工作情况
---
``` shell
# netstat -tlunp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 127.0.0.1:123           0.0.0.0:*                           1625/ntpd       
udp        0      0 0.0.0.0:123             0.0.0.0:*                           1625/ntpd

# ntpstat
# ntptrace -n 127.0.0.1
127.0.0.1: stratum 3, offset -0.069974, synch distance 0.410159

# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
-91.189.91.157   132.246.11.231   2 u 1223  256   20  502.545   40.355 480.912
*211.233.84.186  204.123.2.5      2 u  450  256  316   82.742  -191.88 212.511
+timpany.srv.jre 133.243.238.163  2 u  397  256  222  108.867  -98.866 282.272
+82.200.209.236  89.109.251.22    2 u  864  256  230  306.659  -179.05 183.481
 news.neu.edu.cn 202.118.1.47     2 u 1236  256  120  188.885  -126.77 5680.53
```
- * 响应最精准的服务器
- + 响应这个查询请求的服务器
- refid NTP服务器使用更高一级服务器的名称
- st 正在响应请求的服务器级别
- when 上一次成功请求到现在的秒数
- poll 当前请求的时钟间隔秒数
- offset 时间偏移量，单位毫秒ms

3.3 客户端设置
---
``` shell
# ntpdate 192.168.0.253  #ntpdate NTP server IP
# hwclock -w             #写入BIOS

编辑 /etc/crotab 加入一行
30 8 * * * root /usr/sbin/ntpdate 192.168.0.253 ; /sbin/hwclock -w #192.168.0.253是NTP 服务器地址

重启
# service crond restart
Redirecting to /bin/systemctl restart  crond.service
```