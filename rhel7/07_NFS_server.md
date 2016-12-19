安装
---
``` shell
# yum install nfs-utils nfs-utils-lib
```
配置/etc/exports 文件
---
用户可以把需要共享的文件系统直接编辑到/etc/exports文件中，当NFS服务重新启动时会自动读取/etc/exports文件，
示例
---
``` shell
/share/nfs 192.168.100.1/24(rw,sync,no_root_squash,no_all_squash)
```
- /share/nfs   /share/nfs 目录共享
- 192.168.100.1/24  只有192.168.100.1/24这个网段的主机可以正常读取该目录
- rw 可读可写权限，ro 只读权限，
- no_root_squash 当登录NSF服务器的用户为root时，其权限将被转换成为匿名使用者，它的UID,GID都会转变为nobody身份
- root_squash 如果NFS主机使用共享目录的使用者权限为root,对于这个共享目录来说，它具有roott权限
- all_squash 忽略NFS使用者的身份，其身份都会转变为匿名nobody
- sync 同步写入数据到内存和硬盘中，速度慢，有变动都随时写入磁盘
- async 同步到内存，不写入硬盘,速度快，但是有安全风险

``` shell
[root@centos73 /]# vi /etc/exports
/share/nfs 192.168.100.1/24(rw,sync,no_root_squash,no_all_squash)

[root@centos73 /]# systemctl start nfs-server
[root@centos73 /]# systemctl enable nfs-server
Created symlink from /etc/systemd/system/multi-user.target.wants/nfs-server.service to /usr/lib/systemd/system/nfs-server.service.
[root@centos73 /]# systemctl start rpcbind
[root@centos73 /]# systemctl enable rpcbind
[root@centos73 /]# systemctl start nfs-lock
[root@centos73 /]# systemctl enable nfs-lock
[root@centos73 /]# systemctl start nfs-idmap
[root@centos73 /]# systemctl enable nfs-idmap
```
exportfs命令
---
``` shell
exportfs [-avruv]
```
1. -a 全部挂载（卸载） /etc/export文件中的配置
2. -r 重新挂载 /etc/export文件中的配置，同步更新/var/lib/nfs/xtab中是内容
3. -u 卸载某一目录
4. -v 输出结果到显示屏幕

``` shell
# cat /var/lib/nfs/xtab
```
showmount 命令
---

``` shell
# showmount [-ae] hostname
```
- -a 或-all  以host:dir来显示挂载的目录
- -d directories 显示被客户端挂载的目录名
- -e 或-exports 显示NFS服务器输出清单
要扫描某一主机提供的NFS共享目录时，使用showmount -e IP (或主机hostname)

观察激活的端口
---
``` shell
netstat -utln
```
NFS开启的端口是2049

防火墙和selinux设置
---
NFS监听TCP/UDP 2049端口，portmap监听TCP/UDPD 111端口，还需打开mountd,statd,lockd服务相关端口，防火墙需开放TCP/UDP 的892和662端口，以及TCP的32803和UDP 32769端口 ，/etc/sysconfig/iptables关于NFS设置如下
``` shell
[root@centos73 ~]# firewall-cmd --permanent --add-port=111/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=54302/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=20048/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=2049/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=46666/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=42955/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --add-port=875/tcp
success
[root@centos73 ~]# firewall-cmd --permanent --zone=public --add-service=nfs
success
[root@centos73 ~]# firewall-cmd --reload
success
```
NFS的selinux设置
---
将本机的NFS共享设置成为可读可写，需要开放相关布尔值变量
``` shell
# setsebool -P nfs_export_all_rw on
```
如果需要将远程NFS共享到本机，需要开放相关布尔值变量
``` shell
[root@centos73 ~]# setsebool -P nfs_export_all_rw on
[root@centos73 ~]# setsebool -P use_nfs_home_dirs on

[root@centos73 ~]# setsebool -P allow_gssd_read_tmp 1
[root@centos73 ~]# setsebool -P allow_nfsd_anon_write 1
[root@centos73 ~]# setsebool -P nfs_export_all_ro 1
[root@centos73 ~]# setsebool -P nfs_export_all_rw 1
[root@centos73 ~]# setsebool -P use_nfs_home_dirs 1
[root@centos73 ~]# setsebool -P nfs_export_all_rw on
```
- allow_ftpd_use_nfs 允许ftp访问这个挂载
- allow_nfsd_anon_write 启用这个变量允许写入到一个公共目录匿名ngsd
- httpd_use_nfs
- nfs_export_all_ro  只读权限
- nfs_export_all_rw 读写权限
- qemu_use_nfs 允许QEMU使用nfs
- sambe_share_nfs
- use_nfs_home_dirs 允许支持nfs主目录
- virt_use_nfs
- xen_use_nfs

检查nfs服务
---
``` shell
root@centos73 ~]# showmount -e
Export list for centos73:
/share/nfs 192.168.100.1/24
[root@centos73 ~]# exportfs -rv
exporting 192.168.100.1/24:/share/nfs
```
在客户机挂载
---
``` shell
root@gitlab:~# mkdir /data
root@gitlab:~# mount.nfs 192.168.100.139:/share/nfs /data
root@gitlab:~# df -h
/dev/mapper/ubuntu--vg-root   18G  5.9G   11G  37% /
/dev/sda1                    472M  103M  346M  23% /boot
192.168.100.139:/share/nfs    17G  5.2G   12G  31% /data
已经挂载上了，下面放个文件，再返回nfs服务器上查看文件是否存在

oot@gitlab:~# cd /data/
root@gitlab:/data# cp /home/richard/test .
root@gitlab:/data# ll
total 8
drwxrwxrwx  2 root root   46 Dec 18 20:03 ./
drwxr-xr-x 24 root root 4096 Dec 18 20:02 ../
-rwxrwxrwx  1 root root 1406 Dec 18 19:38 initial-setup-ks.cfg*
-rw-r--r--  1 root root    0 Dec 18 20:03 test
root@gitlab:/data# mv test 192.168.100.10
root@gitlab:/data# ls
192.168.100.10  initial-setup-ks.cfg

返回nfs服务器，查看文件是否存在
[root@centos73 ~]# ll /share/nfs/
总用量 4
-rw-r--r--. 1 root root    0 12月 18 20:03 192.168.100.10
-rwxrwxrwx. 1 root root 1406 12月 18 19:38 initial-setup-ks.cfg
```
