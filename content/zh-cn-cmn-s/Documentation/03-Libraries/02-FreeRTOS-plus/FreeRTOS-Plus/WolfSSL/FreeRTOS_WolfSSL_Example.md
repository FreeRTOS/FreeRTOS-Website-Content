---
title: FreeRTOS-Plus WolfSSL 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

可执行示例


### 下载

本页显示的示例
位于官方 [FreeRTOS zip 文件下载内容](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的以下目录中：  

FreeRTOS-Plus/Demo/FreeRTOS_Plus_WolfSSL_Windows_Simulator


### 简介

本页展示的项目演示了 WolfSSL
用于 TCP/IP 客户端与 TCP/IP 服务器之间的安全通信的情况。
 
  
### 硬件设置

本演示使用 [FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。
该模拟器提供了极其方便的独立评估环境，
因为它可以用微软免费的 [Visual C ++ Express](https://visualstudio.microsoft.com/vs/community/) 工具来构建，
无需使用任何外部硬件。然而，与
使用真正的 FreeRTOS 移植不同的是，FreeRTOS Windows 模拟器移植并不
显示实时行为。

由于 FreeRTOS 模拟器是在 Windows 环境下运行的，演示应用程序
也可以访问并使用 Windows TCP/IP 堆栈和 Windows
环回虚拟网络接口。使用环回接口后，
没有实时网络连接的情况下也能使用项目。

虽然此演示应用程序不需要在构建时包含任何自定义 TCP/IP
功能，但通常很容易
在常用（如lwIP ）或自定义 TCP/IP 堆栈，
或其他传输媒介（例如蓝牙）上运行 WolfSSL。WolfSSL 提供 
便于使用的 [I/O 抽象层](https://wolfssl.com/wolfSSL/Docs-wolfssl-manual-5-portability.html)，
使用户可以自己编写输入/输出函数。

只要是在标准 Windows 计算机上执行此应用程序，
就不需要外部硬件和硬件设置。


### TCP/IP 服务器任务

FreeRTOS TCP/IP 服务器任务在 SecureTCPServerTask.c
源文件中实现。
它会创建一个 TCP/IP 套接字，该套接字被配置为侦听来自
FreeRTOS TCP/IP 客户端任务的连接。接受连接后，TCP/IP
服务器任务只需将其通过套接字接收的所有数据写入
控制台，直到此连接关闭。

每次接受一个连接时都会创建一个 WolfSSL 对象，
每次关闭连接时则都会删除一个 WolfSSL 对象。

下方流程图描述了服务器行为。

![显示 RTOS TCP/IP 服务器任务行为的流程图](/media/2018/RTOS-socket-server-task.jpg)
*RTOS 服务器任务的行为*


### TCP/IP 客户端任务

FreeRTOS TCP/IP 客户端任务在 SecureTCPClientTask.c 源文件中
实现。
它会创建一个 TCP/IP 套接字，然后将此套接字反复连接至 FreeRTOS
TCP/IP 服务器任务，并通过此套接字发送 10 个字符串，然后将其
再次关闭。在每个迭代之间使用短暂延迟，以防止
服务器任务写入控制台的速度太快。

每次连接套接字时都会创建一个 WolfSSL 对象，
每次关闭套接字时都会删除一个 WolfSSL 对象。

下方流程图描述了客户端行为。

![显示 RTOS TCP/IP 客户端任务行为的流程图](/media/2018/RTOS-socket-client-task.jpg)
*RTOS 客户端任务的行为*


### 构建和执行演示

1. 确保已安装 Microsoft Visual C++。

   [免费 Express 版本](https://visualstudio.microsoft.com/vs/community/)
   。

2. Visual C ++ 解决方案文件被称为 FreeRTOS_Plus_WolfSSL.sln，
   位于下载文件的 FreeRTOS-Plus/Demo/FreeRTOS_Plus_WolfSSL_Windows_Simulator
   目录中。双击文件打开 Visual C++，或者
   在 Visual C++ IDE 中打开文件。

   ![在编译器开发工具中查看的 RTOS 项目](/media/2018/RTOS_project_viewed_in_the_compiler_IDE.jpg)
   *在 Visual C++ IDE 中查看的 RTOS 项目*

   在解决方案资源管理器中：

   * 实现演示应用程序的源文件列于 Demo App Source 文件夹中。
   * 实现加密功能的源文件在 FreeRTOS-Plus/WolfSSL 文件夹中列出。
   * 实现 RTOS 功能的源文件列于 FreeRTOS 文件夹中。

3. 构建和执行应用程序。

   ![执行 RTOS 任务时生成的输出](/media/2018/RTOS_WolfSSL_demo_output.jpg)
   *执行演示应用程序时生成的输出*
