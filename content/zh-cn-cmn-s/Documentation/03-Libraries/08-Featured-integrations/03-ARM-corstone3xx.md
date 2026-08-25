---
title: "精选 FreeRTOS IoT 集成 "
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


#### 针对基于 Arm Cortex-M MCU 的 Arm Corstone-3xx 平台

*您可以利用此精选参考集成灵活调整其功能，同时利用您的硬件功能。
或者，为了简单起见，也可以考虑 
[ExpressLink 精选集成](06-STM32-Expresslink)。*


## 引言

此参考集成演示了
如何通过集成模块化 FreeRTOS [内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)和
[库](/Documentation/03-Libraries/01-Library-overview/Library-categories)并利用基于
[Arm TrustZone (Armv8-M)](https://www.arm.com/architecture/learn-the-architecture/m-profile) 的硬件强制安全性来开发云连接应用程序并对其进行安全更新。


为了利用硬件强制安全性，此集成使用 PSA 认证参考实现
[Trusted Firmware-M](https://www.trustedfirmware.org/projects/tf-m/)。Trusted Firmware-M 提供各种安全服务，
例如安全启动、加密、安全存储、认证和更新服务，符合
[PSA 认证要求](https://www.psacertified.org/blog/psa-certified-10-security-goals-explained/)。该集成
基于 [Corstone-300](https://developer.arm.com/Processors/Corstone-300) 平台。


开发人员和合作伙伴可以利用此集成作为起点，构建 FreeRTOS 内核
和基于库的软件堆栈，而这一切离不开基于 Arm Cortex-M 的平台。所有组件
都以模块化方式组合在一起，以便轻松跨平台移植此集成。

[\![](/media/2022/example-integration-corstone3xx.png) Corstone-300](https://developer.arm.com/Processors/Corstone-300)


## 安全功能和函数演示

Trusted Firmware-M (TF-M) 利用 Arm TrustZone 技术提供
相互隔离的非安全处理环境 (NSPE) 和安全处理环境 (SPE)。FreeRTOS 内核、
中间件和应用程序在 NSPE 中运行，而 TF-M 在 SPE 中运行。TF-M 通过 PSA 认证功能 API
向 NSPE 提供 PSA RoT 安全服务。这种隔离可确保 TF-M 代码、资产（密钥、证书等）
和数据免受 NSPE 中的漏洞的影响。


该演示展示了如何利用 TF-M 的 PSA 加密和安全存储功能在 Corstone-300 和 AWS IoT Core 之间
建立安全 TLS 连接。此外，它还演示了如何使用 TF-M 固件更新服务对平台进行安全 OTA 更新
。


### 安全 TLS 连接

Corstone-300 通过安全 TLS 连接与 AWS IoT Core 进行通信。NSPE 中运行的 Mbed TLS 用于
建立 TLS 连接。Mbed TLS 利用 TF-M 提供的 PSA Crypto API 来执行加密操作，
利用 [PKCS # 11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) API
执行 TLS 客户端身份验证并将 TLS 客户端证书和私钥导入设备。


PKCS#11 已通过薄适配层与 TF-M 集成。在该集成中，PKCS#11 API 通过该适配层调用相应的
PSA Secure Storage API 或 Cryptographic API。这可确保密钥和证书受到保护，
加密操作在 TF-M 的 SPE 中安全地执行，
并与非安全处理环境中的内核、库和应用程序隔离。密钥和证书会被安全存储。
这是通过 TF-M 的内部可信存储 (ITS) 和受保护存储 (PS) 服务实现的。TLS 客户端身份验证期间的签名
由 TF-M 的加密服务执行。


### 安全 OTA 更新


FreeRTOS OTA 代理可为平台提供 OTA PAL 层来集成并启用 OTA 更新。该演示集成了
OTA PAL 实现，该实现利用在 TF-M 中实现的 PSA 认证固件更新 API。这
允许 Corstone-300 从 AWS IoT Core 接收新映像，使用 TF-M 对其进行身份验证，
然后再将其部署为活动映像。安全 (TF-M) 和非安全（FreeRTOS 内核和应用程序）映像可以
分开更新。


每次启动设备时，MCUBoot（引导加载程序）都会在启动映像之前验证
映像签名是否有效。由于安全 (TF-M) 和非安全（FreeRTOS 内核和应用程序）映像是分开签名的，
MCUBoot 在启动之前会验证两个映像签名是否有效。如果任一映像签名验证失败，
MCUBoot 将停止启动过程。


### 内存安全证明

“核心”FreeRTOS 库符合记录的代码质量标准，包括
在每次代码签入时运行的内存安全证明。


## 演示入门

我们提供两个示例，分别为“blinky”和“aws-iot-example”。“blinky”示例演示了 FreeRTOS
内核和 TF-M 集成，而“aws-iot-example”演示了与 AWS IoT Core 的连接
（使用 [coreMQTT-agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) 库）
以及安全 OTA（使用 [OTA 代理](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)）。
如需查看源代码和入门指南，请访问
GitHub 上的 [FreeRTOS/iot-reference-arm-corstone3xx](https://github.com/FreeRTOS/iot-reference-arm-corstone3xx)。

