---
title: "嵌入式 Web 服务器演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 所有演示
    link: /Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview
---


### 使用 FreeRTOS ARM7 GCC 移植


![lpc-e2124.gif](/media/2018/lpc-e2124.gif)

**从 FreeRTOS V4.0.3 起，此演示需要 CrossWorks v1.6 或更高版本。**

## 引言

此演示应用程序使用 [FreeRTOS GCC ARM7 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106)以及 
[Rowley Associates](http://www.rowley.co.uk/) CrossWorks 集成开发工具，以创建多任务 
嵌入式 Web 服务器示例。 

该示例执行 12 个标准演示应用程序任务、一个空闲任务和一个包含
[Adam Dunkels uIP (�IP) 嵌入式 TCP/IP 堆栈和小型 Web 服务器示例的任务](http://www.sics.se/~adam/uip/)。

自此演示创建以来，FreeRTOS 对 uIP 堆栈进行了一些修改。请参阅 
[嵌入式以太网示例列表](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)页面，了解更多 
信息。

此演示经过预配置可在 LPC-E2124 嵌入式以太网开发板上执行 
（如果您希望使用其他开发板，我们也提供了相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）， 
uIP TCP/IP 堆栈移植和嵌入式以太网设备驱动程序由 
[Paul Curtis of Rowley Associates](http://www.rowley.co.uk/msp430/uip.htm) 提供。


## 重要提示！使用 �IP 演示的注意事项

*使用此演示之前，请阅读以下所有要点。*

### RTOS 配置


此演示使用单独记录的 [FreeRTOS GCC ARM7 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106)。
Demo/uIP_Demo_Rowley_ARM7/FreeRTOSConfig.h 文件用于定制移植以用于 LPC2124 开发板
。


### 源代码组织


* FreeRTOS/Demo/uIP_Demo_Rowley_ARM7 目录包含 Rowley CrossWorks 项目文件 (rtosdemo.hzp) 和 main.c。
* FreeRTOS/Demo/uIP_Demo_Rowley_ARM7/uip 目录包含 uIP 源代码。
* 请参阅[源代码组织部分](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)了解标准 FreeRTOS 下载中包含的所有文件的说明。
* main.c 包含应用程序入口点。它负责创建所有任务，然后启动实时内核。


### 构建演示应用程序

CrossWorks 为 GCC 开发工具提供了一个用户友好界面，
极大地简化了启动配置、链接和调试。要构建应用程序：
1. 在 CrossWorks IDE 中打开 FreeRTOS/Demo/uIP_Demo_Rowley_ARM7/rtosdemo.hzp 项目文件。
2. 确保已选定 "*Thumb FLASH Debug*" 配置（见下图）。请务必选择此配置，
 因为它目前是唯一包含所有必要设置的配置。  
  

![](/media/2018/selectthumbflashdebug.jpg)  

选择 Thumb Flash Debug 配置
3. 从 IDE 的 "*Build*" 菜单中选择 "*Build Solution*" 选项。在构建应用程序的过程中，不应出现警告或错误。


### 加载和执行演示应用程序


这些说明描述了如何从 CrossWorks 内部使用 [J-Link USB JTAG 调试接口](http://www.segger.com/jlink.html) 
对闪存进行编程并调试应用程序。CrossWorks 还支持 Wiggler（低成本）和 CrossConnect JTAG 接口。 
如果您无法访问任何 JTAG 接口，请参阅 GCC ARM7 主移植页面，获取有关使用 Philips 免费闪存编程软件的信息
。 

1. 将您选择的 JTAG 接口连接到嵌入式计算机并接通电源。
2. 从 "*Target*" 菜单中为您的调试接口选择适合的 "*Connect To*" 选项。
3. 从 "*Debug*" 菜单中选择 "*Start Debugging*"。


### 连接演示应用程序


若要连接嵌入式计算机，您必须设置兼容的 IP 地址并使用正确的电缆。

IP 地址已在 FreeRTOS/Demo/uIP_Demo_Rowley_ARM7/uip/uipopt.h 文件中配置。此 IP 地址必须设置在
与您主机所在的相同子网上，且不得与同一子网上的任何其他 IP 地址冲突。 


仅当集线器位于嵌入式计算机和您的主机之间时，才能使用标准 CAT5 以太网电缆。如需直接连接（不使用集线器），
则需使用交叉（或点对点）电缆。


正确配置后，在任何 HTTP 客户端（如 Internet Explorer）的地址栏中键入 'http://nnn.nnn.nnn.nnn' 进行连接
（请将 nnn 替换为正确的 IP 地址）。


### 演示应用程序功能

此演示应用程序可创建 12 个[标准演示应用程序任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)。 
这些任务用于演示和测试 RTOS 内核功能。
此外，还创建了一个 'Check' 任务，以确保标准演示任务正确执行。'Check' 任务每三秒监控一次
标准演示任务，然后切换黄色 LED。如果黄色 LED 每三秒切换一次，则表示 'Check' 任务未发现
任何错误。如果 LED 的切换速率增加到 500 毫秒，则表示至少一个任务出现错误。

此外还创建了一个单独任务，以执行 uIP TCP/IP 堆栈和 Web 服务器。 
uIP 以太网驱动程序只能轮询以太网接口。LPC-E2124 的 8 位接口模式不允许对
[CS8900](http://www.cirrus.com/en/products/pro/detail/P46.html) 以太网控制器执行中断操作。因此，uIP 任务 
以高优先级运行，
当此任务不执行操作时，会将处理时间让渡给其他任务。 


要实现此功能，需要对 Paul Curtis 提供的 uIP 代码作出少许修改。


* 将 uIP 随附的 main.c 文件重命名为 uIP_Task.c，以避免与演示应用程序的 main.c 冲突
 。同样，将 uIP_Task.c 中的 main() 函数重命名为 vuIP_TASK()，
 因为它现在被创建为一个任务，而不是作为应用程序入口点。
* 黄色 LED 现在用于 'check' 任务，而非 uIP 任务。
* 嵌入式 TCP/IP 驱动程序中使用的定时器滴答计数已更改为使用 RTOS 滴答计数。
* 对 vTaskDelay() 的调用已添加到 TCP/IP 驱动程序代码中，当 TCP/IP 任务不执行操作时，可让渡处理时间
 。
* 最大连接数量已从 10 个增加到 20 个。


### **执行上下文**


RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意： 
 启动 RTOS 调度器时(调用 vTaskStartScheduler)，处理器必须处于监管者模式 
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序项目，则在调用 vTaskStartScheduler() 之前，请确保处理器已进入监管器模式。

请参阅 [LPC2000 GCC 文档](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106#configuration-and-usage-details)， 
获取有关 RTOS 调度器设置和使用的详细信息。


### **许可**

请注意，uIP 堆栈与 FreeRTOS 分开授权。 
[用户必须熟悉许可条件](http://www.sics.se/~adam/uip/)。
