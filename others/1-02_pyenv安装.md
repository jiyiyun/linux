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

```