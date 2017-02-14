create Pycharm logo
===
1. create a file name is Pycharm.desktop

vi /usr/share/applications/Pycharm.desktop

``` shell
# cat Pycharm.desktop 
[Desktop Entry]
Type=Application
Name=Pycharm
GenericName=Pycharm3
Comment=Pycharm3:The Python IDE
Exec=sh /home/richard/software/pycharm2016/bin/pycharm.sh
Icon=/home/richard/software/pycharm2016/bin/pycharm.png
Terminal=pycharm
Categories=Pycharm;
```
2. chmod 777 /usr/share/applications/Pycharm.desktop