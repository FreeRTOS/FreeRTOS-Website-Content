---
title: "在 AT91SAM7X256 上使用 CrossStudio 和 GCC 的 lwIP 嵌入式 Web 服务器演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



在 AT91SAM7X256 上使用 CrossStudio 和 GCC 的 lwIP 嵌入式 Web 服务器演示

[[嵌入式以太网示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]


  




|  |
| --- |
| <br />![](/media/2018/sam7xek.gif)<br />*Studio Cadrage*<br /> |



  

本页描述了 FreeRTOS SAM7X 嵌入式以太网示例应用程序。此演示创建了一个简单的 Web 服务器，
使用：
* FreeRTOS GCC SAM7 ARM 移植。
* [Rowley CrossStudio IDE](http://www.rowley.co.uk/arm/index.htm) 以及 [CrossConnect USB JTAG 调试接口](http://www.rowley.co.uk/arm/CrossConnect.htm)。演示 
 也可以使用[标准（命令行）GCC](#使用-gcc命令行版本构建演示)构建。
* Adam Dunkels 开源 [lwIP 嵌入式 TCP/IP 堆栈](http://www.sics.se/~adam/lwip/)。
* Atmel AT91SAM7X-EK 开发板（如果您想使用其他开发板，我们也提供了相关[说明](porting-a-freertos-demo-to-different-hardware.md)）。


我们还提供了[替代项目](portsam7xiar.md)来展示 
如何通过 IAR 编译器使用更简单的 �IP TCP/IP 堆栈。

此演示：


* 完全由开源软件组成。
* 包括用于 SAM7X 集成 EMAC （以太网媒体访问控制器）外围设备的更全面的驱动程序。
* 演示 lwIP 与 FreeRTOS的集成。
* 演示创建动态数据。
* 包括一个样本中断驱动的 USB 串行 CDC 驱动程序（感谢 Scott Miller 提供
 此 FreeRTOS HID 类 USB 驱动程序改编）。



请注意，lwIP 与 FreeRTOS 分开授权。用户必须熟悉 [lwIP 许可证](http://savannah.nongnu.org/projects/lwip)。

从 FreeRTOS V4.0.3 起，该演示项目文件包含一个内核感知窗口，位于调试器中。这提供了系统中每个任务状态的有用信息，
但可能拖慢调试器的性能。关闭此窗口将提高调试操作速度。





---


### *重要提示！SAM7X Web 服务器演示使用说明*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [EMAC 和 USB 驱动程序](#emac-和-usb-驱动程序)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)
5. [使用 GCC（命令行）构建演示](#使用-gcc命令行版本构建演示)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织



FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件多于此演示使用的文件。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

LwIP CrossStudio 演示项目 *rtosdemo.hzp* 位于
Demo/lwIP_Demo_Rowley_ARM7 目录下，应从 CrossWorks IDE 内部打开。



Adam Dunkels lwIP 代码位于 Demo/lwIP_Demo_Rowley_ARM7/lwip-1.1.0 目录中。



Demo/lwIP_Demo_Rowley_ARM7/EMAC 目录包含 EMAC 驱动程序，最后，Demo/lwIP_Demo_Rowley_ARM7/USB 目录
包含 USB CDC 驱动程序源代码。







---


### 演示应用程序


### 演示应用程序设置



直接使用点对点（交叉）电缆，或使用标准以太网电缆通过集线器或交换机，
将所选开发板连接到运行 Web 浏览器的计算机上。点对点连接时，原型板应该也允许使用标准以太网电缆， 
但我尚未测试此配置。

此演示使用的 IP 地址是由
文件 Demo/lwIP_Demo_Rowley_ARM7/EMAC/SAM7_EMAC.h 中的常量 emacIPADDR0 到 emacIPADDR3 设置。
运行 Web 浏览器的计算机使用的 IP 地址必须和原型板使用的 IP 地址相兼容。
为此，可以将二者 IP 地址中的前三个八位元组设置成相同的值。
例如，如果运行 Web 浏览器的计算机所用 IP 地址是
192.168.100.1，那么原型板的 IP 地址可以使用 192.168.100.2 到 192.168.100.254 范围内的任何地址
（任何网络上的现有地址除外）。 



SAM7_EMAC.h 还包含定义网关地址、网络掩码和 MAC 地址的常量。
请务必确保所配置的 MAC 地址在原型板所连接的网络上具有唯一性。



Demo/lwIP_Demo_Rowley_ARM7/EMAC/SAM7_EMAC.c 包含定义 USE_RMII_INTERFACE。必须针对硬件
进行适当设置。将 USE_RMII_INTERFACE 设置为 1，可将 MAC 配置为在 RMII 模式下运行。将 USE_RMII_INTERFACE 设置为 0，
可将 MAC 配置为在 MII 模式下运行。



如果您想测试 USB CDC 驱动程序，则需要用 USB 连接目标硬件和 Windows 主机。目标板
可以通过同一条电缆供电。USB 设备会将自己标识为串行 COM 端口（相对于主机），然后，
在连接时，以 115200 波特持续传输字符串流。数据从空闲任务钩子发送到 CDC
驱动程序。



演示应用程序使用内置在原型板上的 LED ，因此不需要其他硬件设置。



  



### 构建用于调试的演示应用程序



目前提供两种项目配置。"THUMB Flash Debug" 使用最小优化，可轻松与 CrossConnect JTAG 调试接口
一起使用。"THUMB Flash Release" 具有更多优化，因此不太适合调试器。

只需在 CrossWorks IDE 中打开 rtosdemo.eww 工作区文件，确保选择 *THUMB flash debug* 配置
（见下图），然后在 IDE “Build” 菜单中选择 “Build Solution”。
  




![csselectbuild.gif](/media/2018/csselectbuild.gif)
  

选择 *THUMB flash debug* 配置


  



### 运行演示应用程序


1. 确保 CrossConnect JTAG 调试接口已连接，并且原型板已接通电源。
2. 确保以太网电缆已按上文所述完成连接。
3. 从 “Target” 菜单中选择 “Connect USB CrossConnect for ARM”，将 CrossConnect JTAG 接口连接到目标
 。
4. 在 IDE 的 “Debug” 菜单中选择 “Start Debugging”。
5. 嵌入式微控制器闪存将自动使用演示应用程序进行编程，并且调试器会在
 main() 函数开始处中断。在 IDE 的 "Debug" 菜单中选择 "Go"
 以开始执行应用程序。



  



### 功能



演示应用程序可创建 21 个任务，主要包括标准演示应用程序任务 
 （请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息）。
除了与 lwIP TCP/IP 堆栈和嵌入式网络服务器相关联的任务，还创建了一个示例 USB CDC 任务、 
一个“检查”任务和空闲任务。



如果演示应用程序正确执行，其表现如下：


* LED DS1、DS2 和 DS3 处于 "flash"（闪烁）任务的控制之下。每个 LED 都将以恒定的频率闪烁，其中 LED DS1
 速度最快，LED DS3 速度最慢。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。 
 因此，系统创建了一个“检查”任务，用于确保所有其他标准演示任务中 
 没有检测到任何错误。 

 LED DS4 由"检查"任务控制。每 3 秒，“检查”任务就会将系统中的所有标准演示任务检查一次，
 以确保任务执行无误。然后会切换至 LED DS4。如果 LED DS4 每 3 秒钟切换一次，
 则说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 发现了至少一个错误。
* 目标硬件将向标准 Web 浏览器提供包含 TCP/IP 统计信息的网页。该页面
 每隔几秒钟自动更新一次要连接到目标，请执行下列操作：



	1. 在连接的计算机上打开 web 浏览器。
	2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。
	

	![](/media/2018/enterurl.gif)  
	在 web 浏览器中输入 IP 地址  
	（当然，根据您的系统，使用正确的 IP 地址）
* 演示应用程序还将自己标识为 “FreeRTOS 演示 CDC 驱动程序”（对于 USB 主机），并且主机的 “找到新硬件”向导
 将为设备提示合适的驱动程序的位置。 



![](/media/2018/foundnewcdc.gif)  
检测到 USB 连接时，Windows 的“找到新硬件”消息。

 将向导定向到文件 FreeRTOSCDC.inf 所在的目录 FreeRTOS/Demo/lwIP_Demo_Rowley_ARM7/USB
 将指示 Windows 如何与 CDC 设备进行通信。



 成功安装驱动程序后，SAM7X 目标将显示为串行 COM 端口并持续向主机
 流式传输数据字节。 





![](/media/2018/devman.gif)  
“FreeRTOS CDC 演示”在 Windows 设备管理器中显示为 COM端口。


 可以使用哑终端程序（例如超级终端）来查看传输的数据，该哑终端程序需设置为 115200 baud，有 8 个数据位，无奇偶校验，
 有 1 个停止位且无流量控制。




![](/media/2018/hyperterm.gif)  
在超级终端上查看通过 USB 端口传输的数据。




---


### EMAC 和 USB 驱动程序


### Web 服务器和 EMAC 操作


最基本的 Web 服务器功能位于文件 Demo/lwIP_Demo_Rowley_ARM7/BasicWEB.c 中。每个
HTTP 连接都会立即得到服务，随后关闭。更全面的实现可以为每个连接生成一个新任务，
然后等待数据到达，并在连接关闭时删除任务。

LwIP 堆栈内的链式内存缓冲区实现导致数据以多个可变长度段落的形式被发送到 EMAC 驱动程序
和从 EMAC 驱动程序接收。这与仅有单个缓冲区的 uIP 堆栈不同，对于后者，所有
数据可以单个段落的形式复制到 EMAC 驱动程序和从 EMAC 驱动程序复制出来。因此，lwIP 演示使用的 EMAC 驱动程序
包括 EMAC 外围设备管理，该驱动程序比 uIP 项目使用的等效驱动程序更为全面。



由 EMAC 接收的数据在 DMA 的控制下缓冲。如果缓冲区可用于处理 EMAC 中断,
则会产生 EMAC 中断。中断服务程序所做的只是通过信号量向 EMAC 驱动程序发出数据可用于处理的 
信号。信号量立即解除对接口任务的阻塞，该任务处理数据，并在必要时生成响应， 
或将数据传递到 TCP/IP 堆栈。



驱动程序在信号量上阻塞（具有超时）。因此，如果没有数据可用于处理，则任务将定期解除阻塞，
以执行 TCP/IP 堆栈所需的定期处理。



EMAC 可用接收缓冲区数量由文件
Demo/lwIP_Demo_Rowley_ARM7/EMAC/emac.h 中的变量 NB_RX_BUFFERS 设置。每个接收缓冲区为 128 字节，此大小仅适用于硬件
且不得更改。



EMAC 可用的传输缓冲区数量由 emac.h 中的 constant NB_TX_BUFFERS 设置。



  



### EMAC 驱动程序重入


可以通过多个任务访问 EMAC 驱动程序。它本质上是不可重入的，因此 
由网络接口级别的信号量（在文件 ethernetif.c 内）保证访问。这与 uIP 演示不同，对于后者，
只有一个任务可以访问驱动程序，不需要明确的保证。

  



### 对 lwIP 代码的修改


lwIP 代码的可移植（非特定于硬件）部分基本上保持不变，只稍微编辑了几个地方，
移除了良性编译器警告。

  



### USB 驱动程序


USB 驱动程序由第三方提供，作为原始 FreeRTOS HID 类演示的改编。提供该驱动程序， 
希望它是有用的，但无法直接获得支持。还请注意，它将大量使用队列，相比其他
更简单的循环缓冲区实现，它会降低效率。

  





---


### RTOS 配置和使用详情



此演示使用 FreeRTOS SAM7 GCC 移植。

  


### RTOS 移植特定配置


此移植的特定配置项目位于 Source/Demo/lwIP_Demo_Rowley_ARM7/FreeRTOSConfig.h。您可编辑此文件中定义的常量，
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
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

  

请参阅 Demo/lwIP_Demo_Rowley_ARM7/EMAC/SAM7_EMAC_ISR.c 中定义的 vEMACISR() 以获取完整示例。

  


### 使用 SAM7 以外的部件


SAM7 使用标准 ARM7 内核，并配备处理器特定外围设备。核心实时内核组件应该
能够在所有 ARM7 设备上移植，但需要考虑外围设备的设置和内存要求。应考虑的事项：
* prvSetupTimerInterrupt() in Source/portable/GCC/ARM7_AT91SAM7S/port.c 配置 SAM7 定时器以生成 RTOS tick。
* 移植、内存访问和系统时钟由 Demo/lwIP_Demo_Rowley_ARM7/main.c 中的启动文件和 prvSetupHardware() 配置。
* 中断服务程序的设置和管理假设存在 AIC（中断控制器）外围设备。
* 串行、USB 和以太网驱动程序。
* 寄存器位置定义由位于 FreeRTOS/Source/portable/GCC/ARM7_AT91SAM7S 中的 Atmel 提供的头文件提供。
* RAM 大小：参见下面的内存分配部分。


  


### 在抢占式和协同式 RTOS 内核之间切换


将 Demo/lwIP_Demo_Rowley_ARM7/FreeRTOSConfig.h 中的定义configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0 
可使用协同式调度。

  


### 编译器选项



与所有的移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是基于提供的演示应用程序项目文件
搭建您的应用程序。

  


### 执行上下文



RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意： 
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式 
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。






中断服务程序总是在 ARM 模式下运行。其他所有代码将运行在 ARM 或 THUMB 模式，这取决于构建。
应该注意的是，portmacro.h 中定义的一些宏只能从 ARM 模式代码调用，而且如果从 THUMB 代码
调用会导致编译时错误。请注意，此特定演示仅使用 THUMB 模式进行了测试。


仅为系统/用户、IRQ 和 SWI 模式分配了堆栈。


SWI 指令由实时内核使用，不能被应用程序代码使用
（无需修改 RTOS 内核代码）。



  


### MAC 接口


确保已针对硬件正确配置了 USE_RMII_INTERFACE。请参阅上述演示应用程序硬件设置说明。

  


### 内存分配


SAM7X 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c 
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节 
获取完整信息。

  





---


### 使用 GCC（命令行版本）构建演示


提供了一个 makefile 和 linker 脚本，以允许使用 GCC 标准命令行版本构建 lwIP Web 服务器
演示。Makefile 位于 Demo/lwIP_Demo_Rowley_ARM7 目录中。 

请注意，取决于所使用的 GCC 版本，makefile 可能需要将优化级别设置为最小的 O1。或者，-fomit-frame-pointer 选项可以添加到 CFLAGS。



Linux 用户请注意，由于我无法访问 Linux 主机，makefile 仅在区分大小写的 Win32 主机上进行了测试。在 Linux 主机上遇到的任何构建问题都可能
是文件名中包含错误大写字母的结果。如果遇到任何此类问题，请告知我，以便在发布未来版本时予以纠正。 




  

  

  

  

  












