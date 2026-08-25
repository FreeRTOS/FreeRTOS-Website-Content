---
title: "SAMA5D3 (ARM Cortex-A5) RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---





 SAMA5D3 (ARM Cortex-A5) RTOS 演示


 包括使用 IAR 嵌入式编译器的 FreeRTOS-Plus-CLI

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![Atmel Cortex-A5 RTOS](/media/2018/SAMA5D3_Xplained.jpg)

  




### 简介


此页面记录了一个 FreeRTOS 演示应用程序。
该应用程序运行于 Atmel ATSAMA5D3 嵌入式处理器。ATSAMA5D3 具有 ARM Cortex-A5 核心和一个
Atmel 高级中断控制器 (AIC)。预置 RTOS 示例
项目构建使用 ARM 编译器和 IDE 的 [IAR 嵌入式工作台](http://www.iar.com/ewarm)
并针对 [SAMA5D3 Xplained](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D3-XPLD) 评估板。

  







[![Atmel Cortex-A5 RTOS](/media/2018/SAMA5_ARM_Cortex-A5.png)](/media/2018/SAMA5_ARM_Cortex-A5.png)

  

**运行 SAMA5 RTOS 演示的 EWARM 中的 RTOS 状态查看器窗口
   

 点击放大** 







---


#### *重要提示！关于使用 FreeRTOS Atmel SAMA5 演示项目的注意事项*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#atmel-sama5-arm-cortex-a5-演示应用程序)
3. [构建说明](#构建说明)
4. [RTOS 配置和使用详情](#rtos-配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)，以及
在
[不配备
 GIC 的 ARM Cortex-A 处理器上使用 FreeRTOS 的相关说明页面](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)[SAMA5 使用 Atmel 自带的高级
中断控制器 (AIC) 而不是 ARM 的通用中断控制器 (GIC)]。


---


### 源代码组织


FreeRTOS zip 文件包含所有 RTOS 移植和所有
RTOS 演示应用程序的源代码。这些文件中只有一小部分要用于
Atmel SAMA5 ARM CORTEX-A5 RTOS 演示应用程序。[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面描述
FreeRTOS zip 文件下载包的结构，并提供
关于如何创建新 RTOS 项目的信息。

IAR 嵌入式工作台项目文件位于 FreeRTOS/Demo/cortex_A5_SAMA5D3x_Xplained_IAR
目录。



IAR 项目包括
/FreeRTOS-Plus 目录中包含的文件，因此
如果 /FreeRTOS-Plus 目录已删除或移出默认位置，则不会构建项目
。



  





---


### Atmel SAMA5 ARM Cortex-A5 演示应用程序



#### 硬件和软件设置



不需要特定的硬件配置。

  



#### 功能



常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
定义在 main.c 的顶部，用于在非常基本的
“blinky” 演示与全面的测试和演示应用程序之间切换。
  



#### mainCREATE_SIMPLE_Blinky_DEMO_ONLY 设置为 1 的功能



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky 函数。

main_blinky() 函数创建一个简单的演示，其中包括两个
任务和一个队列。第一个任务（队列发送任务）使用队列来
反复发送数字
100 给第二任务（队列接收任务）。接收任务会
在每次收到消息时，切换 LED 的状态
。消息每 200 毫秒发送一次，因此 LED 的状态将
每 200 毫秒切换一次。




  



#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 的功能




[![Atmel Cortex-A5 RTOS](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

  

**CLI 中查看的运行时统计信息
   

 点击放大** 



如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。

main_full() 会创建一个全面测试和演示应用程序
以展示：



* [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口。
* Atmel USB 设备 CDC 驱动程序。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。


由 USB 设备 CDC 驱动程序创建的虚拟 COM 端口
被用作 CLI 的输入和输出接口。
在 Windows 设备上安装虚拟 COM 端口所需的 .inf 文件
名为 6119.inf，与 IAR 项目位于相同的目录下。
使用枚举的
虚拟 COM 移植，通过哑终端程序连接到 FreeRTOS-Plus-CLI，
例如 [Tera Term](http://en.sourceforge.jp/projects/ttssh2/releases/)
或超级终端，以 115200 bps 的波特率显示信息。与 FreeRTOS-Plus-CLI 一样，
在 CLI 中键入 'help' 来查看注册命令列表。

SAM5 ARM CORTEX-A5 Xplained 评估板通过它的 USB 设备端口供电，
因此，一旦 RTOS 演示应用程序开始执行，USB CDC 设备将枚举，
并且每次重新启动 RTOS 演示应用程序时都将重新枚举。
这意味着终端程序无法连接到虚拟 COM 端口，直到
RTOS 应用程序开始运行。
每次停止并重新启动 RTOS 演示应用程序时，终端程序都必须和虚拟 COM 端口断开连接并重新建立连接。



完整演示创建的大多数其他任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务集
。这些任务由所有 RTOS 演示应用程序使用，适用于任何编译器和
任何架构。它们虽然不具有特定的功能，但确实演示了用到的 RTOS
API 并测试了 RTOS 内核移植。



应用程序在最后会创建“检查”任务。检查任务定期查询标准 RTOS
演示任务，确保它们按预期运行。
检查任务还切换 LED 状态，为系统状态提供视觉指示。
**如果检查任务没有检测到任何可能的错误，它将
每三秒钟切换一次 LED 状态。如果检查任务
检测到潜在错误，则将每 200 毫秒切换一次 LED 状态**。



**注意：**一些标准演示任务会检查自带的计时。
如果处理 USB 中断所花费的时间过多，
计时检查会失败（导致“检查”任务收到错误报告）。



  





---


### 构建说明


#### 构建和执行演示应用程序


请注意，RTOS 演示项目引用了 /FreeRTOS-Plus
和 /FreeRTOS/Demo/Common 目录中的通用文件，因此
如果 /FreeRTOS-Plus 已删除或从其默认位置移出，则项目将不会编译。
1. 从嵌入式工作台 (EWARM) IDE 内部打开 FreeRTOS/Demo/CORTEX_A5_SAMA5D3x_Xplained_IAR/RTOSDemo.eww
 。
2. 打开 main.c 并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，根据需要生成
 简单的闪烁演示项目或完整的测试和演示应用程序。
3. 在 IDE 的 "Project" 菜单中选择 "Build All"，或按 F7 构建
 演示。演示构建时， FreeRTOS 相关文件
 不应生成任何错误或警告。
4. 确保目标硬件连接到
 使用该硬件 USB 连接器的主机。
5. 在 IDE 的 "Project" 窗口中选择 "Download and Debug"，下载
 已经构建的可执行文件到 ARM Cortex-A5 RAM 并启动调试会话。



  





---


### RTOS 配置和用法详情


#### FreeRTOS ARM Cortex-A 移植特定配置


请注意：一些 ARM Cortex-A 处理器
使用其自带的通用中断控制器 (GIC)，而其他处理器，例如
SAMA5D3 采用专有的中断控制器。我们还有专门的网页
介绍在两个场景中使用 RTOS 的方法。那么
请参阅
介绍[在未集成 
ARM 通用终端控制器的 ARM Cortex-A 嵌入式处理器上使用 RTOS 的相关说明
](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)。


此演示的特定配置内容位于
FreeRTOS/Demo/CORTEX_A5_SAMA5D3x_Xplained_IAR/FreeRTOSConfig.h 头
文件。


  



#### FreeRTOS 使用的资源


此演示项目配置为从 PIT（周期中断控制器）中生成 RTOS
tick 中断。RTOS 使用的其他资源记录
在
[
有关在未集成 
ARM 通用中断控制器](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)的 ARM Cortex-A 嵌入式处理器上使用 RTOS 的说明页面上（如前所述）。

  


#### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-A 演示应用程序项目中，用于
为 RTOS 内核分配所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


#### 其他事项



请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










