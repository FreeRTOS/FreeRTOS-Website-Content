---
title: "Atmel SAM4S RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel SAM4S RTOS 演示使用免费的 Atmel Studio 6 IDE、GCC 和 Atmel 软件框架

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![Atmel 的 SAM4 微控制器](/media/2018/SAM4.jpg)

  

### 简介


此页面记录 FreeRTOS 演示应用程序，适用于
[SAM4S ARM Cortex-M4 微控制器](https://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-4s-mcus)
（此微控制器来自 Atmel）。演示
使用 FreeRTOS GCC ARM Cortex-M3/4 移植、免费
[Atmel Studio 6 IDE](https://www.microchip.com/avr-support/atmel-studio-7) 和
综合 [Atmel 软件框架](https://www.microchip.com/avr-support/advanced-software-framework-(asf)
(ASF) 的组件。该项目被预先配置为在 SAM4S-EK 评估套件上运行。





---


### *重要提示！关于使用 FreeRTOS SAM4S 演示项目*的说明


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#atmel-arm-cortex-m4-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织


FreeRTOS zip 文件包含所有 FreeRTOS 的源文件
移植的源文件和所有演示应用程序，其中只有少数
是本项目需要的。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
新项目。

ATSAM4S 演示应用程序的 Atmel Studio 6 Solution 文件名为
RTOSDemo.atsln，位于 FreeRTOS/Demo/CORTEX_M4_ATSAM4S_Atmel_Studio
目录中。



此页中的[项目目录结构准备](#构建和执行演示应用程序)章节
包含有关准备此目录的重要信息。



  





---


### Atmel ARM Cortex-M4 演示应用程序


  



### 硬件设置



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0（请参阅下文功能
章节），则演示中将包括标准的 com 测试任务。标准
演示 com 测试会创建两个任务：将字符发送到 USART 的 Tx 任务
和预期接收 Tx 任务发送的每个字符的 Rx 任务。USART 端口
需要一个环回连接器才能让此机制正常运行：只需
在 9 路连接器上将引脚 2 连接至引脚 3，此连接器在 SAM4S-EK 上标记为“USART”
。

应该注意的是，添加 com 测试任务是为了演示
任务和中断之间通讯使用的队列，以及
在中断服务程序中执行的上下文切换。使用的
串行驱动程序**不是**为了展示高效的实现过程。
实际应用程序应使用 USART 的外围 DMA 通道 (PDC)。



  



### 功能性



mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。演示的行为
取决于其设置。
  



### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：

* **main_blinky() 函数：** 

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 RTOS 调度器。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
 它每隔 200 毫秒向队列发送数值 100。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 。它以指定的块时间从队列中反复读取，
 如果队列为空，则此任务会进入[阻塞状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)
 。每次从队列接收的值为 100 时，任务都切换红色 LED。
 因此，由于队列发送任务每 200 毫秒向队列发送一次，
 队列接收任务应退出
 阻塞状态，每 200 毫秒切换红色 LED。



  



### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：

* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* 引发 RTOS 任务上下文切换的简单中断服务程序。


创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
如何测试 RTOS 移植。

main() 创建 34 个任务和 3 个软件定时器后会
启动 RTOS 调度器。然后，演示在运行期间动态地连续
创建并删除另外两个任务。



创建“检查”软件定时器，定期检查标准
演示任务，以确保所有任务都能
正常运行。检查软件定时器
回调函数切换 SAM4S-EK 硬件上的绿色 LED。
这给出了
直观反馈。**如果 LED 每 3 秒钟切换一次，则表示
检查软件定时器未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查软件定时器已
在一个或多个任务中发现了问题。**如需测试这个机制，可以
移除环回连接器。这么做会导致
com 测试任务失败。



  



### 项目目录结构准备



Atmel Studio 要求项目构建的所有源文件位于
包含 Atmel Studio 项目本身的目录或其子目录下。
因此，有必要将演示应用程序使用的 FreeRTOS
和标准演示源文件从
它们在标准 FreeRTOS 目录结构中的位置复制到演示
目录中。提供一个名为 CreateProjectDirectoryStructure.bat 的批处理文件
完成此功能。

CreateProjectDirectoryStructure.bat 位于 FreeRTOS/Demo/CORTEX_M4_ATSAM4S_Atmel_Studio，
**而且必须先执行完毕才能成功构建
演示应用程序**。



  



### 构建和执行演示应用程序


1. 确保已执行 CreateProjectDirectoryStructure.bat 批处理文件。
2. 打开 FreeRTOS/Demo/CORTEX_M4_ATSAM4S_Atmel_Studio/RTOSDemo.atsln，
 其位于 Atmel Studio IDE 中。
3. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
4. 确保目标硬件连接使用
 合适的 J-Link 或 SAM-ICE 接口连接到主机计算机。此项目使用
 J -Link 创建。
5. 从 IDE 的 ‘构建 (Build)’菜单中选择 '构建解决方案 (Build Solution)'，
 RTOS演示项目构建时不应报错或出现警告。
6. 构建完成后，从 IDE 的 Debug 菜单中选择 "Start Debug and Break"
 对 SAM4S 微控制器闪存进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。



  





---


### RTOS 配置和用法详情



  



### ARM Cortex-M4 FreeRTOS 移植特定配置


此演示的特定配置项位于 FreeRTOS/Demo/CORTEX_M4_ATSAM4S_Atmel_Studio/src/FreeRTOSConfig.h。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。特别是：

* **configTICK_RATE_HZ** 

 此常量设置了 RTOS tick 中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。
 降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY** 

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位移位值，根据定义可作为原始数字直接用于
 ARM Cortex-M4 NVIC 寄存器。configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 与其等效，但定义为仅使用 4 个优先级位，这些位在 SAM4
 NVIC 中实现。
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
FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。



我们还建议确保将所有优先级位分配为
抢占式优先级位，并且不设置子优先级位，就和演示
中的一样。





每个移植都将 'BaseType_t' 定义为该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。





  


### 中断服务程序



与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。



下列源代码片段仅作为示例提供。中断
使用信号量与任务（未显示）同步，并调用 portEND_SWITCHING_ISR
以确保中断直接返回任务。参见函数
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
中断服务程序中调用，而且中断的优先级须
小于或等于 configMAX_SYSCALL_interrupt_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。


  



### FreeRTOS 使用的资源


FreeRTOS 需要独占使用 SysTick 和 PendSV 中断。其也使用 SVC 编号 #0。


  


### 抢占式内核和协同式 RTOS 内核之间的切换


将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M4 演示应用项目中，以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


### 其他事项



请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










