git 报错:  fatal: 拒绝合并无关的历史
----
当远程github仓库和本地不一致的时候会报这样的错，执行下面命令，解决
``` shell
git pull origin master --allow-unrelated-histories 
```
