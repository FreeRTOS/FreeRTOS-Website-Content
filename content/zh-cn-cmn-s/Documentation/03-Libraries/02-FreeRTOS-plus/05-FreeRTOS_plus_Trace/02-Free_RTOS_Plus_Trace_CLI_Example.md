---
title: FreeRTOS-Plus-Trace 和 FreeRTOS-Plus-CLI 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 适用于 FreeRTOS 的 Percepio View
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/01-Percepio_View
  - title: Tracealyzer™
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


使用 [FreeRTOS Win32 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)


### 下载

本页显示的示例
位于官方 [FreeRTOSzip 文件下载内容](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的以下目录中：

FreeRTOS-Plus/Demo/FreeRTOS_Plus_CLI_with_Trace_Windows_Simulator


### 简介

此页面描述了一个简单 FreeRTOS 示例，它运行
于FreeRTOS Win32 模拟器中。
使用该模拟器可轻松
在标准台式电脑上评估 FreeRTOS-Plus-CLI 和 FreeRTOS-Plus-Trace，此过程仅使用
免费开发工具，且无需
连接任何外部硬件。

为尽量简化操作，FreeRTOS-Plus-CLI 命令行
界面是通过默认 Windows 环回 IP 地址 127.0.0.1 上的 UDP 套接字访问的。
使用环回适配器允许
在单台计算机上使用演示，而不需要实时网络连接。

实现下列命令：

+ *追踪*

  追踪命令用于启动和停止追踪记录。如果只输入一个参数，FreeRTOS-Plus-CLI
  将只处理这条命令。  要开始 FreeRTOS-Plus-Trace 记录，
  请输入："trace start"。要停止 FreeRTOS-Plus-Trace 记录，请输入："trace stop"。当追踪停止时，
  追踪缓冲区中的结果将自动保存到主计算机的硬盘中。查看追踪的说明，
  请参阅本页后续内容。

+ *echo_parameters*

  这演示了如何创建和实现一个接受可变数量参数的命令。
  FreeRTOS-Plus-CLI 不会检查所提供的参数的数量，
  命令的执行只是简单的回传参数，一次一个。例如，如果用户输入 “echoo_parameters one two
  three four"，那么生成的结果将是：参数是 1: one 2: two 3: three 4: four

+ *echo_3_parameters*

  这演示了如何创建一条需要精确参数数量的命令。该命令将不会
  被 FreeRTOS-Plus-CLI 接受，除非只提供三个参数。当命令被接受时，
  命令的实现会以类似于上文详述的 echoo_parameters 命令的方式
  回声显示所有三个参数。

+ *run-time-stats*

  [显示一个表格](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)，
  其中每一行都显示单个任务在运行状态下花费的时间。也就是说，为每个任务分配了多少执行时间。
  绝对值和相对值都会显示，
  不过在使用 Windows 模拟器时，绝对时间没有单位。


### 演示功能

使用两项任务和一个队列生成一个简单的执行
模式，可在 FreeRTOS-Plus-Trace 图形界面中查看。

低优先级队列发送任务会反复向队列发送消息。
较高优先级队列接收任务会反复尝试读取
队列中的消息，从而在没有可用消息时阻止队列读取操作
。下面提供了对结果执行
模式的说明。

它还会创建一个追踪监控任务，当它确定追踪记录器的状态
自上次执行以来已更改时，
会令该任务打印一条消息。

应注意的是，由于使用 Windows 模拟器，
在应用程序运行时显示并记录在追踪日志中的计时信息
没有有意义的单位。


### 构建和执行演示

1. 确保已安装 Microsoft Visual C++。
   [免费 Express 版本](https://visualstudio.microsoft.com/vs/community/)
   可以使用。

2. Visual C++ 解决方案文件名为 FreeRTOS_Plus_CLI_with_Trace.sln，
   位于下载内容的 FreeRTOS-Plus/Demo/FreeRTOS_Plus_CLI_with_Trace_Windows_Simulator
   目录中。双击文件打开 Visual C++，或者
   在 Visual C++ IDE 中打开文件。

   ![在编译器开发工具中查看的 RTOS 项目](/media/2018/RTOS_project_viewed_in_dev_tool_editor.png)
   <br />
   *在 Visual C++ IDE 中查看的 RTOS 项目*

   在解决方案资源管理器中：

   * 实现演示应用程序的源文件列于 Demo App Source 文件夹中。
   * 实现 FreeRTOS-Plus-CLI 功能的源文件位于
     FreeRTOS-Plus/FreeRTOS-Plus-CLI 文件夹中。
   * 实现 FreeRTOS-Plus-Trace 记录器功能的源文件位于
     FreeRTOS-Plus/FreeRTOS-Plus-Trace 文件夹中。
   * 实现 RTOS 功能的源文件列于 FreeRTOS 文件夹中。

3. 生成项目，然后执行项目。（F7 将生成项目，F5 将执行项目）。


### 访问命令控制台

命令控制台使用 IP 地址 127.0.0.1 和端口 5001 上的 UDP 套接字接收命令
行输入，并使用同一 IP 地址和端口 5002 上的 UDP 套接字输出。UDP 控制台
程序，例如[免费 YAT 实用程序](http://sourceforge.net/projects/y-a-terminal/)，
可用作 UDP 接口。请注意，127.0.0.1 是环回 IP 地址，因此
不需要实时网络连接。

![所需的 UDP 命令控制台配置](/media/2018/YAT-console-configuration.jpg)
<br />
*所需的 YAT 终端设置*


### 创建 FreeRTOS-Plus-Trace 记录

创建追踪记录：

1. 测试 UDP 终端与正在运行的应用程序之间的 UDP 连接，
   方法为运行 "task-stats" 和 "run-time-stats"
   命令。

2. 输入 "trace start" 命令启动追踪记录器
   （在 UDP 终端中输入命令）。让
   记录运行大约五到十秒钟，然后
   通过输入 "trace stop" 命令结束记录。

   ![从控制台启动并停止 RTOS 追踪后的快照](/media/2018/command-line-input-and-output.jpg)
   <br />
   *从 UDP 控制台启动并停止 RTOS 追踪后的快照*


### 在 FreeRTOS-Plus-Trace 中查看追踪记录

要打开并查看追踪记录，请执行下列操作：

1. [如果尚未安装 FreeRTOS-Plus-Trace](http://percepio.com/tz/freertostrace/)，请从 Percepio 网站进行下载
   。

2. 在 FreeRTOS-Plus-Trace 应用程序中打开追踪文件。
   追踪文件将作为
   FreeRTOSPlusTrace.dump 保存在包含
   Visual Studio 项目的目录中。

3. 追踪数据将显示在主 FreeRTOS+Trace
   窗口中。向下滚动追踪显示，直到您注意到
   屏幕左侧的 "Tx" 和 "Rx" 标记。这些是
   队列发送和队列接收任务
   分别执行的时间。放大该区域将
   生成类似于下方屏幕截图的显示。请注意，
   该屏幕截图中所有可视性过滤器均已勾选，但并非其中所有过滤器
   在免费 FreeRTOS-Plus-Trace 版本中都可用。

   ![在 FreeRTOS-Plus-Trace 中查看 RTOS 追踪](/media/2018/Viewing-the-RTOS-trace-in-FreeRTOS-Trace.jpg)
   <br />
   *在带有解释性注释的 FreeRTOS-Plus-Trace 中查看所记录的 RTOS 追踪*

   上图已使用一些绿色数字进行注释，以突出显示
   重点。具体请参阅上图：

   1. 在 (1) 处，CLI 任务正在运行。在实际方案中，在真正的
      硬件上，CLI 任务仅在有要处理的输入时
      执行。在此模拟环境中，TCP/IP 堆栈不
      允许阻止，因此 CLI 任务始终可用于
      调度器。
   2. 在 (2) 处，Tx 任务（队列发送任务）取消阻止，因为
      此时应向队列发送另一条消息。Tx 任务
      抢占 CLI 任务。
   3. 在 (3) 处，Tx 任务调用 xQueueSend() 发送消息给
      名为 DemoQ 的队列。优先级较高的 Rx 任务（队列接收任务）被阻止
      在队列中，等待消息到达。因此现在它取消阻止并
      抢占 Tx 任务。
   4. 在 (4) 处，Rx 任务再次调用 xQueueReceive()，但队列
      再次为空，因此 Rx 任务重新进入已阻止状态（由
      追踪视图中 xQueueReceive() 标签的红色表示），允许
      Tx 任务再次进入运行状态。
   5. 在 (5) 处，Tx 任务调用 vTaskDelayUntil() 进入已阻止
      状态，直到它再次向队列发送消息
      为止。
   6. 在 (6) 处，空闲任务正在运行。


### 更多

这个简单的示例只演示了基本功能。应用程序
FreeRTOS-Plus-Trace 下载内容中包含更全面的 FreeRTOS
Windows 模拟器项目以及预先记录的示例追踪日志文件。
您可访问 [Percepio 网站](http://percepio.com/tz/freertostrace/)了解更多
信息。
