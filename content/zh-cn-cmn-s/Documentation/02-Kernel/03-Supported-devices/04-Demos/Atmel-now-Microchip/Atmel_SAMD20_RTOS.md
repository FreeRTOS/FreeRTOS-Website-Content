---
title: "Atmel SAMD20"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---




 Atmel [SAMD20](https://www.microchip.com/wwwproducts/en/ATSAMD20G18) ARM [Cortex-M0+](http://www.arm.com/products/processors/cortex-m/cortex-m0plus.php) 演示


使用FreeRTOS Studio 和 GCC 构建的 FreeRTOS和 Atmel -Plus-CLI

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  




|  |
| --- |
| <br />![Atmel SAMD20 ARM Cortex-M0+ MCU](/media/2018/SAMD20.jpg)<br /><br /><br />**SAMD20 Xplained PRO** <br /><br /> |






### 引言



此页面描述了一个演示项目，该项目使用了 FreeRTOS 和
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
在来自 Atmel的 SAMD20 Cortex-M0+ 微控制器上。

该项目使用 FreeRTOS ARM Cortex-M0 GCC 端口、通过免费的
[Atmel Studio IDE](https://www.microchip.com/avr-support/atmel-studio-7)（使用 Visual Studio 框架
并且包括一个内核意识FreeRTOS插件）构建 ，并且针对
成本非常低的 [SAMD20 Xplained Pro](http://www.microchipdirect.comPartDetail.aspx/?q=p:10500351#tc:description)
评估板。



命令行接口字符输入和输出使用
Atmel 在其 Atmel 软件框架（[ASF](https://www.microchip.com/avr-support/advanced-software-framework-(asf)）中提供的驱动程序。



\#define 用于在简单的 blinky 应用程序和
包含 FreeRTOS-Plus-CLI 组件的综合测试和演示应用程序之间
切换构建。



  




![](/media/2018/Atmel_Studio_Plugin.png)
  


**带有 Kernel Aware FreeRTOS 插件的 Atmel Studio IDE** 



  





---


#### *重要提示！关于使用 SAMD20 ARM Cortex-M0 + 演示的说明*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)


另请参阅常见问题：[我的应用程序未
运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)
  





---


### 源代码组织


FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此
包含比 SAMD20 演示所需更多的文件。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
了解目录结构说明。

Atmel Studio 解决方案文件名为RTOS Demo.atsln ，位于
FreeRTOS/演示/CORTEX_M0 +_Atmel_SAMD20_Xplained 目录。



  





---


### 构建和运行 ARM CORTEX-M0 + RTOS 应用程序


1. 打开 FreeRTOS/Demo/CORTEX_M0+_Atmel_SAMD20_Xplained/RTOSDemo.atsln
 （从 Atmel Studio IDE 中打开）。
2. 在 main.c 顶部找到mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 定义
 。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 以创建简单的
 blinky 演示，或设置为 0 来创建全面的演示，其中也包括
 命令行解释器。
3. 从 Atmel Studio “构建”菜单中选择“重建 RTOS 演示” （或按F7 ）以构建
 演示项目。
4. 在 SAMD20 Xplained Pro 板的 USB 端口
 和主机之间连接 USB 电缆。
5. 从 Atmel Studio “调试”菜单中选择“开始调试并中断”
 对微控制器闪存进行编程并启动调试
 会话。



  




### 演示应用程序功能


#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY  设置为 1 的功能



在  mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 的情况下进行构建会导致  main () 调用
main_blinky ()。main_blinky () 演示的介绍如下。

* **main_blinky() 函数：** 

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 调度器。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask () 执行。



 在将值 100 发送至 main_blinky () 中创建的队列前，prvQueueSendTask () 反复阻止了 200 毫秒
 。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的  prvQueueReceiveTask () 执行
 。



 prvQueueReceiveTask() 会重复阻塞
 从 main_blinky() 中创建的队列中读取数据的尝试，
 每次接收到数据时都会切换 LED 指示灯。队列发送任务每 200 毫秒向队列发送数据，
 所以 LED 将每 200 毫秒切换一次。



  



#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 的功能



在 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 的情况下进行构建会导致 main () 调用
main_full ()。下面描述了 main_full () 演示。
* **Main_full () 函数：** 

 main_full() 会创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、一些特定应用程序的测试任务、
 管理 FreeRTOS-Plus-CLI 的任务和定时器。然后它会启动
 调度器。
* **FreeRTOS-Plus-CLI 任务：** 



[![ARM Cortex-M0+](/media/2018/SAMD20_run_time_stats.png)](/media/2018/SAMD20_run_time_stats.png)
  


**单击以放大** 


 SAMD20 Xplained Pro 主板通过单根
 USB 电缆连接到主机计算机。USB 连接提供调试器接口和
 虚拟 COM 端口连接。虚拟 COM 端口用于提供
 命令行接口所需的字符输入和输出
 (CLI)。因此，可以从任何串行终端程序对 CLI 进行访问，
 如超级终端，或如右图 Tera Term 所示的终端程序。

 图像显示 COM 20 正在使用，但很可能是虚拟
 COM 端口将在主机计算机上枚举到不同的端口号。



 与 FreeRTOS-Plus-CLI 一样， “帮助”命令将显示
 已注册（因此可用）的命令列表。在
 执行 'run-time-stats' 命令后，会捕获到图像，该命令会生成一个表，
 显示每个RTOS任务消耗的 CPU 时间量。
* **“注册测试”任务：** 

 这些任务用已知值填充寄存器，然后检查
 每个寄存器在整个任务生命周期内是否保持其预期值
 。每个任务使用不同的值集。包含意外值的寄存器
 表示上下文切换机制中存在错误
 。
* **“检查”软件定时器：** 

 检查[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的周期最初设置为三
 秒。其回调函数检查所有标准演示任务和
 寄存器检查任务是否仍在执行，
 且执行时是否报告任何错误。如果检查定时器回调发现
 任务已停顿，或报告了错误，之后它会将
 检查定时器的周期从最初的三秒钟更改为仅 200 毫秒。回调
 函数还会切换 LED 以显示
 系统状态指示：**如果 LED 每三秒切换一次
 ，则表示未发现任何问题。如果 LED 指示灯每 200 毫秒切换一次，说明
 至少在一个任务中发现了问题**。



  





---


###  RTOS 配置和使用详情


  


#### 中断服务程序



导致上下文切换的中断服务程序
无特殊要求。
portEND_SWITCHING_ISR() 宏可用于从 ISR 内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。




在
main.c 的末端提供名为 Dummy_IRQHandler() 的虚拟中断处理程序作为参考实现。
此外，还在下方对 Dummy_IRQHandler () 进行了复制。






```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
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


请注意，FreeRTOSConfig.h中包含了以下行，以将中断处理程序函数名称FreeRTOS映射
中断处理程序函数映射到 CMSIS 中断处理程序函数名称上。
这使编译器工具供应商提供的链接器脚本可
在无需修改的情况下使用。



```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler

```




  


#### RTOS 端口特定配置


这些演示的特定配置项目包含在 FreeRTOS/Demo/cortex_M0 +_Atmel_SAMD20_Xplained/RTOSDemo/src/config/FreeRTOSConfig.h 中。开发人员
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量设置了 RTOS 滴答中断的频率。提供的 500Hz 值可用于
 测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。



每个移植都将 "BaseType_t" 定义为
最高效的数据类型。所有 ARM Cortex-M0 + 端口都将 BaseType_t 定义为长类型。




请注意 vPortEndScheduler () 尚未实现。



  


#### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M0 + 演示应用项目中，以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分获取
完整信息。







  

  

  

  

  










