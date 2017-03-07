ansible module模块
---

ansible提供了丰富的模块，包括cloud 云计算 、Commands 命令行 、Database 数据库 、Inventory 资产管理 、File 文件管理 、Network 网络管理 、System 系统管理等模块。

```txt
[root@proxy ~]# ansible-doc -l
a10_server                         Manage A10 Networks AX/SoftAX/Thunder/vThunder devices                                                                        
a10_service_group                  Manage A10 Networks devices' service groups                                                                                   
a10_virtual_server                 Manage A10 Networks devices' virtual servers                                                                                  
acl                                Sets and retrieves file ACL information.                                                                                      
add_host                           add a host (and alternatively a group) to the ansible-playbook in-memory inventory                                            
airbrake_deployment                Notify airbrake about app deployments                                                                                         
alternatives                       Manages alternative programs for common commands                                                                              
apache2_mod_proxy                  Set and/or get members' attributes of an Apache httpd 2.4 mod_proxy balancer pool                                             
apache2_module                     enables/disables a module of the Apache2 webserver
：
```
默认模块名称为 Command ，-m command可以省略

ping 模块不用参数

```txt
[root@proxy ~]# ansible spark -m ping
192.168.100.22 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.21 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.23 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```
1 . 远程命令模块 ： command (默认) 、script 、shell 

- command可以执行远程权限范围内所有shell命令
- script是在远程主机执行主控端存储的shell 脚本文件，相当于scp + script组合
- shell 功能是执行远程主机shell脚本文件

例子：

```txt
# ansible web_server -m command -a 'free -m'
# ansible web_server -m script -a '/home/test.sh 12 34'
# ansible web_server -m shell -a '/home/test.sh'
```

2 . copy模块： 实现主控端向目标主机拷贝文件，类似与scp功能

示例

将控制主机/home/test.sh拷贝到web_servers组/tmp 目录下。并更新文件主属性和权限

```txt
# ansible web_servers -m copy -a 'src=/home/test.sh dest=/tmp  owner=root group=root mode=0755'
```
也可以用file模块实现权限更改

```txt
-m file 'path=/home/test.sh owner=root group=root mode=0755'
```

```txt
测试shell脚本

[root@proxy ~]# cat /home/test.sh 
#!/bin/bash

date

将/home/test.sh脚本传输到所有spark组node上，并修改文件权限
[root@proxy ~]# ansible spark -m copy -a "src=/home/test.sh dest=/tmp owner=richard group=richard mode=0755"
192.168.100.22 | SUCCESS => {
    "changed": true, 
    "checksum": "dae3fc8841918fcd3ce64b8b742f80e47e129de4", 
    "dest": "/tmp/test.sh", 
    "gid": 1000, 
    "group": "richard", 
    "md5sum": "3faa1334851f4866da13355a189bfb87", 
    "mode": "0755", 
    "owner": "richard", 
    "size": 19, 
    "src": "/root/.ansible/tmp/ansible-tmp-1488748935.24-260397996524982/source", 
    "state": "file", 
    "uid": 1000
}
192.168.100.21 | SUCCESS => {
    "changed": true, 
    "checksum": "dae3fc8841918fcd3ce64b8b742f80e47e129de4", 
    "dest": "/tmp/test.sh", 
    "gid": 1000, 
    "group": "richard", 
    "md5sum": "3faa1334851f4866da13355a189bfb87", 
    "mode": "0755", 
    "owner": "richard", 
    "size": 19, 
    "src": "/root/.ansible/tmp/ansible-tmp-1488748935.16-156076103161022/source", 
    "state": "file", 
    "uid": 1000
}
192.168.100.23 | SUCCESS => {
    "changed": true, 
    "checksum": "dae3fc8841918fcd3ce64b8b742f80e47e129de4", 
    "dest": "/tmp/test.sh", 
    "gid": 1000, 
    "group": "richard", 
    "md5sum": "3faa1334851f4866da13355a189bfb87", 
    "mode": "0755", 
    "owner": "richard", 
    "size": 19, 
    "src": "/root/.ansible/tmp/ansible-tmp-1488748939.73-69627482240783/source", 
    "state": "file", 
    "uid": 1000
}
[root@proxy ~]# 
```
执行这个shell脚本

```txt
[root@proxy ~]# ansible spark -m shell -a '/tmp/test.sh'
192.168.100.23 | SUCCESS | rc=0 >>
Mon Mar  6 05:27:12 CST 2017

192.168.100.21 | SUCCESS | rc=0 >>
Mon Mar  6 05:27:12 CST 2017

192.168.100.22 | SUCCESS | rc=0 >>
Mon Mar  6 05:27:12 CST 2017
``
写一个脚本放在本地，由远端主机执行

```txt
一个简单脚本
[root@proxy ~]# cat /home/hello-ansible.sh 
#!/bin/bash

echo I come from 192.168.100.9
echo hostname proxy

执行/home/hello-ansible.sh脚本
[root@proxy ~]# ansible spark -m script -a '/home/hello-ansible.sh'
192.168.100.21 | SUCCESS => {
    "changed": true, 
    "rc": 0, 
    "stderr": "Shared connection to 192.168.100.21 closed.\r\n", 
    "stdout": "I come from 192.168.100.9\r\nhostname proxy\r\n", 
    "stdout_lines": [
        "I come from 192.168.100.9", 
        "hostname proxy"
    ]
}
192.168.100.23 | SUCCESS => {
    "changed": true, 
    "rc": 0, 
    "stderr": "Shared connection to 192.168.100.23 closed.\r\n", 
    "stdout": "I come from 192.168.100.9\r\nhostname proxy\r\n", 
    "stdout_lines": [
        "I come from 192.168.100.9", 
        "hostname proxy"
    ]
}
192.168.100.22 | SUCCESS => {
    "changed": true, 
    "rc": 0, 
    "stderr": "Shared connection to 192.168.100.22 closed.\r\n", 
    "stdout": "I come from 192.168.100.9\r\nhostname proxy\r\n", 
    "stdout_lines": [
        "I come from 192.168.100.9", 
        "hostname proxy"
    ]
}
[root@proxy ~]# 
```
```txt
[root@proxy ~]# ansible-doc -l      #查看所有模块
```

```txt
[root@proxy ~]# ansible-doc copy    #查看copy模块的用法
```

示例 2
为所有服务器安装ntp服务并设置为开机启动。

步骤1：安装ntp服务

执行命令：

```txt
# ansible apps -s -m yum -a "name=ntp state=present"
```
步骤2：启动ntp服务并设置为开机启动

执行命令：

```txt
# ansible apps -m service -a "name=ntpd state=started enabled=yes"
```

参考资料
--- 

- 《python自动化运维》