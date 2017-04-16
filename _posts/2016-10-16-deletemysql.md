---
layout: post
title: "卸载MySQL"
excerpt: "Mac更新10.12后关机很慢，甚至根本关不上，重启也一样。最近才知道是本地MySQL服务的问题。记录下卸载MySQL的方法。"
categories: [MySQL]
tags: [MySQL]
date: 2016-10-16
comments: true
---

* TOC
{:toc}
---

## 卸载MySQL

```shell
sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
vim /etc/hostconfig  (and removed the line MYSQLCOM=-YES-)
rm -rf ~/Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm -rf /var/db/receipts/com.mysql.*
```