 服务器 CPU 跑满，或者使用服务器越来越慢
====
From Aliyun [minerd  异常进程，占用了大量 CPU 资源](https://help.aliyun.com/knowledge_detail/41206.html)
问题原因
---
> 使用 top 命令看到有一个 minerd  异常进程，占用了大量 CPU 资源。
定位，该进程是一个挖矿程序，一般存在  /tmp/minerd 目录下。如果使用 top 查看不到，用 ps 命令可以找到相关进程。

处理方法
---
1. 使用类似如下命令通过 pid 获取对于文件的路径
``` shell
ls -l /proc/$PID/exe 

#$PID 为进程对应的 PID 号，可以通过前述说明，通过 ps 或者 top 获取
```
2. 使用 kill 命令关闭进程。
3. 删除步骤 1 获取的对应的文件。

最后，建议平时增强服务器的安全维护，优化代码，以避免因程序漏洞等导致服务器被入侵。


