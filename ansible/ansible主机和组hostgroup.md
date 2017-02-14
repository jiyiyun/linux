安装ansible
---
```txt
yum install ansible     # RHEL/CentOS/Fedora，需要配置 EPEL
pt-get install ansible  # Debian/Ubuntu
zypper install ansible  # OpenSUSE
pip install ansible
```
Inventory
---
Inventory 文件用来定义你要管理的主机。其默认位置在 /etc/ansible/hosts ，如果不保存在默认位置，也可通过 -i 选项指定。被管理的机器可以通过其 IP 或域名指定。未分组的机器需保留在 hosts 的顶部，分组可以使用 [] 指定
``` txt
也可以通过数字和字母模式来指定一系列连续主机，如：

[1:3].linuxtoy.org # 等价于
1.linuxtoy.org、2.linuxtoy.org、3.linuxtoy.org  
[a:c].linuxtoy.org # 等价于
a.linuxtoy.org、b.linuxtoy.org、c.linuxtoy.org
```

创建免密码登录
---
``` txt
在控制主机上生成id.rsa、id.rsa.pub，将公钥发送给每个host
~/.ssh# scp id_rsa.pub 192.168.10.11:/root
~/.ssh# scp id_rsa.pub 192.168.10.12:/root
~/.ssh# scp id_rsa.pub 192.168.10.13:/root

将公钥写入到.ssh/authorized_keys文件
cat id_rsa.pub >> .ssh/authorized_keys
cat id_rsa.pub >> .ssh/authorized_keys
cat id_rsa.pub >> .ssh/authorized_keys
```

创建ansible主机和组hosts和group
---
``` txt
/etc/ansible/hosts 

[centos]
192.168.10.11
192.168.10.12
192.168.10.13

[k8s]
node1.k8s.com
node2.k8s.com
node3.k8s.com
```
测试是否可以正常工作

``` txt
# ansible  all -m ping -u root
192.168.0.161 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.15.160 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.15.161 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

参考资料
---
- [Ansible 英文官网]https://www.ansible.com/resources
- [Ansible中文权威指南]http://www.ansible.com.cn/index.html
- [Ansible 快速上手]https://linuxtoy.org/archives/hands-on-with-ansible.html