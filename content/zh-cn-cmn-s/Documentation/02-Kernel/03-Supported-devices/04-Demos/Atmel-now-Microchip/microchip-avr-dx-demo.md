---
title: "Microchip AVR Dx 移植演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

适用于 Microchip AVR Dx 移植的 FreeRTOS 演示 
使用 XC8、AVR-GCC 和 IAR EWAVR 编译器


 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


\![[TOD 描述图像]](/media/2020/Screen-Shot-2020-08-21-at-12.20.42-PM.png)

  

Microchip  AVR 微控制器有多个适用的 FreeRTOS 移植。本页描述了 AVR Dx 
系列的移植，包括 [AVR DA](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-da) 和 [AVR DB](https://www.microchip.com/wwwproducts/en/AVR128DB64) 系列。可提供适用于 Atmel AVR-GCC、XC8 和 
AVR 的 [IAR 嵌入式
 工作台](https://www.iar.com/iar-embedded-workbench/#!?architecture=AVR) (IAR EWAVR) 等编译器。


### 支持的设备


这些演示和示例是为 AVR128DA48 配置的，它有 128 KB 闪存和 16 KB SRAM， 
此内存配置对于具有大量实时任务的应用程序而言足够使用。FreeRTOS 演示的大小取决于所使用的编译器，但在 
[Full 演示](#full-演示)配置中，需要大约 15 KB 或更少的程序内存。除空闲任务外，运行 10 个实时任务， 
需要大约 2 KB 的 SRAM。因此，有足够的 SRAM 用于通信 
缓冲、高级算法和应用程序的其他 SRAM 密集型部分。


### 支持的编译器和 IDE


这些移植适用于三种不同的编译器。括号中显示了用于开发移植的版本：


* XC8 (v2.20)
* AVR-GCC（版本 3.6.2.1778）
* IAR EWAVR (7.30)


以下 IDE 版本用于移植的开发和测试：


* [Microchip MPLAB X](https://www.microchip.com/mplab/mplab-x-ide)
 （5.40，含设备包 AVR-Dx_DFP 1.2.52）


适用于 XC8 端口
* [Atmel Studio 7](https://www.microchip.com/mplab/avr-support/atmel-studio-7) 
 （7.0.2397，含设备包 AVR-Dx_DFP 1.1.45）


用于 AVR-GCC 移植和演示应用程序项目


XC8 和 AVR-GCC 编译器集成在 Microchip MPLAB X 和 Atmel Studio 7 IDE 中。


### 演示应用程序


适用于 AVR DA 微控制器的 FreeRTOS 演示应用程序（Blinky 演示、Minimal 演示、Full 演示）均面向 
[AVR128DA48 Curiosity Nano 评估套件](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151)。此等演示应用程序可以使用 MPLAB X (XC8)、Atmel Studio 
(AVR-GCC)，或 IAR EWAVR 构建。 


Atmel START 提供了更高级的应用程序示例。该示例面向以下三类板的组合： 
[Curiosity 
 Nano Base for Click 板](https://www.microchip.com/developmenttools/ProductDetails/AC164162)、[AVR128DA48 Curiosity Nano 评估套件](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151)和 
[OLED1 
 Xplained Pro 板](https://www.microchip.com/developmenttools/ProductDetails/atoled1-xpro)。


  



---


### 重要提示！使用 Microchip AVR Dx 移植的注意事项


*使用此 RTOS 移植前，请阅读下述所有要点。*


* [源代码组织](#源代码组织)
* [演示应用程序功能](#演示应用程序)
* [在 QEMU 
 仿真器中使用 Microchip AVR Dx 构建和运行 RTOS 演示应用程序](#构建-rtos-演示应用程序)
* [RTOS 配置和使用详情](#配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)




---



### 源代码组织


FreeRTOS 内核和演示的代码可从 FreeRTOS.org 上的[主下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)获取。FreeRTOS zip 文件下载内容包含所有 FreeRTOS 移植和演示应用程序的源代码——因此包含的文件比此项目所需文件多得多。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节， 
获取目录结构的描述以及有关新建 FreeRTOS 项目的信息。


AVR128DA48 演示应用程序的 MPLAB X 项目位于 `FreeRTOS/Demo/AVR_Dx_MPLAB.X` 目录下。而 
AVR128DA48 演示应用程序的 Atmel Studio 7 项目称为 `RTOSDemo.atsln`，位于 
`FreeRTOS/Demo/AVR_Dx_AtmelStudio` 目录下。


AVR128DA48 演示应用程序的 MPLAB X 项目位于 `FreeRTOS/Demo/AVR_Dx_MPLAB.X` 目录下。


AVR128DA48 演示应用程序的 Atmel Studio 7 项目名为 `RTOSDemo.atsln`，位于 
`FreeRTOS/Demo/AVR_Dx_AtmelStudio` 目录下。 


AVR128DA48 演示应用程序的 IAR EWAVR 项目名为 `RTOSDemo.eww`，位于 
`FreeRTOS/Demo/AVR_Dx_IAR` 目录下。 




---


  


### Microchip  AVR Dx 演示应用程序


### 功能



每个移植都配有三个不同的演示，可通过定义 (`#define mainSELECTED_APPLICATION`) 选择。 
此定义位于 `main.c` 文件。每个演示都自带 `main-<demo-name>.c` 文件。此结构体适用于全部 
三个 IDE（Atmel Studio 7、MPLAB X 和 IAR EWAVR）。它们都使用相同的 `FreeRTOSConfig.h` 文件， 
以容纳最全面的演示（[Full 演示](#full-演示)）。 


#### Blinky 演示


如果 `mainSELECTED_APPLICATION` 设置为 0，则 `main()` 调用 `main_blinky()`，后者创建 
一个简单的演示，如下所示：


1. `The main_blinky()` 函数创建一个队列和两个任务，然后启动 RTOS 调度器。
2. 队列发送任务通过 `main_blinky.c` 中的 `prvQueueSendTask()` 实现。此任务每 200 毫秒向队列发送一个固定 
 值 (100)。
3. 队列接收任务通过 `main_blinky.c` 中的 `prvQueueReceiveTask()` 实现。此任务 
 在队列读取时进入阻塞状态，并在每次从队列发送任务发出的消息被接收时，解除阻塞并切换 LED。队列 
 发送任务每 200 毫秒向队列发送一次消息，因此队列接收任务每 200 毫秒解除阻塞状态并切换一次 LED 
 。


#### Minimal 演示


如果 `mainSELECTED_APPLICATION` 设置为 1，则 `main()` 调用 `main_minimal()`，后者创建 
下列测试任务： 


* 整数数学测试通过 `integer.c` 中的 `vStartIntegerMathTasks()` 实现。此测试创建一个 
 任务函数，它重复执行 32 位计算，检查结果是否符合预期。
* 寄存器测试通过 `regtest.c` 中的 `vStartRegTestTasks()` 实现。此测试创建两个任务， 
 它们在所有寄存器中写入不同的值并验证内容是否在上下文切换期间被保留。
* 轮询队列测试通过 `PollQ.c` 中的 `vStartPolledQueueTasks()` 实现。此测试创建两个任务， 
 它们通过单个队列进行通信。其中一个任务作为生产者，另一个作为消费者。所有队列访问
 都不会被阻塞。
* 串行通信测试通过 `comtest.c` 中的 `vAltStartComTestTasks()` 实现。它 
 创建两个任务，它们在中断驱动程序串口上运行。为确保所有传输内容都被接收， 
 应使用环回连接器。


最后，创建通过 `vErrorChecks()` 实现的检查任务，对标准演示任务进行定期检查， 
以确保所有任务都正常运行。检查任务还会切换 LED，以提供系统状态的 
视觉反馈。如果 LED 每 3 秒切换一次，则表示检查任务未发现任何问题。如果 LED 停止切换，
则表示检查任务在至少一个任务中发现了问题。


我们提供了 Minimal 演示项目文件，目的是展示 RTOS 内核的使用， 
而不是提供一个优化的解决方案。对于 `comtest.c` 而言尤其如此，它使用了中断驱动的 UART 驱动程序示例 
(`serial.c`)。我们编写此等文件旨在强调（并因此测试）RTOS 内核实现， 
而不是提供一个优化的解决方案示例。



#### Full 演示


如果 `mainSELECTED_APPLICATION` 设置为 2，则 `main()` 调用 `main_full()` 以创建 
综合演示，用于演示和测试几个 FreeRTOS 功能，包括[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview)、 
[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)、[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)、 
[信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)、[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) 
等等。此演示创建了以下测试： 


* 通过 `semtest.c` 中的 `vStartSemaphoreTasks()` 实现的信号量测试任务创建两个任务集， 
 每个任务集包含两个任务。任务集内的任务共享一个变量，其访问由信号量保护。
* 通过 `TaskNotify.c` 文件中的 `vStartTaskNotifyTask()` 实现的直达任务通知任务 
 创建一个单独执行某些测试的任务，之后再循环操作，通过软件定时器 
 和中断来接收通知。
* 通过 `Regtest.c` 中的 `vStartRegTestTasks()` 实现的寄存器测试任务创建两个任务， 
 它们在所有寄存器中写入不同的值并验证其内容是否在上下文切换期间被保留。
* 通过 `RecMutex.c` 中的 `vStartRecursiveMutexTasks()` 实现的递归互斥锁任务 
 演示递归互斥锁的使用。此任务创建了三个访问相同递归互斥锁的任务。


然后，创建通过 `vErrorChecks()` 实现的检查任务，对标准演示任务进行定期检查， 
以确保所有任务都正常运行。检查任务还会切换 LED，以提供系统状态的视觉反馈 
。如果 LED 每 3 秒切换一次，则表示检查任务未发现任何问题。如果 LED 停止切换， 
则表示检查任务在至少一个任务中发现了问题。 


创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务集。标准演示任务供所有 
FreeRTOS 移植演示应用程序使用，不具有特定功能。它们用于演示 FreeRTOS API 的使用方法和 
RTOS 移植的测试方法。 



### 构建 RTOS 演示应用程序


#### 开发工具选项


这些演示应用程序可用于 Atmel Studio、MPLAB X 和 IAR EWAVR。这表示，共有三个编译器：AVR-GCC、XC8 和 
IAR EWAVR。从演示代码角度来看，三个演示项目都是相同的。各移植文件对于 
Atmel Studio 和 MPLAB X 的移植文件也是相同的，但 IAR EWAVR 使用了不同的移植文件。


#### 准备项目文件


开始前，我们首先通过下载（或以递归方式克隆）GitHub 存储库获取 FreeRTOS 内核和演示的代码（下载地址： 
https://github.com/FreeRTOS/FreeRTOS）。FreeRTOS 下载包含 
用于多个处理器移植和演示应用程序的源代码，但每个支持的处理器架构都需要少量 
特定于架构的 RTOS 代码。这是 RTOS 可移植层，位于 
`FreeRTOS/Source/Portable/<compiler>/<architecture>` 子目录，其中 `<compiler>` 
和 `<architecture>` 分别是用于创建移植的编译器和移植运行的架构 
。请参阅 [FreeRTOS 源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面， 
获取 FreeRTOS 目录结构的完整说明。 


注意：GCC 和 XC-8 编译器的移植文件相同，因此 MPLAB-X 项目使用了
位于 `.../Portable/GCC/AVR_AVR_Dx` 文件夹的文件。


对于 AVR Dx 设备，可在以下文件夹中找到所有必要的移植文件和演示：



![](/media/2020/Screen-Shot-2020-08-21-at-2.38.12-PM.png)
文件夹结构。



下一步是从 `FreeRTOS/Demo` 内的项目文件夹中打开应用程序。每个 
IDE/编译器的项目都链接了所有必要文件。


#### 使用 MPLAB X 和 XC8 构建


要使用 MPLAB X 编译演示项目，请按以下步骤操作：


1. 启动 MPLAB-X。
2. 从开始菜单中选择 File -> Open Project 并浏览到项目所在的文件夹：



![](/media/2020/Screen-Shot-2020-08-21-at-2.44.20-PM.png)
3. 选择并打开 "AVR_Dx_MPLAB.X"。
4. 构建项目。


#### 使用 Atmel Studio 7 和 AVR-GCC 构建


要使用 Atmel Studio 7 编译演示项目，请按以下步骤操作：


1. 启动 Atmel Studio。
2. 在工具菜单中选择 File -> Open -> Project/Solution。浏览到项目所在的文件夹：



![](/media/2020/Screen-Shot-2020-08-21-at-2.44.33-PM.png)
3. 选择 "RTOSDemo.asln" 并打开此项目。
4. 构建项目。


#### 使用 IAR EWAVR 构建


要使用 IAR EWAVR 编译演示项目，请按以下步骤操作：


1. 启动 IAR 嵌入式工作台。
2. 在菜单中选择 File -> Open Workspace 并浏览到项目位置。



![](/media/2020/Screen-Shot-2020-08-21-at-2.42.12-PM.png)
3. 选择并打开 "RTOSDemo.eww"。
4. 构建项目。



### 配置和用法详情


### RTOS 移植特定配置


FreeRTOS 演示的特定配置项目位于每个项目文件夹内的 `FreeRTOSConfig.h` 文件中。 
下文给出了几个定义示例。您可以编辑此文件中定义的所有常量，以适配特定的应用程序。 


* `#define configCPU_CLOCK_HZ`：定时器使用的微控制器时钟，用于计算通信的延迟和波特率 
 。
* `#define configTICK_RATE_HZ`：用于设置 RTOS tick 的频率。该值在所有演示中都设为 1000 Hz， 
 以测试 RTOS 内核功能。
* `#define configUSE_PREEMPTION`：在抢占式和协同式 FreeRTOS 内核之间切换。
* `#define configUSE_TIMER_INSTANCE`：此移植允许用户选择用于 RTOS tick 的定时器。 
 `FreeRTOS_Config.h` 文件详细描述了可用选项列表，支持函数/宏 
 位于 `porthardware.h` 文件。


每个移植还将 '`BaseType_t`' 类型定义为该处理器的最有效数据类型。 
AVR Dx 移植将 '`BaseType_t`' 定义为 char（8 位）： 


* `#define portBASE_TYPE char`


注意：tick 定时器选项列表包含可用于 AVR Dx 系列中较大成员的选项。请参阅 
可用选项列表中的特定设备数据表。


#### 编译器使用的内存区域


FreeRTOS 移植需要您定义编译器使用的堆和堆栈。这样做是为了容纳 
更全面的演示示例（[Full 演示](#full-演示)），但是您可以根据应用程序的实现自定义大小 
。当前移植使用以下定义（所有工具/编译器都有类似的定义）：


* `#define configTOTAL_HEAP_SIZE 0x1000`
* `#define configMINIMAL_STACK_SIZE 120`


注意：IAR 编译器需要两个堆栈（`CSTACK` 和 `RSTACK`）；`CSTACK` 
配置为 120 个字节， `RSTACK` 配置为 30 个字节。 


#### 内存分配


`Source/Portable/MemMang/heap_1.c` 包含在 AVR Dx 演示应用程序项目中，以提供 
RTOS 内核所需的内存分配。请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节 
获取完整信息。


#### 演示应用程序 USART 和移植驱动程序



`demos` 应用程序文件夹包含两个驱动程序的示例。
* USART 驱动程序包含在 `serial.c` 文件中。它是一个基于中断的驱动程序， 
 使用连接到板载调试器 USART 的 USART 实例。这样，您就可以在电脑上查看串行通信测试 
 (`ComTest`) 任务发送的消息，除板本身和 USB 电缆外，无需使用任何特殊硬件 
 。由于 
 `ComTest` 会验证发送的数据是否被正确接收，因此 USART 驱动程序启用了 RX 和 TX 信号之间的内部环回连接。
* 演示应用程序包括一个名为 `partest.c` 的文件，该文件是 MCU 的完整移植的驱动程序。 
 （该名称具有历史意义，后来失去了其含义，但它源自 'parallel port test'。）该文件包含 
 用于设置 LED、清除 LED 和切换 LED 的接口函数。在这些示例中，移植 C 被选为 
 连接板载 LED 的移植。要将演示从一个硬件平台移植到另一个硬件平台， 
 首先要让 LED 输出正常工作，因此我们选择了 LED 引脚。对于选定的硬件平台 (AVR128DA48 Curiosity 
 Nano)，由 `partest.c` 控制的其他 LED 引脚未与 LED 物理连接。


 


### 其他注意事项


无需阅读本节即可使用移植。


#### 使用其他硬件平台


之所以选择 AVR128DA48 Curiosity Nano 板是因为其功能易于使用， 
但您也可以轻松使用其他任何硬件平台。Tick 定时器的多个可用选项以及可用演示有助于 
在 AVR Dx 系列中的任何设备上开发 FreeRTOS 应用程序。


#### 使用其他 AVR Dx 设备


FreeRTOS 演示移植可在此系列中的任何设备上运行。只需在开发工具配置窗口中更改设备类型， 
然后重新编译项目即可。


#### Tick 定时器选择


所有可用的演示移植都使用 TCB0 作为默认 tick 定时器 (`#define configUSE_TIMER_INSTANCE 0`)。此定时器 
适用于所有 AVR Dx 设备。您也可以使用 `configUSE_TIMER_INSTANCE` 来选择其他定时器，如下所示（请参阅 
`FreeRTOS_Config.h` 文件了解可用选项）：


* `#define configUSE_TIMER_INSTANCE 0 - use TCB0 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 1 - use TCB1 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 2 - use TCB2 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 3 - use TCB3 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 4 - use TCB4 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 5 - use RTC as the tick timer`


#### 时钟配置


AVR Dx 移植使用片上振荡器作为主时钟。考虑到其内部架构，内部时钟只能 
使用特定的预定义值。为方便您使用 AVR Dx 平台，我们还提供了一份 
`clk_config.h` 文件。此文件包含支持的时钟配置列表、时钟初始化程序 
(`clk_init()`)，并使用 `#define configCPU_CLOCK_HZ`（在文件 `FreeRTOS_Config.h` 中） 
作为输入。


#### 串口配置


当 `mainSELECTED_APPLICATION` 设置为 1 时，项目包含一个中断驱动的驱动程序示例，用于串行通信， 
该驱动程序使用了 USART1 实例（文件 `serial.c`）。必要时，任何其他可用 USART 实例 (USART0-5) 
可直接作为替代实例使用。此外，还应配置 USART Rx 和 Tx 引脚。我们已针对当前演示 
在硬件初始化过程中完成了配置：




```c
void init_minimal( void ) 
{ 
    /* Configure UART pins: PC1 Rx, PB0 Tx */ 
    PORTC.DIR &= ~PIN0_bm; 
    PORTC.DIR |= PIN1_bm;

    ... 
} 
```

#### LED 移植配置


LED 是获取演示应用程序运行视觉反馈的最简单方法，因此很有必要尽快使用新硬件平台上的 
LED。


无论是向其中移植演示的硬件平台还是在其中开发演示的硬件平台，它们的 LED 不太可能出现在相同 IO 端口上， 
因此需要做出少许修改。


`partest.c` 文件中的函数 `vParTestInitialise()` 包含 IO 端口模式和方向 
配置。`main.c` 文件中的函数 `prvSetupHardware()` 包含额外的通用硬件配置， 
可能也需要根据所使用的移植进行修改。


对上段提到的两个函数进行必要的修改，然后编写一个简单的程序， 
以检查 LED 输出是否正常工作。


#### 使用中断


如果没有特殊要求，可以使用不用于上下文切换的中断。中断矢量的安装方法 
取决于所使用的移植和编译器。请参阅您正在使用的移植的现有演示。如果 
中断用于上下文切换，则需要对其进行特殊处理。请参阅 `serial.c` 和移植文件， 
获取用于上下文切换的中断使用示例。









