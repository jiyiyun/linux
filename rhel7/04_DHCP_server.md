DHCP 服务器
---
DHCP工作流程
1. 发现阶段: DHCP客户端给整个网段发送DHCP discover 报文，每台主机都会接收到该请求广播，只有DHCP服务器会响应
2. 提供阶段: 收到DHCP discover报文的DHCP 服务器会响应，从尚未出租的IP池中分配一个给DHCP客户端，其中包括IP和DHCP offer信息
3. 选择阶段: 如果该网段有多台DHCP服务器响应，DHCP客户端选择第一个收到的DHCP offer信息，然后以广播形式应答一个DHCP request信息，该应答包含它所选定的DHCP服务器请求IP地址的内容，之所以是广播，是为了通知所有DHCP服务器它将选择那台DHCP服务器所提供的IP地址
4. 确认阶段：DHCP服务器确认所提供的IP地址阶段，DHCP服务器收到DHCP客户端回复的DHCP request信息以后，它向DHCP 客户端发送包含其IP地址和其他设置的DHCP ACK信息，告诉DHCP客户端可以使用该地址，然后客户端将其与自己的网卡绑定，其他DHCP服务器收回曾提供的IP地址
5. 重新登录：以后DHCP客户端重新登录时，不需要再发送DHCP discover信息，而是直接发送包含IP的DHCP request信息，如果可以继续用返回DHCP ACK，如果已经被其他主机使用，则DHCP服务器给客户端返回NACK,客户端收到此信息以后，必须重新发送DHCP descover信息来请求新地址  
6. 更新租约：客户端租约过半时会自动向DHCP 服务网请求更新租约信息

1. 按照和配置文件
---
``` shell 
# yum install dhcp
```
配置文件的主要参数 vi /etc/dhcp/dhcpd.conf
- ddns-uodate-style 配置DHCP-DNS互动更新模式
- defaule-lease-time 默认租赁时间，秒
- max-lease-time 最大租赁时间
- fixed-address ip 给客户端一个固定IP
- authritative 拒绝不正确的IP地址要求
