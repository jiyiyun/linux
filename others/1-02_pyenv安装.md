pyenv的安装
---

```txt
官网： https://github.com/pyenv/pyenv-installer

rich@R:~$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
rich@R:~$ git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenvvirtualenv

ubuntu添加环境变量
rich@R:~$ vi .profile
添加
export PYENV_ROOT=/home/rich/.pyenv
export PATH="/home/rich/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

rich@R:~$ sudo vi /etc/profile
这个是添加全局环境变量
export PYENV_ROOT=/home/rich/.pyenv
export PATH="/home/rich/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

centos添加环境变量

vi ~/.bash_profile
添加
export PYENV_ROOT=/home/rich/.pyenv
export PATH="/home/rich/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

rich@R:~$ sudo vi /etc/profile
这个是添加全局环境变量
export PYENV_ROOT=/home/rich/.pyenv
export PATH="/home/rich/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install --list列出可安装版本
$ pyenv install --list
  2.7.15
  3.6.8
  3.7.0
  3.7.1
  3.7.2

$ pyenv install 3.6.8


$pyenv global 3.6.8

$pyenv global system

pyenv local设置从当前目录开始往下递归都继承这个设置
$pyenv local 3.6.8

$pyenv version 查看当前生效版本
$pyenv versions查看系统已有版本

rich@R:~$ pyenv versions
* system (set by /home/rich/.pyenv/version)
  3.7.2

rich@R:~$ pyenv --help
Usage: pyenv <command> [<args>]

Some useful pyenv commands are:
   commands    List all available pyenv commands
   local       Set or show the local application-specific Python version
   global      Set or show the global Python version
   shell       Set or show the shell-specific Python version
   install     Install a Python version using python-build
   uninstall   Uninstall a specific Python version
   rehash      Rehash pyenv shims (run this after installing executables)
   version     Show the current Python version and its origin
   versions    List all Python versions available to pyenv
   which       Display the full path to an executable
   whence      List all Python versions that contain the given executable


virtualenv虚拟环境，可以隔离多个python版本

```