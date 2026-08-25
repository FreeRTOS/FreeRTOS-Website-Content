---
title: FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

在兼容双核 ARM Cortex-A9 处理器的 Xilinx Zynq SoC 上运行

[[可构建的 TCP/IP 和 FAT FS 示例](TCP_FAT_demo_projects)]


## 简介

![](/media/2018/MicroZed.jpg)
*没有任何硬件？现在，您仍然可以使用 [Win32 demo](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) 来尝试 RTOS TCP 和 FAT 示例
 。该演示使用免费工具构建，并在
 Windows 环境中运行。*

Zynq FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 演示包括以下标准示例：

* [FTP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [HTTP web 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [TCP 回显客户端](TCP_Echo_Clients)
* [TCP 回显服务器](TCP_Echo_Server)
* [使用 UDP 套接字的命令行界面](UDP_CLI)
* [UDP 日志记录，将 FreeRTOS-Plus-TCP 日志输出发送到 UDP 端口](UDP_Logging)

FreeRTOS-Plus-FAT 用于创建和格式化 RAM 磁盘，然后将
RAM 磁盘和 FAT 格式的 SD
卡挂载到同一个虚拟文件系统。然后，挂载好的文件系统为
FreeRTOS-Plus-TCP FTP 和 HTTP 服务器示例提供存储空间。

即使没有插入 SD 卡，也可以访问 RAM 磁盘
。


此项目使用基于 GCC 的免费版 [Xilinx SDK](https://www.xilinx.com/products/design-tools/legacy-tools/sdk.html)
开发工具构建，
并且所提供的硬件项目允许演示在 [ZC702](http://www.xilinx.com/zc702)
或者更低成本的 [MicroZed](https://www.avnet.com/wps/portal/us/products/avnet-boards/avnet-board-families/microzed/)
评估板上运行。

**重要提示：**DMA 的组合操作需要用到的缓冲大小为 32 个字节的倍数，
必须将 [BufferAllocation_1.c](Embedded_Ethernet_Buffer_Management)
与本演示配合使用。


## 说明

### 前提条件

要使 FreeRTOS-Plus-TCP 和
FreeRTOS-Plus-FAT 示例在 Xilinx Zynq SoC 上构建和运行，需满足以下前提条件：

* 具备 ZC702 或 MicroZed 评估板。

  [FreeRTOS TCP/IP 和 FAT 中间件组件也可
  使用
  [FreeRTOS Windows 移植](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)]进行评估，
  无需购买任何特殊硬件。

* 安装基于 Eclipse 的 Xilinx SDK 开发工具。发布此演示时
  ，与发布时的最新 SDK
  版本兼容的项目将同步发布。

* FreeRTOS Labs [源代码下载内容](Download_FreeRTOS_Plus_TCP)。


### 硬件设置

不需要特定的硬件设置。


### 打开项目

**注意：以前的 FreeRTOS Labs 版本要求最终用户
创建 BSP 项目，而现在可由 
SDK 自动完成。现在，BSP 项目与硬件
和应用程序项目一起发布，因此无需单独创建 BSP
。**

Eclipse 项目从
FreeRTOS-Labs 源代码树中的各种目录构建文件，因此要确保目录结构体没有被修改
。

1. 启动 SDK Eclipse IDE ，在出现提示时选择现有的 Eclipse
   工作区或创建一个新的工作区。

2. 从 IDE 的 "File" 菜单中选择 "Import"。弹出导入对话框
   。

3. 在导入对话框中，选择 "General->Existing Projects Into Workspace"，
   然后定位到 /FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_and_FAT_Zynq_SDK 并选定，
   该目录位于 FreeRTOS Labs 源代码目录树中。

4. 导入对话框的项目窗口将弹出四个项目，
   如下所示
   。确保选择 RTOSDemo 和 RTOSDemo_bsp 项目，
   然后根据所使用的开发板选择 MicroZed_hw_platform 或者
   ZC702_hw_platform。

   单击 "Finish" 按钮关闭导入对话框。

   ![导入 RTOS TCP/IP 和 FAT 项目](/media/2018/importing_the_zynq_tcpip_projects.png)
   *导入项目*

5. 右键单击项目资源管理器中的 "RTOSDemo"
   项目，然后从弹出菜单中选择 "Refresh"。

   ![针对 Zynq TCP/IP 示例](/media/2018/projects_in_the_sdk_project_explorer_window.png)创建板级支持包
   *Eclipse 项目资源管理器中的三个项目*

6. 现在便可以构建项目了。

   再次右键单击项目资源管理器窗口中的 "RTOSDemo"
   项目。这次从弹出菜单中选择
   选择 "Build Project"。


### 软件设置 #1：设置静态或动态 IP 地址

![为 RTOS TCP/IP 目标分配 IP 地址](/media/2018/SDK_Network_Address_Setup_In_FreeRTOSConfig.png)
*中的网络地址设置 FreeRTOSConfig.h*

[FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
和 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 头文件分别用作
FreeRTOS-Plus-TCP 和 FreeRTOS 配置文件。两者都可以从
SDK 的 Eclipse IDE 打开。

如果 Zynq 所连接的网络上有 [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4)
服务器，则
在 FreeRTOSIPConfig.h 中将 [ipconfigUSE_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 设置为 1，并且无需进一步配置IP地址
。如果
[配置了主机名](#软件设置-3设置主机名)，则无需知道 DHCP 服务器分配给 Zynq 的 IP 地址，
因为可以直接通过名称找到 Zynq。不过您也可以查看 IP 地址，
因为它是通过 [UDP 日志工具](#软件设置-5打印和记录消息)输出的。

如果所连接的网络没有 DHCP 服务器，则在
FreeRTOSIPConfig.h 中将 ipconfigUSE_DHCP 设置为 0，然后手动配置 IP 地址和[网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
。IP 地址和网络掩码分别使用
FreeRTOSConfig.h中的 configIP_ADDR0/3 和 configNET_MASK0/3 常量进行设置。
请注意，IP 地址设置位于 FreeRTOSConfig.h，
而非 FreeRTOS**IP**Config.h，因为它与应用程序有关，
而非 TCP/IP 堆栈配置选项。

手动设置 IP 地址时，必须确保所选择的
IP 地址与网络掩码兼容。大多数情况下，
IP 地址只要前三个八位字节
与主机地址的前三个八位字节相同即视为兼容。例如，
如果主机的 IP 地址为 192.168.0.100，
则任何 192.168.0.nnn 地址都是兼容的（nnn 不得为 0 或 255，或
网络上已存在的其他 IP 地址）。

此外，还需要设置[网关](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
地址，且该地址也需
与网络掩码兼容。这一步骤必不可少，即使网络上并没有网关
（否则，内部完整性检查时将触发 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
失败）。网关地址使用
FreeRTOSConfig.h 中的 configGATEWAY_ADDR0/3 常量设置。


### 软件设置 #2：设置 MAC 地址

MAC 地址使用
FreeRTOSConfig.h 的 configMAC_ADDR0/5 常量设置。

如果只有一个运行示例的嵌入式目标连接到网络，
则无需修改 [MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)。

如果有多个运行 FreeRTOS-Plus-TCP 示例的嵌入式目标连接到
同一网络，则必须确保每台计算机都有
唯一的 MAC 地址。


### 软件设置 #3：设置主机名

使用
名称来识别网络节点通常比使用 IP 地址识别方便。当
IP 地址未知时更是如此。例如，与其向 IP 地址发送
诸如 “ping 192.168.0.200” 之类的 ping 请求， 不如
向主机名发送诸如 “ping MyHostName” 之类的 ping 请求（其中
MyHostName 是分配给网络节点的名称）。

如果只有一个运行 FreeRTOS-Plus-TCP 示例的嵌入式设备连接到
网络，则无需修改默认主机名，
即 “RTOSDemo”。如果有多个运行示例的嵌入式设备
连接到同一网络，则必须
为每个嵌入式设备分配不同的主机名。

主机名由 mainHOST_NAME 常量设置，该常量位于
main.c 源文件顶部的 mainHOST_NAME 常量设置。
根据网络拓扑，也可使用由
mainDEVICE_NICK_NAME 常量设置的第二个主机名，
该常量也定义在 main.c 顶部。


### 软件设置 #4：设置回显服务器地址

如果使用 TCP 回显客户端示例，则将常量
configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3
（在 FreeRTOSConfig.h 中）设置为[合适的回显服务器](TCP_Echo_Clients)的 IP 地址。


### 软件设置 #5：打印和记录消息

![定向 RTOS 调试输出](/media/2018/SDK_Logging_Setup.png)
*FreeRTOSConfig.h 中的日志记录配置*

FreeRTOSIPConfig.h 中的日志记录配置，其中 [FreeRTOS_debug_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
已禁用，并将 [FreeRTOS_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
设置为通过 UDP[(UDP_Logging)] 发送 TCP/IP 堆栈和应用程序日志记录消息。
接收发送的
UDP 日志记录消息的 IP 地址和端口号，以及一些其他
日志记录相关参数都使用 FreeRTOSConfig.h 中的常量设置，
如右图所示。

对日志消息进行缓冲，以便由低优先级后台
RTOS 任务传输。

可以在许多不同的终端程序中查看日志输出。  Cinetix 的 [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm)（是一款便捷的独立实用程序）
便可用于实现此目的
。


## 运行示例

现在，硬件和软件均已配置好，可以开始执行示例。
以下说明描述了如何从
RAM 下载并执行应用程序：

1. 首先，必须创建调试配置。

   从 IDE 的 "Run" 菜单中选择 "Debug Configurations..."。将弹出调试配置
   对话框。

2. 双击 "Xilinx C/C++ application (System Debugger)"
   选项以创建新的调试配置。

3. 如下图所示，完成新的调试配置选项卡
   。图片中假定使用的是 MicroZed
   硬件平台。

   ![RTOS TCP/IP 调试配置 1](/media/2018/zynq_debug_configuration_1.png)

   ![RTOS TCP/IP 调试配置 1](/media/2018/zynq_debug_configuration_2.png)

4. 确保使用适当的调试连接将 Zynq 评估平台连接到主机，
   然后点击
   "Debug" 按钮以关闭调试配置对话框，
   将应用程序下载到 RAM，并启动调试会话。


### 基本连接性测试

在尝试以下示例之前，建议
通过启动、运行应用程序，然后对目标执行 ping 操作以测试基本连接性。
如果收到 ping 回复，
则说明应用程序正在运行且已正确连接到网络。

若要对设备执行 ping 操作，请打开命令提示符并键入 "ping RTOSDemo"，
假定主机名尚未发生改变，仍是默认的 “RTOSDemo” 。

如果未收到 ping 回复，则关闭 DHCP，为目标分配一个静态
IP 地址，然后使用分配的 IP
地址代替主机名重试。

本页的设置说明描述了如何设置静态 IP 地址以及如何设置
主机名。

![对 TCP 目标进行 ping 操作](/media/2018/pinging_the_target.png)
*对目标执行 ping 操作并接收 ping 响应*


### 包含的示例

该项目包含以下示例：

* [使用 UDP 套接字的命令行界面](UDP_CLI)
* [FTP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [HTTP web 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [TCP 回显客户端](TCP_Echo_Clients)
* [TCP 回显服务器](TCP_Echo_Server)
* [UDP 日志记录，将 FreeRTOS-Plus-TCP 日志输出发送到 UDP 端口](UDP_Logging)
