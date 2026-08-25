---
title: "ARM Cortex-R5 Xilinx UltraScale MPSoC"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


![具有 4 个 64 位 ARM Cortex-A53 核心和 2 个 32 位 ARM Cortex-R5 实时核心的 Xilinx UltraScale MPSoC](/media/2018/UltraScale_MPSoC_Schematic.png)

**[Xilinx SDK](https://www.xilinx.com/products/design-tools/legacy-tools/sdk.html)
 （软件开发工具包）包含创建 FreeRTOS 项目的向导，适用于 
 [Zynq UltraScale MPSoC](http://www.xilinx.com/products/technology/ultrascale-mpsoc.html) 上的所有核心，包括 ARM Cortex-A53（64 位）、ARM Cortex-R5 和 Microblaze 处理器。**


### 引言

本页记录的 FreeRTOS 演示应用程序面向 ARM CORTEX-R5 核心，
位于 Xilinx Zynq UltraScale+ MPSoC 上。针对同一设备上的
64 位 ARM Cortex-A53 核心的类似项目[单独提供](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-UltraScale_MPSoC_64-bit)。

本演示使用独立的 BSP
（由 SDK 生成的板级支持包），并将 FreeRTOS 构建为
应用程序的一部分。硬件设计项目针对 Xilinx ZCU102
评估板。

FreeRTOS 也作为 Xilinx SDK 包的一部分分发，
SDK 包含为 UltraScale+ MPSoC 的 64 位 ARM Cortex-A53、ARM Cortex-R5 和 Microblaze 核心生成 FreeRTOS 的向导
。如果使用 SDK 向导创建 FreeRTOS 项目，
则 FreeRTOS 将构建为 BSP 的一部分，而非应用程序的一部分。
有关创建 FreeRTOS BSP 的说明，[
请参阅本页内容](#构建说明使用独立-bsp)。



ARM CORTEX-R5 FreeRTOS 移植可实现完全中断嵌套模型，
并支持向量浮点单元 (VFP/FPU)。


---


### 重要！使用 FreeRTOS ARM Cortex-R5 移植的注意事项


*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#功能)
3. [构建说明](#构建说明使用独立-bsp)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)


另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting/#freertos-faq---my-application-does-not-run-what-could-be-wrong)”，以及
“[ARM Cortex-A 嵌入式处理器上 FreeRTOS 的使用说明](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)”页面，
因为关于在 ARM Cortex-A 核心上运行 RTOS 的信息也适用于
在 ARM Cortex-R 核心上运行 RTOS 的情况。


---




### 源代码组织



FreeRTOS 下载内容包含所有 RTOS 移植的源代码及
所有 RTOS 演示应用程序，因此下载内容包含的源文件
远多于使用 Zynq UltraScale+ Cortex-R5 MPSoC 移植和演示应用程序所需的源文件
。
请参阅本网站的[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解相关下载文件。

ARM Cortex-R5 演示应用程序使用的目录结构体
如下所示。根目录 CORTEX_R5_UltraScale_MPSoC
位于 FreeRTOS/Demo 中。



```c

CORTEX_R5_UltraScale_MPSoC
  |
  +-RTOSDemo_R5               Contains the SDK project and C files specific to the demo.
  |
  +-RTOSDemo_R5_bsp           Contains the hardware board support package.
  |
  +-ZynqMP_ZCU102_hw_platform The ZCU102 hardware description.


```



与目录结构有关的注意事项：


* ZynqMP_ZCU102_hw_platform 和 RTOSDemo_R5_bsp 目录中的项目
 由 Xilinx SDK 创建。
* RTOSDemo_R5 目录只包含
 Zynq UltraScale+ MPSoC 演示特定的源文件。FreeRTOS 源文件以及
 实现所有演示应用程序中常见任务的源文件位于
 [目录树中的其他位置](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)。
 项目仅会在默认目录结构体
 未改变的情况下创建。另请参阅相关页面，了解
 [如何在 Eclipse 项目资源管理器中
 使用虚拟路径和链接路径](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)。









---


### Zynq UltraScale+ MPSoC ARM Cortex-R5 演示应用程序


### 功能


常量 mainSELECTED_APPLICATION 定义 (#define) 在
main.c 的顶部，用于在基本和简单 Blinky 样式演示以及
更全面的测试和演示应用程序之间切换。





### mainSELECTED_APPLICATION 设置为 0 时的功能


如果 mainSELECTED_APPLICATION 设置为 0，则 main() 将调用
main_blinky()，会在 main_blinky.c C 源文件中实现。

main_blinky() 实现了使用两个任务和一个队列的简单示例。
一个任务使用队列将值 100 重复发送到另一个任务。
接收任务在每次收到消息后会将消息打印到 USB UART 端口 (J83)，
使用的波特率为 115200。



任务每隔 200 毫秒发送值 100 至队列，因此
每 200 毫秒将消息打印至 UART。







### mainSELECTED_APPLICATION 设置为 1 时的功能


如果 mainSELECTED_APPLICATION 设置为 1，则 main() 会调用 main_full()，
会在 main_full.c C 源文件中实现。

main_full() 会创建一个综合应用程序，此程序会测试 RTOS 移植，
及演示：


* [直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
* [使用静态和动态分配的内存创建的 RTOS 对象](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。


由综合演示创建的大多数任务来自一组
[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务，适用于所有 RTOS
演示应用程序。这些任务没有特定功能或目的，仅为
演示所使用的 FreeRTOS API，测试 RTOS 架构和编译器
移植。

此演示还创建了以下任务：


* 中断嵌套测试任务

 使用定时器测试中断嵌套，并测试嵌套中断使用的 RTOS 队列
 。演示会从 TTC 定时器 0 生成 RTOS tick 中断，
 因此中断嵌套测试使用 TTC 定时器 2、3 和 4。
* 寄存器测试任务

 寄存器测试任务会测试 RTOS 上下文切换机制。任务
 首先用已知的唯一值填充所有 ARM Cortex-R5 ALU 和 FPU 寄存器，
 然后反复检查
 最初写入寄存器的值是否在任务有效期内
 保持不变。寄存器检查任务的性质
 决定了它们必须用汇编代码
 编写。
* “检查”任务

 检查任务会定期查询标准演示任务和
 寄存器检查任务，以确保其仍在如期执行和运行，
 然后将状态消息打印到 USB UART (J83)。
 其传输速率为 115200 baud。






![在 Zynq UltraScale+ MPSoC 的 ARM Cortex-R5 核心上执行 RTOS 演示时生成的输出结果](/media/2018/Zynq_UltraScale_free_RTOS_demo_output.png)



**完整演示生成的输出结果**







### 硬件设置


将演示配置为通过 JTAG 接口下载并运行生成的可执行文件
。为启动 JTAG，SW6 库上的所有四个开关都需
设置为朝向板的中央。







---


### 构建说明——使用独立 BSP


本部分介绍了如何构建上文描述的演示，
该演示可在官方 FreeRTOS 下载中找到。接下来的部分将介绍
如何使用 Xilinx SDK 创建项目，在这种情况下，FreeRTOS 源
文件将构建为 BSP 的一部分。



### 将 RTOS 演示项目导入 SDK Eclipse 工作区



要将 Xilinx 软件开发工具包 (SDK) 项目导入现有或全新 Eclipse 工作区：



1. 从 SDK 的 "File" 菜单中选择 "Import"。将出现如下所示的
 对话框。如图所示，选择 "General->Existing Project into Workspace"。



![将 Xilinx MicroBlaze RTOS 演示项目导入 SDK](/media/2018/Importing-the-Xilinx-MicroBlaze-RTOS-demo-project-into-the-SDK.jpg)



**首次单击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_R5_UltraScale_MPSoC
 作为根目录。然后，确保 RTOSDemo_R5、RTOSDemo_R5_bsp 和
 ZynqMP_ZCU102_hw_platform 项目在 "Projects" 区内被选中，
 **并且确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。




![将免费的 ARM Cortex-R5 RTOS 演示源项目导入 Xilinx SDK](/media/2018/Import_ARM_Cortex_R5.png)



**确保勾选所有三个项目，不勾选 "Copy projects into workspace"**
3. 导入所有三个项目后， SDK IDE 的项目资源管理器窗口
 将显示如下。

 ZynqMP_ZCU102_hw_platform 和 RTOSDemo_R5_bsp 项目是
 RTOSDemo_R5 项目的依赖项，因此只需要显式构建 RTOSDemo_R5 项目。






![在 Eclipse 项目资源管理器中查看 ARM Cortex-R5 RTOS 项目。](/media/2018/ARM_Cortex-R5_projects-in-the-project-explorer.png)



**导入工作区的所有三个项目**






### 构建演示应用程序 RTOS


1. 打开项目的 main.c 文件，并设置 mainSELECTED_APPLICATION，
 根据需要生成简单的 blinky 演示，或完整的测试和演示
 应用程序。
2. 在 Eclipse IDE 的 "Project" 菜单中选择 "Rebuild All"。






### 启动调试会话


1. 确保 ZCU102 目标硬件通电，
 并使用适当的调试接口将其连接到主计算机。
2. 确保 SW6 排上的所有四个开关都设置为朝向
 板的中心。由此可启动 JTAG。
3. 在 IDE 的 "Run" 菜单中选择 "Debug Configurations..."。屏幕上会
 出现调试配置对话框。双击
 "Xilinx C/C++ application (System Debugger)" 创建新的调试
 配置。
4. 如下图所示配置 "Target Setup" 选项卡。




![ARM Cortex-R5 RTOS 演示 Eclipse 的 "Target Setup" 选项卡](/media/2018/MPSoC_ARM_Cortex_R5_Eclipse_target_setup_tab.png)



**Target Setup 选项卡上的所需设置**
5. 如下图所示配置 "Application" 选项卡。




![ARM Cortex-R5 RTOS 演示 Eclipse 的 "Application" 选项卡](/media/2018/MPSoC_ARM_Cortex_R5_Eclipse_application_tab.png)



**Application 选项卡上的所需设置**





 "Debug Configurations" 对话框中的所有其他选项卡均可保留
 默认设置。
6. 单击 "Debug" 按钮开始调试。应用程序将
 下载到 RAM，调试器会在进入 main() 时中断。这
 可能需要在 Debug 窗口中选择正确的 ARM Cortex-R5 核心，
 目的是查看正确的源代码，并使用调试
 控制。




![选择 ARM Cortex-R5 核心调试 RTOS 项目](/media/2018/Selecting_the_ARM_Cortex-R5_core.png)



**在 Debug 窗口中选择 ARM Cortex-R5 0 核心**


---


### 构建说明——创建 FreeRTOS BSP


[上一节](#构建说明使用独立-bsp)介绍了如何构建
主要 FreeRTOS zip 文件下载中的 RTOS 项目。
FreeRTOS 还配备了 Xilinx SDK。本部分介绍了如何
使用 SDK 为 ARM Cortex-R5 核心创建FreeRTOS 项目。
###
 创建新的 FreeRTOS 项目


1. 从 SDK 的 "File" 菜单中选择 "New->Application Project"。将
 出现 "New Project" 对话框。


![创建一个新的 RTOS 项目](/media/2018/SDKNewApplicationProject.jpg)


**选择 "New Application Project" 菜单项**
2. 在 "New Project" 对话框中，首先选择 "psu_cortexr5_0" 作为
 处理器，然后根据需要选择硬件平台，最后
 选择 freertos 作为操作系统平台，然后单击 "Next"。此时会出现 "New Project
 Templates" 对话框。


![创建 ARM Cortex-R5 RTOS 项目所需的 "New Project" 设置](/media/2018/Free_RTOS_Cortex-R5.png)


**所需的 New Project 对话框设置**
3. 选择 FreeRTOS Hello World 模板，然后单击 "Finish"。SDK
 将创建硬件描述项目、BSP 项目和应用程序
 项目。FreeRTOS 源代码将构建为 BSP 的一部分。


![适用于 ARM Cortex-R5 RTOS 移植的 RTOS 模板](/media/2018/sdk_rtos_template.jpg)


**选择 FreeRTOS 模板**


### 配置 FreeRTOS BSP


官方 FreeRTOS 演示使用独立的 BSP，并将 FreeRTOS 构建为
应用程序的一部分。此时，要对 FreeRTOS 进行配置，需手动编辑
[FreeRTOSConfig.h 头文件](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

SDK 创建的项目
（如前所述）会将 FreeRTOS 构建为 BSP 的一部分。此时，
FreeRTOSConfig.h 头文件无需手动编辑，而是要对 FreeRTOS进行配置，
使用 SDK 环境中的对话框。


1. 按照上述说明，通过 SDK 创建 FreeRTOS Hello World
 应用程序。
2. 从 SDK 的 “Xilinx Tools” 菜单中选择 "Board Support Package Settings"。
 会显示 "Board Support Package Settings" 对话框。
3. 在 "Board Support Package Settings" 对话框的左侧窗格中选择 freertos，
 然后使用同一对话框右侧窗格中的表格，根据需要配置
 FreeRTOS。


![在 Xilinx SDK 中配置 RTOS](/media/2018/configure_freertos_sdk.jpg)



**使用 Board Support Package Settings 对话框配置 FreeRTOS**


---


### RTOS 配置和使用详情

### FreeRTOS ARM CORTEX-R 移植特定配置


请注意！
[有关在 ARM Cortex-A
 核心上运行 RTOS 的信息，另有专门页面介绍](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)。该页面上的信息也适用于在 ARM Cortex-R 核心上运行 RTOS
。
需特别注意
configMAX_API_CALL_INTERRUPT_PRIORITY 设置的值和含义。

本演示的特定配置项位于 /FreeRTOS/Demo/CORTEX_R5_UltraScale_MPSoC/RTOSDemo_R5/src/FreeRTOSConfig.h 中。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。


### 中断向量表


默认情况下，SDK 项目会将中断向量表定义为 BSP 的一部分。这会
增加安装 FreeRTOS 处理程序
（具体方法见[“在 ARM Cortex-A（和 ARM Cortex-R）
嵌入式处理器上运行 FreeRTOS”](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)页面）的难度。因此，本演示
会在 FreeRTOS_asm_vectors.S 中定义自己的中断向量表，并且
链接器脚本包含一个编辑，目的是确保使用 FreeRTOS 向量表，
而非使用 BSP 定义的向量表。


### [应用程序定义的]中断服务程序


此演示使用 Xilinx 提供的驱动程序来配置中断控制器，
并安装应用程序定义的中断。示例请参见
FreeRTOS/Demo/CORTEX_R5_UltraScale_MPSoC/RTOSDemo_R5/src/Full_Demo/IntQueueTimer.c，
其中实现并安装了中断嵌套测试使用的中断服务程序
。

Xilinx 驱动器需要中断
服务程序 (ISR) 来接受 void * 参数，但是该参数
并不总是使用。因此，所需的 ISR 原型为：


```c

    void Interrupt_Handler( void *pvUnusedParameter );

```


如果 ISR 使得一个比当前执行的任务具有相等或更高优先级的任务
并因 ISR 而解除阻塞状态，则 ISR 必须请求上下文切换，
方可退出。此时，中断服务程序会中断一项 RTOS 任务，
但返回另一项 RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）可用于
从 ISR 内部请求上下文切换。
下列源代码片段仅作为示例提供。ISR 示例
使用直达任务通知以同步任务（未显示），并调用 portYIELD_FROM_ISR()，
以确保中断直接返回到任务。


```c

void Dummy_IRQHandler( void *pvUnusedInThisExample )
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* The parameter is not used in this case. */
    ( void ) pvUnusedInThisExample;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A direct to task notification is used for this
 purpose. Note lHigherPriorityTaskWoken is initialised to pdFALSE. */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task referenced by xTaskToNotify was blocked waiting for the
 notification, and sending the notification caused the task to unblock, and
 the unblocked task has a priority higher than or equal to the currently
 Running task (the task that this interrupt interrupted), then
 lHigherPriorityTaskWoken will have been set to pdTRUE internally within
 vTaskNotifyGiveFromISR(). Passing pdTRUE into the portYIELD_FROM_ISR() macro
 will result in a context switch being pended to ensure this interrupt returns
 directly to the unblocked, higher priority, task. Passing pdFALSE into
 portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```


只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
从中断服务程序中调用，并且中断的优先级必须
小于或等于 configMAX_API_CALL_INTERRUPT_PRIORITY
配置常量设置的优先级（即数值更大）。


### FreeRTOS 使用的资源


相关信息请参阅“[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)”页面。
本演示项目被配置为从 TTC channel 0 生成 tick 中断。


### 内存分配


本演示使用的 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 头文件同时定义了
[configSUPPORT_STATIC_ALLOCATION 和 configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)，
，本演示展示了这两种方法的使用。 
Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-R5 演示应用程序项目中，用于提供
使用动态内存分配创建对象时所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。


### 其他事项


请注意，vPortEndScheduler() 尚未实现。
