CentOS系统
===
``` shell
[root@localhost ~]# fdisk -l

磁盘 /dev/sda：53.7 GB, 53687091200 字节，104857600 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x00030c61

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     1026047      512000   83  Linux
/dev/sda2         1026048    67108863    33041408   8e  Linux LVM

磁盘 /dev/mapper/centos-root：31.6 GB, 31637635072 字节，61792256 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节


磁盘 /dev/mapper/centos-swap：2147 MB, 2147483648 字节，4194304 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节

[root@localhost ~]# fdisk -l|grep /dev/sd
磁盘 /dev/sda：53.7 GB, 53687091200 字节，104857600 个扇区
/dev/sda1   *        2048     1026047      512000   83  Linux
/dev/sda2         1026048    67108863    33041408   8e  Linux LVM
[root@localhost ~]# fdisk /dev/sda
欢迎使用 fdisk (util-linux 2.23.2)。

更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。


命令(输入 m 获取帮助)：n
Partition type:
   p   primary (2 primary, 0 extended, 2 free)
   e   extended
Select (default p): 
Using default response p
分区号 (3,4，默认 3)：
起始 扇区 (67108864-104857599，默认为 67108864)：
将使用默认值 67108864
Last 扇区, +扇区 or +size{K,M,G} (67108864-104857599，默认为 104857599)：
将使用默认值 104857599
分区 3 已设置为 Linux 类型，大小设为 18 GiB

命令(输入 m 获取帮助)：w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: 设备或资源忙.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
正在同步磁盘。
[root@localhost ~]# partprobe
[root@localhost ~]# df -h
文件系统                 容量  已用  可用 已用% 挂载点
/dev/mapper/centos-root   30G  1.4G   29G    5% /
devtmpfs                 910M     0  910M    0% /dev
tmpfs                    920M     0  920M    0% /dev/shm
tmpfs                    920M  8.5M  912M    1% /run
tmpfs                    920M     0  920M    0% /sys/fs/cgroup
/dev/sda1                497M  124M  373M   25% /boot
tmpfs                    184M     0  184M    0% /run/user/0
[root@localhost ~]# fdisk -l|grep /sd
磁盘 /dev/sda：53.7 GB, 53687091200 字节，104857600 个扇区
/dev/sda1   *        2048     1026047      512000   83  Linux
/dev/sda2         1026048    67108863    33041408   8e  Linux LVM
/dev/sda3        67108864   104857599    18874368   83  Linux
[root@localhost ~]# vgdisplay 
  --- Volume group ---
  VG Name               centos
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               31.51 GiB
  PE Size               4.00 MiB
  Total PE              8066
  Alloc PE / Size       8055 / 31.46 GiB
  Free  PE / Size       11 / 44.00 MiB
  VG UUID               mK7ZEQ-6Sb6-fcgR-ATGU-et9Z-tFHc-Kc2DQF
   
[root@localhost ~]# vgextend centos /dev/sda3
  Physical volume "/dev/sda3" successfully created
  Volume group "centos" successfully extended
[root@localhost ~]# lvdisplay 
  --- Logical volume ---
  LV Path                /dev/centos/swap
  LV Name                swap
  VG Name                centos
  LV UUID                13egta-KMMZ-cS6C-09YK-vBmY-jxyV-8tNaKd
  LV Write Access        read/write
  LV Creation host, time localhost, 2016-11-14 22:29:08 +0800
  LV Status              available
  # open                 2
  LV Size                2.00 GiB
  Current LE             512
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:1
   
  --- Logical volume ---
  LV Path                /dev/centos/root
  LV Name                root
  VG Name                centos
  LV UUID                g9D3kx-Nlg7-vM9g-sUty-Y6zf-KXUP-qMiIsE
  LV Write Access        read/write
  LV Creation host, time localhost, 2016-11-14 22:29:08 +0800
  LV Status              available
  # open                 1
  LV Size                29.46 GiB
  Current LE             7543
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:0
   
[root@localhost ~]# lvextend -L +18G /dev/centos/root 
  Size of logical volume centos/root changed from 29.46 GiB (7543 extents) to 47.46 GiB (12151 extents).
  Logical volume root successfully resized.
[root@localhost ~]# df -Th                                                  #查看系统类型，格式化要用
文件系统                类型      容量  已用  可用 已用% 挂载点
/dev/mapper/centos-root xfs        30G  1.4G   29G    5% /
devtmpfs                devtmpfs  910M     0  910M    0% /dev
tmpfs                   tmpfs     920M     0  920M    0% /dev/shm
tmpfs                   tmpfs     920M  8.5M  912M    1% /run
tmpfs                   tmpfs     920M     0  920M    0% /sys/fs/cgroup
/dev/sda1               xfs       497M  124M  373M   25% /boot
tmpfs                   tmpfs     184M     0  184M    0% /run/user/0

[root@localhost ~]# xfs_growfs /dev/centos/root 
meta-data=/dev/mapper/centos-root isize=256    agcount=4, agsize=1931008 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=0        finobt=0
data     =                       bsize=4096   blocks=7724032, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
log      =internal               bsize=4096   blocks=3771, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 7724032 to 12442624
[root@localhost ~]# df -h
文件系统                 容量  已用  可用 已用% 挂载点
/dev/mapper/centos-root   48G  1.4G   47G    3% /
devtmpfs                 910M     0  910M    0% /dev
tmpfs                    920M     0  920M    0% /dev/shm
tmpfs                    920M  8.5M  912M    1% /run
tmpfs                    920M     0  920M    0% /sys/fs/cgroup
/dev/sda1                497M  124M  373M   25% /boot
tmpfs                    184M     0  184M    0% /run/user/0
[root@localhost ~]# 
```