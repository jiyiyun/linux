centos 系统
---
-  vi /etc/ssh/sshd_config
``` shell
# If you want to change the port on a SELinux system, you have to tell
# SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#
#Port 22          #Port Setting
Port 2222
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

# Authentication:

#LoginGraceTime 2m
#PermitRootLogin yes      #root login setting
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10
```
ubuntu 系统
---
-  vi /etc/ssh/sshd_config
``` shell
# Package generated configuration file
# See the sshd_config(5) manpage for details

# What ports, IPs and protocols we listen for
Port 22                  # Port Setting

# Authentication:
LoginGraceTime 120
PermitRootLogin prohibit-password     #root login setting
StrictModes yes
```