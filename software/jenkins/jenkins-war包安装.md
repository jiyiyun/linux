jenkins war包安装
---

1 . 官网下载war包

https://jenkins.io/index.html

2 . 安装jdk

```txt
rpm -ivh jdk-8u121-linux-x64.rpm
```

3 . 安装tomcat

```txt
yum install tomcat
```

4 . 将jenkins.war包放在tomcat的webapps目录底下,默认在/var/lib/tomcat/webapps

```txt
[root@localhost webapps]# pwd
/var/lib/tomcat/webapps
[root@localhost webapps]# ls
jenkins.war
```

5 . 重启tomcat

```
systemctl restart tomcat
```
重启tomcat后在/var/lib/tomcat/webapps自动生成jenkins文件夹

```txt
[root@localhost webapps]# ls
jenkins  jenkins.war
```
6 . 登录jenkins

```txt
http://192.168.100.65:8080/jenkins
```

7 . 填写密钥

```txt
Unlock Jenkins

To ensure Jenkins is securely set up by the administrator, a password has been written to the log (not sure where to find it?) and this file on the server:

/usr/share/tomcat/.jenkins/secrets/initialAdminPassword

Please copy the password from either location and paste it below.
```

8 . 找到密钥

```txt
[root@localhost webapps]# cat /usr/share/tomcat/.jenkins/secrets/initialAdminPassword
31735ba34a0843abb7348fc96dff3b06
[root@localhost webapps]# 
```
容器安装用docker logs Jenkins容器可以找到密钥