---
title: IPv6 演示项目
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


适用于 FreeRTOS Windows 模拟器

该 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目 [](https://en.wikipedia.org/wiki/IPv6)
为目前仅支持 IPv4 的 FreeRTOS-Plus-TCP TCP/IP 堆栈增加了 IPv6 功能。虽然由此产生的双 IPv4 / IPv6
版本功能齐全，但仍在进行优化、测试范围和文档改进，以及内存
安全检查。在这项工作完成之前，
代码将作为 [FreeRTOS-Plus-TCP GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)的一个分支提供。


## 源代码和项目文件

此演示应用程序可在
[labs/ipv6_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi) 中找到
（隶属于 [FreeRTOS-Plus-TCP](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) 存储库）。该演示应用程序可在
上述存储库的 `demos/IPv6_Multi_WinSim_demo` 目录中找到。

此演示展示了 FreeRTOS-Plus-TCP IPv6 and 和多接口库的几种协议（UDP、TCP、ICMP/ping、NTP）。此演示将针对所述的每个协议同时使用 IPv6 和 IPv4。

FreeRTOS-Plus-TCP 多接口 Visual Studio 项目文件位于
demos/IPv6_Multi_WinSim_demo 目录中。
您可以在 .props 文件中找到多个指示源文件位置的宏：

- $(FREERTOS_SOURCE_DIR) 内核源

- $(FREERTOS_INCLUDE_DIR) 内核 头文件

- $(DEMO_COMMON_SOURCE_DIR) 演示的公共目录的位置

- $(PLUS_TCP_SOURCE_DIR) The FreeRTOS-Plus-TCP 源文件

- $(PLUS_TCP_INCLUDE_DIR) The FreeRTOS-Plus-TCP 头文件

- $(UTILITIES_SOURCE_DIR) tcp_utilities 目录的位置

您可以更改这些宏，让项目使用不同的
源树。


## 目标硬件

此项目使用
[FreeRTOS-Plus-TCP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
FreeRTOS Windows 模拟器。Windows 模拟器提供了一个方便的评估平台，但它
不能显示实时行为。模拟时间比实际时间慢。


## 编译器/工具链

已预配置此项目，以使用
[免费的 Microsoft Visual C++](https://visualstudio.microsoft.com/) (MSVC) Express 版本构建。使用的是
MSVC Express Edition 2010。


## 功能

IPv6_Multi_WinSim_demo 演示可执行一些基本的网络活动：

- 对局域网中的 IPv4 地址进行ARP 地址解析

- 对局域网中的 IPv6 地址进行邻居发现

- 使用 DNS（异步或同步）查找 IPv4 或 IPv6 地址。

- 使用 LLMNR 查找本地主机 (IPv4/IPv6)（不再视为安全操作） 

- 通过 IPv4/IPv6 与 NTP 服务器对话并使用 UDP 获取时间

- 使用 TCP/HTTP 从任何公共服务器下载文件

- 使用 IPv4 或 IPv6 对网络或局域网上的任何服务器执行 ping 操作

此演示可以轻松适应您的各种需求。它的工作原理与使用命令行接口 (CLI) 执行上述任务类似。

下面是一些示例：

```
	http4 google.co.uk /index.html
	http6 amazon.com /index.html
	ping4 10.0.1.10
	ping6 2001:470:ec54::
	dnsq4 yahoo.com
	ntp6a 2.europe.pool.ntp.org

```

最后一行将首先查找所述的 NTP 服务器，发送请求并等待回复。时间
将打印在日志中。

虽然它被称为 CLI，但演示中并未包含标准输入。所有命令都在 main.c 中进行硬编码。

关键字可以包含一些单字母后缀：4 或 6（用于 IPv4/IPv6），“a”表示
执行异步 DNS 查找，“c”表示在开始任务前清除所有缓存。


## 构建说明

1. 通过克隆
   [labs/ipv6_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)
   （隶属于 FreeRTOS-Plus-TCP 存储库）下载源代码。

2. 从 Visual Studio IDE 中打开 `FreeRTOS_Plus_TCP_IPv6_Multi.sln` Visual Studio 解决方案文件
   。该解决方案文件位于“demos/IPv6_Multi_WinSim_demo”目录中。

3. 此演示使用 WinPCap 通过访问真实网络连接上的原始以太网数据来创建虚拟网络连接，
   因此只能与有线网络接口一起使用。许多计算机都有
   多个真实网络接口。在 FreeRTOSConfig.h 中设置 configNETWORK_INTERFACE_TO_USE
   以告知演示应使用哪个真实接口创建虚拟接口。执行应用程序时，
   控制台上会显示可用的接口号。

4. 虚拟接口有自己的 MAC 地址。将常量 configMAC_ADDR0 设置为 configMAC_ADDR5，
   以确保虚拟网络连接使用的 MAC 地址在网络上是唯一的。可以编辑此文件中定义的常量，
   位于 FreeRTOSConfig.h底部。

5. 在这种情况下， IP 地址是通过静态分配方式进行的。它不由 [DHCP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4)托管。
   如果 IP 地址的前三个八进制数与同一网络中其他 IP 地址的前三个八进制数一致，
   则所配置的 IP 地址有效——每个 IP 地址在网络中都必须是唯一的。

6. 在 IDE 的 Build 菜单中选择 "Build Solution"（或按 F7 ）以构建应用程序。


## 调试说明

F10 作为标准 Visual Studio 键用于启动调试会话并在进入 main() 时中断调试。
可使用同一台主机构建应用程序、调试应用程序
并且（因为使用了 Win32 模拟器）运行应用程序。无特殊调试说明。
