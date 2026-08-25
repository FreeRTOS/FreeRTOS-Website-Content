---
title: 蜂窝接口演示（双向验证）
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

FreeRTOS 提供了一套专为 IoT 应用程序设计的网络堆栈。应用程序可以访问
不同级别的通信协议（MQTT、HTTP、安全套接字等）。以太网、Wi-Fi 和 BLE 等
常见连接技术已与
FreeRTOS 的网络堆栈集成，还预集成了多种[微控制器和模块](https://devices.amazonaws.com/search?page=1&sv=freertos)
。

本项目中的演示将展示如何使用蜂窝连接与 MQTT 代理
（例如 AWS IoT Core）建立经过双向验证的 MQTT 连接。演示使用的
[蜂窝接口库](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) 是某外部项目的子模块
。该蜂窝接口库通过统一 API 提供了
一些常用蜂窝调制解调器的功能。

- [Quectel BG96](https://www.quectel.com/product/lpwa-bg96-cat-m1-nb1-egprs)
- [Sierra Wireless HL7802](https://www.sierrawireless.com/iot-modules/lpwa-modules/hl7802/)
- [U-Blox Sara-R4](https://www.u-blox.com/en/product/sara-r4-series)

FreeRTOS 的 MQTT 和 HTTP 库使用
抽象的[传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface) 以通用方式发送/接收数据。本项目中的
演示基于蜂窝接口库提供的统一 API，
提供了该传输接口的[实现](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/using_mbedtls/using_mbedtls.c)
。

## 硬件设置

本项目中的演示可以在
[FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) 中运行。
您需要一台 Windows 计算机和一个受支持的蜂窝调制解调器来运行演示。构建演示时，需要使用
Visual Studio，例如社区免费版 [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
。

FreeRTOS Windows 模拟器使用 COM 端口与蜂窝模块进行通信。
请按照如下步骤设置蜂窝模块通信。

1. 将蜂窝模块连接到计算机。大多数蜂窝开发套件都有 USB 连接器，
   因此只需将其连接到计算机的 USB 端口，然后在 Windows 设备管理器中查找 COM 端口即可。
   例如，如下图所示，连接调制解调器时，您会看到新的 COM69 出现。如果
   蜂窝开发套件没有 USB 接口，请使用
   [如此处所示](https://www.amazon.com/Serial-Usb-Adapter/s?k=Serial+To+Usb+Adapter) 的 USB 适配器。

   ![屏幕截图 1：Windows 设备管理器中的蜂窝模块 COM 端口](fr-content-src/uploads/2020/12/Screenshot-1.png)

2. 使用 [Putty](https://www.putty.org/) 或其他终端工具验证与蜂窝模块的连接。
   。请参阅蜂窝模块手册，了解波特率、奇偶校验和流控制等设置。在
   终端工具中，输入 "ATE1"。调制解调器会返回 "OK"。您可能还会看到 "ATE1" 的回显，
   具体取决于您的调制解调器设置。输入 "AT"，调制解调器会返回 "OK"。

   ![屏幕截图 2：在 Putty 中使用 AT 命令测试 COM 端口](fr-content-src/uploads/2020/12/Screenshot-2.png)

## 组件和接口

本项目使用其他 GitHub 项目中的五 (5) 个子模块，
如下图黄色方框所示。

![图 1：组件和接口](fr-content-src/uploads/2020/12/Figure-1.png)

- [蜂窝演示应用程序](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common) 的
  功能与
  [coreMQTT 演示](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth) 中大致相同，
  只是新增了将蜂窝网络设置为传输方式的逻辑。（最初的 coreMQTT 演示专为
  FreeRTOS Windows 模拟器上的 Wi-Fi 设计。）

- [传输接口](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/using_mbedtls/using_mbedtls.c)
  是 MQTT 库（[coreMQTT](https://freertos.o/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 项目的子模块）的必要组件，
  用于发送和接收数据包。

- [TLS 移植接口](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Utilities/mbedtls_freertos/mbedtls_freertos_port.c)
  是 mbedTLS 库在 FreeRTOS 上运行所需的组件。

- [通信接口](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c)
  被蜂窝接口库用来通过 UART 连接与蜂窝调制解调器进行通信。

## 开发者参考和 API 文档

请参阅[托管 doxygen](https://freertos.org/Documentation/api-ref/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)。

## 源代码组织

Visual Studio 的演示项目文件名为 _\<xyz>__mqtt*mutual_auth_demo.sln，其中 _xyz*
是蜂窝调制解调器的名称。这些文件位于
GitHub 上 [FreeRTOS_Cellular_Interface_Windows_Simulator](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator)
存储库的以下目录：

1. [MQTT_Mutual_Auth_Demo_with_BG96](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_BG96)

2. [MQTT_Mutual_Auth_Demo_with_HL7802](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_HL7802)

3. [MQTT_Mutual_Auth_Demo_with_SARA_R4](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_SARA_R4)

```c
./FreeRTOS-Plus
├── Demo
│   ├── FreeRTOS_Cellular_Interface_Windows_Simulator
│   │   ├── Common
│   │   │   ├── FreeRTOSConfig.h
│   │   │   ├── FreeRTOSIPConfig.h
│   │   │   ├── MutualAuthMQTTExample.c
│   │   │   ├── cellular_platform.c
│   │   │   ├── cellular_platform.h
│   │   │   ├── cellular_setup.c
│   │   │   ├── comm_if_windows.c
│   │   │   ├── core_mqtt_config.h
│   │   │   ├── main.c
│   │   │   └── mbedtls_config.h
│   │   ├── MQTT_Mutual_Auth_Demo_with_BG96 ( demo project for Quectel BG96 )
│   │   │   ├── WIN32.vcxproj
│   │   │   ├── WIN32.vcxproj.filters
│   │   │   ├── WIN32.vcxproj.user
│   │   │   ├── cellular_config.h
│   │   │   ├── demo_config.h
│   │   │   └── mqtt_mutual_auth_demo_with_bg96.sln
│   │   ├── MQTT_Mutual_Auth_Demo_with_HL7802 ( demo project for Sierra Wireless HL7802 )
│   │   └── MQTT_Mutual_Auth_Demo_with_SARA_R4 ( demo project for U-Blox Sara-R4 )
│   │
├── Source
│   ├── Application-Protocols
│   │   ├── coreMQTT ( submodule : coreMQTT )
│   ├── FreeRTOS-Cellular-Interface ( submodule : FreeRTOS-Cellular-Interface )
│   ├── FreeRTOS-Cellular-Modules
│   │   ├── bg96 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-Quectel-BG96 )
│   │   ├── hl7802 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-Sierra-Wireless-HL7802 )
│   │   └── sara-r4 ( submodule : Lab-FreeRTOS-Cellular-Interface-Reference-ublox-SARA-R4 )
│   ├── Utilities
│   │   ├── backoff_algorithm ( submodule : backoffAlgorithm )
│   │   ├── logging
│   │   ├── mbedtls_freertos
│   │   │   ├── mbedtls_bio_freertos_cellular.c
│   │   │      └── ( code for adapting mbedtls with cellular socket )
│   │   │   ├── mbedtls_bio_freertos_plus_tcp.c
│   │   │   ├── mbedtls_freertos_port.c
│   │   │   └── threading_alt.h
├── ThirdParty
│   ├── mbedtls ( submodule : mbedtls )

```

## 配置应用程序设置

### 配置蜂窝网络

在蜂窝配置
[cellular_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator)（位于
"MQTT_Mutual_Auth_Demo_with__\<cellular_module>_/cellular_config.h"）中，
必须根据您的网络环境修改以下参数。

| 配置                | 描述                                                                                                                                          | 值                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| CELLULAR_COMM_INTERFACE_PORT | 蜂窝通信接口利用计算机上的 COM 端口<br/> 与 Windows 模拟器上的蜂窝模块通信。 | 连接到蜂窝模块的 COM 端口。       |
| CELLULAR_APN                 | 网络注册的默认 [APN](https://en.wikipedia.org/wiki/Access_Point_Name)。                                                         | 根据您的网络运营商指定此值。 |
| CELLULAR_PDN_CONTEXT_ID      | 蜂窝网络的 PDN 上下文 ID。                                                                                                             | 默认值为 CELLULAR_PDN_CONTEXT_ID_MIN。     |
| CELLULAR_PDN_CONNECT_TIMEOUT | 网络注册的 PDN 连接超时。                                                                                                        | 默认值为 100000 毫秒。             |

### 配置 MQTT 代理

有关连接到 MQTT 代理的配置，详见演示配置
[demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator)（位于
"MQTT_Mutual_Auth_Demo_with__\<cellular_module>_/demo_config.h"）。请参阅
[MQTT 双向验证演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) 文档，
了解更多信息。

### 配置 COM 端口设置

有关 COM 端口设置，请参阅蜂窝模块文档。如有必要，请更新
[comm_if_windows.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/comm_if_windows.c) 中的
设置。

### 配置其他子模块

"FreeRTOSConfig.h"、"mbedtls_config.h" 和 "core_mqtt_config.h"（位于
"MQTT_Mutual_Auth_Demo_with__\<cellular_module>_）包含其相应
子模块的配置。

## 演示执行步骤流程

演示应用程序执行三类操作。搜索
下图中的函数名称，即可在源代码中找到执行这些操作的确切位置。

1. 注册蜂窝网络
   。（请参阅 [cellular_setup.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/Common/cellular_setup.c)。）

2. 使用 MQTT 代理与 AWS IoT 建立安全连接
   。（请参阅 [using_mbedtls.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Source/Application-Protocols/network_transport/using_mbedtls/using_mbedtls.c)。）

3. 执行 MQTT
   操作。（请参阅 [MutualAuthMQTTExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator/MQTT_Mutual_Auth_Demo_with_BG96/DemoTasks/MutualAuthMQTTExample.c)。）

下图说明了演示应用程序与其他组件之间的交互。

[\![演示流程](fr-content-src/uploads/2020/12/cellular_demo_sequence-1.png) **演示流程 点击图像放大**](fr-content-src/uploads/2020/12/cellular_demo_sequence-1.png)

## 构建并运行 MQTT 双向验证演示

1. 在 Visual Studio 中，打开与您的蜂窝调制解调器匹配的 mqtt_mutual_auth_demo.sln 项目
   。

2. 设置 Amazon Web Services 账号，并在 AWS IoT Core 上将设备注册为 AWS IoT 设备。
   请参阅 coreMQTT 双向验证演示中的[使用 AWS IoT 消息代理](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection)，
   了解详情。

3. 配置设备名称、AWS IoT 设备端点，并设置凭据
   （在 [demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator) 中，该文件位于
   "MQTT_Mutual_Auth_Demo_with__\<cellular_module>_/demo_config.h"）。

4. 编译并运行。

控制台中成功执行 bg96_mqtt_mutual_auth_demo.sln 项目的输出结果如下所示。

```c
[INFO] [CELLULAR] [commTaskThread:287] Cellular commTaskThread started
>>>  Cellular SIM okay  <<<
>>>  Cellular GetServiceStatus failed 0, ps registration status 0  <<<
>>>  Cellular module registered  <<<
>>>  Cellular module registered, IP address 10.160.13.238  <<<
[INFO] [MQTTDemo] [prvConnectToServerWithBackoffRetries:583] Creating a TLS connection to xxxxx-ats.iot.us-west-2.amazonaws.com:8883.

[INFO] [MQTTDemo] [MQTTDemoTask:465] Creating an MQTT connection to xxxxx-ats.iot.us-west-2.amazonaws.com.

[INFO] [MQTTDemo] [prvCreateMQTTConnectionWithBroker:683] An MQTT connection is established with XXXXXXXXXX-ats.iot.us-west-2.amazonaws.com.
[INFO] [MQTTDemo] [prvMQTTSubscribeWithBackoffRetries:741] Attempt to subscribe to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [prvMQTTSubscribeWithBackoffRetries:748] SUBSCRIBE sent for topic testClient13:24:47/example/topic to broker.


[INFO] [MQTTDemo] [prvMQTTProcessResponse:872] Subscribed to the topic testClient13:24:47/example/topic with maximum QoS 1.

[INFO] [MQTTDemo] [MQTTDemoTask:479] Publish to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [MQTTDemoTask:485] Attempt to receive publish message from broker.

[INFO] [MQTTDemo] [prvMQTTProcessResponse:853] PUBACK received for packet Id 2.

[INFO] [MQTTDemo] [MQTTDemoTask:490] Keeping Connection Idle...


[INFO] [MQTTDemo] [MQTTDemoTask:479] Publish to the MQTT topic testClient13:24:47/example/topic.

[INFO] [MQTTDemo] [MQTTDemoTask:485] Attempt to receive publish message from broker.

[INFO] [MQTTDemo] [prvMQTTProcessIncomingPublish:908] Incoming QoS : 1

[INFO] [MQTTDemo] [prvMQTTProcessIncomingPublish:919]
Incoming Publish Topic Name: testClient13:24:47/example/topic matches subscribed topic.
Incoming Publish Message : Hello World!

```
