---
title: "Atmel AVR (MegaAVR) / WinAVR 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel AVR (MegaAVR) / WinAVR 移植

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]



![STK500.jpg](/media/2018/STK500.jpg)  




ATmega323/ATmega32 和 ATmega128 目前有两种移植：一种使用 AVR 的 [IAR Embedded WorkbenchTM](https://www.iar.com/)，另一种使用 [WinAVR (GCC)](http://winavr.sourceforge.net/)。此页面仅提供 WinAVR 移植的相关信息。



此外还有一些移植可用于 [ATmega320x/480x](microchip-atmega-0-port-for-xc8-avr-gcc-and-iar-ewavr) 和 [AVR Dx](microchip-avr-dx-port-for-xc8-avr-gcc-and-iar-ewavr)，适用于 WINAVR (AVR GCC)、MPLAB XC8 和 AVR 的 IAR 嵌入式工作台。 




AVR WinAVR 演示应用程序配置为在 Atmel
[STK500](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500) 原型板上 
使用运行频率为 8MHz 的 AVR ATMega323 嵌入式处理器运行（如需使用其他开发板，请参阅相关[说明](porting-a-freertos-demo-to-different-hardware.md) )。如果
使用 ATMega32，频率可以提高到 16 MHz。此移植还与 ATMega128 处理器一起使用。



ATMega323 的 2 KBytes RAM 容量足够运行 10 个实时任务，包括空闲任务。





从 V4.1.0 开始，AVR 演示应用程序演示了协程的使用。
  





---


#### 重要提示！使用 AVR/WinAVR RTOS 移植的注意事项：


*使用此移植之前，请阅读以下所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织


FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。



AVR WinAVR 演示应用程序 makefile 位于 Demo/AVR_ATMega323_WinAVR 目录下。



  





---


### 演示应用程序



FreeRTOS 源代码下载包括用于 Mega AVR GCC RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置




演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3 
连接在一起）。

为了达到最佳效果， LED 应连接到标准 PC 并行端口上的八条数据线。 
忽略这些 LED 不会导致 RTOS 演示应用程序 
失败，但会删除表明一切都按预期运行的一些视觉反馈。 

















STK500 原型板上必须提供以下链接才能确保演示应用程序能够运行， 
如上图所示： 


1. PORTB 到 LEDS 的链接
2. PORTD 第 0 位和第 1 位到 RS 的链接
3. SPROG3 到 ISP6PIN 的链接（对 AVR ATMega323 进行编程的正确链接）



演示应用程序包含通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3 
连接在一起）。


  



#### 构建 RTOS 演示应用程序



FreeRTOS V3.0.0 已将以前用于构建演示应用程序的批处理文件替换为单个 makefile。这
得益于 WinAVR 后期版本中 ELF 和 COFF 格式支持得到了改进。

要生成演示应用程序：


1. 确保 WinAVR 已正确安装，并可从您的 PATH 环境访问。
2. 打开命令提示符并导航至 Demo/AVR_ATMega323_WinAVR 目录。
3. 键入 "make" 以构建项目。构建项目时不应报错或出现警告。
4. 要强制完全重建，请键入 "make clean"。
5. 可在 makefile 中调整优化级别 (option -O) 和调试级别 (option -g)
 以满足您的应用程序要求。



构建过程将生成一个名为 RTOSDemo.elf 的文件，适合在
免费的 Atmel AVR Studio IDE 中执行和调试，以及一个名为 RTOSDemo.hex 的文件，适合烧录到处理器中。

生成用于调试和模拟的文件时，确保在 makefile 中使用 -g 选项。



  



#### 功能


RTOS 演示应用程序创建 10 个标准演示任务。
 1. LED 0-2 由标准的 ‘flash’ 协程控制，以固定的频率闪烁。 
 每个 LED 都由单独的任务控制闪烁。
2. LED 4 和 5 由标准的 'comtest' 任务控制。每次传输 RS232 字符时， 
 LED 4 都会切换。每次收到并验证 RS232 字符时，
 LED 5 都会切换。
3. 并非所有任务都会更新 LED 的状态，所以没有可见的指示表明它们运行正常。 
 因此系统创建了一个 ‘Check’ 任务，用于确保在任何其他任务中 
 均未检测到错误。 
 LED 7 由 'check' 任务控制。如果任何其他实时任务中都没有检测到错误，
 LED 7 将每隔几秒钟闪烁一次。如果在任何其他任务中检测到错误，则 LED 7 将
 停止闪烁。



请参阅[标准演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解
演示应用程序任务的全部详情。 



  





---


### 配置和使用详情


#### RTOS 移植特定配置



此移植的特定配置项位于 Demo/AVR_ATMega323_WinAVR/FreeRTOSConfig.h。 
您可以编辑此文件中定义的常量，确保适配您的应用程序。特别是 
用于设置 RTOS tick 的频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于 
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将有助于提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。此移植将
BaseType_t 定义为 char 类型。


  



#### 使用 AVR ATMega323 以外的微控制器


1. 更改 makefile 顶部的 MCU 定义。
2. 在 Demo/AVR_ATMega323_WinAVR/FreeRTOSConfig.h 中设置正确的时钟频率
3. 确保设置后的 configTOTAL_HEAP_SIZE 定义能够匹配可用的 RAM。
4. 滴答 ISR 由定时器 1 上的比较匹配生成。所有 AVR 设备上的定时器配置并不相同
 。检查 Source/portable/GCC/ATMega323/port.c 中的函数 prvSetupTimerInterrupt()，以查看 
 您选择的设备是否需要任何修改。


无论使用哪个零件，确保熔断 MCU 保险丝以提供正确的时钟频率（这可以从 
AVR Studio 开发工具完成）。  



#### 在抢占式和协同式 RTOS 内核之间切换


将 Demo/AVR_ATMega323_WinAVR/FreeRTOSConfig.h 中的定义configUSE_PREEMPTION 设置为 1  
可使用抢占式调度，设置为 0 可使用协同式调度。


  



#### 内存管理


MegaAVR 演示应用程序 makefile 中包含 Source/Portable/MemMang/heap_1.c，用于提供 
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节 
获取完整信息。

  



#### 开发工具选项



与所有的移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序 makefile 构建应用程序。


  



#### RTOS 演示应用程序串行端口驱动程序


演示应用程序中包含的串行端口驱动程序使用 AVR ATMega323 手册中详细说明的计算来设置 
波特率寄存器。在某些波特率下，我发现有必要稍微调整已计算的设置。我怀疑这是因为 
安装在原型板中安装的 8MHz 晶体不准确，以及波特计算中的四舍五入误差。



此外还应注意，编写串行驱动程序是为了测试部分 RTOS 内核功能，并不是
用于表示优化过的解决方案。

  



#### Linux 用户注意事项：



我只测试了 Win2K 主机的 makefile，但希望该文件也能与 GCC 的 Linux 版本兼容。

   

  

  

  

  












