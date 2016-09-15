---
layout: post
title: "关于cocoaPods安装的那些事"
excerpt: "安装cocoapods顺序
Xcode->homebrew->RVM->Ruby->CocoaPots;"
categories: [cocoaPods]
tags: [cocoaPods安装]
date: 2016-08-01 
modified: 
comments: true
---

[TOC]

安装cocoapods顺序
Xcode->homebrew->RVM->Ruby->CocoaPots;

查看gcc版本
`gcc --version`

安装homebrew
`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

homebrew 修复问题
`brew doctor`

homebrew升级
`brew update`

更新连接
`brew install autoconf`

当执行这句安装cocoapods时

`sudo sudo gem install -n /usr/local/bin cocoapods`

出现这个的时候

```
ERROR:  While executing gem ... (TypeError)
    no implicit conversion of nil into String
```


请
更新gem
`sudo gem update --system`

安装rvm
`curl -L get.rvm.io | bash -s stable`

安装ralis
`gem install rails`

ruby的版本号过低
```
ERROR:  Error installing cocoapods:
activesupport requires Ruby version >= 2.2.2.
```

查看ruby的版本
`ruby -v`
// 查看已经安装的ruby版本
`rvm list`

// 查看所有可用的ruby
`rvm list known`

// 设置默认ruby
`rvm 2.3.0 --default`

// 更新rvm文档
`rvm docs generate-ri`

`sudo gem install cocoa pods`
`sudo gem install -n /usr/local/bin cocoapods`
`pod setup`

// 查看pod版本
`pod --version`


``






关于pod setup 特别慢的问题
可以用 GitHub Desktop

1.访问 [https://github.com/CocoaPods/Specs](https://github.com/CocoaPods/Specs)，然后将Specs项目fork到自己的github账户上
2. 用GitHub Desktop, 然后clone Specs项目。
3. 将clone的Specs项目的文件夹改名为master，然后拖到/Users/用户名/.cocoapods/repos目录下。
4. 运行pod setup



关于cocoapods的使用

不更新Specs的pod install 速度会快
`pod install --verbose --no-repo-update`


