keeplived安装设置
---

keeplived最初是专为LVS负载均衡设计的，后来加入VRRP功能，具有了高可用failover功能，还有健康检查healthcheck功能

- 负载均衡 load blancer
- 健康检查 healthcheck
- 高可用 failover   

1 . 安装keepalived

```txt
[root@master ~]# yum install keepalived
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



参考资料
---

- 跟老男孩学Linux运维











