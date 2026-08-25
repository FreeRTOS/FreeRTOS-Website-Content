---
title: "Atmel AT91FR40008 (ARM7) RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel AT91FR40008 (ARM7) RTOS 移植

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


  


![](/media/2018/embestboard.jpg)




该移植由 John Feller 在 Embest 的 [ATEB40X 原型板](http://www.embedinfo.com/English/Product/ateb40x.asp)上开发。
ATEB40X 是 Atmel AT91EB40 的克隆版，使用开源的 GCC 开发工具（如果您想使用其他开发板，可以参考[说明](porting-a-freertos-demo-to-different-hardware.md)）。



开发板自带并行端口 JTAG 接口和闪存编程实用程序。





---


### 重要提示！使用 [AT91R40008](http://www.microchip.com/wwwproducts/en/AT91R40008) RTOS 移植的注意事项


*使用此 RTOS 移植前,请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织



FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，获取
下载文件的描述和有关创建新项目的信息。

AT91R40008 GCC 演示应用程序的生成文件位于 FreeRTOS/Demo/ARM7_AT91FR40008_GCC 目录。



FreeRTOS/Demo/ARM7_AT91FR40008_GCC/Serial 目录中包含一个中断驱动的串行端口驱动程序示例。








---


### 演示应用程序



FreeRTOS 源代码下载文件包括 AT91 GCC RTOS 移植的完全抢占式多任务演示应用程序。

### ARM、THUMB、ROM 和 RAM 版本



提供以下批处理文件来构建演示应用程序。批处理文件
先调用 make，然后再为相关版本设置必要的环境变量。


* ROM_ARM.bat：创建适合闪存编程的 ARM 模式发布版本。
* RAM_ARM.bat：创建适合在 RAM 执行的 ARM 模式调试版本。
* ROM_THUMB.bat：创建适合闪存编程的 THUMB 模式发布版本。
* RAM_THUMB.bat：创建适合在 RAM 执行的 THUMB 模式调试版本。


批处理文件位于 Demo/ARM7_AT91FR40008_GCC 目录。在批处理文件间切换， 
需要完全重建。可以 'touch'（更新文件存取时间）生成文件，强制进行完全重建。


  


### RTOS 演示应用程序硬件设置


演示应用程序包括 ComTest 任务，其中一个任务会向另一个任务传输 RS232 字符。为使该实时任务正确运行，
必须将环回连接器安装到 Embest 原型板的 RS232 端口 0 
（9 路连接器上的引脚 2 和 3 必须连接在一起）。 

演示应用程序使用原型板中内置的 LED，因此不需要进一步设置硬件。



  


### 构建和执行 RTOS 演示应用程序 - 单独运行于闪存




RTOS 演示应用程序在闪存和 RAM都能执行。本节介绍如何创建
发布版本并将其写入 AT91FR40008 闪存。假设 [GNUARM 和 UNXUTILS 开发工具](#win32-gnu-开发工具) 
已正确安装并包含在 PATH 中（以便在 Windows DOS 提示下使用）。


*要构建应用程序*：




1. 打开 DOS 提示，并转到 Demo/ARM7_AT91FR40008_GCC 目录。
2. 输入 "rom_arm"（或 "rom_thumb"），执行 rom_arm.bat 批处理文件。批处理文件会为发布版本设置必要的环境变量，然后
 调用 *make*。构建应该成功完成，没有错误或警告。


*将 RTOS 演示下载到闪存*：




1. 连接主机和目标硬件的并行端口 JTAG 接口。
2. 打开 Embest 闪存编程实用程序。
3. 在闪存编程实用程序中，打开 ATEB40x.cfg 配置文件。这将为目标板设置所有
 必要的闪存参数。
4. 继续在闪存编程实用程序中，将待编程的文件设置为 Demo/ARM7_AT91FR40008/rtosdemo.hex。
 它是上述构建过程输出的十六进制文件。


![](/media/2018/embestselectfile.gif)  
选择要下载的文件
5. 点击 "Erase" 按钮擦除闪存内容，然后点击 "Program" 对闪存进行编程。


*执行演示应用程序*：


关闭原型板电源，移除 JTAG 接口，然后重新接通电源。演示应用程序将开始 
执行。



  


### 构建和执行 RTOS 演示应用程序 - 在 RAM 中调试



移植的作者还测试并提供了用于 RAM 执行的链接器脚本。

请参阅 [LPC2106 ARM7 GCC](portlpc2106.md) 移植 
文档页面的对应部分，了解 GCC 调试工具的使用详情。





### 功能



演示应用程序创建所有标准最小演示应用程序实时任务（请参阅 
 [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分，了解各个任务的详细信息）。



如果演示应用程序正确执行，其表现如下：


* LED D3、D4 和 D5 由 "flash" 任务控制。每个 LED 都将以恒定频率闪烁，LED D3
 频率最高，LED D5 频率最低。
* 安装回环连接器后，ComTest Rx 任务会接收 ComTest Tx 任务传输的每个字符
 。每传输一个字符都会切换 LED D8 的状态，每正确接收一个字符都会切换 LED D7 的状态
 。只有接收到的字符与 ComTest Rx 任务预期接收到的字符一致时，LED D7 才会切换状态。
* 并非所有任务都会更新 LED 状态，所以没有可见的指示来表明它们运行正常。 
 因此，系统创建了一个检查 (Check) 任务，用于确保所有其他任务中没有检测到任何错误。 

 LED D10 由 "Check" 任务控制。每隔三 
 “检查”任务就会检查一次系统中的所有任务，以确保任务均在正确执行，没有错误，它 
 随后切换 LED D10 的状态。如果 LED D10 每三秒切换一次，则表示从未检测到错误。 
 如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）移除来检查此机制，
 因为这样做是在故意制造一个错误。


### 配置和用法详情


### Win32 GNU 开发工具



预构建的 GNU ARM7 开发工具可以从多个位置获取。
我在 Windows 2000 主机上使用从 [http://www.gnuarm.com](http://www.gnuarm.com/) 获取的开发工具。二进制 
发行版包括便捷安装程序。安装程序会安装所需的一切。一些 GNU 开发工具 
的发行版需要单独安装 Cygwin，相比之下不太方便。

此外，还需要 *GNU make* 兼容实用程序，我使用的是 [UNXUTILS](http://unxutils.sourceforge.net/) 版本。 





  


### RTOS 移植特定配置


此移植的特定配置项目位于 Source/Demo/ARM7_AT91FR40008_GCC/FreeRTOSConfig.h。可以编辑此文件中定义的常量
编辑此文件中定义的常量。特别是，可通过定义 configTICK_RATE_HZ 来设置
RTOS 滴答的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。




请注意，vPortEndScheduler() 尚未实现。





  


### 中断服务程序



不会引起上下文切换的中断服务程序没有特殊要求，可以正常编写。例如
：

```c

    void vASimpleISR( void ) __attribute__((interrupt("IRQ")));

    void vASimpleISR( void )
    {
        /* ISR code goes here. */
    }

```


**注意：**在 ISR 内强制切换上下文的方法从 FreeRTOS V4.5.0 开始已发生更改。很遗憾，新方法
使用不同的语法，但不再依赖于使用的编译器的版本、命令行开关或优化级别。
因此改用这里描述的方法，今后应该无需再做任何修改。



此处的示例假设中断处理程序被直接矢量化，也就是说，没有所有中断通用的入口代码
。一些其他 FreeRTOS 演示应用程序被配置为使用通用入口，作为此方法的替代方法。



编写可以引起上下文切换的中断服务程序：


1. 编写处理程序函数。该函数进行实际的 ISR 处理。处理程序函数是一个标准 C 函数，没有
特殊要求。
2. 编写包装函数。该函数是 ISR 入口，必须使用“裸”属性声明。包装函数
是必须设置为中断处理程序的函数。该函数必须在 portSAVE_CONTEXT()
和 portRESTORE_CONTEXT() 调用之间调用实际的处理程序函数。与所有 ISR 函数一样，包装器必须编译为 ARM 代码（而不是 THUMB 代码）。
3. 在 ISR 内切换上下文意味着 ISR 完成时执行的任务不一定
是中断发生时执行的任务。可以通过调用 portYIELD_FROM_ISR() 来进行这种上下文切换。



例如：

```c

    /* Declare the wrapper function using the naked attribute.*/
    void vASwitchCompatibleISR_Wrapper( void ) __attribute__ ((naked));

    /* Declare the handler function as an ordinary function.*/
    void vASwitchCompatibleISR_Handler( void );

    /* The handler function is just an ordinary function. */
    void vASwitchCompatibleISR_Handler( void )
    {
        long lSwitchRequired = pdFALSE;

        
        /* ISR code comes here. If the ISR wakes a task then
 lSwitchRequired should be set to 1. */


        /* If the ISR caused a task to unblock, and the priority 
 of the unblocked task is higher than the priority of the
 interrupted task then the ISR should return directly into 
 the unblocked task. portYIELD_FROM_ISR() is used for this 
 purpose. */
        if( lSwitchRequired )
        {
            portYIELD_FROM_ISR();
        }
    }

    void vASwitchCompatibleISR_Wrapper( void )
    {
        /* Save the context of the interrupted task. */
        portSAVE_CONTEXT();
        
        Call the handler function. This must be a separate 
 function unless you can guarantee that handling the 
 interrupt will never use any stack space. */
        vASwitchCompatibleISR_Handler();

        /* Restore the context of the task that is going to 
 execute next. This might not be the same as the originally 
 interrupted task.*/
        portRESTORE_CONTEXT();
    }

```

  

请参阅 Demo/ARM7_AT91FR40008_GCC/serial/serialISR.c 中定义的 vUART_ISR()，获取完整示例。

  


### 使用 AT91R40008 以外的部件


AT91R40008 使用标准的 ARM7 内核，并带有处理器特定外围设备。核心实时内核组件应该
能够在所有 ARM7 设备上移植，但需要考虑外围设备的设置和内存要求。需要考虑的事项：
* Source/portable/GCC/ARM7_AT91R40008/port.c 中的 prvSetupTimerInterrupt() 配置 AT91R40008 定时器以生成 RTOS 滴答。
* 端口、内存访问和系统时钟由 Demo/ARM7_AT91FR40008_GCC/main.c 中的 prvSetupHardware() 配置。
* 中断服务程序设置和管理假设存在中断控制器。
* 串口驱动程序。
* 文件 AT91R40008.h 提供了寄存器位置定义，该文件包含在 Demo/ARM7_AT91FR40008_GCC/FreeRTOSConfig.h 的头部。
* 启动代码、内存映射和矢量表设置包含在 Demo/ARM7_AT91FR40008_GCC/boot.s 中。
* RAM 大小：参见下面的内存分配部分。


  


### 在抢占式和协同式 RTOS 内核之间切换


将 Demo/ARM7_AT91FR40008_GCC/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度； 
设置为 0，则可使用协作式。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序生成文件构建应用程序。

  


### 执行上下文



RTOS 调度器以特权模式执行，任务以系统模式执行。



注意！： 
 启动 RTOS 调度器时（vTaskStartScheduler 被调用），处理器必须处于监管器模式 
 。FreeRTOS 下载中包含的演示应用程序，
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。




中断服务例程总是在 ARM 模式下运行。其他所有代码将运行在 ARM 或 THUMB 模式，这取决于构建。
应该注意的是，portmacro.h 中定义的一些宏只能从 ARM 模式代码调用，而且如果从 THUMB 代码
调用会导致编译时错误。


Demo/ARM7_AT91FR40008_GCC/boot.s 仅为系统/用户、IRQ 和 SWI 模式配置堆栈。


SWI 指令由实时内核使用，因此应用程序代码不能使用。



  


### 内存分配


AT91FR40008 演示应用程序生成文件包含 Source/Portable/MemMang/heap_2.c， 
以分配 RTOS 内核所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分 
以获取完整信息。



  


### 串行端口驱动器



此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。


  


### Linux 用户注意事项：



我仅使用 GNUARM 开发工具的 Win32 版本测试了生成文件。


   

  

  

  

  










