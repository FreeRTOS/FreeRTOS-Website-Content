---
title: FreeRTOS LTS 库现已纳入我们合作伙伴的工具链
created: 2021-10-19 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 10 月 19 日发布

2020 年 12 月，我们推出了第一个 FreeRTOS Long Term Support（LTS）版本。有了 LTS 版本， 
开发人员可以放心使用 FreeRTOS 版本，该版本自发布之日起两年内提供稳定的功能、安全补丁和 
关键漏洞修复服务。我们的合作伙伴反响热烈， 
正着手将 LTS 版本集成到他们的工具链中。我们的理念是 
让用户能够在自己选择的环境中使用我们的软件，根据这一理念，这些集成将使 
开发 IoT 应用程序的开发人员能够在他们熟悉的环境（供应商的集成开发环境 (IDE) 或软件开发工具包 (SDK)）中，从单一位置访问 IoT 和 AWS 连接所需的所有 FreeRTOS 
库 
。我们很高兴地宣布， 
以下合作伙伴已将 LTS 版本集成到其工具链中，并完成验证：


**Arm**：

一些开发人员使用的集成开发环境所带的插件能够帮助开发人员方便地新增和维护驱动程序、板级支持包 (BSP) 以及 
其他库。这些插件 
通过通用微控制器软件接口标准 (CMSIS) 内容包格式实现以上功能。在 Arm Cortex 处理器的基础上， 
[CMSIS-Pack](https://developer.arm.com/tools-and-software/embedded/cmsis/cmsis-packs) 定义了 
提供软件组件、设备参数、电路板支持信息和代码的标准化方式 
。FreeRTOS 内核以 CMSIS-Pack 形式提供；我们目前以 CMSIS-Pack 格式提供其他 FreeRTOS LTS 库， 
方便开发人员在所选工作流中访问。这些 
CMSIS-Pack 还与最近推出的 [Keil Studio Cloud](https://www.keil.arm.com/) 集成， 
后者是一款基于浏览器的 IDE ，用于 IoT、ML 和嵌入式开发。如果您想了解更多详细信息并亲身 
体验通过 Keil Studio Cloud 使用 FreeRTOS 库， 
[您会发现](https://devsummit.arm.com/en/sessions/73)[](https://devsummit.arm.com/en/sessions/145) 
[Arm DevSummit](https://devsummit.arm.com/en) 上的研讨会和会议非常有趣。


**Espressif**：

Espressif 的软件开发工具包（测试版）提供对 FreeRTOS LTS 库的支持，用于 Espressif 
开发板：[ESP-AWS-IoT](https://github.com/espressif/esp-aws-iot/tree/release/beta)。为了简化 
LTS 库在 AWS IoT 连接中的使用，Espressif 创建了几个示例，包括通过 MQTT 的 OTA、 
Device Shadow 和带有 TLS 相互身份验证的 coreMQTT。请参阅 
[The ESP 杂志博客](https://blog.espressif.com/support-for-lts-release-of-aws-iot-device-sdk-for-embedded-c-on-esp32-8eeeea28b79b) 
了解更多详情。 


**Infineon**：

Infineon 已将 FreeRTOS LTS 库集成到 AnyCloud（Infineon 的云连接 
解决方案），以帮助开发人员利用 PSoC 6 MCU 的连接器件快速构建应用程序。AnyCloud 
包含于 [ModusToolbox](https://www.cypress.com/products/modustoolbox) 中，可提供 
连接性、安全性、固件升级支持和应用层协议（如 MQTT）等核心功能。 
有关 AnyCloud 和 FreeRTOS LTS 库支持的信息，请访问 
[ModusToolBoxAnyCloudSDK](https://community.cypress.com/gfawx74859/attachments/gfawx74859/ModusToolboxAnyCloudSDK/46/2/AnyCloud_1.3_User_Guide_0C.pdf)。


**NXP**：

NXP 的 MCUXpresso 软件和工具提供全面的开发解决方案，旨在 
优化、简化并加快基于 NXP 通用、交叉和蓝牙 MCU 应用 
的嵌入式系统开发。MCUXpresso 软件和工具汇集了 NXP 软件 
功能的精华。MCUXpresso 软件开发工具包 (SDK) 
可在 [NXP 的网站](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-software-development-kit-sdk:MCUXpresso-SDK)上找到， 
该网站还提供[](https://www.nxp.com/pages/part-i-an-introduction-to-aws-iot-and-freertos-the-concepts-and-benefits-of-using-it-together-with-lpc-mcus:TIP-AMAZON-AND-LPC-PART-I) 
与 AWS IoT 连接的自定进度培训。


**Realtek**：

Realtek 已将FreeRTOS LTS 库集成到他们的 [AmebaPro SDK](https://github.com/ambiot/ambpro1_sdk)中。 
本 SDK 包含一些示例，演示如何在 AmebaPro 板上使用 FreeRTOS LTS 库进行 AWS IoT 连接 
和 [AmazonKinesis](https://aws.amazon.com/kinesis/video-streams) 视频流。请参阅 
[《入门指南》](https://github.com/ambiot/ambpro1_sdk/blob/main/doc/AmebaPro_Amazon_FreeRTOS-LTS_Getting_Started_Guide_v1.2_r.pdf) 
即可立即体验。


**Renesas**：

Renesas 通过 Renesas 灵活配置软件包 (FSP) 为 FreeRTOS LTS 库提供支持， 
其中包括使用 Renesas RA 系列微控制器进行嵌入式系统设计的软件。 
您可访问 Renesas 灵活配置软件包的 [主页](https://www.renesas.com/us/en/software-tool/flexible-software-package-fsp) 
获取最新的 [FSP 版本](https://info.renesas.com/en-fsp-download)、[GitHub 存储库](https://github.com/renesas/fsp/releases) 
和[文档](https://www.renesas.com/us/en/software-tool/flexible-software-package-fsp#document)。

我们的其他伙伴正积极进行集成，我们希望 
很快能分享他们的成果。我们很希望看到 FreeRTOS LTS 版本如何优化下一代嵌入式应用程序的开发和 
维护。我们期待您的反馈。如有任何意见或要求，您可以通过 
[FreeRTOS 论坛](https://forums.freertos.org/)联系我们！ 


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

