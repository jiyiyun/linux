ansible运行太慢问题的解决
---

ansible查询运用openssl协议进行加密传输

ansible效率优化-开启ControlPersist







方法2： 修改/etc/ssh/ssh_config (效果不明显)
---

```txt
#Host *
#       GSSAPIAuthentication yes   #将yes 修改成为no 
Host *
        GSSAPIAuthentication no
```
知识补充：

GSSAPI ( Generic Security Services Application Programming Interface) 是一套类似Kerberos 5 的通用网络安全系统接口。该接口是对各种不同的客户端服务器安全机制的封装，以消除安全接口的不同，降低编程难度。但该接口在目标机器无域名解析时会有问题。修改本机的客户端配置文件ssh_conf，可以更改该参数。


ansible service模块

```txt
root@gitlab:~# ansible httpd  -m service -a 'name=httpd  state=restart'
192.168.100.23 | FAILED! => {
    "changed": false, 
    "failed": true, 
    "msg": "value of state must be one of: running,started,stopped,restarted,reloaded, got: restart"
}
192.168.100.33 | FAILED! => {
    "changed": false, 
    "failed": true, 
    "msg": "value of state must be one of: running,started,stopped,restarted,reloaded, got: restart"
}

以上报错说明:service状态只能是running,started,stopped,restarted,reloaded其中一个

root@gitlab:~# ansible httpd  -m service -a 'name=httpd  state=restarted'
192.168.100.33 | SUCCESS => {
    "changed": true, 
    "name": "httpd", 
    "state": "started"
}
192.168.100.23 | SUCCESS => {
    "changed": true, 
    "name": "httpd", 
    "state": "started"
}

```
参考资料
---

- ansible太慢解决 http://blog.csdn.net/wang1144/article/details/52159889
- 修改/etc/ssh/ssh_config 参数 http://www.iyunv.com/thread-249471-1-1.html