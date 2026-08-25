---
title: AWS IoT Device Shadow 操作演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 引言

本演示说明如何使用 AWS IoT Device Shadow 库来连接 AWS 设备 Shadow 服务。
它使用 [coreMQTT 库](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)通过 TLS（相互身份验证）
与 AWS IoT MQTT 代理建立 MQTT 连接，并使用 [coreJSON 解析器](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)解析
从 AWS Shadow 服务接收的 shadow 文档。该演示展示了一些基本的 shadow 操作，
例如如何更新 shadow 文档以及如何删除 shadow 文档。该演示还展示了如何向 MQTT 库注册回调函数，
以处理 shadow `/update`
和 `/update/delta` 消息等消息（由 AWS Device Shadow 服务发送）。

本演示仅用于学习练习，因为请求更新 Shadow 文档（状态）和更新
响应是由同一应用程序完成的。在实际生产场景中，外部应用程序（例如，
在用户的手机上运行的应用程序）会请求远程更新设备状态，
即使设备当前未连接。连接后，
设备将确认更新请求。

此演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
无需任何特定 MCU 硬件。


### 源代码组织

演示项目名为 `shadow_device_operations_demo.sln`，可在
GitHub 上的 [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) 存储库中的以下目录中找到：

```c
FreeRTOS-Plus\Demo\AWS\Device_Shadow_Windows_Simulator\Device_Shadow_Demo
```


### 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，因此
请按照
[TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)的说明操作：

1. [安装了必要组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   （如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置了 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   。

5. **（最重要的是！）** [在尝试运行 Shadow 演示之前，请先测试网络连接](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   。

所有这些设置都应在 Shadow 演示项目中设置。


### 配置 AWS IoT MQTT 代理连接

在本演示中，您将使用 MQTT 连接到 AWS IoT MQTT 代理。此连接以与
[MQTT 相互身份验证演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)的相同配置方式配置。


### 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 Visual Studio 解决方案
   文件 `FreeRTOS-Plus\Demo\AWS\Device_Shadow_Windows_Simulator\Device_Shadow_Demo\shadow_main_demo.sln`
   。

2. 在 IDE 的 '**build**'（构建）菜单中选择 '**build solution**' （构建解决方案）。


### 功能

该演示创建了一个单个应用程序任务，该任务通过一系列示例循环，演示
shadow `/update` 和 `/update/delta` 回调，以模拟切换远程 IoT 设备的状态。它发送
带有新 `desired` 状态的 shadow 更新，并等待 IoT 设备更改其 `reported` 状态
（根据新 `desired` 状态更改。）此外，还使用 shadow `/update` 回调打印
不断变化的 shadow 状态。此演示还使用安全的 MQTT 连接到 AWS IoT MQTT 代理，
并假设设备 shadow 处于 `powerOn` 状态。默认情况下，演示使用经典的未命名
shadow。可定义 `democonfigSHADOW_NAME` 以选择命令的 shadow（可选）。

演示执行以下操作：

1. 使用 `shadow_demo_helpers.c` 中的辅助函数建立 MQTT 连接。

2. 使用 Device Shadow 库定义的宏，为 IoT 设备 shadow 操作汇编 MQTT 主题字符串
   。

3. 发布到用于删除设备 Shadow 的 MQTT 主题，以删除任何现有设备 Shadow。

4. 订阅 `/update/delta`/`/update/accepted` 和 `/update/rejected` 的 MQTT 主题
   （使用 `shadow_demo_helpers.c` 中的辅助函数）。

5. 使用 `shadow_demo_helpers.c` 中的辅助函数发布所需的 `powerOn` 状态。这会导致
   `/update/delta` 消息发送到设备。

6. 在 `prvEventCallback` 中处理传入 MQTT 消息，
   并通过使用由 Device Shadow 库定义的函数 (`Shadow_MatchTopicString`) 确定消息是否和设备 shadow 相关。
   如果消息是设备 shadow `/update/delta` 消息，则主演示函数将发布第二条
   消息以更新报告状态为 `powerOn`。如果收到 `/update/accepted` 消息，
   请验证其是否具有与先前在更新消息中发布的客户端令牌相同的客户端令牌。这将标志着
   演示结束。

演示的结构体
可在 GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L811-L1128) 中找到
。

此屏幕截图显示演示正确执行时的预期输出：

[\![](/media/2020/Shadow-Demo-Sucess.png)](/media/2020/Shadow-Demo-Sucess.png)
*点击放大*


#### *连接到 AWS IoT MQTT 代理*

为了连接到 AWS IoT MQTT 代理，我们使用与 MQTT 相互身份验证演示中的 `MQTTConnect()`
[相同的方法](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)。


#### *删除 Shadow 文档*

要删除 Shadow 文档，请使用 Device Shadow 库定义的宏以空消息调用 `xPublishToTopic`
。这会使用 `MQTT_Publish` 发布到 `/delete` 主题。演示
如何在 `prvShadowDemoTask` 中完成此操作的示例可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L871-L877) 中找到
。


#### *订阅 Shadow 主题*

订阅设备 Shadow 主题以接收来自 AWS IoT 代理有关 Shadow 更改的通知
。Device Shadow 主题由 Device Shadow 库中定义的宏汇编。展示
如何在 `prvShadowDemoTask` 函数中完成此操作的示例可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L918-L937) 中找到
。


#### *发送 Shadow 更新*

为发送 shadow 更新，该演示使用 Device Shadow 库定义的宏，通过 JSON 格式的消息调用 `xPublishToTopic`
。这会使用 `MQTT_Publish` 发布到 `/delete` 主题。展示
如何在 `prvShadowDemoTask` 函数中完成此操作的示例可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L1019-L1029) 中找到
。


#### *处理 Shadow Delta 消息和 Shadow Update 消息*

注册到 [coreMQTT 客户端库](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)的用户回调函数
（使用函数 [`MQTT_Init()`](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#mqttinit) 完成注册）
将向我们通报传入数据包事件。示例回调函数的代码可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L687-L768) 中找到
。

回调函数确认传入数据包的类型为 `MQTT_PACKET_TYPE_PUBLISH`，并使用
Device Shadow 库 API `Shadow_MatchTopic` 确认传入的消息为 shadow 消息。

如果传入消息是类型为 `ShadowMessageTypeUpdateDelta` 的 shadow 消息，则
调用 `prvUpdateDeltaHandler` 以处理此消息。处理程序 `prvUpdateDeltaHandler` 使用
[coreJSON 库](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) 解析消息以获取 `powerOn` 的增量值
状态，并将其与本地维护的当前设备状态进行比较。如果这些值不同，
则会更新本地设备状态，以反映来自 shadow 文档的 `powerOn` 状态的新值
。`prvUpdateDeltaHandler` 的源代码可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L475-L591) 中找到
。

如果传入消息是类型为 `ShadowMessageTypeUpdateAccepted` 的 shadow 消息，则
调用 `prvUpdateAcceptedHandler` 以处理此消息。处理程序 `prvUpdateAcceptedHandler`
使用 [coreJSON 库](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)解析消息，以从消息中获取 `clientToken`
。该处理程序函数会检查 JSON 消息中的客户端令牌
是否与应用程序使用的客户端令牌相匹配。如果不匹配，该函数将记录一条警告消息。
`prvUpdateAcceptedHandler` 的代码可在
GitHub 上的 [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L595-L678) 中找到
。
