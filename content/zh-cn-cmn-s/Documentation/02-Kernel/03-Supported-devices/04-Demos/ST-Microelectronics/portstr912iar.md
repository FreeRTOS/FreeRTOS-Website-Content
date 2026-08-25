---
title: "在 STR912 ARM9 微控制器上使用 FreeRTOS 的 lwip 嵌入式 Web 服务器演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[嵌入式以太网示例](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]

|  |
| --- |
| <br />![](/media/2018/str9.jpg)<br /> |

本页详细介绍了用于 [IAR 开发工具](http://www.iar.com/)的 FreeRTOS [STR91x ARM9](http://www.st.com/internet/mcu/subclass/828.jsp) 移植。

此移植配有嵌入式 Web 服务器演示，面向 [STR910-EVAL 开发套件](http://www.st.com/internet/evalboard/product/116931.jsp)
（如需使用其他开发板，我们也提供了相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)），该开发套件：

* 或者，使用[开源 lwIP TCP/IP 堆栈](http://savannah.nongnu.org/projects/lwip/) **1**。
* 包括基础 ENET 外围设备驱动程序。
* 演示使用简单的 CGI 脚本语言（由 Adam Dunkels 提供）创建动态数据。
* 创建超过 40 个演示任务。
* 编译代码大小保持在 32 KB 字节以下，以确保其能够使用 IAR 开发工具套件的 KickStart 版本进行编译。

(**1** Paul YU 最初将 lwIP 集成到现有 FreeRTOS 演示中。ST 也提供了支持。非常感谢！）

**注意：**如果项目构建失败，很可能是使用的 IAR
Embedded Workbench 版本过低。如果是这种情况，
则项目文件也很可能（在无提示的情况下）已经损坏，
即使已更新 IAR 版本，也需要将项目文件恢复到初始状态，才能构建项目。

---

### *重要！使用 STR9 RTOS 移植 Web 服务器演示的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件远多于此演示使用的文件。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
下载文件的描述和有关创建新项目的信息。

STR9 Web 服务器演示项目工作区 rtosdemo.eww 位于
Demo/ARM9_STR91X_IAR 目录，应从 Embedded Workbench IDE 中打开。

lwIP 堆栈位于 Demo/Common/ethernet/lwIP。

---

### 演示应用程序

### 演示应用程序设置

* **以太网——使用 lwIP 演示时**
 直接使用点对点（交叉）电缆或通过使用标准以太网电缆的集线器/路由器将 STR910-EVAL 开发板连接到运行
 Web 浏览器的计算机上。

 有关以太网协议自动协商的详细信息，请参阅以下有关库文件使用的说明。

 此演示使用的 IP 地址是由
 Demo/ARM9_STR91X_IAR/lwIP/include/lwIPWebServer/BasicWEB.h 文件中的 emacIPADDR0 到 emacIPADDR3 常量设置的。
 运行 Web 浏览器的计算机使用的 IP 地址必须和原型板使用的 IP 地址相兼容。
 为此，可以将二者 IP 地址中的前三个八位元组设置成相同的值。
 例如，如果运行 Web 浏览器的计算机所用 IP 地址是
 192.168.100.1，那么原型板的 IP 地址可以使用 192.168.100.2 到 192.168.100.254 范围内的任何地址
 （任何网络上的现有地址除外）。

 此演示使用的 MAC 地址是通过 Demo/ARM9_STR91X_IAR/library/include/91x_enet.h 文件中的 MAC_ADDR0 到 MAC_ADDR5 常量设置的。
 请务必确保所配置的 MAC 地址在开发板所连接的网络上具有唯一性。
* **LED**
 此演示应用程序使用了原型板中内置的 LED，因此无需使用其他硬件设置。
* **UART**
 此演示应用程序包括一个中断驱动的 UART 测试，其中一个任务传输字符，另一个任务接收这些字符。如需正确操作此功能，
 必须将环回连接器安装到 STR910-EVAL 原型板的 UART 连接器上
 （9 路连接器上的引脚 2 和 3 必须相互连接）。标记为 JP13 的跳线必须处于 UART2 位置（穿过最接近丝网上标记 UART2 的两个引脚）
 。

### 演示项目组织

![](/media/2018/str9proj.gif)

RTOSDemo 工作区 (Demo/ARM9_STR91X_IAR/RTOSDemo.eww) 包含单个项目，我们为该项目提供了以下配置
：

* **ARM - lwIP - D**：
 ARM 模式的 lwIP 演示，调试配置。
* **ARM - lwIP - R**：
 ARM 模式的 lwIP 演示，释放配置。

### 构建用于调试的演示应用程序

只需从 IAR Embedded Workbench IDE 中打开 rtosdemo.eww 工作区文件，如果使用了 32K 限制版编译器，则务必选择 *THUMB* 配置，
然后在 IDE 的 "Project" 菜单中选择 "Build Target"。

### 运行演示应用程序

1. 确保 J-Link JTAG 调试接口已连接，并且开发板已接通电源。
2. 确保以太网电缆已按上文所述完成连接。
3. 在 IDE 的 "Project" 菜单中选择 "Debug"。
4. STR9 闪存将自动使用演示应用程序进行编程，并且调试器
 会在重置的矢量地址处中断。在 IDE 的 "Debug" 菜单中选择 "Go"，
 以开始执行应用程序。

### 功能

此演示应用程序可创建超过 40 个任务，主要包括标准演示应用程序任务
 （有关各个任务的详细信息，请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分）。
除标准演示任务外，还创建了以下任务，用以演示开发板和 RTOS 的功能。

1. **Web 服务器任务：**提供包含动态生成的数据的页面，以显示 RTOS 任务以及 TCP/IP 状态和统计信息。
2. **LCD 任务：**LCD 任务是唯一可以直接访问 LCD 的任务，因此确保了互斥性。任何
 想要显示文本的任务会向 LCD 任务发送一条消息，其中包含指向应显示的字符串的指针。LCD 任务
 本身只在等待此类消息到达的队列中保持阻塞状态，该任务依次处理每条消息。
3. **LCD 消息任务：**LCD 消息任务只会定期向 LCD 任务发送消息。从
 LCD 消息任务发出的消息会在 LCD 顶行显示。
4. **检查任务：**检查任务每三秒仅执行一次，但其具有最高优先级，因此保证能够获得处理时间
 。其 main 函数用于检查其他所有任务是否仍在运行。大多数任务都会保持唯一计数，
 每当任务成功执行一次函数后，该计数就会递增。如果此类任务出现任何错误，
 则计数将永久停止。如果检查任务发现任何计数器变量的值指示发生错误，
 则会在错误状态标志下设置一个位
 。随后，该错误标志值会转换为字符串并发送到
 LCD 任务，以显示在 LCD 底行。

如果执行正确，该演示应用程序会实现以下效果：

* 开发板将向标准 Web 浏览器提供网页。要连接到目标，请执行下列操作：

	1. 在连接的计算机上打开 web 浏览器。
	2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。


	![](/media/2018/enterurl.gif)
	在 web 浏览器中输入 IP 地址
	（当然，根据您的系统，使用正确的 IP 地址）
* LED LD2、LD3 和 LD4 由 'flash' 任务控制。每个 LED 将以恒定频率闪烁，LED LD2 的频率最快，
 LED LD4 的频率最慢。
* 在 UART 上每传输一个字符，LD5 都会切换一次状态。由于切换速度过快，因此无法看清每个字符。
* LCD 顶行将显示 LCD 消息任务（如上所述）发送的轮转消息：IAR - STR912 - DEMO - www.FreeRTOS.org.
* 底行将显示检查任务（如上所述）发送的轮转消息。如果所有任务均未出现错误，
 则检查状态标志为 0：检查状态标志——等于 0x00。

---

### 配置和用法详情

### 库文件

此演示高度依赖 STMicroelectronics 外围设备库文件，并附有以下说明和修改：

* **LCD 驱动程序**
 我对 LCD 驱动程序做了一些微小的优化。然而，将整个字符串写入 LCD 可能仍需 100 毫秒左右。鉴于 LCD 任务的操作
 优先级高于某些标准演示任务，我已经在驱动程序中引入了一些延迟。这强制性地让 LCD 任务在某些操作中暂时进入阻塞状态，
 如此一来，优先级较低的演示任务便得以执行。

### HTML 页面

HTML 页面被转换为内置在闪存映像中的 C 语言常量结构体。这可以使用 Perl 脚本
Demo/ARM9_STR91X_IAR/webserver/makdefsdata 实现。

### 执行上下文

注意！
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序项目，则在调用 vTaskStartScheduler() 之前，请确保处理器已进入监管器模式。

要使用 ARM 模式，必须在项目设置中定义预处理器常量 \_RUN_TASK_IN_ARM_MODE\_。当然，还必须设置编译器，
以便生成 ARM 代码。

### RTOS 移植特定配置

此移植的特定配置项目位于 Source/Demo/ARM9_STR91X_IAR/FreeRTOSConfig.h。可以编辑此文件中定义的常量，
以适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会使用 #define 将 'BaseType_t' 定义为该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

任务上下文在进入 ISR 时自动保存并在退出时恢复。因此，中断服务程序应该像
任何其他函数一样进行定义，无需特殊语法或汇编文件包装。

我们提供了 portEND_SWITCHING_ISR() 宏，以便 ISR 在适当的情况下（例如，当在 UART 上接收的字符
唤醒了等待该字符的高优先级任务时）执行任务切换。

有关示例，请参阅 serial.c 文档中的 UART1_IRQHandler() 函数。

### 抢占式内核和协同式 RTOS 内核之间的切换

将 Demo/ARM9_STR91X_IAR/FreeRTOSConfig.h 中的 configUSE_PREEMPTION 定义设置为 1，可使用抢占式调度，
设置为 0，则可使用协作式调度。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序 makefile 构建应用程序。

### 内存分配

STR9 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。

