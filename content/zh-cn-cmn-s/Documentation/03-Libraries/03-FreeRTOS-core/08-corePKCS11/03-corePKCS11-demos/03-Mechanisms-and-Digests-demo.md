---
title: corePKCS11 机制和摘要演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

* 本页内容：
	+ [源代码组织](#源代码组织)
	+ [配置演示项目](#配置演示项目)
	+ [构建演示项目](#构建演示项目)
	+ [功能](#功能)

		- [查询摘要能力](#查询摘要能力)
		- [创建摘要](#创建摘要)
		- [使用 OpenSSL](#使用-openssl)
		- [使用 Python3 shell](#使用-python3-shell)


## 简介

本演示是 corePKCS11 演示系列中的第二个。它介绍了 PKCS #11 API 中 
用于查询 PKCS #11 插槽的能力和使用该插槽创建消息摘要的部分。请点击 
[此处](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)查阅 PKCS #11 标准。 
插槽是一个可以放置令牌的接口。令牌是一种专门用于加密操作（如保存密钥、生成密钥） 
以及为普通操作（如创建 SHA 摘要）提供硬件加速 
的硬件设备。

corePKCS11 演示项目使用  
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以在 Windows 上使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。

本演示中介绍的函数集分类如下：

* 插槽和令牌管理函数
* 消息摘要函数


### 源代码组织

基于 corePKCS11 的相互身份验证演示的 Visual Studio 解决方案称为 `pkcs11\_demo.sln`， 
可在 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` 目录中找到 
（详见 FreeRTOS 主下载内容）。

[\![](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)   
*点击放大* 


## 配置演示项目

要配置演示项目，请在 `pkcs11\_demo\_config.h` 中将 `configPKCS11\_MECHANISMS\_AND\_DIGESTS\_DEMO` 设置为 1。


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。

1. 从 Visual Studio IDE 中打开 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\pkcs11\_demos.sln` Visual Studio 
   解决方案文件。

2. 在 IDE 的 'build'（构建）菜单中选择 'build solution' （构建解决方案）。


## 功能

启用后，此演示的入口点为 `vPKCS11MechanismsAndDigestDemo`。此演示的目的是查询一个插槽的能力， 
然后用这个插槽来生成一份摘要。在运行时 
查询令牌的能力，可以让令牌在插槽内交换时更加灵活 
。大部分时间，令牌将保留在插槽中，但如果它被移除， 
那么能力将有可能改变。对于该演示，使用 SHA-256 算法来创建摘要。


### 查询摘要能力：

```c
/* The PKCS #11 standard defines a mechanism to be a "A process for  
 * implementing a cryptographic operation." For example, the SHA-256 algorithm  
 * will be the mechanism used in this demo to perform a digest (hash operation).  
 *  
 * The mechanism types are defined in "pkcs11t.h", and are prefixed CKM_, to  
 * provide a portable way to identify mechanisms.  
 */  
CK_MECHANISM_TYPE xMechanismType = 0;  
  
/* The CK_MECHANISM_INFO allows the application to retrieve the minimum and  
 * maximum key sizes supported by the mechanism (could be in bits or bytes).  
 * The structure also has a flags field that is populated with bit flags  
 * for what features the mechanism supports.  
 */  
CK_MECHANISM_INFO MechanismInfo = { 0 };  
  
xResult = pxFunctionList->C_GetMechanismInfo( pxSlotId[ 0 ],  
                                              CKM_SHA256,  
                                              MechanismInfo );  
configASSERT( CKR_OK == xResult );  
  
if( 0 != ( CKF_DIGEST & MechanismInfo.flags ) )  
{  
    configPRINTF( ( "The Cryptoki library supports the " \  
    "SHA-256 algorithm.\r\n" ) );  
}  
else  
{  
    configPRINTF( ( "The Cryptoki library doesn't support the " \  
    "SHA-256 algorithm.\r\n" ) );  
}  

```

创建散列是一个非常常见的操作，有许多用途。例如，Git 使用散列来唯一地识别 
提交。另一个例子是 Python 字典，它使用每个关键值的散列来实现更快的查找 
。加密操作使用散列来验证消息或通信的完整性。 
通常，加密操作与签名结合，以核实消息的完整性和消息发送人 
的身份。签名将在签名和验证演示页面中介绍。

虽然摘要操作不需要任何特定的硬件，但它们仍然包括在 PKCS #11 中， 
以允许为所有加密操作创建一个独立的、功能齐全的模块。这有助于缩小 
漏洞范围，并使应用程序的测试更加容易。由于散列 
常用于加密操作（如 TLS 握手），因此散列算法 
中的漏洞可能导致机密泄露和数据丢失。为了避免出现这种情况，PKCS #11允许 
您在自己的模块中实现加密操作所需的全部功能。这允许您创建一个 
安全属性可以独立验证的独立安全模块。同时还允许 
应用程序保护敏感数据。

用 PKCS #11 生成摘要的过程可分成三个步骤。首先，将创建摘要的机制 
与 `C\_DigestInit()` 一起传递给 PKCS #11。然后，包含信息的缓冲区 
及其长度与 `C\_DigestUpdate()` 一起传递。最后，通过调用 
`C\_DigestFinal()` 创建散列并将其放入缓冲区。


### 创建摘要：

```c
/* Hash with SHA256 mechanism. */  
xDigestMechanism.mechanism = CKM_SHA256;  
  
/* Initializes the digest operation and sets what mechanism will be used  
* for the digest. */  
xResult = pxFunctionList->C_DigestInit( hSession,  
                                        xDigestMechanism );  
configASSERT( CKR_OK == xResult );  
  
/* Pass a pointer to the buffer of bytes to be hashed, and its size. */  
xResult = pxFunctionList->C_DigestUpdate( hSession,  
                                          pxKownMessage,  
                                          sizeof( pxKownMessage ) - 1 );  
configASSERT( CKR_OK == xResult );  
  
/* Retrieve the digest buffer. Since the mechanism is an SHA-256 algorithm,  
* the size will always be 32 bytes. If the size cannot be known ahead of time,  
* a NULL value to the second parameter xDigestResult, will set the third parameter,  
* pulDigestLen to the number of required bytes. */  
xResult = pxFunctionList->C_DigestFinal( hSession,  
                                         xDigestResult,  
                                         ulDigestLength );  
configASSERT( CKR_OK == xResult );  
  
```

一个有趣的练习是比较由 PKCS #11 操作生成的散列与由 
不同工具的 SHA-256 实现生成的散列。大多数 Linux 发行版、MacOS 和 Windows 
都支持 OpenSSL。请参阅 OpenSSL 说明，以便在您的平台上安装。 

通常，因为 OpenSSL 常用于建立 TLS 连接，所以大多数设备上都安装了 OpenSSL。 
另外，hashlib 模块是 Python3 标准库的一部分， 
因此可在支持 Python3 的设备上跨平台使用。


### 使用 OpenSSL：

```c
#The "n" flag is set to strip new line characters.  
$ echo -n "Hello world\ | openssl dgst -sha256  

```


### 使用 Python3 shell：

```c
>>> import hashlib  
>>> hashlib.sha256("Hello world!".encode("utf8")).hexdigest()  

```
两者的输出以及演示的输出应为： 
"c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a"。生成散列值后， 
就可以对它们进行比较，以验证信息确实是 “Hello world!”。

