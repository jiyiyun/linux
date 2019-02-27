quota磁盘配额管理
---

```txt
作用: 显示磁盘已使用空间与限制
用法: quota [-选项][用户名称...] 或 quota[选项][群组名称]

主要选项如下
-g 列出群组的磁盘空间限制
-q 列出列表，只列出超限制部分
-u 列出用户的磁盘空间限制
-v 显示该用户或群组所有挂入系统的存储设备的空间限制
-V 显示版本信息

执行quota命令可以查询磁盘空间限制，并可知已使用多少空间

#quota USER_NAME

quotacheck 检查磁盘的使用空间与限制
作用: 检查磁盘的使用空间与限制
用法: quotacheck [-选项][文件系统]
-a 扫描在/etc/fstab文件里，有加入quota设置的分区
-d 显示详细的指令执行过程，便于排错
-g 扫描磁盘空间时，计算每个群组识别码所占用的目录和文件数
-R 排除根目录
-u 扫描磁盘空间时，计算每个用户识别码所占用的目录和文件数
-v 显示指令执行过程

#quotacheck -a

9 quotaoff 关闭磁盘空间限制
quotaoff [选项][文件系统]
-a 关闭在/etc/fstab 文件里加入quota设置的分区的空间限制
-g 关闭群组的磁盘空间限制
-u 关闭用户的磁盘空间限制
-v 显示指令执行过程

10 quotaon 开启磁盘空间限制
quotaon[选项][文件系统]
-a 开启在/etc/fstab文件里加入quata设置的分区空间限制
-g 开启群组磁盘空间限制
-u 开启用户磁盘空间限制
-v 显示指令执行过程

说明:开启quotaon前提是各分区的文件系统根目录必须有quota.user 和quotagroup文件
11 quotastats 显示磁盘空间限制
12 repquota 检查磁盘空间限制状态
-a 列出在/etc/fstab中设置分区使用情况
-g 列出群组的磁盘空间限制
-u 列出用户的磁盘空间限制
-v 显示指令执行过程

文件服务，FTP服务，E-Mail服务都要对用户可以使用的磁盘容量进行限制
相对于其它配额软件，quota具有基于内核优势
1)磁盘配额可以对每个用户磁盘使用情况进行追踪限制，这种追踪是利用文件或者文件夹所有权来实现
  的，当一个用户在linux ext 2/3/4分区上复制或者存储一个新的文件时，他就拥有对这个文件所有权
  ，磁盘配额程序将此文件大小计入该用户的磁盘配额空间
2)设置了磁盘配额以后，分析报告中所给出的剩余空间是当前这个用户的磁盘配额剩余空间，磁盘配额
  程序对每个分区的磁盘使用情况是独立跟踪控制的，无论它们是否位于同一块物理磁盘上
3)操作系统可以对磁盘配额进行检测，它可以扫描整个磁盘分区，检测每个用户对磁盘的使用情况，并用
  不同颜色标识出磁盘使用空间超过报警值和配额限制的用户
4)登录到相同计算机的多个用户不干涉其它用户的工作能力，一个或者多个用户不独占公用磁盘上的空间
  在个人计算机的共享文件夹中，用户不使用过多的磁盘空间

  磁盘配额管理提供了一种基于用户和分区的文件存储管理，使得管理员可以方便利用这个工具合理的分配存储资源，避免磁盘空间使用失控造成的系统崩溃

实现磁盘配额管理步骤
1)检查linux内核是否打开磁盘配额支持
2)修改/etc/fstab 对所选文件系统激活配额选项
3)更新装载文件系统，使改变生效
4)在该文件系统引导时建立aquota.user文件
5)扫描相应文件系统，用quotacheck命令生成基本配额文件
6)使用edquota命令，对特定用户采用配额限制
7)最后，用命令激活配额

(1)检查内核配置文件，是否支持quota 

[root@localhost ~]# grep CONFIG_QUOTA /boot/config-3.10.0-957.el7.x86_64
CONFIG_QUOTA=y
CONFIG_QUOTA_NETLINK_INTERFACE=y
# CONFIG_QUOTA_DEBUG is not set
CONFIG_QUOTA_TREE=y
CONFIG_QUOTACTL=y
CONFIG_QUOTACTL_COMPAT=y

有列出说明支持，如果当前内核不支持quota修改/etc/fstab 对所选文件系统激活配额选项，使用root
用户添加usrquota和(或)grpquota选项

   LABEL=/home   /home    ext3   defaults,usrquota 1 2

(2)重新挂载文件系统。在/etc/fstab中添加了usrquota和(或)grpquota后，重新挂载每个相应的fstab条目
   被修改的文件系统，如果该分区还没被使用，使用umount 接着mount重新挂载这个文件系统，如果正在
   使用，要重新挂载最简洁的方式是使用#mount -o remount /home
(3)在该文件系统上建立aquota.user文件
   #touch /home/aquota.user
   #chmod 600 /aquota
(4)扫描相应文件系统，用quotacheck命令生成基本配额文件，quotacheck命令检查启用了磁盘配额的
   文件系统，并为每个文件系统建立一个当前磁盘用表，该表被用来更新操作系统的磁盘用量文件，此外
   文件系统的磁盘配额文件也被更新，要在文件系统上创建磁盘配额文件(aquota.user aquota.group)
   使用quotacheck 命令的-c选项
   #quotacheck -acug /home
   -a 选项表明/etc/fstab中所有挂载了非NFS文件系统都被检查，以此来决定是否启用了配额
   -c 选项指定每个启用了配额管理的文件系统都应该创建配额文件
   -u 选项指定检查用户磁盘配额
   -g 选项指定检查群组磁盘配额
   如果-u -g选项被指定，则只有用户配额被创建，如果只有-g选项则只有群组配额文件被创建
   
   文件配额文件被创建后，运行如下命令生成每个启用磁盘配额的文件系统当前磁盘用量
   #quotacheck -avug
   -a 检查所有启用磁盘配额的本地挂载的文件系统
   -u 检查用户磁盘配额信息
   -g 检查群组磁盘配额信息
   -v 检查过程中显示详细状态信息
   quotacheck运行完毕后，和启用配额(用户和群组)相应的配额文件中就会写入用于每个启用了磁盘配额
   的文件系统(/home)的数据
   
   要定期运行quotacheck的方法是使用cron
   /etc/cron.hourly
   /etc/cron.daily
   /etc/cron.weekly
   /etc/cron.monthly
   
(5)使用edquota命令分配磁盘配额，要为用户配置配额，以root用户身份执行
    #edquota -u USER_NAME
	为每个需要实现配额的用户执行该步骤
	Filesystem：进行磁盘配额管理的系统
	blocks：已经使用的区块数量
	soft：block使用量的"软性"限制
	hard：block使用量的"硬性"限制
	inodes：已经使用的inode数量
	soft：inode使用量的"软性"限制
	hard：inode使用量的"硬性"限制
	
	edquota -t命令和edquota相似
	以上也可以使用setquota命令设置
	setquota -u  0 0 3 5 /dev/loop0
	setquota -t  864000 864000 /dev/loop0
	864000为10天的秒数
(6)磁盘配额设置好后，必须以命令quotaon -av命令启用配额管理

管理(维护)磁盘配额

创建磁盘配额报告使用repquota工具
要查看所有启用quota的文件系统磁盘用量，使用命令
#repquota -a

磁盘配额的启用和禁用
quotaoff -vaug
要重新启用使用
quotaon -vaug

要为指定文件系统启用配额
quotaon -vug /home

为群组启用磁盘配额
edquota -g GROUP

要校验群组配额是否被设置
quota -g GROUP

磁盘配额不但可以对用户容量进行限制，也可以对用户创建的文件数量限制iNode

如果不进行磁盘配额限制，在DDOS攻击时磁盘塞满会造成宕机，FTP服务器塞满垃圾文件，邮箱服务器
塞满垃圾邮件磁盘耗尽
```