---
title: "Atmel AVR32 AT32UC3A0512 和 AT32UC3B0256 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



Atmel AVR32 AT32UC3A0512 和 AT32UC3B0256 移植

（包括 lwIP TCP/IP 示例应用程序）
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)][[嵌入式以太网示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]


  


![](/media/2018/evk1100.jpg)  
EVK1100 开发系统（未显示以太网电缆）

  


**注意：**FreeRTOS 下载中的 AVR32 移植适用于 ES 标记的芯片。请参阅
适用于最新芯片的最新移植的 [Atmel 软件框架](https://www.microchip.com/avr-support/advanced-software-framework-(asf))。



  

此页面显示了适用于 [AVR32 AT32UC3](https://www.microchip.com/wwwproducts/en/AT32UC3C1512C) 系列微控制器的FreeRTOS AVR32 UC3A 和 UC3B 移植以及演示应用程序。



提供了使用 AVR32 GCC 和
[IAR](http://www.iar.com/ewavr32)（需要 V2.21A 或更高版本）开发工具构建标准演示应用程序的说明。对于 UC3A 移植，还提供了[嵌入式 TCP/IP 示例](#lwip-嵌入式-tcpip-示例)。
TCP/IP 演示使用 [lwIP TCP/IP 堆栈](http://savannah.nongnu.org/projects/lwip/)，包括基本的 Web 和TFTP 服务器实现。



演示应用程序是在 [EVK1100](https://www.microchip.com/webdoc/evk1100/evk1100.Introduction.html) 和
[EVK1101](https://www.microchip.com/webdoc/evk1101/pr01.html) 评估板上开发，并以这些评估板为目标，分别用于 AVR32UC3A 和 AVR32UC3B 演示（如果您想使用其他开发板，可以参考[说明](porting-a-freertos-demo-to-different-hardware.md)）。



*感谢 Atmel 工程师为开发此移植做出的巨大贡献！*



还有一个单独的[移植正在开发](http://sourceforge.net/projects/ap7x-freertos/)，适用于 AVR32 AP7000 系列。







---


### 重要提示！Atmel AVR32 移植使用说明


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


本节介绍标准演示应用程序。有关 TCP/IP 演示的信息可以在[此页面底部](#lwip-嵌入式-tcpip-示例)找到。



### 源代码组织



FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。




GCC 工具的 AT32UC3A 演示 makefile 位于 FreeRTOS/Demo/AVR32_UC3/AT32UC3A/GCC 目录下。



GCC 工具的 AT32UC3B 演示 makefile 位于 FreeRTOS/Demo/AVR32_UC3/AT32UC3B/GCC 目录下。



IAR 工具的 AT32UC3A 演示项目文件名为 RTOSDemo.eww，可以
在 FreeRTOS/Demo/AVR32_UC3/AT32UC3A/IAR 目录中找到。







---


### 演示应用程序


  


### 演示应用程序硬件设置



演示应用程序包括中断驱动的 UART 测试，其中一个任务传送字符，
随后另一个任务接收此类字符。为正确操作此功能，必须将环回连接器安装到 EVK1100 开发板的 UART_0 连接器或 EVK1101 开发板的 USART1 连接器
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

演示应用程序使用 EVK1100 / EVK1101 中内置的 LED，因此不需要进一步设置硬件。



  


### 功能




main() 只需设置硬件，创建所有演示应用程序任务，
然后启动 RTOS 调度器。FreeRTOS 网站的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节介绍了
有关标准演示任务的更多信息。

除了一个标准演示应用程序任务子集， main.c 还会
定义一个“检查”任务。

检查任务每三秒钟仅执行一次，但具有
高优先级，保证能够获得处理器时间。其功能是
检查其他所有任务是否仍在运行，并且在任何时候
均没有检测到错误。此外， “检查”任务还执行内存分配，
通过反复分配和释放内存块来完成。



如果正确执行（“检查”任务没有检测到任何错误），演示应用程序的行为如下（请注意，已为 EVK1100
正确分配了 LED。并非所有 LED 都在 EVK1101 上）：



* LED1、LED2 和 LED3 由 'flash' 任务控制。各灯都将以恒定的频率闪烁，其中 LED1 最快，LED3 最慢。
* LED4 和 LED5 由标准 ComTest 任务控制。每当通过 RS232 端口传输字符时，LED4 都会切换状态。
 每当 ComTest Rx 任务通过 RS232 端口接收字符时， LED5 都会切换状态，并确认接收的字符是否符合预期。
* LED 6（红色的一半）由“检查”任务控制。切换速率为三秒表示未检测到错误。切换速率
 为 500 毫秒表示至少在一个其他任务中检测到一个错误
 [可以通过从 RS232 端口中移除环回连接器来检查此机制，此方式会故意创建错误]。
* 如果检查任务在任何其他任务或内存分配器中检测到错误，LED 6（绿色的一半）也将亮起。



此演示应用程序创建了 35 个任务。



  


### 构建和执行演示应用程序 - IAR


1. 在嵌入式工作台 IDE 中打开 FreeRTOS/Demo/AVR32_UC3/AT32UC3A/IAR/RTOSDemo.eww 项目。
2. 在 “Project” 菜单中选择 “Rebuild all”。项目构建时不应报错或出现警告。
3. 使用 Atmel [JTAG ICE mk-II](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATJTAGICE2) 将 EVK1100 开发板 JTAG 连接到您的主机 PC。
4. 为 EVK1100 通电。可以通过 USB 数据线将 EVK1100 连接到主机 PC，也可以使用 EVK1100 电源插口。使用后者时
 请小心电源极性！
5. 在 "Project" 菜单中选择 "Debug"。AVR32 闪存将写入演示应用程序，并且调试器将启动。



IAR 项目工作区分为多个单独的文件夹，以便于导航。它还包含两个配置，即调试和发布。




![](/media/2018/avr32iarproject.gif)  
AVR32 项目工作区
  


### 构建和执行演示应用程序 - GCC



为便于构建、下载和调试管理，提供了一份全面的 makefile。



#### 要构建项目：


1. 打开命令提示符（Cygwin 或 Windows）并导航到 FreeRTOS/Demo/AVR32_UC3/AT32UC3A/GCC 或 FreeRTOS/Demo/AVR32_UC3/AT32UC3B/GCC 目录
 （分别针对 UC3A 和 UC3B 演示）。
2. 输入命令 “make”。





#### 要对 AVR32 UC3A 或 AVR32 UC3B 闪存进行编程：


1. 使用 Atmel [JTAG ICE mk-II](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATJTAGICE2) 将 EVK1100 或 EVK1101 开发板 JTAG 连接到您的主机 PC。
2. 为 EVK1100 或 EVK1101 通电。可以通过 USB 数据线将 EVK1100 或 EVK1101 连接到主机 PC，也可以使用电源插口。使用后者时
 请小心电源极性！
3. 构建成功后（如上述说明），保持在同一目录中并输入 “make program”。以下是应获得的输出——


```c

$ make program

Programming MCU memory from `uc3a0512-rtosdemo.elf'.
Connected to JTAGICE mkII version 4.7, 4.20 at USB.
     Unlocking flash: ================================================== 100.0%
       Erasing flash: done
Writing 46736 bytes from uc3a0512-rtosdemo.elf to memory at 0x80000000.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Writing 2992 bytes from uc3a0512-rtosdemo.elf to memory at 0x8000b690.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Writing 4096 bytes from uc3a0512-rtosdemo.elf to memory at 0x8000c240.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Resetting CPU.

```





#### 其他命令：


在编程好闪存后，若要开始执行程序，只需输入命令 “make run”。

如果您安装了 [Doxygen](http://www.stack.nl/~dimitri/doxygen/)，则可以使用命令 “make doc” 创建 HTML 文档。



命令可以组合成一行。例如，要构建文件，
就要对闪存进行编程，然后从单行输入命令 “make program run”，开始执行程序。





#### 启动 GDB 调试器：


1. 首先必须启动 GDB 代理：



	1. 打开另一个命令提示符。
	2. 在新的命令提示窗口中，输入命令 'avr32gdbproxy -finternal@0x80000000,512Kb -a extended-remote:4242'。这会启动 avr32gdbproxy 并
	 将它连接到端口号为 “4242”，名为 “extended-remote” 的主机。
2. 返回原始命令提示符，使用上述说明构建并下载 FreeRTOS 演示。
3. 输入命令 “avr32-gdb” 以启动 GDB 客户端。
4. 接下来，使用命令 “target extended-remote:4242” 连接到 GDB 代理来启动调试会话。
5. 分别使用 UC3A 或 UC3B 的命令 “sym uc3a0512-rtosdemo.elf” 或 “sym uc3b0256-rtosdemo.elf” 加载符号表。
6. 最后，通过输入命令 “cont” 来启动程序执行。以下是示例会话的输出：


```c

$ avr32-gdb

GNU gdb 6.4.atmel.1.0.0
Copyright 2005 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "--host=i686-pc-cygwin --target=avr32".

(gdb) target extended-remote:4242
Remote debugging using :4242
0x80000000 in ?? ()

(gdb) sym uc3a0512-rtosdemo.elf
Reading symbols from /cygdrive/c/e/dev/FreeRTOS/Demo/AVR32_UC3/AT32UC3A/GCC/
                                                  uc3a0512-rtosdemo.elf...done.

(gdb) cont
Continuing.

```



请参阅 [GDB 手册](http://www.gnu.org/software/gdb/documentation/)，获取有关使用 GDB 调试器的完整信息。





---


### 配置和用法详情


  


### RTOS 移植特定配置


此端口的特定配置项目位于 FreeRTOS/Demo/AVR32_UC3/FreeRTOSConfig.h。可以编辑
此文件中定义的常量，确保适配您的应用程序。特别是：
用于设置 RTOS tick 频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将有助于提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。




请注意，vPortEndScheduler() 尚未实现。





  


### 中断服务程序



请注意，在默认情况下，AVR32 移植允许嵌套中断，在 ISR 中对 API 函数的调用必须在临界区内进行。



不会引起上下文切换的中断服务程序没有特殊要求，可以按照编译器文档编写。




如果您希望中断服务程序造成上下文切换，则需要特殊语法。以下演示适用于 GCC 编译器。请参阅文件
FreeRTOS/Demo/AVR32_UC3/serial/serial.c，了解 GCC 和 IAR 语法的示例。



要向可执行上下文切换的 ISR 写入数据，请执行以下操作：


1. 使用 “naked” 属性声明 ISR。
2. ISR 中的第一个语句必须是对 portENTER_SWITCHING_ISR() 宏的调用。这必须在声明任何本地变量之前。
3. ISR 中的最后一个语句必须是对 portEXIT_SWITCHING_ISR( bool ) 宏的调用。将布尔值传递给宏，以指示
是否需要上下文切换。

例如：


```c

    void vASwitchCompatibleISR( void ) __attribute__ ((naked));

    void vASwitchCompatibleISR( void )
    {
        /* Macro must be called first. */
        portENTER_SWITCHING_ISR();

        /* Variables declarations can come next. */
        long lSwitchRequired = 0L;


        /* ISR code comes here.  If the ISR wakes a task then
        lSwitchRequired should be set to 1. */


        /* Final statement is the closing macro. */
        portEXIT_SWITCHING_ISR( lSwitchRequired );
    }

```






  


### 在抢占式和协同式 RTOS 内核之间切换


将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

  


### 内存分配


Source/Portable/MemMang/heap_3.c 包含在 AVR32 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

  


### 串行端口驱动器



此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。



  




---


### lwIP 嵌入式 TCP/IP 示例




嵌入式以太网示例使用上述 FreeRTOS GCC 和 IAR 移植。上述标准演示的构建、下载、调试和配置说明
也与 TCP/IP 示例相关。本节仅提供 TCP/IP 示例所特有的一些其他信息。

  


### 源代码组织



嵌入式 TCP/IP 示例的 makefile/项目文件分别位于 GCC 的 FreeRTOS/Demo/lwIP_AVR32_UC3/GCC 目录下或 IAR 的 FreeRTOS/Demo/lwIP_AVR32_UC3/IAR 目录下。
makefile 提供与上述标准演示
相同的设施。

  


### TCP/IP 软件设置


演示使用的 IP 地址由文件 FreeRTOS/Demo/lwIP_AVR32_UC3Demo/conf_eth.h 中的常量 emacIPADDR0 到 emacIPADDR3 设置。
运行 Web 浏览器的计算机使用的 IP 地址必须和原型板使用的 IP 地址相兼容。可以将二者 IP 地址中的前三个八位字节
设置为相同来保证这一点。例如，如果网络浏览器计算机使用 IP 地址 192.168.100.1，则可以为原型板给定
192.168.100.2 至 192.168.100.254 范围内的任何地址（不包括网络上已存在的任何地址）。

conf_eth.h 还包含用于配置 MAC 地址、网关地址和网络掩码的常量。开发板所连接网络的 MAC 地址**必须**唯一
。





  


### 硬件设置


将 EVK1100 原型板直接使用点对点（交叉）电缆或通过使用标准以太网电缆的
集线器/路由器连接到运行 web 浏览器的计算机。原型板也可以在采用点到点连接时使用标准的以太网电缆，但我尚未测试过
此配置。

  


### 演示应用程序功能


#### LED Flash 任务


演示应用程序包括标准 flash 任务（如上文标准演示应用程序所述）。这提供了正在运行的演示的视觉反馈。

#### Web 服务器


EVK1100 将向标准 Web 浏览器提供包含 FreeRTOS 任务信息的网页。该页面将每隔几秒钟自动更新一次。
要连接到目标，请执行下列操作：

1. 在连接的计算机上打开浏览器。
2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。





![](/media/2018/enterurl.gif)  
在 Web 浏览器中输入 IP 地址  
（当然，根据您的系统，使用正确的 IP 地址）
#### TFTP 服务器


基本的 TFTP 服务器允许将单个小文件发送到演示应用程序，然后从演示应用程序中攫取。以下是 TFTP 会话示例的输出，该 TFTP 会话发送然后接收
文件 samplefile.txt 到以 IP 地址 172.25.218.100 运行的 EVK1100：


```c

    C:tftp 172.25.218.100 put samplefile.txt
    Transfer successful: 19 bytes in 1 second, 19 bytes/s

    C:>tftp 172.25.218.100 get samplefile.txt
    Transfer successful: 19 bytes in 1 second, 19 bytes/s

    C:>

```


  

  

  

  

  










