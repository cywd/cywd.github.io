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

这里拿`GitHub`和`GitLab`来举例

首先生成两种不同的**SSH Key**

```
.ssh
├── config
├── id_rsa          # GitHub
├── id_rsa.pub      # GitHub
├── id_rsa_com      # GitLab
├── id_rsa_com.pub  # GitLab
└── known_hosts
```

然后需要一个config文件来进行配置

```
# config文件内容

Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa

Host 192.168.19.224
    HostName 192.168.19.224
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa_com
```

其中HostName和Host可以不一致，使用时是用的Host，个人会写成一致的

验证

```shell
ssh -T git@github.com   # ssh -T 用户名@配置文件中的Host
```

