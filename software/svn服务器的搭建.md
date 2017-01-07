svn 服务器的搭建
---
1. 安装svnversion
---
``` txt
  206  yum install svn
  207  yum install mariadb-server
  208  yum install httpd mod_davsvn mod_perl
  209  yum install wget gcc-c++ make unzip perl*
  210  yum install wget gcc-c++ make unzip perl
  211  yum install gcc
  212  yum install ntsysv vim
```
2. 创建好服务端
---
```txt
  245  cd /opt/                         #进入opt目录
  246  ls
  247  mkdir svn                        #创建svn文件夹
  248  svnadmin create svn/project      #初始化
  249  cd                               #返回用户自己的目录
  253  mkdir project project/server project/client project/test       #创建临时目录
  254  ls
  256  svn import project/ file:///opt/svn/project -m "init svn dir"  #将临时目录导入到svn服务器
  257  rm -rf project/                  #删除临时目录
```
3. 配置svn配置文件
---
``` txt
  259  vi /opt/svn/project/conf/passwd            #配置用户名和密码
  260  vi /opt/svn/project/conf/authz             #配置项目的rw权限
  261  vi /opt/svn/project/conf/svnserve.conf     #配置免密码，密码,授权文件路径
  262  chmod -R 777 /opt/svn/                     #设置文件权限
  263  svnserve -d -r /opt/svn/                   #启动svn服务

 [root@centos ~]# cat /opt/svn/project/conf/passwd 
### This file is an example password file for svnserve.
### Its format is similar to that of svnserve.conf. As shown in the
### example below it contains one section labelled [users].
### The name and password for each user follow, one account per line.

[users]
# harry = harryssecret
# sally = sallyssecret

pm = pm_pw
server_group = server_pw
client_group = client_pw
test_group = test_pw

[root@centos ~]# cat /opt/svn/project/conf/authz 
### This file is an example authorization file for svnserve.

[aliases]
# joe = /C=XZ/ST=Dessert/L=Snake City/O=Snake Oil, Ltd./OU=Research Institute/CN=Joe Average

[groups]
# harry_and_sally = harry,sally
# harry_sally_and_joe = harry,sally,&joe

# [/foo/bar]
# harry = rw
# &joe = r
# * =

# [repository:/baz/fuz]
# @harry_and_sally = rw
# * = r
#
[groups]
project_p = pm
project_s = server_group
project_c = client_group
project_t = test_group
       
[project:/]
@project_p = rw
* =
                     
[project:/server]
@project_p = rw
@project_s = rw
* =
                      
[project:/client]
@project_p = rw
@project_c = rw
* =
                    
[project:/doc]
@project_p = rw
@project_s = rw
@project_c = rw
@project_t = rw
*  =

[root@centos ~]# cat /opt/svn/project/conf/svnserve.conf 
### This file controls the configuration of the svnserve daemon, if you
### use it to allow access to this repository.

# anon-access = read
# auth-access = write
anon-access = none
auth-access = write

# password-db = passwd
password-db = /opt/svn/project/conf/passwd


# authz-db = authz
authz-db = /opt/svn/project/conf/authz
[root@centos ~]# 
```
4. 在ubutnu Desktop 测试
---
``` txt
rich@ubuntu:~$ svn co svn://192.168.100.132/project


Authentication realm: <svn://192.168.100.132:3690> fbeebbba-eaaa-446c-8145-b8d4f2699c6d

Username: pm

Password for 'pm': *****


A    project/client

A    project/test

A    project/server

Checked out revision 1.

rich@ubuntu:~$ ls

Desktop    Downloads  id_rsa.pub  Pictures  Public  Videos
Documents  examples.desktop  Music project   Templates

rich@ubuntu:~$ cd project/

rich@ubuntu:~/project$ ls

client  server  test

```
5. 参考资料
---
[linux下搭建SVN服务器完全手册] http://www.cnblogs.com/wrmfw/archive/2011/09/08/2170465.html