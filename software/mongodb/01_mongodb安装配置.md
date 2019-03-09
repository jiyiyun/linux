
1. mongoDB官网下载安装包 
2. 解压 # tar -zxvf mongodb-linux-x86_64-3.0.6.tgz
3. mv  mongodb-linux-x86_64-3.0.6/ /usr/local/mongodb

创建环境变量将其添加到 PATH 路径中：

export PATH=<mongodb-install-directory>/bin:$PATH

```
# cat /etc/profile

#java
export JAVA_HOME=/usr/java/jdk1.8.0_131
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib:$CLASSPATH
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

#mongoDB
export MONGODB_HOME=/usr/local/mongodb-linux-x86_64-rhel70-3.6.3
export PATH=$PATH:$MONGODB_HOME/bin

#kafka
export KAFKA_HOME=/usr/local/kafka_2.12-1.1.0
export PATH=$PATH:$KAFKA_HOME/bin

#zookeeper
export ZOOKEEPER_HOME=/usr/local/zookeeper-3.4.10
export PATH=$PATH:$ZOOKEEPER_HOME/bin
```
启动mongoDB

```txt
[root@bogon ~]# mongod
2019-03-07T18:59:10.324+0800 I CONTROL  [initandlisten] MongoDB starting : pid=13892 port=27017 dbpath=/data/db 64-bit host=bogon
2019-03-07T18:59:10.324+0800 I CONTROL  [initandlisten] db version v3.6.3

[root@bogon ~]# mongo
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.3
Welcome to the MongoDB shell.
For interactive help, type "help"

这种启动方式类似于
cd mondoDB目录/bin
./mongod
./mongo
```

由于这是个JavaScript shell ,所以可以执行一些命令

```txt
> 2+3
5
> 3*6
18

> db.runoob.insert({x:10})
WriteResult({ "nInserted" : 1 })
将数字10插入到runoob集合中

> db.runoob.find()
{ "_id" : ObjectId("5c80fb611ec31e746ce5c723"), "x" : 10 }

```
参考
- https://www.mongodb.com/download-center/community
- http://www.runoob.com/mongodb/mongodb-linux-install.html