---
title: "SAMA5D4 (ARM Cortex-A5) RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---





 SAMA5D4 (ARM Cortex-A5) RTOS 演示


 包括 FreeRTOS-Plus-CLI，并使用 IAR 嵌入式编译器

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![Atmel Cortex-A5 RTOS](/media/2018/SAMA5D4_EK.jpg)

  




### 简介


此页面为 ATSAMA5D4 嵌入式处理器的 FreeRTOS 演示。
Atmel该处理器配备 ARM Cortex-A5 核心和
Atmel 高级中断控制器 (AIC)。预配置 RTOS 示例
（针对
[SAMA5D4-EK](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D4-EK)
评估硬件）旨在为
[IARARM ](http://www.iar.com/ewarm) 嵌入式工作台
嵌入式开发工具提供参考。

  







[![Atmel Cortex-A5 RTOS](/media/2018/SAMA5_ARM_Cortex-A5.png)](/media/2018/SAMA5_ARM_Cortex-A5.png)

  

**运行 SAMA5 RTOS 演示的 EWARM RTOS 状态视图 (State Viewer) 窗口
   

 点击放大** 







---


#### *重要提示！ARM Cortex-A5 RTOS 演示项目*的使用说明


*使用此 RTOS 移植前,请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#atmel-sama5d4-arm-cortex-a5-演示应用程序)
3. [构建说明](#构建说明)
4. [RTOS配置和使用详情](#rtos-配置和使用详情)


另请参阅：
* 常见问题：[我的应用程序没有运行，可能出了什么问题？](/Why-FreeRTOS/FAQs/Troubleshooting)
* 将 RTOS
 [用于 ARM Cortex-A 处理器（不含通用中断控制器 (GIC)）](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)上的操作说明。




---


### 源代码组织


官方 FreeRTOS zip 文件下载中包含所有 RTOS移植
和所有 RTOS 演示项目的源文件。此
AtmelSAMA5D4 ARM Cortex-A5 RTOS 演示应用程序只需要文件的一个小子集。相关
[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面描述了
FreeRTOS zip 文件下载的结构体，并提供了
关于如何创建新 RTOS 项目的信息。

用于构建此演示的 IAR 嵌入式工作台项目位于
FreeRTOS/Demo/CORTEX_A5_SAMA5D4x_EK_IAR 目录下。此项目包括
/FreeRTOS-Plus/Source 目录下的源文件，因此
当 /FreeRTOS-Plus 目录移出默认位置或删除时
不会构建此项目。



  





---


### Atmel SAMA5D4 ARM Cortex-A5 演示应用程序


#### 硬件和软件设置



此演示不需要专门的硬件配置。

  



#### 功能



常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 用于
实现基本的 “blinky” 演示与大型测试和演示应用程序之间的切换。
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 定义于 main.c 顶部。
  



##### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能



mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 调用 main_blinky()。

main_blinky() 创建一个非常基本的演示，这个演示只创建两个
任务和一个队列。第一个任务（队列发送任务）通过队列
反复发送数字 100 给第二任务（队列接收任务）。队列
接收任务每次接到数据
就会切换 LED。每隔 200 毫秒就会有数据发送到队列，因此队列
接收任务每隔 200 毫秒切换一次 LED。




  



##### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能




[![Atmel Cortex-A5 RTOS](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

  

**在 CLI 中查看的运行时统计信息
   

 点击放大** 



当将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。

main_full() 创建一个综合演示和测试应用程序，此程序会演示：



* [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口和解释器。
* Atmel 自带的 USB CDC 驱动程序，为 CLI 提供输入和输出。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。


在 Windows 计算机上安装 CDC 虚拟 COM 端口所需的 .inf 文件
称为 6119.inf，与 IAR 项目位于相同的目录下。
哑终端程序，例如
[Tera Term](http://en.sourceforge.jp/projects/ttssh2/releases/)
或 Hyperterminal 可用于通过枚举的虚拟 COM 端口连接 CLI。
其传输速率为 115200 baud。
按照 FreeRTOS-Plus-CLI 的惯例，在 CLI 中键入 'help' 可以查看
已注册命令列表。

RTOS 演示应用程序启动执行后， USB CDC 设备将立刻开始枚举，
并且在 RTOS 演示应用程序每次重启时都将重新枚举。
这意味着
在 RTOS 应用程序真正运行前，终端程序无法连接到虚拟 COM 端口，而且每次
RTOS 演示重新开始时，终端程序都必须断开然后重新连接到 CDC 虚拟 COM 端口。
如果 RTOS 演示停止或重新开始之前未断开哑终端与 CDC 端口之间的连接，
那么创建另一个连接之前可能需要
关闭并重启哑终端程序。



完整演示中创建的许多其他任务来自[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)集。
标准演示任务由 RTOS 演示应用程序用于每个 RTOS 移植，
它们没有特定的功能。这些任务用于演示 RTOS
正在使用的 API 函数，测试 RTOS 架构移植。



演示还创建了一个 'check' 任务。Check 任务定期检查
标准 RTOS 演示任务的状态，确保它们按预期运行。
Check 任务切换 LED 以直观显示系统状态；
**如果 LED 每 3 秒切换一次，则表示所有任务都在
按预期执行。如果 LED 指示灯每 200 毫秒切换一次，则说明 check 任务检测到
一个或多个演示任务中可能存在错误**。



**注意：**一些标准演示任务会检查自带的计时。
如果处理USB中断所花费的时间过多，
计时检查会失败（导致错误并报告给“检查”任务）。



  





---


### 构建说明


#### 构建并执行 RTOS 演示应用程序


请注意，RTOS 演示项目从 /FreeRTOS-Plus 和
/FreeRTOS/Demo/Common 目录引用常见文件。
如果其中任何一个目录被删除或移出默认位置，
则演示项目将不会执行编译操作。
1. 打开 FreeRTOS/Demo/CORTEX_A5_SAMA5D4x_EK_IAR/RTOSDemo.eww
 （从 IAR 嵌入式工作台 (EWARM) IDE 中打开）。
2. 设置 main.c 顶部的 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，
 构建简单的 blinky 演示或完整的测试和演示应用程序，
 如上所述。
3. 从 IDE 的“项目 (Project)”菜单中选择“构建全部 (Build All)”，或按下 F7 键
 构建 RTOS 演示。
4. 确保目标硬件已启动，并且已经通过其
 调试器的 J-Link USB 接口以及目标硬件的 USB-A 接口（通过 CLI 运行完整演示时）
 连接至主计算机。
5. 从 IDE 的“项目 (Project)”窗口中选择“下载并调试 (Download and Debug)”。调试会话开始前，
 已构建的可执行文件将下载至 ARM Cortex-A5 RAM
 。



  





---


### RTOS 配置和使用详情


#### FreeRTOS ARM Cortex-A 移植特定配置


请注意！

SAMA5D4 使用专有的 Atmel 中断控制器，不使用 ARM 自带的
通用中断控制器 (GIC)。还有专门的网页
介绍在两个场景中使用 RTOS 的方法。使用 SAMA5D4 时
请参阅
说明[
如何在 ARM Cortex-A 嵌入式处理器（不含
 ARM GIC](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)）上使用 RTOS 的网页。


此演示的特定配置内容位于
FreeRTOS/Demo/CORTEX_A5_SAMA5D4x_EK_IAR/FreeRTOSConfig.h 标头
文件。


  



#### FreeRTOS使用的资源


RTOS演示配置为从 PIT（周期中断控制器）中生成 RTOS
滴答中断。RTOS 使用的其他资源
已记录在
[
有关在未集成 
ARM 通用中断控制器](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md)的 ARM Cortex-A 嵌入式处理器上使用 RTOS 的说明页面上（如前所述）。

  


#### 内存分配


Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-A 演示应用程序项目中，用于
为 RTOS 内核分配所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分获取
以获取完整信息。

  


#### 其他事项



请注意，vPortEndScheduler() 尚未实现。



  

  

  

  

  










