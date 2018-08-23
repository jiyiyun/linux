ansible module模块
---

ansible提供了丰富的模块，包括cloud 云计算 、Commands 命令行 、Database 数据库 、Inventory 资产管理 、File 文件管理 、Network 网络管理 、System 系统管理等模块。

默认模块名称为 Command ，-m command可以省略

ping 模块不用参数

1 . 远程命令模块 ： command (默认) 、script 、shell
---

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
---

示例

将控制主机/home/test.sh拷贝到web_servers组/tmp 目录下。并更新文件主属性和权限

```txt
# ansible web_servers -m copy -a 'src=/home/test.sh dest=/tmp  owner=root group=root mode=0755'
```
也可以用file模块实现权限更改

```txt
-m file 'path=/home/test.sh owner=root group=root mode=0755'
```

3 . stat模块(获取远程文件状态信息，包括atime ctime  mtime  md5  uid  gid 等)
---

```txt
root@gitlab:~# ansible registry -m stat -a 'path=/etc/sysctl.conf'
192.168.100.8 | SUCCESS => {
    "changed": false, 
    "stat": {
        "atime": 1489311340.9800003, 
        "checksum": "d599534a0fc9ac7757ed53aef73a9e39c90e49a3", 
        "ctime": 1482628013.6520224, 
        "dev": 64768, 
        "exists": true, 
        "gid": 0, 
        "gr_name": "root", 
        "inode": 33853150, 
        "isblk": false, 
        "ischr": false, 
        "isdir": false, 
        "isfifo": false, 
        "isgid": false, 
        "islnk": false, 
        "isreg": true, 
        "issock": false, 
        "isuid": false, 
        "md5": "324c073ebf5a4811bf7fd5610f170350", 
        "mode": "0644", 
        "mtime": 1478401812.0, 
        "nlink": 1, 
        "path": "/etc/sysctl.conf", 
        "pw_name": "root", 
        "rgrp": true, 
        "roth": true, 
        "rusr": true, 
        "size": 449, 
        "uid": 0, 
        "wgrp": false, 
        "woth": false, 
        "wusr": true, 
        "xgrp": false, 
        "xoth": false, 
        "xusr": false
    }
}
root@gitlab:~# 
```
4 . get_url模块
---

实现在远程主机下载指定URL到本地，支持sha256sum文件校验

```txt
root@gitlab:~# ansible registry -m get_url -a 'url=https://www.baidu.com dest=/tmp/index.html'
192.168.100.8 | SUCCESS => {
    "changed": true, 
    "checksum_dest": null, 
    "checksum_src": "77e920ff2d5ce5ac4bb3c399c7f3fa29dd7ced82", 
    "dest": "/tmp/index.html", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "8f1f3fef541f7dbb36a8755a9f0eff40", 
    "mode": "0644", 
    "msg": "OK (227 bytes)", 
    "owner": "root", 
    "size": 227, 
    "src": "/tmp/tmpaNrrnu", 
    "state": "file", 
    "uid": 0, 
    "url": "https://www.baidu.com"
}
root@gitlab:~# 
```
5 . yum 模块(centos) apt模块(ubuntu)
---

```txt
CentOS系统
root@gitlab:~# ansible registry -m yum -a 'name=curl state=latest'
192.168.100.8 | SUCCESS => {
    "changed": false, 
    "msg": "", 
    "rc": 0, 
    "results": [
        "All packages providing curl are up to date", 
        ""
    ]
}

ubuntu系统
root@gitlab:~# ansible gitlab -m apt -a 'pkg=curl state=latest'
192.168.100.10 | SUCCESS => {
    "cache_update_time": 0, 
    "cache_updated": false, 
    "changed": false
}
root@gitlab:~#
```

6 . cron模块(远程主机crontab设置)
---

7 . mount模块(远程主机分区挂载)
---

8 . service模块(远程主机服务管理)
---

```txt
root@gitlab:~# ansible gitlab -m service -a 'name=docker state=stopped'
192.168.100.10 | SUCCESS => {
    "changed": true, 
    "name": "docker", 
    "state": "stopped"
}
root@gitlab:~# docker ps
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
root@gitlab:~# 
```

9 . sysctl模块(远程主机sysctl设置)
---

10 . user服务模块(远程主机用户管理)
---

```txt
添加用户
root@gitlab:~# ansible registry -m user -a "name=johnd comment='john Doe'"
192.168.100.8 | SUCCESS => {
    "changed": true, 
    "comment": "john Doe", 
    "createhome": true, 
    "group": 1001, 
    "home": "/home/johnd", 
    "name": "johnd", 
    "shell": "/bin/bash", 
    "state": "present", 
    "system": false, 
    "uid": 1001
}

删除用户
root@gitlab:~# ansible registry -m user -a "name=johnd state=absent remove=yes"
192.168.100.8 | SUCCESS => {
    "changed": true, 
    "force": false, 
    "name": "johnd", 
    "remove": true, 
    "state": "absent"
}

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
script 模块
---

写一个脚本放在本地，由远端主机执行(shell模块，不必copy过去，直接在本地执行命令 )

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

附录1

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
附录2：

```txt
[root@proxy ~]# ansible-doc -l      #查看所有模块
```

```txt
[root@proxy ~]# ansible-doc copy    #查看copy模块的用法
```
附录3：

playbook模块格调用格式如下，以command模块为例

```txt
- name: reboot the server
  command: /sbin/reboot -t now
```
参考资料
--- 

- 《python自动化运维:技术与最佳实践》刘天斯著ISBN:978-7-111-48306-9