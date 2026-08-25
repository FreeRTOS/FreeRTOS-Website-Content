---
title: "FreeRTOS 现已获得 SESIP 3 级认证"
date: 2024 年 10 月 9 日
feature: blog
authors:
  - kanherea
---

由 [Aniruddha Kanhere](../author/kanherea) 撰写于 2024 年 10 月 9 日

## 什么是 SESIP？

请参阅我们之前的博客文章：[为什么 FreeRTOS 的 SESIP™ 认证很重要](/Community/Blogs/2021/why-sesip-certification-for-freertos-matters) 
了解有关 SESIP 认证的更多信息以及为何它对嵌入式系统很重要。

## SESIP 3 级认证

安全是 FreeRTOS 的首要任务。为了实现安全承诺，FreeRTOS 已经 
获得[IoT 平台安全评估标准](https://globalplatform.org/sesip) (SESIP™) 3 级保证[认证](https://trustcb.com/iot/sesip/sesip-certificates)。 
[FreeRTOS](https://www.freertos.org/) 主要用于嵌入式系统处理器，目前仍然开发者的首选方案之一， 
由合作超过 21 年的社区提供支持。虽然其 
核心是一个[实时操作系统 (RTOS) 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)， 
但 FreeRTOS 还提供必要的库，例如 [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)， 
即一个安全且不断演变的 TCP/IP 库。此外，它还包含 IoT 应用程序协议库， 
例如 [CoreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)，帮助 
开发者安全连接到云端。作为开源项目，FreeRTOS 在社区贡献的助力下 
蓬勃发展，确保它仍然是嵌入式系统开发的首选方案。

想要查阅 3 级证书，请[在此](https://www.trustcb.com/iot/sesip/sesip-certificates/) 
搜索 “FreeRTOS”。

## SESIP 2 级和 SESIP 3 级有何区别？

SESIP™ 认证拥有五个保证等级，分别为一级到五级。随着保证等级上升，测试 
也变得越来越复杂和严格。[GlobalPlatform™](https://globalplatform.org/sesip/) 负责管理 
[五个 SESIP™ 保证等级](https://trustcb.com/iot/sesip/)，而测试合作伙伴负责开展测试。TrustCB™ 
为所有五个级别的 SESIP™ 认证提供认证。

SESIP3 是针对（部分）IoT 平台的重要保证等级。它要求一位评估者 
开展全面源代码分析，并将分析结果用于脆弱性分析，因此比 SESIP2 提供的保证 
多得多。SESIP3 属于白盒测试，测试人员实施限时源代码 
分析与限时渗透测试，相比之下 SESIP2 属于封闭测试， 
开发者不参与其中。

评估的范围和深度：

* SESIP2 开展的是更为有限的安全评估，侧重于评估目标 (TOE) 的安全功能。
* SESIP3 需要更全面、更深入的安全分析，包括 TOE 的完整功能规范、
实施细节和指导文档。

攻击抵抗性：

* SESIP2 评估对基本攻击潜力的抵抗性。
* SESIP3 评估对增强型基本攻击潜力的抵抗性，更加复杂。

开发环境控制：

* SESIP2 对 TOE 的开发环境的要求极低。
* SESIP3 要求为安全开发环境提供更强有力的控制和证据。

配置管理：

* SESIP2 对配置管理有基本要求。
* SESIP3 需要更广泛的配置管理实践，包括自动化，以确保 TOE 的完整性。

总而言之，与 SESIP2 相比，SESIP3 提供了更严格、更全面、更高级别的安全保证， 
使其适用于 IoT 和具有更高安全要求的嵌入式产品。

获得 SESIP 3 级认证的组件：

| 组件名称 | 版本 | GIT 哈希值标识符 |
| -------------- | ------- | ------------------- |
| FreeRTOS 内核 | [V10.6.1](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/V10.6.1) | 0264280230aa6a828247b5f05bf57e33f1994581 |
| FreeRTOS+TCP | [V3.1.0](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/V3.1.0) | 0bf460c935ca59cf0423ef0ac3505f13961c2e9e |
| corePKCS #11 | [V3.5.0](https://github.com/FreeRTOS/corePKCS11/tree/v3.5.0) | 781f5774948fa8e6427be544b1bf1ad512ae9e90 |
| OTA 更新 | [V3.4.0](https://github.com/aws/ota-for-aws-iot-embedded-sdk/tree/v3.4.0) | f9760892ba152f2c9104d08192ea5ffbbf9fa8ea |
| Mbed TLS | [V2.28.7](https://github.com/Mbed-TLS/mbedtls/tree/mbedtls-2.28.7) | 555f84735aecdbd76a566cf087ec8425dfb0c8ab |

上述所有库以及其他辅助库，例如 CoreMQTT 和供应商驱动程序均添加 
作为 [FreeRTOS/iot-reference-nxp-rt1060](https://github.com/FreeRTOS/iot-reference-nxp-rt1060/tree/v202403.00-SESIP) 存储库的子模块， 
该存储库用于 SESIP 评估。 

## SESIP 认证范围

理想情况下，与 FreeRTOS 捆定的所有内容都将获得 SESIP 认证。这对 IoT 设备来说尤其重要， 
特别是在用于网络之间安全通信的软硬件堆栈导致应用程度变得愈发复杂的情况下。

但是，正如我们在前一篇博客文章中提到的，当应用程序参加 SESIPTM 认证时，开发者的 TOE 重点是其直接控制的代码或硬件。当开发者选择未经 SESIP™ 认证的硬件和软件时，测试机构（例如 Riscure）将需要测试整个软硬件堆栈。因此，我们选择了以下组件用于 SESIP 3 级认证，因为这有助于应用程序开发者在不违反 SESIP 认证保证的情况下选择其他库和/或其他硬件堆栈。

[![图 1：SESIP 3 级认证涵盖的组件](/media/2024/SESIP_level3_scope.png)](/media/2024/SESIP_level3_scope.png)
*图 1：SESIP 3 级认证涵盖的组件*


## 环境假设

SESIP™ 认证过程中测试 FreeRTOS 时必须作出一些环境假设，以便缩小测试参数的范围。
假设：

* 平台只会部署在不需要物理攻击保护的环境中。TOE 必须具有内存保护单元 (MPU) 作为底层硬件。
* 接着假设应用程序开发者应遵循开发最佳实践，以避免内存损坏攻击。实际操作过程中需要信任开发团队，并且必须实施限制 FreeRTOS 源代码修改的开发团队规则。只有经过授权和值得信赖的人员才能访问 TOE 开发环境。
* 第三，连接到 AWS IoT 和其他安全服务时，假设部署平台的硬件应提供密码安全的随机数生成器。
* 最后一个假设是固件空中升级 (FOTA) 功能使用 [AWS IoT OTA 更新管理器](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html)。FOTA 功能依靠集中式系统来传递命令和固件有效载荷。集中式系统不在测试范围内，连接到集中式系统的设备才是测试对象。 

基于以上假设，我们来看一下测试的五大环节。

### 平台身份验证

SESIP3 测试涵盖的所有组件的源代码存储库包含一个 manifest.yml 文件。此文件提供 TOE 的唯一标识，包括物品的名称、描述和特定版本。它还包含任何源代码依赖项的相同信息。manifest.yml 文件中的版本字段是 git 标签标识符，此标识符也对应组件的 git 哈希值。
第三方 Mbed-TLS 库包含一个 ChangeLog 文件，该文件唯一地标识存储库中源代码的版本。版本号还对应 Mbed-TLS 的 git 标签和 git 哈希值。

### 平台实例身份验证

当设备连接到 AWS IoT Core 时，主要标识符被称为 ThingName。此 ThingName 在系统的所有设备中必须是唯一的。AWS IoT Core 还允许设备具有其他属性，例如序列号或软件版本。设备制造商可以选择在制造过程中对 ThingName 进行硬编码，也可以选择添加在配置设备时设置 ThingName 的软件。无论使用哪种方法，ThingName 都由用户存储在安全位置，例如闪存或安全元件，以确保其无法更改。然后，设备使用这个唯一的 ThingName 与 AWS IoT Core 服务交互。

### 平台的安全更新

OTA (Over-The-Air) 更新过程始于设备的 OTA Agent 通过向配置的服务器发送消息以检查新更新。当有新的更新可用时，服务器会将更新元数据发送到设备上的 OTA Agent。根据具体配置，Agent 要么将新的固件映像存储在文件中，要么将其直接写入预留的闪存位置。然后，OTA Agent 通过检查新映像的数字签名来验证其完整性。验证后，OTA Agent 会通知应用程序更新成功。接着，设备将重新启动并开始运行新固件。应用程序开发者负责提供更新基础架构并实施验证新固件映像数字签名的机制，该机制可以是自定义解决方案，也可以使用平台特定的安全功能。

### 应用程序的安全更新

over-the-air (OTA) Agent 旨在简化应用程序开发者为向产品添加 OTA 更新功能而必须编写的代码量。这种集成负担主要包括 OTA Agent 的初始化，也可能涉及创建自定义回调函数用于响应 OTA 完成事件消息的操作。
要使客户端接受 OTA 更新，接收到的更新版本号需要高于其当前运行的固件版本。
设备软件的应用程序版本由开发者设置，方法是为 appFirmwareVersion 数据结构的构建号、次版本号和主版本号赋值。

### 安全通信支持

为了创建安全通信的嵌入式应用程序，开发者通常使用 TLS（传输层安全）库。对于 SESIP3 认证，应用程序需要专门使用 TLS 并选择密码套件 ECDHE_RSA_WITH_AES_128_GCM_SHA256。之所以指定使用这个特殊的密码套件，是因为它提供了强大的加密算法和协议，以确保通信的机密性和完整性。此外，应用程序必须为 TLS 套接字连接设置信任根服务器证书。这样可以确保设备能够对与之通信的服务器进行身份验证，从而防止中间人攻击和其他安全漏洞。通过遵守这些特定的 TLS 要求，嵌入式应用程序可以满足 SESIP3 认证规定的严格安全标准，从而为 IoT 和其他嵌入式系统中的安全通信提供更高级别的保证。

## 接下来做什么？

我建议查看库和存储库及其文档，以开始使用 SESIP 3 级认证的 FreeRTOS 让您的应用程序变得安全可靠。
