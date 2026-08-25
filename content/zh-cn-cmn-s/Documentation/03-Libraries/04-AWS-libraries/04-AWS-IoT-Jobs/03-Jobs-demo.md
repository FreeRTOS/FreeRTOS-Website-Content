---
title: AWS IoT Jobs 库演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

AWS IoT Jobs 库演示展示了如何
通过 MQTT 连接，连接到 [AWS IoT Jobs 服务](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html)、
从 AWS IoT 检索[作业](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology)，以及在设备上处理作业。该
AWS IoT Jobs 演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
不需要微控制器硬件。该演示与 MQTT 相互身份验证演示一样，使用 TLS 与 AWS IoT MQTT 代理
[建立安全连接](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)。


## 源代码组织

演示项目名为 `jobs_demo.sln`，可在
GitHub 上的 [FreeRTOS-Plus Jobs_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo)
中的以下目录中找到：

```c
FreeRTOS-Plus\Demo\AWS\Jobs_Windows_Simulator\Jobs_Demo
```

## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，因此
请按照为 [TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)提供的说明进行操作
：

1. [安装了必要组件](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   （如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic)（可选）。

3. [设置了 MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   。

应在 Jobs 演示项目中更改上述设置。


### 配置 AWS IoT MQTT 代理连接

在本演示中，您将使用 MQTT 连接到 AWS IoT MQTT 代理。此连接的配置
方式与 [MQTT 相互身份验证演示](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection)中的配置方式相同。


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。
要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 Visual Studio 解决方案文件 `FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/jobs_demo.sln`
   。

2. 在 IDE 的 **“Build”** 菜单中选择 **“Build Solution”**。


## 功能

该演示展示了用于从 AWS IoT 接收作业并在设备上处理作业的工作流程。该演示
是交互式的，要求您使用 AWS IoT 控制台或 AWS CLI 创建作业。
有关创建任务的更多信息，请参阅 *AWS CLI
 命令参考*中的 [create-job](https://docs.aws.amazon.com/cli/latest/reference/iot/create-job.html)。该演示要求作业文件的
"action" 键设置为 "print"，以便将信息打印到控制台。此作业文件的格式
如下：

```c
{
    "action": "print",
    "message": "INSERT_MESSAGE_HERE"
}
```

使用 AWS CLI，可按如下方式创建作业（命令提示符）：

```c
aws iot create-job \
    --job-id t12 \
    --targets arn:aws:iot:us-east-1:1234567890:thing/device1 \
    --document '{"action":"print","message":"hello world!"}'
```

上面使用的实参仅为示例。

该演示还使用将“Action ”键设置为“Publish ”的作业文档
将消息重新发布到主题。作业文件的格式如下：

```c
{
    "action": "publish",
    "message": "INSERT_MESSAGE_HERE",
    "topic": "topic/name/here"
}
```
演示循环，直到收到一个作业文档，并将“action”键设置为“exit”以退出演示。
作业文件的格式如下：

```c
{
    "action: "exit"
}
```


### Jobs 演示的入口点

Jobs 演示入口点函数的源代码可在
GitHub 上的 [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L741-L935) 中找到
。此函数执行以下操作：

1. 使用 `mqtt_demo_helpers.c` 中的辅助函数建立 MQTT 连接。

2. 使用 `mqtt_demo_helpers.c` 中的辅助函数订阅 `NextJobExecutionChanged` API 的 MQTT 主题。
   （主题字符串之前已使用 Jobs 库定义的宏汇编。）

3. 使用 `mqtt_demo_helpers.c` 中的辅助函数发布到 `StartNextPendingJobExecution` API 的 MQTT 主题。
   （主题字符串之前已使用 Jobs 库定义的宏汇编。）

4. 反复调用 `MQTT_ProcessLoop` 以接收传入消息，这些消息将传递给 `prvEventCallback`
   处理。

5. 演示程序接收到退出操作后，
   使用 `mqtt_demo_helpers.c` 中的辅助函数取消订阅 MQTT 主题并断开连接。


### 接收到的 MQTT 消息的回调

此函数从 Jobs 库调用 `Jobs_MatchTopic` 以对传入的 MQTT 消息进行分类。
如果消息类型对应于新作业，则会调用 `prvNextJobHandler`。

函数 `prvNextJobHandler` 及其调用的函数
从 JSON 格式的消息中解析作业文档，并执行作业指定的操作。尤其值得关注
的函数是 `prvSendUpdateForJob`。

此传入消息回调函数的源代码可在
GitHub 上的 [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L622-L718) 中找到
。


### 发送正在运行的作业的更新

函数 `prvSendUpdateForJob` 调用 Jobs 库中的 `Jobs_Update`，
以填充紧随其后的 MQTT 发布操作中使用的主题字符串。

`prvSendUpdateForJob` 函数的源代码可在
GitHub 上的 [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L400-L445) 中找到
。
