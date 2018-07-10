---
layout: post
title: Linux下自制SSL证书
excerpt: "Linux下自制SSL证书"
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

```
openssl rsa -inserver.key -out server.key
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

| 名称       | 解释                                                         |
| ---------- | ------------------------------------------------------------ |
| key        | 通常指私钥                                                   |
| csr        | 是`Certificate Signing Request`的缩写，即证书签名请求，这不是证书，可以简单理解成公钥，生成证书时要把这个提交给权威的证书颁发机构。 |
| crt        | 即 `certificate`的缩写，即证书。                             |
| p12        | 个人信息交换语法标准， 包含私钥、公钥及其证书， 密钥库和私钥用相同密码进行保护 |
| JKS        | 存放密钥的容器。`.jks .keystore .truststore`等               |
| Keytool    | 是一个`Java`数据证书的管理工具 ,`Keytool`将密钥（key）和证书（certificates）存在一个称为`keystore`的文件中。 |
| KeyStore   | 服务器的密钥存储库，存服务器的公钥私钥证书。用于服务器认证服务端。包含两种数据： 1.密钥实体（Key entity）——密钥（secret key）又或者是私钥和配对公钥（采用非对称加密）   2. 可信任的证书实体（trusted certificate entries）——只包含公钥 |
| TrustStore | 服务器的信任密钥存储库，存`CA`公钥。用于客户端认证服务器。   |
| X.509      | 是一种证书格式.对`X.509`证书来说，认证者总是`CA`或由`CA`指定的人，一份`X.509`证书是一些标准字段的集合，这些字段包含有关用户或设备及其相应公钥的信息。 |

`X.509`的证书文件，一般以`.crt`结尾，根据该文件的内容编码格式，可以分为以下二种格式：

| 名称   | 解释                                                         |
| ------ | ------------------------------------------------------------ |
| PEM  | `Privacy Enhanced Mail`,打开看文本格式,以"-----BEGIN..."开头, "-----END..."结尾,内容是`BASE64`编码.` Apache`和`*NIX`服务器偏向于使用这种编码格式. |
| DER | `Distinguished Encoding Rules`,打开看是二进制格式,不可读.`Java`和`Windows`服务器偏向于使用这种编码格式 |



# 参考

[https://blog.csdn.net/andy_zhang2007/article/details/78805578](https://blog.csdn.net/andy_zhang2007/article/details/78805578)

[https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html](https://www.cnblogs.com/yjmyzz/p/openssl-tutorial.html)

[https://blog.csdn.net/fyang2007/article/details/6180361](https://blog.csdn.net/fyang2007/article/details/6180361)