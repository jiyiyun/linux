Keepalived+MySQL双机热备
===

关于mysql 双备在 database/mysql 相关专栏

keeplived最初是专为LVS负载均衡设计的，后来加入VRRP功能，具有了高可用failover功能，还有健康检查healthcheck功能

- 负载均衡 load blancer
- 健康检查 healthcheck
- 高可用 failover   

安装keepalived

```txt
[root@master ~]# yum install keepalived -y
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

lb算法

lb_algo rr|wrr|lc|wlc|sh|dh|lblc

Round-robin（轮循）、Weight-round-robin（带权轮循）

lb种类

lb_kind NAT|DR|TUN

NB: Type “path” refers to the full path of the script being called. Note that for scripts requiring
arguments the path and arguments must be enclosed in double quotes (“).


配置实例：

```txt
vrrp_instance VI_1 { 
    state BACKUP                #都修改成BACKUP 
    interface eth0 
    virtual_router_id 60        #默认51 主从都修改为60 
    priority 100                #在mysql-ha2上LVS上修改成80 
    advert_int 1 
    nopreempt                   #不抢占资源，意思就是它活了之后也不会再把主抢回来 
    authentication { 
    auth_type PASS 
    auth_pass 1111 
    } 
virtual_ipaddress { 
    192.168.5.55 
    } 
} 
##################第二部分################### 
virtual_server 192.168.5.55 3306 { 
    delay_loop 6 
    lb_algo wrr 
    lb_kind DR 
    nat_mask 255.255.255.0 
    persistence_timeout 50 
    protocol TCP 
 real_server 192.168.5.234 3306 { 
    weight 1 
    notify_down /usr/local/mysql/bin/mysql.sh 
    TCP_CHECK { 
        connect_timeout 10 
        nb_get_retry 3 
        connect_port 3306 
        } 
    } 
}
```

创建终止脚本

```txt
[root@keepalive_master ~]# vi /etc/keepalived/mysql.sh

#/bin/bash
killall -9 keepalived
```



keepalived健康检查 HTTP_GET

```txt
一：
real_server 192.168.2.188 80 {
     weight 1
     HTTP_GET {
       url {
       path /index.html
       digest bfaa334fdd71444e45eca3b7a1679a4a  #http://192.168.2.188/index.html的digest值          }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }
digest值的获取方法：
[root@188-test html]# genhash -s 192.168.2.188 -p 80 -u /index.html
MD5SUM = bfaa334fdd71444e45eca3b7a1679a4a
genhash命令：
[root@188-test html]# genhash
genhash v1.0.0 (18/11, 2002)
Usage:
  genhash -s server-address -p port -u url
  genhash -S -s server-address -p port -u url
  genhash -h
  genhash -r

Commands:
Either long or short options are allowed.
  genhash --use-ssl         -S       Use SSL connection to remote server.
  genhash --server          -s       Use the specified remote server address.
  genhash --port            -p       Use the specified remote server port.
  genhash --url             -u       Use the specified remote server url.
  genhash --use-virtualhost -V       Use the specified virtualhost in GET query.
  genhash --verbose         -v       Use verbose mode output.
  genhash --help            -h       Display this short inlined help screen.
  genhash --release         -r       Display the release number
```

二：

```txt
real_server 192.168.2.188 80 {
      weight 1
      HTTP_GET {
          url {
          path /index.html
          status_code 200      #http://192.168.2.188/index.html的返回状态码
            }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }
```

参考文章
---

- 跟老男孩学Linux运维
- MySQL高可用性之Keepalived+MySQL（双主热备） http://www.linuxidc.com/Linux/2015-06/118767.htm
- Linux下Keepalived+MySQL实现高可用 http://www.linuxidc.com/Linux/2013-10/91685.htm
- http://blog.sina.com.cn/s/blog_4f9fc6e10102w6xy.html
- Linux 高可用（HA）集群之keepalived详解 http://freeloda.blog.51cto.com/2033581/1280962
- MySQL + keepalived （CentOS7）高可用方案 http://blog.csdn.net/cjfeii/article/details/48623079
- http://blog.csdn.net/jibcy/article/details/7872127
- http://www.keepalived.org/pdf/UserGuide.pdf