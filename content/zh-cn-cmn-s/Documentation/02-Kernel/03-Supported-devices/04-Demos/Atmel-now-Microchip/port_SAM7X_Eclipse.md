---
title: "SAM7X Web 服务器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



SAM7X Web 服务器和 USB 鼠标演示，使用 Eclipse、GCC 和 OpenOCD 实现完全开源的开发环境

[[嵌入式以太网示例](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]





|  |
| --- |
| <br />![](/media/2018/sam7xek.gif)<br /> |
|




此演示使用 FreeRTOS 在 AT91SAM7X-EK 原型板上创建了一个简单的 Web 服务器和 HID 类鼠标驱动程序的实现
（如果您希望使用替代开发板，我们也提供相关[说明](porting-a-freertos-demo-to-different-hardware.md)）。
本演示项目配置为使用 [Eclipse Europa](http://www.eclipse.org/)、 
[Yagarto](http://www.yagarto.de/) GCC 工具、[OpenOCD](http://openocd.sourceforge.net/)
和 [uIP mini TCP/IP 堆栈](http://www.sics.se/~adam/uip/index.php/Main_Page)。内置在 AT91SAM7X-EK 上的小操纵杆
用于提供鼠标输入。



自此演示创建以来，FreeRTOS 已对 uIP 堆栈做出一些修改。详情请参阅[嵌入式以太网示例列表](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)页面。



FreeRTOS zip 文件包含除 Eclipse 和 Yagarto 工具以外的所有必要内容。 
请仔细按照[这些说明](Eclipse.md)正确安装和配置 Eclipse，
以便与此演示应用程序一起使用。 



随附的 OpenOCD 可执行和相关配置文件经过设置用于兼容 
Macraigor Wiggler 的 JTAG 接口。



请注意，uIP 和 OpenOCD 与 FreeRTOS.org 分开授权。用户必须熟悉相应的许可证。



Linux 用户须知：虽然所使用的工具均为跨平台工具，但我仅在 Windows 主机上测试了 SAM7X/Eclipse 构建。





[\![](/media/2018/eclipse-banner.gif)](http://www.highintegritysystems.com/down-loads/stateviewer-plug-in/)





---


### *重要提示！Eclipse AT91SAM7X Web 服务器演示使用说明*


*使用此 RTOS 移植前，请阅读下述所有要点。*



1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)


另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)


---


### 源代码组织



Eclipse SAM7X 演示的 Eclipse 工作区位于 FreeRTOS/Demo/ARM7_AT91SAM7X256_Eclipse 目录下。在
Eclipse 启动过程中提示选择工作区位置时请选择此目录。在构建项目**前**，请务必阅读 [Eclipse 安装和配置说明](Eclipse.md)。

下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此其包含的文件
远多于此演示使用的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述和有关创建新项目的信息。







---


### 演示应用程序


### 演示应用程序设置



直接使用点对点（交叉）以太网电缆，或使用标准以太网电缆通过集线器/路由器
将 AT91SAM7X-EK 原型板连接到运行 Web 浏览器的计算机上。点对点连接时，原型板应该也允许使用标准以太网电缆， 
但我尚未测试此配置。

演示使用的 IP 地址由
文件 Demo/ARM7_AT91SAM7X256_Eclipse/RTOSDemo/FreeRTOSConfig.h中的常量 UIP_IPADDR0 到 UIP_IPADDR3 设置。
运行 Web 浏览器的计算机使用的 IP 地址必须和原型板使用的 IP 地址相兼容。
为此，可以将二者 IP 地址中的前三个八位元组设置成相同的值。
例如，如果运行 Web 浏览器的计算机所用 IP 地址是
192.168.100.1，那么原型板的 IP 地址可以使用 192.168.100.2 到 192.168.100.254 范围内的任何地址
（任何网络上的现有地址除外）。 



演示使用的 MAC 地址由常量 UIP_ETHADDR0 至 UIP_ETHADDR5 进行设置，它们也可以在 FreeRTOSConfig.h 中找到。
请务必确保所配置的 MAC 地址在原型板所连接的网络上具有唯一性。



演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。



  



### 构建演示应用程序


再次提醒，请参阅 Eclipse 安装和配置[说明](Eclipse.md)
以了解更多详细信息。
1. 确保已安装 [Yagarto](http://www.yagarto.de/)（或等效）GCC 工具，并且 Yagarto/bin 
 目录包含在您的 PATH 环境变量中。
2. 打开 FreeRTOS/Demo/ARM7_AT91SAM7X256_Eclipse Eclipse 工作区。
3. 确保 FreeRTOS_ROOT 变量已配置。
4. 按 F7（或从 "Project" 菜单中选择 "Build All"）以构建演示应用程序。



  



### 运行演示应用程序


再次提醒，请参阅 Eclipse 安装和配置[说明](Eclipse.md)
以了解更多详细信息。
1. 确保 Wiggler JTAG 调试接口已连接，并且 AT91SAM7X-EK 开发板已接通电源。
2. 确保以太网电缆已按上文所述完成连接。
3. 从"Run External Tools" 菜单中选择 "OpenOCD Programmer"， | 然后等待编程完成。对于一台速度相对较快的电脑，
 这大约需要 20 秒。



之后，如果您希望开始调试会话，请执行以下步骤：
1. 从"Run External Tools" 菜单中选择 "OpenOCD Server" | 。
2. **注意：**之后您可能收到一条错误消息："DBGACK set while target was in unknown state. Reset or initialize target before resuming"。 
 如果遇到这种情况，请停止服务器（点击控制台中错误输出上方的红色方块），然后再次使用 "Run External Tools" | 菜单项
 启动服务器。错误消息应仅在第一次尝试时出现。
3. 切换到调试视角。
4. 在调试窗格中选择可执行的 OpenOCD 服务器。
5. 点击 "Debug RTOSDemo" 加速按钮（带有绿色小虫图标的按钮）。



  



### 功能



此演示应用程序创建了 27 个任务。这些任务主要包含标准 
演示应用程序任务（请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息）。

除了标准演示任务外，还创建了以下任务/函数：


* uIP 任务  

 此任务操作所有的网络处理。它大部分时间都阻塞在某个信号量上，
 等待被传入的网络数据包生成的中断唤醒。
* USB 任务  

 该任务用于处理 USB 枚举。一旦枚举，USB 任务会定期读取内置在 SAM7X EK 上的操纵杆。任何操纵杆输入
 都作为鼠标输入提供给主机。请注意，此功能仅在不使用调试器，“单独”运行演示时有效。
* “检查” tick 钩子  

 tick 钩子函数用于监测标准演示任务——使用 LED
 DS4 指示系统状态。DS4 每 5 秒切换一次，
 表示所有标准演示任务在执行过程中都未发生错误。切换频率
 增加到 500 毫秒，
 表示在至少一个演示任务中发现了错误。




如果演示应用程序正确执行，其表现如下：




* LED DS1、DS2 和 DS3 处于 "flash"（闪烁）任务的控制之下。每个 LED 都将以恒定的频率闪烁，其中 DS1
 速度最快，LED DS3 速度最慢。
* “检查”函数将每 5 秒切换一次 LED DS4。
* 目标硬件将向标准 web 浏览器提供下述网页。要连接到目标，请执行下列操作：  

	1. 在连接的计算机上打开 web 浏览器。
	2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。


	![](/media/2018/enterurl.gif)  
	在 web 浏览器中输入 IP 地址  
	（当然，根据您的系统，使用正确的 IP 地址）
* SAM7X EK 上的操纵杆将向主机提供鼠标输入。仅当不使用调试器时，鼠标才会起作用。


  



### 提供的网页



每个提供的页面顶部包含一个菜单，其中含有指向其他每个页面的链接。




![](/media/2018/rtosstats.jpg)  
提供的 RTOS 统计页面


RTOS 统计页面提供了系统内每个任务状态的运行时信息，包括堆栈高水位线（任务开始执行后，
可随时在此处获取最小数量的堆栈）。该页面大约每 2 秒重新加载一次，具体取决于网络负载。



此页面分三个部分传输：HTML 标头和菜单、动态生成的内容以及 HTML 页脚。这样，
页面的加载速度相对较快。可以通过一次性传输整个页面来进一步优化加载速度。



有时，连续重新加载 RTOS 统计页面会导致无法从该页面离开。





![](/media/2018/SAM7X_WEB_Server_IO.jpg)  
提供的 IO 页面
IO 页面提供了一个简单的界面，展示被发送到 SAM7 微控制器的数据。



复选框允许设置和查询 LED DS4 的状态。点击 "Update IO" 按钮可将变更发送到目标硬件。请注意， LED
DS4 也处于“检查” tick 钩子的控制之下，因此将每 5 秒切换一次——覆写从 Web 服务器发送的任何命令。



TCP 统计信息和连接页面显示运行时网络信息。请注意，这些页面单独传输每行数据，因此加载速度较慢。 
这演示了如何通过牺牲已实现的数据吞吐量来利用小型传输缓冲区优化内存使用。




  





---


### RTOS 配置和使用详情



此演示使用 FreeRTOS SAM7S GCC 移植——重要的使用信息详见 [SAM7X/Rowley CrossWorks 演示文档页面](portsam7xlwIP.md)。
请阅读链接页面上提供的使用信息！





  

  

  

  

  










