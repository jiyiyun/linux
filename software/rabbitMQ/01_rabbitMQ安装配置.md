RabbitMQ安装
---

rabbitMQ是用erlang写的，首先需要安装erlang

- erlang官网 http://www.erlang.org/
- rabbitMQ官网下载 http://www.rabbitmq.com/install-rpm.html

yum 安装，先分别安装erlang，rabbitMQ更新源，再分别安装erlang和rabbitMQ
- $ sudo yum install erlang -y
- $ sudo yum install socat logrotate  -y
- $ sudo yum install rabbitmq-server

配置

插件管理
```txt
$ sudo rabbitmq-plugins list

$ sudo rabbitmq-plugins enable rabbitmq_management
The following plugins have been configured:
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_web_dispatch
Applying plugin configuration to rabbit@bogon...
The following plugins have been enabled:
  rabbitmq_management
  rabbitmq_management_agent
  rabbitmq_web_dispatch

enabled 3 plugins.
Offline change; changes will take effect at broker restart.


```

用户管理
---

添加用户add_user  rabbitmqctl add_user username password

删除用户delete_user  rabbitmqctl delete_user username password

更改密码change_password rabbitmqctl change_password username password

设置权限tags  rabbitmqctl set_user_tags username tag

参考
---

- http://www.rabbitmq.com/install-rpm.html
- https://fedoraproject.org/wiki/EPEL