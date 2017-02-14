mesos配置
===
Apache Mesos基本术语
---
- (1) Mesos-master: mesos master,主要负责管理各个framework和slave ，并将slave上的资源分配给framwork
- (2) Mesos-slave : 负责管理本节点上各个mesos-task ,比如为各个executor分配资源
- (3) Framework : 计算框架，如：Hadoop,Spark等，通过MesosSchedulerDriver接入Mesos
- (4) Executer : 执行器，安装到mesos-slave上，用于启动计算框架task
当用户试图添加一种新的计算框架到Mesos中时，需要实现一个Framework scheduler和executor以接入Mesos。

总体架构
---
Apache Mesos由四个组件组成，分别是Mesos-master，mesos-slave，framework和executor。

Mesos-master是整个系统的核心，负责管理接入mesos的各个framework（由frameworks_manager管理）和slave（由slaves_manager管理），并将slave上的资源按照某种策略分配给framework（由独立插拔模块Allocator管理）。

Mesos-slave负责接收并执行来自mesos-master的命令、管理节点上的mesos-task，并为各个task分配资源。mesos-slave将自己的资源量发送给mesos-master，由mesos-master中的Allocator模块决定将资源分配给哪个framework，当前考虑的资源有CPU和内存两种，也就是说，mesos-slave会将CPU个数和内存量发送给mesos-master，而用户提交作业时，需要指定每个任务需要的CPU个数和内存量，这样，当任务运行时，mesos-slave会将任务放到包含固定资源的linux container中运行，以达到资源隔离的效果。很明显，master存在单点故障问题，为此，mesos采用了zookeeper解决该问题。

Framework是指外部的计算框架，如Hadoop，Mesos等，这些计算框架可通过注册的方式接入mesos，以便mesos进行统一管理和资源分配。Mesos要求可接入的框架必须有一个调度器模块，该调度器负责框架内部的任务调度。当一个framework想要接入mesos时，需要修改自己的调度器，以便向mesos注册，并获取mesos分配给自己的资源， 这样再由自己的调度器将这些资源分配给框架中的任务，也就是说，整个mesos系统采用了双层调度框架：第一层，由mesos将资源分配给框架；第二层，框架自己的调度器将资源分配给自己内部的任务。当前Mesos支持三种语言编写的调度器，分别是C++，java和python，为了向各种调度器提供统一的接入方式，Mesos内部采用C++实现了一个MesosSchedulerDriver（调度器驱动器），framework的调度器可调用该driver中的接口与Mesos-master交互，完成一系列功能（如注册，资源分配等）。

Executor主要用于启动框架内部的task。由于不同的框架，启动task的接口或者方式不同，当一个新的框架要接入mesos时，需要编写一个executor，告诉mesos如何启动该框架中的task。为了向各种框架提供统一的执行器编写方式，Mesos内部采用C++实现了一个MesosExecutorDiver（执行器驱动器），framework可通过该驱动器的相关接口告诉mesos启动task的方法。
![mesos arch](http://dongxicheng.org/wp-content/uploads/2012/04/mesos-arch.jpg)

![mesos 总体框架](http://mesos.apache.org/assets/img/documentation/architecture3.jpg)

1. 按照官方文档编译mesos
http://mesos.apache.org/documentation/latest/getting-started/

2. 按赵官方文档测试。
- mesos默认安装路径

``` shell
root@mesos1:/usr/local/sbin# ls
mesos-agent      mesos-slave             mesos-start-masters.sh  mesos-stop-cluster.sh
mesos-daemon.sh  mesos-start-agents.sh   mesos-start-slaves.sh   mesos-stop-masters.sh
mesos-master     mesos-start-cluster.sh  mesos-stop-agents.sh    mesos-stop-slaves.sh
```
- mesos 配置文件路径

``` shell
root@mesos1:/usr/local/etc/mesos# ls
mesos-agent-env.sh.template  mesos-deploy-env.sh.template  mesos-master-env.sh.template  mesos-slave-env.sh.template
```
3. 配置mesos集群
---
1. 测试环境
- master(master)           192.168.100.11
- resourcemanager(slave)   192.168.100.12
- datanode1(slave)         192.168.100.13

4.配置mesos-master-env.sh
---
* mesos-start-masters.sh：用于SSH登录到各个master并且进行start操作，如果单机执行，只需注释跟SSH相关操作(直接通过daemon mesos-master启动)
* mesos-stop-master.sh：用于SSH登录到各个master，并且进行stop操作，如果单机执行，只需注释SSH相关操作(直接执行killall mesos-master)
* mesos-daemon.sh：用于启动mesos daemon，默认会执行一些动作(设置ulimit -n以及启动对应的环境变量设置/usr/local/etc/PROCNAME-env.sh)
* mesos-agent实际的二进制文件，可以通过--help来查看对应参数，参数参考：http://mesos.apache.org/documentation/latest/configuration
* /usr/local/etc/mesos/mesos-master-env.sh：设置mesos环境变量，变量命名规则为MESOS_参数，其中{参数}为mesos-master --help中的参数，设置如下

``` shell
    export MESOS_log_dir=/var/log/mesos/master   # 设置日志目录
    export MESOS_work_dir=/var/run/mesos/master  # 设置work目录，会存放一些运行信息
    export MESOS_ip=127.0.0.1                    # 设置IP
    # export MESOS_port=5050                     # 设置PORT，默认是5050
    export MESOS_CLUSTER=mesos_test_cluster1     # 设置集群名称
    export MESOS_hostname=127.0.0.1              # 设置master hostname
    export MESOS_logging_level=INFO              # 设置日志级别
    export MESOS_offer_timeout=60secs            # 设置offer的超时时间
    # export MESOS_agent_ping_timeout=15         # 设置ping 超时时间，默认15s
    # export MESOS_allocation_interval=1         # 设置资源 allocation间隔，默认1s
注意：offer_timeout非常关键，默认是不超时，如果一个offer发给scheduler后scheduler不做任何处理(acceptOffers或者declineOffer)，那么这个offer一直会被这个scheduler给占用了，直到scheduler自己结束进程或者退出注册。所以offer_timeout一般要设置，用于防止由于scheduler自身的问题(偶发性hang住，或者程序问题没有处理offer)导致资源无法利用
```

``` shell
root@mesos1:/usr/local/etc/mesos# cp mesos-master-env.sh.template mesos-master-env.sh          
root@mesos1:/usr/local/etc/mesos# vi mesos-master-env.sh

# This file contains environment variables that are passed to mesos-master.
# To get a description of all options run mesos-master --help; any option
# supported as a command-line option is also supported as an environment
# variable.

# Some options you're likely to want to set:
# export MESOS_log_dir=/var/log/mesos
export MESOS_log_dir=/var/log/mesos/master
export MESOS_work_dir=/var/lib/mesos/master
export MESOS_ip=192.168.100.11
# export MESOS_port=5050
export MESOS_CLUSTER=mesos_cluster1
export MESOS_hostname=mesos1
export MESOS_logging_level=INFO
export MESOS_offer_timeout=60secs
# export MESOS_agent_ping_timeout=15
# export MESOS_allocation_interval=1
```
5、配置mesos-agent
---
* mesos-start-agent.sh：用于SSH登录到各个agent并且进行start操作，如果单机执行，只需注释跟SSH相关操作(直接通过daemon mesos-agent启动)
* mesos-stop-agent.sh：用于SSH登录到各个agent，并且进行stop操作，如果单机执行，只需注释SSH相关操作(直接执行killall mesos-agent)
* mesos-daemon.sh：用于启动mesos daemon，默认会执行一些动作(设置ulimit -n以及启动对应的环境变量设置/usr/local/etc/PROCNAME-env.sh)
* mesos-agent实际的二进制文件，可以通过--help来查看对应参数，参数参考：http://mesos.apache.org/documentation/latest/configuration/
* /usr/local/etc/mesos/mesos-agent-env.sh：设置mesos-agent环境变量，变量命名规则为MESOS_参数，其中{参数}为mesos-agent --help中的参数，设置如下：

``` shell
# The mesos master URL to contact. Should be host:port for
# non-ZooKeeper based masters, otherwise a zk:// or file:// URL.
export MESOS_master=172.24.133.164:5050

# Other options you're likely to want to set:
export MESOS_ip=172.24.133.164
export MESOS_port=5051
export MESOS_hostname=mesos_cl_agent164
export MESOS_log_dir=/var/log/mesos/agent
export MESOS_work_dir=/var/run/mesos/agent
export MESOS_logging_level=INFO
export MESOS_isolation=cgroups
```

``` shell
root@mesos3:/usr/local/etc/mesos# cp mesos-agent-env.sh.template mesos-agent-env.sh
root@mesos3:/usr/local/etc/mesos# vi mesos-agent-env.sh

export MESOS_master=192.168.100.11:5050
export MESOS_ip=192.168.100.12
export MESOS_port=5051
export MESOS_hostname=mesos2
export MESOS_log_dir=/var/log/mesos/agent
export MESOS_work_dir=/var/run/mesos/agent
export MESOS_logging_level=INFO

```
6. 配置slave

``` shell
# To get a description of all options run mesos-agent --help; any option
# supported as a command-line option is also supported as an environment
# variable.

# You must at least set MESOS_master.

# The mesos master URL to contact. Should be host:port for
# non-ZooKeeper based masters, otherwise a zk:// or file:// URL.
#export MESOS_master=unknown-machine:5050

# Other options you're likely to want to set:
# export MESOS_log_dir=/var/log/mesos
# export MESOS_work_dir=/var/run/mesos
# export MESOS_isolation=cgroups

export MESOS_master=192.168.100.11:5050
export MESOS_ip=192.168.100.13
export MESOS_port=5051
export MESOS_hostname=mesos3
export MESOS_log_dir=/var/log/mesos/slave
export MESOS_work_dir=/var/run/mesos/slave
export MESOS_logging_level=INFO
export MESOS_isolation=cgroups
```
7. 启动
===
1. mesos-master
---
* 执行sh mesos-start-masters.sh
* ps aux | grep mesos-master 能看到master进程
* netstat -nltp | grep mesos，能看到master已经绑定5050端口
* 查看http://127.0.0.1:5050，可以看到当前mesos集群的一些状态

2. mesos-agent
---

* 执行sh mesos-start-agents.sh
* ps aux | grep mesos-agent 能看到agent进程
* netstat -nltp | grep mesos，能看到agent已经绑定5051端口
* 查看http://127.0.0.1:5050，可以看到当前mesos集群的一些状态，同时看到对应的agent

3. mesos-slave
---
* 执行sh mesos-start-slaves.sh
* ps aux | grep mesos-slaves 能看到agent进程
* netstat -nltp | grep mesos，能看到agent已经绑定5051端口
* 查看http://127.0.0.1:5050，可以看到当前mesos集群的一些状态，同时看到对应的slaves

附录:设置SSH KEY免密钥登录
---
现在设置master免秘钥登录mesos2和mesos3
``` shell
root@mesos1:~/.ssh# ssh-keygen -t rsa -f ~/.ssh/mesos1.rsa -C "mesos1"
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/mesos1.rsa.
Your public key has been saved in /root/.ssh/mesos1.rsa.pub.
The key fingerprint is:
4e:84:23:1e:7b:d5:18:81:b8:36:dc:11:17:a7:ad:80 mesos1
The key's randomart image is:
+--[ RSA 2048]----+
|     ..o=o.      |
|    ..oo B       |
|   .Eo+.= o      |
|   .=+.= .       |
|   .o.. S        |
|     . o         |
|        .        |
|                 |
|                 |
+-----------------+
root@mesos1:~/.ssh# ll
total 32
drwx------ 2 root root 4096 Nov 22 17:27 ./
drwx------ 6 root root 4096 Nov 22 17:22 ../
-rw-r--r-- 1 root root  776 Nov 22 17:24 authorized_keys
-rw-r--r-- 1 root root  444 Nov 22 17:24 known_hosts
-rw------- 1 root root 1675 Nov 22 17:27 mesos1.rsa
-rw-r--r-- 1 root root  388 Nov 22 17:27 mesos1.rsa.pub

root@mesos1:~/.ssh# ssh-add -l
Could not open a connection to your authentication agent.

root@mesos1:~/.ssh# ssh-agent bash
root@mesos1:~/.ssh# ssh-add -l
The agent has no identities.

root@mesos1:~/.ssh# ssh-add mesos1.rsa
Identity added: mesos1.rsa (mesos1.rsa)

root@mesos1:~/.ssh# scp mesos1.rsa.pub 192.168.100.12:/root/.ssh/
root@192.168.100.12's password: 
mesos1.rsa.pub                                                                         100%  388     0.4KB/s   00:00    
root@mesos2:~/.ssh# cat mesos1.rsa.pub >> authorized_keys             ##写入mesos3的授权文件

root@mesos1:~/.ssh# scp mesos1.rsa.pub 192.168.100.13:/root/.ssh/
root@192.168.100.13's password: 
mesos1.rsa.pub                                                                         100%  388     0.4KB/s   00:00    
root@mesos3:~/.ssh# cat mesos1.rsa.pub >> authorized_keys             #写入mesos3的授权文件

root@mesos1:~/.ssh# ssh 192.168.100.12
root@mesos2:~# exit

root@mesos1:~/.ssh# ssh 192.168.100.13

```
4 、mesos目录
---
``` shell
# ls /usr/local/include/mesos/
appc            authorizer     executor      hook.hpp     master      mesos.proto  quota          scheduler      type_utils.hpp  values.hpp
attributes.hpp  containerizer  executor.hpp  http.hpp     mesos.hpp   module       resources.hpp  scheduler.hpp  uri             version.hpp
authentication  docker         fetcher       maintenance  mesos.pb.h  module.hpp   roles.hpp      slave          v1
```

参考资料
---
[mesos 学习笔记1 -- mesos安装和配置](http://www.cnblogs.com/SailorXiao/p/5786781.html) http://www.cnblogs.com/SailorXiao/p/5786781.html
