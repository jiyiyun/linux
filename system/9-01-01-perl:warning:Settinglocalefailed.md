perl: warning: Setting locale failed
===
今天编译mesos-0.28.2出现以下报错
``` shell
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = "en_US:",
	LC_ALL = (unset),
	LC_TIME = "zh_CN.UTF-8",
	LC_MONETARY = "zh_CN.UTF-8",
	LC_ADDRESS = "zh_CN.UTF-8",
	LC_TELEPHONE = "zh_CN.UTF-8",
	LC_NAME = "zh_CN.UTF-8",
	LC_MEASUREMENT = "zh_CN.UTF-8",
	LC_IDENTIFICATION = "zh_CN.UTF-8",
	LC_NUMERIC = "zh_CN.UTF-8",
	LC_PAPER = "zh_CN.UTF-8",
	LANG = "en_US.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to a fallback locale ("en_US.UTF-8").
```
baidu了下
``` shell
- # vi /root/.bashrc
- export LC_ALL=C
- # source /root/.bashrc
```
