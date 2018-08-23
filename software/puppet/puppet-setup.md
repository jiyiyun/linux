puppet-setup
===

首先要装epel-release

这是server端 Puppet-master(官网安装方法)
---

CentOS系统
```txt
yum install puppetserver
```
Location

```txt
/etc/sysconfig/puppetserver — RHEL
/etc/default/puppetserver — Debian
```
Open the init config file:

 # Modify this if you'd like to change the memory allocation, enable JMX, etc
 
```txt
JAVA_ARGS="-Xms2g -Xmx2g"
```
Replace 2g with the amount of memory you want to allocate to Puppet Server. For example, to allocate 1GB of memory, use <code>JAVA_ARGS="-Xms1g -Xmx1g"</code>; for 512MB, use <code>JAVA_ARGS="-Xms512m -Xmx512m"</code>.

For more information about the recommended settings for the JVM, see Oracle’s docs on JVM tuning.

Restart the puppetserver service after making any changes to this file.

或者(非官网安装方法)

```txt
yum install puppet puppet-server facter -y
```

ubuntu系统

```txt
apt-get install puppetserver
```

这是客户端 puppet-agent

Install the puppet-agent package

For Yum-based systems

On your Puppet agent nodes, run 

```txt
sudo yum install puppet-agent
```
For Apt-based systems

On your Puppet agent nodes, run 

```txt
sudo apt-get install puppet-agent
```
Settings for agents (all nodes)
---

Roughly in order of importance. Most of these can go in either [main] or [agent], or be specified on the command line.

Basics

server — The Puppet master server to request configurations from. Defaults to puppet; change it if that’s not your server’s name.
     ca_server and report_server — If you’re using multiple masters, you’ll need to centralize the CA; one of the ways to do this is by configuring ca_server on all agents. See the multiple masters guide for more details. The report_server setting works about the same way, although whether you need to use it depends on how you’re processing reports.

certname — The node’s certificate name, and the unique identifier it uses when requesting catalogs; defaults to the fully qualified domain name.
For best compatibility, you should limit the value of certname to only use letters, numbers, periods, underscores, and dashes. (That is, it should match /\A[a-z0-9._-]+\Z/.)
The special value ca is reserved, and can’t be used as the certname for a normal node.

environment — The environment to request when contacting the Puppet master. It’s only a request, though; the master’s ENC can override this if it chooses. Defaults to production.

参考资料
---

- https://docs.puppet.com/puppetserver/latest/install_from_packages.html
- https://docs.puppet.com/puppet/4.8/config_important_settings.html#settings-for-agents-all-nodes