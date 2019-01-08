ubuntu,deepin创建应用桌面图标，centos也可以参考
---

```txt
深度linux 安装Gnome Terminal在应用栏找不到图标解决方法
vi /usr/share/applications/org.gnome.Terminal.desktop

StartupNotify=true
X-GNOME-SingleWindow=false
#OnlyShowIn=GNOME;Unity;

注销掉 OnlyShowIn=GNOME;Unity; 这一行即可

将pycharm在应用栏显示
用普通用户权限手动创建 /usr/share/applications/Pycharm.desktop 文件
root@richard-PC:~# cat /usr/share/applications/Pycharm.desktop 
[Desktop Entry]
Type=Application
Name=Pycharm
GenericName=Pycharm201802
Comment=Pycharm2018:The Python IDE
Exec=sh /home/richard/pycharm/pycharm-community-2018.2.1/bin/pycharm.sh
Icon=/home/richard/pycharm/pycharm-community-2018.2.1/bin/pycharm.png
Terminal=pycharm
Categories=Pycharm;

安放路径要填写正确
```