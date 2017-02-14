两个不同网站 linux管理多个ssh公钥密钥
===
```shell
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/id.rsa.gitlab.com.richard -C "richard818@qq.com"
```
当有多个ssh密钥需要管理时，一定要修改config文件的权限，否则你配置后仍然时无效的
- touch ~/.ssh/config
- chmod 600 ~/.ssh/config	

``` shell
~/.ssh/config文件的内容为：
Host github.com
    IdentityFile ~/.ssh/id_rsa.github
    User git
Host git.coding.net
    IdentityFile ~/.ssh/id_rsa.coding
    User git
 ```
其中User后面的值为你访问的git ssh地址的@之前的部分，比如：git@github.com:dongritengfei/beego.git的@前面是git，所以User后面的值为git。Host就是你的git仓库的域名或者IP。

然后是用这个命令来测试是否配置ok

```shell
ssh -T git@github.com
Welcome to GitHub, you name!

```
如果你看到这个就说明你ok了，如果你看到下面的样子：

``` shell
Bad owner or permissions on /home/admin/.ssh/config

```
那你需要执行：

``` shell
chmod 600 ~/.ssh/config
```
然后再试试应该就可以了。


同一个网站不同账号 解决ssh权限问题（）:
===
通常一台电脑生成一个ssh不会有这个问题，当一台电脑生成多个ssh的时候，就可能遇到这个问题，解决步骤如下：

1、查看系统ssh-key代理,执行如下命令
---
``` shell
$ ssh-add -l
```
　　以上命令如果输出  The agent has no identities. 则表示没有代理。如果系统有代理，可以执行下面的命令清除代理:
``` shell
$ ssh-add -D
```
2、然后依次将不同的ssh添加代理，执行命令如下：
---
``` shell
$ ssh-add ~/.ssh/id_rsa
$ ssh-add ~/.ssh/aysee
```
　你会分别得到如下提示：
``` shell
2048 8e:71:ad:88:78:80:b2:d9:e1:2d:1d:e4:be:6b:db:8e /Users/aysee/.ssh/id_rsa (RSA)
和
2048 8e:71:ad:88:78:80:b2:d9:e1:2d:1d:e4:be:6b:db:8e /Users/aysee/.ssh/id_rsa (RSA)
2048 a7:f4:0d:f1:b1:76:0b:bf:ed:9f:53:8c:3f:4c:f4:d6 /Users/aysee/.ssh/aysee (RSA)
```
如果使用 ssh-add ~/.ssh/id_rsa的时候报如下错误，则需要先运行一下 ssh-agent bash 命令后再执行 ssh-add ...等命令

- Could not open a connection to your authentication agent.

3、配置 ~/.ssh/config 文件
---
　　如果没有就在~/.ssh目录创建config文件，该文件用于配置私钥对应的服务器
``` shell
# Default github user(first@mail.com)
 
Host github.com
HostName github.com
User git
IdentityFile C:/Users/username/.ssh/id_rsa
 
# aysee (company_email@mail.com)
Host github-aysee
HostName github.com
User git
IdentityFile C:/Users/username/.ssh/aysee
```
-  Host随意即可，方便自己记忆，后续在添加remote是还需要用到。 
-  配置完成后，在连接非默认帐号的github仓库时，远程库的地址要对应地做一些修改，比如现在添加second帐号下的一个仓库test，则需要这样添加：

``` shell
git remote add test git@github-aysee:ay-seeing/test.git
```
并非原来的git@github.com:ay-seeing/test.git

```shell
　　ay-seeing 是github的用户名
```
4、测试 ssh
---
``` shell
ssh -T git@github.com
```
　　你会得到如下提示，表示这个ssh公钥已经获得了权限

``` shell
Hi USERNAME! You've successfully authenticated, but github does not provide shell access.
```
参考资料
---
- [生成多个git ssh密钥](http://www.cnblogs.com/ayseeing/p/4445194.html)
- [linux管理多个ssh公钥密钥](http://rongmayisheng.com/post/linux%E7%AE%A1%E7%90%86%E5%A4%9A%E4%B8%AAssh%E5%85%AC%E9%92%A5%E5%AF%86%E9%92%A5)