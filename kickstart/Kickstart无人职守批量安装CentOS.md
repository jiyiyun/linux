PXE+DHCP+Apache+Kickstart无人职守批量安装CentOS
===

关闭防火墙和selinux
---

```txt
[root@localhost html]# systemctl disable firewalld
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
Removed symlink /etc/systemd/system/basic.target.wants/firewalld.service.
[root@localhost html]# vi /etc/selinux/config
SELINUX=disabled
```
设置httpd 部分
---
安装httpd

```txt
yum install httpd –y
```
设置httpd为开机启动

```txt
systemctl enable httpd
```
挂载光到光盘全部内容至http 的根目录/var/www/html/ 下
HTTP部分设置完毕

安装X windows
---

```txt
yum -y groupinstall Desktop
yum -y groupinstall "X Window System"
yum install libX11                    #前面没有报错就不用装
yum -y groupinstall chinese-support   #安装中文支持可以不装 
```
安装TFTP
---

``` txt
yum install tftp-server –y
```
配置tftp

```
[root@localhost ~]# vi /etc/xinetd.d/tftp
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
```
设置TFTP为开机自启动

```txt
[root@localhost ~]# systemctl start tftp
[root@localhost ~]# systemctl enable tftp
Created symlink from /etc/systemd/system/sockets.target.wants/tftp.socket to /usr/lib/systemd/system/tftp.socket.
```
安装syslinux
---

```txt
# yum install syslinux
```
将pxelinux拷贝到tftpboot目录

```
#cp /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot/
```
安装dhcp服务
---

```txt
ddns-update-style interim; 
ignore client-updates; 
filename "pxelinux.0"; 　　#pxelinux 启动文件位置;
next-server 192.168.111.130;　　#TFTP Server 的IP地址;

subnet 192.168.111.0 netmask 255.255.255.0 {

        option routers                  192.168.111.130; 
        option subnet-mask              255.255.255.0;

        range dynamic-bootp 192.168.111.100 192.168.111.200; 
        default-lease-time 21600; 
        max-lease-time 43200;
}
```
启动dhcp

```
systemctl start dhcp
```

安装kickstart
---

``` txt
yum install system-config-kickstart
```
kickstart在图形桌面配置

```txt
# startx
# system-config-kickstart
```
下一步，下一步最后自动生成ks.conf文件

```
platform=x86, AMD64, or Intel EM64T 
#version=DEVEL 
# Firewall configuration 
firewall --disabled 
# Install OS instead of upgrade 
install 
# Use network installation 
url --url=http://192.168.111.130/cdrom/ 　　#这个选项告诉安装程序：到服务器192.168.111.130 的HTTP根目录下的cdrom 文件夹下寻找安装介质
# Root password 
rootpw --iscrypted $1$vsvtP./e$6PVMNfJd.shq2LgFJjYfA1 
# System authorization information 
auth  --useshadow  --enablemd5 
# Use graphical install 
graphical 
firstboot --disable 
# System keyboard 
keyboard us 
# System language 
lang en_US 
# SELinux configuration 
selinux --disabled 
# Installation logging level 
logging --level=info 
# Reboot after installation 
reboot 
# System timezone 
timezone  --isUtc Asia/Shanghai 
# Network information 
network  --bootproto=dhcp --device=eth0 --onboot=on 
# System bootloader configuration 
key --skip 
bootloader --append="rhgb quiet" --location=mbr --driveorder=sda 
# Clear the Master Boot Record 
zerombr 
# Partition clearing information 
clearpart --all --initlabel 
# Disk partitioning information 
part / --fstype="ext4" --size=8192 
part swap --fstype="swap" --size=1024 
part /home --fstype="ext4" --size=2048

%packages 
@base

%end
```
说明：key --skip 如果是红帽系统，此选项可以跳过输入序列号过程；如果是CentOS 系列，则可以不保留此项内容；

reboot 此选项必须存在，也必须文中设定位置，不然kickstart显示一条消息，并等待用户按任意键后才重新引导；

clearpart --all --initlabel 此条命令必须添加，不然系统会让用户手动选择是否清除所有数据，这就需要人为干预了，从而导致自动化过程失败；


参考资料
---
- 使用PXE+DHCP+Apache+Kickstart无人值守安装CentOS5.8 x86_64 http://yuhongchun.blog.51cto.com/1604432/1100567
- CentOS 6.4下PXE+Kickstart无人值守安装操作系统 http://www.cnblogs.com/mchina/p/centos-pxe-kickstart-auto-install-os.html