ansible匹配目标服务
---

ansible <pattern_goes_here> -m <module_name> -a <arguments>

实例：重启所有web server组的apache服务

ansible webserver -m service -a 'name=httpd state=restart'

<pattern_goes_here> 规则

pattern 模式;图案;花样，样品;榜样，典范

```txt
all 或者 *                        匹配所有主机
webservers                        配置webserver组
web_server:dns_server:nfs_server  匹配多个组用 ：号隔开
192.168.1.*                       匹配一个网段
~(web|db).* \.example\ .com       支持正则表达式匹配主机
webserver:!192.168.1.22           匹配webserver组且排除192.168.1.22主机
web_server&db_server              匹配两个集群的交集
```
