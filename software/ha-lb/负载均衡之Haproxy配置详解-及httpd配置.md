负载均衡之Haproxy配置详解（及httpd配置）
---

下图描述了使用keepalived+Haproxy主从配置来达到能够针对前段流量进行负载均衡到多台后端web1、web2、web3、img1、img2.但是由于haproxy会存在单点故障问题，因此使用keepalived来实现对Haproxy单点问题的高可用处理。

![p1](http://img.blog.csdn.net/tantexian747FFD3C4F5D479A8AD84C244C78CB34)

常用开源软件负载均衡器有：Nginx、LVS、Haproxy。


三大主流软件负载均衡器对比(LVS VS Nginx VS Haproxy)

LVS：
---

```txt
1、抗负载能力强。抗负载能力强、性能高，能达到F5硬件的60%；对内存和cpu资源消耗比较低
2、工作在网络4层，通过vrrp协议转发（仅作分发之用），具体的流量由linux内核处理，因此没有流量的产生。
2、稳定性、可靠性好，自身有完美的热备方案；（如：LVS+Keepalived）
3、应用范围比较广，可以对所有应用做负载均衡；
4、不支持正则处理，不能做动静分离。
5、支持负载均衡算法：rr（轮循）、wrr（带权轮循）、lc（最小连接）、wlc（权重最小连接）
6、配置 复杂，对网络依赖比较大，稳定性很高。
```

Ngnix：
---

```txt
1、工作在网络的7层之上，可以针对http应用做一些分流的策略，比如针对域名、目录结构；
2、Nginx对网络的依赖比较小，理论上能ping通就就能进行负载功能；
3、Nginx安装和配置比较简单，测试起来比较方便；
4、也可以承担高的负载压力且稳定，一般能支撑超过1万次的并发；
5、对后端服务器的健康检查，只支持通过端口来检测，不支持通过url来检测。
6、Nginx对请求的异步处理可以帮助节点服务器减轻负载；
7、Nginx仅能支持http、https和Email协议，这样就在适用范围较小。
8、不支持Session的直接保持，但能通过ip_hash来解决。、对Big request header的支持不是很好，
9、支持负载均衡算法：Round-robin（轮循）、Weight-round-robin（带权轮循）、Ip-hash（Ip哈希）
10、Nginx还能做Web服务器即Cache功能。
```

HAProxy的特点是：
---

```txt
1、支持两种代理模式：TCP（四层）和HTTP（七层），支持虚拟主机；
2、能够补充Nginx的一些缺点比如Session的保持，Cookie的引导等工作
3、支持url检测后端的服务器出问题的检测会有很好的帮助。
4、更多的负载均衡策略比如：动态加权轮循(Dynamic Round Robin)，加权源地址哈希(Weighted Source Hash)，加权URL哈希和加权参数哈希(Weighted Parameter Hash)已经实现
5、单纯从效率上来讲HAProxy更会比Nginx有更出色的负载均衡速度。
6、HAProxy可以对Mysql进行负载均衡，对后端的DB节点进行检测和负载均衡。
9、支持负载均衡算法：Round-robin（轮循）、Weight-round-robin（带权轮循）、source（原地址保持）、RI（请求URL）、rdp-cookie（根据cookie）
10、不能做Web服务器即Cache。
```
三大主流软件负载均衡器适用业务场景：

1、网站建设初期，可以选用Nigix/HAproxy作为反向代理负载均衡（或者流量不大都可以不选用负载均衡），因为其配置简单，性能也能满足一般的业务场景。如果考虑到负载均衡器是有单点问题，可以采用Nginx+Keepalived/HAproxy+Keepalived避免负载均衡器自身的单点问题。

2、网站并发达到一定程度之后，为了提高稳定性和转发效率，可以使用LVS、毕竟LVS比Nginx/HAproxy要更稳定，转发效率也更高。不过维护LVS对维护人员的要求也会更高，投入成本也更大。

注：Niginx与Haproxy比较：Niginx支持七层、用户量最大，稳定性比较可靠。Haproxy支持四层和七层，支持更多的负载均衡算法，支持session保存等。具体选型看使用场景，目前来说Haproxy由于弥补了一些Niginx的缺点用户量也不断在提升

衡量负载均衡器好坏的几个重要因素： 

```txt
1、会话率 ：单位时间内的处理的请求数  
2、会话并发能力：并发处理能力  
3、数据率：处理数据能力  
经过官方测试统计，haproxy  单位时间处理的最大请求数为20000个，可以同时维护40000-50000个并发连接，最大数据处理能力为10Gbps。综合上述，haproxy是性能优越的负载均衡、反向代理服务器。
```

总结HAProxy主要优点：

```txt
一、免费开源，稳定性也是非常好，这个可通过我做的一些小项目可以看出来，单Haproxy也跑得不错，稳定性可以与LVS相媲美；
二、根据官方文档，HAProxy可以跑满10Gbps-New benchmark of HAProxy at 10 Gbps using Myricom's 10GbE NICs (Myri-10G PCI-Express)，这个作为软件级负载均衡，也是比较惊人的；
三、HAProxy可以作为MySQL、邮件或其它的非web的负载均衡，我们常用于它作为MySQL(读)负载均衡；
四、自带强大的监控服务器状态的页面，实际环境中我们结合Nagios进行邮件或短信报警，这个也是我非常喜欢它的原因之一；
五、HAProxy支持虚拟主机。
```
本次使用环境：

```txt
环境centos7.1
Haproxy 1.5.4
Haproxy+keeplived  172.31.2.31
Haproxy+keeplived  172.31.2.32
```

文本部分：

```txt
global                                            # 全局参数的设置
    log         127.0.0.1 local2                  # log语法：log <address_1>[max_level_1] # 全局的日志配置，使用log关键字，
                                                    指定使用127.0.0.1上的syslog服务中的local0日志设备，记录日志等级为info的日志
    chroot      /var/lib/haproxy                  #改变当前工作目录
    pidfile     /var/run/haproxy.pid              #当前进程id文件
    maxconn     4000                              #最大连接数
    user        haproxy                           #所属用户
    group     haproxy                             #所属组
    daemon                                        #以守护进程方式运行haproxy
    stats socket /var/lib/haproxy/stats
defaults
    mode                    http                  #默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
    log                        global             #应用全局的日志配置
    option                  httplog               # 启用日志记录HTTP请求，默认haproxy日志记录是不记录HTTP请求日志
                                                                 
    option                  dontlognull          # 启用该项，日志中将不会记录空连接。所谓空连接就是在上游的负载均衡器
                                                  或者监控系统为了探测该 服务是否存活可用时，需要定期的连接或者获取某
                                                  一固定的组件或页面，或者探测扫描端口是否在监听或开放等动作被称为空连接；
                                                  官方文档中标注，如果该服务上游没有其他的负载均衡器的话，建议不要使用
                                                  该参数，因为互联网上的恶意扫描或其他动作就不会被记录下来
    option http-server-close                     #每次请求完毕后主动关闭http通道
    option forwardfor       except 127.0.0.0/8   #如果服务器上的应用程序想记录发起请求的客户端的IP地址，需要在HAProxy
                                                  上 配置此选项， 这样 HAProxy会把客户端的IP信息发送给服务器，在HTTP
                                                  请求中添加"X-Forwarded-For"字段。 启用  X-Forwarded-For，在requests
                                                  头部插入客户端IP发送给后端的server，使后端server获取到客户端的真实IP。 
    option                  redispatch           # 当使用了cookie时，haproxy将会将其请求的后端服务器的serverID插入到
                                                  cookie中，以保证会话的SESSION持久性；而此时，如果后端的服务器宕掉
                                                  了， 但是客户端的cookie是不会刷新的，如果设置此参数，将会将客户的请
                                                  求强制定向到另外一个后端server上，以保证服务的正常。
    retries                 3                    # 定义连接后端服务器的失败重连次数，连接失败次数超过此值后将会将对应后端
                                                  服务器标记为不可用
    timeout http-request    10s                  #http请求超时时间
    timeout queue           1m                   #一个请求在队列里的超时时间
    timeout connect         10s                  #连接超时
    timeout client          1m                   #客户端超时
    timeout server          1m                   #服务器端超时
    timeout http-keep-alive 10s                  #设置http-keep-alive的超时时间
    timeout check           10s                  #检测超时
    maxconn                 3000                 #每个进程可用的最大连接数
frontend  main *:80                             #监听地址为80
    acl url_static       path_beg       -i /static /images /javascript /stylesheets
    acl url_static       path_end       -i .jpg .gif .png .css .js
    use_backend static          if url_static
    default_backend             my_webserver     #定义一个名为my_app前端部分。此处将对于的请求转发给后端
backend static                                   #使用了静态动态分离（如果url_path匹配 .jpg .gif .png .css .js静态文件则访问此后端）
    balance     roundrobin                       #负载均衡算法（#banlance roundrobin 轮询，balance source 保存session值，支持static-rr，
                                                  leastconn，first，uri等参数）
    server      static 127.0.0.1:80 check        #静态文件部署在本机（也可以部署在其他机器或者squid缓存服务器）
backend my_webserver                             #定义一个名为my_webserver后端部分。PS：此处my_webserver只是一个自定义名字而已，但是需要
                                                  与frontend里面配置项default_backend 值相一致
    balance     roundrobin                       #负载均衡算法
    server  web01 172.31.2.33:80  check inter 2000 fall 3 weight 30              #定义的多个后端
    server  web02 172.31.2.34:80  check inter 2000 fall 3 weight 30              #定义的多个后端
    server  web03 172.31.2.35:80  check inter 2000 fall 3 weight 30              #定义的多个后端
```
更多关于Haproxyacl配置请参考博文：http://blog.csdn.net/tantexian/article/details/50015975

配置完成则重启服务：

```txt
systemctl restart haproxy
```
假若想访问监控界面：配置stats uri  /haproxy项，重启服务：

接下来对Haproxy+web负载均衡使用进行实战讲解：

首先配置三台web服务器：172.31.2.33、172.31.2.34、172.31.2.35

三台都是同样操作：

1、实验环境

centos 7.1 X64 mini版 

2、配置web服务器(node33/34/35)：

测试方便，关闭selinux、关闭iptables

一下都采用默认，不做配置即可。

```txt
yum install httpd -y
# vim /etc/httpd/conf/httpd.conf 
```
httpd监听端口：

下述针对Haproxy的配置文件进行详解：

vim /etc/haproxy/haproxy.cfg

下述将选择Haproxy作为负载均衡器进行讲解

跟多关于keepalived+Haproxy请参考文章：http://blog.csdn.net/tantexian/article/details/50056229


原文

- http://blog.csdn.net/tantexian/article/details/50056199