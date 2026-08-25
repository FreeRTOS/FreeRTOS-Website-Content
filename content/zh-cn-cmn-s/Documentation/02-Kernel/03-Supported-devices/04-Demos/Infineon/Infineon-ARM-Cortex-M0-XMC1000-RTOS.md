---
title: "Infineon XMC1000 ARM Cortex-M0 演示 支持 IAR、Keil 和 GCC 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[XMC1000](http://www.infinion.com/xmc1000/)]
[[Cortex-M0](http://www.arm.com/products/processors/cortex-m/cortex-m0.php)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ARM Cortex-M0 RTOS](/media/2018/XMC1300.jpg)

**XMC1300 启动套件** 

## 简介

本页介绍的演示应用程序适用于 Infineon XMC1000 系列 ARM Cortex-M0
微控制器。

已针对以下 ARM Cortex-M0 编译器提供预配置的项目：

* [IAR](http://www.iar.com/ewarm)
* [GCC](https://launchpad.net/gcc-arm-embedded)（使用 
  [Atollic TrueSTUDIO](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html) Eclipse 项目）
* [ARM Keil](http://www.keil.com/arm/mdk.asp)

每个项目包含三个构建配置，
分别对应以下三个 XMC1000 评估板：

* [Boot Kit XMC1100](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)
* [Boot Kit XMC1200](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)
* [Boot Kit XMC1300](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)

每个构建配置均可以使用 #define 进一步配置，
来创建简单的 blinky 风格应用程序，或更全面的测试和演示
应用程序。

![与 IAR 编译器一起使用的 FreeRTOS 内核感知调试器](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)   
*IAR IDE 附带的 FreeRTOS 状态查看器插件截图*

**注意：**如果无法构建 IAR 项目，可能是使用的 IAR
Embedded Workbench 版本过低。如果是这种情况，
则项目文件也很可能（在无提示的情况下）已经损坏，即使已更新 EWARM 版本，
也需要在主 FreeRTOS zip 文件下载中将项目文件恢复到初始状态，
才能构建项目。

---

### *重要！使用 XMC1000 ARM Cortex-M0 演示的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

## 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，
因此包含的文件比 XMC1000 演示所需的文件多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
和新项目创建的信息。

支持的所有三个编译器的项目文件位于
FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC 目录。

* IAR Embedded Workbench 项目名为 RTOSDemo.eww。
* Keil 项目名为 RTOSDemo.uvproj。
* Atollic TrueSTUDIO 项目采用常见的 Eclipse 项目名称 .project 。

---

## 构建和运行 ARM CORTEX-M0 RTOS 应用程序

RTOS 演示项目可配置为
运行简单的 "blinky" 风格的项目，或者更全面的测试和演示应用程序。main.c 顶部的
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
设置用于在两者之间进行选择。

将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
可创建基本的 Blinky 演示。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
可创建更全面的测试和演示应用程序。在构建项目之前，
请确定已设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 常量。

演示使用了内置在 Boot 套件 PCB 上的 LED ，
因此不需要任何硬件设置。任何跳线和开关都应保持在
默认位置。

以下各小节介绍了如何使用这三种
支持的 ARM Cortex-M0 编译器和工具链。

1. [使用 IAR Embedded Workbench 构建](#使用-iar-embedded-workbench-构建)
2. [使用 ARM Keil 构建](#使用-arm-keil-构建)
3. [使用 ARM GCC 在 Atollic TrueSTUDIO Eclipse IDE 构建](#使用-arm-gcc-在-atollic-truestudio-eclipse-ide-构建)


#### 使用 IAR Embedded Workbench 构建

1. 打开 FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC/RTOSDemo.eww
   （在 IAR Embedded Workbench IDE 中）。
2. 为目标硬件的构建配置设置正确选项。
   为 XMC1100、XMC1200 和 XMC1300 启动套件提供构建配置
   。使用 EWARM IDE 工作区窗口顶部的下拉列表
   设置活动构建配置。
3. 从 IAR Embedded Workbench 的 "Project" 菜单中选择 "Rebuild All"（或按 F7）以构建
   演示项目。
4. 通过 USB 连接线将选定的 XMC1000 启动套件的 USB 端口与主机连接。
5. 在 IAR Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"，
   对微控制器闪存进行编程并启动调试会话
   。


#### 使用 ARM Keil 构建

1. 在 Keil IDE 中打开 FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC/RTOSDemo.uvproj
   。
2. 为目标硬件的构建配置（在 Keil IDE 中称为*目标*）
   设置正确选项。
   为 XMC1100、XMC1200 和 XMC1300 启动套件提供构建配置
   。活动构建配置通常显示在
   IDE 菜单工具栏的下拉列表中。
3. 从 Keil 的 "Project" 菜单中选择 "Rebuild Target"（或按 F7）以构建
   演示项目。
4. 通过 USB 连接线将选定的 XMC1000 启动套件的 USB 端口与主机连接。
5. 从 Keil 的 "Project" 菜单中选择 "Start/Stop Debug Session"，
   对微控制器闪存进行编程并启动调试会话
   。


#### 使用 ARM GCC 在 Atollic TrueSTUDIO Eclipse IDE 构建

请注意， Eclipse 项目使用的文件引用与项目位置相关。
该项目或其引用的任何文件**不得改变
其在 FreeRTOS 目录结构中的默认位置**
（此目录结构在 FreeRTOS 下载包解压时创建）。

1. 启动 Eclipse IDE ，根据提示创建创建一个新的或选择一个现有的
   工作区。

2. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
   如下对话框。选择 "General->Existing Project into Workspace"，如下所示。

   ![将 Cortex-M0 RTOS 演示项目导入 Atollic TrueSTUDIO Eclipse IDE](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)   
   *首次点击 "Import" 时显示的对话框*

3. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC
   作为根目录。确保在 "Projects" 区域中勾选 RTOSDemo 项目，
   **并且确保未勾选 "Copy Projects Into Workspace" 复选框**，
   然后再点击 "Finish" 按钮（请参阅下图，查看正确的复选框状态）。

   ![导入 Eclipse CDT 时，选择 RTOS 源代码](/media/2018/Selecting_RTOSDemo_In_Eclipse.jpg)   
   *确保勾选 RTOSDemo，且未勾选 "Copy projects into workspace"*

4. 导入项目后，右键单击 Eclipse 项目资源管理器窗口中的项目名称，
   然后使用弹出菜单中的 "Build Configurations->Set Active" 选项，
   为目标硬件的构建配置设置正确选项。
   为 XMC1100、XMC1200 和 XMC1300 启动套件提供构建配置
   。

5. 从 Eclipse 的 "Project" 菜单中选择 "Rebuild Project" 以构建
   演示项目。

6. 通过 USB 连接线将选定的 XMC1000 启动套件的 USB 端口与主机连接。

7. 从 Eclipse 的 "Run" 菜单中选择 "Debug"，
   以进行启动配置，
   用于对微控制器闪存进行编程并启动调试会话。


## 演示应用程序功能

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，构建演示会导致 main() 调用
main_blinky()。main_blinky() 会创建一个非常简单的演示， 
如下所示。

* **main_blinky() 函数：** 

  main_blinky() 会创建一个队列和两个任务，然后启动调度器。

* **队列发送任务：** 

  队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
  prvQueueSendTask() 在一个循环中运行，
  在将值 100 发送到 main_blinky() 中创建的队列之前，
  该函数会被反复阻塞 200 毫秒。

* **队列接收任务：** 

  队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现。
  prvQueueReceiveTask() 在一个循环中运行，
  会反复尝试从 main_blinky() 中创建的队列读取数据，并在读取过程中阻塞。数据到达时，
  任务会自动解除阻塞，检查数据的值，如果该值等于
  预期的 100，则切换 LED 的状态。

  传递给队列接收函数的 "block time" 参数规定，
  此任务应当无限期地保持在“已阻塞”状态，
  直到队列上有可用数据为止。只有当
  队列发送任务写入队列时，队列接收任务才会解除“已阻塞”
  。由于队列发送任务每 200 毫秒向队列写入一次，
  队列接收任务每 200 毫秒解除一次“已阻塞”状态，
  因此 LED 每 200 毫秒切换一次。


#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，构建演示会导致 main() 调用
main_full()。main_full() 会创建更全面的测试和演示应用程序，
如下所示。

* **main_full() 函数：** 

  main_full() 会创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、 
  一些特定于应用程序的测试任务和一个定时器，然后启动调度器。

* **“寄存器测试”任务：** 

  这些任务用已知值填充寄存器，然后检查
  每个寄存器在整个任务生命周期内是否保持其预期值
  。每个任务使用一组不同的值。寄存器测试任务以非常低的优先级执行，
  因此经常被抢占。寄存器中包含意外值
  表示上下文切换机制中存在错误
  。

* **“中断信号量获取”任务** 

  该任务仅阻塞在
  由滴答钩子函数（在 main.c 中定义）释放的信号量上。每次
  收到信号量时，它会切换 LED 4 的状态。信号量
  每隔 50 毫秒释放一次，因此 LED 4 每 50 毫秒切换一次状态。

* **“检查”软件定时器：** 

  检查软件定时器的周期最初设置为三秒
  。其回调函数检查所有标准演示任务和
  寄存器检查任务是否仍在执行，
  且执行时是否报告任何错误。如果检查定时器回调发现
  任务已停顿，或报告了错误，便会将
  检查定时器的周期从最初的三秒钟更改为仅 200 毫秒。回调函数还会在每次调用时
  切换 LED 5 的状态。这可直观体现
  系统状态：**如果 LED 5 每三秒切换一次，
  则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，则表示
  已发现至少一个任务存在问题**。

---

## RTOS 配置和使用详情

### 中断服务程序

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

请注意，FreeRTOSConfig.h 中包含以下行，以将 FreeRTOS
中断处理程序函数名称映射到 CMSIS 中断处理程序函数名称上。
这使编译器工具供应商提供的链接器脚本可
在无需修改的情况下使用。

```c
	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler

```


### RTOS 移植特定配置

这些演示的特定配置项位于 FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC/FreeRTOSConfig.h 中。 
可以编辑 FreeRTOSConfig.h 中定义的常量，以满足您的应用程序的需求。尤其是以下常量：

* **configTICK_RATE_HZ**

  此常量设置了 RTOS 滴答中断的频率。提供的 500Hz 值可用于
  测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
  降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
对处理器而言最有效的数据类型。所有 ARM Cortex-M0 移植都将 BaseType_t 定义为长整型。

请注意，vPortEndScheduler() 尚未实现。


### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOS/Demo/CORTEX_M0_Infineon_XMC1000_IAR_Keil_GCC/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置 为 1， 
即可使用抢占式内核，设置为 0 即可使用协同式内核。


### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M0 演示应用程序项目中，用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，以了解全部信息。


