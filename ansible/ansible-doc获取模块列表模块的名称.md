ansible-doc 获取模块列表
---
``` txt
[root@centos1 ~]# ansible-doc -l
```

ansible-doc-s module_name :获取指定模块的使用信息

```txt
[root@centos1 ~]# ansible-doc raw
> RAW

  Executes a low-down and dirty SSH command, not going through the module
  subsystem. This is useful and should only be done in two cases. The first case
  is installing `python-simplejson' on older (Python 2.4 and before) hosts that
  need it as a dependency to run modules, since nearly all core modules require
  it. Another is speaking to any devices such as routers that do not have any
  Python installed. In any other case, using the [shell] or [command] module is
  much more appropriate. Arguments given to [raw] are run directly through the
  configured remote shell. Standard output, error output and return code are
  returned when available. There is no change handler support for this module.
  This module does not require python on the remote system, much like the [script]
  module.

  * note: This module has a corresponding action plugin.

Options (= is mandatory):

- executable
        change the shell used to execute the command. Should be an absolute path
        to the executable.
        when using privilege escalation (`become'), a default shell will be
        assigned if one is not provided as privilege escalation requires a shell.
        [Default: (null)]
= free_form
        the raw module takes a free form command to run

Notes:
  * If using raw from a playbook, you may need to disable fact gathering
        using `gather_facts: no' if you're using `raw' to bootstrap python
        onto the machine.
  * If you want to execute a command securely and predictably, it may be
        better to use the [command] or [shell] modules instead.
  * the `environment' keyword does not work with raw normally, it requires a
        shell which means it only works if `executable' is set or using the
        module with privilege escalation (`become').
EXAMPLES:
# Bootstrap a legacy python 2.4 host
- raw: yum -y install python-simplejson

# Bootstrap a host without python2 installed
- raw: dnf install -y python2 python2-dnf libselinux-python

# Run a command that uses non-posix shell-isms (in this example /bin/sh
# doesn't handle redirection and wildcards together but bash does)
- raw: cat < /tmp/*txt
  args:
    executable: /bin/bash


MAINTAINERS: Ansible Core Team, Michael DeHaan
(END)
```
ansible 命令格式
---
``` txt
ansible <host-pattern> [-f forks] [-m module_name] [-a args]
```
