inventory
---
``` txt
n.
清查;存货清单;财产目录，财产目录的编制;存货总值
vt.
盘存;编制…的目录;开列…的清单;总结
```
ansible可以同时操作一组或者多组服务器，通过inventory文件配置，默认路径/etc/ansible/hosts
- inventory默认路径为 /etc/ansible/hosts

``` txt
mail.example.com

[webserver]
foo.example.com
bar.example.com

[mailserver]
one.example.com
two.example.com
```
- []用于分类，默认端口是ssh 标准22，改为其他使用：端口号

``` txt
web.example.com:2222
```
定义group变量（组变量）
---

```txt
/etc/ansible/group_vars/ralegh
/etc/ansible/group_vars/football
/etc/ansible/group_vars/basketball
```
```txt
ansible_ssh_host
      将要连接的远程主机名.与你想要设定的主机的别名不同的话,可通过此变量设置.

ansible_ssh_port
      ssh端口号.如果不是默认的端口号,通过此变量设置.

ansible_ssh_user
      默认的 ssh 用户名

ansible_ssh_pass
      ssh 密码(这种方式并不安全,我们强烈建议使用 --ask-pass 或 SSH 密钥)

ansible_sudo_pass
      sudo 密码(这种方式并不安全,我们强烈建议使用 --ask-sudo-pass)

ansible_sudo_exe (new in version 1.8)
      sudo 命令路径(适用于1.8及以上版本)

ansible_connection
      与主机的连接类型.比如:local, ssh 或者 paramiko. Ansible 1.2 以前默认使用 paramiko.1.2 以后默认使用 'smart','smart' 方式会根据是否支持 ControlPersist, 来判断'ssh' 方式是否可行.

ansible_ssh_private_key_file
      ssh 使用的私钥文件.适用于有多个密钥,而你不想使用 SSH 代理的情况.

ansible_shell_type
      目标系统的shell类型.默认情况下,命令的执行使用 'sh' 语法,可设置为 'csh' 或 'fish'.

ansible_python_interpreter
      目标主机的 python 路径.适用于的情况: 系统中有多个 Python, 或者命令路径不是"/usr/bin/python",比如  \*BSD, 或者 /usr/bin/python
      不是 2.X 版本的 Python.我们不使用 "/usr/bin/env" 机制,因为这要求远程用户的路径设置正确,且要求 "python" 可执行程序名不可为 python以外的名字(实际有可能名为python26).

      与 ansible_python_interpreter 的工作方式相同,可设定如 ruby 或 perl 的路径....
```

一个主机文件的例子:
``` txt
some_host         ansible_ssh_port=2222     ansible_ssh_user=manager
aws_host          ansible_ssh_private_key_file=/home/example/.ssh/aws.pem
freebsd_host      ansible_python_interpreter=/usr/local/bin/python
ruby_module_host  ansible_ruby_interpreter=/usr/bin/ruby.1.9.3
```
参考资料
---
[Inventory文件] http://www.ansible.com.cn/docs/intro_inventory.html#inventoryformat