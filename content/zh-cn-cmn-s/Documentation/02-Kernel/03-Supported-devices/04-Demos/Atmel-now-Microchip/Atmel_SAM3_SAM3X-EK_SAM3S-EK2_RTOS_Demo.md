---
title: "Atmel SAM3 RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel SAM3 RTOS 演示使用免费 Atmel Studio 6 IDE、GCC 和 Atmel 软件框架

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![的 SAM3 微控制器 Atmel](/media/2018/SAM4.jpg)

  

### 简介


此页介绍了 [Atmel Studio 6 IDE](https://www.microchip.com/avr-support/atmel-studio-7) RTOS 演示应用程序在
[SAM3S](http://www.microchip.com/wwwproducts/en/ATSAM3S1C) 及
[SAM3X](http://www.microchip.com/wwwproducts/en/ATsam3x8e) ARM Cortex-M3 微控制器上运行
（这两款微控制器均来自 Atmel）。演示
使用 FreeRTOS GCC ARM Cortex-M3 移植和
综合 [Atmel 软件框架](https://www.microchip.com/avr-support/advanced-software-framework-(asf)的组件
(ASF) 的组件。

此外提供了两个预配置的项目。一个预配置项目在 SAM3S-EK2 评估工具上运行，
另一个在 SAM3X-EK 评估工具上运行。







---


#### *重要提示！FreeRTOS SAM3 演示项目*的使用说明


*使用此 RTOS 移植之前，请阅读以下所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#atmel-studio-arm-cortex-m3-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织


为便于分发，官方 FreeRTOS zip 文件下载
包含所有 RTOS 移植和所有 RTOS 演示应用程序
的源代码文件。此页上显示的项目只需要这些文件的
一个小子集。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
的相关信息。

ATSAM3S-EK2 演示应用程序的 Atmel Studio 6 解决方案文件称为
RTOSDemo.atsln，位于 FreeRTOS/Demo/CORTEX_ATSAM3S-EK2_Atmel_Studio
目录下。



ATSAM3X-EK 演示应用程序的 Atmel Studio 6 解决方案文件同样称为
RTOSDemo.atsln，位于 FreeRTOS/Demo/CORTEX_ATSAM3X_Atmel_Studio
目录下。



此页中的[项目目录结构准备](#构建和执行演示应用程序)章节
包含此目录准备相关的重要信息。



  





---


### Atmel Studio ARM Cortex-M3 演示应用程序


  



#### 硬件设置



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0（请参阅下文功能
章节），则演示中将包括标准的 com 测试任务。标准
演示 com 测试会创建两个任务：将字符发送到 USART 的 Tx 任务
和预期接收 Tx 任务发送的每个字符的 Rx 任务。USART 端口
需要一个环回连接器才能让此机制正常运行：只需
在 SAM3S-EK2 和 SAM3X-EK 硬件中标记为 “USART” 的九针连接器上
将引脚 2 与引脚 3 相连。

应该注意的是，添加 com 测试任务是为了演示
任务和中断之间通讯使用的队列，以及
从内部中断服务例程执行上下文切换。使用的
串行驱动程序**不是**为了展示高效的实现过程。
实际应用程序应使用 USART 的外围 DMA 通道 (PDC)。



  



#### 功能性



mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。演示的行为
取决于其设置。
  



#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：

* **main_blinky() 函数：** 

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 RTOS 调度器。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
 它每隔 200 毫秒向队列发送数值 100。
* **队列接收任务:** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 在main_blinky.c中。它以块时间从队列中反复读取
 如果队列为空，则此任务会进入[阻塞状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)
 。因此每次从队列中收到数值 100 时，此任务都会切换
 红色/橙色 LED,因为队列发送任务
 每隔 200 毫秒就向队列发送数值，队列接收任务应退出
 已阻塞状态并每隔 200 毫秒切换红色/橙色 LED。



  



#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：

* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* 引发 RTOS 任务上下文切换的简单中断服务例程。


创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API
如何测试 RTOS 移植。

main() 创建 34 个任务和 3 个软件定时器后会
启动 RTOS 调度器。然后，演示在运行期间动态地连续创建
创建并删除另外两个任务。



创建“检查”软件定时器，定期检查标准
演示任务，以确保所有任务都能
正常运行。check 软件定时器的
回调函数切换 SAM3 开发硬件上的绿色 LED。
这为系统健康提供了
直观反馈。**如果 LED 每 3 秒钟切换一次，则表示
检查软件定时器未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查软件定时器已
在一个或多个任务中发现了问题。**如需测试这个机制，可以
移除环回连接器。这么做会导致
com 测试任务失败。



  



#### 项目目录结构准备



Atmel Studio要求项目构建的所有源文件所在的目录，或所
包含 Atmel Studio 项目本身的目录或其子目录下。
因此，有必要将演示应用程序使用的 FreeRTOS
和演示应用程序使用的标准演示源文件
它们在标准 FreeRTOS 目录结构中的位置复制到
目录中复制。提供一个名为CreateProjectDirectoryStructure.bat的批处理文件
来完成复制操作。

CreateProjectDirectoryStructure.bat
与 Atmel Studio 6 解决方案位于相同的目录下，
**而且必须先执行完毕才能
成功构建**演示应用程序。



  



#### 构建和执行演示应用程序


1. 确保 CreateProjectDirectoryStructure.bat batch file 批处理文件已执行。
2. 打开 FreeRTOS/Demo/CORTEX_ATSAM3S-EK2_Atmel_Studio/RTOSDemo.atsln
 或 FreeRTOS/Demo/CORTEX_ATSAM3X_Atmel_Studio/RTOSDemo.atsln
 （根据适用情况而定）从 Atmel Studio IDE 中打开。
3. 打开 main.c，将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为生成
 简单的 blinky 演示，或完整的测试和演示应用程序
 。
4. 确保目标硬件连接使用
 合适的J-Link或SAM-ICE接口连接到计算机。此项目使用
 J -Link 创建。
5. 从 IDE 的 ‘构建 (Build)’菜单中选择 '构建解决方案 (Build Solution)'，
 RTOS演示项目的构建应该不会报错或出现警告。
6. 构建完成后，从 IDE 的调试 (Debug) 菜单中选择“开始调试并中断 (Start Debug and Break)”
 对 SAM3 微控制器闪存进行编程，启动调试
 会话，并让调试程序在进入 main() 函数时中断。



  





---


### RTOS 配置和使用详情



  



#### ARM Cortex-M3 FreeRTOS 移植特定配置


此演示的特定配置项目位于 FreeRTOS/Demo/CORTEX_ATSAM3S-EK2_Atmel_Studio/src/FreeRTOSConfig.h
或 FreeRTOS/Demo/CORTEX_ATSAM3X_Atmel_Studio/src/FreeRTOSConfig.h，具体取决于正在使用的项目。
[您可以编辑此文件中定义的常量，使其适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。特别是：

* **configTICK_RATE_HZ** 

 此常量设置了 RTOS tick 中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。
 降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY** 

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位移位值，根据定义可作为原始数字直接用于
 ARM CORTEX-M3 NVIC 寄存器中，但 configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是等效常量，仅通过 SAM3 NVIC 中实现的
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
Atmel SAM3 ARM Cortex-M3 微控制器上可以指定的最低优先级实际上为 15——这是由
FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
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



与所有的端口一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


#### 内存分配


ARM Cortex-M3 演示应用程序项目中包含 Source/Portable/MemMang/heap_4.c，用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 章节获取
以获取完整信息。

  


#### 其他事项



请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










