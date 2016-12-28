OpenSUSE Leap 42.1 改用国内源并更新系统
----
安装好了OpenSUSE最小版，连通了外网，zypper update太慢太慢，好长时间没有动静，决定用国内更新源


禁用原有软件源
---
``` shell
sudo zypper mr -da
```
添加科大镜像源

```shell
sudo zypper ar -fc https://mirrors.ustc.edu.cn/opensuse/distribution/leap/42.1/repo/oss USTC:42.1:OSS
sudo zypper ar -fc https://mirrors.ustc.edu.cn/opensuse/distribution/leap/42.1/repo/non-oss USTC:42.1:NON-OSS
sudo zypper ar -fc https://mirrors.ustc.edu.cn/opensuse/update/leap/42.1/oss USTC:42.1:UPDATE-OSS
sudo zypper ar -fc https://mirrors.ustc.edu.cn/opensuse/update/leap/42.1/non-oss USTC:42.1:UPDATE-NON-OSS
```

添加阿里更新源
---
``` shell
zypper addrepo -f http://mirrors.aliyun.com/opensuse/update/leap/42.1/oss  openSUSE-42.1-Update-Oss
zypper addrepo -f http://mirrors.aliyun.com/opensuse/update/leap/42.1/non-oss/ openSUSE-42.1-Update-Non-Oss
zypper addrepo -f http://mirrors.aliyun.com/opensuse/distribution/leap/42.1/repo/oss/ openSUSE-42.1-Oss
zypper addrepo -f http://mirrors.aliyun.com/opensuse/distribution/leap/42.1/repo/non-oss/  openSUSE-42.1-Non-Oss
zypper addrepo -f http://mirrors.aliyun.com/packman/openSUSE_Leap_42.1/ aliyun-packman
```
手动刷新软件源
---
``` shell
sudo zypper ref
```
更新系统
---
``` shell
sudo zypper up
```

参考资料
---
- [openSUSE leap 42.1添加阿里镜像源] http://www.jianshu.com/p/876d2f9c60c5
- [OpenSUSE Leap 42.1 改用国内源并更新系统] http://m.w2bc.com/article/99471