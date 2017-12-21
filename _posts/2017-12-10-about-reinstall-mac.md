---
layout: post
title: 关于重新安装Mac
excerpt: "由于在升级系统的时候意外断电黑屏，导致系统故障，遂重装系统，本文主要记录下，重装系统及新系统需要做的事情。"
categories: ["Mac"]
tags: ["Mac"]
date: 2017-12-10
comments: true
---

* TOC
{:toc}
---

# 重装系统

开机的时候按住 `Command + R`，直到出现苹果标及进度条。

进入恢复模式之后，可以先格式化磁盘，然后选第二项安装系统，前提是要先联接上Wi-Fi，然后等着就行的，有进度时间提示，根据每个人网速不同时间不定。整个进度都走完会进入系统，由于我是格式化了磁盘，所以会提示进行各种设置，都设置完就可以进入系统了，新的一样。

# 新系统配置开发环境

## 最先的一些配置

打开"安全性与隐私"中"任何来源"选项.

```
sudo spctl --master-disable
```

显示所有隐藏文件

```
defaults write com.apple.finder AppleShowAllFiles YES
```



## Xcode

这个不多说，第一个安装毫无疑问。`App Store` 下载即可。就是时间比较久。

## 一些常用软件

由于`Xcode`比较大安装比较慢，期间我会安装一些常用的软件

### QQ 微信

不多说，可以从官网或者`App Store` 下载。

### Paste 2

可以查看复制的历史记录的软件。很好用。个人从 App Store 下载。

### App Icon Gear

生成` 1x 2x 3x `图片 和` Launch Image `。 开发时会用到。

### Status Barred

去掉带状态条的截屏图片中的状态条。

### Sip

取色器，还挺好用的

### IconKit

生成 `iOS Mac` 的 应用图标。平时要求不太严格的时候还挺好用的。要求严格找设计吧。

### Keynote Numbers Pages

办公软件

### The Unarchiver

解压RAR的

### 有道词典

用来查单词

### 网易云音乐

超级好的歌单和评论。

### HandShaker

锤子出品的安卓手机传输软件。

### 蓝灯

`github`上找。不多说。

### Typora

网上搜。用来写`Markdown`，个人用着还习惯。

### Reveal 4

可以去 [史蒂芬周的博客](http://www.sdifen.com) 找。个人硬盘备份。

### Dash

[史蒂芬周的博客](http://www.sdifen.com) 找

### ifunboxmac

[官网](http://www.i-funbox.com/en_download.html)下载

### MindNode

思维导图

### Office 

不得不装，适应周边大环境。虽然个人觉得 Pages 什么的更好用。

### Photoshop AI

偶尔用来切个图

## iTerm2 + oh my zsh

谁用谁知道。

先安装`iTerm2`

[iTerm2官网](http://www.iterm2.com)

[下载](http://www.iterm2.com/downloads.html)

安装`oh my zsh`

[oh my zsh官网](http://ohmyz.sh)

`curl` 

```shell
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

`wget`

```shell
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

`curl`在`command line tools`安装之后，就会有。

`cURL` [官网](https://curl.haxx.se)

安装`command line tools`，安装完Xcode会有，或者也可以

```shell
xcode-select --install
```

然后会有提示。点击安装就可以。

而`wget`可以通过`homebrew`安装

```shell
brew install wget
```

或者

```shell
curl -O http://ftp.gnu.org/gnu/wget/wget-1.13.4.tar.gz

tar xzvf wget-1.13.4.tar.gz
cd wget-1.13.4
./configure --with-ssl=openssl
sudo make
sudo make install
which wget #Should output: /usr/local/bin/wge
```



配色、主题和插件

配色采用[solarized](http://ethanschoonover.com/solarized)

打开`iTerm2`的偏好设置，`Profiles -> Colors` 选择 `Solarized Dark`。

主题采用`agnoster`

```
vi ~/.zshrc
```

打开后找到`ZSH_THEME="robbyrussell"`修改为`ZSH_THEME="agnoster"`

这个时候会出现乱码 `？`

不要担心，是因为没有配套的字体。

`Powerline`字体下载安装

`clone`到随便的位置，`cd`到`fonts`目录，执行 `install.sh`。这样字体就都安装了。

```shell
git clone https://github.com/powerline/fonts.git
cd fonts
./install.sh
```

接着可以到`iTerm2`偏好设置中，找到修改字体的选项，修改字体为后缀带有`powerline`的字体。`？`是不是没有了。

接着安装插件，注意插件有很多，不过安装的插件越多程序反应会越慢。

这里我们只安装一个插件 [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting.git)

执行

```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

接着再

```shell
vi ~/.zshrc
```

打开后找到

```shell
plugins=( [已有插件]  zsh-syntax-highlighting )
```

source 一下 使其生效。

```
source ~/.zshrc
```

## Homebrew

[官网](https://brew.sh)

安装(Install)

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

安装 `tree`

```shell
brew install tree
```

## Git

安装`command line tools`就有了。当然也可以自己安装。

说下个人`Git`的配置

别名

```shell
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci "commit -m"
git config --global alias.s status
git config --global alias.p push
```

## CocoaPods

安装`rvm`

```
curl -L https://get.rvm.io | bash -s stable
```

安装`rails`

```
sudo gem install rails
```

安装`CocoaPods`

```
sudo gem install -n /usr/local/bin cocoapods
```

然后

```
pod setup
```



## Python3

安装

```shell
brew install Python3
```

## mysql

[官网](https://www.mysql.com)

`Mac OS `系统的`MySQL`的版本：`MySQL Community Server (GPL)`，在下载页面提供有两种格式的文件下载,一种为`tar.gz`格式，另一种为`dmg`格式，这里推荐`dmg`格式。

一路安装。中间会有个弹框，请记住里面的密码 （是`mysql root `账户默认的密码）

安装好以后，去系统的偏好设置里找到`mysql`，开启`mysql`服务。

此时我们在命令行输入`mysql -u root -p`命令会提示`commod not found`，我们还需要将`mysq`l加入系统环境变量。

```shell
cd ~/
# 分别打开.zshrc 和 .profile
vim ./.zshrc 
vim ./.profile
```

添加 

```shell
# Add Mysql to PATH for scripting.
export PATH="$PATH:/usr/local/mysql/bin" 
```

source 一下 使其生效

```shell
source ~/.profile
source ~/.zshrc 
```

现在你就可以通过`mysql -u root -p`登录`mysql`了，会让你输入密码，就是之前记下来那一串。

登陆成功后，可以更改密码

```
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('你想要设置的新密码');
```

也可以使用` homebrew`安装 `mysql`，这里就不说了。

## 各种编辑器

### Sublime

### VisualCode

### Atom

### TextMate

### Android Studio

写Android的

### WebStorm

不多说

### PyCharm

个人用来写Python项目

### Unity

不多说

