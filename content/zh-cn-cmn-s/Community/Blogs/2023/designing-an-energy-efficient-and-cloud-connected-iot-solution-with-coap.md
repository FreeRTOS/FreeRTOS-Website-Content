---
title: 利用 CoAP 设计节能型云连接 IoT 解决方案
date: 2023 年 12 月 12 日
feature: blog
authors:
- mohameda
---
物联网 (IoT) 设备开发过程中需要考虑两个主要因素，分别为 
效率和云兼容性。能耗和数据使用效率 
对于降低运营和维护成本而言非常重要，特别是对于使用电池的蜂窝设备。节能 
是一个复杂的问题，而选择合适的通信协议则是其中一个重要 
方面。一般来说，除了设备管理之外，IoT 设备还必须与 
能够处理和分析数据以生成有用见解的云平台进行通信。


本博客概述了受限制的应用程序协议 (CoAP)，这是一种具有内置效率的通信协议， 
还详细介绍了维护云兼容性的步骤。本博客随后 
会提供示例实现序列，该序列使用 
[1NCE 
FreeRTOS 蓝图](https://github.com/1NCE-GmbH/blueprint-freertos)。


### 受限 IoT 设备中的协议选择


CoAP 采用客户端/服务器通信模型，使用请求/响应模式，并且基于 UDP 协议进行通信。它包括主要的 Web 概念， 
例如[统一资源标识符](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) (URI) 和互联网媒体类型，同时还提供符合 REST 原则的服务， 
因而成为针对受限 IoT 设备进行优化的 HTTP 子集。为实现安全通信， CoAP 可以 
与数据报传输层安全性 (DTLS) 结合使用。 


图 1 和图 2 显示了发送 MQTT 和 CoAP 测试数据包所需的通信阶段。


要使用 MQTT，需要考虑：


1. 三次 TCP 握手（186 字节）。
2. MQTT 连接和[连接确认](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) (ACK)（253 字节）。
3. 包含有效载荷的实际发布数据包（126 字节）。


……总共需要 565 字节。

如果连接未通过周期性 PINGREQ 数据包保持活动状态，则必须重复前两个阶段， 
对于报告间隔较长的受限 IoT 设备来说，实现这一点可能极具挑战性， 
在此期间设备通常需要进入省电模式。不稳定的蜂窝网络覆盖可能会导致 
客户端断开连接，并且还需要启动新连接。



[![MQTT 通信示例](/media/2023/sample-mqtt-comm.png)](/media/2023/sample-mqtt-comm.png)
  

**图 1：MQTT 通信示例** 

借助 CoAP 和无连接 UDP 协议，IoT 设备可以直接发送数据，无需 
建立连接。在此示例中，可以看到测试数据包需要 59 字节， 
如果需要更可靠的通信，可以启用可选的确认功能。这会添加来自服务器的 46 字节 ACK 消息， 
总共需要 105 字节。



[![CoAP 通信示例](/media/2023/sample-coap-comm.png)](/media/2023/sample-coap-comm.png)
  

**图 2：CoAP 通信示例** 

使用无连接协议以及发送更少的数据可以降低 IoT 设备的能耗。 
下图来自在 1NCE 进行的实验，显示使用 CoAP 时能耗最多 
可降低 47.6%。使用 1NCE 软件平台上的 
[Energy Saver 工具](https://help.1nce.com/dev-hub/docs/1nce-os-energy-saver) 还可以
进一步节约能源，该工具可用于最大限度地减少有效载荷大小。



[![能耗比较 (MQTT/CoAP)](/media/2023/energy-consumption.png)](/media/2023/energy-consumption.png)
  

**图 3：能耗比较 (MQTT/CoAP)** 

### 使用更高效的 IoT 协议，同时保持云兼容性


CoAP 可能是受限 IoT 设备的合适选择。然而，它在 IoT 云平台中的采用 
仍然有限，这使得设计可从不同云平台访问的高效 IoT 解决方案 
极具挑战性。


为解决这一问题，1NCE 引入了 [IoT Integrator](https://help.1nce.com/dev-hub/docs/1nce-os-device-integrator)（图 4）。使用此工具，IoT 设备可以 
通过 CoAP、UDP 或轻量级机器对机器 (LwM2M) 等协议向 1NCE 端点发送消息。 
然后，这些消息可以转发到 [AWS IoT Core](https://aws.amazon.com/iot-core)、Webhook 和其他集成。



[![1NCE OS – IoT Integrator](/media/2023/1nce-os-iot.png)](/media/2023/1nce-os-iot.png)
  

**图 4：1NCE OS – IoT Integrator** 

### 1NCE FreeRTOS 蓝图


1NCE FreeRTOS 蓝图包含多个演示，演示 IoT 设备如何 
使用蜂窝连接与 1NCE 的软件平台建立安全高效的通信。


#### 前提条件


* [1NCE SIM 卡](https://1nce.com/en-us/1nce-connect)。
* [B-L475E-IOT01A2 
 STM32 发现套件 IoT 节点](https://www.st.com/en/evaluation-tools/b-l475e-iot01a.html)，[通过 X-NUCLEO-STMODA1 扩展板连接到 BG96（LTE Cat M1/Cat NB1/EGPRS m 调制解调器）](https://www.st.com/en/evaluation-tools/steval-stmodlte.html)。
* [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)
* [STM32 ST-LINK 
 实用程序](https://www.st.com/en/development-tools/stsw-link004.html)


### CoAP 演示组件


为了实现安全通信，该蓝图使用 1NCE SDK 集成（如图 5 所示） 
从 1NCE OS 设备身份验证端点获取 DTLS 凭据。通过 SIM ICCID 识别设备后， 
可以检索凭据。该蓝图还包含使用 PSK 身份验证的 DTLS 的示例 MbedTLS 配置 
。


为获取 DTLS 凭据，应用程序需调用 `os_auth()` 函数。此函数使用 
SDK 中定义的网络接口与 1NCE 设备身份验证端点进行通信， 然后将接收的 
凭据添加到 Mbedtls 配置中。



[![1NCE SDK 集成](/media/2023/1nce-sdk-integration.png)](/media/2023/1nce-sdk-integration.png)
  

**图 5：1NCE SDK 集成
 （点击放大）**

此外，还需要集成可以创建并处理 CoAP 数据包的第三方库。该蓝图 
使用开源 Lobaro CoAP 库，其集成如图 6 所示。 
要在 CoAP 库和 FreeRTOS Secure Socket API 之间添加网络接口，只需定义 
`CoAP_Send` 和 `CoAP_Recv` 函数。这些函数使用已配置用于 DTLS 通信 
并连接到 1NCE 的 CoAP 服务器的套接字句柄。



[![CoAP 库集成](/media/2023/coap-lib-integration.png)](/media/2023/coap-lib-integration.png)
  

**图 6：CoAP 库集成
 （点击放大）**

#### 配置


* **设备**   

 要启用 CoAP 演示，应将定义 "`CONFIG_COAP_DEMO_ENABLED`" 添加到 
 `config_files/aws_demo_config.h` 中。  

 在 `/aws_demos/config_files/nce_demo_config.h` 中，演示配置如下：
	+ `PUBLISH_PAYLOAD_FORMAT`测试有效载荷
	+ `COAP_PORT`对于 DTLS 通信，应设置为 5684
	+ `CLIENT_ICCID`SIM ICCID
	+ `COAP_URI_QUERY`CoAP URI 查询选项， 
	 用于在 AWS IoT Core 中配置 MQTT 发布数据包的主题。
* **云**   

 用户需要从 1NCE 门户设置所需的云集成。例如 
 [AWS 集成设置](https://help.1nce.com/dev-hub/docs/cloud-integrator-aws-configuration)。


#### 运行演示


配置演示并将其闪存到开发板后，设备将向 1NCE OS 注册， 
并且以下事件将显示在门户中。



[![1NCE OS 设备注册](/media/2023/1nce-os-dev-reg.png)](/media/2023/1nce-os-dev-reg.png)
  

**图 7：1NCE OS 设备注册** 

之后，从设备发送的 CoAP 消息将显示在门户上，如下所示：



[\![](/media/2023/coap-msg-sent.png)](/media/2023/coap-msg-sent.png)
  

**图 8：发送到 1NCE OS 的 CoAP 消息** 

该消息还将转发到配置的云集成 (AWS IoT Core)。



[![转发的 MQTT 消息](/media/2023/fwd-mqtt-msg.png)](/media/2023/fwd-mqtt-msg.png)
  

**图 9：转发的 MQTT 消息** 

使用 Energy Saver 工具，应用程序只能发送值更新，无法发送 
整个 JSON 对象，如以下示例所示。



[![有效载荷尺寸缩小](/media/2023/payload-size-reduc.png)](/media/2023/payload-size-reduc.png)
  

**图 10：有效载荷尺寸缩小** 

这有助于降低设备的能耗和数据使用量。要启用此功能， 
请在 `/aws_demos/config_files/nce_demo_config.h` 中定义 "`CONFIG_NCE_ENERGY_SAVER`"，
然后使用函数 `os_energy_save()` 创建有效载荷。


### 其他演示（UDP 和 LwM2M）


该蓝图还包含一个用于基本通信的 [UDP 演示](https://github.com/1NCE-GmbH/blueprint-freertos/tree/main#udp-demo)。此外， 
[LwM2M 演示](https://github.com/1NCE-GmbH/blueprint-freertos/tree/main#lwm2m-demo) 可用于需要更高级 IoT 设备管理的 
应用程序。


### 总结


使用 CoAP 可以大大减少 IoT 设备的能耗和数据使用量。借助 
1NCE OS 中的 IoT Integrator 工具，可以在不影响云兼容性的情况下降低能耗和数据使用量。 
1NCE FreeRTOS 蓝图中的 CoAP 演示为有兴趣测试和评估 CoAP 的开发人员提供了一个起点， 
并展示了如何将 CoAP 与 FreeRTOS 集成，还包括与 1NCE 软件平台的通信， 
以进行设备身份验证以及发送可转发到 
配置的云平台的 CoAP 消息。
