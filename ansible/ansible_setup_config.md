ansible安装
---
```shell
yum install ansible -y
apt install ansible -y
zypper in ansible -y
```

设置免密码登录
---
- 控制端

``` shell
# cd ~/.ssh/
# ssh-keygen
# scp id_rsa.pub 192.168.100.37:/root
```
- 被控端

```shell
# cat id_rsa.pub >> ~/.ssh/authorized_keys
```
- 验证ssh免密码登录是否ok

``` shell
# ssh 192.168.100.36
Last login: Mon Jan  2 16:57:17 2017 from 192.168.100.1
[root@centos2 ~]# exit
logout
Connection to 192.168.100.36 closed.
[root@centos1 .ssh]# ssh 192.168.100.37
Last login: Mon Jan  2 16:57:19 2017 from 192.168.100.1
[root@centos3 ~]# exit
logout
Connection to 192.168.100.37 closed.
```
- 编辑 # vi /etc/ansible/hosts 文件，把所有node加上

```shell
# vi /etc/ansible/hosts
[centos]
192.168.100.36
192.168.100.37

[opensuse]
192.168.100.149
```
- 测试ansibel控制端和被控端连通情况

```shell
[root@centos1 .ssh]# ansible all -m ping
192.168.100.37 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.36 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.100.149 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}

[root@centos1 .ssh]# ansible all -a "/bin/echo hello"
192.168.100.36 | SUCCESS | rc=0 >>
hello

192.168.100.37 | SUCCESS | rc=0 >>
hello

192.168.100.149 | SUCCESS | rc=0 >>
hello
```
默认使用当前用户执行命令，如果要使用其它用户名 使用-u 参数指定用户名： -u richard，使用richard用户名执行该命令

```txt
ansible -i hosts all -m ping -u www
```
该命令选项的作用分别为:
```txt
-i：指定 inventory 文件，使用当前目录下的 hosts
-all：针对 hosts 定义的所有主机执行，这里也可以指定组名或模式
-m：指定所用的模块，我们使用 Ansible 内置的 ping 模块来检查能否正常管理远端机器
-u：指定远端机器的用户
```
known_hosts
---
主机更新，known_hosts会报错，解决办法

```txt
1. 更新known_hosts对应的主机指纹
2. 禁用host_key_checking 

/etc/ansible/ansible.cfg or ~/.ansible.cfg

[defaults]
host_key_checking = False

3. 修改环境变量
$ export ANSIBLE_HOST_KEY_CHECKING=False
```

参考资料
---
- http://www.ansible.com.cn
- https://linuxtoy.org/archives/hands-on-with-ansible.html