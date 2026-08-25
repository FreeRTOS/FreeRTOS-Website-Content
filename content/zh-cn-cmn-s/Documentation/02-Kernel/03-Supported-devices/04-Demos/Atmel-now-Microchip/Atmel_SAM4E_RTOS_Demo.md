---
title: "Atmel SAM4E-EK"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel SAM4E-EK 上的 FreeRTOS

包括 FreeRTOS-Plus-CLI、FreeRTOS-Plus-FAT SL 和 FreeRTOS-Plus-UDP
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]



### 简介



此页面显示了 [ATSAM4E](https://www.microchip.com/wwwproducts/en/ATSAM4E16E) 的 FreeRTOS 移植和演示应用程序，
ATSAM4E 是 Atmel 的一个 32 位微控制器，
具有 ARM CORTEX-M4F 核心。演示是使用功能丰富并且
免费的 [Atmel Studio](https://www.microchip.com/avr-support/atmel-studio-7) IDE 构建，
并针对 [SAM4E-EK](https://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAM4E-EK) 评估
硬件。

演示项目的配置可用于构建简单的 blinky 演示或
综合测试和演示应用。综合应用程序使用
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
命令行界面、[FreeRTOS-Plus-UDP](FreeRTOS-Plus/FreeRTOS_Plus_UDP/FreeRTOS_Plus_UDP.md) UDP/IP 堆栈和
FreeRTOS-Plus-FAT SL 超精益兼容 DOS 的 FAT 文件系统。



  






|  |  |
| --- | --- |
| <br />[![在 Atmel ARM Cortex-M 微控制器上运行的 RTOS](/media/2018/SAM4E-EK.jpg)](/media/2018/SAM4E-EK.jpg)<br /><br /><br />**具备 FreeRTOS 的 SAM4E-EK jpg<br /> <br />点击放大**<br /><br /> | <br />[![Atmel Studio 中的 ARM Cortex-M4 RTOS 查看器](/media/2018/Atmel_Studio_Plugin.png)](/media/2018/Atmel_Studio_Plugin.png)<br /><br /><br />**Atmel Studio，具有 FreeRTOS 内核<br /> <br />感知插件。点击放大**<br /><br /> |








---


#### 重要提示！使用此 ARM Cortex-M4F 演示的注意事项


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---



  



### 源代码组织



FreeRTOS 下载内容包含
所有 RTOS 移植的源代码和演示应用程序项目，因此它包含的大多数文件与
SAM4E-EK 演示无关。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
所下载文件的描述。

构建 SAM4E-EK Atmel 演示的 RTOS Studio 项目位于
FreeRTOS/Demo/CORTEX_M4_ATSAM4E_Atmel_Studio 目录下。**注意：**
Atmel Studio 项目引用来自
FreeRTOS 和 FreeRTOS-Plus 目录树内多个目录的文件，因此项目将仅从此目录生成。



  



### 演示应用程序


#### 功能


常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于
main.c 的顶部，用于在简单 "blinky" 样式的入门项目
以及更全面的应用程序之间进行切换，其中包括额外的 FreeRTOS-Plus
命令行、联网和 FAT 文件系统组件。

  



##### 当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1


当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 调用 main_blinky()。
main_blinky() 会创建一个非常简单的示例，示例使用一个软件定时器，一个
队列和两个任务。
* Blinky 软件定时器：

 此示例展示了自动重载的软件定时器。定时器回调
 的唯一功能是切换 LED。
* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 任务位于每 200 毫秒向队列发送一次值 100
 的循环中。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 实现。任务位于一个循环中，阻止
 从队列读取的尝试（在阻塞时不消耗 CPU 周期），
 每收到一个值就切换一个 LED。队列发送任务
 每 200 毫秒写入队列，所以队列接收任务
 每 200 毫秒切换一次 LED。



  



##### 当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0


当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 调用 main_full()。
main_full() 会创建一个交互式测试和演示应用程序，
这个应用程序会创建大量 RTOS 任务和软件定时器，包括网络连接。

如果 [ipconfigUSE_DHCP](FreeRTOS-Plus/FreeRTOS_Plus_UDP/UDP_IP_Configuration.md#constants_affecting_dhcp_and_dns_behaviour)
 在 [FreeRTOSIPConfig.h](FreeRTOS-Plus/FreeRTOS_Plus_UDP/UDP_IP_Configuration.md) 中设置为 1，则 SAM4E-EK 必须
连接到包含 DHCP 服务器的网络中。如果 ipconfigUSE_DHCP
在 FreeRTOSIPConfig.h 中设置为 0，则演示将使用静态 IP 地址，
这个地址是由 configIP_ADDR0 到 configIP_ADDR3 之间的常量配置，这些常量的定义见
FreeRTOSConfig.h（而非 FreeRTOSIPConfig.h）。在每种情况下， 使用的 IP 地址
获取后会显示在 LCD 屏幕上。



静态 IP 地址
必须与它们所连接的网络兼容。如果
配置的 IP 地址的前三个八进制数与
已经在网络中的其他 IP 地址的前三个八进制数相匹配，那么就能确保它们是兼容的。



配置 MAC 地址使用的是
同样在 FreeRTOSConfig.h 中定义的常量 configMAC_ADDR0 到 configMAC_ADDR5。每个
连接到网络的节点必须使用唯一的 MAC 地址。



演示中包含的功能：


* **FreeRTOS-Plus-CLI，通过 FreeRTOS-Plus-UDP 套接字**访问 

 FreeRTOS-Plus-UDP 用于为命令行接口提供输入和输出
 。可以通过
 任何 UDP 哑终端访问命令行接口。默认情况下，端口 5001 用于发送到
 CLI，端口 5002 用于接收来自 CLI 的回复。
 下图显示了将免费
 [YAT 终端](https://sourceforge.net/projects/y-a-terminal/)
 用于此目的时所需的配置。



 在 FreeRTOS-Plus-CLI 中，输入 “help” 来查看已注册
 命令的列表，在这种情况下包括
 一组通用命令、一组 FAT 文件系统相关命令，
 和一组与联网相关的命令。



 请注意，至少在撰写本文时，演示中的网络驱动程序
 只具有基本功能，
 不会展示以太网硬件的全部功能。
   









|  |  |
| --- | --- |
| <br />[![通过 UDP 联网连接到 RTOS](/media/2018/connecting_yat_to_the_CLI.jpg)](/media/2018/connecting_yat_to_the_CLI.jpg)<br /><br /><br />**配置 YAT 以连接到<br /> <br /> CLI（IP 地址：192.168.0.13）。<br /> <br /> 点击放大。**<br /><br /> | <br />[![RTOS 命令行会话](/media/2018/a_sample_cli_session.jpg)](/media/2018/a_sample_cli_session.jpg)<br /><br /><br />**CLI 会话示例。< br/> < br/> 点击放大**<br /><br /> |
* **使用 FreeRTOS-Plus-FAT SL 创建、查看、复制和删除文件** 

 FAT 文件系统创建一组示例文件，可以通过
 命令行界面访问并操作。此示例
 的功能与
 [-Plus FreeRTOS-FAT SL Win32 模拟器演示文档页面](FreeRTOS-Plus/FreeRTOS_Plus_FAT_SL/Demos/File_System_Win32_Simulator_demo.md)中的描述相同，
 - 此页面中还有一个演示视频。**注意：**使用
 **此页面**上的说明来连接 CLI，请勿参考
 Win32 演示页面上或视频中的说明。
* **FreeRTOS-Plus-UDP 回显客户端示例** 

 如果将 mainINCLUDE_ECHO_CLIENT_TASKS 在 main_full.c 的顶部设置为 1，
 则将创建[标准 UDP 回显示例](FreeRTOS-Plus/FreeRTOS_Plus_UDP/Embedded_Ethernet_Examples/Common_Echo_Clients.md)
 。回显服务器的 IP 地址由
 常量 configECHO_SERVER_ADDR0 到 configECHO_SERVER_ADDR3 设定，
 这些常量位于 FreeRTOSConfig.h。
* **标准演示任务和检查软件定时器** 

 该演示创建了大量[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)。
 这些任务没有特定的
 功能，只用于测试 RTOS 移植并演示 FreeRTOS
 API。



 标记为 D2 的 LED 由一个标准演示软件定时器以闪烁的形式控制。



 会创建一个“检查软件定时器”，为
 标准演示任务的状态提供视觉反馈。软件定时器监控所有其他
 任务，然后切换 LED D4。如果所有其他任务都如期正常运行。
 那么 LED 将每 3 秒切换一次。如果在其他任何任务中
 发现疑似错误，那么 LED 的切换频率将增加到
 每 200 毫秒一次。


  


#### 使用 Atmel Studio 构建和调试演示应用程序


1. 从 Atmel Studio IDE 中打开项目（关于项目的名称和位置，
 请参阅本页面顶部的
 源代码组织章节）。
2. 使用合适的调试器接口连接到 SAM4E-EK 硬件。示例
 项目是使用 J-Link 创建和测试的。
3. 从 Atmel Studio 的 "Build" 菜单中选择 "Rebuild RTOSDemo"（或按 F7）
 以构建演示项目。
4. 从 Atmel Studio 的 "Debug" 菜单中选择 "Start Debugging and Break"
 对微控制器闪存进行编程并且启动调试会话。


  




  



### 配置和使用详情


#### ARM Cortex-M4 FreeRTOS 移植特定配置


此演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_M4_ATSAM4E_Atmel_Studio/src/config/FreeRTOSConfig.h 中。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。特别是：

* **configTICK_RATE_HZ** 

 此常量设置了 RTOS tick 中断的频率。此演示
 使用的设置取决于 configCREATE_LOW_POWER_DEMO 设置。
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





每个移植将 'BaseType_t' 定义为该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。





  


#### 中断服务程序



与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。



下列源代码片段仅作为示例提供。中断
使用信号量与任务（未显示）同步，并调用 portEND_SWITCHING_ISR()
以确保如果任务的优先级等同或高于中断优先级，
则中断会直接返回到任务。




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


  



#### FreeRTOS 使用的资源


FreeRTOS 需要独占 SysTick 和 PendSV 中断。其也使用 SVC 编号 #0。


  


#### 抢占式内核和协同式 RTOS 内核之间的切换


将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

  


#### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


#### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M4 演示应用项目中，以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


#### 其他事项



请注意，vPortEndScheduler() 尚未实现。



   

  

  

  

  










