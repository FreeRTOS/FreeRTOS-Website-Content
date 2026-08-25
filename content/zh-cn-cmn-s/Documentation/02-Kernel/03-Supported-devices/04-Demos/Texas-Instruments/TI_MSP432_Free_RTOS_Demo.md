---
title: "TI MSP432 ARM Cortex-M4F RTOS演示支持IAR、ARM (Keil) 和 TI (CCS) 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[ARM Cortex-M4F](http://www.arm.com/products/processors/cortex-m/cortex-m4-processor.php)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Texas Instruments MSP432 Launchpad 开发套件](/media/2018/MSP432_Launchpad_Development_Kit.jpg)

 MSP-EXP432P401R LaunchPad 开发套件

### 简介

此页面记录的演示应用程序面向
[Texas Instruments MSP432 微控制器](http://www.ti.com/MSP432)
 - 该微控制器是采用 ARM Cortex-M4F 核心的 MSP430
低功耗微控制器的变体。

我们为以下三种 ARM Cortex-M4 编译器分别提供了面向 MSP432P401R Launchpad
开发套件的预配置 MSP432 项目：

* [IAR](http://www.iar.com/ewarm) 使用 ARM IDE 的嵌入式工作台
* 使用 uVision IDE 的[ ARM](http://www.keil.com/arm/mdk.asp)
* 使用基于 Code Composer Studio Eclipse 的工具的 [TI](http://www.ti.com/tool/ccstudio)

每个项目都可进行编译，以创建简单的 blinky 演示
或综合测试和演示应用程序。

综合演示使用 [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
通过 UART 创建一个简单的命令行接口。

blinky 演示使用 FreeRTOS的无滴答空闲模式来降低功耗。

### “无滴答”低功耗操作

通过停止 RTOS 滴答中断，微控制器可以维持在深度节能状态，
直到中断发生，或者到了 RTOS 内核
将任务转换为“就绪”状态的时间。

请注意，本文仅演示了通用 ARM Cortex-M 无滴答实现，
以防止进入任何高级 MSP432 低功耗模式，
因此避免了可通过其他方式实现节能效果的演示
。

FreeRTOS 旨在允许通用无滴答模式被
特定于应用程序的实现覆盖。通过提供特定于目标的无滴答实现，
允许 RTOS 滴答中断
由低功耗时钟而非 ARM Cortex-M SysTick 时钟生成。之后，
应用程序编写器可以通过使用睡眠前和睡眠后宏将实现定制为特定于
应用的实现。通过定制特定于 MSP432
的无滴答实现，
可显著降低功耗。

请参阅 [低功耗支持](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
和[适用于 ARM Cortex-M MCU 的低功耗 RTOS](/low-power-ARM-cortex-rtos)
页面。

![FreeRTOS 内核感知调试器，可与 IAR 编译器结合使用](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 FreeRTOS 状态查看器插件的屏幕截图

 该插件为 IAR IDE 附带

---

### *重要提示！使用 TI MSP432 ARM Cortex-M4F 演示的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含每个 FreeRTOS 移植的源代码和
所有演示应用程序，因此包含的文件数量远多于 MSP432
演示所需的文件。请参阅此网站的[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解有关下载文件的描述。

IAR、Keil uVision 和 CCS 项目均位于
/FreeRTOS/Demo/CORTEX_M4F_MSP432_LaunchPad_IAR_CCS_KEIL 目录：

* IAR ARM 嵌入式工作台（EWARM）项目称为 RTOSDemo.eww
* Keil uVision 项目称为 RTOSDemo.uvproj
* CCS 项目具有通常的 Eclipse 项目名称 .project

---

#### 构建和运行 MSP432 ARM Cortex-M4F RTOS 应用程序

RTOS 演示项目可以被配置为建立
一个简单的 blinky 项目，同时演示 FreeRTOS 的通用无滴答低功率模式，
或者一个全面的测试和演示应用。常量
configCREATE_SIMPLE_TICKLESS_DEMO
在项目的 FreeRTOSConfig.h 文件顶部定义，
用于在二者之间进行切换。

* 如果 configCREATE_SIMPLE_TICKLESS_DEMO
 设置为 1，则创建简单的无滴答演示。
* 如果 configCREATE_SIMPLE_TICKLESS_DEMO
 设置为 0，则创建全面演示。

请注意本页顶部包含的[注释](#无滴答低功耗操作)，
了解使用所演示的通用
无滴答实现与使用特定于 MSP432
的无滴答实现时的节能效果区别。

此演示使用了在 Launchpad 开发套件上构建的 LED，
因此无需进行硬件设置。

以下各小节提供了每个 ARM
Cortex-M4 工具链的使用说明。

1. [使用 IAR 嵌入式工作台构建](#使用iar嵌入式工作台构建)
2. [使用 ARM Keil 构建](#使用-arm-keil-构建)
3. [使用 Code Composer Studio 构建](#使用基于-ti-eclipse-的-code-composer-studio-ccs-构建)

#### 使用IAR嵌入式工作台构建

1. IAR 嵌入式工作台应该能够使用可通过 Launchpad 硬件的 USB 连接器访问的
 CMSIS DAP 调试接口。
 但想要实现最快、最可靠的调试体验，
 建议将 JLINK Lite 连接到 Launchpad 硬件的外部 JTAG 连接器。
 如果使用的是外部 JTAG 连接器，则使用 Launchpad
 硬件的 "JTAG Switch" 必须设置为 "Ext"。
2. 打开 FreeRTOS/Demo/CORTEX_M4F_MSP432_LaunchPad_IAR_CCS_KEIL/RTOSDemo.eww
 （位于 IAR嵌入式工作台 IDE 中）。
3. 从 IAR 嵌入式工作台的 "Project" 菜单中选择 "Rebuild All"（或按 F7）以构建
 以构建演示项目。
4. 从IAR嵌入式工作台的 "Project" 菜单中选择 "Download and Debug"，
 对微控制器闪存进行编程并启动调试会话
 会话。

**注意：**IAR 项目如果在比最初用于创建项目的 EWARM 版本更低的版本中打开，则可能无法构建并损坏
（因此它不能再用于任何 IAR 版本）
。

#### 使用 ARM Keil 构建

1. Keil uVision 应该能够使用可通过 Launchpad 硬件的 USB 连接器访问的
 CMSIS DAP 调试接口。
 但想要实现最快、最可靠的调试体验，
 建议将 UINK ME  连接到 Launchpad 硬件的外部 JTAG 连接器。
 如果使用的是外部 JTAG 连接器，则使用 Launchpad
 硬件的 "JTAG Switch" 必须设置为 "Ext"。
2. 确保 MSP432 包已安装并可供
 uVision IDE 使用。
3. 在 Keil IDE 中打开 FreeRTOS/Demo/CORTEX_M4F_MSP432_LaunchPad_IAR_CCS_KEIL/RTOSDemo.uvprojx
 。
4. 从 Keil 的 "Project" 菜单中选择 "Rebuild Target"（或按 F7）以构建
 演示项目。
5. 从 Keil 的 "Project" 菜单中选择 "Start/Stop Debug Session"，
 对微控制器闪存进行编程并启动调试会话
 会话。

#### 使用基于 TI Eclipse 的 Code Composer Studio (CCS) 构建

1. 使用硬件的 USB 连接器将 Launchpad 开发套件直接连接到主机
 （运行 CCS 的计算机），无需其他调试
 接口。确保 Launchpad 硬件的 "JTAG Switch"
 设置为 "XDS"。
2. 启动 CCS Eclipse IDE，然后按照提示创建一个新的或选择一个现有的
 工作区。
3. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Code Composer Studio->CCS Projects"（如下所示）。

![将 ARM Cortex-M4 RTOS 演示项目导入 CCS Eclipse IDE](/media/2018/import_code_composer_studio.jpg)

**首次点击 "Import" 时显示的对话框**
4. 在下一个对话框中，选择/FreeRTOS/Demo/CORTEX_M4F_MSP432_LaunchPad_IAR_CCS_Keil
 作为根目录。确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 **并且确保未勾选 'Copy Projects Into
 Workspace' 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/import_CCS_project.jpg)

**确保已勾选 RTOS 演示，并且确保未勾选 "Copy projects into workspace"**
5. 从 CCS Eclipse 的 "Project" 菜单中选择 "Build All"，以构建
 演示项目。
6. 从 Eclipse 的 "Run" 菜单中选择 "Debug"，
 对微控制器闪存进行编程并启动调试
 会话。

**注 1：**所有编译器的项目都包含在
FreeRTOS .zip 文件下载的同一个目录中。如果该目录已包含由不同的编译器生成的对象文件，
那么 Code Composer Studio (CCS)
将无法构建项目。必须从目录及其子目录删除中所有中间文件，
之后才能在
IAR 或 uVision 项目已经使用的情况下切换使用
Code Composer Studio 项目。

**注 2：**CCS 项目引用了使用相对路径的文件，包括
/FreeRTOS-Plus 目录中的FreeRTOS-Plus-CLI 文件。如果目录路径已更改或文件已移动，
则无法构建项目。Eclipse
的 'export' 功能可用于将项目转换为独立项目，
此项目只能使用 .project 文件所在目录下的目录。

### 演示应用程序功能

#### 使用无滴答操作的简单 blinky 示例

当 configCREATE_SIMPLE_TICKLESS_DEMO 设置为
1 时创建简单的无滴答示例。configCREATE_SIMPLE_TICKLESS_DEMO 定义于 FreeRTOSConfig.h 顶部。

FreeRTOS 无滴答闲置模式在闲置期间（没有可执行的应用程序任务的期间）停止周期性 RTOS 滴答中断
。
此 blinky 示例创建了两个任务，它们每秒只取消阻塞一次，
因此在大部分执行时间内都会停止滴答中断。

通过停止 RTOS 滴答中断，微控制器可以维持在深度节能状态，
直到中断发生，或者到了 RTOS 内核
将任务转换为“就绪”状态的时间。

请注意本页顶部包含的[注释](#无滴答低功耗操作)，
了解使用所演示的通用
无滴答实现与使用特定于 MSP432
的无滴答实现时的节能效果区别。

将 configCREATE_SIMPLE_TICKLESS_DEMO 设置为 1 会导致 main() 调用
main_blinky()：

* **main_blinky() 函数：**

 main_blinky() 在启动调度器前会创建队列、队列发送任务和队列接收任务
 。
* **队列发送任务：**

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。

 prvQueueSendTask() 每秒向队列发送一次值 100。
* **队列接收任务：**

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 实现。

 prvQueueReceiveTask() 在数据达到队列前保持阻塞状态。
 该任务每次从队列接收值 100 后闪烁 LED。
 由于任务每秒向到队列发送一次数据，因此 LED
 每秒闪烁一次。

#### 综合测试和演示应用程序

![](/media/2018/MSP432_CLI.jpg)

 CLI 会话示例

当 configCREATE_SIMPLE_TICKLESS_DEMO 设置为
0 时创建综合示例。configCREATE_SIMPLE_TICKLESS_DEMO 定义于 FreeRTOSConfig.h。

综合演示包括一个
[命令行接口](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
(CLI)，在其中可查看任务和运行时统计信息。下文提供了
CLI 的连接和使用说明。

将 configCREATE_SIMPLE_TICKLESS_DEMO 设置为 0 会导致 main() 调用
main_full()：

* **main_full() 函数：**

 main_full() 创建了一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、
 CLI、Check 任务、Register Test 任务，并启动了
 调度器。
* **"Reg Test" 任务：**

 Reg Test 任务用于测试上下文切换机制，
 通过向 MCU 寄存器填入已知的值，然后连续检查每个
 寄存器在整个任务生命周期内是否保持其预期值。
* **"Check" 任务：**

 "Check" 任务监测系统内所有其他任务的状态，
 寻找停滞的任务或报告错误的任务。
 它每次被调用时都会切换 LED。

 如果 LED 每 3 秒钟切换一次，则 check 任务确定
 演示正在按预期运行。如果 LED
 每 200 毫秒切换一次，则至少发现了一个错误。

要连接到 CLI：

1. 通过硬件的 USB 连接器为 Lauchpad 硬件供电。
2. 运行综合演示。MPS432 上的 UART 将在主机上
 作为一个名为 "XDS110 Class Application/User UART" 的虚拟 COM 端口
 进行枚举。
3. 打开 Tera Term 或 Hyper Terminal 等哑终端程序，
 并以 19200 波特率连接到枚举的 COM 端口。
4. 与 FreeRTOS-Plus-CLI 一样，在控制台中键入 "help" 以查看
 已注册命令列表。右侧显示了 CLI 会话示例。

---

### RTOS 配置和使用详情

#### 中断服务程序

##### 优先级分配

请注意！请参阅[专门介绍如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0(或其他较小数值)，
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心上的最低优先级实际上是 255，但不同
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位，
并且提供的库函数要求以不同的方式指定优先级。例如，
TI MSP432 ARM Cortex-M4 微控制器实现了 3 个优先级位，
允许使用最多 8 个不同的优先级（0 到 7，含 0 和 7）。最低优先级对应
最大数字。某些库函数会使用数值 7 作为
最低优先级，而其它函数则会使用数值 224 作为最低优先级（
即 7 \<\< 5，这样 ARM Cortex-M 才能在中断控制器中看到该值）。
这两个数字分别由
FreeRTOSConfig.h中的 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configKERNEL_INTERRUPT_PRIORITY 定义。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为子优先级位。

##### 实施中断服务程序

导致上下文切换的中断服务程序
无特殊要求。在
/FreeRTOS/Demo/CORTEX_M4F_MSP432_LaunchPad_IAR_CCS_Keil/Full_Demo/serial.c
中定义的 vUART_Handler() 函数可作为示例使用。下面是另一个例子：

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A [task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for a notification,
 and giving the notification caused the task to unblock, and the unblocked
 task has a priority higher than the current Running state task (the task that
 this interrupt interrupted), then lHigherPriorityTaskWoken will have been set
 to pdTRUE internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into
 the portYIELD_FROM_ISR() macro will result in a context switch being pended
 to ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

#### 特定于RTOS 移植的配置

专用于此类演示的[配置项](/Documentation/02-Kernel/03-Supported-devices/02-Customization)包含在 FreeRTOSConfig.h
文件中，该文件位于项目文件所在的目录。您可以
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量设置了 RTOS 滴答中断的频率。提供的 500Hz 值可用于
 测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
。所有 ARM Cortex-M4F 移植都将 BaseType_t 的类型定义为 long。

请注意 vPortEndScheduler() 尚未实现。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM CORTEX-M4F 演示应用程序项目中，用以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
