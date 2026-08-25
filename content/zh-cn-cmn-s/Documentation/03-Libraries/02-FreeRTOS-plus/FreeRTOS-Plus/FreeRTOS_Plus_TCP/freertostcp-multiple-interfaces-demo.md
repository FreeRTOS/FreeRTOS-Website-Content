---
title: FreeRTOS-Plus-TCP 多接口演示项目
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


适用于 FreeRTOS Windows 模拟器

该 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目将为
目前只有单接口的 FreeRTOS-Plus-TCP TCP/IP 堆栈添加多接口和多端点支持。虽然由此产生的
多接口版本功能齐全，但仍在进行优化、测试范围
和文档改进以及内存安全检查。在这项工作完成之前，
代码可作为 [FreeRTOS-Plus-TCP 存储库](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)的分支使用。

---

## 源代码和项目文件

此演示应用程序位于 `labs/ipv6_multi` 分支中
（隶属于 [FreeRTOS-Plus-TCP](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) 存储库）。该演示应用程序可在
上述存储库的 `demos/Multi\_interface\_demo` 目录中找到。

此演示展示了
FreeRTOS-Plus-TCP IPv6 和多接口库的多接口（或者更确切地说是多端点）功能。

当设备有多个接口时，生成的 IP 数据包可以发送到其中任何一个接口。但是，
选择正确的接口很重要，因为在子网分离的情况下，
数据包可能无法抵达预期目标。此外，将数据包发送到所有接口只会产生不必要的
网络流量。


此演示使用两种不同[类型](https://en.wikipedia.org/wiki/Classful_network)的 IP 地址。
由于 Windows 模拟器环境没有可供 FreeRTOS 使用的多个接口，
此演示只被配置使用一个接口：以太网。您可以根据需要
修改以下宏来更改 IP 地址：

在 `FreeRTOSConfig.h`中

```c
/* Default IP address configuration. Used in ipconfigUSE_DNS is set to 0, or
 * ipconfigUSE_DNS is set to 1 but a DNS server cannot be contacted. */
#define configIP1_ADDR0                      192
#define configIP1_ADDR1                      168
#define configIP1_ADDR2                      0
#define configIP1_ADDR3                      200

```

以及在 `main.c` 中

```c
/* Second set of IP address to be used by this demo. */
#define configIP2_ADDR0                 10
#define configIP2_ADDR1                 0
#define configIP2_ADDR2                 1
#define configIP2_ADDR3                 6

```

如下所示，此演示尝试对在
`main.c` 中配置的不同子网掩码上两个 IP 地址进行 ping 操作。通过 [Wireshark](https://www.wireshark.org/) 等网络分析器，
您可以看到用来 ping 下方 IP 地址的 IP 地址属于同一
子网。也就是说，`10.0.1.6` 将用于 ping `10.0.1.10`，`192.168.0.200` 将用于 ping `192.168.0.1`。

```c
#define democonfigCLASS_A_IP_ADDRESS  "10.0.1.10"    /* IP address of another
                                                        device on the network
                                                        with configured static
                                                        IP that can be pinged. */

#define democonfigCLASS_C_IP_ADDRESS  "192.168.0.1"  /* IP address of the router. */

```


## 目标硬件

此项目使用了 [FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。
Windows 模拟器提供了一个方便的评估平台，但它
不能显示实时行为。模拟时间比实际时间
慢很多。


## 编译器/工具链

已预配置此项目，以使用
[Microsoft Visual C++ (MSVC) 的免费 Express 版本](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
进行构建。使用的是 MSVC Express Edition 2010。


## 功能

该演示包含以下标准演示配置：

* 两组可 ping A 类和 C 类 IP 地址的任务，
  使用宏 `democonfigCLASS_A_IP_ADDRESS`
  和 `democonfigCLASS_C_IP_ADDRESS` 配置，如上所示。


## 构建说明

1. 通过克隆
   "[labs/ipv6_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)" 分支
   （隶属于 FreeRTOS-Plus-TCP 存储库）下载源代码。

2. 从 Visual Studio IDE 中打开 Visual Studio 解决方案文件 Multi_interface_demo.sln
   。该解决方案文件位于
   “demos/Multi_interface_demo” 目录中。

3. 演示使用 WinPCap，
   通过访问真实网络连接上的原始以太网数据创建虚拟网络连接——因此只有使用有线网络接口才有效。许多
   计算机都有多个真实网络接口。在
   FreeRTOSConfig.h 中设置 configNETWORK_INTERFACE_TO_USE 以告诉演示该使用哪个真实接口
   来创建虚拟接口。

   当
   执行应用程序时，可用接口数会显示在控制台上（见下图）。

   ![](/media/2020/Interfaces_displayed-lanczos3-1024x593.png)

4. 您需要为另一台设备配置 IP 地址，该 IP 地址类型要
   不同于路由器的 IP 地址类型。也就是说，如果路由器使用 192.x.x.x （ C类 IP 地址），则
   其他设备应使用 10.x.x.x (`democonfigCLASS_A_IP_ADDRESS`) ，反之亦然。

   **使用个人电脑**

   如果您将个人电脑当作第二台设备来使用，则需要进入 "`Control Panel > Network and
   Sharing Center > Change adapter settings`"。然后您就可以看到您电脑的所有适配器。
   选择你想在此演示中使用的一个适配器。右键单击它并选择 "`Properties`"。
   您将看到一个窗口（如下所示）。

   ![](/media/2020/Adapter_Properties.png)

   选择 "Internet Protocol Version 4 (TCP/IPv4)" ，然后单击 "Properties"。一个新的
   窗口会被打开。在该窗口中进行更改（如下图所示）。

   ![](/media/2020/Static_IP_settings.jpg)

   **请注意，图中所示的 IP 地址（以及您设置的 IP 地址）
   应与 democonfigCLASS_A_IP_ADDRESS 相同。**

5. 虚拟接口有自己的 MAC 地址。
   将常量 configMAC_ADDR0 设置为 configMAC_ADDR5 以确保
   虚拟网络连接使用的 MAC 地址在网络上是唯一的。这些常量
   位于 FreeRTOSConfig.h 底部。

6. 在这种情况下， IP 地址是通过静态分配方式进行的。它不由 [DHCP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4)托管。

   如果配置的 IP 地址的前三个
   八位数与同一网络上的其他 IP 地址的前三个八位数相匹配，那么该 IP 地址就有效
   ——网络上的每个 IP 地址都必须是唯一的
   。

7. 在 IDE 的 Build 菜单中选择 "Build Solution"（或按 F7 ）
   以构建应用程序。


## 调试说明

在 Visual Studio 标准版中，F10 是
用来在进入 main() 时启动调试会话和中断的按键。

可使用同一台主机构建应用程序、调试应程序以及
并且（因为使用了  Win32 模拟器）运行应用程序。
无特殊调试说明。
