---
title: 推出三个精选 FreeRTOS IoT 集成以提升 IoT 应用程序安全性
date: 2022 年 5 月 9 日
feature: blog
categories:
- 长期支持
authors:
- luciodj
---
我们很高兴地宣布推出三个[精选 FreeRTOS IoT 集成](../../featured-freertos-iot-integrations)， 
这些集成是与合作伙伴 Espressif、NXP 和 STMicroelectronics 合作开发的。每个项目 
都演示了如何使用最新的 FreeRTOS 和 AWS 嵌入式 C SDK 
[长期支持 (LTS)](https://freertos.org/lts-libraries.html) 库，以及最新的 
微控制器架构功能，以*提高 IoT 应用程序的 
安全性和模块化水平*。这三个项目不仅旨在为开发者提供更安全的云连接设备示例， 
更旨在提供可轻松自定义的示例，以形成 
具有生产价值的全面 IoT 产品。

这些参考集成项目演示了如何使用不同的微控制器架构 
以及安全存储密钥的不同方法，都通过 
AWS IoT Core 服务的双向 TLS 验证建立更安全的云连接，并支持 Over the Air (OTA) 更新，能够
在整个产品生命周期保证应用程序的安全。OTA 更新 
可以与应用程序 (MQTT) 遥测和命令/控制任务无缝并行执行， 
这得益于新 [MQTT-Agent 库](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) 的实现。

具体而言：

* **[Espressif ESP32-C3](../../featured-freertos-iot-integration-targeting-an-espressif-esp32-c3-risc-v-mcu)** 
  集成旨在利用其最新一代 RISC-V（32 位）核心， 
  并利用板载数字签名外围设备（片上安全程序集） 
  更安全地管理密钥，同时加速所有加密操作。得益于 ESP32-C3 系统片上蓝牙 (BLE5) 
  功能， 
  [ESP32-C3 DevKitM-1](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html) 
  评估套件可提供经济实惠且完整的 IoT 设备开发平台。
  
* **[NXP i.MX RT1060](../../NXP-RT1060-SE050)** 集成基于 
  [i.MX RT1060 评估套件](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1060-evaluation-kit:MIMXRT1060-EVK) 
  (MIMXRT1060-EVK) 与 EdgeLock® SE050 开发套件 (OM-SE050)，以保证基于硬件的安全性。 
  这个新项目基于先前为获得 
  第一个 [FreeRTOS SESIP 安全认证](https://freertos.org/2021/03/why-sesip-certification-for-freertos-matters.html) 所做的工作， 
  提供了一个有用示例，演示了如何将 AWS IoT Embedded C SDK 库 
  与预配置的（即插即用）安全元件相结合，以建立 IoT 设备身份并提高 
  与 AWS IoT Core 通信的安全性。
  
* **[STMicro STM32U5](../../STM32U5)** 集成基于 
  [STM32U5 系列](https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html) Arm 
  32 位 Cortex-M33 核心（采用 ARM v8-M 架构），该核心 
  结合了 [Arm TrustZone 技术](https://developer.arm.com/ip-products/security-ip/trustzone) 
  和片上硬件信任根 (RoT)，以支持安全启动和安全数据存储。在 
  这个项目中，OTA 客户端使用 Arm 的 PSA API。本地可执行映像 
  和远程 IoT 云端身份验证所需的私钥和其他密钥完全存储在 TF-M 中， 
  无法从非安全端访问。

请务必阅读每个新的[精选 FreeRTOS IoT 集成](../../featured-freertos-iot-integrations) 
页面，以深入了解如何利用 FreeRTOS 及其 
[核心库](https://freertos.org/freertos-core/overview.html) 快速 
轻松地开发更安全、更强大的 IoT 应用程序。 

FreeRTOS 是一款基于 MIT 许可且适用于微控制器的开源实时操作系统， 
可用于轻松对低功耗小型边缘设备进行编程、部署、保护、连接和管理。点击以下链接，即可开始使用 
[FreeRTOS](https://freertos.org/RTOS.html) 及其众多 
[库和演示项目](/Documentation/03-Libraries/01-Library-overview/Library-categories)。请通过 
[FreeRTOS.org](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/) 或 
[GitHub](https://github.com/freertos/freertos) 下载源代码。


### 作者简介

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio 是 Amazon Web Services 的产品经理。过去 20 年里，他在半导体行业 
担任过各种技术和营销职务。他是一名富有见解的高产作家，发表了 
许多关于嵌入式控制应用程序编程的文章和技术书籍。热爱 
飞行的他还获得了 FAA 和 EASA 私人飞行员执照。  
[查看此作者的文章](../author/luciodj) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

