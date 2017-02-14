1. 下载jdk , jdk-8u77-linux-x64.tar.gz

2. 下载 eclipse

3. 配置jdk的环境变量，

打开 /etc/profile文件（sudo vim /etc/profile），在文件末尾添加下语句：

``` shell
export JAVA_HOME=/opt/jvm/jdk1.8.0_77
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

使其立即生效：sudo source /etc/profile
```
4. 进入eclipse 

./eclipse-inst
