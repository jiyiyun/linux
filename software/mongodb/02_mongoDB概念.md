mongoDB基本概念
- SQL术语概念     MongoDB术语概念   解释/说明
- database       database        数据库
- table          collection      数据库表
- row            document        表记录
- column         field           字段
- index          index           索引
- table joins    
- primary key    primary key      主键

数据库

MongoDB默认数据库为db,在data目录中，MongoDB单个实例可以容纳多个数据库，每一个都有自己的集合和权限

show dbs查看

```txt
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
test    0.000GB

- admin：这是root数据库，admin库中创建的用户继承所有数据库权限，一些特定的服务器端命令只能在这个库中执行
- local:该数据库永不会被复制，用来存储仅限本地单台服务器的任意集合
- config:当MongoDB在分片设置的时候，config数据库在内部使用，保存分片相关信息

查看当前数据库
> db
test

切换MongoDB数据库
> use local
switched to db local
> db
local
```
创建数据库

```
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
> use aaa
switched to db aaa
> db.aaa.insert({"name":"菜鸟教程"})
WriteResult({ "nInserted" : 1 })
> show dbs
aaa     0.000GB
admin   0.000GB
config  0.000GB
local   0.000GB
```

2.6 MongoDB shell的使用

```txt
> new Date()
ISODate("2019-03-09T09:18:41.833Z")
>
> db
aaa

创建
定义一个局部变量personalbaseinfo
> personalbaseinfo={"name":"zhangsan","age":"8"}
{ "name" : "zhangsan", "age" : "8" }
将局部变量personalbaseinfo赋值给文档对象，保存在集合personalinfo中
> db.personalinfo.insert(personalbaseinfo)
WriteResult({ "nInserted" : 1 })

读取
> db.personalinfo.find()
{ "_id" : ObjectId("5c83862f447d8654b7b84fff"), "name" : "zhangsan", "age" : "8" }
find可以获取所有文档，如果只查询一个文档，使用findOne()
> db.personalinfo.findOne()
{
        "_id" : ObjectId("5c83862f447d8654b7b84fff"),
        "name" : "zhangsan",
        "age" : "8"
}

更新
> personalbaseinfo.address="beijing"
beijing
> db.personalinfo.update({"name":"zhangsan"},personalbaseinfo)
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.personalinfo.find()
{ "_id" : ObjectId("5c83862f447d8654b7b84fff"), "name" : "zhangsan", "age" : "8", "address" : "beijing" }

删除
> db.personalinfo.remove({"name":"zhangsan"})
WriteResult({ "nRemoved" : 1 })

使用诀窍

```txt
> help
        db.help()                    help on db methods
        db.mycoll.help()             help on collection methods
        sh.help()                    sharding helpers
        rs.help()                    replica set helpers
        help admin                   administrative help
        help connect                 connecting to a db help
        help keys                    key shortcuts
        help misc                    misc things to know
        help mr                      mapreduce

        show dbs                     show database names
        show collections             show collections in current database
        show users                   show users in current database
        show profile                 show most recent system.profile entries with time >= 1ms
        show logs                    show the accessible logger names
        show log [name]              prints out the last segment of log in memory, 'global' is default
        use <db_name>                set current database
        db.foo.find()                list objects in collection foo
        db.foo.find( { a : 1 } )     list objects in foo where a == 1
        it                           result of the last line evaluated; use to further iterate
        DBQuery.shellBatchSize = x   set default number of items to display on shell
        exit                         quit the mongo shell
>
```