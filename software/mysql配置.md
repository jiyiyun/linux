mysql配置
---
``` shell
[root@centos73 ~]# iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
[root@centos73 ~]# firewall-cmd --permanent --zone=public --add-service=mysql
success
[root@centos73 ~]# firewall-cmd --permanent --zone=public --add-port=3306/tcp
success
[root@centos73 ~]# mysqladmin -V
mysqladmin  Ver 9.0 Distrib 5.5.52-MariaDB, for Linux on x86_64

初始化mariadb
[root@centos73 ~]# mysql_secure_installation

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user.  If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none): 
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] y

New password: 
Re-enter new password: 
Password updated successfully!
Reloading privilege tables..
 ... Success!


By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] y
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
```
mysql 修改密码
---
``` shell
[root@centos73 ~]# mysqladmin -u root -p password y    #password 后面的y是新密码
Enter password:                                        #这里输入以前的密码
```
修改密码的另一种方式
---
``` shell
[root@centos73 ~]# mysqladmin -u root -p old-password t  #old-password后面是新密码
Enter password:                                          #这里是旧密码
```
mysql配置文件/etc/mysql/my.cnf
---

使用mysqladmin进行数据库操作
---
mysqladmin是一个可以执行管理操作的程序,检查服务器的配置和当前状态，创建并删除数据库等
- create db_name
``` shell
root@ubuntu:~# mysqladmin create testing -u root -p
Enter password:

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| testing            |
+--------------------+
4 rows in set (0.05 sec)
```
- mysqladmin drop db_name 删除数据库
``` shell
root@ubuntu:~# mysqladmin  drop testing -u root -p
Enter password: 
Dropping the database is potentially a very bad thing to do.
Any data stored in the database will be destroyed.

Do you really want to drop the 'testing' database [y/N] y
Database "testing" dropped
root@ubuntu:~# 
```
查看mysql状态mysqladmin proc stat
---
``` shell
root@ubuntu:~# mysqladmin proc stat -u root -p
Enter password: 
+----+------+-----------+----+---------+------+-------+------------------+
| Id | User | Host      | db | Command | Time | State | Info             |
+----+------+-----------+----+---------+------+-------+------------------+
| 38 | root | localhost |    | Query   | 0    |       | show processlist |
+----+------+-----------+----+---------+------+-------+------------------+
Uptime: 1245  Threads: 1  Questions: 112  Slow queries: 0  Opens: 48  Flush tables: 1  Open tables: 41  Queries per second avg: 0.089

Uptime     服务器已经运行的秒数
Threads    活动线程(客户)数
Questions  服务器启动以来查询的的次数
Slow queries  超过long_query_time秒的查询数量
Opens         服务器已经打开的数据库表的数量
Open tables   目前已经打开的表的数量

使用--with-debug=full编译的Mysql 显示
Memory in use
Maximum memory used:
```

添加用户
---
两种方法 1. 使用GRANT 语句, 2 ，直接操作Mysql 授权表

``` shell
mysql> grant all privileges on *.* to 'test'@'localhost' identified by 'test' with grant option;
Query OK, 0 rows affected (0.00 sec)

mysql> grant all privileges on *.* to 'test'@'%' identified by 'test' with grant option;
Query OK, 0 rows affected (0.00 sec)

```
Ubuntu 14.04设置防火墙
---
``` shell
root@ubuntu:~# ufw allow 3306/tcp
Rules updated
Rules updated (v6)

root@ubuntu:~# ufw status
Status: inactive

root@ubuntu:~# ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
root@ubuntu:~# ufw allow 22/tcp
Rule added
Rule added (v6)

root@ubuntu:~# ufw disable
Firewall stopped and disabled on system startup

```

