磁盘扩容
===

``` shell
root@ubuntu:/home/richard# fdisk -l|grep  /dev/sd                      #查看LVM
Disk /dev/sda: 80 GiB, 85899345920 bytes, 167772160 sectors
/dev/sda1  *       2048   999423   997376  487M 83 Linux
/dev/sda2       1001470 62912511 61911042 29.5G  5 Extended
/dev/sda5       1001472 62912511 61911040 29.5G 8e Linux LVM
```

```txt
root@ubuntu:/home/richard# fdisk /dev/sda 

备注
在原来硬盘上增加容量用    fdisk /dev/sda

如果是新增硬盘用          fdisk /dev/sdb
第三块硬盘就是sdc 第四块就是sdd，以此类推
```

```txt
Welcome to fdisk (util-linux 2.27.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition type
   p   primary (2 primary, 1 extended, 1 free)
   l   logical (numbered from 5)
Select (default p): 

Using default response p.
Selected partition 4
First sector (62912512-167772159, default 62912512): 
Last sector, +sectors or +size{K,M,G,T,P} (62912512-167772159, default 167772159): 

Created a new partition 4 of type 'Linux' and of size 50 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Re-reading the partition table failed.: Device or resource busy

The kernel still uses the old table. The new table will be used at the next reboot or after you run partprobe(8) or kpartx(8).
```

```txt
这一步有时候不做也可以
root@ubuntu:/home/richard# partprobe                                       #重新计算容量
```

```txt
root@ubuntu:/home/richard# fdisk -l
Disk /dev/sda: 80 GiB, 85899345920 bytes, 167772160 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x904d67f5

Device     Boot    Start       End   Sectors  Size Id Type
/dev/sda1  *        2048    999423    997376  487M 83 Linux
/dev/sda2        1001470  62912511  61911042 29.5G  5 Extended
/dev/sda3         999424   1001469      2046 1023K 83 Linux
/dev/sda4       62912512 167772159 104859648   50G 83 Linux                   #新增容量到了/dev/sda4
/dev/sda5        1001472  62912511  61911040 29.5G 8e Linux LVM

root@ubuntu:/home/richard# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        401M  5.9M  395M   2% /run
/dev/mapper/ubuntu--vg-root   28G  1.4G   26G   6% /                            #还没有增加
tmpfs                        2.0G     0  2.0G   0% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M   55M  393M  13% /boot
tmpfs                        100K     0  100K   0% /run/lxcfs/controllers
tmpfs                        401M     0  401M   0% /run/user/1000
```

```txt
已经有lvm这一步可以不用

root@ubuntu:/home/richard# pvcreate /dev/sda4                                 #创建物理卷,已经有lvm的使用vgdisplay查看vg名称
  Physical volume "/dev/sda4" successfully created
```

使用vgdisplay查看逻辑卷组名称

使用lvdisplay 查看逻辑卷名称

```txt
将新增的分区加入到逻辑卷组 vg

root@ubuntu:/home/richard# vgextend ubuntu-vg /dev/sda4                       #先把新分区拓展到vg 再添加到lv，lv名称用lvdisplay查看
  Volume group "ubuntu-vg" successfully extended
root@ubuntu:/home/richard# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        401M  5.9M  395M   2% /run
/dev/mapper/ubuntu--vg-root   28G  1.4G   26G   6% /
tmpfs                        2.0G     0  2.0G   0% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M   55M  393M  13% /boot
tmpfs                        100K     0  100K   0% /run/lxcfs/controllers
tmpfs                        401M     0  401M   0% /run/user/1000

给逻辑卷lv增加容量:可以给不同的lv增加不同的容量，也可以先给不同的VG分配不同的容量再给不同的lv分配不同的容量

root@ubuntu:/home/richard# lvextend -L +50G /dev/mapper/ubuntu--vg-root         #拓展lv容量,
  Size of logical volume ubuntu-vg/root changed from 28.52 GiB (7301 extents) to 78.52 GiB (20101 extents).
  Logical volume root successfully resized.
root@ubuntu:/home/richard# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        401M  5.9M  395M   2% /run
/dev/mapper/ubuntu--vg-root   28G  1.4G   26G   6% /
tmpfs                        2.0G     0  2.0G   0% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M   55M  393M  13% /boot
tmpfs                        100K     0  100K   0% /run/lxcfs/controllers
tmpfs                        401M     0  401M   0% /run/user/1000

给lv分配好容量再重新计算lv大小
root@ubuntu:/home/richard# resize2fs /dev/mapper/ubuntu--vg-root               #格式化虚拟分区
resize2fs 1.42.13 (17-May-2015)
Filesystem at /dev/mapper/ubuntu--vg-root is mounted on /; on-line resizing required
old_desc_blocks = 2, new_desc_blocks = 5
The filesystem on /dev/mapper/ubuntu--vg-root is now 20583424 (4k) blocks long.
```
调整好了，查看调整后的容量

```txt
root@ubuntu:/home/richard# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        401M  5.9M  395M   2% /run
/dev/mapper/ubuntu--vg-root   78G  1.4G   73G   2% /
tmpfs                        2.0G     0  2.0G   0% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M   55M  393M  13% /boot
tmpfs                        100K     0  100K   0% /run/lxcfs/controllers
tmpfs                        401M     0  401M   0% /run/user/1000
```
