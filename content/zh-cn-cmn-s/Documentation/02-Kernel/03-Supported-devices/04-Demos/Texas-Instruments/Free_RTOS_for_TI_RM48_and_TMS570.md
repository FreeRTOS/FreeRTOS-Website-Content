---
title: "使用 Code Composer Studio 5 的 TI Hercules Safety MCU RTOS 演示 RM48 和 TMS570 (Cortex-R4F)"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RM48 TMDXRM48USB U 盘和 TMS570 TMDX570LS31USB U 盘](/media/2018/Free-RTOS-Hercules.jpg)

### 简介

本页记录的 FreeRTOS 演示应用程序
[用于 RM4](http://www.ti.com/mcu/docs/mcuproductcontentnp.tsp?sectionId=95&familyId=2056&tabId=2841)
和[TMS570](http://www.ti.com/mcu/docs/mcuproductcontentnp.tsp?sectionId=95&familyId=1870&tabId=2824)
安全微控制器，此类安全微控制器产自 [Texas Instruments](http://www.ti.com/) 公司。
此演示应用程序使用 FreeRTOS Cortex-R4 Code Composer Studio (CCS) 移植，
并面向[TMDXRM48USB](http://www.ti.com/tool/tmdxrm48usb)
和 TMS570 [TMDX570LS31USB](https://www.ti.com/product/TMS570LS3137-EP)
U 盘评估板。该项目使用 CCS5 创建。

Hercules RM4x 和 TMS570 安全微控制器系列让客户能够轻松
开发安全关键产品，以满足
ISO 26262 和 IEC 61508 安全标准的要求。此类基于 ARM Cortex-R4
的微控制器提供性能、内存和外设等多个选项。双核
锁步 CPU 架构、硬件 BIST、MPU、ECC 以及片上时钟和电压
监控是一些关键的安全功能，可满足
运输、工业和医疗应用的需求。对于安全关键型应用程序，
可以轻松实现
从 FreeRTOS 到 WITTENSTEIN high integrity systems 完全安全认证的
 [SAFERTOS](http://www.safertos.com/)内核。

---

### *重要提示！关于 FreeRTOS Cortex-R4 CCS 演示项目*的使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#ti-cortex-r4f-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

此页中的[项目目录结构准备](#准备-code-composer-studio-eclipse-项目目录)章节
包含有关准备项目目录的重要信息。

FreeRTOS zip 文件包含所有 FreeRTOS的源文件
移植的源文件以及所有演示应用程序。这些文件中只有一小部分要用于
RM48 和 TMS570 演示应用程序。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
和新项目创建的信息。

RM48 和 TMS570 RTOS 演示项目包含在
FreeRTOS/Demo/CORTEX_R4_RM48_TMS570_CCS5 目录中。此项目
包含以下四个构建配置：

1. RM48 项目，使用仿真（软件）浮点。
2. RM48 项目，使用硬件浮点。
3. TMS570 项目，使用仿真（软件）浮点。
4. TMS570 项目，使用硬件浮点。

![选择RTOS构建](/media/2018/selecting-a-build-configuration-in-CCS.jpg)

**若要选择构建配置，请右键单击项目
 资源管理器中的项目，然后选择“构建配置->设置活动”菜单项。** 

---

### TI Cortex-R4F 演示应用程序

RM48 和 TMS570 演示应用程序具有相同的功能。

### 硬件设置

演示应用程序使用内置在 U 盘评估板上的 LED，
com 测试任务（如下所述）在环回模式下使用 UART。
因此，无需进行硬件设置。

### 功能

演示的行为取决于 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 的设置，
该设置已在 main.c 中定义。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：

* **main_blinky() 函数：** 

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 RTOS 调度器。
* **队列发送任务:** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
 它每隔 200 毫秒向队列发送数值 100。
* **队列接收任务:** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 。它使用指定的非零块时间重复从队列中读取数据
 。如果队列为空，
 会导致任务进入[阻塞状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)
 。每次从队列接收的值为 100 时，任务都切换红色 LED。
 因此，由于队列发送任务每 200 毫秒向队列发送一次，
 队列接收任务退出阻塞状态，
 每 200 毫秒切换一次红色 LED。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：

* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* UART 中断用于演示“任务与中断”以及“中断与任务”之间的通信，
 以及来自中断服务程序的上下文切换
 。

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

main() 创建 43 个任务和 2 个软件定时器，
之后启动 RTOS 调度器。然后，演示在运行期间动态地连续
和删除另外两个任务。

除了标准演示任务外，还在
main_full() 中定义和/或创建了以下任务和测试：

"Check" 定时器：检查软件定时器周期设置为三秒。
与检查软件定时器关联的回调函数不仅检查所有标准演示任务是否仍在执行，
而且还检查执行时
是否报告任何错误。如果检查软件定时器发现
任务已停止，或报错，则记录该错误，
然后检查软件定时器切换红色 LED。如果报告错误锁存，
检查软件定时器将切换绿色 LED。因此，
如果系统正常运行，绿色 LED 将每三秒钟切换一次，
如果检测到错误，则红色 LED 将每三秒钟切换一次
。

"Reg test" 任务：此类任务使用已知值填充核心寄存器和浮点寄存器，
然后检查每个寄存器在任务生命周期内是否保持其期望值
。每个任务使用一组不同的值
。由于 reg 测试任务以非常低的优先级执行，因此经常被抢占
。包含意外值的寄存器指示
上下文切换机制中的错误，
并且将导致检查定时器（如上所述）切换红色 LED。

“LED” 软件定时器：与 LED
软件定时器关联的回调函数保持旋转白色 LED 这一模式。

### 准备 Code Composer Studio (Eclipse) 项目目录

Eclipse 项目既可以是标准 makefile 项目，也可以是托管 make 项目。
RM48 和 TMS570 项目为托管 make 项目。因此意味着
以下两种情况：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

本示例采用第一种。为此，目录FreeRTOS/Demo/CORTEX_R4_RM48_TMS570_CCS5
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件会将所有必需的 FreeRTOS 源文件复制到
演示项目目录内的子目录中。

**CreateProjectDirectoryStructure.bat 必须在将 CCS 项目导入 Eclipse 工作区
之前执行。** 

CreateProjectDirectoryStructure.bat 不能在
在 CCS Eclipse IDE 中执行。

---

### 将演示应用程序项目导入 CCS Eclipse 工作区

要将 Cortex-R4F 项目导入现有或新的 Eclipse 工作区，需完成以下操作：
1. 在 CCS 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Existing Projects into Workspace"。  

![将 Cortex-R4 CCS5 项目导入 Eclipse 工作区](/media/2018/CCS5_import.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_R4_RM48_TMS570_CCS5
 作为根目录。然后，请确保勾选 "Projects" 区域中的 CORTEX_R4_RM48_TMS570_CCS5 项目，
 **并确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态， 
 图片中不包含 "Finish" 按钮）。

![选择要导入 Eclipse 的 FreeRTOSCortex-R4 项目](/media/2018/Code_Composer_Studio_Cortex-R4_Project_Selection.jpg)

**确保已勾选两个项目，未勾选 "Copy projects into workspace"（将项目复制到工作区）**

### RTOS 配置和使用详情

### Cortex-R4 FreeRTOS 移植专用配置

此演示的特定配置项目位于 FreeRTOS/Demo/CORTEX_R4_RM48_TMS570_CCS5/FreeRTOSConfig.h。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ** 

 此常量可用于设置 RTOS 滴答中断的频率。提供的值 (1000 Hz) 对于
 测试 RTOS 内核功能非常有用，但此频率比大多数应用程序所需的频率都要高。
 降低频率将提高效率。

每个移植都将 "BaseType_t" 定义为
。此移植将 BaseType_t 定义为长类型。

### 中断服务程序

与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

以下源代码段取自演示应用程序中的 serial.c ，
提供了以下示例。**注意：**演示应用程序中的串口驱动程序用于测试移植，
并演示“任务与中断”以及“中断与任务”之间的通信
。并非旨在提供高效实现的示例
。生产实现不应该在队列中传递单个字符，
并应使用硬件功能，如 DMA 和 FIFO 。

---

```c

/* The interrupt implementation uses the standard __interrupt compiler keyword. */
__interrupt void vSCIInterruptHandler( void )
{
/* xHigherPriorityTaskWoken must be initialised to pdFALSE. */
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
char cChar;
BaseType_t xVectorValue = serialSCI_INTVEC0_REG;

    switch( xVectorValue )
    {
        case serialRECEIVE_BUFFER_FULL:
            /* Receive buffer full interrupt, send received char to a queue.
 The address of xHigherPriorityTaskWoken is used as a parameter. */
            cChar = serialSCI_RD_REG;
            xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );
            break;
    }

    /* If calling xQueueSendFromISR() above caused a task to leave the blocked
 state, and the task that left the blocked state has a priority above the
 task that this interrupt interrupted, then xHighPriorityTaskWoken will have
 been set to pdTRUE. If xHigherPriorityTaskWoken equals true then calling
 portYIELD_FROM_ISR() will result in this interrupt returning directly to the
 unblocked task. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```

---

**中断服务程序示例，用于演示如何使用
 portYIELD_FROM_ISR() 宏。** 

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
中断服务程序调用。

### FreeRTOS使用的资源

RTI 通道 0、SWI 指令以及系统软件中断 (SSI) 0 需要专用于 FreeRTOS
。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 Cortex-R4 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
