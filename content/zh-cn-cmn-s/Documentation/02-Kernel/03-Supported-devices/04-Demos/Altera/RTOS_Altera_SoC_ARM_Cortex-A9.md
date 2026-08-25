---
title: "Altera Cyclone V SoC RTOS 演示 (ARM Cortex-A9)"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Cyclone V SoC 开发套件](/media/2018/cyclonev_soc_with_Cortex-A9.jpg)

### 简介

本页记录了 Cortex-A9 核心的 FreeRTOS 演示应用程序，该核心使用于
[Altera Cyclone V SoC](https://www.intel.com/content/www/us/en/products/details/fpga/cyclone/v.html)
硬处理系统 (HPS)。

该项目使用基于 ARM DS-5 Eclipse 的免费 Altera 版本 IDE 与 GCC 编译器进行构建，
两者均为
[Embedded Software and Tools for Intel® SoC FPGA](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html#tab-blade-1-1)
(EDS) 的部分组件。请注意，仅使用 EDS 的 DS-5 和编译器组件，
无需安装任何 FPGA 工具来构建或使用本 RTOS 演示。

该项目已预配置为在
[Cyclone V SoC Development Kit](https://www.intel.com/content/www/us/en/products/details/fpga/development-kits/cyclone/v-sx.html)
硬件上执行。

[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 用于创建命令控制台。 

---

#### *重要提示！FreeRTOS Cyclone V SoC ARM Cortex-A9 演示*使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#altera-cyclone-v-soc-arm-cortex-a9-演示应用程序)
3. [构建说明](#构建说明)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)以及
[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS 的说明](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md)页面。

---

### 源代码组织

FreeRTOS .zip 文件下载中仅有一小部分文件
需用于 Altera Cyclone V SoC 演示。[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面描述
FreeRTOS zip 文件下载的结构体。

ARM DS-5 Eclipse 项目文件位于 FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK 目录下
。请注意，RTOS 项目包括
/FreeRTOS-Plus 目录下的文件，因此如果
/FreeRTOS-Plus 目录已删除或目录结构已变更，则无法构建项目
。

---

### Altera Cyclone V SoC ARM Cortex-A9 演示应用程序

#### 硬件和软件设置

尽管此页面上显示的 RTOS 演示已被预先配置为
在 Altera Cyclone V SoC 开发套件上运行，但它可以很快地适应在任何
支持访问 UART 和 LED 的 Cyclone V SoC 评估板上运行。
* **UART**

 UART 用于控制台 IO。下载中的演示使用了 UART 0 来实现
 此用途。UART 0 使用了 UART 到 USB 转换器，
 因此采用 USB 数据线进行连接。

 如您需要使用 UART 0 以外的 UART，则需相应更新
 FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK/Altera_Code/SoCSupport/uart0_support.c 
 源文件。
* **LED 数字输出**

 数字输出用于切换 LED。如果需要使用
 不同的数字输出，则更新 FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK/LEDs.c
 。

#### 功能

演示中的行为由 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 的
\#define 常量定义，其声明位于 main.c 顶部。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky 函数。

main_blinky() 函数创建一个简单的演示，其中包括两个
[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview)和一个[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
一个任务通过队列将值 100 反复
发送到另一个任务。每次接收消息时，接收任务都会切换一次
LED。消息每 200 毫秒发送一次，因此 LED 的状态将
每 200 毫秒切换一次。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

![在 ARM Cortex-A9 上使用 RTOS CLI MPU](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

 CLI 会话示例

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：
* [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [事件组](FreeRTOS-Event-Groups.md)。

使用 115200 baud 的传输频率通过 UART 连接到 FreeRTOS-Plus-CLI。在 CLI 中键入 "help"
查看已注册命令列表。

演示创建的大多数 RTOS 任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
RTOS 任务集。这些任务由所有 FreeRTOS 演示应用程序使用，
且它们除了演示如何使用 FreeRTOS
API 函数并测试 RTOS 内核移植之外，没有特定的功能或目的。

演示项目还创建了一个“检查” 任务。 RTOS检查任务可定期查询标准演示任务，
确保其按预期运行。此外，检查任务还会
切换 LED，以给出系统状态的视觉指示。
**如果 LED 每 3 秒切换一次，则表示检查任务未发现执行演示存在
任何问题。如果 LED 每 200 毫秒切换一次，
则表示检查任务在至少一个任务中发现问题。**

---

### 构建说明

请注意，ARM DS-5 Eclipse 项目[同时使用虚拟文件夹和链接](Project_Workspace_Relative_File_Paths_Eclipse.md)，
这些虚拟文件夹和链接引用了 /FreeRTOS-Plus 和 /FreeRTOS/Demo/Common 目录下的文件
。因此，在 Eclipse 项目浏览器中查看的[虚拟]文件结构体与
磁盘上查看的[实际]文件结构体不一致。
1. 打开 ARM DS-5 Eclipse IDE 新建工作区或选择一个现有的
 工作区。
2. 在 IDE 的 "File" 菜单中选择 "Import"，
 打开导入对话框。
3. 在 "Import" 对话框中，选择 "General->Existing Projects Into Workspace"，
 然后浏览并选中 FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK
 目录。您将看到一个名为 "RTOSDemo" 的项目。
4. 确保 RTOSDemo 已勾选，**且 Copy Projects Into Workspace 选项
 在**点击 "Finish" 之前未勾选。

 ![将 RTOS 演示项目导入 ARM DS-5 Eclipse 工作区](/media/2018/importing_RTOS_into_Altera_Eclipse.png)

 将 RTOSDemo 导入 Eclipse 工作区，**无需**
 将其复制到工作区。
5. 当
 [Altera EDS](https://www.intel.com/content/www/us/en/software-kit/665453/intel-soc-fpga-embedded-development-suite-soc-eds-pro-edition-software-version-18-1-for-windows.html) 安装后，
 用于构建项目的 GCC 编译器也一同安装完毕。需要更新项目以设置编译器的
 位置。

 在 IDE 的 "Project" 菜单中选择 "Properties"，以弹出
 属性对话框。在对话框中选择 "C/C++Build->Settings->
 Cross Settings"，然后将编译器路径设置为适合安装的路径
 。

**注意：**如果下图所示的对话框选项卡
 缺失或包含错误消息，则说明
 您的 DS-5 版本可能未安装 CDT 交叉编译器插件。
 在这种情况下，可以通过以下方式手动安装插件：
 [按照ARM 网站上提供的说明操作](http://ds.arm.com/developer-resources/tutorials/adding-custom-gcc-toolchains-to-ds-5/)。
 须在上述插件安装后新建工作区。

![设置构建 RTOS](/media/2018/Setting_the_path_to_the_Altera_compiler.png) 的编译器的路径

 在 RTOS 项目的属性对话框中设置编译器的路径
6. 打开 main.c 并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
7. 确保已使用合适的调试接口将目标硬件
 连接至主机。Cycle V SoC 开发套件已具有
 它的 BitBlaster 接口。也可以使用其他调试接口（如 ARM 的 D-Stream）
 。
8. 在 IDE 的 "Project" 菜单中选择 "Build All"。
9. 构建完成后，
 从 IDE 的 "Debug" 菜单中选择 "Debug Configurations..."，
 配置和运行适合您所选连接方法（如 BitBlaster、D-Stream 等）的调试配置。
 下方可点击的屏幕截图显示了使用 D-Stream 调试器的
 配置。**注意第三个屏幕截图中的预加载器脚本选择。**

[![D-stream Cortex-A 调试配置](/media/2018/D-Stream_Cortex-A_CycloneV.jpg)](/media/2018/D-Stream_Cortex-A_CycloneV.jpg)
[![D-stream Altera Cortex-A 调试配置](/media/2018/D-Stream_Cortex-A_CycloneV_2.jpg)](/media/2018/D-Stream_Cortex-A_CycloneV_2.jpg)
[![Altera 使用 ARM 的 DS-5 进行 SoC 调试](/media/2018/D-Stream_Cortex-A_Cyclone_3.jpg)](/media/2018/D-Stream_Cortex-A_Cyclone_3.jpg)

**点击图像放大**

---

### RTOS 配置和使用详情

#### FreeRTOS ARM Cortex-A 移植特定配置

请注意！请参阅
[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS 的说明](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md)，
请特别注意
configMAX_API_CALL_INTERRUPT_PRIORITY 设置的值和含义。

在此演示中，configSETUP_TICK_INTERRUPT 被定义为调用 vConfigureTickInterrupt()，
此调用在 main.c 中实现。vApplicationIRQHandler() 也在
main.c 中实现。

此演示特定的配置项目位于 [FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK/FreeRTOSConfig.h]().
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

#### [应用程序定义的]中断服务程序

此演示使用 Altera 提供的驱动器来配置中断控制器，但
由于在其定义源文件范围之外无法访问驱动器本身的中断表
，所以使用了一个 FreeRTOS 特定函数来实际寄存中断
句柄。vRegisterIRQHandler() 即用于此用途，并
在 main.c 中实现。

```c

/*  

 * ulID - the ID of the interrupt as defined in the Altera provided  

 * alt_interrupt_common.h header file.  

 *  

 * pxHandlerFunction - the C function being registered to handle the interrupt.  

 *  

 * pvContext - a reference to additional data of the application writer's choice  

 * that can be used from within the interrupt handler.  

 */  

void vRegisterIRQHandler( uint32_t ulID,  

                          alt_int_callback_t pxHandlerFunction,  

                          void *pvContext );  

vRegisterIRQHandler() function prototype  

```

C 处理程序本身含有以下原型；

```c

/*  

 * ulICCIAR - the value of the generic interrupt controller's (GIC's) IAR register  

 * at the time the hander is called.  

 *  

 * pvContext - the pointer to additional data for the handler that was passed into  

 * the call to vRegisterIRQHandler() used to register the handler.  

 */  

void vAnISRHandlingFunction( uint32_t ulICCIAR, void *pvContext );  

The prototype of an interrupt handling function that can be registered using vRegisterIRQHandler()  

```

如果 ISR 使得一个比当前执行的任务具有相等或更高优先级的 RTOS 任务
解除阻塞状态（请参阅 pxHigherPriorityTaskWoken 参数的说明，其位于
函数 API 文档，例如
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)），
那么 ISR 必须在 ISR 退出前请求上下文切换
。此时，中断服务程序会中断一个 RTOS 任务，
但会返回到另一个 RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）可用于
从 ISR 内请求上下文切换。
请参阅以下源代码片段示例。ISR 示例
使用信号量与任务（未显示）同步，并调用 portYIELD_FROM_ISR()
以确保中断直接返回到任务。

```c

void Dummy_IRQHandler( uint32_t ulUnused, void *pvUnused )  

{  

long lHigherPriorityTaskWoken = pdFALSE;  

    /* The parameter is not used. */  

    ( void ) ulUnused;  

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

An example interrupt handler  

```

只有以 “FromISR” 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用，而且相应中断的优先级必须
小于或等于 configMAX_API_CALL_INTERRUPT_PRIORITY 配置常量设置的
优先级（即数值较高的值）。

#### FreeRTOS使用的资源

相关信息请参阅[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md) 的页面。
此演示被配置为从 Cortex-A9 核心的专用定时器中生成 tick 中断
。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-A 演示应用程序项目中，用于
为 RTOS 内核分配所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。

