---
layout: post
title: 在RedHat上部署OpenResty
excerpt: "在RedHat上部署OpenResty"
categories: ["Linux", "OpenResty"]
tags: ["Linux", "OpenResty"]
date: 2018-07-06
comments: true
---

* TOC
{:toc}
---

# 1.安装依赖库

```shell
yum install -y gcc gcc-c++ readline-devel pcre-devel openssl-devel tcl perl
```

# 2.下载及安装`OpenResty`

包括一些下载地址和安装说明可以看[OpenResty官网](http://openresty.org/cn/)。

我这里就说一下我的安装过程，

```shell
# 我这里规定下载的要放到这里  /home/soft/
cd /home/soft/
wget --no-check-certificate https://openresty.org/download/openresty-1.13.6.2.tar.gz
tar -xzvf openresty-1.13.6.2.tar.gz
cd openresty-1.13.6.2/
```

下面开始配置

```shell
# 解释一下，--prefix= 是openresty的安装路径，
# --with-openssl= 指定openssl， 
# --with-pcre= 指定pcre，
# --add-module= 加模块， 
# --with-http_ssl_module 支持https
./configure  --prefix=/home/openresty --with-http_ssl_module --with-openssl=/home/solft/openssl/openssl-1.0.2g --with-pcre=/home/solft/pcre-8.40 --add-module=/home/solft/nginx_http_upstream_check_module
```

接着

```shell
gmake
```

注意执行gmake的时候可能会报错。看报什么错，如果是关于opessl的，可以像上一步手动指定openssl

如果没有出现什么问题可以接着执行

```shell
gmake install
```

如果一切顺利，恭喜部署成功了。

最后为了方便调用可以

```shell
export PATH=$PATH:/home/openresty/nginx/sbin
```

或者是改成其他名字

```shell
export OPENRESTY_HOME="/home/openresty/"
export OPENRESTY_NGINX="/home/openresty/nginx/sbin/nginx"
```

# 3.注意

`openssl`的版本更替中，`API`的改动非常大，版本兼容有问题，`OpenResty`需要的`openssl`版本，一定要匹配。

我这里是` openresty-1.13.6.2` 和 `openssl-1.0.2g`以及`pcre-8.40`。

