---
layout: post
title: 同一电脑下多个SSH-Key配置
excerpt: ""
categories: [Git]
tags: ["SSH", Git]
date: 2018-06-06
comments: true
---

* TOC
{:toc}
---

# 配置

这里拿`GitHub`和`GitLab`来举例

首先生成两种不同的**SSH Key**

```shell
.ssh
├── config
├── id_rsa          # GitHub
├── id_rsa.pub      # GitHub
├── id_rsa_com      # GitLab
├── id_rsa_com.pub  # GitLab
└── known_hosts
```

然后需要一个`config`文件来进行配置

```
# config文件内容

Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa

Host gitlab     # 别名，以后连接远程服务器就可以用命令  ssh gitlab
    HostName 192.168.19.224   # 主机名
    Port     22               # 端口
    User     git			  # 用户名
    PreferredAuthentications publickey   
    IdentityFile ~/.ssh/id_rsa_com    # 密钥文件的路径
```

其中`HostName`和`Host`可以不一致，使用时是用的`Host`，个人会写成一致的。

## 注意

这里纠正一下，本来我是写成一样的，但是现在这个`ssh`我有两个用途，一个是`git ssh`，一个是`ssh`远程登录，如果写成一样的会导致远程登录的时候也会访问这个`SSH key`，如果服务器没有这个`key`的话，就会如下：

```shell
root@192.168.19.224: Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).
```

这个时候该怎么解决呢，有两种方法，

1.`HostName`和`Host`写成不同的，不过相应的，比如`clone`的时候地址也要改变如

```shell
# 原来是 git clone git@192.168.19.224:root/test.git
git clone git@gitlab:root/test.git
```

2.在服务器上增加这个`key`

```shell
~/.ssh/authorized_keys  #在服务器上这个文件里增加你的SSH key
```

# 验证

```shell
ssh -T git@github.com   # ssh -T 用户名@配置文件中的Host
```

