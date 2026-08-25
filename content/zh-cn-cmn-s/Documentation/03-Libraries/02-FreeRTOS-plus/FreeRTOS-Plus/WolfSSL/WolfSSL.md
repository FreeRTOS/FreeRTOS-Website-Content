---
title: WolfSSL
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


嵌入式系统具有目前最先进的网络安全性能

**-  [立即在 FreeRTOS Windows 模拟器中进行评估](FreeRTOS_WolfSSL_Example) -**

**技术亮点**

* 比 OpenSSL 小 20 倍
* 只需要 20-100KB 的闪存
* 只需要 1-36KB 的 RAM
* 支持 TLS 1、1.1 和 1.2（客户端和服务器）
* 支持 DTLS 1 和 1.2（客户端和服务器）
* 哈希函数：MD2、MD4、MD5、SHA-1、SHA-2、SHA-256、SHA-384、SHA-512、BLAKE2b 和 RIPEMD-160
* 块、流和 AEAD 密码：AES (CBC/CTR/GCM/CCM)、Camellia、DES、3DES、ARC4、RABBIT、HC-128 密码
* 公钥选项：RSA、DSS、DH、EDH、NTRU
* 私钥加密：PKCS #8、#5、#12
* 支持 PEM 和 DER 证书
* 密钥生成和 ECC 支持
* 证书生成
* FreeRTOS 移植层
* OpenSSL 兼容层


## 简介

WolfSSL 是一款轻量级的 TLS/SSL 库，可提升**安全性**、**身份验证便捷性**、**完整性**
和**保密性**，适用于网络通信。

WolfSSL 比 yaSSL 小 10 倍左右，
在某些构建配置下甚至比 OpenSSL 小 20 倍。根据用户反馈，
在标准 SSL 操作中，
WolfSSL 的性能明显比 OpenSSL 更加优越。

WolfSSL 的体积小、速度快、功能多，非常适合
与 FreeRTOS 一起使用，但 WolfSSL 不会牺牲任何功能。WolfSSL
支持最新的行业标准，
比如[传输层安全](http://en.wikipedia.org/wiki/Transport_Layer_Security)
(TLS) 协议 1.2 版本，以及渐进流、块和 AEAD 密码，
比如 [AES-GCM](http://en.wikipedia.org/wiki/Galois/Counter_Mode)、[RABBIT](http://www.ecrypt.eu.org/stream/rabbitpf.html)
和 [NTRU](http://en.wikipedia.org/wiki/NTRU)。


## FreeRTOS 集成示例

WolfSSL 已移植到 FreeRTOS，我们提供了相应的[示例项目](FreeRTOS_WolfSSL_Example)。
该示例在 FreeRTOS Windows 模拟器中运行，
允许用户在标准 Windows 计算机上评估 WolfSSL 在 FreeRTOS 环境中的表现，
而无需依赖外部目标硬件。


## 应用程序集成

WolfSSL 以一组 ANSI 标准 C 源文件的形式提供，
这些文件可以添加到任何 C 语言项目中，
并使用任何兼容 ANSI 的 C 语言编译器进行构建。关于使用交叉编译器构建 WolfSSL 的说明，
请参阅用户手册。

WolfSSL 提供简单的 API，
可以轻松集成到现有应用程序中，也适用于新应用程序。
本网站上的[简单 WolfSSL 客户端使用示例](Using-SSL-TLS-in-a-client-site-application)
和[简单 WolfSSL 服务器端使用示例](Using-SSL-TLS-in-a-server-site-application)
页面演示了基本集成的操作步骤，
[此处提供的 FreeRTOS 模拟器示例项目](FreeRTOS_WolfSSL_Example)
可作为参考。
用户手册中包含了完整的配置和 API 引用信息。
