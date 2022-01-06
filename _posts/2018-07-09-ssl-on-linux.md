---
layout: post
title: Linux下自制HTTPS证书
excerpt: "Linux下自签证书，用于单向认证，双向认证"
categories: ["Linux", "OpenResty", "SSL", "Nginx"]
tags: ["Linux", "OpenResty", "SSL", "Nginx"]
date: 2018-07-09
comments: true
---

* TOC
{:toc}
---

# OpenSSL

## 介绍

[OpenSSL](https://baike.baidu.com/item/openssl/5454803?fr=aladdin)是一个安全[套接字](https://baike.baidu.com/item/%E5%A5%97%E6%8E%A5%E5%AD%97)层密码库，囊括主要的[密码算法](https://baike.baidu.com/item/%E5%AF%86%E7%A0%81%E7%AE%97%E6%B3%95)、常用的[密钥](https://baike.baidu.com/item/%E5%AF%86%E9%92%A5)和证书封装管理功能及[SSL](https://baike.baidu.com/item/SSL)协议，并提供丰富的应用程序供测试或其它目的使用。

## 查看版本信息

### 普通

```shell
openssl version
```

输出

```shell
OpenSSL 1.0.2g  1 Mar 2016
```

### 详细

```shell
openssl version -a
```

输出

```shell
OpenSSL 1.0.2g  1 Mar 2016
built on: reproducible build, date unspecified
platform: linux-x86_64
options:  bn(64,64) rc4(16x,int) des(idx,cisc,16,int) idea(int) blowfish(idx)
compiler: gcc -I. -I.. -I../include  -fPIC -DOPENSSL_PIC -DZLIB_SHARED -DZLIB -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -Wa,--noexecstack -m64 -DL_ENDIAN -O3 -Wall -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM -DECP_NISTZ256_ASM
OPENSSLDIR: "/usr/local/ssl"
```

# 制作证书

## CA

创建一个新的 CA 根证书，在 nginx 安装目录下新建 ca 文件夹，进入 ca，创建几个子文件夹

```shell
mkdir ca && cd ca  
mkdir newcerts private conf server

# newcerts 子目录将用于存放 CA 签署过的数字证书(证书备份目录)；private 用于存放 CA 的私钥；conf 目录用于存放一些简化参数用的配置文件；server 存放服务器证书文件。
```

### conf 目录新建 openssl.conf 文件

```nginx
[ ca ] 
default_ca     = CA_default          	# The default ca section 

[ CA_default ] 
dir            = ./                   # top dir
database       = ./index.txt          # index file.  
new_certs_dir  = ./newcerts           # new certs dir 

certificate    = ./private/ca.crt         # The CA cert  
serial         = ./serial             # serial no file  
private_key    = ./private/ca.key  # CA private key  
RANDFILE       = ./private/.rand      # random number file 

default_days   = 3650                     # how long to certify for  
default_crl_days= 30                     # how long before next CRL  
default_md     = sha256                     # message digest method to use  
unique_subject = no                      # Set to 'no' to allow creation of  
                                         # several ctificates with same subject. 
policy         = policy_match              # default policy 

[ policy_match ] 
countryName = match  
stateOrProvinceName = match  
organizationName = match  
organizationalUnitName = match  
localityName            = optional  
commonName              = supplied  
emailAddress            = optional  
```

### 生成私钥 key 文件

```shell
openssl genrsa -out private/ca.key 2048 
```

输出

```shell
Generating RSA private key, 2048 bit long modulus  
.......+++
.........................+++
e is 65537 (0x10001)  
private 目录下有 ca.key 文件生成。 
```

### 生成证书请求 csr 文件

```shell
openssl req -new -key private/ca.key -out private/ca.csr  
```

### 生成凭证 crt 文件

```shell
openssl x509 -req -days 365 -in private/ca.csr -signkey private/ca.key -out private/ca.crt  
```

private 目录下有 ca.crt 文件生成。

### 为我们的 key 设置起始序列号(可以是任意四个字符)和创建 CA 键库

```shell
echo FACE > serial  
touch index.txt  
```

### 为 "用户证书" 的移除创建一个证书撤销列表

```shell
openssl ca -gencrl -out ./private/ca.crl -crldays 7 -config "./conf/openssl.conf"  

```

输出:

```shell
Using configuration from ./conf/openssl.conf  
private 目录下有 ca.crl 文件生成。 
```

## 服务器证书的生成

### 创建一个 key

```shell
openssl genrsa -out server/server.key 2048  
```

### 为我们的 key 创建一个证书签名请求 csr 文件

```shell
openssl req -new -key server/server.key -out server/server.csr  
```

### 使用我们私有的 CA key 为刚才的 key 签名

```shell
openssl ca -in server/server.csr -cert private/ca.crt -keyfile private/ca.key -out server/server.crt -config "./conf/openssl.conf"
```

输出

```shell
Using configuration from ./conf/openssl.conf  
Check that the request matches the signature  
Signature ok  
The Subject's Distinguished Name is as follows  
countryName           :PRINTABLE:'CN'  
stateOrProvinceName   :ASN.1 12:'BJ'  
localityName          :ASN.1 12:'BJ'  
organizationName      :ASN.1 12:'****'  
organizationalUnitName:ASN.1 12:'BJ'  
commonName            :ASN.1 12:'**'  
emailAddress          :IA5STRING:'****'  
Certificate is to be certified until Aug 17 10:15:15 2029 GMT (3650 days) 
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y  
Write out database with 1 new entries  
Data Base Updated  
```

注：签名信息每次必须输入一致



## 客户端证书的生成 

### 创建存放 key 的目录 users

```shell
mkdir users
```

### 为用户创建一个 key

```shell
openssl genrsa -des3 -out ./users/client.key 2048  
```

输出：

```shell
Enter pass phrase for ./users/client.key:123  
Verifying - Enter pass phrase for ./users/client.key:123  
#要求输入 pass phrase，这个是当前 key 的口令，以防止本密钥泄漏后被人盗用。两次输入同一个密码(比如我这里输入     123)，users 目录下有 client.key 文件生成。
```

### 为 key 创建一个证书签名请求 csr 文件

```shell
openssl req -new -key ./users/client.key -out ./users/client.csr  
```

users 目录下有 client.csr 文件生成。

### 使用我们私有的 CA key 为刚才的 key 签名

```shell
openssl ca -in ./users/client.csr -cert ./private/ca.crt -keyfile ./private/ca.key -out    ./users/client.crt -config "./conf/openssl.conf"  
```

将证书转换为大多数浏览器都能识别的 PKCS12 文件

```shell
openssl pkcs12 -export -clcerts -in ./users/client.crt -inkey ./users/client.key -out ./users/client.p12  
```

输出

```shell
Enter pass phrase for ./users/client.key:  
Enter Export Password:  
Verifying - Enter Export Password:  
```

输入密码后，users 目录下有 client.p12 文件生成。

最终目录大概如下

```shell
.
├── conf
│   └── openssl.conf
├── index.txt
├── index.txt.attr
├── index.txt.attr.old
├── index.txt.old
├── newcerts
│   ├── FACE.pem
│   └── FACF.pem
├── private
│   ├── ca.crl
│   ├── ca.crt
│   ├── ca.csr
│   └── ca.key
├── serial
├── serial.old
├── server
│   ├── server.crt
│   ├── server.csr
│   └── server.key
└── users
    ├── client.crt
    ├── client.csr
    ├── client.key
    └── client.p12
```



# Nginx配置

```nginx
server {
    listen 443; 
    server_name localhost; 
    ssi on; 
    ssi_silent_errors on; 
    ssi_types text/shtml; 

    ssl                  on;
    ssl_certificate      /usr/local/nginx/ca/server/server.crt; 
    ssl_certificate_key  /usr/local/nginx/ca/server/server.key; 
    # 这里放ca证书，用来校验ca颁发的客户端证书
    ssl_client_certificate /usr/local/nginx/ca/private/ca.crt; 

    ssl_session_timeout  5m; 
    ssl_verify_client on;  # 开户客户端证书验证 
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    # ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDH:AES:HIGH:!aNULL:!MD5:!ADH:!DH;

    ssl_prefer_server_ciphers   on; 
}
```

# 解释

## SSL

`Secure Sockets Layer`,现在应该叫`"TLS"`,但由于习惯问题,我们还是叫`"SSL"`比较多.`http`协议默认情况下是不加密内容的,这样就很可能在内容传播的时候被别人监听到,对于安全性要求较高的场合,必须要加密,`https`就是带加密的`http`协议,而`https`的加密是基于`SSL`的,它执行的是一个比较下层的加密,也就是说,在加密前,你的服务器程序在干嘛,加密后也一样在干嘛,不用动,这个加密对用户和开发者来说都是透明的.

## X.509

这是一种证书标准,主要定义了证书中应该包含哪些内容.其详情可以参考`RFC5280`,`SSL`使用的就是这种证书标准.

## PEM

`Privacy Enhanced Mail`,打开看文本格式,以`"-----BEGIN..."`开头, `"-----END..."`结尾,内容是`BASE64`编码. 查看`PEM`格式证书的信息:

```shell
openssl x509 -in server.pem -text -noout 
```

`Apache`和`*NIX`服务器偏向于使用这种编码格式.

## DER

`Distinguished Encoding Rules`,打开看是二进制格式,不可读. 查看`DER`格式证书的信息:

```shell
openssl x509 -in server.der -inform der -text -noout 
```

`Java`和`Windows`服务器偏向于使用这种编码格式.

## CRT

`CRT`应该是`certificate`的三个字母,其实还是证书的意思,常见于`*NIX`系统,有可能是`PEM`编码,也有可能是`DER`编码,大多数应该是`PEM`编码,相信你已经知道怎么辨别.

## CER

还是`certificate`,还是证书,常见于`Windows`系统,同样的,可能是`PEM`编码,也可能是`DER`编码,大多数应该是`DER`编码.

## KEY

通常用来存放一个公钥或者私钥,并非`X.509`证书,编码同样的,可能是`PEM`,也可能是`DER`. 查看`KEY`的办法:

```shell
openssl rsa -in server.key -text -noout 
```

如果是`DER`格式的话,同理应该这样了:

```shell
openssl rsa -in server.key -text -noout -inform der
```

## CSR

`Certificate Signing Request`,即证书签名请求,这个并不是证书,而是向权威证书颁发机构获得签名证书的申请,其核心内容是一个公钥(当然还附带了一些别的信息),在生成这个申请的时候,同时也会生成一个私钥,私钥要自己保管好.做过`iOS APP`的朋友都应该知道是怎么向苹果申请开发者证书的吧. 查看的办法:

```shell
openssl req -noout -text -in server.csr 
```

如果是DER格式的话:

```shell
openssl req -noout -text -in server.csr -inform der
```

## PFX/P12

`predecessor of PKCS#12`,对`*nix`服务器来说,一般`CRT`和`KEY`是分开存放在不同文件中的,但`Windows`的`IIS`则将它们存在一个`PFX`文件中,(因此这个文件包含了证书及私钥)这样会不会不安全？应该不会,`PFX`通常会有一个"提取密码",你想把里面的东西读取出来的话,它就要求你提供提取密码,`PFX`使用的时`DER`编码,如何把`PFX`转换为`PEM`编码？

```shell
openssl pkcs12 -in server.pfx -out server.pem -nodes
```

这个时候会提示你输入提取代码. `server.pem`就是可读的文本.
生成`pfx`的命令类似这样:

```shell
openssl pkcs12 -export -in server.crt -inkey privateKey.key -out server.pfx -certfile ca.crt
```

其中`ca.crt`是`CA`(权威证书颁发机构)的根证书,有的话也通过`-certfile`参数一起带进去.这么看来`,PFX`其实是个证书密钥库.

## Keytool

是一个`Java`数据证书的管理工具 ,`Keytool`将密钥（`key`）和证书（`certificates`）存在一个称为`keystore`的文件中。 

## KeyStore

服务器的密钥存储库，存服务器的公钥私钥证书。用于服务器认证服务端。包含两种数据： 1.密钥实体（`Key entity`）——密钥（`secret key`）又或者是私钥和配对公钥（采用非对称加密）   2. 可信任的证书实体（`trusted certificate entries`）——只包含公钥

## TrustStore

服务器的信任密钥存储库，存`CA`公钥。用于客户端认证服务器。

## JKS

即`Java Key Storage`,这是`Java`的专利,跟`OpenSSL`关系不大,利用`Java`的一个叫"`keytool`"的工具,可以将`PFX`转为`JK`S,当然了,`keytoo`l也能直接生成`JKS`.

## 证书编码的转换

PEM转为DER 

```shell
openssl x509 -in server.crt -outform der -out server.der
```

DER转为PEM 

```shell
openssl x509 -in server.crt -inform der -outform pem -out server.pem
```

(提示:要转换`KEY`文件也类似,只不过把`x509`换成`rsa`,要转`CSR`的话,把`x509`换成`req`...)

## 证书格式介绍

PKCS 全称是 Public-Key Cryptography Standards ，是由 RSA 实验室与其它安全系统开发商为促进公钥密码的发展而制订的一系列标准，PKCS 目前共发布过 15 个标准。 常用的有：

1. PKCS#7 Cryptographic Message Syntax Standard
2. PKCS#10 Certification Request Standard
3. PKCS#12 Personal Information Exchange Syntax Standard

X.509是常见通用的证书格式。所有的证书都符合为Public Key Infrastructure (PKI) 制定的 ITU-T X509 国际标准。

1. **PKCS#7**常用的后缀是： .P7B .P7C .SPC
2. **PKCS#12**常用的后缀有： .P12 .PFX
3. **X.509 DER**编码(ASCII)的后缀是： .DER .CER .CRT
4. **X.509 PEM**编码(Base64)的后缀是： .PEM .CER .CRT
5. **.cer/.crt**是用于存放证书，它是2进制形式存放的，不含私钥。
6. **.pem跟crt/cer**的区别是它以Ascii来表示。
7. **pfx/p12**用于存放个人证书/私钥，他通常包含保护密码，2进制方式
8. **p10**是证书请求
9. **p7r**是CA对证书请求的回复，只用于导入
10. **p7b**以树状展示证书链(certificate chain)，同时也支持单个证书，不含私钥。

# 参考

[https://blog.csdn.net/andy_zhang2007/article/details/78805578](https://blog.csdn.net/andy_zhang2007/article/details/78805578)

[https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html](https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html)

[https://www.chinassl.net/ssltools/convert-ssl.html](https://www.chinassl.net/ssltools/convert-ssl.html)

