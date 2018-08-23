git设置多个SSH-KEY
===
1、生成一个公司用的SSH-Key

``` shell
root@mesos1:~# ssh-keygen -t rsa -f ~/.ssh/gitlab.rsa -C "test@gitlab.com"

root@mesos1:~# ssh-keygen -t rsa -f ~/.ssh/github.rsa -C "test@github.com"
```
在~/.ssh/目录会生成id-rsa和id-rsa.pub私钥和公钥。
- 将gitlab.rsa.pub中的内容粘帖到公司gitlab服务器的SSH-key的配置中。
- 将github.rsa.pub中的内容粘帖到公司github服务器的SSH-key的配置中。

2、添加私钥,(ssh key分为公钥和私钥，要把私钥添加到本地，公钥添加到gitlab和github)
---

``` shell
root@mesos1:~/.ssh# ls
github.rsa  github.rsa.pub  gitlab.rsa  gitlab.rsa.pub

root@mesos1:~/.ssh# ssh-add -l
The agent has no identities.                   #还是空的没有添加私钥

root@mesos1:~/.ssh# ssh-add gitlab.rsa
Identity added: gitlab.rsa (gitlab.rsa)        #gitlab私钥已添加

root@mesos1:~/.ssh# ssh-add github.rsa
Identity added: github.rsa (github.rsa)        #github私钥已经添加

```
如果执行ssh-add时提示"Could not open a connection to your authentication agent"，可以现执行命令：

``` shell
Could not open a connection to your authentication agent.
root@mesos1:~/.ssh# ssh-agent bash
```
3、检查私钥添加好了没有
---

``` shell
ssh-add -l 显示已经添加好的私钥列表
root@mesos1:~/.ssh# ssh-add -l
2048 75:4c:14:27:37:c6:42:e8:65:a4:f1:e2:ef:9e:37:74 gitlab.rsa (RSA)
2048 8f:08:fe:bf:fb:0a:07:5a:b3:2b:5b:58:55:b0:64:4b github.rsa (RSA)

ssh-add -D  清空以添加的私钥
```
4、创建配置文件
---
在 ~/.ssh 目录下新建一个config文件

``` shell
root@mesos1:~/.ssh# vi config

# gitlab
Host gitlab.com
    HostName gitlab.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/gitlab.rsa
# github
Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/github.rsa
```
5、测试添加好了没有
---

``` shell
root@mesos1:~/.ssh# ssh -T git@github.com
```
Hi richard! You've successfully authenticated, but GitHub does not provide shell access.
就表示成功的连上github了.也可以试试链接公司的gitlab.

参考资料
---
[git 配置多个SSH-Key](https://my.oschina.net/stefanzhlg/blog/529403)https://my.oschina.net/stefanzhlg/blog/529403

