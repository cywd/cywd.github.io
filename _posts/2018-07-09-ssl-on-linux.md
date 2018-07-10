---
layout: post
title: Linux下自制HTTPS证书
excerpt: "Linux下自签证书，用于单向认证，双向认证"
categories: ["Linux", "OpenResty", "SSL"]
tags: ["Linux", "OpenResty", "SSL"]
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

## 准备目录

创建一个测试目录

```shell
mkdir /home/testDemo 
```

```shell
cd /home/testDemo/
```

创建要生成证书的目录

```shell
mkdir ssl
```

```shell
cd ssl/
```

## 制作CA证书

### 1.创建CA证书密钥 ca.key

```shell
openssl genrsa -des3 -out ca.key 2048
```

输出

```shell
Generating RSA private key, 2048 bit long modulus
.............+++
..................................................+++
e is 65537 (0x10001)
Enter pass phrase for ca.key: ← 输入一个新密码 
Verifying - Enter pass phrase for ca.key: ← 确认密码 
```

### 2.创建CA证书的申请文件 ca.csr

```shell
openssl req -new -key ca.key -out ca.csr
```

输出

```shell
Enter pass phrase for ca.key: ← 刚刚创建ca.key的密码
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN ← 国家代号，中国输入CN 
State or Province Name (full name) [Some-State]:Beijing ← 省的全名，拼音 
Locality Name (eg, city) []:Beijing ← 市的全名，拼音
Organization Name (eg, company) [Internet Widgits Pty Ltd]:MyCompany Corp. ← 公司英文名
Organizational Unit Name (eg, section) []: ← 可以不输入 
Common Name (e.g. server FQDN or YOUR name) []: ← 此时不输入
Email Address []:admin@mycompany.com ← 电子邮箱，可随意填

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []: ← 可以不输入 
An optional company name []: ← 可以不输入 
```

### 3.创建一个自当前日期起为期十年的CA证书 ca.crt

其中`-extfile`后面的路径是`openssl version -a`查出来的`OPENSSLDIR`。

```shell
openssl x509 -req -days 3650 -sha256 -extfile /usr/local/ssl/openssl.cnf -extensions v3_ca -signkey ca.key -in ca.csr -out ca.crt
```

输出

```shell
Signature ok 
subject=/C=CN/ST=Beijing/L=Beijing/O=MyCompany Corp./emailAddress=admin@mycompany.com
Getting Private key 
Enter pass phrase for ca.key: ← 输入前面创建ca.key的密码
```

### 4.根据CA证书生成truststore JKS文件 ca.truststore

```shell
keytool -keystore ca.truststore -keypass 123456 -storepass 123456 -alias ca -import -trustcacerts -file ./ca.crt
```

输出

```shell
所有者: EMAILADDRESS=admin@mycompany.com, O=MyCompany Corp., L=Beijing, ST=Beijing, C=CN
发布者: EMAILADDRESS=admin@mycompany.com, O=MyCompany Corp., L=Beijing, ST=Beijing, C=CN
序列号: e326870e0912e25f
有效期开始日期: Tue Jul 09 09:27:53 CST 2018, 截止日期: Fri Jul 06 09:27:53 CST 2028
证书指纹:
	 MD5: 04:1F:42:2F:6A:C0:B8:94:6E:25:31:35:F6:0E:AD:AF
	 SHA1: D5:E1:3E:E2:0E:CE:43:B5:65:2A:9E:8D:DA:75:3B:B7:AB:28:7D:96
	 SHA256: 6D:C4:C8:30:8D:AC:D9:DC:AA:EC:64:E8:42:1D:5A:B2:DB:7A:9D:CB:EF:0A:0B:4D:FE:54:90:B5:F1:9B:B3:0B
	 签名算法名称: SHA256withRSA
	 版本: 3

扩展:

#1: ObjectId: 2.5.29.35 Criticality=false
AuthorityKeyIdentifier [
KeyIdentifier [
0000: D0 E6 93 81 F6 ED A5 54   CE 81 38 E8 83 D2 B3 2B  .......T..8....+
0010: 5A 47 24 AC                                        ZG$.
]
]

#2: ObjectId: 2.5.29.19 Criticality=false
BasicConstraints:[
  CA:true
  PathLen:2147483647
]

#3: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: D0 E6 93 81 F6 ED A5 54   CE 81 38 E8 83 D2 B3 2B  .......T..8....+
0010: 5A 47 24 AC                                        ZG$.
]
]

是否信任此证书? [否]:  yes
错误的答案, 请再试一次
是否信任此证书? [否]:  y
证书已添加到密钥库中
```

## 制作服务端证书

### 1.创建服务端证书密钥 server.key

```shell
openssl genrsa -des3 -out server.key 2048
```

输出

```shell
Generating RSA private key, 2048 bit long modulus
........................+++
.................................................................................................+++
e is 65537 (0x10001)
Enter pass phrase for server.key: ← 输入新密码
Verifying - Enter pass phrase for server.key: ← 确认密码
```

运行时会提示输入密码,此密码用于加密`key`文件(参数`des3`便是指加密算法,当然也可以选用其他你认为安全的算法.),以后每当需读取此文件(通过`openssl`提供的命令或`API`)都需输入口令.如果觉得不方便,也可以去除这个口令,但一定要采取其他的保护措施! 

去除`key`文件口令的命令: 

```shell
openssl rsa -in server.key -out server.key
```

### 2.创建服务端证书的申请文件 server.csr

```shell
openssl req -new -key server.key -out server.csr
```

输出

```shell
Enter pass phrase for server.key: ← 输入前面创建server.key的密码
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN ← 国家代号，中国输入CN 
State or Province Name (full name) [Some-State]:Beijing ← 省的全名，拼音 
Locality Name (eg, city) []:Beijing ← 市的全名，拼音
Organization Name (eg, company) [Internet Widgits Pty Ltd]:MyCompany Corp. ← 公司英文名
Organizational Unit Name (eg, section) []: ← 可以不输入 
Common Name (e.g. server FQDN or YOUR name) []:192.168.27.222 ← 服务器主机名(或者IP)，若填写不正确，浏览器会报告证书无效，但并不影响使用
Email Address []:admin@mycompany.com ← 电子邮箱，可随意填

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []: ← 可以不输入 
An optional company name []: ← 可以不输入 
```

### 3.创建自当前日期起有效期为期十年的服务端证书 server.crt

```shell
openssl x509 -req -days 3650 -sha256 -extfile /usr/local/ssl/openssl.cnf -extensions v3_req -CA ca.crt -CAkey ca.key -CAcreateserial -in server.csr -out server.crt
```

输出

```shell
Signature ok
subject=/C=CN/ST=Beijing/L=Beijing/O=MyCompany Corp./CN=192.168.27.222/emailAddress=admin@mycompany.com
Getting CA Private Key
Enter pass phrase for ca.key: ← 输入前面创建ca.key的密码
```

### 4.导出p12文件 server.p12

```shell
openssl pkcs12 -export -in server.crt -inkey server.key -out server.p12 -name "server"
```

输出

```shell
Enter pass phrase for server.key: ← 输入前面创建server.key的密码
Enter Export Password: ← 输入创建p12的密码
Verifying - Enter Export Password: ← 确认创建p12的密码
```

### 5.将p12 文件导入到keystore JKS文件 server.keystore

这里`srcstorepass`后面的`p12pwd`为`server.p12`的密码`deststorepass`后的`keystorepwd`为`keyStore`的密码

```shell
keytool -importkeystore -v -srckeystore  server.p12 -srcstoretype pkcs12 -srcstorepass p12pwd -destkeystore server.keystore -deststoretype jks -deststorepass keystorepwd
```

输出

```shell
已成功导入别名 server 的条目。
已完成导入命令: 1 个条目成功导入, 0 个条目失败或取消
[正在存储server.keystore]
```

## 制作client客户端证书

### 1.创建客户端证书密钥文件 client.key

```shell
openssl genrsa -des3 -out client.key 2048
```

输出

```shell
Generating RSA private key, 2048 bit long modulus
.............................................+++
...............................................................+++
e is 65537 (0x10001)
Enter pass phrase for client.key:
Verifying - Enter pass phrase for client.key:
```

### 2.创建客户端证书的申请文件 client.csr

```shell
openssl req -new -key client.key -out client.csr
```

输出

```shell
Enter pass phrase for client.key: ← 输入上一步中创client.key建的密码
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN ← 国家代号，中国输入CN 
State or Province Name (full name) [Some-State]:Beijing ← 省的全名，拼音 
Locality Name (eg, city) []:Beijing ← 市的全名，拼音
Organization Name (eg, company) [Internet Widgits Pty Ltd]:MyCompany Corp. ← 公司英文名
Organizational Unit Name (eg, section) []: ← 可以不输入 
Common Name (e.g. server FQDN or YOUR name) []:cy ← 自己的英文名，可以随便填 
Email Address []:admin@mycompany.com ← 电子邮箱，可随意填

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []: ← 可以不输入 
An optional company name []: ← 可以不输入 
```

### 3.创建一个自当前日期起有效期为十年的客户端证书 client.crt

```shell
openssl x509 -req -days 3650 -sha256 -extfile /usr/local/ssl/openssl.cnf -extensions v3_req -CA ca.crt -CAkey ca.key -CAcreateserial -in client.csr -out client.crt
```

输出

```shell
Signature ok
subject=/C=CN/ST=Beijing/L=Beijing/O=MyCompany Corp./emailAddress=admin@mycompany.com
Getting Private key 
Enter pass phrase for ca.key: ← 输入前面创建ca.key的密码
```

### 4.导出.p12文件 client.p12

```shell
openssl pkcs12 -export -in client.crt -inkey client.key -out  client.p12 -name "client"
```

输出

```shell
Enter pass phrase for client.key: ← 输入前面创建client.key的密码
Enter Export Password: ← 输入创建p12的密码
Verifying - Enter Export Password: ← 确认创建p12的密码
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
4. **X.509 PAM**编码(Base64)的后缀是： .PEM .CER .CRT
5. **.cer/.crt**是用于存放证书，它是2进制形式存放的，不含私钥。
6. **.pem跟crt/cer**的区别是它以Ascii来表示。
7. **pfx/p12**用于存放个人证书/私钥，他通常包含保护密码，2进制方式
8. **p10**是证书请求
9. **p7r**是CA对证书请求的回复，只用于导入
10. **p7b**以树状展示证书链(certificate chain)，同时也支持单个证书，不含私钥。

# 参考

[https://blog.csdn.net/andy_zhang2007/article/details/78805578](https://blog.csdn.net/andy_zhang2007/article/details/78805578)

[https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html](https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html)

[https://blog.csdn.net/fyang2007/article/details/6180361](https://blog.csdn.net/fyang2007/article/details/6180361)

[https://www.chinassl.net/ssltools/convert-ssl.html](https://www.chinassl.net/ssltools/convert-ssl.html)