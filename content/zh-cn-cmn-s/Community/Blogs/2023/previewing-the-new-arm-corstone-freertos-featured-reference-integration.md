---
title: 预览全新 Arm Corstone FreeRTOS 精选参考集成
date: 2023 年 8 月 1 日
feature: blog
authors:
  - sam-tayloramazon-com
---
大多数人将 Arm 与我们的硬件设计和 Cortex CPU 联系在一起， 
 但是我们对支持这些硬件的软件生态系统的持续承诺同样重要。对我们来说， 
 使开发人员能够轻松地利用我们的最新 CPU、ML 加速器和其他系统 IP 的功能非常重要。由于 FreeRTOS 为越来越多的嵌入式和 
 IoT 设备提供支持，因此它对我们和整个 Arm 生态系统来说都是至关重要的软件。在这篇文章中， 
 我想向您介绍一下我们与 FreeRTOS 团队密切合作的方式， 
 以确保 Arm 硬件完全支持 FreeRTOS，以及开发人员如何快速开始使用最新的 Cortex-M CPU。


最近，我们一直在开发 
 [FreeRTOS 精选参考集成](../../featured-freertos-iot-integrations.md)
 (FRI) 用于我们的 [Arm Corstone-300 和 Corstone-310 平台](../../arm-corstone-3xx.md)。 
 该参考集成演示了 
 如何通过集成模块化的 FreeRTOS 内核和库， 
 并利用基于 Arm TrustZone（Armv8-M）的硬件强制安全性，确保云连接应用程序的安全更新。今天，我们很高兴地宣布， 
 Corstone-300 的首个预览版软件已在 FreeRTOS GitHub 上发布，任何人都可以试用： 
 [https://github.com/FreeRTOS/iot-reference-arm-corstone3xx](https://github.com/FreeRTOS/iot-reference-arm-corstone3xx)。


在接下来的几个月里，我们将对这个项目进行进一步扩展， 
 使其成为运行 FreeRTOS 和 
 [AWS IoT Device SDK for Embedded C](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html#iot-device-sdks)（在 Arm Cortex-M 微控制器上）的完整、可移植和安全的示例 
 。



什么是 Arm Corstone？什么是 Arm 虚拟硬件？
---------------------------------------------------


对于那些不熟悉 Corstone-300 和 Corstone-310 的人， 
 我也许应该花点时间解释一下它们是什么。Arm 为微控制器开发了许多不同的 IP： 
 从我们的 Cortex-M 处理器核心和 Ethos-U 机器学习加速器，到 
 系统 IP、软件和工具。我们的 Corstone 平台将所有这些元素集合在一起， 
 形成可配置的子系统，SoC 设计师可以将其作为设计起点。


由于 Cortex-M55 和 -M85 器件在市场上仍然很新， 
 我们还提供 Corstone 平台，并将其作为 
  [Arm 虚拟硬件](https://www.arm.com/products/development-tools/simulation/virtual-hardware)和 
 [固定虚拟平台](https://developer.arm.com/downloads/-/arm-ecosystem-fvps) (FVP)。 
 这些平台提供了一个硬件模型， 
 允许在可用芯片之前对软件进行测试。虚拟平台作为开发人员 
 免费试用 Arm 所有最新内核和架构功能的简便方法，越来越受欢迎， 
 而且无需等待硬件可用。


我们最近的两个 Corstone 是：


* [Corstone-300](https://developer.arm.com/Processors/Corstone-300)：采用了 Cortex-M55，配备 
 [TrustZone-M](https://www.arm.com/technologies/trustzone-for-cortex-m) 和  
 [Helium 
 向量扩展](https://www.arm.com/technologies/helium)，同时还可选配 Ethos-U55 ML 加速器。
* [Corstone-310](https://developer.arm.com/Processors/Corstone-310)：采用了具有 TrustZone-M 和 
 Helium 向量扩展的高性能 Cortex-M85，同时集成了 Ethos-U55 ML 加速器。



[![Corstone-310 SSE-310 子系统示例集成](/media/2023/example-integration-corstone3xx.png)](/media/2023/example-integration-corstone3xx.png)
  

Corstone-310 SSE-310 子系统示例集成。点击放大。 

因此，在考虑构建 FreeRTOS FRI 时，从我们最新的两个 
Corstone 平台开始是很有意义的。



Arm Corstone FRI 的元素
--------------------------------


在构建 FRI 时，我们努力牢记以下几点：


* 尽量保持简单、熟悉，并遵循 
 其他 FreeRTOS FRI 使用的方法。
* 包括访问 Corstone-300 和 Corstone-310 所有功能的基本软件。
* 使其易于构建、修改和移植到其他基于 Arm 的硬件上。
* 展示如何通过在 TrustZone for Cortex-M 上运行的安全服务来支持 AWS IoT Device SDK for Embedded C 的功能 
 。


对于我们来说，可移植性非常重要， 
 因为我们希望开发人员和合作伙伴能够在其他平台上使用此功能。因此，我们从基于 
 [CMSIS](https://www.arm.com/technologies/cmsis)
 驱动程序的简单 BSP 开始。CMSIS 是一种通用的低级微控制器软件标准， 
 得到了许多不同芯片供应商的支持。它还包括用于 
 信号处理 ([CMSIS-DSP](https://arm-software.github.io/CMSIS_5/DSP/html/index.html)) 和机器学习 
 ([CMSIS-NN](https://arm-software.github.io/CMSIS_5/NN/html/index.html)) 的优化库，您可以根据需要将其添加到您的应用程序中。


未来，我们希望加入其他一些可选的 CMSIS 可移植性 API， 
 如通用的 IoT 套接字接口， 
 以方便已在现有产品中使用 CMSIS 的开发人员。这还为 Arm 的芯片合作伙伴提供了一个 
 支持 FreeRTOS 的优秀示例，从而缩短了他们产品的上市时间。



使其安全且可更新
-----------------------------


如今，每个人都知道确保 IoT 设备的安全性有多么重要。我们也知道， 
 安全不是开发时才做的事情；只有能在现场更新固件， 
 才能保持设备安全。这就是为什么在过去的几年里， 
 安全一直是 Arm 关注的重点。我们已经在博客上分享了我们的一些早期工作， 
 我非常希望看到其他行业参与者在过去几个月中的发展。


很多人都知道，Arm 的 IoT 安全工作通过 
  [PSA 认证](https://www.psacertified.org/)实现了标准化。 
 除了为 IoT 设备中的硬件可信根提供标准外， 
 PSA 认证还包括[加密](https://arm-software.github.io/psa-api/crypto/)、 
 [安全存储](https://arm-software.github.io/psa-api/storage/)、 
 [认证](https://arm-software.github.io/psa-api/attestation/)以及最近的 
 [固件
 更新](https://arm-software.github.io/psa-api/fwu/)。Arm Corstone FRI 包括带有 Mbed TLS 和 MCUboot 的 TrustedFirmware-M， 
 可提供一整套符合 PSA 认证所有安全要求的安全软件。


现在，我们的最终目标是确保 TLS 连接和固件更新能够 
 使用由 TF-M 提供的安全服务，并得到 TrustZone-M 中的硬件隔离支持。 
 我们通过两个重要的集成点来实现这一目标：


1. **PKCS11 支持**——我们有一个简单的包装器， 
 在 Mbed TLS 和 PSA Crypto API 基础上实现了对 PKCS11 的支持。这使得 
 [PKCS#11](../../pkcs11/index.md) API 能够执行 TLS 客户端认证， 
 并使用 TF-M 提供的 
 底层 PSA 安全存储和 PSA Crypto 支持将 TLS 客户端证书和私钥导入设备中。
2. **AWS OTA PAL 支持**——我们还集成了一个桥接程序，可将 AWS OTA PAL 
 映射到 TF-M 实现的 PSA 固件更新 API。这允许 Corstone-300 
 接收来自 AWS IoT Core 的新映像， 
 并在将映像部署为活动映像之前使用 TF-M 进行验证。安全映像（TF-M）和非安全映像（FreeRTOS 内核和应用程序） 
 可分别更新。每次启动设备时， 
 MCUBoot（引导加载程序） 
 都会在启动映像前验证映像签名是否有效。由于安全 (TF-M) 和非安全（FreeRTOS 内核 
 和应用程序）映像是分别签名的， 
 因此 MCUBoot 会在启动前验证两个映像签名是否有效。如果其中一个验证失败，MCUBoot 
 就会停止启动过程。


之前，这两个桥接程序分别存在于不同的存储库中， 
 但现在我们直接将它们包含在 Corstone FRI 中。有关 FRI 安全特性的更多信息， 
 请访问项目登陆页面。



敬请期待——更多精彩等您发现
--------------------------------


正如我之前提到的，我们今天发布的代码只是 Arm Corstone FRI  
 的第一个预览版。在接下来的几个月里，我们有很多内容要添加。例如， 
 这个第一个预览版使用了我们的 FVP 中内置的虚拟套接字接口进行基本连接， 
 但在未来，我们还想要全面支持 FreeRTOS TCP/IP 和 
 lwIP。我们还计划增加对 HTTP、 
 [AWS IoT Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) 和 
 [AWS IoT Device Defender](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html) 的支持。 
 之后，我们还有很多事情要做， 
 包括启用 Ethos-U 和 ML 示例。有人有兴趣在不进行全面固件更新的情况下 
 更新设备上的 ML 资产吗？我不保证， 
 但这就是我们未来想要做的事情。


今天，我们很高兴能与大家分享第一版预览版。我们 
 希望您能够尝试 
 并在 [FreeRTOS 论坛](https://forums.freertos.org/)上分享您的反馈意见， 
 以及对我们下一步工作的建议。

