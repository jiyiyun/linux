Ubuntu 卸载vmware player
===
``` shell
在终端输入命令

    ws@ubuntu:/usr/bin$ vmware-installer -l

Product Name | Product Version
vmware-player | 3.0.0.203739

    ws@ubuntu:/usr/bin$ sudo vmware-installer -u vmware-player

弹出卸载界面，一路下一步就可以了。

总结：
1. vmware-installer -l 看装的什么产品
2. sudo vmware-installer -u <产品名>， 即可卸载相应产品
3.有时候需要用locate定位删除
    locate update  
    locate vmware-player  

```
