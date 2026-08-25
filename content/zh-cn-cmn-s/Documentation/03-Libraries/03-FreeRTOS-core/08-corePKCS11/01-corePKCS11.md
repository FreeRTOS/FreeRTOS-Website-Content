---
title: corePKCS11
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: corePKCS11 库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
external Links:
- title: corePKCS11 API 引用
  link: https://freertos.github.io/corePKCS11/v3.5.0/
---


## 简介

corePKCS11 是基于软件的 PKCS #11 应用程序编程接口 (API) 子集的模拟实现 
。在生产设备转向特定安全硬件实现之前， 
该系统可实现独立于硬件的快速原型设计和开发。

[PKCS #11](https://en.wikipedia.org/wiki/PKCS_11) 是一种标准化且广泛使用的 API， 
用于操作常见的加密对象。它之所以重要， 
是因为它所规定的函数允许应用程序软件使用、创建、修改和删除加密对象， 
而无需将这些对象暴露在应用程序的内存中。例如，FreeRTOS AWS 参考集成使用 PKCS #11 API 的**一个小型子集**， 
除其他外，可访问创建网络连接所需的密钥（私钥）， 
该网络连接由[传输层安全](https://en.wikipedia.org/wiki/Transport_Layer_Security) 
（TLS）协议进行验证和保护，应用程序永远不会“看到”密钥。由 
[OASIS PKCS#11 技术委员会](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=pkcs11) 负责对 PKCS #11 进行维护。

一般来说，安全加密处理器（如可信平台模块（TPM）、硬件安全 
模块（HSM）、安全元件或任何其他类型的安全硬件 Enclave）的供应商 
都会随硬件一起发布 PKCS #11 实现。因此，只模拟 corePKCS11 软件的目的是 
提供一个独立于硬件的 PKCS #11 实现，供开发使用， 
然后再在生产设备中切换到特定于安全硬件的实现。

由于 PKCS #11 接口已被定义为 
[PKCS #11 规范](https://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)的一部分， 
因此用另一种实现方法替换该库时， 
由于接口不会发生变化，因此只需很少的移植工作。可以用与 corePKCS #11 一起发布的系统测试 
来验证硬件特定的 PKCS #11 实现与 corePKCS11 的行为相同。


**corePKCS11 代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| core_pkcs11.c | 0.8 K | 0.8K |
| core_pki_utils.c | 0.5K | 0.3K |
| core_pkcs11_mbedtls.c | 8.9K | 7.5K |
| 总估算 | 10.2K | 8.6K |

