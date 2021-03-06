---
layout: post
title: "MAC终端的一些使用"
excerpt: "MAC终端的一些使用和快捷键"
categories: [Mac, Terminal]
tags: [Mac, Terminal]
date: 2014-12-05 
modified: 
comments: true
---

* TOC
{:toc}
---

## 一些快捷键

```
crtl + l // 清屏 Ctrl + L
ctrl + a // 移到行首
ctrl + e // 移到行尾
ctrl + y // 插入最近删除的单词或语句
ctrl + k // 删除光标处到行尾部分
ctrl + u // 删除光标处到行首部分
ctrl + w // 删除光标处到当前单词开头部分或语句
ctrl + f // 向前一个字符（右箭头）
ctrl + b // 向后一个字符 （左箭头）
ctrl + d // 删除当前光标字符
ctrl + n // 向下移动一行 (可以代替下箭头)
ctrl + p // 向上移动一行 (可以代替上箭头)
ctrl + h // 退格 删除前一个字符
```

## 一些命令

```
sudo －s  // 为了防止误操作破坏系统，再用户状态下时没有权限操作系统重要文件的，所以先要取得root权限 
ps   // 显示进程当前状态  ps u
kill // 终止进程
date // 显示系统的当前日期和时间
time // 统计程序的执行时间 
cal  // 显示日历
who  // 列出当前登录的所有用户 
whoami // 显示当前正进行操作的用户名 
tty  // 显示终端或伪终端的名称 
stty // 显示或重置控制键定义 
du   // 查询磁盘使用情况  du -k subdir
w    // 显示当前系统活动的总信息
env  // 显示当前所有设置过的环境变量 
uname // 显示操作系统的有关信息
clear // 清除屏幕或窗口内容
alias // 给某个命令定义别名  alias del=rm -i
unalias // 取消对某个别名的定义  unalias del
history // 列出最近执行过的几条命令及编号 
pwd     // 显示当前目录的路径名 
touch   // 更新文件的访问和修改时间
dircmp  // 比较两个目录的内容 emp: dircmp dir1 dir2
diff    // 比较并显示两个文件的差异 diff file1 file2
cat 文件名 // 显示或连接文件  cat filename
pg     // 分页格式化显示文件内容 pg filename
more   // 分屏显示文件内容  more filename
od     // 显示非文本文件的内容  od -c filename
head   // 显示文件的最初几行  head -20 filename
tail   // 显示文件的最后几行  tail -15 filename
cut    // 显示文件每行中的某些域  cut -f1,7 -d: /etc/passwd
file   // 显示文件类型 file filename
open   // 使用默认的程序打开文件 open -a AppName fileName
ln     // 链接文件 ln -s file1 file2
paste  // 横向链接文件 paste file1 file2
r	   // 重复执行最近执行过的 某条命令  r -2
ls 参数 目录名 // 列出文件 参数 -w 显示中文，-l 详细信息， -a 包括隐藏文件
cd 目录名     // 跳到目录 
chmod 参数 权限 文件  // 更改文件权限 参数 -R 表示对目录进行递归操作，rwx 读写课之行 124 二进制
mkdir 目录名  // 建立新目录
rm 文件名     // 删除文件
rmdir 空文件夹 // 删除空文件夹 
rm -r 文件夹名 // 删除文件夹及其子文件 -r 表示递归  -f表示强制
mv 文件       // 移动文件
mvdir dir1 dir2 // 移动或重命名一个目录
cp 参数 源文件 目标文件 // 拷贝文件  参数 -R 表示对目录进行递归操作
grep  // 在文件中按模式查找 grep "^[a-zA-Z]" filename
uniq  // 去掉文件中的重复行 uniq file1 file2
wc // 统计文件的字符数、词数和行数 wc filename
uname	// 显示操作系统的有关信息	uname -a
df	// 显示文件系统的总空间和可用空间	df /tmp
```

## mac相关的一些操作

```
defaults write com.apple.finder AppleShowAllFiles YES  // 显示隐藏文件
defaults write com.apple.finder AppleShowAllFiles NO   // 隐藏隐藏文件
defaults write com.apple.finder AppleShowAllFiles -bool true // 显示隐藏文件
defaults write com.apple.finder AppleShowAllFiles -bool false // 隐藏隐藏文件


find ./ -name "*.html" -exec rm -rf {} \;  // 注意 {}和\;之间有空格

/*
find [目录名] -name "文件名" -exec rm -rf {} \;
搜索删除文件，例如：find / -name *.raw -exec rm -rf {} \; 其中， -exec 表示后面执行命令 "{}" 表示查询到的文件名 -rf 为删除命令rm的参数，r 表示递归删除， f表示不需要确认，两个参数可根据需要去留
*/

find . -name .DS_Store -print0 | xargs -0 Git rm -f --ignore-unmatch
// 删除原有的.DS_Store


cat /etc/shells  // 查看一共有多少shell
chsh -s /bin/zsh // 切换到zsh
chsh -s /bin/bash // 切换到bash
zsh   // 切换到zsh
bash  // 切换到bash
```

## iTerm2

```shell
Ctrl + J	// 相当于return或者回车
Command + r     // 清除屏幕上的内容
Command + t/w   // 打开/关闭 tab
Command + 数字   // 切换到第 n 个 tab
// 双击 选中一个单词，自动复制
```



## 技巧  

```shell
sudo chown -R `whoami` /usr/local   // 修复/usr/local权限
```

