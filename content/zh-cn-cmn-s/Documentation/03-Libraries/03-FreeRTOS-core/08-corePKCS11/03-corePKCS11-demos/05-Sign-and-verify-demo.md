---
title: corePKCS11 签名与验证演示
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


## 引言

本演示为 corePKCS11 演示系列中的第四个。它介绍了 PKCS #11 API 中
用于签署消息并验证消息签名的部分。PKCS #11 标准参见
[此处](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)。

corePKCS11 演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
无需任何特定 MCU 硬件。

本演示中介绍的函数集分类如下：

* 对象管理函数
* 签名和 MAC 函数


### 源代码组织

基于 PKCS #11 的双向验证的 Visual Studio 解决方案演示名为 `pkcs11\_demos.sln`，
位于 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` 目录中
（此为 FreeRTOS 主下载文件的目录）。

[\![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*点击放大*


## 配置演示项目

要配置演示项目，请在 `pkcs11_demo_config.h` 中将 `configPKCS11_SIGN_AND_VERIFY_DEMO` 设置为 1。
此为默认启用项。完成上述操作后，即可运行演示。此演示无需其他配置
。


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。

1. 在 Visual Studio IDE 中，打开 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\pkcs11\_demos.sln`
   Visual Studio 解决方案文件。
2. 在 IDE 的 '**build**'（构建）菜单中选择 '**build solution**' （构建解决方案）。


## 功能

此演示的入口点为 `vPKCS11SignVerifyDemo`。请注意，此演示需要
对象演示中的 `prvObjectGeneration` 函数创建的公钥和私钥对。

此演示将使用此密钥签署消息摘要。（关于如何创建摘要，请参阅"机制与摘要"演示。）
另外，此演示还介绍了一些有用的函数，可以在 “core_pkcs11.h” 头文件中找到。
这些函数可用于精简之前的演示中呈现的一些功能。

第一步是查找对象演示中生成的私钥和公钥的对象句柄。


### 找到合适的对象句柄

```c
/* This function will:
 * Find an object, given it's label.
 *
 * This is done using the FindObjects group of functions defined as
 * "Object Management Functions" in PKCS #11.
 *
 * This will acquire the object handle for the private key created in the
 * "objects.c" demo.
 */

xResult = xFindObjectWithLabelAndClass( hSession,
                                        pkcs11configLABEL_DEVICE_PRIVATE_KEY_FOR_TLS,
                                        CKO_PRIVATE_KEY,
                                        &xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );
configASSERT( xPrivateKeyHandle != CK_INVALID_HANDLE );

/* Acquire the object handle for the public key created in the "objects.c"
 * demo. */
xResult = xFindObjectWithLabelAndClass( hSession,
                                        pkcs11configLABEL_DEVICE_PUBLIC_KEY_FOR_TLS,
                                        CKO_PRIVATE_KEY,
                                        &xPublicKeyHandle );
configASSERT( xResult == CKR_OK );
configASSERT( xPublicKeyHandle != CK_INVALID_HANDLE );

```
找到对象句柄后，可以用其签署消息摘要，并验证签名
。应始终保护私钥，因为私钥可以用于签署消息，
使收件人能够验证私钥的持有者是否真的是撰写消息的人。任何
拥有由私钥生成的公钥并用其验证消息的人都必须能够
假定实际上这是来自已知发件人的有效消息。


### 创建签名

```c
/* Initializes the sign operation and sets what mechanism will be used
 * for signing the message digest. Specify what object handle to use for this
 * operation, in this case the private key object handle.
 */

xResult = pxFunctionList->C_SignInit( hSession,
                                      &xMechanism,
                                      xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );

/* Sign the message digest that was created with the C_Digest series of
 * functions. A signature will be created using the private key specified in
 * C_SignInit and put in the byte buffer xSignature. */

xResult = pxFunctionList->C_Sign( hSession,
                                  xDigestResult,
                                  pkcs11SHA256_DIGEST_LENGTH,
                                  xSignature,
                                  &xSignatureLength );
configASSERT( xResult == CKR_OK );
configASSERT( xSignatureLength == pkcs11ECDSA_P256_SIGNATURE_LENGTH );

```

下一步是使用公钥来确保 PKCS # 11 堆栈可以确认我们收到的消息来自发件人
。（公钥派生自用于创建
消息签名的私钥。）为完成此操作，可以使用 PKCS # 11 堆栈来验证包含签名的缓冲区
。


### 验证签名

```c
/* Verify the signature created by C_Sign. First we will verify that the
 * same Cryptoki library was able to trust itself.
 *
 * C_VerifyInit will begin the verify operation, by specifying what mechanism
 * to use (CKM_ECDSA, the same as the sign operation) and then specifying
 * which public key handle to use.
 */

xResult = pxFunctionList->C_VerifyInit( hSession,
                                        &xMechanism,
                                        xPublicKeyHandle );

configASSERT( xResult == CKR_OK );

/* Given the signature and it's length, the Cryptoki will use the public key
 * to see if the sender can be trusted. If C_Verify returns CKR_OK, it means
 * that the sender of the message has the same private key as the private key
 * that was used to generate the public key, and we can trust that the
 * message we received was from that sender.
 *
 * Note that we are not using the actual message, but the digest that we
 * created earlier of the message, for the verification.
 */

xResult = pxFunctionList->C_Verify( hSession,
                                    xDigestResult,
                                    pkcs11SHA256_DIGEST_LENGTH,
                                    xSignature,
                                    xSignatureLength );

if( xResult == CKR_OK )
{
    configPRINTF( ( "The signature of the digest was verified with the" \
                    " public key and can be trusted.\r\n" ) );
} else
{
    configPRINTF( ( "Unable to verify the signature with the given public" \
                    " key, the message cannot be trusted.\r\n" ) );
}

```


### 如何验证终端中的签名

演示将输出签名缓冲区的内容以及可用于验证签名的十六进制格式的公钥
。

![](/media/2020/pkcs11_sign_verify_demo-300x224.png)


### 提取公钥

可按照以下步骤，从含有公钥的二进制文件中导出公钥。

1. 将公钥以十六进制字节形式导出并打印。演示会将
   十六进制字节打印到控制台。

2. 创建名为 "`DevicePublicKeyAsciiHex.txt`" 的空白文本文件。

3. 将公钥的十六进制值复制并粘贴到此文本文件中。

4. 使用 xxd 工具将十六进制文件转换为二进制文件：

   ```c
   $ xxd -r -ps DevicePublicKeyAsciiHex.txt DevicePublicKeyDer.bin
   ```

   xxd 将抓取一个包含十六进制数据的文本文件，并在其中输出其对应的二进制文件。请参阅 “`$ man xxd`”，
   了解关于 xxd 的更多信息。

5. 将公钥的二进制编码转换为 PEM 格式：

   ```c
   $ openssl ec -inform der -in DevicePublicKeyDer.bin -pubin -pubout -outform pem -out public_key.pem
   ```

   我们现在已经提取了公钥，可以使用它来验证由 PKCS # 11 堆栈生成的签名。


### 提取签名

1. 创建名为 "`signature.txt`" 的空白文本文件。

2. 复制粘贴由演示写入控制台的签名缓冲区。

3. 将签名转换为二进制格式。

   ```c
   $ xxd -r -ps signature.txt signature.bin
   ```

**警告：运行对象生成演示将创建一个新的密钥对，导致需要重复上述步骤！**


#### 使用 OpenSSL 验证签名

OpenSSL 可用于验证签名是否可信，以及 PKCS # 11 堆栈的工作行为是否符合预期
。OpenSSL 是一套广泛使用的加密组件，可提供许多实用功能。下面的命令
使用提取的公钥来验证由 PKCS # 11 堆栈创建的二进制签名。

```c
$ openssl dgst -sha256 -verify public_key.pem -signature signature.bin msg.txt
```
