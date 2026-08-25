---
title: FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


在 Atmel SAM4E ARM Cortex-M4 微控制器上运行

[[可构建的 TCP/IP 和 FAT FS 示例](TCP_FAT_demo_projects)]


## 简介

在 SAM4E Xplained Pro 上运行的 ![RTOS 和 TCP/IP](/media/2018/sam4e_xplained_pro.jpg)
*没有任何硬件？现在，您仍然可以使用 [Win32 demo](examples_FreeRTOS_simulator) 来尝试 RTOS TCP 和 FAT 示例
。该演示使用免费工具构建，并在 Windows 环境中运行。*

Atmel SAM4E ARM CORTEX-M4 TCP/IP 和 FAT 演示包括以下标准示例：

* [HTTP 网络服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [FTP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [TCP 回显服务器](TCP_Echo_Server)
* [TCP 回显客户端](TCP_Echo_Clients)
* [使用 UDP 套接字的命令行界面](UDP_CLI)
* [UDP 日志记录，将 FreeRTOS-Plus-TCP 日志输出发送到 UDP 端口](UDP_Logging)

FreeRTOS-Plus-FAT 用于安装 FAT 格式的 SD 卡。之后，挂载的文件
系统为 HTTP 和 FTP 服务器示例提供存储。

该项目使用免费的基于 [Atmel Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio)
GCC 的开发工具构建，针对
Atmel [SAM4E Xplained Pro](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=atsam4e-xpro)
评估套件。


## 说明

### 硬件设置

不需要特定的硬件设置。


### 定位项目

构建此页面上所描述演示的 Atmel Studio 项目
位于 /FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_AND_FAT_ATSAM4E
[FreeRTOS Labs 下载包](/Documentation/03-Libraries/05-FreeRTOS-labs/RTOS_labs_download)目录中。


### 软件设置 #1：设置静态或动态 IP 地址

![为 RTOS TCP/IP 目标分配 IP 地址](/media/2018/Atmel_Studio_Network_Address_Setup_In_FreeRTOSConfig.png)
*中的网络地址设置 FreeRTOSConfig.h*


[FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
和 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 头文件分别用作
FreeRTOS-Plus-TCP 和 FreeRTOS 配置文件。两者都可以从
从 Atmel Studio IDE 中打开。

如果在 SAM4E 所连接的网络上使用 [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) 服务器，
则
将 [ipconfigUSE_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 设置
（在 FreeRTOSIPConfig.h 中设置），
。如果[配置了主机名](#软件设置-3设置主机名)，
则不需要知道 DHCP 服务器分配给 SAM4E 的 IP 地址，
因为 SAM4E 可以直接通过其主机名寻址。
不过您也可以查看 IP 地址，
查看的，因为它是由 [UDP 日志记录工具](#软件设置-5打印和记录消息)打印出来的。

如果所连接的网络没有 DHCP 服务器，则在
FreeRTOSIPConfig.h 中将 ipconfigUSE_DHCP 设置为 0，然后手动配置 IP 地址和[网络掩码](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
使用的常量为 FreeRTOSConfig.h 中的 configIP_ADDR0/3 和 configNET_MASK0/3 常量。
请注意，IP 地址常量位于 FreeRTOSConfig.h，而不是
FreeRTOS**IP**Config.h 中，因为它们与
应用程序相关，而不是与 TCP/IP 堆栈直接相关。

必须确保手动配置的 IP 地址与
网络掩码兼容。在大多数情况下，兼容的 IP 地址将使用
与主计算机相同的前三个八位字节。例如，如果
主机 IP 地址为 172.25.218.100，则
任何 172.25.218.nnn 地址（除非 nnn 为 0、255 或
已存在于网络上的数字）都是兼容的。

还需要设置[网关](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
地址，该地址对于 SAM4E 连接的网络是正确的，
或如果不存在网关则至少与网络掩码兼容
。必须执行此步骤，
以防止内部完整性检查触发[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
失败。网关地址是使用
FreeRTOSConfig.h 中的 configGATEWAY_ADDR0/3 常量设置。


### 软件设置 #2：设置 MAC 地址

MAC 地址使用
FreeRTOSConfig.h中的 configMAC_ADDR0/5 常量设置。

如果只有一个运行 FreeRTOS-Plus-TCP 示例的目标连接到网络，
则无需修改 [MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)。

如果多个运行 FreeRTOS-Plus-TCP 示例的目标连接到
同一网络，则必须确保每个目标有
唯一的 MAC 地址。


### 软件设置 #3：设置主机名

使用
文本名称而不是 IP 地址来标识网络上的节点通常更方便。当
IP 地址由 DHCP 分配时尤其如此，因此它是未知的。例如，
ping 请求
可以发送到主机名，
如 "ping MyHostName"（其中 "MyHostName" 是分配给
网络节点的名称），而不是发送到 IP 地址，如 "ping 172.25.218.200"。

如果只有一个运行 FreeRTOS-Plus-TCP 示例的目标连接到
网络，则无需修改默认主机名，
该主机名设置为 "RTOSDemo"。如果多个运行
FreeRTOS-Plus-TCP 示例的目标连接到同一网络，则
需要为每个目标分配不同的主机名。

主机名由 mainHOST_NAME 常量设置，该常量位于
main.c 源文件顶部的 mainHOST_NAME 常量设置。
根据网络拓扑，也可使用由
mainDEVICE_NICK_NAME 常量设置的第二个主机名，
该常量也定义在 main.c 顶部。


### 软件设置 #4：设置回显服务器地址

如果使用 TCP 回显客户端示例，则将常量
configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3
（在 FreeRTOSConfig.h 中）设置为[合适的回显服务器](TCP_Echo_Clients)的 IP 地址。然后，FreeRTOS-Plus-TCP
将发送回显请求至
配置的回显服务器，并从其中接收回显回复。


### 软件设置 #5：打印和记录消息

![定向 RTOS TCP/IP 堆栈调试输出](/media/2018/Atmel_Studio_Logging_Setup.png)
*FreeRTOSConfig.h 中的日志记录配置*

在 FreeRTOSIPConfig.h 中，[FreeRTOS_debug_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
已禁用，[FreeRTOS_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
设置为通过 UDP[(UDP_Logging) ]发送 TCP/IP 堆栈和应用程序日志记录消息。
接收发送的
UDP 日志记录消息的 IP 地址和端口号，以及一些其他
日志记录相关参数都使用 FreeRTOSConfig.h 中的常量设置，
如右图所示。

对日志消息进行缓冲，以便由低优先级后台
RTOS 任务。

可以在许多不同的终端程序中查看日志输出，
包括 Cinetix 的 [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm)
。


### 软件设置 #6：硬件特定设置

该项目交付经过预先配置，可在 SAM4E Xplained Pro
评估板上执行。可能需要更新 IO 配置以
在不同硬件上使用演示，或者如果使用不同的 PHY，则需要更新网络驱动程序
。


## 运行示例

以下说明描述了如何
在 SAM4E Xplained Pro 评估板上构建、下载并执行应用：

1. 按照上面详述的软件配置步骤操作。

2. 如果可用，将一张空的 FAT 格式的 SD 卡插入
   SAM4E Xplained Pro 的 SD 卡插槽。

3. 检查 main.c 顶部的注释，并设置
   在演示中和演示外构建单个示例的常量。

   注意：如果未使用 SD 卡，则不包括
   HTTP 或 FTP 服务器示例。

4. 确保 SAM4E Xpalained Pro 硬件已使用目标的调试 USB 端口连接到主
   计算机（运行 Atmel Studio 的计算机），
   并使用以太网电缆连接到合适的网络。

5. 首先按 F7 生成项目，然后按 F5
   编程目标闪存，然后启动应用程序
   执行

**当应用程序执行时，LED0 每半秒切换一次。**


### 基本连接性测试

建议在对以下链接的示例进行实验之前测试基本连接性
。这可以通过 ping 目标来完成。
如果收到 ping 回复，则说明应用程序正在运行
且已正确连接到网络。

若要 ping 设备，请打开命令提示符并键入 "ping "，
其中  是分配给目标的名称，默认
为 "RTOSDemo"。

如果未收到 ping 回复，则关闭 DHCP，为目标分配一个
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
