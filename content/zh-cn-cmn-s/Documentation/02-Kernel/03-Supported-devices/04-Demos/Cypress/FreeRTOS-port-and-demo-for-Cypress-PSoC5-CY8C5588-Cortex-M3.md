---
title: "FreeRTOS PSoC5 CY8C5588 演示"
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
| <br />![](/media/2018/Cypress-PSoC5-CY8CKit-001-PS.jpg)<br /> |

此演示应用程序已经过以下评估套件测试：  

* [CY8CKIT-001 PSoC® 开发套件](http://www.cypress.com/?rID=37464)
* 使用 [CY8CKIT- 010 PSoC® CY8C55 系列处理器模块套件](http://www.cypress.com/?rID=43673)

PSoC5 演示包括带有多个外围设备的示意图设计，以演示它们与 RTOS 的集成。外围设备包括 UART、LCD 字符显示器和两种不同类型的定时器实现方式。

该演示使用：   

* FreeRTOS GCC 和 Keil ARM Cortex-M3 移植。
* [PSoC Creator 1.0 测试版 5](http://www.cypress.com/?id=2494) 及其包含的 GNU ARM 工具链。
* 或配置为使用 Keil MDK 或 RVDS ARM 工具链的 PSoC Creator。

---

### *重要提示！关于使用 PSoC5 ARM Cortex-M3 演示的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

请参阅 FreeRTOS 网站[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，了解下载文件的描述以及有关创建新项目的信息。

**PSoC Creator 工作区 - GCC**

* PSoC5 FreeRTOS 演示的 PSoC Creator 工作区文件名为 FreeRTOS_Demo Workspace.cywrk，并且位于 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_GCC 目录下。

**PSoC Creator 工作区 - Keil**

* PSoC5 FreeRTOS 演示的 PSoC Creator 工作区文件名为 FreeRTOS_Demo Workspace.cywrk，并且位于 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_Keil 目录下。

**PSoC Creator 工作区 - RVDS**

* PSoC5 FreeRTOS 演示的 PSoC Creator 工作区文件名为 FreeRTOS_Demo Workspace.cywrk，并且位于 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_RVDS 目录下。

---

### 演示应用程序

### PSoC5 演示应用程序设置

PSoC5 包含可再配置硬件。演示所需组件的原理图设计如下所示。设计包括：四个数字输出、一个数字输入、一个 UART 驱动器和四个单独的定时器，其中两个定时器作为 PWM 实现，另外两个作为定时器。根据原理图设计，需将输出和输入映射到主板上的物理引脚。可将引脚配置在 Design-wide-resource 中，默认值请参阅下文。

![](/media/2018/PSoC5_Schematic_Design.png)

启用 LED 和 UART COM 测试之前，需要在主板上进行以下几项连接操作。

* P0[0] 连接到 Rx 以进行 UART 输入或 P0[1] 连接到 Rx 以进行环回。
* P0[1] 连接到 Tx 以进行 UART 输入或 P0[0] 连接到 Tx 以进行环回。
* P0[4] 连接到 LED1。
* P0[5] 连接到 LED2。
* P0[6] 连接到 LED3。
* P0[7] 连接到 LED4。
* P1[7] 连接到 SW1。

![](/media/2018/PSoC5_Wiring_Scheme.jpg)

演示应用程序还使用 LCD 字符显示器，该液晶字符显示器需要引脚 P2[0:6]。无需其他安装步骤。

使用 MiniProg3 编程器/调试器对 CY8C5588 进行编程和调试。第一次用 USB 连接评估板和 PC 时，系统会提示您安装各种 USB 驱动器。在 [PSoC Creator](http://www.cypress.com/?rID=38050) 安装过程中，可能会提示您安装所需的 USB 驱动器作为 PSoC 编程器的一部分。

### 构建和执行演示应用程序

这三个演示应用程序都使用 PSoC Creator IDE，但配置为使用不同的工具链进行编译和链接。

* **使用随附的 GCC 工具链**
	1. 从 PSoC Creator IDE 打开 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_GCC/FreeRTOS_Demo Workspace.cywrk 工作区文件。
	2. 从 IDE 的 'Build' 菜单中选择 'Clean and Build FreeRTOS_Demo'。构建项目时不应报错或出现警告。
	3. 按照编程和调试说明操作。
![](/media/2018/PSoC_Creator_Generic_Toolchains.png)

* **使用 Keil ARM 工具链**  

	1. 从 PSoC Creator IDE 打开 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_Keil/FreeRTOS_Demo Workspace.cywrk 工作区文件。
	2. 从 IDE 的 'Tools' 菜单中选择 'Options'。在 'Options' 对话框中，展开 'Project Management' 并选择 'Generic Toolchains'。
	3. 对于 'ARM MDK Generic'，单击 'Browse' 按钮并定位到 Keil 安装中包含 'arm[ar|asm|cc|link].exe' 工具的目录。例如，C:KeilARMBIN40。单击 'OK' 接受。
	4. 在 IDE 主窗口中，右键单击空白工具栏区域以打开上下文菜单，然后选择 'Build Configuration / Toolchain'。确保从 'Build Configuration / Toolchain' 工具栏中的第二个下拉列表框选择 'ARM MDK Generic'。
	5. 从 IDE 的 'Project' 菜单中选择 'Build Settings'。展开 'Linker' ，然后在 'Build Settings' dialog' 对话框中选择 'General'。
	6. 修改 'Additional Library Directories' 以添加 MDK 'armlib' 目录的路径。例如，C:/Keil/ARM/RV31/LIB/armlib。单击 'OK' 接受。
	7. 从 IDE 的 'Build' 菜单中选择 'Clean and Build FreeRTOS_Demo'。构建项目时不应报错或出现警告。
	8. 按照编程和调试说明操作。![](/media/2018/PSoC_Creator_Linker_Additional_Libraries.png)
* **使用 RVDS ARM 工具链**
	1. 从 PSoC Creator IDE 打开 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_RVDS/FreeRTOS_Demo Workspace.cywrk 工作区文件。
	2. 从 IDE 的 'Tools' 菜单中选择 'Options'。在 'Options' 对话框中，展开 'Project Management' 并选择 'Generic Toolchains'。
	3. 对于 'ARM RVDS Generic'，单击 'Browse' 按钮并定位到 RVDS 安装中包含 'arm[ar|asm|cc|link].exe' 工具的目录。例如，C:Program FilesARMRVCTPrograms4.1561win_32-x86_64。单击 'OK' 接受。
	4. 在 IDE 主窗口中，右键单击空白工具栏区域以打开上下文菜单，然后选择 'Build Configuration / Toolchain'。确保从 'Build Configuration / Toolchain' 工具栏中的第二个下拉列表框选择 'ARM MDK Generic'。
	5. 从 IDE 的 'Build' 菜单中选择 'Clean and Build FreeRTOS_Demo'。构建项目时不应报错或出现警告。
	6. 按照编程和调试说明操作。
* **编程和调试**
	1. 从 IDE 的 'Debug' 菜单中选择 'Select Debug Target...'。在此对话框中，选择具有匹配序列号的 MiniProg3。单击 'Port Acquire'，选择 PSoC5 设备，然后单击 'Connect' 按钮，并关闭对话框。
	2. 在 IDE 的 'Debug' 菜单中选择 'Execute Code'。演示应用程序被编程到闪存中，然后调试器在 main() 处暂停。
	3. 在 IDE 的 'Debug' 菜单中选择 "Continue"。
	4. 或者，在将应用程序编程到闪存之前，在 IDE 的 'Debug' 菜单中选择 'Program'。演示应用程序将被编程到闪存中，设备将重置并开始执行应用程序。
	5. 如有必要，按下电路板上的 SW1 开关以允许演示应用程序继续进行。

### 功能

此演示应用程序创建了 52 个持久性任务，并定期动态创建和销毁另外 2 个任务。这些任务主要是标准演示应用程序任务（请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分，了解各个任务的详细信息）。

除了标准演示任务外，还创建了以下任务和测试：

* 高优先级中断测试  

使用自由运行定时器产生高频周期性中断，以演示如何使用配置常量 configKERNEL_INTERRUPT_PRIORITY。中断服务程序测量在各中断之间发生的处理器时钟的数量，由此测量中断定时中的抖动。测得的最大抖动时间测锁定在 usMaxJitter 变量中，并通过如下所述的 'Check' 任务显示在 LCD 显示屏上。timertest.c 源文件中配置并处理快速中断。这演示了如何在不影响更高优先级的中断处理的情况下配置 RTOS 内核。
* 检查任务  

该任务每 5 秒钟执行一次。其主要函数是检查所有标准演示任务是否仍在运行。如果在演示任务中发现任何意外行为，检查任务函数将向 LCD 写入错误代码。如果所有的演示任务都按照其预期的行为执行，那么检查任务将“通过”以及完成的迭代次数和如上所述的最大抖动时间写入 LCD。
* 中断队列测试  

PWM 外围设备产生 2000 Hz 和 2001 Hz 的中断。这些中断用作操作队列的触发器，其中触发器在队列中的任务之间生成上下文切换。如果中断频率远高于系统 tick 抢占，这意味着中断导致任务子集之间生成更频繁的上下文切换。

演示应用程序执行时表现如下：  

* 'Check' 任务将每 5 秒向显示器写入"Pass" 以及已完成的检查迭代次数和抖动时间（以纳秒为单位）。
* 如果标准演示任务出故障，则 'Check' 任务在检测到故障时将在显示器上打印出 "Fail"、检测到故障时的迭代以及抖动时间（以纳秒为单位）。
* LED 1、2 和 3 由标准 "flash" 任务控制。每个 LED 将以不同的固定频率切换。
* LED 4由标准演示 COM test Rx 任务控制。它将在每次传输字符时进行切换。UART 配置为环回模式，
 因此 COM test Rx 任务将接收每个传输的字符。

---

### RTOS 配置和使用详情

### RTOS 移植专用配置

专门用于此类演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_nnn/FreeRTOSConfig.h 中（其中 nnn 表示所使用的编译器）。可根据您的应用程序编辑此文件中所定义的常量。特别是：

* **configTICK_RATE_HZ**  

该常量可以用于设置 RTOS tick 的频率。演示项目提供的数值1000 Hz可用于测试 RTOS 内核功能，但速度高于大多数应用程序所需要的速度。降低此值可以提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**  

请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

请注意：ARM Cortex-M3 核心使用低数值数字表示高优先级中断，这似乎有点违反常理，而且很容易记混！如果您希望分配低优先级的中断，请不要将其优先级分配为 0 （或其他较小数值） ，因为这可能会导致中断实际上在系统中具有最高优先级。因此，如果此优先级高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，可能会导致系统崩溃。

ARM Cortex-M3 核心的最低优先级实际上是 255。然而，不同的 ARM Cortex-M3 供应商采用了不同数量的优先级位，并提供以不同方式指定优先级的库函数。使用提供的示例作为参考。

Cypress Design Wide Resource 可用于配置由每个外围设备所生成的中断的优先级。如果应用程序提供了自己的中断服务程序实现以访问内核 API，确保优先级在**数值**上等于或大于 configMAX_SYSCALL_INTERRUPT_PRIORITY，从而保证实际上具有较低的优先级。

如需安装自定义中断服务程序，请调用 *Peripheral_StartEx(vCustomISR)* 函数（其中' Peripheral' 是与 ISR 相关联的外围设备的名称），传递原型声明为 *CY_ISR_PROTO(vCustomISR)* 的中断服务程序函数以及声明为 *CY_ISR(vCustomISR)* 的函数。有关示例，请参见 IntQueueTimer.c 中的函数 vInitialiseTimerForIntQTests()。在此函数中，通过调用 isr_High_Frequency_2001Hz_StartEx() 安装 ISR。

每个移植 # 定义 'BaseType_t' 等于该处理器的最有效数据类型。此移植将 BaseType_t 定义为长整型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

在演示应用程序中，将向量表复制到 RAM 中。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。

宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。serial.c 中名为调用 vUartRxISR() 的 ISR 演示了所使用的 portEND_SWITCHING_ISR()。

请注意，portEND_SWITCHING_ISR() 将启用中断。

另请注意上文“RTOS 移植专用配置”部分中提供的有关安装自定义中断服务程序的信息。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_CY8C5588_PSoC_Creator_nnn/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 以使用抢占式内核，或设置为 0 以使用协同式内核。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。保证这一点的最佳方法是将应用程序建立在提供的演示应用程序文件上。

### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM Cortex-M3 演示应用程序项目中，以提供 RTOS 内核所需的内核分配。请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，以了解全部信息。

Design-wide-resource（FreeRTOS_Demo.cydwr）包含生成链接脚本的配置选项。当使用堆 3（Source/Portable/MemMang/heap_3.c）作为您的项目的一部分时，选择 'System' 选项卡，并展开 'Configuration' 以配置 'Heap Size' 。

