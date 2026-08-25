---
title: "适用于基于 GCC 的 Raisonance RIDE ARM 开发工具的 ST Microelectronics STR75x 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![](/media/2018/str750.jpg)STR750 评估板<br /> |

此 STR750 ARM7 演示应用程序已预配置为在 [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) 评估板上执行，
该评估板来自 [ST Microelectronics](http://www.st.com/)（如果您希望使用替代开发板，我们也提供了[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。

本页介绍的 RTOS 移植和演示应用程序
需要 [GNUARM GCC 工具链](http://www.gnuarm.org/)的 Raisonance RIDE IDE 接口。RLink In-circuit 调试器和编程器
需要直接从 RIDE IDE 对微控制器闪存进行编程。

使用 ST 提供的处理器外设库来提升开发效率。

---

### *重要！关于使用 STR750 GCC ARM RTOS 移植的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件
比 STR750 移植此演示使用的文件更多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，查看目录结构说明
和创建新项目的信息。

STR75x GCC ARM7 移植包含的演示 RIDE 项目名为 RTOSDemo.prj，可在 Demo/ARM7_STR75x_GCC 目录中找到。
此文件应直接从 RIDE IDE 中打开。

Demo/ARM7_STR75x_GCC/ST library 目录包含演示应用程序使用的 ST 外设库
组件。

---

### 演示应用程序

演示应用程序配置为创建 22 个完全抢占式任务。

### 演示应用程序硬件设置

在使用 RLink JTAG 接口之前，必须先从 STR75x-EVAL 评估板上移除 JP13。

标准“ComTest”任务在 UART0 上发送和接收字符。一个任务发送的字符
需要另一个任务来接收，如果任何字符被遗漏或接收顺序错误，则标记错误情况。评估板的 UART 0 上
需要一个环回连接器，才能使此功能正常工作（只需在标记为 CN4 的串行端口连接器上
将引脚 2 和 3 连接在一起即可）。

演示应用程序使用内置在评估板上的 LED ，因此不需要特定的硬件设置。

### RIDE 项目

![](/media/2018/str750ride.gif)
RIDE 演示应用程序项目

该项目包含 4 个文件夹：

1. **演示源文件**

 包含演示应用程序的源文件。
2. **库源文件**

 包含 RTOS 内核和演示应用程序使用的 ST 外设库的组件。
3. **RTOS 源文件**

 包含 FreeRTOS 实时内核的源文件。
4. **系统文件**

 包含启动代码和中断向量表定义。
重要提示：本项目使用的启动文件和链接器脚本已根据 Raisonance RIDE 发行版中
 包含的文件和脚本进行了修改。只应使用 Demo/ARM7_STR75X_GCC/SystemFiles 目录中包含的文件。

### 构建演示应用程序 - THUMB 模式

FreeRTOS 下载中的项目已预配置为使用 THUMB 模式。要使用 THUMB 模式构建项目，只需从 RIDE "Project" 菜单中
选择 "Build all" 。

这两个文件 serialISR.c 和 portISR.c
包含中断服务程序，因此必须编译为 ARM 模式。所有其他文件将编译为 THUMB 模式。

重要提示：
为此，应用于 serialISR.c 和 portISR.c 的项目选项不同于应用于所有其他文件的项目选项。如果编辑全局项目项目选项（使用
"Options" | "Project" 菜单选项），则应用于这两个文件的特殊选项将丢失，必须手动重置。如果不这样做，*项目将无法成功构建*。

为确保将 portISR.c 和 serialISR.c 编译为 ARM 模式：

1. 右键单击项目工作区内的文件，会出现一个弹出菜单。
2. 从弹出菜单中选择 "Options"，然后选择 "Local Options"。![](/media/2018/ridelocaloptions.gif)
设置文件的本地选项
 文件
3. 从弹出窗口中选择 "ARM Specific Options"，并确保未选择 "Generate THUMB Code"。![](/media/2018/ridespecificoptions.gif)

 确保为此文件生成 ARM 代码

### 构建演示应用程序 - ARM 模式

以下对项目选项的修改将导致所有文件使用 ARM 模式：

	1. 打开项目选项对话框，然后选择 "Defines"。删除定义 "THUMB_interwork"，保留 STR75X_GCC 作为唯一剩余的定义。


	![](/media/2018/ridearmbuild1.gif)
	删除 THUMB_INTERWORK 定义。
	2. 在同一个项目选项对话框中，选择 "ARM Specific Options"，并确保未选择 "Generate THUMB Code"。请注意，这次我们设置的是全局项目选项，而不是前面所述的
	 单个文件的本地选项。![](/media/2018/ridespecificoptions.gif)

	 确保为此项目生成 ARM 代码。

在 "Project" 菜单中选择 "Build all"，将整个项目重新构建为 ARM 代码。

### 对 STR750 FLASH 进行编程并启动调试器

1. 确保 RLink JTAG 接口正确连接到 STR75x-EVAL。
2. 接通目标板的电源。
3. 确保调试选项配置如下所示。![](/media/2018/ridedebugoptions.gif)
调试接口选项
- 在 RIDE 的 "Debug" 菜单中选择 "Start rtosdemo.elf"。





### 功能



演示应用程序创建 19 个[标准演示任务]/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview()，一个 "check" 任务、一个 "print" 任务
以及 "idle" 任务。


"print" 任务是一项“网关守卫”任务。也就是说，这是唯一应该直接访问 LCD 的任务，因此始终保证独占
（一致性）访问。"print" 任务只是阻塞队列以等待来自希望在 LCD 上显示文本的其他任务的消息。
到达的消息将解除阻塞任务，该任务将消息内容写入 LCD，然后再次阻塞。尽管在此应用程序中实际上只有一个生成显示文本的任务，
但此功能仅用于演示目的。



"check" 任务负责确保所有标准演示任务都按预期执行。该任务通常每 3 秒执行一次，
但其在系统内拥有最高优先级，因此保证能够获得执行时间。"check" 任务发现的任何错误都会被锁定，
直到处理器重置。"check" 任务在每个执行周期结束时会向 "print" 任务发送通过或失败的消息，以在 LCD 上显示。



如果正确执行，该演示应用程序将实现以下效果：



* LED LD2 到 LD4 由 "flash" 任务控制。
	各 LED 将以恒定的频率闪烁，其中 LD2 最快，LD4 最慢。
* LED LD5 处于标准 ComTest Tx 任务的控制之下。每次 ComTest Tx 任务
	通过 RS232 端口传输字符时，其状态都会切换。
* 大多数标准演示任务不会更新 LED，因此没有明确迹象表明它们运行正常，因此
	由 "check" 任务监控。

	LCD 上显示的 "Pass" 表示检查任务从未检测到任何任务中发生错误。每次显示文本时，
	文本的位置略有偏移，以提供检查任务本身仍在执行的视觉指示。
	错误检测机制可以通过在演示运行时从串行端口中移除回环连接器来进行测试，
	其中 "Pass" 消息应更改为 "Fail"。


---


### 配置和使用详情



#### RTOS 移植特定配置



此移植的特定配置项目位于 Demo/ARM7_STR75x_GCC/FreeRTOSConfig.h 中。可以编辑此文件中定义的常量，
以使其适合您的应用程序。特别是，configTICK_RATE_HZ 定义用于
设置 RTOS 滴答的频率。所提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但该值
高于大多数应用程序要求的频率。降低该值将会提高效率。

每个移植都会使用 #define 将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。




请注意，vPortEndScheduler() 尚未实现。






### 中断服务程序



STR75x 演示在调用用户定义的中断服务程序 C 代码之前自动保存和恢复任务上下文。这
与 STR71x 移植相反，后者通过 FreeRTOS 提供的宏在 C 代码中保存和恢复
上下文。这种替代方法用于演示。从用户的角度来看，其优点是简化了语法，
但缺点是不执行上下文切换的中断的执行时间稍长。


中断服务程序必须编写为 ARM 模式 C 函数。
例如：

```c

	void vAnISR( void )
	{
		/* ISR C code goes here. */

		/* Clear the interrupt within the peripheral here. */
	}

```





通常情况下，您需要中断服务程序来引起上下文切换。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。只需在中断服务程序中调用宏 END_SWITCHING_ISR()
来执行，如下所示：

```c

	void vAnISR( void )
	{
		/* ISR C code goes here. */

		/* Clear the interrupt within the peripheral here. */

		/* Pass in true to cause a context switch, or false to return
		to the interrupted task. */
		portEND_SWITCHING_ISR( pdTRUE );
	}

```





有关完整示例，请参阅 Demo/ARM7_STR75x_GCC/serial/serialISR.c 中的函数 vSerialISR()。





用户定义的中断程序必须替换 Demo/ARM7_STR75x_GCC/SystemFiles/ctr0_str75x_FreeRTOS.s 中 ST 提供的存根。







### 在抢占式和协作式 RTOS 内核之间切换


将 Demo/ARM7_STR75x_GCC/FreeRTOSConfig.h 中的定义 configUSE_PREMPTION 设置为 1，可使用抢占式内核；
设置为 0，则可使用协作式内核。




### 编译器选项



与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
提供的演示应用程序项目文件为基础构建您的应用程序，如[源组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分所述。




### 执行上下文



RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意：
启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
。FreeRTOS 下载内容中所包含的演示应用程序
会在 main 函数调用前切换到监管器模式。如果您没有使用
这些演示应用程序，则请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。






使用 Demo/ARM7_STR75x_GCC/SystemFiles/STR75x_COMMON_FreeRTOS.ld 中定义的常量配置每个必要操作模式的堆栈大小。无需
为用户/系统模式配置堆栈。



SWI 指令由实时内核使用，因此不能由应用程序代码使用。






### 内存分配
Source/Portable/MemMang/heap_1.c 包含在 ARM7 演示应用程序项目中，用来为实时内核分配
所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分
获取完整信息。




### 串行端口驱动程序

此外还应注意，编写串行驱动程序是为了测试部分实时内核功能，而不是
代表优化的解决方案。特别是，它们并不使用 FIFO。





### 滴答中断

时间基准 (TB) 外围设备用于生成滴答中断。

