---
title: "Atmel ARM Cortex-M7 SAMV71/SAME70 RTOS 演示，使用 IAR、Atmel Studio (GCC) 和 ARM Keil 嵌入式开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


 使用 [IAR](http://www.iar.com/ewarm)、
 [Atmel Studio](https://www.microchip.com/avr-support/atmel-studio-7) (GCC)
 和 ARM Keil 嵌入式开发工具

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![Atmel 的 SAMV71 Cortex-M7 微控制器](/media/2018/SAMV71_Xplained_Ultra_Angle.png)

  



### 简介


此页文档包含：
* FreeRTOS 演示应用程序，适用于
 [SAMV7 ARM Cortex-M7 微控制器](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-v-mcus)
 （此微控制器来自 Atmel）。此项目
 可以使用 [IAR](http://www.iar.com/ewarm)、
 [Atmel Studio](https://www.microchip.com/avr-support/atmel-studio-7)
 或 ARM Keil 工具构建，并针对
 [SAM V71 Xplained Ultra 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMV71-XULT)。
* FreeRTOS 在
 [SAME7 ARM CORTEX-M7 微控制器上的演示应用](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus)
 （此微控制器来自 Atmel）。此项目
 可以使用
 [Atmel Studio](https://www.microchip.com/avr-support/atmel-studio-7)
 编译器 (GCC) 和 IDE ，并针对
 [SAM E70 Xplained Ultra 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAME70-XPLD)。



由于 SAM V70 包含超集功能，因此 SAM V70 Xplained Ultra 开发板也可以
用于评估 RTOS 在 SAM V70、
[SAM S70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-s-mcus)、
和 [SAM E70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus)
ARM Cortex-M7 设备上的运行。








|  |
| --- |
| <br />[\![](/media/2018/Atmel_Cortex-M7_IDE_Plug_In.png)](/media/2018/Atmel_Cortex-M7_IDE_Plug_In.png)<br /><br />**FreeRTOS 查看器窗口打开的 Atmel Studio。<br /> 点击放大。** <br /><br /> |








---


### *重要提示！关于使用 SAMV7 和 SAME7 ARM Cortex-M7 RTOS 演示的说明*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#atmel-arm-cortex-m7-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和用法详情)


另请参阅常见问题[我的应用程序未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)
特别注意建议
在开发时使用 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义）。

  





---


### 源代码组织


FreeRTOS zip 文件下载包含所有 FreeRTOS 移植的源文件
以及所有演示应用程序的项目。因此，它的文件数量
远超此项目所需。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
获取目录结构的描述以及创建
新 FreeRTOS 项目的信息。

SAMV7 演示应用程序的 Atmel Studio 项目文件名为
RTOSDemo.atsln，位于 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_AtmelStudio
目录。



SAME7 演示应用程序的 Atmel Studio 项目名为
RTOSDemo.atsln，位于 FreeRTOS/Demo/CORTEX_M7_SAME70_Xplained_AtmelStudio
目录。



SAMV7 演示应用程序的 ARM 工作区 IAR 嵌入式工作台名为
RTOSDemo.eww，位于 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_IAR_Keil
目录。



SAMV7 演示应用程序的 ARM Keil 项目文件名为
RTOSDemo.uvprojx，位于 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_IAR_Keil
目录。



  





---


### Atmel ARM Cortex-M7 演示应用程序


### 功能


mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。演示的行为
取决于其设置。
  



### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能


如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 ，则 main ()
调用 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：
* **main_blinky() 函数：** 
main_blinky() 会创建一个队列和两个任务。然后它会启动
 RTOS 调度器。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask () 执行。
 它每 200 毫秒向队列发送值 100。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的  prvQueueReceiveTask () 实现
 。每当收到来自队列发送任务的消息时，它会在队列读取操作上进入阻塞状态，同时解除 LED 阻塞并切换 LED
 。队列发送任务
 每 200 毫秒发送到队列，所以队列
 接收任务离开阻塞状态并每 200 毫秒
 切换一次 LED。



  



### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main()
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序，
以展示：

* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](FreeRTOS-Event-Groups.md)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)


创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务集。所有 FreeRTOS 移植演示应用程序使用标准演示任务，
它们没有特定的功能。它们用于演示如何使用 FreeRTOS API ，
并测试 RTOS 移植。

创建“检查”任务以定期检查标准
演示任务，确保所有任务都能按预期
正常运行。检查任务还会切换 LED，以提供系统状态的
视觉反馈。**如果 LED 每 3 秒钟切换一次，则表示
检查任务未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查任务已
在一个或多个任务中发现了问题。**


  



### 构建和执行演示应用程序—— Atmel Studio


1. 打开项目文件 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_AtmelStudio/RTOSDemo.atsln
 或 FreeRTOS/Demo/CORTEX_M7_SAME70_Xplained_AtmelStudio/RTOSDemo.atsln
 （从 Atmel Studio IDE 中打开）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
3. 确保目标硬件使用
 合适的调试器接口与主计算机连接——演示是使用 J-Link 进行开发和调试的；
 也可以使用目标硬件上的
 Edge 调试接口。
4. 从 IDE 的 '**Build**’ 菜单中选择 '**Build Solution**'。
 RTOS 演示项目的构建应该不会报错或出现警告。
5. 构建完成后，从 IDE 的 '**Debug**' 菜单中选择 '**Start Debugging and Break**'
 对 Cortex-M7 微控制器进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。


  



### 构建和执行演示应用程序—— IAR


1. 打开 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_IAR_Keil/RTOSDemo.eww
 （位于 IAR 嵌入式工作台 IDE）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
3. 确保目标硬件使用
 合适的调试器接口连接至主机——演示是使用 J-Link
 进行开发和调试的。
4. 从 IDE 的 '**Project**' 菜单中选择 '**Rebuild All**'，
 RTOS 演示项目构建时不应报错或出现警告。
5. 构建完成后, 从 IDE 的 '**Project**' 菜单选择 '**Download and Debug**'
 对 Cortex-M7 微控制器进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。


  



### 构建和执行演示应用程序——Keil


1. 打开项目文件 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_IAR_Keil/RTOSDemo.uvprojx
 （位于 Keil uVision IDE 内）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
3. 确保目标硬件使用
 合适的调试器接口连接至主机——演示是使用 J-Link
 进行开发和调试的。
4. 从 IDE的 '**Project**' 菜单中选择 '**Build Target**'。
 RTOS演示项目的构建应该不会报错或出现警告。
5. 构建完成后，从 IDE 的 '**Debug**' 菜单中选择 '**Start/Stop Debug Session**'
 对 Cortex-M7 微控制器进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。



  





---


### RTOS 配置和用法详情



  



### ARM Cortex-M7 FreeRTOS 移植特定配置


此演示的特定配置项目包含在文件 FreeRTOS/Demo/CORTEX_M7_SAMV71_Xplained_IAR_Keil/FreeRTOSConfig.h
或 FreeRTOS/Demo/CORTEX_M7_SAME70_Xplained_IAR_Keil/FreeRTOSConfig.h。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。特别是：

* **configTICK_RATE_HZ**

 此常量设置了 RTOS tick 中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。
 降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 鉴于 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位未移位值，并且被定义为作为原始数据直接在
 ARM CORTEX-M7 NVIC 寄存器中用作原始数字，configLIBRARY_lowest_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 为等效，定义为仅使用 SAMV7 和 SAME7 NVIC 中实现的 3 个优先位
 。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未移位的 3 位格式。



请注意！请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小表示中断优先级越高。这一点
可能有悖直觉，容易混淆！如果要将
中断设置为低优先级，请不要将其优先级指定为 0（或其他低数值），
因为这会导致该中断在系统中具有
最高优先级，并且如果这个优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，可能会导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
因此是最高优先级。



ARM Cortex-M 核心的最低优先级实际上是 255，但是不同的
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位，
并提供优先级指定方式不同的库函数。例如，
在 Atmel SAMV7/SAME7 ARM CORTEX-M7 微控制器上，您可以指定的最低优先级实际上是 7，这是由
FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。



我们还建议确保将所有优先级位分配为
抢占式优先级位，并且不设置子优先级位，就和演示
中的一样。





每个移植都会将 'BaseType_t' 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。





  


### 中断服务程序



与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。



下列源代码片段仅作为示例提供。中断
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
与任务同步（未显示），并调用 portEND_SWITCHING_ISR
以确保中断直接返回任务。




```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification
 then sending the notification will have removed the task from the Blocked
 state. If the task left the Blocked state, and if the priority of the task
 is higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the
 portEND_SWITCHING_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```


只有以 “FromISR” 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_interrupt_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。


  



### FreeRTOS 使用的资源


FreeRTOS 需要独占 SysTick 和 PendSV 中断。其也使用 SVC 编号 #0。


  


### 在抢占式和协同式 RTOS 内核之间切换


将 FreeRTOSConfig.h 内的 configUSE_PREEMPTION 定义设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M7 演示应用项目中以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


### 其他事项


请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










