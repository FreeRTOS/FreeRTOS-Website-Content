---
title: corePKCS11 对象演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

* 本页内容：
	+ [源代码组织](#源代码组织)
	+ [配置演示](#配置演示项目)
	+ [构建演示](#构建演示项目)
	+ [功能](#功能)


## 引言

本演示是 corePKCS11 演示系列中的第三个。它介绍了 PKCS #11 API 中
用于管理对象的部分。对象定义为“存储在令牌上的项。可以是数据、
证书或密钥”。该演示概述了如何使用 PKCS #11 来提取一些
常用的对象。该界面特别有用，因为它不仅可移植，使用起来也很灵活。
使用 PKCS #11 来操作这些对象有利于提高安全性，
因为它将攻击对象的范围缩小到专门用于加密操作和保护对象的模块。

**注意：**此演示将向 Windows 文件系统写入 (EC) 公钥和私钥。这两个密钥
 都包含在名为 "`FreeRTOS_P11_Key.dat`" 的二进制格式文件中。签名和验证演示直接依赖于此文件，
 没有它将无法运行。

可在[此处](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)查阅 PKCS #11 标准。

该 corePKCS11 演示项目使用 [FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
无需任何特定 MCU 硬件。

本演示中介绍的函数集分类如下：

* 对象管理函数


## 源代码组织

基于 PKCS #11 的双向验证的 Visual Studio 解决方案演示名为 `pkcs11\_demo.sln`，
位于 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11\_Windows\_Simulator\` 目录
在主 FreeRTOS 下载中。

[\![](/media/2020/PKCS11-Source-Code-Organization.png)](/media/2020/PKCS11-Source-Code-Organization.png)
*点击放大*


## 配置演示项目

要配置演示项目，请在 `pkcs11\_demo\_config.h` 中将 `configPKCS11\_OBJECT\_DEMO` 设置为 1。此
为默认启用项。完成上述操作后，即可运行演示，
此演示不需要其他配置步骤。


## 构建演示项目

此演示项目使用的是  [Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)。

1. 从 Visual Studio IDE 中打开 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\pkcs11_demo.sln` Visual Studio
   解决方案文件。
2. 从 IDE 的 '`build`' 菜单中选择 '`build solution`'。


## 功能

启用后，此演示的入口点为 `vPKCS11ObjectDemo`。目前，该演示分为两个
更小的演示：`prvObjectImporting` 展示了如何将对象导入PKCS # 11模块，
`prvObjectGeneration` 展示了如何在 PKCS#11 模块中生成对象。

直接在 IoT 设备上生成凭据更安全，因为如此一来凭据不会
暴露于任何外部系统中。如果 IoT 设备具有安全元件，则安全性更高。安全
元件是保护私钥等敏感数据的专用芯片。它们可提供额外保护，
针对可能尝试提取 IoT 设备私钥的攻击者。仅仅将私钥
存储在闪存中并不安全。

此演示展示如何将证书导入到 PKCS #11 堆栈中。这很有用，
因为它允许您存储应用程序希望信任的任何服务器的证书。模板是描述对象的 CK_ATTRIBUTE 数组
。


### 创建 X.509 证书模板：

```c
/* The PKCS11_CertificateTemplate_t is a custom struct defined in "iot_pkcs11.h"
 * in order to make it easier to import a certificate. This struct will be
 * populated with the parameters necessary to import the certificate into the
 * Cryptoki library.
 */
PKCS11_CertificateTemplate_t xCertificateTemplate;

/* The object class is specified as a certificate to help the Cryptoki library
 * parse the arguments.
 */
CK_OBJECT_CLASS xCertificateClass = CKO_CERTIFICATE;

/* The certificate type is x509, which is the only type
 * supported by this stack. To read more about x509 certificates, use
 * the following links:
 *
 * https://en.wikipedia.org/wiki/X.509
 * https://www.ssl.com/faqs/what-is-an-x-509-certificate/
 *
 */
CK_CERTIFICATE_TYPE xCertificateType = CKC_X_509;

/* The label will help the application identify which object it wants
 * to access.
 */
CK_BYTE pucLabel[] = pkcs11configLABEL_DEVICE_CERTIFICATE_FOR_TLS;

/* Specify certificate class. */
xCertificateTemplate.xObjectClass.type = CKA_CLASS;
xCertificateTemplate.xObjectClass.pValue = &xCertificateClass;
xCertificateTemplate.xObjectClass.ulValueLen = sizeof( xCertificateClass );

/* Specify certificate subject. */
xCertificateTemplate.xSubject.type = CKA_SUBJECT;
xCertificateTemplate.xSubject.pValue = xSubject;
xCertificateTemplate.xSubject.ulValueLen = strlen( ( const char * ) xSubject );

/* Point to contents of certificate. */
xCertificateTemplate.xValue.type = CKA_VALUE;
xCertificateTemplate.xValue.pValue = ( CK_VOID_PTR ) pkcs11demo_RSA_CERTIFICATE;
xCertificateTemplate.xValue.ulValueLen = ( CK_ULONG ) sizeof( pkcs11demo_RSA_CERTIFICATE );

/* Specify certificate label. */
xCertificateTemplate.xLabel.type = CKA_LABEL;
xCertificateTemplate.xLabel.pValue = ( CK_VOID_PTR ) pucLabel;
xCertificateTemplate.xLabel.ulValueLen = strlen( ( const char * ) pucLabel );

/* Specify certificate type as x509. */
xCertificateTemplate.xCertificateType.type = CKA_CERTIFICATE_TYPE;
xCertificateTemplate.xCertificateType.pValue = &xCertificateType;
xCertificateTemplate.xCertificateType.ulValueLen = sizeof( CK_CERTIFICATE_TYPE );

/* Specify that the certificate should be on a token. */
xCertificateTemplate.xTokenObject.type = CKA_TOKEN;
xCertificateTemplate.xTokenObject.pValue = &xTokenStorage;
xCertificateTemplate.xTokenObject.ulValueLen = sizeof( xTokenStorage );

```

模板创建后，可以将其与数组中的条目数一起传递给 `C_CreateObject`
。如果能够创建 x509 证书，则 PKCS#11 模块将解析参数并返回 `CKR_OK`
。这是将已知证书导入 PKCS #11 模块的好方法。


### 创建 X.509 证书:

```c
/* Once the Cryptoki library has finished importing the new certificate
 * a CK_OBJECT_HANDLE is associated with it. The application can now use this
 * to refer to the object in following operations.
 *
 * xCertHandle in the below example will have it's value modified to
 * be the CK_OBJECT_HANDLE.
 *
 * To compare the hard coded x509, in PEM format, with the DER formatted
 * x509 certificate that is created by the Cryptoki library, use the following
 * OpenSSL command:
 * "$ openssl x509 -in FreeRTOS_P11_Certificate.dat -inform der -text"
 *
 * See this explanation for the difference between the PEM format and the
 * DER format:
 * <https://stackoverflow.com/questions/22743415/what-are-the-differences-between-pem-cer-and-der/22743616>
 *
 */
xResult = pxFunctionList->C_CreateObject( hSession,
                                          ( CK_ATTRIBUTE_PTR ) &xCertificateTemplate,
                                          sizeof( xCertificateTemplate ) / sizeof( CK_ATTRIBUTE ),
                                          &xCertHandle );

configASSERT( xResult == CKR_OK );
configASSERT( xCertHandle != CK_INVALID_HANDLE );

```

演示的后半部分介绍如何使用 PKCS #11 生成密钥对。这种方法更可取，
因为应用程序永远不会暴露于包含私钥的内存。这减少了
攻击者提取私钥的潜在途径，
因为私钥实际上从未存储在 PKCS #11 模块之外。

在以下代码中，同样使用模板来生成密钥。


### 创建密钥对生成模板：

```c
/* CK_ATTTRIBUTE's contain an attribute type, a value, and the length of
 * the value. An array of CK_ATTRIBUTEs is called a template. They are used
 * to create, search for, and manipulate objects. The order of the
 * template does not matter.
 *
 * In the below template we create a public key:
 * Specify the key type as EC.
 * The key will be able to verify a message.
 * Specify the EC Curve.
 * Assign a label to the object that will be created.
 */
CK_ATTRIBUTE xPublicKeyTemplate[] =
{
    { CKA_KEY_TYPE, &xKeyType, sizeof( xKeyType ) },
    { CKA_VERIFY, &xTrue, sizeof( xTrue ) },
    { CKA_EC_PARAMS, xEcParams, sizeof( xEcParams ) },
    { CKA_LABEL, pucPublicKeyLabel, sizeof( pucPublicKeyLabel ) - 1 }
};

/* In the below template we create a private key:
 * The key type is EC.
 * The key is a token object.
 * The key will be a private key.
 * The key will be able to sign messages.
 * Assign a label to the object that will be created.
 */
CK_ATTRIBUTE xPrivateKeyTemplate[] =
{
    { CKA_KEY_TYPE, &xKeyType, sizeof( xKeyType ) },
    { CKA_TOKEN, &xTrue, sizeof( xTrue ) },
    { CKA_PRIVATE, &xTrue, sizeof( xTrue ) },
    { CKA_SIGN, &xTrue, sizeof( xTrue ) },
    { CKA_LABEL, pucPrivateKeyLabel, sizeof( pucPrivateKeyLabel ) - 1 }
};

```

最后，创建此模板，此模板传递给 `C_GenerateKeyPair` 时，
PKCS #11 模块会创建一个新的密钥对。


### 创建密钥对：

```c
/* This function will generate a new EC private and public key pair. You can
 * use " $openssl ec -inform der -in FreeRTOS_P11_Key.dat -text " to see
 * the structure of the keys that were generated.
 */
xResult = pxFunctionList->C_GenerateKeyPair( hSession,
                                             &xMechanism,
                                             xPublicKeyTemplate,
                                             sizeof( xPublicKeyTemplate ) / sizeof( CK_ATTRIBUTE ),
                                             xPrivateKeyTemplate,
                                             sizeof( xPrivateKeyTemplate ) / sizeof( CK_ATTRIBUTE ),
                                             &xPublicKeyHandle,
                                             &xPrivateKeyHandle );
configASSERT( xResult == CKR_OK );

```
