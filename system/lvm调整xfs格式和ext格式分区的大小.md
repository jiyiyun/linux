centos7 调整XFS格式的LVM大小
---
前提：XFS是centos7 预装的操作系统，XFS只能扩大不能缩小，所以需要利用xfsdump / xfsrestore 工具在必须缩小lvm 的情况下，备份与还原资料。

```txt
本实验的效果是：
1，/dev/mapper/centos-home仅仅保留500G；
2，将/home分出来的空间分给/dev/mapper/centos-root。

step1：安裝 xfsdump 套件

# yum -y install xfsdump
step2：备份 /home

# xfsdump -f /home.xfsdump /home

    please enter label for this dump session (timeout in 300 sec)
    -> home
    please enter label for media in drive 0 (timeout in 300 sec)
    -> home

step3：缩减/dev/mapper/centos-home大小

卸載 /home
# umount /home

將 /home 的 Logical Volume 縮減為 5GB
# lvreduce -L 5G /dev/mapper/centos-home

    Do you really want to reduce home? [y/n]: y

step4：增加/dev/mapper/centos-root的空间大小

# lvextend -l +100%FREE /dev/centos/root

延展 xfs 空间
# xfs_growfs /dev/centos/root


step5：恢复/home的内容

格式化 /home 的 lvm
# mkfs.xfs -f /dev/mapper/centos-home

挂载 /home  /dev/mapper/centos-home
# mount /home

还原备份资料到 /home
# xfsrestore -f /home.xfsdump /home

注意：重新格式化/home目录，源文件会丢失，要把/home目录提前备份

```
参考资料
- [centos7 调整XFS格式的LVM大小] http://www.mykernel.cn/archives/499

ext 格式系统lvm调整大小 Ubuntu默认
---

```txt
2.卸载挂载分区

[root@localhost ~]# umount /home 

如果提示无法卸载，则是有进程占用/home，使用如下命令来终止占用进程： fuser -m -v -i -k /home

3.检查VolGroup-lv_home文件的错误性，-f   即使文件系统没有错误迹象，仍强制地检查正确性。

[root@localhost ~]# e2fsck -f /dev/mapper/VolGroup-lv_home 

4.调整/home为20G，

[root@localhost ~]# resize2fs -p /dev/mapper/VolGroup-lv_home 20G 

5.重新挂载并查看

[root@localhost ~]# mount /home 

[root@localhost ~]# df -h 

6.划分20G外面的剩余空间。使用lvreduce指令用于减少LVM逻辑卷占用的空间大小。可能会删除逻辑卷上已有的数据，所以在操作前必须进行确认。记得输入 “y”

[root@localhost ~]# lvreduce -L 20G /dev/mapper/VolGroup-lv_home 

8.使用lvextend指令：扩展逻辑卷空间到/dev/mapper/VolGroup-lv_root目录下，也就是“/”目录下。

[root@localhost ~]# lvextend -L +1.01T /dev/mapper/VolGroup-lv_root

9.执行操作，使之生效，中间一定要耐心等待。

[root@localhost ~]# resize2fs -p /dev/mapper/VolGroup-lv_root

```
参考资料
---
[linux调整lvm分区大小（/home分区过大，/root分区过小] http://tianshili.blog.51cto.com/5050423/1638563
[如何调整LVM 逻辑分区的大小？] http://www.linuxidc.com/Linux/2016-06/132709.htm