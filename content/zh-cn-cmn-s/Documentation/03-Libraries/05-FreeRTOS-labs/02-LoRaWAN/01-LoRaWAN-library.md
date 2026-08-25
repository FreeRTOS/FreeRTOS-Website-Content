---
title: LoRaWAN
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意**：在 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 中提供 FreeRTOS LoRaWAN 演示项目，
供社区成员使用和参考。此演示虽然功能完善，
但可能并不符合我们的生产代码标准。它可从
GitHub 上的 [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) 存储库中获取
。


## 引言

[LoRa](https://en.wikipedia.org/wiki/LoRa)（长距离的简称）是一种扩频调制技术，
衍生自啁啾扩频（CSS）技术。LoRaWAN
由 [LoRa 联盟](https://lora-alliance.org/)开发，是 LoRa 网络的系统架构和通信协议规范。
LoRaWAN 是一种媒体访问控制 (MAC) 层协议，使 LoRa 在更广泛的应用程序中得以实现。

LoRa 联盟定义了 LoRaWAN 的网络层和系统架构。图 1
描绘了 LoRaWAN 连接流程，
不同组件将终端节点连接到云端和应用服务器。

[\![](/media/2020/Figure-1-2.png)](/media/2020/Figure-1-2.png)
*图 1 - LoRaWAN 网络架构。点击放大。*

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
DevNonce、根密钥 (AppKey、NwkKey ) 在本地派生会话密钥，
使得安全密钥不会通过无线交换。JS 向 LNS 传递网络会话密钥并向 AS 传递应用程序会话密钥。
终端设备安全地存储各自的根密钥，而等效的匹配密钥则安全地
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
请参阅[此处](https://resources.lora-alliance.org/document/lorawan-specification-v1-0-3)。


## FreeRTOS的 LoRaWAN 堆栈

FreeRTOS 为嵌入式软件开发人员提供了诸多好处。[继续阅读](/Why-FreeRTOS/FAQs/What-is-this-all-about#why-use-an-rtos)。

如图 2 所示，FreeRTOS 的 LoRaWAN 堆栈使用 LoRaWAN 管理任务对 LoRaWAN 网络的
时序约束进行抽象，从而为应用程序层提供更简单的编程模型。
它将处理无线中断和 MAC 层事件的问题与用户应用程序分开。
这使得应用程序任务能够顺序执行，具有更模块化。这也允许拥有
定义良好的 Helper API。Helper API 可以在不同的应用程序中复用，例如阻塞 API 可以用于
加入网络、发送和接收原始数据。如果设备不支持安全配置，
还可以使用用于配置和获取加入证书的辅助函数。对于当前版本，
仅支持 A 类设备功能。未来版本将支持 B 类和 C 类设备，
同时支持应用程序在不同的操作类型之间切换。堆栈还暴露了
无线硬件抽象层 (HAL)，该层为应用程序提供了直接控制 LoRa 无线模块或调制解调器的能力
。HAL 可以用于一个或多个 LoRa 无线电收发器或 LoRa 无线电调制解调器。

FreeRTOS 的 LoRaWAN 堆栈使用 LoRaMac-Node，这是 Semtech 对 LoRaWAN 
终端设备协议规范的开源实现。此堆栈实现了 LoRaWAN 的 1.0.3 版规范。了解更多有关 LoRaMac-Node 的详细信息，
请访问 [Semtech 的文档](http://stackforce.github.io/LoRaMac-doc/)。
FreeRTOS 支持 LoRaWAN 的源代码可在[此处](https://github.com/Lora-net/LoRaMac-node)获得。

[\![](/media/2020/Figure-2.png)](/media/2020/Figure-2.png)
*图 2 - FreeRTOS 中的 LoRaWAN 堆栈。点击放大。*
