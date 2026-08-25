---
title: "Xilinx Zynq-7000 (双核 ARM Cortex-A9 ) SoC 移植，在 ZC702 评估套件上演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Xilinx Zynq-7000 SoC ZC702 评估套件](/media/2018/ZC702.jpg)

|  |
| --- |
| [**另请参阅在 Zynq 上运行的 FreeRTOS-Plus-TCP和FreeRTOS-Plus-FAT 示例**](/Documentation/03-Libraries/03-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCPIP_FAT_Examples_Xilinx_Zynq) |

本页记录了 Xilinx Zynq-7000 SoC 的 FreeRTOS 演示应用程序，
演示应用程序融合了双核 ARM Cortex-A9 处理器。

演示已预配置为使用
[Xilinx SDK](https://www.xilinx.com/products/design-tools/legacy-tools/sdk.html)工具
（撰文时使用的版本为 2016.1）进行构建，并在
[ZC702](http://www.xilinx.com/products/boards-and-kits/EK-Z7-ZC702-G.htm)
评估板上执行演示。

该项目使用默认的硬件设计和板级支持包 (BSP)，配有 SDK，
可构建 FreeRTOS 和 lwIP 作为应用程序的一部分（而非 BSP 的一部分）
。

---

### 重要提示！Xilinx Zynq-7000 SoC 上的 FreeRTOS ARM Cortex-A9 端口使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#zynq-7000-soc-演示应用程序)
3. [构建说明](#构建说明)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”以及
“[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS 的说明](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)”页面。

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码及
演示应用程序。这意味着它包含的文件比使用
Zynq 端口或官方 Zynq 演示应用程序多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
获取关于已下载文件的说明
和新项目创建的信息。

演示应用程序使用的目录结构如下所示
。CORTEX_A9_Zynq_ZC702 根目录本身
位于 FreeRTOS/Demo 中。

```c

CORTEX_A9_Zynq_ZC702
    |
    +-RTOSDemo           Contains the SDK project and C files specific to the demo.
    |
    +-RTOSDemo_bsp       Contains the hardware BSP.
    |
    +-ZC702_hw_platform  The hardware description.


```

与目录结构体有关的注意事项：

* ZC702_hw_platform 和 RTOSDemo_bsp 目录中包含的项目
 是选择 ZC702 作为适用于新项目的目标硬件时，由 SDK 默认生成的
 。
* RTOSDemo 目录只包含特定
 于 Zynq 演示的源文件。FreeRTOS 源文件以及
 实现所有演示应用程序中常见任务的源文件位于
 [目录树中的其他位置](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)。
 因此，仅当默认目录结构
 未改变的情况下可被创建。另请参阅相关页面，了解
 [如何在 Eclipse 项目资源管理器中
 使用虚拟路径和链接路径](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)。

---

### Zynq-7000 SoC 演示应用程序

### 功能

常量 mainSELECTED_APPLICATION 定义 (#define) 位于
main.c 顶部，用于在简单的 Blinky 样式演示、更全面的
测试和演示应用程序以及 lwIP 演示间进行切换，如
下列两章节所述。

### mainSELECTED_APPLICATION 设置为 0 时的功能

如果 mainSELECTED_APPLICATION 设置为 0，则 main() 将调用
main_blinky()，此函数在 main_blinky.c 中实现。

main_blinky() 创建一个非常简单的演示，包括两个任务和一个队列。
一个任务反复将值 100 通过队列发送到另一个任务。
每次收到消息时，接收任务都会切换一次 LED。消息
每 200 毫秒发送一次，因此 LED 每 200 毫秒切换一次。

### mainSELECTED_APPLICATION 设置为 1 时的功能

如果 mainSELECTED_APPLICATION 设置为 1，则 main() 会调用 main_full()，
在 main_full.c 中实现。

![FreeRTOS ARM Cortex-A9](/media/2018/SampleCLISession.png)
main_full() 会创建一项综合测试和演示应用程序
以展示：

* [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口。
* RTOS正在使用[静态分配和动态分配RAM](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)的对象被创建。
* [直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。

通过 USB 到 UART bridge USB 迷你连接器（使用 115200 baud 的传输速率）连接到 FreeRTOS-Plus-CLI
。在 CLI 中键入 "help" ，查看已注册命令列表。

演示创建的大多数任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务。这些任务由所有 FreeRTOS 演示应用程序使用，
且它们除了演示如何使用 FreeRTOS
测试 RTOS 内核端口以外，没有特定功能或用途。

除标准演示任务外，还创建了以下任务：

* 寄存器测试任务

 这两个任务用于测试 RTOS 内核的上下文切换机制，首先
 填充每个具有已知和唯一值的 Cortex-A9 寄存器（包括浮点寄存器）
 ，然后反复检查
 原本写入寄存器的该值是否保持在寄存器中，且全程
 保持不变。任务以尽可能低的优先级执行
 （空闲优先级），因此会频繁被抢占。寄存器检查任务的性质
 要求其必须以汇编方式编写。
* 中断嵌套测试任务

 使用两个定时器从中断中测试 FreeRTOS 队列，中断
 嵌套到 3 的深度（包括 RTOS tick 中断）。第三个
 定时器被配置用于生成 20KHz 中断，其优先级
 高于最大系统调用中断优先级（最大
 系统调用中断优先级在["运行
 FreeRTOS于 Cortex-A9"](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)页面予以解释） - 产生
 嵌套总深度为 4 的测试中断。

 高频定时器也用作方便的时间源，用于
 收集[运行时间统计数据](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)。
 可使用 CLI 查看所收集的统计数据。
* “检查”任务

 检查任务可定期查询标准演示任务和
 寄存器测试任务，以确保其正常工作。此外，检查
 任务也会切换 LED，以给出系统状态的视觉指示
 。
 **如果 LED 每 3 秒切换一次，则表示检查任务未发现执行演示存在
 任何问题。如果 LED 每 200 毫秒切换一次，
 则表示检查任务在至少一个任务中发现问题。**

### mainSELECTED_APPLICATION 设置为 2 时的功能

如果将 mainSELECTED_APPLICATION 设置为 2，则 main() 将调用 main_lwIP()，
其在 main_lwIP.c 中实现。

lwIP 示例可以被配置为使用静态或动态 IP
地址：

* 要使用动态分配的IP地址，请将 LWIP_DHCP 在
 lwipopts.h 中设置为 1，并将目标连接到包含 DHCP 服务器的网络
 。获得的 IP 地址将被打印到 UART 控制台。
* 要使用静态 IP 地址，请在 lwipopts.h 中将 LWIP_DHCP 设置为 0，并
 使用
 FreeRTOSConfig.h底部从 configIP_ADDR0 到 configIP_ADDR3 的常量设置静态 IP 地址。用于定义
 网络掩码的常量也位于 FreeRTOSConfig.h 底部。所选的
 IP 地址和网络掩码必须与
 嵌入目标将连接的网络兼容。这通常可以
 通过设置目标 IP 地址和网络掩码的前三个八进制位以
 分别匹配主机 IP 地址和网络掩码的前三个八进制位来实现
 。所选 IP 地址在网络上必须唯一。

如果目标和主机系统直接连接（未通过集线器或交换机），
则必须使用交叉（点对点）以太网电缆。

当正确连接时，演示将使用 lwIP 套接字 API 创建
一个 FreeRTOS-Plus-CLI 命令控制台，并使用 lwIP 原始 API 创建一个
基础 HTTP 网络服务器。服务器端包含 (SSI) 功能用于生成
服务网页中的动态数据。
要连接到 HTTP 服务器，只需将目标的 IP 地址键入
Web 浏览器的地址栏。

要连接到 FreeRTOS-Plus-CLI，请打开命令提示符，然后输入 `telnet <ipaddr>`，
其中 `<ipaddr>` 是目标的 IP 地址。连接后键入 "help"，
查看已注册命令列表。请注意，此示例并不实现
真正的 telnet 服务器，只是使用 telnet 端口编号，轻松
使用 telnet 工具完成连接。

### 硬件设置

演示使用默认硬件配置。

当使用底部边缘上的集成 Digilent JTAG 模块查看主板时，
所有五向启动选择开关都必须切换到右手边
。由此可通过 JTAG 启动。

---

### 构建说明

### 将演示应用程序项目导入 SDK Eclipse 工作区

要将 Xilinx 软件开发套件 (SDK) 项目导入现有或全新 Eclipse 工作区，请执行以下操作：

1. 从 SDK 的 "File" 菜单中选择 "Import"。将出现如下所示的
 对话框。如图所示，选择 "General->Existing Project into Workspace"。

![将 Xilinx MicroBlaze RTOS 演示项目导入 SDK](/media/2018/Importing-the-Xilinx-MicroBlaze-RTOS-demo-project-into-the-SDK.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702
 作为根目录。然后，确保 RTOSDemo、 RTOSDemo_bsp和
 ZC702_hw_platform 项目在 "Projects" 区中已勾选，
 **并且确保未勾选 'Copy Projects Into
 Workspace' 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![将免费的 ARM Cortex-A9 RTOS 演示源项目导入 Xilinx SDK](/media/2018/Importing-Zynq-projects-into-the-SDK.jpg)

**确保勾选了全部三个项目，不勾选 "Copy projects into workspace"**
3. 导入全部三个项目后，SDK IDE 的项目资源管理器窗口
 将如下图所示。

 ZC702_hw_platform 和 RTOSDemo_bsp 项目是
 RTOSDemo 项目的依赖项目，因此只需要明确构建 RTOSDemo 项目即可。

![在 Eclipse 项目浏览器中查看的 Cortex-A9 RTOS项目。](/media/2018/Zynq-projects-in-the-project-explorer.jpg)

**导入工作区的全部三个项目**

### 构建演示应用程序

1. 打开项目的 main.c 文件，并设置 mainSELECTED_APPLICATION，
 根据需要生成简单的 blinky 演示、完整的测试和演示
 或 lwIP 以太网示例（视需要而定）。
2. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。应用程序应
 成功构建，没有任何错误或警告。

**注意：**截至本文撰写之时，
SDK 中的依赖关系管理有一处故障。如果对头文件进行编辑，则必须
对整个项目进行完全清洁和重新构建，以使变更生效。未完成上述操作
将导致似乎无法解释的运行时间行为。

### 启动调试会话

1. 确保 ZC702 评估板通过其
 板载 Digilent JTAG 端口联通电源并连接至主机。
2. 在 IDE 的 "Run" 菜单中选择 "Debug Configurations..."。屏幕上会
 出现调试配置对话框。双击
 "Xilinx C/C++ application (System Debugger)" 创建新的调试
 配置。
3. 如下图所示配置 "Target Setup" 选项卡。

![ARM Cortex-A9 目标设置选项卡](/media/2018/Zynq_target_setup_tab.jpg)

**Target Setup 选项卡上的所需设置**
4. 如下图所示配置 "Application" 选项卡。

![ARM Cortex-A9 RTOS应用程序选项卡](/media/2018/Zynq_application_tab.jpg)

**Application 选项卡上的所需设置**

 "Debug Configurations" 对话框中的所有其他选项卡均可保留
 默认设置。
5. 单击 "Debug" 按钮开始调试。应用程序将
 下载到 RAM，调试器会在进入 main() 时中断。

---

### RTOS 配置和使用详情

### FreeRTOS ARM Cortex-A 移植特定配置

请注意！请参阅
[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS 的说明](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)页面，
特别注意
configMAX_API_CALL_INTERRUPT_PRIORITY 设置的值和含义，**以及**
关于与 GCC 一同使用浮点单元的特别注释。

此演示的特定配置项目位于/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702/RTOSDemo/src/FreeRTOSConfig.h。
[可以编辑此文件中定义的常量，以适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

### 中断向量表

默认情况下，SDK 项目会将中断向量表定义为 BSP 的一部分。这会
增加安装 FreeRTOS 处理程序
（具体方法详见[“在 ARM Cortex-A 嵌入式处理器上
运行 FreeRTOS”页面](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)）的难度。因此，此演示
会在 FreeRTOS_asm_vectors.S 中定义自己的中断向量表。
由 BSP 定义的向量表
会在运行时替换为 FreeRTOS_asm_vectors.S 中定义的向量表，这是通过调用 vPortInstallFreeRTOSVectorTable() 来实现的，
在演示中，这一步在 prvSetupHardware() 函数中完成。

FreeRTOS_asm_vectors.S 中定义的向量表放置在
名为 .freertos_vectors 的链接器区段中，而链接器脚本 lscript.ld
会将 .freertos_vectors 区段放置在 .text 区域的开头。

### [应用程序定义的]中断服务程序

此演示使用 Xilinx 提供的驱动程序来配置中断控制器，
并安装应用程序定义的中断。示例位于
FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702/RTOSDemo/src/Full_Demo/serial.c 和
FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702/RTOSDemo/src/Full_Demo/IntQueueTimer.c 中。

Xilinx 驱动程序需要中断
服务程序 (ISR) 来接受 void * 参数，但是该参数
并不总是使用。因此，所需的 ISR 原型为：

```c

    void Interrupt_Handler( void *pvUnusedParameter );

```

serial.c 中名为 prvUART_Handler() 的中断处理程序
提供了一个不使用其参数的中断处理程序示例。本
IntQueueTimer.c 中名为 prvTimerHandler() 的中断处理程序
提供了一个使用其参数确定
由哪个外围设备生成中断的中断示例。在这种情况下，可安装相同的中断处理程序实现，
并将其作为多个定时器的处理程序。

如果某任务的优先级等于或高于当前正在执行的任务，
并因 ISR 而解除阻塞状态，则 ISR 必须请求上下文切换，
方可退出。此时，中断服务程序会中断一项 RTOS 任务，
但返回另一项 RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）可用于
从 ISR 内部请求上下文切换。
下列源代码片段仅作为示例提供。ISR 示例
使用信号量与任务（未显示）同步，并调用 portYIELD_FROM_ISR()
以确保中断直接返回任务。引用的 prvUART_Handler()
和 prvTimerhandler() 函数提供了更多示例。

```c

void Dummy_IRQHandler( void *pvUnusedInThisExample )
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* The parameter is not used in this case. */
    ( void ) pvUnusedInThisExample;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to pdFALSE. */
    [xSemaphoreGiveFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than or equal to the currently Running task (the task that this
 interrupt interrupted), then lHigherPriorityTaskWoken will have been set to
 pdTRUE internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portYIELD_FROM_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
从中断服务程序中调用，并且中断的优先级必须
小于或等于 configMAX_API_CALL_INTERRUPT_PRIORITY
配置常量设置的优先级（即数值更大）。

### FreeRTOS使用的资源

相关信息请参阅[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors) 页面。
此演示配置为从 SCU 定时器生成滴答中断。

### 内存分配

ARM Cortex-A 演示应用程序项目中包含的 Source/Portable/MemMang/heap_4.c 可用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
