---
layout: post
title: "iOS HTTPS双向认证"
excerpt: "主要是针对自签证书的双向认证，这里只说iOS端代码实现"
categories: [iOS, HTTPS]
tags: [iOS, HTTPS, 双向认证]
date: 2017-06-10
comments: true
---

* TOC
{:toc}
---

# 准备证书

首先需要后端提供的证书

## CA证书.cer（根证书）

如果后端提供的是`.crt`格式的根证书，我们需要转换一下：

双击`.crt`文件添加根证书到钥匙串，然后右键选择导出为`.cer`

## 客户端.p12文件

如果后端提供的是`.pem`，我们需要转换一下：

双击`.pem`文件添加根证书到钥匙串，然后右键选择导出为`.p12`文件

# OC代码

结合`AFNetworking`实现了自签证书的双向认证

```objective-c
static AFHTTPSessionManager *baseURLManager = nil;
+ (AFHTTPSessionManager *)baseURLManager
{
    if (!baseURLManager)
    {
        baseURLManager = [AFHTTPSessionManager manager];
        baseURLManager.responseSerializer = [AFHTTPResponseSerializer serializer];
        [baseURLManager.requestSerializer setValue:@"Keep-Alive" forHTTPHeaderField:@"connection"];
        baseURLManager.requestSerializer.timeoutInterval = 10.0f;
        // 设置提交的内容的编码
        [baseURLManager.requestSerializer setValue:@"application/x-www-form-urlencoded; charset=utf-8" forHTTPHeaderField:@"Content-Type"];
    }
    return baseURLManager;
}

+ (NSURLSessionDataTask *)POST:(NSString *)url parameters:(NSDictionary *)parameters success:(void (^)(NSURLSessionDataTask * task, id responseObject))success failure:(void (^)(NSURLSessionDataTask * task, NSError * error))failure {
    
    AFHTTPSessionManager *manager = [self baseURLManager];
    
    NSString *baseUrl = [FHAPITool getBaseURL];
    NSString *finUrl = [baseUrl stringByAppendingString:url];
    
    RLog(@"finurl -- %@", finUrl);
    
    // 配置https验证策略
    if ([finUrl hasPrefix:@"https://"]) {
        [self securityPolicyForHTTPSessionManager:manager];
        
        [[self class] setSessionDidReceiveAuthenticationChallengeWithManager:manager];
    } else {
        manager.securityPolicy = [AFSecurityPolicy defaultPolicy];
    }
    
    NSURLSessionDataTask *dataTask = [manager POST:finUrl parameters:parameters progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nonnull responseObject) {
        
        if (success) {
            success(task, responseObject);
        }
        
    } failure:^(NSURLSessionDataTask * _Nonnull task, NSError * _Nonnull error) {
        RLog(@"error - %@", error);
        if (failure) {
            failure(task, error);
        }
    }];
    
    return dataTask;
}


#pragma mark - privte methods

+ (void)setSessionDidReceiveAuthenticationChallengeWithManager:(AFHTTPSessionManager *)manager{
    
    __weak typeof(manager)weakManager = manager;
    __weak typeof(self)weakSelf = self;
    
    [manager setSessionDidReceiveAuthenticationChallengeBlock:^NSURLSessionAuthChallengeDisposition(NSURLSession *session, NSURLAuthenticationChallenge *challenge, NSURLCredential *__autoreleasing*_credential) {
        NSURLSessionAuthChallengeDisposition disposition = NSURLSessionAuthChallengePerformDefaultHandling;
        __autoreleasing NSURLCredential *credential =nil;
        
        if ([challenge.protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust]) {
            RLog(@"验证服务器1");
            if ([weakManager.securityPolicy evaluateServerTrust:challenge.protectionSpace.serverTrust forDomain:challenge.protectionSpace.host]) {
                RLog(@"验证服务器2");
                
                credential = [NSURLCredential credentialForTrust:challenge.protectionSpace.serverTrust];
                if (credential) {
                    RLog(@"验证服务器3");
                    disposition = NSURLSessionAuthChallengeUseCredential;
                } else {
                    RLog(@"验证服务器4");
                    
                    disposition = NSURLSessionAuthChallengePerformDefaultHandling;
                }
            } else {
                RLog(@"验证服务器5");
                
                disposition = NSURLSessionAuthChallengeCancelAuthenticationChallenge;
            }
        } else {
            RLog(@"验证客户端1");
            
            // client authentication
            SecIdentityRef identity = NULL;
            SecTrustRef trust = NULL;
            NSString *p12 = [[NSBundle mainBundle] pathForResource:@"client"ofType:@"p12"];
            NSFileManager *fileManager = [NSFileManager defaultManager];
            
            if (![fileManager fileExistsAtPath:p12]) {
                NSLog(@"client.p12:not exist");
            } else {
                RLog(@"验证客户端2");
                
                NSData *PKCS12Data = [NSData dataWithContentsOfFile:p12];
                
                if ([[weakSelf class] extractIdentity:&identity andTrust:&trust fromPKCS12Data:PKCS12Data])
                {
                    RLog(@"验证客户端3");
                    
                    SecCertificateRef certificate = NULL;
                    SecIdentityCopyCertificate(identity, &certificate);
                    const void*certs[] = {certificate};
                    CFArrayRef certArray =CFArrayCreate(kCFAllocatorDefault, certs,1,NULL);
                    credential = [NSURLCredential credentialWithIdentity:identity certificates:(__bridge  NSArray *)certArray persistence:NSURLCredentialPersistencePermanent];
                    disposition = NSURLSessionAuthChallengeUseCredential;
                }
                
            }
        }
        *_credential = credential;
        return disposition;
    }];
}

/**
 *  配置https验证策略
 */
+ (void)securityPolicyForHTTPSessionManager:(AFHTTPSessionManager *)manager
{
    
    // 安全策略，配置https请求
//    AFSecurityPolicy * securityPolicy = [AFSecurityPolicy defaultPolicy];
    
    AFSecurityPolicy * securityPolicy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModeCertificate];
    
    //allowInvalidCertificates 是否允许无效证书（也就是自建的证书），默认为NO
    //如果是需要验证自建证书，需要设置为YES
    securityPolicy.allowInvalidCertificates = YES;
    
    //validatesDomainName 是否需要验证域名，默认为YES；
    //假如证书的域名与你请求的域名不一致，需把该项设置为NO；如设成NO的话，即服务器使用其他可信任机构颁发的证书，也可以建立连接，这个非常危险，建议打开。
    //置为NO，主要用于这种情况：客户端请求的是子域名，而证书上的是另外一个域名。因为SSL证书上的域名是独立的，假如证书上注册的域名是www.google.com，那么mail.google.com是无法验证通过的；当然，有钱可以注册通配符的域名*.google.com，但这个还是比较贵的。
    //如置为NO，建议自己添加对应域名的校验逻辑。
    securityPolicy.validatesDomainName = NO;
    
    manager.securityPolicy = securityPolicy;
    
    // 先导入证书
    NSString *cerPath = [[NSBundle mainBundle] pathForResource:@"root" ofType:@"cer"];//证书的路径
    
    NSData *certData = [NSData dataWithContentsOfFile:cerPath];
    securityPolicy.pinnedCertificates = [[NSSet alloc] initWithArray:@[certData]];
}

+ (BOOL)extractIdentity:(SecIdentityRef *)outIdentity andTrust:(SecTrustRef *)outTrust fromPKCS12Data:(NSData *)inPKCS12Data {
    OSStatus securityError = errSecSuccess;
    // client certificate password
    NSDictionary *optionsDictionary = [NSDictionary dictionaryWithObject:@"p12密码" forKey:(__bridge id)kSecImportExportPassphrase];
    
    CFArrayRef items = CFArrayCreate(NULL, 0, 0, NULL);
    securityError = SecPKCS12Import((__bridge CFDataRef)inPKCS12Data, (__bridge CFDictionaryRef)optionsDictionary, &items);
    
    if (securityError == 0) {
        CFDictionaryRef myIdentityAndTrust = CFArrayGetValueAtIndex(items,0);
        const void *tempIdentity = NULL;
        tempIdentity = CFDictionaryGetValue(myIdentityAndTrust, kSecImportItemIdentity);
        *outIdentity = (SecIdentityRef)tempIdentity;
        const void *tempTrust = NULL;
        tempTrust = CFDictionaryGetValue(myIdentityAndTrust, kSecImportItemTrust);
        *outTrust = (SecTrustRef)tempTrust;
    } else {
        NSLog(@"Failedwith error code %d", (int)securityError);
        return NO;
    }
    return YES;
}
```

