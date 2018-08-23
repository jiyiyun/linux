keepalived安装设置
---

keepalived最初是专为LVS负载均衡设计的，后来加入VRRP功能，具有了高可用failover功能，还有健康检查healthcheck功能

- 负载均衡 load blancer
- 健康检查 healthcheck
- 高可用 failover   

1 . 安装keepalived

```txt
[root@master ~]# yum install keepalived
```
建议：安装keepalived依赖

```txt
yum -y install gcc ipvsadm openssl-devel popt-devel kernel-devel
```

2 . 启动keepalived服务并检查(每个keepalived节点都检查)

```txt
[root@controller ~]# systemctl start keepalived
启动keepalived

[root@controller ~]# ps -ef |grep keep|grep -v grep
root      5453     1  0 17:00 ?        00:00:00 /usr/sbin/keepalived -D
root      5454  5453  0 17:00 ?        00:00:00 /usr/sbin/keepalived -D
root      5455  5453  0 17:00 ?        00:00:00 /usr/sbin/keepalived -D

[root@controller ~]# systemctl stop keepalived
测试完毕后关闭keepalived服务
```

keepalived配置文件说明
---
keepalived默认配置文件路径

```txt
[root@block1 ~]# vi /etc/keepalived/keepalived.conf
```
1 . 全局定义(Global Definitions)

这部分主要用来设置keepalive的故障通知机制和Router ID标识

```txt
router_id LVS_DEVEL
一个局域网内Router ID必须的唯一的
```
2 . VRRP定义区块(VRRP instance)

```txt
vrrp_instance VI_1 {
    state MASTER             #Master 和 backup两种状态
    interface eth0           #网络通讯接口，一定要填对
    virtual_router_id 51     #虚拟路由ID，唯一，Master和backup配置相同实例虚路由ID必须一致
    priority 100             #优先级数字越大越优先，Master大于slave
    advert_int 1             #同步时间间隔，默认为1
    authentication {         #认证设置
        auth_type PASS       #认证有PASS和AH(IPSEC)两种，Master和backup必须一样
        auth_pass 1111
    }
    virtual_ipaddress {      #虚IP,绑定的接口和前面interface一致，在实际中要和域名绑定，和高可用服务要监听的IP一致
        192.168.200.16
        192.168.200.17
        192.168.200.18
    }
}
```
12.3高可用服务单实例实战
===

12.3.1 配置keepalived 实现单实例单IP自动漂移接管
---

实际上同时将两个服务器应用同时开启，但是只让有VIP一端的服务器提供服务，宕机后系统自动切换


附录：
---

附录1: keepalive日志问题

keepalived日志默认存放在[root@master ~]# cat /var/log/messages 目录

可以修改让keepalive将日子单独存放在/var/log/keepalive.log

把日志单独存放

修改/etc/sysconfig/keepalived

把KEEPALIVED_OPTIONS="-D" 修改为：KEEPALIVED_OPTIONS="-D -d -S 0"

```txt
KEEPALIVED_OPTIONS="-D -d -S 0"
```
在/etc/rsyslog.conf 末尾添加

```txt
local0.*              /var/log/keepalived.log
```
重启主机验证

```txt
cron                grubby              maillog-20170306    ntpstats/           secure-20170226     tomcat/             
[root@master ~]# tail /var/log/keepalived.log 
Mar 19 18:29:23 master Keepalived_healthcheckers[2023]: SSL handshake/communication error connecting to server (openssl errno: 1) [192.168.100.33]:80.
Mar 19 18:29:23 master Keepalived_healthcheckers[2023]: Removing service [192.168.100.33]:80 from VS [192.168.100.100]:80
Mar 19 18:29:23 master Keepalived_healthcheckers[2023]: Remote SMTP server [127.0.0.1]:25 connected.
Mar 19 18:29:24 master Keepalived_healthcheckers[2023]: SMTP alert successfully sent.
Mar 19 18:29:26 master Keepalived_healthcheckers[2023]: SSL handshake/communication error connecting to server (openssl errno: 1) [192.168.100.23]:80.
Mar 19 18:29:26 master Keepalived_healthcheckers[2023]: Removing service [192.168.100.23]:80 from VS [192.168.100.100]:80
Mar 19 18:29:26 master Keepalived_healthcheckers[2023]: Lost quorum 1-0=1 > 0 for VS [192.168.100.100]:80
Mar 19 18:29:26 master Keepalived_healthcheckers[2023]: Remote SMTP server [127.0.0.1]:25 connected.
Mar 19 18:29:26 master Keepalived_healthcheckers[2023]: SMTP alert successfully sent.
Mar 19 18:29:26 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) Sending gratuitous ARPs on ens32 for 192.168.100.100
[root@master ~]# 
```

附录2： 可以ping通，但是没有数据

```txt
Microsoft Windows [版本 6.3.9600]
(c) 2013 Microsoft Corporation。保留所有权利。

C:\Users\GoodLuck>ping 192.168.100.100

正在 Ping 192.168.100.100 具有 32 字节的数据:
来自 192.168.100.100 的回复: 字节=32 时间<1ms TTL=64
来自 192.168.100.100 的回复: 字节=32 时间=1ms TTL=64

192.168.100.100 的 Ping 统计信息:
    数据包: 已发送 = 2，已接收 = 2，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 0ms，最长 = 1ms，平均 = 0ms

[root@master ~]# ping 192.168.100.100
PING 192.168.100.100 (192.168.100.100) 56(84) bytes of data.
64 bytes from 192.168.100.100: icmp_seq=1 ttl=64 time=0.042 ms
64 bytes from 192.168.100.100: icmp_seq=2 ttl=64 time=0.035 ms
^C
--- 192.168.100.100 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.035/0.038/0.042/0.007 ms
[root@master ~]# 


每个web单节点都可以访问
[root@master ~]# curl 192.168.100.23
<head>This is 100.23</head>
[root@master ~]# curl 192.168.100.33
<head>This is 100.33</head>

但是curl虚IP不行，报错

[root@master ~]# curl 192.168.100.100:80
curl: (7) Failed connect to 192.168.100.100:80; Connection refused
[root@master ~]# curl 192.168.100.100
curl: (7) Failed connect to 192.168.100.100:80; Connection refused
[root@master ~]# 

```txt
[root@master ~]# tail -f /var/log/messages   #查看日志文件文件尽量用tail命令，因为有的日志文件很大，翻页很费时间
Mar 19 19:01:15 master kernel: e1000: ens32 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: None
Mar 19 19:01:15 master NetworkManager[662]: <info>  [1489921275.6267] device (ens32): link connected
Mar 19 19:01:16 master Keepalived_healthcheckers[2023]: Timeout connect, timeout server [192.168.100.33]:80.
Mar 19 19:01:18 master Keepalived_vrrp[2024]: Kernel is reporting: interface ens32 UP
Mar 19 19:01:18 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) Transition to MASTER STATE
Mar 19 19:01:19 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) Entering MASTER STATE
Mar 19 19:01:19 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) setting protocol VIPs.
Mar 19 19:01:19 master Keepalived_healthcheckers[2023]: Netlink reflector reports IP 192.168.100.100 added
Mar 19 19:01:19 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) Sending gratuitous ARPs on ens32 for 192.168.100.100
Mar 19 19:01:24 master Keepalived_vrrp[2024]: VRRP_Instance(VI_1) Sending gratuitous ARPs on ens32 for 192.168.100.100
```

报错分析：

可以ping通但是网页转发有问题，web转发设置需要重新检查
```

附录3:检测http端故障的脚本(keepalived默认检测是的另一个keepalive端有没有存活，没有检测http端的机制，需要脚本检测http节点是否存活)

```txt
#!/bin/bash
#       QQ:752119102
while true
do
       httpdpid=`ps -C httpd  --no-heading  |wc -l`
       if [ $httpdpid -eq 0 ];then
               /etc/init.d/httpd  start
               sleep 5
               httpdpid=`ps -C httpd  --no-heading  |wc -l`
               if [ $httpdpid -eq 0 ];then
                       /etc/init.d/keepalive stop
               fi
       fi
       sleep 5
done
```
参考资料
---

- 跟老男孩学Linux运维
- Linux 高可用（HA）集群之keepalived详解 http://freeloda.blog.51cto.com/2033581/1280962
- http://blog.csdn.net/kkdelta/article/details/39433137
- Keepalived日志 http://www.cnblogs.com/zzzhfo/p/6070575.html
- http://atong.blog.51cto.com/2393905/1351479








