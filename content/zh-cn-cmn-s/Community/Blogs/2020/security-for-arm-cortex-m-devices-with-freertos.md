---
title: 使用 FreeRTOS 确保 Arm Cortex-M 设备的安全
created: 2020-07-17 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- arm-author
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Shebu Varghese Kuriakose](../author/arm-author) 发表于 2020 年 7 月 17 日

确保微控制器的安全非常具有挑战性，部分原因在于这些设备缺乏由硬件强制实施的安全域。 
如需创建两个安全域，通常需要两个微处理器，每个都配有独立的内存保护 
单元 (MPU)。随 Armv8-M 架构一起引入的 Arm TrustZone 
能够在单个 Cortex-M 处理器上实现两种安全处理环境 
（请参阅[在 Armv8-M 微控制器上使用 FreeRTOS](https://www.freertos.org/2020/04/using-freertos-on-armv8-m-microcontrollers.html)）。 
拥有单独的安全处理环境和非安全处理环境后，您将如何利用它们？


## Trusted Firmware-M 简介

[Trusted Firmware-M](https://www.trustedfirmware.org/) (TF-M) 
为 Armv8-M 架构（例如 Cortex-M55、Cortex-M33 和 Cortex-M23 处理器）和双核 Cortex-M 
设备实现了安全处理环境 (SPE)，是符合 
[PSA 认证指南](https://www.psacertified.org/about/developing-psa-certified/) 的 PSA 参考实现， 
可帮助芯片、实时操作系统和设备获得 PSA 认证。TF-M 是开源项目， 
根据 BSD-3 Clause 许可分发，托管于 Trusted Firmware 开放治理社区项目， 
在多种基于 Cortex-M 的微控制器（例如 NXP LPC55S69、ST STM32L5 和 Cypress PSoC 64）上均受支持。 FreeRTOS 
已通过 TF-M 获得 [PSA 功能 API 认证](https://www.psacertified.org/products/freertos/)。

TF-M 提供了一套安全服务，包括加密、认证和安全存储，还通过 
基于 mcuboot 的第二阶段引导加载程序提供安全启动，用于验证平台的运行时映像和更新 
。非安全处理环境 (NSPE) 中的应用程序和库 
可以通过一组标准化的 PSA 功能 API  来利用这些安全服务。在 Armv8-M 设备上，TF-M 使用 
Arm TrustZone 技术将 NSPE 和安全处理环境 (SPE) 代码和数据隔离开来。 
在 Cortex-M 设备上运行的应用程序可以利用 TF-M 服务来确保 
与边缘网关和 IoT 云服务的安全连接。TF-M 还可以保护平台上的关键安全资产， 
例如敏感数据、密钥和证书。
  
![](/media/2020/Figure-1.png)   
*图 1：基于 Armv8-M 且集成了 TF-M 的 Cortex-M 处理器*

TF-M 与 FreeRTOS 已实现初步集成，这可确保在 Cortex-M 设备上运行 FreeRTOS 的应用程序 
能够通过 PSA 功能 API 利用 TF-M 提供的安全服务。该集成 
已在 
Arm [Musca-B1](https://developer.arm.com/tools-and-software/development-boards/iot-test-chips-and-boards/musca-b-test-chip-board) 
参考平台上进行验证，预计会在多个支持 TF-M 的 Cortex-M 平台上得到应用。


## 与 FreeRTOS 内核集成

如下图所示，FreeRTOS 内核在 NSPE 中运行，而 TF-M 在 SPE 中运行。FreeRTOS 任务 
可以通过PSA 功能 API 利用各种 TF-M 安全服务（例如加密、安全存储和认证）。 
非安全调度程序可将任务发出的 PSA 功能 API 调用转发给 TF-M。如需查看该集成 
示例，请访问 [Github](https://github.com/Linaro/amazon-freertos/pull/1/commits)。 
NSPE 可以使用 IPC 或函数调用机制与 TF-M 通信，这些机制可提供不同级别的 
安全保护和隔离。FreeRTOS 可以根据应用程序需求 
使用其中任一机制与 TF-M 通信。 

![](/media/2020/Figure-2.png)   
*图 2：基于 Armv8-M 且集成了 FreeRTOS 和 TF-M 的 Cortex-M 处理器*


## 与 PKCS# 11 集成

FreeRTOS 的参考 IoT 集成提供了各种库和 API，例如安全套接字、TLS、 
OTA 代理和 PKCS#11（公钥加密标准 #11），以提高应用程序的安全性。 

[PKCS#11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) API 可在 FreeRTOS 中用于执行 TLS 客户端身份验证 
并将 TLS 客户端证书和私钥导入设备。PKCS#11 已通过轻量级中间层与 TF-M 集成， 
并在 Arm Musca-B1 参考平台上进行了验证。在集成过程中，PKCS#11 API 
通过中间层调用适当的 PSA 功能安全存储 API 或加密 API，这可确保 
密钥和证书受到保护，在 TF-M 的 SPE 内安全执行加密操作， 
并与 NSPE 中的内核、库和应用程序隔离开来 
。密钥和证书分别安全地存储在芯片存储器和外部闪存中， 
这可由 TF-M 的内部可信存储 (ITS) 和受保护存储 (PS) 服务实现。在进行 TLS 客户端身份验证时，签名操作 
由 TF-M 的加密服务执行。如需查看 
Arm Musca-B1 参考平台上的集成示例（如下图所示）， 
请点击[此处](https://github.com/Linaro/amazon-freertos/pull/2/commits)，其中还包含 
[自述文件](https://github.com/Linaro/amazon-freertos/pull/2/files#diff-2f722d7178d1065f926c803457657e2b)。 
PSA 功能 API 中间层位于 FreeRTOS 项目的 
[psa 文件夹](https://github.com/aws/amazon-freertos/tree/master/libraries/abstractions/pkcs11)， 
可供支持 TF-M 的平台使用。

![](/media/2020/Figure-3.png)   
*图 3：基于 Armv8-M 且集成了 FreeRTOS、PSA 功能 API 中间层和 TF-M 的 Cortex-M 处理器*

表 1 显示了 FreeRTOS 中使用的 PKCS #11 API 与 
在密钥和证书配置以及 TLS 客户端身份验证过程中调用的 PSA 功能 API 的映射关系。

| PKCS11 API | PSA 功能 API |
| --- | --- |
| C_CreateObject | psa_ps_set psa_import_key psa_close_key  |
| C_GenerateKeyPair  | psa_generate_key psa_export_public_key psa_import_key  |
| C_DestroyObject  | psa_ps_remove psa_destroy_key  |
| C_VerifyInit  C_Verify  | psa_verify_hash  |
| C_SignInit  C_Sign | psa_sign_hash |
| C_FindObjectsInit  C_FindObjects  | psa_open_key  |
| C_GetAttributeValue  | psa_ps_get  psa_export_key |
| C_DigestInit  C_DigestUpdate  C_DigestFinal  | psa_hash_setup,  psa_hash_update,  psa_hash_finish  |
| C_GenerateRandom  | psa_generate_random  |

*表 1：PKCS# 11 和 PSA 功能 API 的映射关系*


## 下一步

下一步是扩展 FreeRTOS 安全组件与 TF-M 的集成，使之不再限于 PKCS#11 
接口。应用程序可通过 FreeRTOS OTA 代理在平台上接收、验证和部署新映像 
。将 OTA 代理与 TF-M 的安全启动集成，有助于 FreeRTOS 在 SPE 内验证新映像， 
从而利用平台提供的各种安全功能来缓解 
映像更新漏洞。随着 Mbed TLS 项目开始使用 PSA 功能加密 API 进行加密操作， 
FreeRTOS 发起的所有 TLS 操作都将通过 PSA 功能加密 API 
调用 TF-M 加密服务。当前集成和相关增强功能适用于多种支持 TF-M 的 Cortex-M 设备， 
可简化 FreeRTOS 应用程序开发者的安全工作 
。

请访问 [Trusted Firmware](https://www.trustedfirmware.org/) 项目以详细了解 TF-M， 
并在 [Github](https://github.com/Linaro/amazon-freertos/pulls) 上访问 FreeRTOS 
在 [Musca-B1](https://developer.arm.com/tools-and-software/development-boards/iot-test-chips-and-boards/musca-b-test-chip-board) 上的集成。 
[psa 文件夹](https://github.com/aws/amazon-freertos/tree/master/libraries/abstractions/pkcs11) 中的 PSA 功能 API 中间层 
可供 FreeRTOS 和支持 TF-M 的平台使用。

![](/media/2020/Figure-4.png)   
*图 4：基于 Armv8-M 且完全集成了 FreeRTOS 和 TF-M 的 Cortex-M 处理器*


## 作者简介

![](https://secure.gravatar.com/avatar/db732371ff8ea1e00013619782acc940?s=200&d=mm&r=g)   
Shebu Varghese Kuriakose 是 Arm 开源软件集团软件技术管理总监 
兼可信固件项目委员会主席。Shebu 致力于推动 Trusted Firmware-M 开发路线图， 
并与芯片供应商、RTOS 和工具生态系统开展合作。  
[查看此作者的文章](../author/arm-author) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

