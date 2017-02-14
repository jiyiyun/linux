Marathon
===
Marathon 是一套用于在 Mesos 之上运行长期运行应用程序或者服务的框架。这些应用程序具备高可用性要求，这意味着 Marathon 能够监控并在遭遇故障时以自动化方式重启应用实例，且可以通过弹性方式实现应用规模扩展。Marathon 亦能够运行其它框架，具体包括 Hadoop 以及 Marathon 自身。典型的 Marathon 使用工作流为在集群之内运行 N 个同一应用程序实例，且每个应用实例都需要配备 1 个处理器与 1 GB 内存容量。大家可以向 Marathon 提交请求以创建 N 个运行在各从节点之上的 Mesos 任务。

Marathon 提供一套具象状态传输（简称 REST）API 用于对服务进行启动、终止以及扩展。其同时提供基于浏览器的 GUI 与命令行客户端。其能够以高可用性方式运行在多个 Marathon 实例当中。

参考资料
---
[在 RHEL 7.1 上设置 Mesos/Marathon 集群](http://blog.csdn.net/linuxnews/article/details/53027421) http://blog.csdn.net/linuxnews/article/details/53027421
