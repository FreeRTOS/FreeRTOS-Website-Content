---
title: "Atmel SAM4L 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



低功耗 RTOS 演示——Atmel SAM4L 使用免费的 Atmel Studio 6 IDE、GCC 和 Atmel 软件框架

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![的 SAM4L-EK 微控制器开发套件 Atmel](/media/2018/Atmel_SAM4L-EK.jpg)

  

### 简介


此页面上记录的应用程序演示了如何使用 FreeRTOS 的
[滴答抑制](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
功能是如何为
在 [SAM4L ARM Cortex-M4 微控制器](http://www.microchip.com/wwwproducts/en/ATSAM4LC4C)
（来自 Atmel）上运行的应用程序最大限度地减小功耗的。SAM4L
是专为需要极低功耗的应用程序
设计的。

此演示使用 FreeRTOS GCC ARM Cortex-M3/4 移植，免费的
[Atmel Studio 6 IDE](https://www.microchip.com/avr-support/atmel-studio-7)和
综合 [Atmel 软件框架](https://www.microchip.com/avr-support/advanced-software-framework-(asf)
(ASF) 的组件。该项目经过预先配置，在 [SAM4L-EK](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=atsam4l-ek) 评估套件上运行。







---


#### *重要提示！关于使用 FreeRTOS SAM4L 演示项目*的说明


*使用此 RTOS 移植前,请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#atmel-arm-cortex-m4-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织


FreeRTOS zip 文件包含所有 FreeRTOS的源文件
移植和所有演示应用程序，其中只有少数需要使用在该
是本项目需要的。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
的信息。

ATSAM4L 演示应用程序的 Atmel Studio 6 Solution 文件名称是
FreeRTOS_Demo.atsln，位于 FreeRTOS/Demo/CORTEX_M4_ATSAM4L_Atmel_Studio
目录。



  





---


### Atmel ARM Cortex-M4 演示应用程序


  



#### 硬件设置



演示使用内置在 SAM4L-EK 上的 LED，无需硬件设置。

  



#### 功能性


configCREATE_LOW_POWER_DEMO 常量
在 FreeRTOSConfig.h 的顶部定义。构建项目时，如 configCREATE_LOW_POWER_DEMO 设置为 1，
则会创建低功耗演示。
在将 configCREATE_LOW_POWER_DEMO 设置为 0 的情况下构建项目时，
会创建一个仅标准内核的演示（无滴答抑制）。

  



#### ConfigCREATE_LOW_POWER_DEMO 设置为 1 时的功能



当 configCREATE_LOW_POWER_DEMO 设置为 1 时，main() 会调用 main_low_power()。
main_low_power() 会创建一个非常简单的演示如下：

* 创建两个任务，一个 Rx 任务和一个 Tx 任务。
* Rx 任务阻塞一个队列以等待数据，每一次收到数据
 LED 就会闪烁（打开，然后再关闭），
 阻塞队列。LED 灯只是短暂闪烁，所以它
 不会对电流读数产生太大影响。
* Tx 任务反复进入阻塞状态，长达 500 毫秒。退出阻塞状态时，
 Tx 任务通过队列向 Rx 发送一个值，
 （导致 Rx 任务退出阻塞状态并闪烁 LED）。



  



#### 当 configCREATE_LOW_POWER_DEMO 设置为 1 时观察到的行为


**为了获得最佳的低功耗效果，必须
仅使用 JTAG USB 连接器连接 SAM4L-EK 并为其供电，但不得连接调试器**
（应用程序必须"独立"执行）。

MCU 将其大部分时间花在保持低功率状态（参见下文的
实施部分），在此期间，
内置在 SAM4L-EK 上的主板显示器上
会显示一个
较低的电流读数。



每隔 500 毫秒， MCU 会退出低功率状态以打开 LED，
然后返回到低功耗状态并维持 20 毫秒，然后再次退出低功耗状态
以关闭 LED。这将表现为 LED
每 500 毫秒快速闪烁一次，以及 SAM4L-EK 内置的主板显示器上
当前功耗图表中
迅速出现的两个点。由于速度太快，
这两个点通常看起来只有一个点。






![](/media/2018/SAM4L-EK_board_monitor-e1663867111377.jpg)

  

**当无滴答低功耗应用执行时，
   

 主板显示器显示的电流读数** 



  



#### configCREATE_LOW_POWER_DEMO 设置为 1 时 RTOS 的实现


SAM4L 微控制器有几种不同的低功耗模式。把功耗
控制在最低限度，且不丢失静态
RAM 和 CPU 寄存器的内容的低功耗模式叫做保持模式。每当两个任务处于阻塞状态（即只有空闲任务能够执行）时，RTOS 会关闭
滴答中断并将 SAM4L 置于保持低功耗状态
。
关闭滴答中断使微控制器维持在保持模式，
直到任务需要退出阻塞状态并执行。如果
RTOS 滴答中断没有以这种方式被抑制，那么微控制器将必须在
每次发生滴答中断时都要退出保持模式。

标准 RTOS Cortex-M 端口使用 Cortex-M SysTick 计时器来生成
RTOS 滴答中断，但 SAM4L 进入保持模式时，SysTick 计时器会停止，
因此无法在此演示中使用。相反，RTOS 滴答是
由异步计时器 (AST) 生成的。AST 继续
在保持模式下运行，并且它的完整 32 位宽度和慢时钟显著延长了
RTOS 的滴答抑制时长，远远大于使用
SysTick 的时长。



  



#### ConfigCREATE_LOW_POWER_DEMO 设置为 0 时的功能



当 configCREATE_LOW_POWER_DEMO 设置为 0 时，mail()
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：

* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。


创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API
并测试 RTOS 端口。

创建“检查”任务以定期检查标准
演示任务，以确保所有任务都能
正常运行。检查软件定时器的
回调函数会切换 SAM4L-EK 硬件的 LED。
为系统健康
直观反馈。**如果 LED 每 3 秒钟切换一次，则表示
检查软件定时器未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查软件定时器已
在一个或多个任务中发现了问题。**


  



#### 构建和执行演示应用程序


1. 打开 FreeRTOS/Demo/CORTEX_M4_ATSAM4L_Atmel_Studio/FreeRTOS_Demo.atsln
 （从 Atmel Studio IDE 中打开）。
2. 打开 FreeRTOSConfig.h, 并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
3. 确保目标硬件使用
 内置在 SAM4L-EK 主板上的 J-Link USB 连接器连接到主机上。
4. 从 IDE 的“构建”菜单中选择“构建解决方案” ，
 RTOS演示项目的构建应该不会报错或出现警告。
5. 构建完成后，从 IDE 的“调试”菜单中选择“开始调试并中断”
 对 SAM4L 微控制器闪存进行编程，启动调试
 会话，并命令调试程序中断向 main() 函数输入。

 有两件事会阻止下载：



	1. 如果 SAM4L-EK 事先未连接，那么 J-Link 驱动程序
	 可能会打开一个窗口，询问您是否要更新 J-Link
	 固件，但窗口会（至少在本文写作时）
	 出现在 Atmel Studio 6 窗口**下方**。
	2. J-Link 将默认为使用 JTAG 模式，但 SAM4L-EK
	 需要 SWD 模式，如下所示：
	 
	
	

	![](/media/2018/selecting_swd_mode_in_atmel_studio.jpg)
	
	  

	**确保使用 SWD 模式**
6. 确保调试器已停止（完全停止，而不仅仅是暂停），并且
 应用程序在获取电流读数之前是自由运行的。



  





---


### RTOS 配置和使用详情



  



#### ARM Cortex-M4 FreeRTOS 端口特定配置


此演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_M4_ATSAM4L_Atmel_Studio/src/FreeRTOSConfig.h中。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。特别是：

* **configTICK_RATE_HZ** 

 此常量设置了 RTOS tick 中断的频率。此演示
 使用的设置取决于 configCREATE_LOW_POWER_DEMO 设置。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY** 

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的 8 位偏移值，定义为原始值，直接用于
 ARM Cortex-M4 NVIC 寄存器；configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 与其等效，但定义为仅使用 4 个优先级位，用于 SAM4
 NVIC。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未偏移的 4 位格式。



请注意！请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小表示中断优先级越高。这一点
可能有悖直觉，容易混淆！如果要将
中断设置为低优先级，请不要将其优先级指定为 0（或其他低数值），
因为这会导致该中断在系统中具有
最高优先级，并且如果这个优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，可能会导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。



ARM Cortex-M 核心上的最低优先级实际上是 255，但不同
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位，
并提供优先级指定方式不同的库函数。例如，
在 Atmel SAM4 ARM CORTEX-M4 微控制器上，您可以指定的最低优先级实际上为 15——这是由
FreeRTOSConfig.hCONFIGLIBRARY_LOWEST_INTRUPT_PROJECT中常数定义的。可指定的最高优先级
始终为零。



我们还建议确保将所有优先级位分配为
抢占式优先级位，并且不设置子优先级位，就和演示
中的一样。





每个移植 #defines 'BaseType_t' 为对该处理器而言最有效的
数据类型。此移植将 BaseType_t 定义为长类型。





  


#### 中断服务例程



与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务例程
无特殊要求，可根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。



下列源代码片段仅作为示例提供。中断
使用信号量与任务（未显示）同步，并调用 portEND_SWITCHING_ISR()
以确保如果任务的优先级等同或高于中断优先级，
则中断会直接返回任务。另一例子请参阅
此示例中 serial.c 文件中的 USART1_Handler() 函数
。




```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portEND_SWITCHING_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```


只有以 “FromISR” 结尾的 FreeRTOS API 函数可以从
中断服务例程中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_interrupt_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。


  



#### FreeRTOS使用的资源


FreeRTOS 需要独占 SysTick 和 PendSV 中断。其也使用 SVC 编号 #0。


  


#### 抢占式内核和协作式 RTOS 内核之间的切换


将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 即可使用抢占式内核，
可使用协作式内核。选择协作式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

  


#### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


#### 内存分配


Source/Portable/MemMang/heap_4.c包含在ARM Cortex-M4演示应用项目中，以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分
以获取完整信息。

  


#### 其他事项



请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










