---
title: AWS IoT Device Defender 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**注意**：AWS IoT Device Defender 库现提供预配置的示例，
位于 [FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)和 GitHub 上的 [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) 存储库中
。

## 引言

AWS IoT Device Defender 演示向您展示如何
通过 MQTT 连接与 [AWS IoT Device Defender 服务](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html)交互，
提交 device defender 报告
（包括[自定义指标](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html)），
并验证报告是否被接受。AWS IoT Device Defender 演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 构建和评估
。运行此演示不需要微控制器硬件。本演示建立了一个相互
验证身份的安全连接，通过 [TLS](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/03-TLS-terminology) 连接至 AWS IoT MQTT 代理。


## 源代码组织

演示项目名为 `defender_demo.sln`，位于
GitHub 的 [Device_Defender_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo)
存储库中的以下目录中：

```c
FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo
```


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，
因此，请按照
为 [TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)提供的说明来：

1. [安装必要组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   （例如 WinPCap）。

2. [设置静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   。

上述设置应在
Device Defender 演示项目的 [`FreeRTOSConfig.h`](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/VisualStudio_StaticProjects/FreeRTOS-Kernel/FreeRTOSConfig.h) 文件中更改
。


### 配置 AWS IoT MQTT 代理连接

在本演示中，您将使用 MQTT 连接到 AWS IoT MQTT 代理。此连接的配置
与 [MQTT 相互身份验证演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)相同。


## 构建演示项目

演示项目使用
[Visual Studio 免费社区版](https://visualstudio.microsoft.com/vs/community/)。要
构建演示：

1. 从 Visual Studio IDE 中打开 Visual Studio 解决方案
   文件 `FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/defender_demo.sln`
   。

2. 在 IDE 的 **“Build”** 菜单中选择 **“Build Solution”**。


## 功能

本演示向您展示了如何编制 Device Defender 报告并将其从设备发布到 AWS
IoT Device Defender 服务。演示连接到 AWS IoT 代理，从设备收集网络
和[自定义](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html)
指标，通过收集的指标编制 JSON 报告，并发布报告。
演示的结构体见下文。

`prvDefenderDemoTask()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L721-L966) 文件
。

此屏幕截图显示演示正确执行时的预期输出：

[\![](/media/2020/Defender-Terminal-Output.png)](/media/2020/Defender-Terminal-Output.png)
*点击放大*


### 订阅 Defender 主题

函数 `prvSubscribeToDefenderTopics()` 在下列情况下订阅 MQTT 主题以接收响应：

* 接受其已发布的 Device Defender 报告。

  宏 `DEFENDER_API_JSON_ACCEPTED` 用于构建主题字符串。

* 已发布的 Device Defender 报告被拒绝。

  宏 `DEFENDER_API_JSON_REJECTED` 用于构建主题字符串。


`prvSubscribeToDefenderTopics()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L636-L668) 文件
。


### 收集设备指标

函数 `prvCollectDeviceMetrics()` 收集网络指标（通过
`metrics_collector.h` 中定义的函数）以及自定义指标。所收集的网络指标是：

* 发送和接收的字节和数据包数
* 已开放的 TCP 端口
* 已开放的 UDP 端口
* 已建立的 TCP 连接

收集的自定义指标为：

* 堆栈高水位线（带类型号）
* 设备的任务 ID（带类型编号列表）

`prvCollectDeviceMetrics()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L467-L601rel=) 文件
。


### 生成 Device Defender 报告

函数 `prvGenerateDeviceMetricsReport()` 生成 Device Defender 报告。它在
`report_builder.h` 中定义。函数将网络指标和缓冲区作为输入，以创建 JSON
文档，其格式为 AWS IoT Device Defender 服务预期的格式，并将其写入指定的缓冲区
。  JSON 文档的格式，即 AWS IoT Device Defender 服务预期的格式
指定于[此处](https://docs.aws.amazon.com/iot/latest/developerguide/detect-device-side-metrics.html)。

`prvGenerateDeviceMetricsReport()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L604-L633) 文件
。


### 发布 Device Defender 报告

函数 `prvPublishDeviceMetricsReport()` 在适当的 MQTT 主题上
发布 Device Defender 报告。在 JSON 中，使用宏 `DEFENDER_API_JSON_PUBLISH` 编制报告。

`prvPublishDeviceMetricsReport()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L692-L699) 文件
。


### 处理响应的回调

函数 `prvPublishCallback()` 处理传入的 MQTT 消息。它使用
Device Defender 库中的 `Defender_MatchTopic` API，以检查传入的 MQTT 消息是否来自
AWS IoT Device Defender 服务。如果消息来自服务，它会解析收到的 JSON 响应，
并提取报告 ID。然后它会验证报告 ID 是否与 Device Defender 报告中发送的 ID 相同
。

`prvPublishCallback()` 函数的源代码位于
Github 上的 [DefenderDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Defender_Windows_Simulator/Device_Defender_Demo/DemoTasks/DefenderDemoExample.c#L380-L464) 文件
。
