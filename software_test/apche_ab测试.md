apache ab测试
---
官方文档http://httpd.apache.org/docs/2.2/programs/ab.html

1. windows 系统下载安装apche,进入apachea安装目录C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin

``` shell
Microsoft Windows [版本 6.1.7601]
版权所有 (c) 2009 Microsoft Corporation。保留所有权利。

C:\Users\yingyu>cd C:\Program Files (x86)\Apache Software Foundation\Apache2.2\b
in

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>ab
ab: wrong number of arguments
Usage: ab [options] [http://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make
    -t timelimit    Seconds to max. wait for responses
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>

Microsoft Windows [版本 6.1.7601]
版权所有 (c) 2009 Microsoft Corporation。保留所有权利。

C:\Users\yingyu>cd C:\Program Files (x86)\Apache Software Foundation\Apache2.2\b
in

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>ab
ab: wrong number of arguments
Usage: ab [options] [http://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make
    -t timelimit    Seconds to max. wait for responses
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header for POSTing, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -h              Display usage information (this message)

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>ab -n 100 -c 100
 https://www.baidu.com
SSL not compiled in; no https support

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>ab -n 100 -c 100
 http://192.168.3.15
ab: invalid URL
Usage: ab [options] [http://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make
    -t timelimit    Seconds to max. wait for responses
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header for POSTing, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -h              Display usage information (this message)

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>ab -n 100 -c 100
 http://192.168.3.15/index.php/login
This is ApacheBench, Version 2.3 <$Revision: 655654 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 192.168.3.15 (be patient).....done


Server Software:        Apache/2.4.6
Server Hostname:        192.168.3.15
Server Port:            80

Document Path:          /index.php/login
Document Length:        10044 bytes

Concurrency Level:      100
Time taken for tests:   6.712 seconds
Complete requests:      100
Failed requests:        0
Write errors:           0
Total transferred:      1098272 bytes
HTML transferred:       1004400 bytes
Requests per second:    14.90 [#/sec] (mean)
Time per request:       6712.012 [ms] (mean)
Time per request:       67.120 [ms] (mean, across all concurrent requests)
Transfer rate:          159.79 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   2.7      0      16
Processing:   546 3972 2107.9   3795    6665
Waiting:      499 3893 2091.1   3701    6650
Total:        546 3972 2107.8   3795    6665

Percentage of the requests served within a certain time (ms)
  50%   3795
  66%   5558
  75%   5870
  80%   6525
  90%   6603
  95%   6618
  98%   6634
  99%   6665
 100%   6665 (longest request)

C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin>

```