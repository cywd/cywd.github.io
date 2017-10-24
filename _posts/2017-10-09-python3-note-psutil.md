---
layout: post
title: python3 psutil
excerpt: "psutil模块介绍使用"
categories: [python3]
tags: [python3]
date: 2017-10-09
comments: true
---

* TOC
{:toc}
---

## psutil模块

### 1.介绍

**psutil**是一个跨平台库（http://code.google.com/p/psutil/），能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要应用于系统监控，分析和限制系统资源及进程的管理。它实现了同等命令行工具提供的功能，如ps、top、lsof、netstat、ifconfig、who、df、kill、free、nice、ionice、iostat、iotop、uptime、pidof、tty、taskset、pmap等。目前支持32位和64位的Linux、Windows、OS X、FreeBSD和Sun Solaris等操作系统

### **2.安装**

#### linux

```
wget https://pypi.python.org/packages/source/p/psutil/psutil-2.0.0.tar.gz
tar -xzvf psutil-2.0.0.tar.gz
cd psutil-2.0.0
python setup.py install
```

#### mac pip

```
pip3 install psutil
```

### 3.使用

获取系统性能信息（CPU,内存，磁盘，网络）

#### 1.CPU相关

##### 查看cpu信息

```
import psutil
# 返回系统CPU运行时间的元组，时间为秒。
>>> psutil.cpu_times(precpu=False)
# linux
scputimes(user=11677.09, nice=57.93, system=148675.58, idle=2167147.79, iowait=260828.48, irq=7876.28, softirq=0.0, steal=3694.59, guest=0.0, guest_nice=0.0)
# mac
scputimes(user=11395.62, nice=0.0, system=5876.26, idle=67855.91)
```

##### 显示cpu所有逻辑信息

```
>>> psutil.cpu_times(percpu=True)
# linux
[scputimes(user=11684.17, nice=57.93, system=148683.01, idle=2168982.08, iowait=260833.18, irq=7882.35, softirq=0.0, steal=3697.3, guest=0.0, guest_nice=0.0)]
# mac
[scputimes(user=4080.14, nice=0.0, system=2318.3, idle=15042.66), scputimes(user=1731.44, nice=0.0, system=863.43, idle=18845.4), scputimes(user=3914.96, nice=0.0, system=1862.18, idle=15663.15), scputimes(user=1751.7, nice=0.0, system=875.31, idle=18813.27)]
```

##### 查看用户的cpu时间比

```
>>> psutil.cpu_times().user
11684.4
```

##### 查看cpu逻辑个数

```
>>> psutil.cpu_count()
1
```

##### 查看cpu物理个数

```
>>> psutil.cpu_count(logical=False)
1
```

##### 查看cpu使用率百分比

```python
psutil.cpu_percent(interval=None, percpu=False)
# 返回一个浮点书，代表当前cpu的利用率的百分比，包括sy+user. 当interval为0或者None时，表示的是interval时间内的sys的利用率。
# 当percpu为True返回是每一个cpu的利用率。
# mac
scputimes(user=7.2, nice=0.0, system=4.7, idle=88.1)
```

#### 2.查看系统内存

```
>>> import psutil
>>> mem = psutil.virtual_memory()
>>> mem
#系统内存的所有信息
svmem(total=1040662528, available=175054848, percent=83.2, used=965718016, free=74944512, active=566755328, inactive=59457536, buffers=9342976, cached=90767360)
# mac
svmem(total=8589934592, available=2400677888, percent=72.1, used=6985986048, free=24387584, active=2570063872, inactive=2376290304, wired=2039631872)
```

##### 系统总计内存

```
>>> mem.total
1040662528
```

##### 系统已经使用内存

```
>>> mem.used
965718016
```

##### 系统空闲内存

```
>>> mem.free
112779264
```

##### 获取swap内存信息

```
>>> psutil.swap_memory()
sswap(total=0, used=0, free=0, percent=0, sin=0, sout=0)
```

#### 3.读取磁盘参数

磁盘利用率使用psutil.disk_usage方法获取，磁盘IO信息包括read_count(读IO数)，write_count(写IO数)

read_bytes(IO写字节数)，read_time(磁盘读时间)，write_time(磁盘写时间),这些IO信息用

```
psutil.disk_io_counters()
```

##### 获取磁盘的完整信息

```
psutil.disk_partitions()
```

##### 获取分区表的参数

```
psutil.disk_usage('/')   #获取/分区的状态
```

##### 获取硬盘IO总个数

```
psutil.disk_io_counters()
```

##### 获取单个分区IO个数

```
psutil.disk_io_counters(perdisk=True)    #perdisk=True参数获取单个分区IO个数
```

#### 读取网络信息

网络信息与磁盘IO信息类似,涉及到几个关键点，包括byes_sent(发送字节数),byte_recv=xxx(接受字节数),
pack-ets_sent=xxx(发送字节数),pack-ets_recv=xxx(接收数据包数),这些网络信息用

##### 获取网络总IO信息

```
psutil.net_io_counters()  
```

##### 输出网络每个接口信息

```
psutil.net_io_counters(pernic=True)     #pernic=True
```

#### 获取当前系统用户登录信息

```
psutil.users()
```

#### 获取开机时间

```
psutil.boot_time() #以linux时间格式返回
datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S") #转换成自然时间格式
```

#### 系统进程管理

获取当前系统的进程信息,获取当前程序的运行状态,包括进程的启动时间,查看设置CPU亲和度,内存使用率,IO信息
socket连接,线程数等
获取进程信息

#### 查看系统全部进程

```
psutil.pids()
```

#### 查看单个进程

```
p = psutil.Process(2423) 
p.name()   #进程名
p.exe()    #进程的bin路径
p.cwd()    #进程的工作目录绝对路径
p.status()   #进程状态
p.create_time()  #进程创建时间
p.uids()    #进程uid信息
p.gids()    #进程的gid信息
p.cpu_times()   #进程的cpu时间信息,包括user,system两个cpu信息
p.cpu_affinity()  #get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
p.memory_percent()  #进程内存利用率
p.memory_info()    #进程内存rss,vms信息
p.io_counters()    #进程的IO信息,包括读写IO数字及参数
p.connectios()   #返回进程列表
p.num_threads()  #进程开启的线程数
听过psutil的Popen方法启动应用程序，可以跟踪程序的相关信息
from subprocess import PIPE
p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
p.name()
p.username()
```

