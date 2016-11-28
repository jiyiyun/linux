too  many authentication failures
---- 
- 打开文件 /etc/ssh/sshd_config
- 修改 MaxAuthTries 这个参数的值

- ssh -p 2222 -o PubkeyAuthentication=no 192.168.3.160

编辑vi vi /etc/ssh/sshd_config

修改 将PubkeyAuthentication yes 修改成为 no
RSAAuthentication yes
PubkeyAuthentication no
#AuthorizedKeysFile     %h/.ssh/authorized_keys

