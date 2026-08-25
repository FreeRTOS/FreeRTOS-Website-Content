---
title: FreeRTOS-Plus-TCP 演示项目
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

适用于 Windows 模拟器

---

## 源代码和项目文件

该演示程序可在`FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator`  
官方 [FreeRTOS 压缩文件下载目录](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)和  
GitHub 上的 [FreeRTOS_Plus_TCP_Minimal_Windows_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator) 
存储库中找到。 


## 目标硬件

此项目使用了 [FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。
Windows 模拟器提供了一个便捷的评估平台，但它并未展示实时行为。 
模拟时间比实际时间慢。


## 编译器/工具链

已预配置此项目，以使用 
[Microsoft Visual C++ (MSVC) 的免费 Express 版本](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
进行构建。使用的是 MSVC Express Edition 2010。


## 功能

该演示包含以下标准演示配置：

* 两组 UDP 客户端任务和服务器任务，其中客户端
  任务会将数据发送至服务器任务。一组任务使用标准套接字
  接口。另一组任务使用零复制套接字接口。

构建此项目还可包括以下内容（可选）：


* 一个简单的 TCP echo 客户端任务，该任务向一个服务器
  （地址使用 configECHO_SERVER_ADDR[0-3] 和 echoECHO_PORT 配置）
  发送数据并等待 echo 回复。会检查回复是否正确。

* 一个简单的 TCP echo 服务器任务，该任务使用
  [FreeRTOS_listen()](FreeRTOS-Plus/FreeRTOS_Plus_TCP/API/listen.md) 等待传入连接。
  当建立连接并收到数据时，任务会回复
  相同的数据。


## 构建说明

1. 通过包含源代码和项目文件的[FreeRTOS下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)下载源代码
   。将 zip 文件提取至方便的位置，以确保
   目录结构体得到维护。

2. 从 Visual Studio IDE 中打开 Visual Studio 解决方案文件 FreeRTOS_Plus_TCP_Minimal.sln
   。此解决方案文件在
   "FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator"
   目录下。

3. 演示使用 WinPCap，
   通过访问真实网络连接上的原始以太网数据来创建虚拟网络连接。许多
   计算机具有多个真实的网络端口。在
   FreeRTOSConfig.h. 中设置 configNETWORK_INTERFACE_TO_USE，以告诉演示应该使用哪个真实端口
   来创建虚拟端口。

   当执行应用程序时，可用端口号会显示在控制台上
   （请参阅下文使用说明中的图像）
   。

4. 请按照
   [Echo 客户端示例文档页面](FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Echo_Clients.md)
   设置 echo 服务器并在
   FreeRTOSConfig.h 中设置 echo 服务器的地址。或者， TCP echo 服务器和/或
   客户端也可通过将宏 mainCREATE_TCP_ECHO_TASKS_SINGLE
   和 mainCREATE_TCP_ECHO_SERVER_TASK 设置为 1 的方式进行设置。

5. 虚拟端口有自己的 MAC 地址。
   将常量 configMAC_ADDR0 设置为 configMAC_ADDR5 以确保
   虚拟网络连接使用的 MAC 地址在网络上是唯一的。这些常量
   位于 FreeRTOSConfig.h 底部。

6. 如果 IP 地址分配由
   [DHCP 服务器](FreeRTOS-Plus/FreeRTOS_Plus_TCP/DHCP.md)管理，
   则无需进一步进行配置。

   如果 IP 地址分配不由 DHCP 服务器管理，
   那么在 [FreeRTOS**IP**Config.h](FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_IP_Configuration.md) 中将 ipconfigUSE_DHCP 设置为 0，
   然后编辑 FreeRTOSConfig.h 底部的常量，以确保它们对以太网有效，
   这些常量设置了静态 IP 地址、DNS 服务器地址、
   网关地址和网络掩码的默认值，确保它们对
   以太网有效。如果 IP 地址的前三个八位字节
   与同一网络上的其他 IP 地址的前三个八位字节相匹配，那么该 IP 地址就有效
   ——网络上的每个 IP 地址都必须是唯一的
   。

7. 在 IDE 的 Build 菜单中选择 "Build Solution"（或按 F7 ）
   以构建应用程序。


## 调试说明

F10 作为标准 Visual Studio 键用于启动调试会话并在进入 main() 时中断调试。

可使用同一台主机构建应用程序、调试应用程序
并且（因为使用了  Win32 模拟器）运行应用程序。
无特殊调试说明。


## 使用说明

* 在 main.c 中定义以下常量，以便在构建过程中包含或排除任务：


```c
/* Set the following constants to 1 or 0 to define which tasks to include and  
exclude. */  
#define mainCREATE_SIMPLE_UDP_CLIENT_SERVER_TASKS     1  
#define mainCREATE_TCP_ECHO_TASKS_SINGLE              0  
#define mainCREATE_TCP_ECHO_SERVER_TASK               0  
  

```


## 与其他开源 TCP/IP 堆栈一起使用的旧版演示


进一步阅读关于  [旧版 TCP/IP 演示的更多信息。](FreeRTOS-Plus/FreeRTOS_Plus_TCP/legacy-demo-projects.md)

