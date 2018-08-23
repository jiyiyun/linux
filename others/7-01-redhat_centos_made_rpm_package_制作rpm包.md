制作rpm包
---

制作openssh rpm包

1.配置好编译机的环境

```txt
mkdir -pv /root/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS,TMP}
yum -y install  tcp_wrappers tcp_wrappers-devel tcp_wrappers-libs openssl
```
2.制作rpm

```txt
cd /root/rpmbuild/SOURCES/.
wget http://mirror.team-cymru.org/pub/OpenBSD/OpenSSH/portable/openssh-6.6p1.tar.gz
wget http://mirror.team-cymru.org/pub/OpenBSD/OpenSSH/portable/openssh-6.6p1.tar.gz.asc

cd ../SPECS/
tar xfz ../SOURCES/openssh-6.6p1.tar.gz openssh-6.6p1/contrib/redhat/openssh.spec
mv openssh-6.6p1/contrib/redhat/openssh.spec openssh-6.6p1.spec
rm -rf openssh-6.6p1
sed -i -e "s/%define no_gnome_askpass 0/%define no_gnome_askpass 1/g" openssh-6.6p1.spec
sed -i -e "s/%define no_x11_askpass 0/%define no_x11_askpass 1/g" openssh-6.6p1.spec
sed -i -e "s/BuildPreReq/BuildRequires/g" openssh-6.6p1.spec
chown 74:74 openssh-6.6p1.spec

rpmbuild -ba openssh-6.6p1.spec
```
3.如无意外就制作好了

```txt
[root@compiler SPECS]# ll ../RPMS/x86_64/openssh-* 
-rw-r--r-- 1 root root 417244 Jul 12 12:39 ../RPMS/x86_64/openssh-6.6p1-1.x86_64.rpm
-rw-r--r-- 1 root root 547696 Jul 12 12:39 ../RPMS/x86_64/openssh-clients-6.6p1-1.x86_64.rpm
-rw-r--r-- 1 root root  17020 Jul 12 12:39 ../RPMS/x86_64/openssh-debuginfo-6.6p1-1.x86_64.rpm
-rw-r--r-- 1 root root 374256 Jul 12 12:39 ../RPMS/x86_64/openssh-server-6.6p1-1.x86_64.rpm
```