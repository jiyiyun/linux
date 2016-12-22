iperf网络性能测试工具
===
iperf命令是一个网络性能测试工具。iperf可以测试TCP和UDP带宽质量。iperf可以测量最大TCP带宽，具有多种参数和UDP特性。iperf可以报告带宽，延迟抖动和数据包丢失。利用iperf这一特性，可以用来测试一些网络设备如路由器，防火墙，交换机等的性能。

iperf在linux主机上的安装
---
```shell
yum install iperf -y    #centos
apt install iperf -y    #ubuntu
```
UDP模式
---
iperf客户端
---
``` shell
UDP模式下，以100M发送速率，客户端到服务器192.168.15.161上传带宽测试
# iperf -u -c 192.168.15.161 -b 100M -t 60
------------------------------------------------------------
Client connecting to 192.168.15.161, UDP port 5001
Sending 1470 byte datagrams
UDP buffer size:  208 KByte (default)
------------------------------------------------------------
[  3] local 192.168.3.160 port 48802 connected with 192.168.15.161 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-60.0 sec   719 MBytes   100 Mbits/sec
[  3] Sent 512675 datagrams
[  3] Server Report:
[  3]  0.0-60.0 sec   684 MBytes  95.7 Mbits/sec   0.106 ms 24605/512674 (4.8%)
[  3]  0.0-60.0 sec  1 datagrams received out-of-orde
```
iperf服务器端
---
``` shell
# iperf -u -s
------------------------------------------------------------
Server listening on UDP port 5001
Receiving 1470 byte datagrams
UDP buffer size:  208 KByte (default)
------------------------------------------------------------
[  3] local 192.168.15.161 port 5001 connected with 192.168.3.160 port 48802
[ ID] Interval       Transfer     Bandwidth        Jitter   Lost/Total Datagrams
[  3]  0.0-60.0 sec   684 MBytes  95.7 Mbits/sec   0.107 ms 24605/512674 (4.8%)
[  3]  0.0-60.0 sec  1 datagrams received out-of-o
```

TCP 模式
---
``` shell
# iperf -c 192.168.15.161 -t 60
------------------------------------------------------------
Client connecting to 192.168.15.161, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  3] local 192.168.3.160 port 54868 connected with 192.168.15.161 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-60.0 sec   673 MBytes  94.1 Mbits/sec

服务器端
# iperf -s
------------------------------------------------------------
Server listening on TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  4] local 192.168.15.161 port 5001 connected with 192.168.3.160 port 54868
[ ID] Interval       Transfer     Bandwidth
[  4]  0.0-60.1 sec   673 MBytes  94.0 Mbits/sec
```
同时30个并发
```shell
# iperf -c 192.168.15.161 -P 30 -t 60
```
进行上下带宽测试
---
``` shell
# iperf -c 192.168.15.161 -d -t 30
------------------------------------------------------------
Server listening on TCP port 5001
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
------------------------------------------------------------
Client connecting to 192.168.15.161, TCP port 5001
TCP window size:  102 KByte (default)
------------------------------------------------------------
[  4] local 192.168.3.160 port 54938 connected with 192.168.15.161 port 5001
[  5] local 192.168.3.160 port 5001 connected with 192.168.15.161 port 50288
[ ID] Interval       Transfer     Bandwidth
[  4]  0.0-30.0 sec   233 MBytes  65.1 Mbits/sec
[  5]  0.0-30.2 sec   332 MBytes  92.3 Mbits/sec

```