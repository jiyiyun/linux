使用 Ad-Hoc 管理简单任务
---
如果我们敲入一些命令去比较快的完成一些事情,而不需要将这些执行的命令特别保存下来, 这样的命令就叫做 ad-hoc 命令.

``` txt
Ansible提供两种方式去完成任务,
一是 ad-hoc 命令,
一是写 Ansible playbook.
前者可以解决一些简单的任务, 后者解决较复杂的任务.
```
``` txt
[root@centos1 .ssh]# ansible centos -m raw -a 'pip install robotframework'
192.168.100.37 | SUCCESS | rc=0 >>
Collecting robotframework
  Downloading robotframework-3.0.tar.gz (430kB)
    100% |████████████████████████████████| 440kB 108kB/s 
Installing collected packages: robotframework
  Running setup.py install for robotframework ... done
Successfully installed robotframework-3.0
Shared connection to 192.168.100.37 closed.


192.168.100.36 | SUCCESS | rc=0 >>
Collecting robotframework
  Downloading robotframework-3.0.tar.gz (430kB)
    100% |████████████████████████████████| 440kB 55kB/s 
Installing collected packages: robotframework
  Running setup.py install for robotframework ... done
Successfully installed robotframework-3.8.100.36 closed.


[root@centos1 .ssh]# 
```
使用 Ansible 的命令行工具来重启 centos 组中所有的服务器,每次重启1个,一个起来了再重启下一个

```txt
root@gitlab:~# ansible centos -a "/sbin/reboot" -f 1
192.168.100.35 | FAILED | rc=0 >>
MODULE FAILURE

192.168.100.36 | FAILED | rc=0 >>
MODULE FAILURE

192.168.100.37 | FAILED | rc=0 >>
MODULE FAILURE

root@gitlab:~# 

```
默认以当前用户执行命令，可以指定用户
``` txt
$ ansible atlanta -a "/usr/bin/foo" -u username

$ ansible atlanta -a "/usr/bin/foo" -u username --sudo [--ask-sudo-pass]

```

ansible 有很多模块，默认是command模块，可以通过-m 来指定模块

```txt
root@gitlab:~# ansible centos -m shell -a "echo $TERM"
192.168.100.37 | SUCCESS | rc=0 >>
xterm

192.168.100.35 | SUCCESS | rc=0 >>
xterm

192.168.100.36 | SUCCESS | rc=0 >>
xterm

root@gitlab:~# 

```
file transfer文件传输
---
Ansible能够以并行方式同时scp大量文件到多台主机

```txt
root@gitlab:~# ansible centos -m copy -a "src=/root/.ssh/id_rsa dest=/tmp/id_rsa"
192.168.100.37 | SUCCESS => {
    "changed": true, 
    "checksum": "2add00c5191c285566ab3c733f7b99e903b8d3d2", 
    "dest": "/tmp/id_rsa", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "9a289a2ca31732273636cd33716a7dc9", 
    "mode": "0644", 
    "owner": "root", 
    "size": 1679, 
    "src": "/root/.ansible/tmp/ansible-tmp-1483359423.66-28517516780552/source", 
    "state": "file", 
    "uid": 0
}
192.168.100.35 | SUCCESS => {
    "changed": true, 
    "checksum": "2add00c5191c285566ab3c733f7b99e903b8d3d2", 
    "dest": "/tmp/id_rsa", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "9a289a2ca31732273636cd33716a7dc9", 
    "mode": "0644", 
    "owner": "root", 
    "size": 1679, 
    "src": "/root/.ansible/tmp/ansible-tmp-1483359430.79-141904242737294/source", 
    "state": "file", 
    "uid": 0
}
192.168.100.36 | SUCCESS => {
    "changed": true, 
    "checksum": "2add00c5191c285566ab3c733f7b99e903b8d3d2", 
    "dest": "/tmp/id_rsa", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "9a289a2ca31732273636cd33716a7dc9", 
    "mode": "0644", 
    "owner": "root", 
    "size": 1679, 
    "src": "/root/.ansible/tmp/ansible-tmp-1483359433.22-185925205241639/source", 
    "state": "file", 
    "uid": 0
}
root@gitlab:~# 
```
``` txt
root@gitlab:~# ansible centos -m rm -a "rm -f /tmp/hosts"
ERROR! this task 'rm' has extra params, which is only allowed in the following modules: command, shell, script, include, include_vars, add_host, group_by, set_fact, raw, meta

删除命令错误，没有rm模块，提示中可以用command,shell,raw等模块中的rm命令

root@gitlab:~# ansible centos -m raw -a "rm -f /tmp/hosts"
192.168.100.35 | SUCCESS | rc=0 >>


192.168.100.36 | SUCCESS | rc=0 >>


192.168.100.37 | SUCCESS | rc=0 >>


root@gitlab:~# 

```
验证删除
``` txt
[root@centos3 ~]# cat /tmp/hosts            #执行删除命令前
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA7BUAUKzadvFAHak+iZmGfZJhpMt9BmKchUclyRoMrvz7NECS
-----END RSA PRIVATE KEY-----
[root@centos3 ~]# cat /tmp/hosts            #执行删除命令后
cat: /tmp/hosts: No such file or directory
```
```txt
ansible -i hosts all -m ping -u www
```
该命令选项的作用分别为：

* -i：指定 inventory 文件，使用当前目录下的 hosts
* all：针对 hosts 定义的所有主机执行，这里也可以指定组名或模式
* -m：指定所用的模块，我们使用 Ansible 内置的 ping 模块来检查能否正常管理远端机器
* -u：指定远端机器的用户

``` txt
root@gitlab:~# ansible centos -a 'uptime'
192.168.100.35 | SUCCESS | rc=0 >>
 04:57:22 up  1:31,  2 users,  load average: 0.16, 0.12, 0.13

192.168.100.37 | SUCCESS | rc=0 >>
 04:57:25 up  1:31,  2 users,  load average: 0.00, 0.01, 0.05

192.168.100.36 | SUCCESS | rc=0 >>
 04:57:25 up  1:31,  2 users,  load average: 0.00, 0.01, 0.05

```
此处我们省略了 -m，Ansible 默认使用 command 模块；-a 指定模块的参数，即执行 uptime 命令。

如果被管理端的 Python 为 2.4，那么需要 python-simplejson 这个包。我们可以通过以下命令在所有 CentOS 主机上安装它：

```txt
ansible all -m raw -a 'yum -y install python-simplejson'
```
可通过 ansible-doc 查询模块文档，如：

``` txt
ansible-doc raw
```
附录ansible常用命令
---
如果想通过 sudo 去执行命令,如下:
``` txt
root@gitlab:~# ansible -h
Usage: ansible <host-pattern> [options]

Options:
  -a MODULE_ARGS, --args=MODULE_ARGS
                        module arguments
  --ask-become-pass     ask for privilege escalation password
  -k, --ask-pass        ask for connection password
  --ask-su-pass         ask for su password (deprecated, use become)
  -K, --ask-sudo-pass   ask for sudo password (deprecated, use become)
  --ask-vault-pass      ask for vault password
  -B SECONDS, --background=SECONDS
                        run asynchronously, failing after X seconds
                        (default=N/A)
  -b, --become          run operations with become (nopasswd implied)
  --become-method=BECOME_METHOD
                        privilege escalation method to use (default=sudo),
                        valid choices: [ sudo | su | pbrun | pfexec | runas |
                        doas ]
  --become-user=BECOME_USER
                        run operations as this user (default=root)
  -C, --check           don't make any changes; instead, try to predict some
                        of the changes that may occur
  -c CONNECTION, --connection=CONNECTION
                        connection type to use (default=smart)
  -D, --diff            when changing (small) files and templates, show the
                        differences in those files; works great with --check
  -e EXTRA_VARS, --extra-vars=EXTRA_VARS
                        set additional variables as key=value or YAML/JSON
  -f FORKS, --forks=FORKS
                        specify number of parallel processes to use
                        (default=5)
  -h, --help            show this help message and exit
  -i INVENTORY, --inventory-file=INVENTORY
                        specify inventory host path
                        (default=/etc/ansible/hosts) or comma separated host
                        list
  -l SUBSET, --limit=SUBSET
                        further limit selected hosts to an additional pattern
  --list-hosts          outputs a list of matching hosts; does not execute
                        anything else
  -m MODULE_NAME, --module-name=MODULE_NAME
                        module name to execute (default=command)
  -M MODULE_PATH, --module-path=MODULE_PATH
                        specify path(s) to module library (default=None)
  --new-vault-password-file=NEW_VAULT_PASSWORD_FILE
                        new vault password file for rekey
  -o, --one-line        condense output
  --output=OUTPUT_FILE  output file name for encrypt or decrypt; use - for
                        stdout
  -P POLL_INTERVAL, --poll=POLL_INTERVAL
                        set the poll interval if using -B (default=15)
  --private-key=PRIVATE_KEY_FILE, --key-file=PRIVATE_KEY_FILE
                        use this file to authenticate the connection
  --scp-extra-args=SCP_EXTRA_ARGS
                        specify extra arguments to pass to scp only (e.g. -l)
  --sftp-extra-args=SFTP_EXTRA_ARGS
                        specify extra arguments to pass to sftp only (e.g. -f,
                        -l)
  --ssh-common-args=SSH_COMMON_ARGS
                        specify common arguments to pass to sftp/scp/ssh (e.g.
                        ProxyCommand)
  --ssh-extra-args=SSH_EXTRA_ARGS
                        specify extra arguments to pass to ssh only (e.g. -R)
  -S, --su              run operations with su (deprecated, use become)
  -R SU_USER, --su-user=SU_USER
                        run operations with su as this user (default=root)
                        (deprecated, use become)
  -s, --sudo            run operations with sudo (nopasswd) (deprecated, use
                        become)
  -U SUDO_USER, --sudo-user=SUDO_USER
                        desired sudo user (default=root) (deprecated, use
                        become)
  --syntax-check        perform a syntax check on the playbook, but do not
                        execute it
  -T TIMEOUT, --timeout=TIMEOUT
                        override the connection timeout in seconds
                        (default=10)
  -t TREE, --tree=TREE  log output to this directory
  -u REMOTE_USER, --user=REMOTE_USER
                        connect as this user (default=None)
  --vault-password-file=VAULT_PASSWORD_FILE
                        vault password file
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable
                        connection debugging)
  --version             show program's version number and exit
```