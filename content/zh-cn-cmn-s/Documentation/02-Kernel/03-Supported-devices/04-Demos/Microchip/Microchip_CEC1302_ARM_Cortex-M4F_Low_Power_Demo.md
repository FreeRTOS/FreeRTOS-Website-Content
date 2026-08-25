---
title: "Microchip ARM Cortex-M4F CEC1302 低功耗 RTOS 演示 - 使用 Keil、GCC 和 MikroC 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 简介

本页记录的 RTOS 演示应用程序适用于
[Microchip 的
基于 ARM Cortex-M4F 的 CEC1302 微控制器](http://ww1.microchip.com/downloads/en/DeviceDoc/00002022B.pdf)。为以下编译器和工具组合
提供了预配置项目：
* Keil uVision，使用 ARM 编译器
* Keil uVision，使用 [GCC](https://launchpad.net/gcc-arm-embedded) 编译器
* [mikroC Pro](http://www.mikroe.com/mikroc/arm/) for ARM

该项目可配置为创建一个简单的 "blinky"
样式的项目，用于演示如何利用
[RTOS 的无滴答空闲功能](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)，
或创建一个更全面的测试和演示应用程序，用于测试移植完整性和演示多项
RTOS 功能。

---

### *重要！关于使用 FreeRTOS CEC1302 演示项目的说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#microchip-arm-cortex-m4-rtos-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”，
请特别注意
开发时定义 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义）的建议。

---

### 源代码组织

FreeRTOS zip 文件包含所有 FreeRTOS
移植的源文件以及所有演示应用程序。本项目只需要其中的几个文件
。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
和新项目创建的信息。

* 使用 ARM 编译器的 Keil uVision 项目称为
 RTOSDemo.uvprojx，位于
 FreeRTOS/Demo/CORTEX_M4F_CEC1302_Keil_GCC/Keil_Specific
 目录（此为 [FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的目录）中。
* 使用 GCC 编译器的 Keil uVision 项目也称为
 RTOSDemo.uvprojx，位于
 FreeRTOS/Demo/CORTEX_M4F_CEC1302_Keil_GCC/GCC_Specific
 目录（此为 [FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的目录）中。
* ARM 项目的 MikroC Pro 称为
 RTOSDemo.mcpar，位于
 FreeRTOS/Demo/CORTEX_M4F_CEC1302_MikroC/MikroC_Specific
 目录（此为 [FreeRTOS 主下载文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)的目录）中。

**注意：**MikroC 编译器会在整个项目目录结构中留下许多临时文件，
内置编辑器与
RTOS 源文件使用的格式惯例不兼容，
为便于创建 FreeRTOS 源文件，FreeRTOS MikroC 移植层
将 "const" 关键字定义为空。

---

### Microchip ARM Cortex-M4 RTOS 演示应用程序

#### 硬件设置：uVision 项目

通常，RTOS 演示应用程序通过控制
LED 的切换频率来指示其状态。但是，uVision 演示不针对任何特定硬件，
因此未配置为切换任何特定 IO
端口上的任何特定 LED。相反，名为 ulLED 的变量会在每次切换 LED
时递增。

ulLED 变量随宏 configTOGGLE_LED() 递增，
该宏在 FreeRTOSConfig.h 中定义。如果目标硬件有备用 LED，
则可以更新 configTOGGLE_LED() 以便使用 LED。否则，可以将 ulValue
添加到 uVision IDE 的数据监视窗口中，在该窗口中，
可以看到该值随着 RTOS 演示应用程序的执行而更新（前提是使用了合格调试接口，例如
ULINK）。

uVision 项目的 ARM 编译器和 GCC
编译器版本也可以在下节所述的 Clicker
硬件上执行，方法是新增一条适配器数据线，将 Mikro mProg 数据线映射到标准的 ARM JTAG 连接器上。
所需的输出引脚详见下表（假设为 20 引脚 JTAG 连接器）。

|  |  |  |
| --- | --- | --- |
| **信号名称**  | **ARM 20 引脚号**  | **mPROG 引脚号**  |
| <br /> VCC +3.3V<br />  | <br /> 1<br />  | <br /> 1<br />  |
| <br /> 接地<br />  | <br /> 20<br />  | <br /> 9<br />  |
| <br /> JTAG_TDI<br />  | <br /> 5<br />  | <br /> 8<br />  |
| <br /> JTAG_TMS<br />  | <br /> 7<br />  | <br /> 2<br />  |
| <br /> JTAG_TCLK<br />  | <br /> 9<br />  | <br /> 4<br />  |
| <br /> JTAG_TDO<br />  | <br /> 13<br />  | <br /> 6<br />  |
| <br /> RTCK<br />  | <br /> 11 和 12<br />  | <br /> 接地<br />  |

#### 硬件设置：MikroC Pro for ARM 项目

MikroC 项目预配置为在
[CEC1302 Clicker 板](http://www.mikroe.com/clicker/)上运行，
并使用此硬件中的预置 LED。

#### 功能

该项目提供两个 RTOS 演示应用程序。一个是简单 "blinky" 样式的项目，
演示低功耗无滴答功能，
另一个是更全面的测试和演示应用程序。configCREATE_LOW_POWER_DEMO
设置是在 FreeRTOSConfig.h 中定义，用于在两者之间进行选择。

#### ConfigCREATE_LOW_POWER_DEMO 设置为 1 时的功能

当 configCREATE_LOW_POWER_DEMO 设置为 1 时，main() 会调用 main_low_power()，
创建一个非常简单的演示，如下所示：

* 该演示会创建两个任务，一个 Rx 任务和一个 Tx 任务。
* Rx 任务会阻塞队列以等待数据，每次收到数据时闪烁
 （打开然后再次关闭）一次 LED
 （或切换 ulLED 变量）。LED 只是短暂闪烁，
 因此不会消耗太多电流。
* Tx 任务每隔
 1000 毫秒通过队列向 Rx 任务发送值（导致 Rx 任务退出阻塞状态，使 LED
 闪烁）。

#### 当 configCREATE_LOW_POWER_DEMO 设置为 1 时观察到的行为

这两项任务大部分时间都处于阻塞状态，在此期间，
关闭 RTOS 滴答，ARM Cortex-M4F 置于低功耗状态。
每隔 1000 毫秒，MCU 会先退出低功耗状态，点亮 LED，
再进入低功耗状态并持续 10 毫秒，
然后再次退出低功耗状态以关闭 LED。每隔 1000 毫秒，LED
上会出现短暂闪烁。

#### configCREATE_LOW_POWER_DEMO 设置为 1 时 RTOS 的实现

该演示提供了[低功耗无滴答实现](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)，
使用 CEC1302 休眠定时器来生成 RTOS 滴答中断。

针对 CEC1302
的无滴答实现中包括相同的 configPRE_SLEEP_PROCESSING()
和 configPOST_SLEEP_PROCESSING() 宏，关于两个宏的更多详情，
请参见[介绍
通用 Cortex-M 无滴答实现的页面](low-power-ARM-cortex-rtos.md#using_mcu_specific_features)。预休眠宏可定义为在进入低功耗状态之前
采取额外的特定于应用程序的操作来提高能效，
而后休眠宏可定义为
反转预休眠宏所采取的任何操作。例如，
如果将预休眠宏定义为关闭外设，
将后休眠宏定义为再次打开外设，
则外设会在每次进入休眠模式之前自动关闭，
并在每次退出休眠模式时再次自动打开。

#### configCREATE_LOW_POWER_DEMO 设置为 0 时的功能

当 configCREATE_LOW_POWER_DEMO 设置为 0 时，mail()
调用 main_full() 创建一个全面测试和演示应用程序
以展示：

* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
* [静态分配的 RTOS 对象](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务
。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

创建“检查”任务，用于定期检查标准
演示任务，以确保所有任务
都按预期运行。检查任务会切换 LED（或增加 ulLED 变量）。
这直观地反映出了系统的
运行状况。**如果 LED 每 3 秒切换一次，则表示
检查任务未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查任务
在一个或多个任务中发现了问题。**

### 构建并执行演示应用程序

#### 将 GCC 编译器与 uVision 项目一起使用

1. 确保主机上安装了合适的 GCC 编译器。该项目
 采用 arm-none-eabi-gcc 编译器创建和测试，
 所需的预创建二进制文件可从
 [launchpad.net](https://launchpad.net/gcc-arm-embedded)
 网站免费获取。
2. 在 Keil IDE 中打开 FreeRTOS/Demo/CORTEX_M4F_CEC1302_Keil_GCC/GCC_Specific/RTOSDemo.uvprojx
 。
3. 在 uVision IDE 中打开 "Manage Project Items" 窗口（"Project->Manage->Project Items" 菜单项）
 并为主机设置正确的 GCC 前缀和安装文件夹
 。

![在 Keil uVision 中设置 GCC 编译器的路径](/media/2018/Setting_GCC_Path_In_Keil_uVision.png)

**设置 GCC 编译器二进制文件的路径

 请注意，路径中不包括 "/bin"
4. 打开 FreeRTOSConfig.h，并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
5. 确保使用合适的调试连接器（例如
 ULINK2）连接目标硬件和主机。
6. 在 IDE 的 "Project" 菜单中选择 "Rebuilt All Target Files"，
 RTOSDemo 项目在编译过程中不应报错或出现警告。
7. 构建完成后，从 IDE 的 "Debug" 菜单中选择 "Start/STOP Debug Session"
 将应用程序下载到 CEC1302 ARM Cortex-M4F 微控制器 RAM 内存，
 启动调试会话，并使调试器在进入 main() 函数时中断。
 如果调试会话没有按预期启动，请确保调试选项，
 尤其是调试选项中的 "Connect & Reset Options"
 部分应按下图设置。

![配置调试会话以连接到 ARM Cortex-M 处理器](/media/2018/CEC1302_ARM_Cortex_RTOS_Connect.jpg)

**"Connect & Reset Options" 选项**

#### 将 ARM 编译器与 uVision 项目一起使用

1. 在 Keil IDE 中打开 FreeRTOS/Demo/CORTEX_M4F_CEC1302_Keil_GCC/Keil_Specific/RTOSDemo.uvprojx
 。
2. 打开 FreeRTOSConfig.h，并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
3. 确保使用合适的调试连接器（例如
 ULINK2）连接目标硬件和主机。
4. 在 IDE 的 "Project" 菜单中选择 "Rebuilt All Target Files"，
 RTOSDemo 项目在编译过程中不应报错或出现警告。
 不过链接器也可能会出于下述原因发出警告：
 为了将最大数量的测试添加到全面演示中，
 在链接器脚本的配置中，已将代码和数据放入命名相同的部分中。
5. 构建完成后，从 IDE 的 "Debug" 菜单中选择 "Start/STOP Debug Session"
 将应用程序下载到 CEC1302 ARM Cortex-M4F 微控制器 RAM 内存，
 启动调试会话，并使调试器在进入 main() 函数时中断。
 如果调试会话没有按预期启动，请确保调试选项，
 尤其是调试选项的 "Connect & Reset Options"
 按上文 GCC 说明中的图示要求设置
 。

#### 将 ARM 的 MikroC Pro 编译器与 [Clicker](http://www.mikroe.com/clicker/) 硬件一起使用

**注意：**MikroC 编译器会在整个项目目录结构中留下许多临时文件，
内置编辑器与
RTOS 源文件使用的格式惯例不兼容，
为便于创建 FreeRTOS 源文件，FreeRTOS MikroC 移植层
将 "const" 关键字定义为空。

1. 在 MikroC Pro IDE 中打开 FreeRTOS/Demo/CORTEX_M4F_CEC1302_MikroC/MikroC_Specific/RTOSDemo.mcpar
 。
2. 打开 "Search Paths" 窗口（"Projects->Edit Search Paths" 菜单项）
 并更新主机的正确源文件路径和头文件路径
 。

![设置 FreeRTOS 源文件和头文件的路径](/media/2018/Setting_MikroC_Paths.png)

**设置源文件和头文件的路径**
3. 如本页所提供，MikroC 演示使用 [FreeRTOS/Source/portable/MemMang/heap_4.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
 内存分配器，并定义了 [malloc 失败钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)
 。此外，还必须对 heap_4.c 源文件做少量编辑，
 使其与 MikroC 编译器兼容。打开 heap_4.c 源文件并找到
 以下代码：

```c

#if( configUSE_MALLOC_FAILED_HOOK == 1 )
{
    if( pvReturn == NULL )
    {
        extern void vApplicationMallocFailedHook( void ); /* Move this line. */
        vApplicationMallocFailedHook();
    }
    else
    {
        mtCOVERAGE_TEST_MARKER();
    }
}
#endif

```

 将高亮的行（以 "extern" 开头的行）从当前位置
 移动到源文件的顶部，使其具有文件作用域，
 而非块作用域。
4. 打开 FreeRTOSConfig.h，并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
5. 在 IDE 的 "Build" 菜单中选择 "Build" 以创建可执行镜像。
6. 先确保 Clicker 硬件通过其 USB 端口供电，
 并使用 MikroProg 闪存编程器连接，然后才能从 "Tools" 菜单中选择 "mE Programmer"
 将可执行镜像下载到 CEC1302 ARM Cortex-M4F
 微控制器。如果下载未按预期开始，
 请检查 "Programmer/Debugger Options"
 是否按下图要求（"Tools->Programmer/Debugger Options" 菜单项）设置。

![为 ARM Cortex-M 处理器设置 MikroC Pro 编译器的调试选项](/media/2018/MikroC-clicker-ARM-CortexM-debug-options.png)

**所需的编程器和调试选项**
7. 下载完成后，从 "Debug" 菜单中选择 "Start Debugger"
 以启动调试会话并运行应用程序。
 如果调试器未按预期启动，
 请检查 "Programmer/Debugger Options"
 是否按下图要求（"Tools->Programmer/Debugger Options" 菜单项）设置。

---

### RTOS 配置和使用详情

#### ARM Cortex-M4 FreeRTOS 移植特定配置

此演示的特定配置项位于 /FreeRTOS/Demo/CORTEX_M4F_CEC1302_Keil_GCC/FreeRTOSConfig.h 中。
[可以编辑此文件中定义的常量，以适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ**

 此常量设置了 RTOS 滴答中断的频率。此演示
 使用的设置取决于 configCREATE_LOW_POWER_DEMO 设置。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位移位值，根据定义可作为原始数字直接用于
 ARM Cortex-M4 NVIC 寄存器。configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 与其等效，定义为仅使用 CEC1302 NVIC 中实现的 3 个优先位
 。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未移位的 3 位格式。

请注意！请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记指定中断优先级，
因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心上的最低优先级实际上是 255，但不同
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位，
并且提供的库函数要求以不同的方式指定优先级。例如，
Microchip  CEC1302 ARM Cortex-M4 微控制器上可以指定的最低优先级实际上为 7，这是由
FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为子优先级位。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的
。此移植将 BaseType_t 定义为长整型。

#### 聚合中断和分解中断

CEC1302 可以将多组中断源路由到同一个中断向量（聚合中断），
或将所有中断源路由到各自的唯一中断向量（分解中断）
。RTOS 自身只使用 ARM Cortex-M 系统中断，
这些中断总是被路由到标准的 ARM Cortex-M 系统向量，
但演示应用程序也使用
btimer（基础定时器）和 htimer（休眠定时器）中断，
这两种中断均可聚合或分解。为了同时
演示这两种方法，低功耗无滴答演示配置为使用聚合中断，
全面演示则配置为使用分解中断
（请注意，全面演示之所以使用分解中断，
是因为如果所有定时器中断都通过同一向量路由，
则无法运行中断嵌套测试）。

#### 中断服务程序

与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档进行编写。
宏 portYIELD_FROM_ISR() 可用于在
中断服务例程内请求上下文切换。

请注意，portYIELD_FROM_ISR() 将使中断处于启用状态。

下列源代码片段仅作为示例提供。中断
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
以同步任务（未显示），并调用 portYIELD_FROM_ISR()，
以确保如果任务的优先级等于或高于中断任务的优先级，
则中断会直接返回到任务。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose.
 Note lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)( xHandlingTask, &xHigherPriorityTaskWoken );

    /* If the notified task was blocked waiting for the notification, and the
 task has a priority higher than the current Running state task (the task
 that this interrupt interrupted), then lHigherPriorityTaskWoken will have
 been set to pdTRUE internally within vTaskNotifyGiveFromISR(). Passing
 pdTRUE into the portYIELD_FROM_ISR() macro will result in a context
 switch being pended to ensure this interrupt returns directly to the
 unblocked, higher priority, task. Passing pdFALSE into portYIELD_FROM_ISR()
 has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

只有以 “FromISR” 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。

#### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

#### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
和 [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
都设置为 1，允许 RTOS 对象
[以静态或动态方式创建](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。
Source/Portable/MemMang/heap_4.c
用于提供动态分配 RTOS 对象所需的 RAM。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。

