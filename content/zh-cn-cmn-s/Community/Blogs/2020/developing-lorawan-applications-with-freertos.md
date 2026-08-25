---
title: 使用 FreeRTOS 开发 LoRaWAN 应用程序
date: null
feature: blog
categories:
- 长期支持
authors:
- gvg
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---



由[ Gaurav Gupta ](../author/gvg)于 2020 年 12 月 14 日发布

我们很高兴介绍 [ FreeRTOS Labs 项目 LoRaWAN](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library)，它是 
LoRaWAN 与 FreeRTOS 实现连接的一个参考案例。本项目旨在演示 FreeRTOS 
如何使用 LoRa 技术简化 IoT 应用程序的开发。LoRa 是一种在免许可频谱中 
运行的长距离、低功耗无线技术，专为需要在不同环境中 
远距离发送不频繁、少量数据的传感器而设计。LoRa 是一种物理 
层展布频谱调制技术，源自啁啾扩频 (CSS) 无线通信 
技术。LoRaWAN 是 LoRa 的网络系统架构和通信协议规范， 
由 [LoRa 联盟](https://lora-alliance.org/)开发。 


## LoRaWAN 网络架构

LoRa 联盟定义了 LoRaWAN 的网络层和系统架构。图 1  
描绘了 LoRaWAN 连接流程，显示不同组件将终端节点连接到 
云端和应用程序服务器。

![图 1：LoRaWAN 网络架构](/media/2020/Figure-1-2.png)  
*图 1 - LoRaWAN 网络架构*


LoRa 不同于蜂窝技术，其终端节点不与特定网关相关联。相反，数据 
由节点传输并由多个网关接收。每个网关随后通过蜂窝、 
以太网、卫星、WiFi 等回程线路，将数据包从终端节点转发到基于云的 LoRa 网络 
服务器 (LNS)。LNS 具备一定的复杂性和智能性，能够管理网络、过滤冗余数据包、 
执行安全检查和启用自适应数据速率等。因此，对于移动 LoRaWAN  
终端设备而言，不存在网关间切换。 

应用服务器 (AS) 负责安全地处理、管理和解析传感器应用 
数据，以及为驱动仪表板 UI 提供数据。 

入网服务器 (JS) 管理入网终端设备的空中激活 (OTAA) 流程 
。JS 对终端设备执行入网流程（双向认证），将终端设备 
应当连接到哪个 AS 通知给 LNS，并派生会话密钥。每个 JS 由 
一个 64 位的全局唯一标识符 AppEUI（或 JoinEUI）标识。终端设备基于 DevEUI、Join EUI、 
DevNonce、根密钥 (AppKey、NwkKey ) 在本地派生会话密钥，使得安全密钥不会 
通过无线交换。JS 向 LNS 传递网络会话密钥并向 AS 传递应用程序会话密钥 
。终端设备安全地存储各自的根密钥，而等效的匹配密钥则安全地 
存储在 JS 上。因此，JS 包含其管理的每个终端设备的以下信息：

* DevEUI（终端设备唯一序列标识符）
* 根密钥
  + AppKey（应用程序密钥）
  + NwkKey （网络密钥）
* 应用程序服务器标识符
* 终端设备服务配置文件

个性化激活 (ABP) 过程相对简化和不安全。 
在通过个性化激活过程中，入网流程被跳过，并且可以在生成 ID 和密钥时进行个性化。 
终端设备被绑定到特定的网络或服务，而且其网络地址的一部分 
由网络标识符 (NetID) 构成，这使得他们在供电后可以立即使用。 

LoRaWAN 规范定义了三种终端设备类型：A 类、B 类和 C 类。A 类设备 
大部分时间处于空闲状态（即节能模式）。当终端设备正在监控的传感器环境 
发生变化时，设备会唤醒并启动上行链路，将传感器读数传输 (Tx)  
到 LNS。终端设备随后监听来自 LNS 的响应，在上次启动上行链路传输 (Tx) 之后的 
指定时间（1 秒和 2 秒）内，它至多打开两个接收 (Rx) 窗口。LNS 可以在任一 Rx 窗口中 
发送下行链路消息。B 类设备扩展了A 类设备的 Rx 功能，为来自 LNS 的下行链路消息 
增加预定的 Rx 窗口。这是通过使用由网关传输的时间同步信标来实现的， 
同步信标指示终端设备周期性地打开 Rx 窗口。C 类设备始终保持接收 (Rx) 窗口开启， 
进一步扩展了 A 类设备功能。C 类设备不依赖电池供电，除了在发送 (Tx)  
上行链路消息时，始终监听下行链路消息。因此，在 LNS 和终端设备 
之间的通信中，C 类设备的通信延迟最低。了解有关 LoRaWAN 1.0.3 的详细描述， 
请参阅[此处](https://lora-alliance.org/resource-hub/lorawanr-specification-v103)。 


## FreeRTOS 的 LoRaWAN 堆栈

FreeRTOS 为嵌入式软件开发人员提供了诸多好处。[继续阅读](../../FAQWhat#WhyUseRTOS)。 

如图 2 所示，FreeRTOS 的 LoRaWAN 堆栈使用 LoRaWAN 管理任务对 LoRaWAN 网络的 
时序约束进行抽象，从而为应用程序层提供更简单的编程模型。它 
将处理无线中断和 MAC 层事件的问题与用户应用程序分开。这 
使得应用程序任务能够顺序执行，更具有模块化。这也有助于采用 
定义良好的 Helper API。Helper API 可以在不同的应用程序中复用，例如阻塞 API 可以用于 
加入网络、发送和接收原始数据。如果设备不支持安全配置， 
还可以使用用于配置和获取加入证书的 Helper 函数。当前版本 
仅支持 A 类设备功能。未来版本将支持 B 类和 C 类设备， 
同时支持应用程序在不同的操作类型之间切换。堆栈还暴露了 
无线硬件抽象层 (HAL)，该层为应用程序提供了直接控制 LoRa 无线模块或调制解调器的能力 
。HAL 可以用于一个或多个 LoRa 无线电收发器或 LoRa 无线电调制解调器。

FreeRTOS 的 LoRaWAN 堆栈使用 LoRaMac-Node，这是 Semtech 对 LoRaWAN  
终端设备协议规范的开源实现。此堆栈实现了 LoRaWAN 的 1.0.3 版规范。 
了解更多有关 LoRaMac-Node 的详细信息，请访问 [Semtech 的文档](http://stackforce.github.io/LoRaMac-doc/)。 
FreeRTOS 支持 LoRaWAN 的源代码可在[此处](https://github.com/Lora-net/LoRaMac-node)获得。 

![](/media/2020/Figure-2.png)   
****图 2：FreeRTOS****  
 中的 LoRaWAN 堆栈

## 开发 LoRaWAN IoT 应用程序

在 LoRaWAN 通信中，上行和下行链路消息可以经过确认（需要另一方 
的 ACK）或未经确认（无需 ACK）。下图 3a 和 3b 展示了 
已确认的上行链路和下行链路的序列。了解有关详细说明，请参阅 
 [LoRaWAN 1.0.3](https://lora-alliance.org/sites/default/files/2018-07/lorawan1.0.3.pdf) 规范的第 18 节。 

![图 3a：已确认数据消息的上行时序图（来源：LoRa 联盟）](/media/2020/Figure-3a.png)  
*图 3a：已确认数据消息的上行时序图（来源：LoRa 联盟）*
  
  
![图 3b：已确认数据消息的下行时序图（来源：LoRa 联盟）](/media/2020/Figure-3b.png)  
*图 3b：已确认数据消息的下行时序图（来源：LoRa 联盟）*
  
FreeRTOS 堆栈会生成 A 类设备应用程序任务，该任务定期发送上行链路消息 
并遵循 
[LoRaWAN 地区参数](https://lora-alliance.org/resource-hub/rp2-101-lorawanr-regional-parameters-0)定义的链路公平访问策略。 
上行链路消息在已确认或未确认模式下均可发送。成功启用上行链路后，任务 
将等待下行链路消息或任何其他来自 MAC 层的事件。它将帧负载和移植 
接收到的下行链路消息写入控制台。如果 MAC 层显示有其他下行链路消息挂起 
或有出于控制目的需要发送的上行链路，它会立即发送空上行链路。如果 MAC 层 
检测到帧丢失，它会触发再入网流程来重置帧计数器。处理完 
所有下行链路数据和事件后，任务将恢复休眠状态直到下一个传输周期。

MAC 层到应用程序的所有事件都使用轻量级任务通知发送。LoRaWAN 允许 
将服务器的多个请求捎带到上行链路消息中。这些请求的响应 
由应用程序接收，以便使用队列。如果应用程序想要在发送上行链路有效负载之前 
同时对接收到的多个有效负载进行读取，也会使用下行队列。 


## 低功率模式

A 类设备通信的一个重要功能是，应用程序在其生命周期的大部分时间 
休眠，因而消耗的功率更少。可以使用 FreeRTOS 的无滴答空闲功能为演示项目启用 
低功耗模式，如[此处](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)所述。通过为  
`portSUPPRESS_TICKS_AND_SLEEP(`) 宏提供板特定的实现，并将 
 `configUSE_TICKLESS_IDLE` 设置为 `FreeRTOSConfig.h` 中的适当值，即可以启用无滴答空闲模式。启用无滴答模式后， 
MCU 可以在任务空闲时休眠，但会被无线电中断或其他定时器事件中断唤醒 
。


## 支持的平台

| 供货商 | MCU | LoRa Radio Shield | IDE |
| ------ | --- | ----------------- | --- |
| Nordic | [NRF52840-DK](https://www.nordicsemi.com/Software-and-Tools/Development-Kits/nRF52840-DK) | [sx1262mb2cas](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1262mb2cas) | [Segger Embedded Studio (SES)](https://www.segger.com/downloads/embedded-studio) |
| STMicroeletronics | [STM32-L4](https://www.st.com/en/microcontrollers-microprocessors/stm32l4-series.html) | [sx1276MB1LAS](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276mb1las) | [STM32 系统工作台](https://www.st.com/en/development-tools/sw4stm32.html) |

搭建和测试 FreeRTOS LoRaWAN 应用程序所需的网关硬件：

* [LoRa Raspberry Pi Gateway](https://www.sparkfun.com/products/15336) （请参阅[入门指南](https://cdn.sparkfun.com/assets/3/0/d/e/2/Get_Start_with_RAK2245_Pi_HAT_V2.4R.pdf)，以连接至 The Things Network）


## 总结

[LoRaWAN FreeRTOS Lab 项目](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library)提供了 LoRaWAN 节点的参考实现， 
通过 LoRa 技术使用 FreeRTOS 简化低功率和远距离 IoT 应用程序的开发 
。您可以了解 LoRaWAN 管理器的完整应用程序源代码和详细的 API 引用， 
详情请见 [FreeRTOS LoRaWAN 存储库](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN)。 
我们支持您为这项令人振奋的技术做出贡献，如扩展受支持平台目录和丰富应用示例 
。 

FreeRTOS 是一款 MIT 授权的、适用于微控制器的开源实时操作系统， 
让您可以轻松地编写、部署、保护、连接和管理低功耗的小型边缘设备。您可以 
[从 FreeRTOS.org 或 GitHub (https://github.com/freertos/freertos) 下载源代码](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)开始使用， 
同时了解 FreeRTOS 及其库和演示的更多信息，详情请见  
[FreeRTOS 用户指南](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)。


## 作者：

* Gaurav Gupta（资深合作伙伴解决方案架构师——AWS IoT）
* Paul Butler（资深合作伙伴解决方案架构师——AWS IoT）
* Ravishankar Bhagavandas（软件开发工程师——AWS IoT）


## 作者简介
![](https://secure.gravatar.com/avatar/9f2c9ea3a14d003577468a67df66cb35?s=200&d=mm&r=g) 

Gaurav Gupta 是 AWS IoT 的全球合作伙伴解决方案架构师，他专注于帮助客户和 
合作伙伴，特别是 LoRaWAN 和 Telco 的 IoT 互联推动者，构建他们的产品并与 
 AWS 服务集成。在加入 AWS 之前，他在无线标准、网络架构和一级运营商部署方面 
拥有超过 15 年的经验。他在无线、IoT、云等领域获得了 11 项授权专利，还有几项专利 
有待批准。  
[查看此作者的文章](../author/gvg) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

