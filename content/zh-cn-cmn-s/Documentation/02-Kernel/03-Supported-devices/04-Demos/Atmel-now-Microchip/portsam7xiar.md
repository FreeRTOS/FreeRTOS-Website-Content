---
title: "uIP 嵌入式 Web 服务器演示，使用 FreeRTOS SAM7X ARM 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



uIP 嵌入式 Web 服务器演示，使用 FreeRTOS SAM7X ARM 移植

[[嵌入式以太网示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]


  




|  |
| --- |
| <br />![](/media/2018/sam7xek.gif)<br />*Studio Cadrage*<br /> |
|




本页描述了 FreeRTOS SAM7X 嵌入式以太网 TCP/IP 示例应用程序。该演示使用 FreeRTOS IAR SAM7 ARM 移植和
Adam Dunkels 开源 [uIP](http://www.sics.se/~adam/uip/) 堆栈，在 AT91SAM7X-EK 开发板上创建嵌入式 Web 服务器
（如果您想使用其他开发板，我们也提供了相关[说明](porting-a-freertos-demo-to-different-hardware.md)）。
还提供了一个[替代项目](portsam7xlwIP.md)，用于演示如何使用 GCC 编译器
来使用功能更丰富的 LwIP TCP/IP 堆栈。

自此演示创建以来，FreeRTOS 已对 uIP 堆栈做了一些修改。详情请参阅[嵌入式以太网示例列表](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)页面。



此演示：


* 完全由开源软件组成。
* 包括用于 SAM7X 集成 EMAC （以太网媒体访问控制器）外围设备的基本驱动程序。
* 演示 uIP 与 FreeRTOS的 集成。
* 演示使用简单的 CGI 脚本语言（由 Adam Dunkels 编写）创建动态数据。
* 除 Web 服务器任务和闲置任务之外，还创建了 31 个标准演示任务。



uIP TCP/IP 堆栈与 FreeRTOS 分开授权。用户必须熟悉[uIP 许可证](uip-license.txt)。

**注意：**如果项目构建失败，则可能是使用的 IAR
嵌入式工作台版本过低。如果构建失败， 
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。





---


### *重要提示！SAM7X Web 服务器演示使用说明*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织



FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件多于此演示使用的文件。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

此 SAM7X Web 服务器演示使用标准 FreeRTOS IAR SAM7 移植。uIP IAR 演示项目工作区 *rtosdemo.eww* 位于
Demo/uIP_Demo_IAR_ARM7 目录下，应从嵌入式工作台 IDE 中打开。



Demo/uIP_Demo_IAR_ARM7/SrcIAR 和 Demo/uIP_Demo_IAR_ARM7/resource 目录 
包含 Atmel 库和构建环境的支持文件。



Adam Dunkels uIP 代码位于 Demo/uIP_Demo_IAR_ARM7/uIP 目录下。演示使用的 HTML 文件 
位于 Demo/uIP_Demo_IAR_ARM7/uIP/fs 目录下。



最后，Demo/uIP_Demo_IAR_ARM7/EMAC 目录包含 EMAC 驱动程序。




---


### 演示应用程序


#### 演示应用程序设置



直接使用点对点（交叉）电缆，或使用标准以太网电缆通过集线器或交换机，
将所选开发板连接到运行 Web 浏览器的计算机上。点对点连接时，原型板应该也允许使用标准以太网电缆， 
但我尚未测试此配置。

演示使用的 IP 地址由
文件 Demo/uIP_Demo_IAR_ARM7/uIP/uipopts.h 中的常量 UIP_IPADDR0 到 UIP_IPADDR3 设置。
运行 Web 浏览器的计算机使用的 IP 地址必须和原型板使用的 IP 地址相兼容。
为此，可以将二者 IP 地址中的前三个八位元组设置成相同的值。
例如，如果运行 Web 浏览器的计算机所用 IP 地址是
192.168.100.1，那么原型板的 IP 地址可以使用 192.168.100.2 到 192.168.100.254 范围内的任何地址
（任何网络上的现有地址除外）。 



演示使用的 MAC 地址由常量 UIP_ETHADDR0 至 UIP_ETHADDR5 进行设置，这些常量也位于 uipopts.h 中。
请务必确保所配置的 MAC 地址在原型板所连接的网络上具有唯一性。



Demo/uIP_Demo_IAR_ARM7/EMAC/SAM7_EMAC.c 包含定义 USE_RMII_INTERFACE。必须针对硬件
进行适当设置。将 USE_RMII_INTERFACE 设置为 1，可将 MAC 配置为在 RMII 模式下运行。将 USE_RMII_INTERFACE 设置为 0，
可将 MAC 配置为在 MII 模式下运行。



演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。



  



#### 构建用于调试的演示应用程序



目前提供两种项目配置。“Flash Debug” 使用最小优化，可轻松与 J-Link JTAG 调试接口
一起使用。“Flash Release” 使用完全优化（减去静态群集）。

只需在 IAR 嵌入式工作台 IDE 中打开 rtosdemo.eww 工作区文件，确保选择 *flash debug* 配置
（见下图） ，然后在 IDE "Project" 菜单中选择 "Built Target"。
  




![ewprojselect.jpg](/media/2018/ewprojselect.jpg)
  

选择 *flash debug* 配置


  



#### 运行演示应用程序



IAR 移植无法使用 IAR 模拟器执行，因此必须在目标硬件上执行。



1. 确保 J-Link JTAG 调试接口已连接，并且原型板已接通电源。
2. 确保以太网电缆已按上文所述完成连接。
3. 在 IDE 的 "Project" 菜单中选择 "Debug"。
4. 嵌入式微控制器闪存将自动使用演示应用程序进行编程，并且调试器
 会在重置的矢量处（地址 0）中断。在 IDE 的 "Debug" 菜单中选择 "Go"，
 以开始执行应用程序。



  



### 功能



演示应用程序可创建 33 个任务，主要包括标准演示应用程序任务 
 （请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息）。
此外，还可创建一个 uIP 任务，用于实现嵌入式网络服务器、"Check"（检查）任务和空闲任务。



如果演示应用程序正确执行，其表现如下：


* 目标硬件将向标准 Web 浏览器提供网页。要连接到目标，请执行下列操作：



	1. 在连接的计算机上打开 web 浏览器。
	2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。
	

	![](/media/2018/enterurl.gif)  
	在 web 浏览器中输入 IP 地址  
	（当然，根据您的系统，使用正确的 IP 地址）
* LED DS1、DS2 和 DS3 处于 "flash"（闪烁）任务的控制之下。每个 LED 都将以恒定的频率闪烁，其中 LED DS1
 速度最快，LED DS3 速度最慢。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。 
 因此，系统创建了一个检查 (Check) 任务，用于确保所有其他任务中没有检测到任何错误。 

 LED DS4 由 "Check" 任务控制。每 3 秒， "Check" 任务就会将系统中的所有任务检查一次，
 以确保任务执行无误。然后会切换至 LED DS4。如果 LED DS4 每 3 秒钟切换一次，
 则说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一处错误。




---


### 配置和用法详情


#### HTML 页面


HTML 页面被转换为内置在闪存映像中的 C 语言常量结构体。这可以使用 Perl 脚本
Demo/uIP_Demo_IAR_ARM7/uIP/makdefsdata。Perl 脚本需要 Linux，或者
我使用的 Cygwin shell。

  



#### CGI 脚本


提供的每个网页都包括一些动态数据，以展示 uIP CGI 脚本编写工具的使用。有关更多信息，
请参阅 uIP 文档。

RTOS CGI 文件会生成一个表格，其中包含在演示中执行的每个任务的信息。此表格可供演示，
但由于在其创建过程中必须长时间禁用中断，
因此不推荐用于具有严格实时要求的应用程序。



  



#### Web 服务器和 EMAC 操作


Web 服务器功能包含在文件 Demo/uIP_Demo_IAR_ARM7/uIP_Task.c 中。 

借助 EMAC DMA 操作，EMAC 外围设备与 Web 服务器任务之间的交互变得非常简单。 
uIP 的单缓冲区内存管理
进一步简化了两者之间的交互。LwIP 堆栈实现了更灵活（复杂）的内存管理方案，
因此， lwIP 演示应用程序包含更全面的 EMAC 驱动程序。



由 EMAC 接收的数据在 DMA 的控制下缓冲。如果缓冲区可用于处理 EMAC 中断，
则会产生 EMAC 中断。中断服务程序所做的只是通过信号量向 uIP 任务发出数据可用于处理的信号。
信号量立即解除对 uIP 任务的阻塞，该任务处理数据，并在必要时生成响应。



uIP 任务在信号量上阻塞（具有超时）。因此，如果没有数据可用于处理，则 uIP 任务将定期解除阻塞，
以执行 TCP/IP 堆栈所需的定期处理。



EMAC 可用的接收缓冲区数量由文件
Demo/uIP_Demo_IAR_ARM7/SrcIAR/emac.h 中的常量 NB_RX_BUFFERS 设置。每个接收缓冲区为 128 字节。



EMAC 可用的传输缓冲区数量由 emac.h 中的 constant NB_TX_BUFFERS 设置。每个
传输缓冲区的大小等于 uIP 缓冲区的大小。



下载中包含的驱动程序使用 EMAC 的最基本配置。



  



#### EMAC 驱动器重入


由于 uIP 任务
是唯一访问 uIP 缓冲区的任务，因此此演示无需显式重入。这与 lwIP 演示相反， 
在 lwIP 演示中，通过在网络接口层面使用信号量显式地处理互斥。

  



### 性能


uIP 堆栈每次仅允许一个数据包处于未确认状态。它会等待每个数据包单独完成确认
。因此，通过将动态生成的数据作为一个大数据包而非多个小数据包传输，
可显著提高性能。这可以通过源代码下载中的 CGI 脚本示例来演示。 
用于生成任务表的 CGI 脚本将整张表放入一个数据包中传输，因此加载速度较快。
用于生成文件表和 TCP/IP 统计表的 CGI 脚本会单独传输各自表中的每行数据，
因此页面加载时间较长。

  



#### 对 uIP 代码的修改


在 httpd.c 中的函数 next_scriptstate() 中对标准 uIP 源代码进行了唯一的修改。变量 i 的类型
从 u8_t 更改为长整型，因此 CGI 脚本的最大行的长度可超过 255 个字节。

  



#### RTOS 配置


SAM7X 演示使用标准 SAM7 RTOS 移植。请参阅 [SAM7S 演示文档](portsam7iar.md)
以了解更多详细信息。

注意！ 
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式 
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序项目，则在调用 vTaskStartScheduler() 之前，请确保处理器已进入监管器模式。


  


#### MAC 接口


确保已针对硬件正确配置了 USE_RMII_INTERFACE。请参阅上述演示应用程序硬件设置说明。


   

  

  

  

  










