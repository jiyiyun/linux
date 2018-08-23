git 设置
===

- git 的配置文件在.git/config中
- 一定要设置成为git@形式的才能免密码认证

``` shell
$ git remote add origin git@192.168.100.10:richard/test.git
$ git branch --set-upstream-to=origin/master master
```
