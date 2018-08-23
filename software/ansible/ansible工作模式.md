ansible工作模式
---
* 支持自定义模块功能
* 支持playbook剧本，连续任务按先后设置顺序完成
* 期望每个命令具有幂等性(幂等操作的特点是其任意多次执行所产生的影响均与一次执行的影响相同)

ansible架构
* ansible core : ansible自身核心模块
* host inventory : 主机库,定义可以管控的主机列表
* connection plugins : 连接插件，一般默认基于ssh协议连接
* modules :core modules :(自带模块)、custom modules(自定义模块)
* playbooks :剧本,按照设定编排顺序完成安排任务

![ansible-stucture](http://s1.51cto.com/wyfs02/M01/7A/D9/wKiom1a_UTbwgPO8AAN6D669kL4580.png)

ansible配置文件
---
*  (1)ansible应用程序的主配置文件：/etc/ansible/ansible.cfg

*  (2) Host Inventory定义管控主机：/etc/ansible/hosts

* ansible 获取模块列表

ansible-doc -l：获取列表

* ansible获取模块详细信息

ansible-doc -s  module_name：获取指定模块的使用信息

ansible 命令
---
命令格式

ansible  <host-pattern>  [-f forks] [-m module_name]  [-a args]


- <host-pattern> 指明管控主机，以模式形式表示或者直接给定IP，必须事先定义在文件中；all设置所有
- [-f forks] 指明每批管控多少主机，默认为5个主机一批次
- [-m module_name   使用何种模块管理操作，所有的操作都需要通过模块来指定
- [-a args]   指明模块专用参数；args一般为key=value格式注意：command模块的参数非为kv格式，而是直接给出要执行的命令即可；

注意：<host-pattern>默认读取/etc/ansible/hosts，也可以指明自定义文件路径
  -iPATH, --inventory=PATH：指明使用的host inventory文件路径；


常用模块(module_name)：
---
1. command :默认模块
  -a "COMMAND"

2. ping 模块(无参数)

``` txt
[root@centos1 ~]# ansible all -m ping
192.168.100.37 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.36 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.38 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```
3 raw 模块

一行命令使用raw 模块，再用-a 参数就会执行一行命令

``` txt
[root@centos1 ~]# ansible centos -m raw -a 'mkdir /home/test'
192.168.100.37 | SUCCESS | rc=0 >>
Shared connection to 192.168.100.37 closed.

192.168.100.36 | SUCCESS | rc=0 >>
Shared connection to 192.168.100.36 closed.

[root@centos1 ~]# ansible centos -m raw -a 'ls  /home'
192.168.100.36 | SUCCESS | rc=0 >>
richard  test
Shared connection to 192.168.100.36 closed.

192.168.100.37 | SUCCESS | rc=0 >>
richard  test
Shared connection to 192.168.100.37 closed.
```

4 shell 模块

一般的shell命令都可以在这里执行

``` txt
创建/tmp/test目录

[root@centos1 ~]# ansible centos -m shell -a 'mkdir /tmp/test'
192.168.100.36 | SUCCESS | rc=0 >>

192.168.100.37 | SUCCESS | rc=0 >>

删除目录
[root@centos1 ~]# ansible centos -m shell -a 'rm -rf  /tmp/test/'
192.168.100.36 | SUCCESS | rc=0 >>

192.168.100.37 | SUCCESS | rc=0 >>
```
``` txt
2)user：
-a 'name=  state={present(创建)|absent(删除)}  force=(是否强制操作删除家目录)  system=  uid=  shell= home='
[root@localhost ~]# ansible all -m user -a 'name=ansible state=present'
3)group：
-a 'name= state={present|absent}  gid=  system=(系统组)'
[root@localhost ~]# ansible all -m group -a 'name=mygroup state=presentsystem=true'
4)cron：
-a  'name= state=  minute=  hour= day=  month=  weekday= job='
[root@localhost ~]# ansible all -m cron -a 'name='Time' state=presentminute='*/5' job='/usr/sbin/ntpdate 172.168.0.1 &> /dev/null''

6)file：文件管理
-a 'path=  mode=  owner= group= state={file|directory|link|hard|touch|absent}  src=(link，链接至何处)'
[root@localhost ~]# ansible all -m file -a 'path=/tmp/testdirstate=directory'
[root@localhost ~]# ansible all -m file -a 'path=/tmp/test.txt state=touchmod=600 owner=user1'
7)copy：
-a 'dest=(远程主机上路径)  src=(本地主机路径)  content=(直接指明内容) owner=  group=  mode='
[root@localhosttmp]# ansible web -m copy -a 'src=/etc/yum.repos.d/aliyun.repodest=/etc/yum.repos.d/'
8)template
-a  'dest= src=\'#\'" content=  owner= group=  mode='
9)yum：
-a 'name=  conf_file=(指明配置文件) state={present|latest|absent} enablerepo= disablerepo='        
[root@localhost ~]# ansible all -m yum 'name=httpd state=present'                
10)service：
-a 'name= state={started|stopped|restarted} enabled=(是否开机自动启动)  runlevel='
[root@localhost ~]# ansible all -m service -a 'name=httpd state=started'
11)shell：
-a 'COMMAND'   运行shell命令
[root@localhost ~]# ansible all -m shell -a echo "123456789" |passwd --stdin user1'
12)script：
-a '/PATH/TO/SCRIPT'运行脚本
[root@localhost ~]# ansible all -m script -a '/tmp/a.sh'
```
原文
---
- [ansible自动化运维工具使用详解] http://xuding.blog.51cto.com/4890434/1741852?utm_source=tuicool&utm_medium=referral