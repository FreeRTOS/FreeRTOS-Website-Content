---
title: "Silicon Labs EFM32 Low Power RTOS Demo Using Simplicity Studio (GCC), and Targeting Giant and Pearl Gecko Starter Kits"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 端口](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![EFM Pearl Gecko ARM Cortex-M4 入门套件](/media/2018/pearl-gecko-SLSTK3401A.jpg)

**EFM32 Pearl Gecko 入门套件 SLSTK3401A**

![EFM Giant Gecko ARM Cortex-M4 Starter Kit](/media/2018/efm32gg-stk3700.png)

**EFM32 Giant Gecko 入门套件 STK3700**

### 简介

此页面记录的演示应用程序
[来自 Silicon Labs](http://www.silabs.com/products/mcu/32-bit/Pages/32-bit-microcontrollers.aspx)的EFM32 ARM Cortex-M3和ARM Cortex-M4F微控制器。

两个 [Simplicity Studio](http://www.silabs.com/products/mcu/Pages/simplicity-studio.aspx)
(GCC) 项目,一个已预配置为针对
[EFM32巨型壁虎入门套件(STK3700)](https://www.silabs.com/products/mcu/lowpower/Pages/efm32gg-stk3700.aspx),以及预配置为目标的套件
[EFM32 Pearl Gecko入门套件(SLSTK3401A)](https://www.silabs.com/development-tools/mcu/32-bit/efm32pg1-starter-kit?tab=overview)。

这两个项目都可用于构建全面测试和演示应用程序,
或构建低功耗演示应用程序。该应用程序使用 FreeRTOS
[滴答抑制](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) 功能
(无 tick 闲置)。此处提供了三个 EFM32 特定的无 tick 闲置实现
are provided: an implementation that uses the **RTC** peripheral on the Giant Gecko,
在Giant Gecko上使用 **BURTC** 外设的实现,以及
在Pearl Gecko上使用 **RTCC** 外设。

---

|  |
| --- |
| *重要! 使用 EFM32 RTOS 演示*的注意事项<br />*使用此 RTOS 移植前,请阅读下述所有要点。*<br /><br />1\. [Source Code Organisation](#源代码组织)<br />2\. [The RTOS Demo Application](#the-efm32-gecko-rtos-演示应用程序)<br />3\. [RTOS Configuration and Usage Details](#rtos-配置和使用详情)<br /><br /><br /> 另请参阅常见问题: [我的应用程序未运行,哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting) |

---

### 源代码组织

官方 FreeRTOS zip 文件下载包含所有 RTOS
移植的源文件和所有演示应用程序,其中只有少数是
EFM32 Gecko 项目所需的。请参阅 [源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)
了解关于已下载文件的说明
新项目的信息。

用于 Silicon Labs EFM32 Giant Gecko STK3700 演示应用程序的 Simplicity Studio 项目
位于 FreeRTOS/Demo/CORTEX_EFM32_Giant_Gecko_Simplicity_Studio
目录中。

用于 Silicon Labs EFM32 Pearl Gecko SLSTK3401A 演示应用程序的 Simplicity Studio 项目
位于 FreeRTOS/Demo/CORTEX_EFM32_Pearl_Gecko_Simplicity_Studio
目录中。

这些是在将项目导入至
Simplicity Studio Eclipse 工作区时应选择的目录。

---

### The EFM32 Gecko RTOS 演示应用程序

#### 硬件设置

演示使用内置在 EFM32 Gecko 入门套件板上的 LED,因此无
需硬件设置。

#### 功能性

RTOS 演示项目可以配置为构建简单的低功耗 [无刻度](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
项目,或构建全面测试和演示项目。常量 configCREATE_LOW_POWER_DEMO
定义于 FreeRTOSConfig.h的顶部,可用于在两者间切换
。下表描述了将为
Pearl 和 Giant Gecko 项目的所有 configCREATE_LOW_POWER_DEMO 有效值构建的项目。

|  |
| --- |
| <br /> EFM32 Giant Gecko 演示<br />  |
\| **Setting**  \| **Project Built**  \|
\| <br /> 0<br />  \| <br /> 将构建全面测试和演示应用程序。<br /> <br /> \|
\| <br /> 1<br />  \| <br /> 简单的低功耗 [无刻度](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) 演示将使用以下内容构建<br /> 如下:<br /> <br /><br /><br /><br /><br /> 使用 BURTC 外围设备的无 tick 闲置实现<br /> 包含在 low_power_tick_management_BURTC.c<br /> 源文件的名称。<br /> <br /> 请注意,使用 ULFRCO 时钟的优点是运行功耗极低,<br /> 但会影响时间精度。<br /> <br /> \|
\| <br /> 2<br />  \| <br /> 将构建简单低功耗无 tick 演示,参数<br /> 如下:<br /> <br /><br /><br /><br /><br /> 使用 RTC 外围设备的无 tick 闲置实现<br /> 包含在 low_power_tick_management_RTC.c<br /> 源文件的名称。<br />  \|
\| <br /> EFM32 Pearl Gecko 演示<br />  \|
\| **Setting**  \| **Project Built**  \|
\| <br /> 0<br />  \| <br /> 将构建全面测试和演示应用程序。<br /> <br /> \|
\| <br /> 1<br />  \| <br /> 将构建简单低功耗无 tick 演示,参数<br /> 如下:<br /> <br /><br /><br /><br /><br /> 使用 RTCC 外围设备的无 tick 闲置实现<br /> 包含在 low_power_tick_management_RTCC.c<br /> 源文件的名称。<br />  \|

#### 当(configCREATE_LOW_POWER_DEMO = = 0)时的功能

如果 configCREATE_LOW_POWER_DEMO 设置为 0,则 main () 将调用 main_full ()。
main_full() 在 main_full.c C 源文件中实现。

main_full() 会创建全面测试和演示应用程序
以展示:

* [使用静态和动态内存分配创建的任务和其他 RTOS 对象](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。
* [定向到任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
* [软件计时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [递归互斥体](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/05-Recursive-mutexes)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。

由综合演示创建的大多数任务来自
[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) 任务。标准演示任务被
所有 RTOS 端口演示应用程序所使用。它们没有特定的功能,
创建目的只是为了演示如何使用 FreeRTOS API,并测试 RTOS 端口。

除了标准演示任务外,综合演示还创建 “RegTest”
任务和“检查”任务:

* RegTest 任务

 两个 RegTest 任务用唯一值填充所有 CPU 寄存器,然后
 检查值是否在任务存在期间不发生改变。
 包含意外值的寄存器表示
 上下文切换机制存在错误(或如果演示已被修改,则存在 [用户错误](/Why-FreeRTOS/FAQs/Troubleshooting)
 )。
* 检查任务。

 检查任务负责检查 RegTest 和标准演示
 任务是否按预期执行,并通过切换 LED 来
 显示系统状态。

**如果 LED 每 3 秒钟切换一次,则表示
 检查任务未发现任何问题。
 如果 LED
 每 200 毫秒切换一次,则表示检查任务**在至少一个任务中发现潜在问题。

#### 当(configCREATE_LOW_POWER_DEMO ! = 0)时的功能

如果 configCREATE_LOW_POWER_DEMO 设置为 1 或 2,则 main () 将调用 main_low_power ()。
main_low_power() 在 main_low_power.c C 源文件中实现。
[请参阅上表](#功能性) ,以了解
EFM32 Giant 和 Pearl Gecko 演示的有效 configCREATE_LOW_POWER_DEMO 设置。

main_low_power () 会创建队列、“队列发送”任务和“队列接收”任务。
然后它会启动调度器。

* 队列发送任务

 队列发送任务每秒向队列发送值 100。
* 队列接收任务

 队列接收任务会在队列上阻塞,
 每次从队列发送任务中收到数值 100 时,
 LED 灯就会闪烁(快速开关)。队列发送任务每秒写入队列,因此
 LED 灯会每秒闪烁一次。

这两个任务大部分时间都在阻止状态,在此期间, RTOS
tick 关闭,并根据配置情况,
进入能量模式 2 (EM2)或能量模式 3 (EM3)。

### 构建并执行演示应用程序


[虚拟和链接路径](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)
从项目目录外部引用文件,且如果
目录结构体已更改,可能无法构建。
1. 请确保您的 Simplicity Studio 安装包中
 含有 Giant 和(或)Pearl Gecko 入门套件支持,
 否则将无法构建项目。
 可为额外的 EFM32 设备和入门套件安装支持,
 使用 Simplicity Studio 菜单即可实现。
2. 启动 Simplicity Studio,根据提示选择现有工作区,
 或创建新的工作区。
3. 从 Simplicity Studio IDE 的“文件”菜单中选择“导入”。将出现
 下图所示对话框。选择“导入现有项目至工作区”。

![将低功耗Cortex-M4 RTOS 演示导入Simplicity Studio](/media/2018/Simplicity_Studio_Import_1.jpg)
4. 在下一个对话框中,选择/FreeRTOS/Demo/CORTEX_EFM32_[part]_Gecko_Simplicity_Studio
 作为根目录,其中 [part] 为 “Giant” 或 “Pearl”。然后,确保
 在“项目”区域勾选RTOS演示项目,请勿勾选
 “将项目复制到工作区”框,然后点击完成按钮(正确的
 复选框状态见下图,图片中不包含完成按钮)。

![将低功耗无刻度 RTOS 演示导入Eclipse](/media/2018/Simplicity_Studio_Import_2.jpg)

 项目源文件将显示在 Eclipse 项目浏览器
 窗口中。
5. 打开 FreeRTOSConfig.h,并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示,或完整测试和演示应用程序,
 根据需求操作。有关有效设置,请参阅上表。 [](#功能性)
6. 确保目标硬件使用合适的
 USB 数据线连接到主计算机。
7. 从 Simplicity Studio “项目”菜单中选择“构建全部”,以构建
 应用程序。
8. 构建完成后,从 Simplicity Studio “运行”菜单中选择“调试”,
 对微控制器闪存进行编程并启动调试会话。

---

### RTOS 配置和使用详情

#### ARM Cortex-M3 和 M4F FreeRTOS 端口特定配置

此演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_EFM32_[part]_Gecko_Simplicity_Studio/FreeRTOSConfig.h中。
[可对此文件中定义的常量进行编辑,以适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量:

* **configTICK_RATE_HZ**

 此常量设置了 RTOS tick 中断的频率。此演示
 使用的设置取决于 configCREATE_LOW_POWER_DEMO 设置。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) 文档,以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的 8 位偏移值,定义为原始数据,直接用于
 ARM CORTEX-M NVIC 寄存器中,configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 等效,定义为仅使用 EFM32 NVIC 中实现的 3 个优先级位
 。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未移位的 3 位格式。

请注意!请参阅 [说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住,ARM Cortex-M 核心中,
数字越小,中断优先级越高。这
似乎有悖直觉,而且很容易忘记! 如果希望
为中断分配低优先级,请勿将其优先级指定为 0(或其他较小数值),
因为这实际上可能会导致该中断在系统中具有最高优先级,
因此,如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY,则可能导致系统崩溃。另外,请勿忘记
分配中断优先级,因为默认情况下,中断优先级为 0,
这可能导致其处于最高优先级。

ARM Cortex-M 核心上的最低优先级实际上是 255,但不同
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位,
并且提供的库函数要求以不同的方式指定优先级。例如,
Silicon Labs ARM Cortex-M 微控制器上可以指定的最低优先级实际上为 7——这是由
FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY  定义的。可指定的最高优先级
始终为零。

每个端口 #defines 'BaseType_t',以等效于对处理器最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

#### 中断服务程序

与许多 FreeRTOS 移植不同的是,引发上下文切换的中断服务程序
无特殊要求,可根据编译器文档进行编写。
宏 portYIELD_FROM_ISR() 可用于在
中断服务例程内请求上下文切换。

请注意,portYIELD_FROM_ISR() 将使中断处于启用状态。

下列源代码片段仅作为示例提供。中断
使用直达任务通知以同步任务(未显示),并调用 portYIELD_FROM_ISR(),
以确保如果任务的优先级等于或高于中断任务的优先级,
则中断会直接返回到任务。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A direct to task notification is used for this purpose.
 Note lHigherPriorityTaskWoken is initialised to zero. */
    vTaskNotifyGiveFromISR( xTaskHandle, &lHigherPriorityTaskWoken );

    /* If the task referenced by the xTaskHandle handle was in the Blocked state
 waiting for a notification then calling vTaskNotifyGiveFromISR() will have
 moved the task into the Ready state. If the task was moved into the Ready
 state, and the task's priority is higher than the priority of the currently
 executing task (the task this interrupt interrupted), then
 lHigherPriorityTaskWoken will have been set to pdTRUE internally within
 vTaskNotifyFromISR(). Passing pdTRUE into the portYIELD_FROM_ISR() macro
 will result in a context switch being pended to ensure this interrupt returns
 directly to the unblocked, higher priority, task. Passing pdFALSE into
 portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

只有以 “FromISR” 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量(或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY)设置的优先级。

#### FreeRTOS使用的资源

当 configCREATE_LOW_POWER_DEMO 设置为 0 时,标准 FreeRTOS Cortex-M 端口被
使用,此时需要独占使用 SysTick 和 PendSV 中断。也使用 SVC 编号 #0。

当 configCREATE_LOW_POWER_DEMO 设置为 1 时,需独占访问 RTC、RTCC 或 BURTC
外围设备,具体依配置而定。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M 演示应用程序项目中,用以提供
RTOS 内核所需的内存分配。全面的演示也展示了
[RTOS 对象是
使用静态分配而](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)非动态分配的内存创建的。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 章节,
以获取完整信息。

#### 其他事项

请注意,vPortEndScheduler() 尚未实现。
