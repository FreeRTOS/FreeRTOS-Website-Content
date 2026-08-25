---
title: "使用 AWS IoT ExpressLink 的精选 FreeRTOS IoT 集成"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

其他[精选 FreeRTOS 参考集成](/Documentation/01-FreeRTOS-quick-start/02-Featured-integrations/01-Featured-integrations) 
演示了[长期支持 (LTS) 版本的 FreeRTOS 库](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)， 
以及硬件支持的安全功能，用于帮助创建经过身份验证的安全云连接。 
此页展示如何使用 AWS IoT ExpressLink 模块（以下简称 "ExpressLink"）更轻松地实现 
相同的目标。


ExpressLink 模块属于[硬件 Wi-Fi 和蜂窝模块](https://devices.amazonaws.com/search?page=1&sv=iotxplnk)， 
具有内置云连接、over-the-air (OTA) 更新以及硬件支持的加密和身份验证密钥安全存储功能 
。执行 IoT 应用程序的主机处理器可使用简单的 AT 命令集， 
通过串行端口与 ExpressLink 通信。所有 ExpressLink 模块都使用相同的 
命令集，而不考虑底层无线电类型（例如 Wi-Fi、蜂窝）。使用 ExpressLink 
模块后，IoT 应用程序编写者无需处理复杂的无线电、安全和 IoT 库 
。这些开发人员可以专注于开发差异化功能。

ExpressLink 模块可在任何具有串行端口的设备上使用，比如微型 8 位微控制器 (MCU)、 
机架式服务器。本页重点介绍了通过 
[ST 的 I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink)（针对一系列 STM32 MCU）创建的 ExpressLink 演示 
。


[![](/media/2023/design-of-connected-apps-iotel.png)](/media/2023/design-of-connected-apps-iotel.png)   
**图 1：连接 AWS IoT ExpressLink 的应用程序设计**


## 安全功能和函数演示

所有 AWS IoT ExpressLink 模块均采取以下小节中描述的安全最佳实践。


### 通过双向验证保障 TLS 通信的安全

ExpressLink 模块建立与 AWS IoT 核心的安全加密连接 
通过[传输层安全协议 (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security)。此 
连接经过双向验证，确保设备和云的身份。每个 
模块都预先配置了建立此安全连接所需的唯一标识符、私钥
和证书。该证书已由模块供应商 
在 AWS 注册的证书颁发机构 (CA) 签署。这解决了 
与 IoT 设备调配相关的可扩展性、潜在错误和安全问题，同时降低了复杂性和成本。


### 确保设备身份和机密信息的安全

ExpressLink 模块使用硬件支持的安全存储来确保设备身份和私钥的安全。


### 不泄露供应链中的机密信息

*载入*是指将模块的凭据绑定到 
OEM 账户中 [AWS IoT 注册表](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html)内部的 “thing” 上 
。ExpressLink 使用 
新颖的[按声明载入](https://docs.aws.amazon.com/iot-expresslink/latest/oemonboardingguide/oemog.html) 
机制，在设备首次启动时自动执行此操作。此后期绑定之后， 
就不再需要为使用 IoT 设备供应链的供应商提供任何秘密信息，例如私钥 
。


### 防止未经授权的软件在设备上运行

ExpressLink 模块包括硬件信任根支持的安全引导加载程序， 
该加载程序在每个引导阶段以加密方式验证其固件完整性，有助于防止未经授权的 ExpressLink 固件修改 
。


STM32 示例还使用 Tiny Secure Boot，确保主机（与 ExpressLink 通信的 MCU） 
软件的 ECDSA 签名验证。Tiny SecureBoot 占用空间小于 15K 闪存 
。他们还利用 ExpressLink 模块的功能来验证通过无线接收的新主机映像的完整性（哈希）和真实性（签名）， 
即从主机应用程序中卸载这些加密任务 
。


### 确保 over-the-air (OTA) 更新的安全

OTA 更新通过修补已部署设备中的安全漏洞和错误来增强安全性。 
ExpressLink 的 OTA 功能可实现 ExpressLink 模块和主机 MCU 的安全固件更新。

模块更新不会中断主机 MCU。每个模块都预先配备了 OTA 
“出生证明”，用于验证其固件更新是否已获得模块制造商的授权。模块 
在验证成功后向主机 MCU 发出接受或拒绝更新的信号， 
以确保兼容性。

主机 MCU 更新可以接收任何文件类型，而不仅仅是新固件版本，他们使用与模块更新相同的机制， 
但无法预先配置主机 MCU OTA 证书。相反，必须首先 
生成、上传并安全地存储该证书至 ExpressLink 模块内。ST 示例 
提供了用于此目的的脚本。

在 ExpressLink 模块中验证固件更新可以减轻主机应用程序的繁重加密任务。


## I-CUBE-ExpressLink 入门指南

[I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink) 是一个 CMSIS 包，包含 
大量 FreeRTOS 项目，这些项目使用 ExpressLink 并面向 
[STM32 Arm Cortex MCU](https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html)。
它包括一个 ExpressLink 驱动程序，该驱动程序是通过串行接口管理 ExpressLink 命令和响应的包装器 
。这些命令和响应在多于 10 个 STM32 开发板上运行的应用程序示例上比较常见，并在这些应用程序中广泛使用 
。该包还包含一套丰富的工具， 
可简化主机 OTA 流程，有助于大规模部署，减少所需步骤，而且 
无需熟悉 AWS 控制台。FreeRTOS 项目演示了典型的 IoT 场景：

* 将传感器数据传输到云端。
* 向云发送消息和从云接收消息。
* 使用 [AWS IoT 阴影](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) 
  从云端控制 LED 和其他执行器。（ExpressLink 具有阴影功能。）
* 无线更新主机固件。
* 管理 ExpressLink 模块事件。

这些示例可与 ExpressLink 蜂窝和 Wi-Fi 模块无缝配合使用，
无需修改任何代码。

要开始使用，请观看 STM32 ExpressLink 教程视频：

* 视频 1：[I-Cube-ExpressLink 入门指南](https://www.youtube.com/watch?v=CAu-zse7nbM)。
* 视频 2：[构建 FreeRTOS，发布主机 OTA 更新，启用 ExpressLink_Event](https://youtu.be/CJrZzpHr38g)。
* 视频 3：[使用 Tiny Secure Boot 并执行主机 OTA](https://youtu.be/r7H9otJWWCI)。

然后访问 [I-Cube-ExpressLink](https://github.com/stm32-hotspot/I-CUBE-ExpressLink) github 存储库 
开始开发。存储库提供了完整的功能列表，包括 ExpressLink 
驱动程序、示例源代码，以及安装数据包、生成、构建和 
运行 FreeRTOS ExpressLink 演示的相关说明。
