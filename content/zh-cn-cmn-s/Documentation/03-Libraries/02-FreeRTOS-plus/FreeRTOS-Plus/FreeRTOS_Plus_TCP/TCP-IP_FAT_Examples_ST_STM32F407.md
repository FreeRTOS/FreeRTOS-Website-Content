---
title: FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


在 ST STM32F407 ARM Cortex-M4 微控制器上运行

[[可构建的 TCP/IP 和 FAT FS 示例](TCP_FAT_demo_projects)]


## 简介

在 STM3240G-EVAL 上运行的 ![RTOS 和 TCP/IP](/media/2018/stm3240g-eval.jpg)
*没有任何硬件？现在，您仍然可以使用 [Win32 demo](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) 来尝试 RTOS TCP 和 FAT 示例
。该演示使用免费工具构建，并在 Windows 环境中运行。*

**注 1：**为演示 FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT
（用于 RAM 受限系统），本页面描述的项目
仅使用 STM32 的 192K 字节的内部 RAM。未使用 STM3240G-EVAL 开发板上的外部 RAM
。

**注 2：**本页面上的演示
可以使用
[Atollic TrueStudio IDE](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html) 的 Lite 免费版构建，
因为即使是免费版本，也不存在代码大小限制。

ST STM32F407 ARM Cortex-M4 TCP/IP 和 FAT 演示包括以下标准示例：

* [HTTP 网络服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [FTP 服务器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [TCP 回显服务器](TCP_Echo_Server)
* [TCP 回显客户端](TCP_Echo_Clients)
* [使用 UDP 套接字的命令行界面](UDP_CLI)
* [UDP 日志记录，将 FreeRTOS-Plus-TCP 日志输出发送到 UDP 端口](UDP_Logging)

FreeRTOS-Plus-FAT 用于安装 FAT 格式的 SD 卡。之后，挂载的文件
系统便可为 HTTP 和 FTP 服务器示例提供文件。

此项目使用基于

[Atollic TrueStudio](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html)
GCC 的免费版开发工具（没有代码大小限制）构建并面向
ST [STM3240G-EVAL](http://www.st.com/web/en/catalog/tools/FM116/SC959/SS1532/PF252216?sc=stm3240g-eval)
评估板上）。


## 说明

### 硬件设置

不需要特定的硬件设置。


### 定位项目

构建本页面所述演示的 Atollic TrueStudio 项目
位于名为 /FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_and_FAT_STM32F4xxx 的
[FreeRTOS Labs 下载包](/Documentation/03-Libraries/05-FreeRTOS-labs/RTOS_labs_download)目录中。

**注意**：下载中提供的 ST STM32F407 ARM Cortex-M4 TCP/IP 和 FAT 演示项目
供社区成员使用和参考。此演示虽然功能完善，
但可能并不符合我们的生产代码标准


### 软件设置 #1：设置静态或动态 IP 地址

![为 Free RTOS TCP/IP 目标](/media/2018/STM3240G-EVAL_Network_Address_Setup_In_FreeRTOSConfig.png)分配 IP 地址
*FreeRTOSConfig.h 中的网络地址设置*


[FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
和 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 头文件分别用作
FreeRTOS-Plus-TCP 和 FreeRTOS 配置文件。两者都可以从
从基于 TrueStudio Eclipse 的 IDE 内部打开。

如果使用的是 [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) 服务器，
则
将 [ipconfigUSE_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 设为 1
（在 FreeRTOSIPConfig.h 中设置），
这样就无需进一步配置与 IP 相关的网络地址。如果对 STM32 目标提供了[主机名](#软件设置-3设置主机名)，
则无需知道
DHCP 服务器分配给 STM32 的 IP 地址，因为 STM32
可以使用分配的名称定位。但是，可以查看 IP 地址，
因为它是由 [UDP 日志记录工具](#软件设置-5打印和记录消息)打印出来的。

如果不使用 DHCP 服务器，
则需在 FreeRTOSIPConfig.h 中将 ipconfigUSE_DHCP 设置为 0，[](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
并使用
FreeRTOSConfig.h 中的 configIP_ADDR0/3 和 configNET_MASK0/3 常量配置静态 IP 地址和掩码。
请注意，IP 地址常量位于 FreeRTOSConfig.h，而非
FreeRTOS**IP**Config.h 中，因为它们与
应用程序相关，而不是与 TCP/IP 堆栈直接相关。

必须确保任何手动配置的 IP 地址与
连接 STM32 的网络使用的网络掩码兼容。
在大多数情况下，兼容的 IP 地址将使用
与主计算机相同的前三个八位字节。例如，如果
主计算机的 IP 地址为 172.25.218.100，则
任何 172.25.218.nnn 地址（nnn 为 0、255 或
已在网络中存在的情况除外）都是有效的。

此外，还需要设置[网关](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
地址，该地址应适用于连接 STM32 的网络，
或者如果网关不存在，该地址应至少与配置的网络掩码兼容
。必须执行此步骤，
以防止内部健全性检查触发[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
由于网关地址和网络掩码不匹配而导致的失败。网关
地址使用 FreeRTOSConfig.h 中的 configGATEWAY_ADDR0/3 常量进行设置。


### 软件设置 #2：设置 MAC 地址

如果只有一个运行 FreeRTOS-Plus-TCP 示例的嵌入式目标连接到网络，
则无需修改 [MAC 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)。

如果有多个运行 FreeRTOS-Plus-TCP 示例的嵌入式目标连接到
同一网络，则必须确保分配给每个嵌入式目标的 MAC 地址
都是唯一的。

MAC 地址使用
FreeRTOSConfig.h 中的 configMAC_ADDR0/5 常量设置。


### 软件设置 #3：设置主机名

使用人类可读文本名称而非
IP 地址可以更加方便地识别网络节点。当
IP 地址由 DHCP 服务器分配时尤其如此，因此无需知晓该地址，
而且地址还可能会更改。例如，
ping 请求
可以发送到主机名，
如 "ping MyHostName"（其中 "MyHostName" 是分配给
网络节点的名称），而不是发送到 IP 地址，如 "ping 172.25.218.200"。

如果只有一个运行 FreeRTOS-Plus-TCP 示例的嵌入式目标连接到
网络，则无需修改默认主机名，
即 "RTOSDemo"。如果有多个运行
FreeRTOS-Plus-TCP 示例的目标连接到同一网络，则
必须确保分配给每个嵌入式目标的主机名都是唯一的。

主机名由 mainHOST_NAME 常量设置，该常量位于
main.c 源文件顶部附近。
根据网络拓扑，也可使用
mainDEVICE_NICK_NAME 常量设置的第二个主机名，
该常量也定义在 main.c 顶部。


### 软件设置 #4：设置回显服务器地址

如果使用 TCP 回显客户端示例，则将常量
 configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3 
（在 FreeRTOSConfig.h 中）设置为[合适的回显服务器](TCP_Echo_Clients)的 IP 地址。然后，FreeRTOS-Plus-TCP
将发送回显请求至
配置的回显服务器，并从其中接收回显回复。


### 软件设置 #5：打印和记录消息

![定向 RTOS TCP/IP 堆栈调试输出](/media/2018/TrueStudio_Logging_Setup.png)
*中的日志记录配置 FreeRTOSConfig.h*

交付时，未使用 [FreeRTOS_debug_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
，并且 [FreeRTOS_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
设置为[向 UDP 端口发送 TCP/IP 堆栈和应用程序日志记录消息](UDP_Logging)。
接收
UDP 日志记录消息的 IP 地址和端口号，以及一些其他
日志记录相关参数都使用 FreeRTOSConfig.h 中的常量设置，
如右图所示。

对日志消息进行缓冲，以便由低优先级后台
RTOS 任务传输。

日志输出可在许多不同的终端程序中查看，包括
Cinetix 的 UDP Term。


### 软件设置 #6：硬件特定设置

该项目在交付时已经过预先配置，可在 STM32F40G-EVAL
评估板上执行演示。若要在不同的硬件上执行演示：

* 更新 HAL_ETH_MspInit()，即 ST HAL 驱动程序回调函数，
  以确保它正确配置您的硬件 IO
  。HAL_ETH_MspInit() 在
  main.c 底部附近实现。

* 将
  FreeRTOSConfig.h 中的 configSD_DETECT_GPIO_PORT 和 configSD_DETECT_PIN 设置配置为 GPIO 端口和 PIN，用于检测是否
  存在 SD 卡。

* 如果使用了不同的 PHY，可能需要更新网络驱动程序
  。


## 运行示例

以下说明描述了如何
在 STM3240G-EVAL 评估板上构建、下载和执行应用程序：

1. 按照上面详述的软件配置步骤操作。

2. 如果可用，将一张 FAT 格式的空 SD 卡插入
   STM32F407G-EVAL 的 SD 卡插槽。

3. 检查 main.c 顶部的注释，并按要求设置
   在演示中和演示外构建单个示例的常量
   。

   注意：如果未使用 SD 卡，则不包括
   HTTP 或 FTP 服务器示例。

4. 确保 STM3240G-EVAL 硬件已使用适当的调试连接工具（如 ST Link 或 J-Link）连接到主计算机
   （运行 Atollic TrueStudio 的计算机），
   并使用以太网电缆连接到
   网络。

5. 在 TrueStudio IDE 的 "File" 菜单中选择 "Import"。系统将显示
   如下对话框。选择 "Existing Projects into Workspace"。

   ![将 STM32 TrueStudio 项目导入 Eclipse 工作区](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)
   *首次点击 "Import" 时显示的对话框*

6. 在下一个对话框中，选择 /FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_and_FAT_STM32F4xxx
   作为根目录。然后，确保在 "Projects" 区域中已勾选 RTOSDemo 项目
   并确保
   未勾选 "Copy Projects Into Workspace box"，
   然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态，
   图片中不包含 "Finish" 按钮）。

   ![选择要导入 Eclipse 的 RTOS STM32 项目](/media/2018/Import_RTOS_Atollic.png)
   *确保已勾选 RTOSDemo 且未勾选 "Copy projects into workspace"*

7. 在 TrueStudio IDE 的 "Project" 菜单中选择 "Build All"，
   以创建可执行映像。

8. 在 TrueStudio IDE 的 "Run" 菜单中选择 "Debug"，
   以创建调试配置，用于对
   STM32 闪存进行编程并启动调试会话。

**执行应用程序时会切换绿色 LED 1。**该 LED
是从空闲任务切换的，因此切换频率不一定
保持恒定。


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
