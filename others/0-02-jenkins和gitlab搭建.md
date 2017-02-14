Jenkins
===
``` shell
# docker run -it -d --name=jenkins --restart=always -p 8080:8080 -p 50000:50000 docker.io/library/jenkins:2.7.4

ERROR
Unlock Jenkins

To ensure Jenkins is securely set up by the administrator, a password has been written to the log (not sure where to find it?) and this file on the server:

/var/jenkins_home/secrets/initialAdminPassword

Please copy the password from either location and paste it below.
Administrator password


To Find The Password
---
# docker ps
CONTAINER ID        IMAGE                                      COMMAND                  CREATED             STATUS              PORTS                                              NAMES
d50760c5e7df        docker.io/library/jenkins:2.7.4

# docker logs d50
Running from: /usr/share/jenkins/jenkins.war
webroot: EnvVars.masterEnvVars.get("JENKINS_HOME")
Nov 15, 2016 12:02:43 PM org.eclipse.jetty.util.log.JavaUtilLog info
INFO: Logging initialized @1280ms
Nov 15, 2016 12:02:43 PM winstone.Logger logInternal
INFO: Beginning extraction from war file

*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

3e566cbe2a584c7db7544554eb069ac7

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

*************************************************************
```

gitlab
===
因为gitlab验证默认用22号端口，所以部署gitlab之前先要吧ssh 默认的22端口修改成其他
centos 系统
vi /etc/ssh/ssh_config
vi /etc/ssh/sshd_config

ubuntu 系统
vi /etc/ssh/ssh_config
vi /etc/ssh/sshd_config

``` shell
# docker run -it -d --name=gitlab --restart=always -p 80:80 -p 443:443 -p 22:22 docker.io/gitlab/gitlab-ce:v1.0.0:



登录GitLab
---
- Username: root 
- Password: 5iveL!fe

配置GitLab的默认发信邮箱
---
    GitLab中使用postfix进行邮件发送。因此，可以卸载系统中自带的sendmail。
    使用yum list installed查看系统中是否存在sendmail，若存在，则使用yum remove sendmail指令进行卸载。

    测试系统是否可以正常发送邮件。

    echo "Test mail from postfix" | mail -s "Test Postfix" xxx@xxx.com

    注：上面的xxx@xxx.com为你希望收到邮件的邮箱地址。

    当邮箱收到系统发送来的邮件时，将系统的地址复制下来，如：root@iZ23syflhhzZ.localdomain,打开/etc/gitlab/gitlab.rb,将

    # gitlab_rails['gitlab_email_from'] = 'gitlab@example.com'

    修改为

    gitlab_rails['gitlab_email_from'] = 'root@iZ23syflhhzZ.localdomain'

    保存后，执行sudo gitlab-ctl reconfigure重新编译GitLab。如果邮箱的过滤功能较强，请添加系统的发件地址到邮箱的白名单中，防止邮件被过滤。

       Note:系统中邮件发送的日志可通过`tail /var/log/maillog`命令进行查看。

[GitLab 简明安装配置指南](https://segmentfault.com/a/1190000002722631)https://segmentfault.com/a/1190000002722631