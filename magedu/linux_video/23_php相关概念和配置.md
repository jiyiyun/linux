
PHP is Hypertext Processor 超文本预处理，解释型语言,apache DSO dynamic shared object
bash: 词法分析、语法分析、生成执行路径、opcode操作码，Zend引擎

Scanning -->

php source code -->编译成二进制--->执行二进制，同一用户第一次访问慢第二次就快很多，通过共享缓存机制,可以将编译好的opcode放在共享缓存里，这样只要不涉及私有数据，可以加快其它用户的访问速度，XCache,Zend Oplimized和Zend Guard Loader

nginx处理静态网页比httpd更好

查看php相关软件包

```txt
[root@bogon ~]# yum list all |grep php
php.x86_64                               5.4.16-46.el7                   @base
php-cli.x86_64                           5.4.16-46.el7                   @base
php-common.x86_64                        5.4.16-46.el7                   @base
```
安装阿里云更新源

curl -o /etc/yum.repos.d/Aliyun-CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

```txt
安装php
$ sudo yum install php php-mbstring

php-mbstring mb是多字节，汉字属于多字节，所以这个模块一般都要装。

检查已安装php
[root@bogon ~]# rpm -qa|grep php
php-common-5.4.16-46.el7.x86_64
php-cli-5.4.16-46.el7.x86_64
php-mbstring-5.4.16-46.el7.x86_64
php-5.4.16-46.el7.x86_64

检查php包里有那些
[root@bogon ~]# rpm -ql php
/etc/httpd/conf.d/php.conf
/etc/httpd/conf.modules.d/10-php.conf
/usr/lib64/httpd/modules/libphp5.so
/usr/share/httpd/icons/php.gif
/var/lib/php/session
```
```txt
[root@bogon html]# cat index.php
<title> Hello PHP </title>
<body>
<h1>《春夜喜雨》 杜甫</h1>
<h1>好雨知时节，当春乃发生。</h1>
<h1>随风潜入夜，润物细无声。</h1>
<h1>野径云俱黑，江船火独明。</h1>
<h1>晓看红湿处，花重锦官城。</h1>
</body>

<?php
phpinfo():
?>
```

