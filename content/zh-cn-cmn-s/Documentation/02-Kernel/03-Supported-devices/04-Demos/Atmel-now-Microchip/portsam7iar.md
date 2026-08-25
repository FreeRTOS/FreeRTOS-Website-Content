---
title: "Atmel AT91SAM7S64 (AT91 ARM7) 移植演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



适用于 IAR 开发工具的 Atmel AT91SAM7S64 (AT91 ARM7) 移植

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  




|  |
| --- |
| <br />![SAM7S64-EK.gif](/media/2018/SAM7S64-EK.gif)<br /> |
|


*Studio Cadrage*  



此 Atmel SAM7 ARM7 移植是在 [AT91SAM7S-EK 开发板/原型板](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=AT91SAM7X-EK)上开发的，
该开发板/原型板来自 AT91SAM7S64-IAR 评估套件（如果您希望使用代替开发板，我们也提供了相关相关[说明](porting-a-freertos-demo-to-different-hardware.md)）。还有两个 FreeRTOS
[嵌入式 Web 服务器演示](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)也适用于 SAM7 系列微控制器。



AT91SAM7S64 是一款外设丰富（包括 USB 2.0 设备）、低引脚计数、基于 ARM7TDMI 的闪存微控制器。
评估套件配备一个无时限评估版 ARM [IAR 嵌入式工作台开发
工具](http://www.iar.com/ewarm)（仅限 32KB）、一个 J-Link USB JTAG 调试器接口和一条 USB 数据线（可通过此数据线为开发硬件供电），即启动开发所需的一切。



开发工具包含一个编译器、汇编器和链接器工具链，配备 IDE 以及有限
功能模拟器。



此系统的一个很好的功能是 Atmel 为大多数板载外设提供了库支持
。这大大加快了开发速度，而且到目前为止已经证明是可靠的。




此演示包含 USB HID 类的驱动程序示例（如下所述）。该
[SAM7X lwIP 嵌入式 Web 服务器演示](portsam7xlwIP.md)包括 USB CDC 类驱动程序示例
。



**注意：**如果项目构建失败，则可能是使用的 IAR
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。








---


### *重要提示！关于使用 Atmel ARM7 RTOS 移植的注意事项*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织



FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

IAR ARM7 移植包含 THUMB 模式示例项目。工作区 *rtosdemo.eww* 位于
Demo/ARM7_AtmelSAM7S64_IAR 目录下，应从嵌入式工作台 IDE 内部打开。



Demo/ARM7_AtmelSAM7S64_IAR/SrcIAR 和 Demo/ARM7_AtmelSAM7S64_IAR/resource 目录
包含 Atmel 库和构建环境的支持文件。



Demo/ARM7_AtmelSAM7S64_IAR/serial 和 Demo/ARM7_AtmelSAM7S64_IAR/USB 目录分别包含
中断驱动的串行端口驱动程序和 USB 驱动程序示例。




---


### 演示应用程序



FreeRTOS 源代码下载包含用于 SAM7 RTOS 移植的完全抢占式多任务演示应用程序。

### 演示应用程序硬件设置



演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3
连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。



  



### 构建用于调试的演示应用程序



目前提供两种项目配置。"Flash Debug" 不使用任何优化，可以与 J-Link JTAG 调试接口
一起使用。"Flash Bin" 使用完全优化。

只需在 IAR 嵌入式工作台 IDE 中打开 rtosdemo 工作区文件，确保选择 *flash debug* 配置
（见下图） ，然后在 IDE "Project" 菜单中选择 "Built Target"。
  




![ewprojselect.jpg](/media/2018/ewprojselect.jpg)
  

选择 *flash debug* 配置


  



### 运行演示应用程序



IAR 移植无法使用 IAR 模拟器执行，因此必须在目标硬件上执行。



1. 确保 J-Link JTAG 调试接口已连接，并且原型板已经上电。
2. 在 IDE 的 "Project" 菜单中选择 "Debug"。
3. 嵌入式微控制器闪存将自动使用演示应用程序进行编程，并且调试器
 会在重置的矢量处（地址 0）中断。在 IDE 的 "Debug" 菜单中选择 "Go"，
 以开始执行应用程序。



  



### 功能



演示应用程序创建了 26 个任务，主要包含标准演示应用程序任务
 （请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息）。
以及一个 USB 演示任务。



如果演示应用程序正确执行，其表现如下：


* 原型板将向 USB 主机自我标识为简单的 3 轴操纵杆，
 然后定期传输更新的坐标值。下一小节将对此进行详细描述。
* LED PA.0、PA.1 和 PA.2 由 "flash" 任务控制。每个 LED 将以恒定频率闪烁，LED PA.0
 速度最快， LED PA.2 速度最慢。
* 并非所有任务都会更新 LED，所以没有可见的指示来表明它们正常运行。
 因此，系统创建了一个检查任务，用于确保所有其他任务中没有检测到任何错误。 

 LED PA.3 由检查任务控制。每 3 秒，检查任务就会将系统中的所有任务检查一次，
 以确保任务执行无误。接着，它将切换 LED PA.3 的状态。如果 LED PA.3 每三秒切换一次，
 那么就说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）移除来检查此机制，
 这样做会故意生成一个错误。


### USB 功能[这只能从 Win2K 主机进行测试]





USB 任务演模拟了简单的三轴操纵杆。要检查 USB 功能，请执行以下步骤：
1. 将 USB 线连接到原型板与 USB 主机之间将开始 USB 枚举过程，
 然后显示以下“找到新硬件”对话框。


![](/media/2018/foundnew.gif)  
“找到新硬件”对话框  


 如果这是要安装到您 PC 的第一个“人机接口设备”，还可能会显示第二个对话框。

 如果从 USB 端口为原型板供电，则枚举过程将在
 演示应用程序开始执行时立即开始。
2. 如果系统提示，请重置您的电脑。

 如果正在从调试器中执行 FreeRTOS 演示应用程序，那么
 在重置电脑之前，拔掉 USB 线。现在微控制器的闪存已经被编程，您也可以移除 JTAG
 调试器接口——旦重新连接 USB 线，程序将开始执行。
3. 连接 USB 线后，从 Windows 控制面板打开 "Gaming Options" （有时列为 "Game Controllers"）文件夹。  

  
![](/media/2018/gamingopt.gif)  
选择 "Gaming Options" 文件夹
 这将打开 "Gaming Options" 对话框，其中应列出 FreeRTOS 操纵杆，状态
 显示为 "OK"。  

  
![](/media/2018/gamingopt2.gif)  
Gaming Options 下列出的 FreeRTOS 操纵杆
4. 从列表中选择 FreeRTOS 操纵杆（上图显示它是列表中唯一的控制器）。
 单击属性，查看从 USB 演示任务传输的数据。X 轴和 Y 轴应该在正方形中移动，
 Z 轴只是不断从最大值移动到最小值。  

![](/media/2018/properties.gif)  
三个轴的数据显示
5. FreeRTOS 操纵杆设备可以从 Windows 设备管理器卸载，它将被列为
 “人机接口设备” 下的 “HID 兼容游戏控制器”。  

![](/media/2018/devicemanager.gif)  
卸载 FreeRTOS 操纵杆




---


### 配置和用法详情


### RTOS 移植特定配置



此移植的特定配置项目位于 Demo/ARM7_AT91SAM7S64_IAR/FreeRTOSConfig.h。可以编辑此文件中定义的常量，
确保适配您的应用程序。特别是，configTICK_RATE_HZ 定义用于
设置 RTOS tick 的频率。所提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但该值
高于大多数应用程序要求的频率。降低该值将会提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。




请注意，vPortEndScheduler() 尚未实现。



  


### 中断服务程序



不会引起上下文切换的中断服务程序没有特殊要求，可以按照
正常的 IAR 语法写入。
例如：

```c

    static __arm __irq void vAnISR( void )
    {
        /* ISR C code goes here. */

        /* End the interrupt in the AIC. */
        AT91C_BASE_AIC->AIC_EOICR = 0;
    }

```



通常情况下，您需要中断服务程序来引起上下文切换。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。由于 IAR 内联汇编器的限制，
中断服务程序必须包含汇编文件包装器。






#### 具备上下文切换功能的 ISR 示例



可按照下列模板，在任何源文件中用 C 语言编写 ISR 主体部分。这只是一个普通的
ARM 模式函数，其结尾处包括对 portEND_SWITCHING_ISR() 的调用。


```c

    /* For simplicity the C function should operate in ARM mode.
       Note that the __irq modifier is NOT used. */

    __arm void vASwitchingISR( void )
    {
        char cContextSwitchRequired;

        /* Write the ISR body here as per normal.

        A boolean is used to say whether a context switch is required.
        In this example assume we posted onto a queue and this caused a
        task to be woken. */

        cContextSwitchRequired = pdTRUE;

        /* Immediately before the end of the ISR call the
        portEND_SWITCHING_ISR() macro. */

        portEND_SWITCHING_ISR( ( cContextSwitchRequired ) );

        /* End the interrupt in the AIC. */
        AT91C_BASE_AIC->AIC_EOICR = 0;
    }

```


请参阅 Demo/ARM7_AtemlSAM7S64_IAR/serial/serial.c 中定义的函数 **vSerialISR()** 以了解完整示例。


ISR 的入口点必须写入汇编文件中。这只是
在调用 portSAVE_CONTEXT() 和 portRESTORE_CONTEXT() 宏的之间调用一次 C 函数，具体操作模板如下所示：


```c

        EXTERN vASwitchingISR
        PUBLIC vASwitchingISREntry

    /* This header defines the save/restore macros. */
    #include "ISR_Support.h"

    vASwitchingISREntry:

        portSAVE_CONTEXT      ; Call portSAVE_CONTEXT macro first
        bl  vASwitchingISR    ; Then call the function written in the C file.
        portRESTORE_CONTEXT   ; Call portRESTORE_CONTEXT last.

        END

```


请参阅文件 Demo/ARM7_AtemlSAM7S64_IAR/serial/serialIAR.S79 以了解完整示例。




  


### 使用 AT91SAM7S-EK 以外的原型板


文件 Demo/ARM7_AT91SAM7S64_IAR/FreeRTOSConfig.h 包含 “board.h” 头文件。这定义了一些
只与 Atmel 评估板相关的常量。这些常量与任何其他目标硬件一起使用时，应更换或更新。

  


### 使用 AT91SAM7S64 以外的部件


AT91SAM7S128 和 AT91SAM7S256 是 AT91SAM7S64 的较大内存版本，应该可以直接替代。引脚数较少的
AT91SAM7S32 也是兼容的，但不包括 USB 设备外设。

SAM7 系列使用标准的 ARM7 核心，因此主要的实时内核组件
能在所有 ARM7 设备上移植，但需考虑外设设置和内存要求。
应考虑的事项：



* prvSetupTimerInterrupt() in Source/portable/IAR/AtmelSAM7S64/port.c 配置 ATM91SAM7S64 PIT 以生成 RTOS tick。
* 移植、内存访问和系统时钟配置由 Demo/ARM7_AtmelSAM7S64_IAR/main.c 中的 prvSetupHardware() 执行。
* 中断服务程序设置和管理假设存在高级中断控制器。
* 串口驱动程序。
* 文件 board.h（等等）提供了寄存器位置定义，该文件位于 Demo/ARM7_AT91SAM7S64_IAR/FreeRTOSConfig.h 的顶部。
* 启动代码、内存映射和矢量表设置包含在 Demo/ARM7_AtemlSAM7S64_IAR/SrcIAR/CStartup.s79 中。
* RAM 大小：参见下面的内存分配部分。


### 在抢占式和协同式 RTOS 内核之间切换


将 Demo/ARM7_AT91SAM7S64_IAR/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，
设置为 0 可使用协同式调度。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
提供的演示应用程序项目文件为基础构建您的应用程序，如[源组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节所示。

  


### 执行上下文



RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意：
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。






中断服务程序总是在 ARM 模式下运行。所有其他代码都在 THUMB 模式下执行。



Demo/ARM7_AtemlSAM7S64_IAR/SrcIAR/CStartup.s79 不为所有操作模式配置堆栈。



SWI 指令由实时内核使用，因此不能由应用程序代码使用。



“系统中断”可以从多个来源生成。目前假设所有系统中断都源自
PIT（周期中断定时器）。使用任何其他系统中断都需要一些包装代码来确定
中断起点。



  


### 内存分配


Source/Portable/MemMang/heap_1.c 包含在 ARM7 演示应用程序项目中，用来为实时内核分配
所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


### 串行端口驱动器



此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。特别是，它们不使用外围数据控制器。

  



### USB 驱动程序


USB 驱动程序仅用于演示。虽然起作用，但它是最小实现，
并不完全符合 USB 设备的要求。


  



### IAR 编译器注意事项



构建 FreeRTOS 源代码必须使用大量不同的编译器。IAR 编译器拥有特别强大的
(pedantic) 源检查功能，在编译 FreeRTOS 源代码时会生成几个警告。

遗憾的是，仅仅修改源代码无法修复这些警告，因为这些警告主要与良性代码有关，
添加这些良性代码是为了修复其他编译器生成的警告（主要与类型转换有关）。
因此，项目文件中已经禁用部分警告。

   

  

  

  

  












