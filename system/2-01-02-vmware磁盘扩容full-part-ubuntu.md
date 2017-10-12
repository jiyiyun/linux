第一步：检查现有磁盘情况
---

```txt
root@ubuntu:~# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        396M  6.2M  389M   2% /run
/dev/mapper/ubuntu--vg-root   35G   15G   19G  44% /
tmpfs                        2.0G  468K  2.0G   1% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M  106M  342M  24% /boot
tmpfs                        396M     0  396M   0% /run/user/0
```

第二步：使用fdisk 命令创建新part
---

```txt
root@ubuntu:~# fdisk /dev/sdb 

Welcome to fdisk (util-linux 2.27.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): 

Using default response p.
Partition number (1-4, default 1): 
First sector (2048-629145599, default 2048): 
Last sector, +sectors or +size{K,M,G,T,P} (2048-629145599, default 629145599): 

Created a new partition 1 of type 'Linux' and of size 300 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

root@ubuntu:~# fdisk -l
Disk /dev/sda: 40 GiB, 42949672960 bytes, 83886080 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xa8aa35ac

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sda1  *       2048   999423   997376  487M 83 Linux
/dev/sda2       1001470 83884031 82882562 39.5G  5 Extended
/dev/sda5       1001472 83884031 82882560 39.5G 8e Linux LVM


Disk /dev/sdb: 300 GiB, 322122547200 bytes, 629145600 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x49306c6c

Device     Boot Start       End   Sectors  Size Id Type
/dev/sdb1        2048 629145599 629143552  300G 83 Linux


Disk /dev/mapper/ubuntu--vg-root: 35.5 GiB, 38105251840 bytes, 74424320 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/mapper/ubuntu--vg-swap_1: 4 GiB, 4290772992 bytes, 8380416 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

第三步、将新part 加入到vg
---

```txt
root@ubuntu:~# vgextend ubuntu-vg /dev/sdb1
  Physical volume "/dev/sdb1" successfully created
  Volume group "ubuntu-vg" successfully extended
root@ubuntu:~# vgdisplay 
  --- Volume group ---
  VG Name               ubuntu-vg
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               339.52 GiB
  PE Size               4.00 MiB
  Total PE              86916
  Alloc PE / Size       10108 / 39.48 GiB
  Free  PE / Size       76808 / 300.03 GiB
  VG UUID               bewWSH-Jf4v-XcRF-wXyG-WEU3-tOxp-8hcBW4
```
  
第四步：将新part 加入到lv
---

```txt
root@ubuntu:~# lvextend /dev/ubuntu-vg/root /dev/sdb1 
  Size of logical volume ubuntu-vg/root changed from 35.49 GiB (9085 extents) to 335.48 GiB (85884 extents).
  Logical volume root successfully resized.
root@ubuntu:~# resize2fs 
apphouse/            AppHouse v1.1.1.zip  .bash_history        .cache/              .profile             
apphouse1.2/         AppHouse V1.2.zip    .bashrc              .docker/             .viminfo             
```

第五步：使用resize2fs 更新
---

```txt
root@ubuntu:~# resize2fs /dev/ubuntu-vg/root 
resize2fs 1.42.13 (17-May-2015)
Filesystem at /dev/ubuntu-vg/root is mounted on /; on-line resizing required
old_desc_blocks = 3, new_desc_blocks = 21
The filesystem on /dev/ubuntu-vg/root is now 87945216 (4k) blocks long.
```

第六步：检查是否添加成功
---

```txt
root@ubuntu:~# df -h
Filesystem                   Size  Used Avail Use% Mounted on
udev                         2.0G     0  2.0G   0% /dev
tmpfs                        396M  6.2M  389M   2% /run
/dev/mapper/ubuntu--vg-root  331G   15G  302G   5% /
tmpfs                        2.0G  468K  2.0G   1% /dev/shm
tmpfs                        5.0M     0  5.0M   0% /run/lock
tmpfs                        2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1                    472M  106M  342M  24% /boot
tmpfs                        396M     0  396M   0% /run/user/0
```