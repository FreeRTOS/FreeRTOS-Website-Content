---
title: FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

使用 FreeRTOS Windows 移植

[[可构建 TCP/IP 和 FAT FS 示例](TCP_FAT_demo_projects)]

## 简介

我们提供了两个项目，这两个项目可使用免费工具在 Windows 环境下构建并执行 FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT，
无需
购买任何特殊硬件：

1. **FreeRTOS-Plus-TCP 入门项目**

   FreeRTOS-Plus-TCP 入门项目仅
   包括本页面底部列出的其中两个[示例](#选择要运行的示例)
   ，不包括 FreeRTOS-Plus-FAT、
   FreeRTOS-Plus-CLI 或任何跟踪功能。

2. **综合项目**

   综合项目包括此页面底部列出的所有[示例](#选择要运行的示例)
   。  [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)
   为 FTP 和 HTTP 示例提供文件存储，
   而 [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
   则提供命令行接口。

这两个项目都是预配置的，以便使用
免费版 [Visual Studio C/C++](https://visualstudio.microsoft.com/vs/community/) 构建，
并使用 [FreeRTOS Win32 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。 


## 简介

### 前提条件

构建和运行 Win32 RTOS 移植
示例需满足以下条件：

* 以太网端口已连接的一台 Windows 主机（请参阅下文的[硬件设置](#硬件设置)
  章节）。这些项目已在 Windows XP、Windows 7 和 Windows 10 系统中测试过。

  如果您没有有线以太网端口：

  + 可能可以安装虚拟网卡，然后将虚拟网卡桥接至
    Wi-Fi 接口——若此方法可行，希望您能
    在[支持论坛帖子](https://forums.freertos.org/)中描述您的配置！

  + 我们成功使用了
    [以太网转 Wi-Fi 桥接器](https://www.amazon.com/Vonets-VAP11G-300-Wireless-Multi-Functional-Amplifier/dp/B014SK2H6W/ref=sr_1_1?keywords=VAP11G)，
    （但我们无法为此类设备的使用提供技术支持）。

* Visual Studio C/C + + 的安装版本。[免费社区版](https://visualstudio.microsoft.com/vs/community/)
  已足够使用。详情请参见页面顶部说明，
  该[页面描述了适用于 C/C++ 版本的 Visual Studio 相关的 FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
  。

* 已安装的 [WinPCap](https://www.winpcap.org/) 版本（NPCap 也可以使用）。如果
  您已安装 Wireshark，则可跳过此步骤。

* 如果您想要运行入门项目，请前往 [FreeRTOS 主下载包页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)，或者
  如果你想运行综合项目，请前往 FreeRTOS Labs [源代码下载页面](Download_FreeRTOS_Plus_TCP)
  。**注意** Labs 下载页面上的源代码要旧得多，
  不建议用于生产。

* 最后，虽然严格来说并非前提条件，但我们强烈建议您安装
  [Wireshark](https://www.wireshark.org/) 等工具，以便查看网络流量。


### 硬件设置

此 Win32 示例使用 WinPCap 读写原始以太网数据包，以便在
以太网上创建一个虚拟节点。该虚拟节点拥有
自己的 [MAC 地址](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
和 [IP 地址](/Documentation/03-Libraries/03-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/static_ip_address)。在示例中，主机会使用
其真实的 MAC 地址和 IP 地址与虚拟的 MAC 地址
和 IP 地址进行通信，就好像它们是同一网络上的两台独立计算机那样——
实际上，这两个节点都在同一主机上运行。

要让此设置有效，即使没有使用网络上的其他节点，主机也**必须**物理连接到网络，
否则，
在 Windows 系统下，以太网端口会被断开，无法进行通信
。相关网络不必是真实的网络，只需
将 Windows 主机连接至具有以太网端口的 MCU 开发板即可，
前提是 Windows 认为以太网已连接。

RTOS 模拟器![(/media/2018/Win32_network_environment.png)中的 ]TCP/IP
*真实和虚拟节点连接到同一个网络，因此可以相互通信*


### 打开一个项目

在完成软件设置前，必须先打开项目。

1. **仅限 FreeRTOS-Plus-TCP 入门项目**

   适用于 FreeRTOS-Plus-TCP 入门项目的 Visual Studio 工作区示例名为 FreeRTOS_Plus_TCP_Minimal.sln，
   并位于 FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator
   目录下（此为 [FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的目录）。

2. **综合项目**

   综合项目的 Visual Studio 工作区示例名为 FreeRTOS_Plus_TCP_and_FAT.sln，
   并位于 FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_and_FAT_Windows_Simulator
   目录下（此为 [FreeRTOS labs](Download_FreeRTOS_Plus_TCP) 下载文件的目录）。


### 软件设置 #1：设置静态或动态 IP 地址

![将 IP 地址分配给 RTOS 节点](/media/2018/Network_Address_Setup_In_FreeRTOSConfig.png)
* 中的网络地址设置FreeRTOSConfig.h*

[FreeRTOSIPConfig.h](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
和 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 头文件分别用作
FreeRTOS-Plus-TCP 和 FreeRTOS 配置文件。两者都可以
从 Visual Studio 中打开。

如果在 SAM4E 所连接的网络上使用 [DHCP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) 服务器，
则
在 FreeRTOSIPConfig.h 中将 [ipconfigUSE_DHCP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DHCP) 设置为 1，无需进一步配置 IP 地址
。如果
[配置了主机名](#软件设置-3设置主机名)，则无需知道 DHCP 服务器分配给演示的 IP 地址，
因为可以直接通过名称找到演示。不过您也可以查看 IP 地址，
因为它是使用[日志记录工具](#软件设置-4打印和记录消息)输出的。

如果所连接的网络没有 DHCP 服务器，则在
FreeRTOSIPConfig.h 中将 ipconfigUSE_DHCP 设置为 0，然后手动配置 IP 地址和[网络掩码](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
。IP 地址和网络掩码分别使用
FreeRTOSConfig.h 中的 configIP_ADDR0/3 和 configNET_MASK0/3 常量进行设置。
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

此外，还需要设置[网关](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
地址，且该地址也需
与网络掩码兼容。这一步骤必不可少，即使网络上并没有网关
（否则，内部完整性检查时将触发 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
失败）。网关地址使用
FreeRTOSConfig.h 中的 configGATEWAY_ADDR0/3 常量设置。


### 软件设置 #2：设置（虚拟）MAC 地址

如果只有一台运行示例的计算机连接到网络，
则无需修改[虚拟] [MAC 地址](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)。

如果有多台运行示例的计算机连接到
同一网络，则必须确保每台计算机都有
唯一的[虚拟] MAC 地址。

MAC 地址使用
FreeRTOSConfig.h 中的 configMAC_ADDR0/5 常量设置。


### 软件设置 #3：设置主机名

使用
名称来识别网络节点通常比使用 IP 地址识别方便。当
IP 地址未知时更是如此。例如，与其向 IP 地址发送
诸如 “ping 192.168.0.200” 之类的 ping 请求， 不如
向主机名发送诸如 “ping MyHostName” 之类的 ping 请求（其中
MyHostName 是分配给网络节点的名称）。

如果只有一台运行示例的计算机连接到
网络，则无需修改默认主机名，
即 “RTOSDemo”。如果有多台运行示例的计算机
连接到同一网络，则必须
给每台计算机分配不同的主机名。

主机名由
main.c 源文件顶部的 mainHOST_NAME 常量设置。
根据网络拓扑，也可使用由
mainDEVICE_NICK_NAME 常量设置的第二个主机名，
该常量也定义在 main.c 顶部。


### 软件设置 #4：打印和记录消息

![定向 RTOS 调试输出](/media/2018/Logging_Setup.png)
*FreeRTOSIPConfig.h 中的日志记录配置*

提供 FreeRTOSIPConfig.h 时，FreeRTOS_debug_printf() 会被禁用，
而且 FreeRTOS_printf() 还会调用
名为 vLoggingPrintf() 的 Windows 模拟器特定实用程序文件。

日志输出可发送到：

1. UDP 端口：

   如果 mainLOG_TO_UDP 在 main.c 中被设置为 pdTRUE，则将
   使用 [UDP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) 发送日志输出。
   UDP 数据将被发送至由
   定义在 FreeRTOSConfig.h 中的 configECHO_SERVER_ADDR0 和 ConfigECHO_SERVER_ADDR3 常量设置的 IP 地址
   （即，使用[回显服务器演示](TCP_Echo_Clients)示例时的回显服务器地址）
   和[移植号](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number)
   （同样由 FreeRTOSConfig.h 中的 configPRINT_PORT 常量设置）。

2. 磁盘文件：

   如果 mainLOG_TO_DISK_FILE 在 main.c 中被设置为 pdTRUE ，则日志输出将被
   写入名为 RTOSDemo.log 的文件中。当此文件达到
   40M 字节时，它将被重命名为 RTOSDemo.ful，并启动一个新的日志文件
   。

3. 标准输出：

   如果 mainLOG_TO_STDOUT 在 main.c 中被设置为 pdTRUE ，则日志输出将被
   发送到 stdout。

**注意：**不应从 RTOS 任务中执行与输出相关的 Windows 系统调用。
因此，标准输出和磁盘文件日志数据被传递到
标准 Windows 线程用于输出。UDP 日志记录直接从 RTOS
任务发送，因为它使用 FreeRTOS-Plus-TCP，而不是 Windows TCP/IP 堆栈。


### 软件设置 #5：选择网络接口

大多数计算机都有多个网络接口，因此须
告诉应用程序该使用哪个接口。

先编译（在 Visual Studio 中按 F7），然后运行（在 Visual Studio 中按 F5）
应用程序。控制台屏幕会显示可用的网络
接口。将
FreeRTOSConfig.h 中的 configNETWORK_INTERFACE_TO_USE 常量设置为
正在使用的接口旁边的数字。然后须重新编译程序。

**故障排除：**

* 如果未显示网络接口，那
  可能 Windows 未运行 **NPF** 服务。为解决此问题，
  请在命令控制台输入 "sc start npf" （需要管理员权限），
  然后重新启动应用程序。

* 如果您无法建立通信，或者您
  在 [Wireshark](https://www.wireshark.org/) 中看不到任何网络流量，那请使用有线网络，
  而不要使用无线网络。如果此法不通，则请
  从同一网络的其他计算机连接到 （或 ping）项目
  。

* 请务必确保您的防火墙或 Windows 设置没有阻止
  网络流量。

![RTOS 网络接口](/media/2018/network_interface_in_command_console.png)
*示例开始运行时所显示的可用网络接口*



## 运行示例

现在，硬件和软件均已配置好，可以开始执行示例。


### 基本连接性测试

在尝试以下示例之前，建议
通过启动、运行应用程序，然后对目标执行 ping 操作以测试基本连接性。
如果收到 ping 回复，
且正确连接到网络。

若要 ping 设备，请打开命令提示符并键入 “ping aaa.bbb.ccc.ddd”，其中 aaa.bbb.ccc.ddd 是
网络连接时显示在控制台上的 IP 地址。另外，如果要在配置文件中启用 ping 操作，
则请键入 “ping RTOSDemo” ，这里假设
主机名尚未发生改变，仍是默认的 “RTOSDemo” 。

如果未收到 ping 回复，则关闭 DHCP，为目标分配一个
IP 地址，然后使用分配的 IP
地址代替主机名重试。

本页的设置说明描述了如何设置静态 IP 地址以及如何设置
主机名。

![对 TCP 目标进行 ping 操作](/media/2018/pinging_the_target.png)
*对目标执行 ping 操作，并接收 ping 响应*


### 选择要运行的示例

综合项目包含多个示例，
可以使用 #define 常量
（位于 main.c 顶部）有选择地在构建中包含这些示例。关于每个示例的描述以及
将示例包含在构建中的详情说明，请参阅下方链接。

所有示例均可在综合项目中使用。只有
“与基本 UDP 服务器进行通信的基本 UDP 客户端”和
“TCP 回显客户端 （在同一 RTOS 任务中执行 Rx 和 Tx ）”示例
可在更简单的 FreeRTOS-Plus-TCP 入门项目中使用。

可用示例

* FreeRTOS-Plus-TCP UDP 套接字示例

  1. [使用 UDP 套接字进行输入、输出的命令行接口](UDP_CLI)
  2. [与基础版 UDP 服务器通信的基础版 UDP 客户端（标准和零拷贝）](UDP_client_server)
  3. [使用 FreeRTOS_select()](using_select)
  4. [UDP 回显客户端](UDP_Echo_Clients)

* FreeRTOS-Plus-TCP TCP 套接字示例

  1. [使用 TCP 套接字进行输入、输出的命令行接口](TCP_CLI)
  2. [TCP 回显客户端（在同一 RTOS 任务中执行的 Rx 和 Tx）](TCP_Echo_Clients)
  3. [TCP 回显客户端（在不同 RTOS 任务中执行的 Rx 和 Tx）](TCP_Echo_Clients_Separate)
  4. [TCP 回显服务器](TCP_Echo_Server)

* FreeRTOS-Plus-TCP、FreeRTOS-Plus-FAT Web (HTTP) 和 FTP 示例

  1. [FTP 服务器](FTP_Server)
  2. [HTTP Web 服务器](HTTP_web_Server)

