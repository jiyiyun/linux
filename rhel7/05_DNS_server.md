DNS服务器的设置
---
BIND Berkeley Internet Name Domain

主要配置文件
---
- /etc/hosts   主机的一个列表文件，

``` shell
# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	userver16
```
- /etc/host.conf   转换程序控制文件

``` shell
# cat /etc/host.conf 
# The "order" line is only used by old versions of the C library.
order hosts,bind
multi on
```
- /etc/resolv.conf  #配置程序在请求BIND域名查询主机时，告诉主机域名服务器和IP地址
- /etc/named.conf   #BIND主文件
- /var/named/localhost.zone      #localhost正向域名解析文件
- /var/named/name.local          #localhost区反向域名解析文件
- /etc/named/rfc1912.zones       #区块设置文件
- /var/named/localdomin.zone     #正向解析模板

DNS资源记录格式
---
1. name
2. type
3. rdata
