OpenSuSE网络配置
----
最小版安装，带x-window界面,安装好后网卡eth0没有启动，cd /etc/sysconfig/network/，无ifcfg-eth0文件，复制ifcfg-loo重命名为ifcfg-eth0

一、修改ifcfg-eth0文件（修改如下参数即可）
---
``` shell
# vi /etc/sysconfig/network/ifcfg-eth0
BOOTPROTO=static
IPADDR=192.168.0.100
NETMASK=255.255.255.0
```
二、配置网关（路由）
---
``` shell
# vi /etc/sysconfig/network/routes
default 192.168.0.1
```
三、配置DNS
---
``` shell
# vi /etc/resolv.conf
nameserver 223.5.5.5
nameserver 114.114.114.114
```