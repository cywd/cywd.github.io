---
layout: post
title: "MAC终端的一些使用"
excerpt: "MAC终端的一些使用"
categories: [Mac, Terminal]
tags: [Mac, Terminal]
date: 2014-12-05 
modified: 
comments: true
---



## 一些快捷键

```
crtl + l // 清屏
ctrl + a // 移到行首
ctrl + e // 移到行尾
ctrl + y // 插入最近删除的单词或语句
ctrl + k // 删除光标处到行尾部分
ctrl + u // 删除光标处到行首部分
ctrl + w // 删除光标处到当前单词开头部分或语句
```

## 一些命令

```
sudo －s  // 为了防止误操作破坏系统，再用户状态下时没有权限操作系统重要文件的，所以先要取得root权限 
ps   // 显示进程当前状态 
kill // 终止进程
date // 显示系统的当前日期和时间
time // 统计程序的执行时间 
cal  // 显示日历
who  // 列出当前登录的所有用户 
whoami // 显示当前正进行操作的用户名 
tty  // 显示终端或伪终端的名称 
stty // 显示或重置控制键定义 
du   // 查询磁盘使用情况 
w    // 显示当前系统活动的总信息
env  // 显示当前所有设置过的环境变量 
uname // 显示操作系统的有关信息
clear // 清除屏幕或窗口内容
alias // 给某个命令定义别名 
unalias // 取消对某个别名的定义 
history // 列出最近执行过的几条命令及编号 
pwd     // 显示当前目录的路径名 
touch   // 更新文件的访问和修改时间
dircmp  // 比较两个目录的内容
diff    // 比较并显示两个文件的差异
cat 文件名 // 显示或连接文件 
pg     // 分页格式化显示文件内容
more   // 分屏显示文件内容 
od     // 显示非文本文件的内容 
head   // 显示文件的最初几行
tail   // 显示文件的最后几行
cut    // 显示文件每行中的某些域
file   // 显示文件类型
open   // 使用默认的程序打开文件
r	   // 重复执行最近执行过的 某条命令
ls 参数 目录名 // 列出文件 参数 -w 显示中文，-l 详细信息， -a 包括隐藏文件
cd 目录名     // 跳到目录 
chmod 参数 权限 文件  // 更改文件权限 参数 -R 表示对目录进行递归操作
mkdir 目录名  // 新建文件夹
rm 文件名     // 删除文件
rmdir 空文件夹 // 删除空文件夹 
rm -r 文件夹名 // 删除文件夹及其子文件 -r 表示递归  -f表示强制
mv 文件       // 移动文件
cp 参数 源文件 目标文件 // 拷贝文件  参数 -R 表示对目录进行递归操作
```

mac相关的一些操作

```
defaults write com.apple.finder AppleShowAllFiles YES  // 显示隐藏文件
defaults write com.apple.finder AppleShowAllFiles NO   // 隐藏隐藏文件

cat /etc/shells  // 查看一共有多少shell
chsh -s /bin/zsh // 
zsh   // 切换到zsh
bash  // 切换到bash
```







