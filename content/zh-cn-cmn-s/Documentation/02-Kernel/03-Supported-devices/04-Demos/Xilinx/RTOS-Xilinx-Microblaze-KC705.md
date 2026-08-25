---
title: "Xilinx MicroBlaze 移植 在 Kintex FPGA 的 KC705 评估套件上进行演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Xilinx KC705 Kintex FPGA 评估套件](/media/2018/KC705_Kintex_FPGA.jpg)

此 MicroBlaze 演示使用 Xilinx 的
[Vivado Design Suite](http://www.xilinx.com/products/design-tools/vivado.html/) 制作，
支持 8.x 版本的 [MicroBlaze 软核处理器](http://www.xilinx.com/tools/microblaze.htm)，
并在 Kintex FPGA 的
[KC705 评估套件](http://www.xilinx.com/products/boards-and-kits/ek-k7-kc705-g.html)开发板上进行开发和测试。

该演示包括一个使用 1.4.0 版
[lwIP TCP/IP 堆栈](http://savannah.nongnu.org/projects/lwip/)的嵌入式 Web 服务器实现。
Web 服务器的服务器端包含 (SSI) 功能，用于
提供包含动态任务和运行时统计信息的页面。目前，FreeRTOS 和 lwIP
都作为应用程序的一部分（而不是 BSP 的一部分）构建。

---

### 重要！KC705 MicroBlaze RTOS 演示的使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#xilinx-microblaze-kc705-演示应用程序)
3. [构建和运行说明](#构建说明)
	1. [将项目导入 SDK](#构建说明)
	2. [构建演示应用程序](#构建演示应用程序)
	3. [对 Kintex FPGA 进行编程](#对-kintex-fpga-进行编程)
	4. [启动调试会话](#启动调试会话)
4. [RTOS 配置和使用详情](#rtos-内核配置和使用详情)
	1. 应用程序必须提供的回调函数
	2. 实现中断服务程序 (ISR)
	3. [从 ISR 进行上下文切换](#isr-的切换上下文)
	4. [安装并启用 ISR](#安装并启用-isr)
	5. [异常处理（仅适用于高级用户）](#异常处理仅适用于高级用户)
	6. RTOS 演示特定配置

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码及
演示应用程序，因此它包含的文件数量远多于
使用 MicroBlaze 移植或 KC705 演示应用程序所需的文件。
请参阅本网站的[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
获取关于已下载文件的说明
和新项目创建的信息。

演示应用程序使用的目录结构如下所示
目录结构。MicroBlaze_Kintex7_EthernetLite 根目录
位于 /FreeRTOS/Demo 中。

```c

MicroBlaze_Kintex7_EthernetLite
    |
    +-RTOSDemo  Contains the SDK project and C files specific to the demo.
    |
    +-BSP       Contains the hardware BSP.
    |
    +-Hardware  Contains the hardware description.


```

**注意**：
RTOSDemo 目录只包含
特定于 KC705 MicroBlaze 演示的源文件。RTOS 源文件、lwIP 源文件、
CLI 源文件以及
实现所有演示应用程序通用任务的源文件位于
[目录树中的其他位置](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)。
如果默认目录结构已更改，
包括 /FreeRTOS-Plus 目录（包含 CLI 源文件），
则可能无法构建项目。

另请参阅相关页面，了解
[如何在 Eclipse 项目资源管理器中
使用虚拟路径和链接路径](Project_Workspace_Relative_File_Paths_Eclipse)。

---

### Xilinx MicroBlaze KC705 演示应用程序

### 功能

常量 mainSELECTED_APPLICATION 定义 (#define) 位于
main.c 顶部，用于在简单的 Blinky 样式演示、更全面的
更全面的测试和演示应用程序以及 lwIP 演示之间切换，
如以下三部分所述。

### mainSELECTED_APPLICATION 设置为 0 时的功能

如果 mainSELECTED_APPLICATION 设置为 0，则 main() 将调用
main_blinky()，此函数在 main_blinky.c 中实现。

main_blinky() 会创建一个基本的入门演示，包含两个任务和一个队列。
一个任务使用队列将值 100 定期发送到另一个任务。
每次收到消息时，接收任务都会切换一次 LED。消息
每 200 毫秒发送一次，因此 LED 每 200 毫秒切换一次。

### mainSELECTED_APPLICATION 设置为 1 时的功能

如果 mainSELECTED_APPLICATION 设置为 1，则 main() 会调用 main_full()，
此函数在 main_full.c 中实现。

![在 Xilinx Microblaze 上运行的免费 RTOS](/media/2018/Microblaze_CLI.png)

**CLI 会话示例**

main_full() 会创建一个综合测试和演示应用程序
以展示：
* [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 命令行接口。
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。

通过 KC705 板上标有 “USB UART J6” 的 USB 连接器连接到 FreeRTOS-Plus-CLI
。USB 端口将在主机计算机上枚举为名
“Silicon Labs CP210x USB to UART bridge”的 COM 端口，
然后可以使用 Teraterm 或 HyperTerminal 等哑终端以 115200 波特率连接到该端口。在 CLI 中键入 "help"，
查看已注册命令列表。

由综合演示创建的大多数任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务。这些任务由所有 FreeRTOS 演示应用程序使用，
除了演示使用中的 FreeRTOS
API 和测试 RTOS 移植之外，没有特定的功能或目的。

除了标准演示任务外，还创建了以下任务：

* 寄存器测试任务

 这些任务会通过用已知的唯一值填充每个 MicroBlaze 寄存器来测试 RTOS 内核上下文切换机制，
 然后反复检查
 原始写入寄存器的值
 是否在任务的生命周期内
 保持不变。任务以空闲优先级执行，
 因此会定期被抢占。寄存器检查任务的性质
 决定了它们必须用汇编编写。
* “检查”任务

 检查任务会定期查询标准演示任务和
 寄存器测试任务，以确保其正常运行。检查任务
 还切换 LED 7，以直观显示
 系统状态。
 **如果 LED 7 每 3 秒切换一次，则表示检查任务未发现演示中存在任何问题。
 如果 LED 7 每 200 毫秒切换一次，
 则表示检查任务在至少一个任务中
 发现[潜在]问题。**

### mainSELECTED_APPLICATION 设置为 2 时的功能

如果将 mainSELECTED_APPLICATION 设置为 2，则 main() 将调用 main_lwIP()，
该函数在 main_lwIP. c 中实现。

LwIP 示例配置为使用静态 IP 地址。静态 IP
地址由常量 configIP_ADDR0 设置为 configIP_ADDR3
（位于 FreeRTOSConfig.h 底部）。用于定义网络掩码的常量
网络掩码的常量也位于 FreeRTOSConfig.h底部。所选的
和网络掩码必须
与 MicroBlaze 目标所连接的网络兼容。这通常可以通过
通过设置目标 IP 地址和网络掩码的前三个八进制位以
分别匹配主机 IP 地址和网络掩码的前三个八进制位来实现
。所选 IP 地址在网络上必须唯一。

如果目标和主机系统直接连接（未通过集线器或交换机），
则必须使用交叉（点对点）以太网电缆。如果目标系统和主机系统通过集线器或交换机连接，
则必须使用
标准以太网电缆。

当正确连接时，演示将使用 lwIP 套接字 API 创建
一个 FreeRTOS-Plus-CLI 命令控制台，并使用 lwIP 原始 API 创建一个
基础 HTTP 网络服务器。服务器端包含 (SSI) 功能用于生成
服务网页中的动态数据。
要连接到 HTTP 服务器，只需将目标的 IP 地址键入
Web 浏览器的地址栏。

要连接到 FreeRTOS-Plus-CLI，请打开命令提示符，然后输入 `telnet <ipaddr>`，
其中 `<ipaddr>` 是目标的 IP 地址。连接后键入 "help"，
查看已注册命令列表。请注意，此示例并不实现
真正的 telnet 服务器，只是使用 telnet 端口编号，轻松
使用 telnet 工具进行轻松连接。

---

### 构建说明

### 将演示应用程序项目导入 SDK Eclipse 工作区

要将 Xilinx 软件开发套件 (SDK) 项目导入现有或全新 Eclipse 工作区，请执行以下操作：

1. 从 SDK 的 "File" 菜单中选择 "Import"。将出现如下所示的
 对话框。如图所示，选择 "General->Existing Project into Workspace"。

![将 Xilinx MicroBlaze RTOS 演示项目导入 SDK](/media/2018/Importing-the-Xilinx-MicroBlaze-RTOS-demo-project-into-the-SDK.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 /FreeRTOS/Demo/MicroBlaze_Kintex7_EthernetLite
 作为根目录。然后，确保在 "Projects" 区域中已勾选 RTOSDemo、BSP 和
 Hardware 项目，
 **并且确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![将免费的 ARM Cortex-A9 RTOS 演示源项目导入 Xilinx SDK](/media/2018/import_KC705_projects.png)

**确保勾选了全部三个项目，不勾选 "Copy projects into workspace"**
3. 导入全部三个项目后，SDK IDE 的项目资源管理器窗口
 如下图所示。

 Hardware 和 BSP 项目是
 RTOSDemo 项目的依赖项，因此只需要显式构建 RTOSDemo 项目。

![在 Eclipse 项目资源管理器中查看 MicroBlaze KC705 RTOS 项目。](/media/2018/KC705_Project_Explorer.png)

**导入工作区的所有三个项目**

### 构建演示应用程序

1. 打开项目的 main.c 文件，并设置 mainSELECTED_APPLICATION，
 根据需要生成简单的 blinky 演示、完整的测试和演示
 或 lwIP 以太网示例（视需要而定）。
2. 从 IDE 的 "Project" 菜单中选择 "Rebuild All"。应用程序应
 成功构建，没有任何错误或警告。

**注意：**截至本文撰写之时，
SDK 中的依赖项管理存在一处故障。如果对头文件进行编辑，则必须
对整个项目进行完全清洁和重新构建，以使变更生效。未完成上述操作
将导致似乎无法解释的运行时行为。

### 对 Kintex FPGA 进行编程

必须先对 Kintex FPGA 进行编程，然后才能将应用程序
下载到 MicroBlaze 软核微控制器。此步骤仅需在
每次重启时执行一次。
1. 确保 KC705 硬件已通电，
 并使用其 JTAG USB 连接连接到主机。
2. 从 IDE 的 "Xilinx Tools" 菜单中选择 "Program FPGA"。此时屏幕上
 将显示 "Program FPGA" 窗口。
3. 单击 "Program" 之前，按如下所示配置 "Program FPGA" 窗口。
 base_microblaze_design_wrappers 文件位于
 工作区中的 Hardware 项目中。

![对 Kintex FPGA 进行编程，以在 MicroBlaze 上运行 RTOS 演示](/media/2018/programming-the-Kintex-FPGA.png)

**对 Kintex FPGA 进行编程所需的配置**

### 启动调试会话

1. 确保 Kintex FPGA 已按上述方式进行编程，
 并且仍使用硬件的 JTAG USB 连接器
 连接到主机。
2. 在 IDE 的 "Run" 菜单中选择 "Debug Configurations..."。屏幕上会
 出现调试配置对话框。双击
 "Xilinx C/C++ application (System Debugger)" 创建新的调试
 配置。**注意**：
 如果打算使用 FreeRTOS 内核感知状态查看器插件，请使用 GDB 选项代替 System Debugger 选项。
3. 如下图所示配置 "Target Setup" 选项卡。

![Kintex FPGA MicroBlaze RTOS "Target Setup" 选项卡](/media/2018/Kintex_FPGA_Debug_Configuration.png)

**Target Setup 选项卡上的所需设置**
4. 如下图所示配置 "Application" 选项卡。

![Kintex FPGA MicroBlaze RTOS "Application" 选项卡](/media/2018/Kintex_FPGA_Application_Tab.png)

**Application 选项卡上的所需设置**

 "Debug Configurations" 对话框中的所有其他选项卡均可保留
 默认设置。
5. 单击 "Debug" 按钮开始调试。应用程序将
 下载到 RAM，调试器会在进入 main() 时中断。

---

### RTOS 内核配置和使用详情

### 应用程序须提供的回调函数

* void vApplicationSetupTimerInterrupt( void );

 这是应用程序定义的回调函数，用于安装滴答
 中断处理程序。该函数作为应用程序回调，
 而不是 RTOS 内核端口层的组成部分，因为 RTOS 内核
 将在许多不同的 MicroBlaze 和 FPGA 配置上运行，
 并非所有配置都定义或提供相同的定时器外围设备。

 vApplicationSetupTimerInterrupt() 必须安装 RTOS 内核定义的
 函数 vPortTickISR() 作为滴答中断处理程序。

 官方演示应用程序
 在 main.c 中包括 vApplicationSetupTimerInterrupt() 的示例实现。
 示例实现使用 Xilinx 定时器/计数器作为
 滴答中断源。如果您的硬件平台
 包含此外围设备，
 则无需修改即可使用示例实现。
* void vApplicationClearTimerInterrupt( void );

 这是应用程序定义的回调函数，用于清除
 vApplicationSetupTimerInterrupt() 回调函数安装的任何
 中断。它是
 该函数作为应用程序回调，因为 RTOS 内核
 将在许多不同的 MicroBlaze 和 FPGA 配置上运行，
 并非所有配置都定义或提供相同的定时器外围设备。

 官方演示应用程序
 在 main.c 中包括 vApplicationClearTimerInterrupt() 的示例实现。
 该示例实现补充了相同文件中
 的 vApplicationSetupTimerInterrupt() 示例实现，
 方法是：清除由 Xilinx 定时器/计数器外围设备生成的中断。
 如果您的应用程序未修改所提供的
 vApplicationSetupTimerInterrupt() 的示例实现，
 则也可以使用所提供的 vApplicationClearTimerInterrupt()，
 而无需进行任何修改。

### 实现中断服务程序 (ISR)

实现 ISR 的函数是普通的 C 函数，但必须符合以下
原型。

```c

void ISRFunctionName( void *ISRParameter );

```

### ISR 的切换上下文

ISR 通常会使任务解除阻塞
状态。例如，在任务处理到达队列数据
的情况下。队列为空时，没有要处理的数据，任务
可能会选择进入阻塞状态，以等待更多数据可用。
如果此时 ISR 将数据发送到队列，
则任务将自动解除阻止状态，因为队列不再为空。

如果 ISR 导致任务解除阻塞状态，并且
解除阻塞状态的任务优先级高于
或等于当前执行的任务（被中断的任务），则
应在 ISR 中执行上下文切换，
以确保 ISR 直接返回到新解除阻塞的
更高优先级任务。ISR 中断一个任务，
而返回到另一个任务。

宏 portYIELD_FROM_ISR() 是 taskYIELD() 的中断安全版本。该宏
需要一个参数（如果不为零），该参数将间接导致
上下文切换。以下是 portYIELD_FROM_ISR() 的使用示例，
该示例取自官方演示应用程序中的 serial. c 文件：

```c

/* Note that this function is called from the UART interrupt handler, it is not
itself an interrupt handler, so its prototype does not have to match that
required by all interrupt handlers. */
static void prvRxHandler( void *pvUnused, UBaseType_t uxByteCount )
{
signed char cRxedChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* While there are characters to process. */
    while( XUartLite_IsReceiveEmpty( xUartLiteInstance.RegBaseAddress ) == pdFALSE )
    {
        /* Obtain the next character. */
        cRxedChar = XUartLite_ReadReg( xUartLiteInstance.RegBaseAddress,
                                       XUL_RX_FIFO_OFFSET);

        /* Place the received character in the received queue. If writing to the
 queue causes a task to leave the Blocked state, and the task has a
 priority equal to or above the priority of the interrupted task, then
 xHigherPriorityTaskWoken will automatically get set to pdTRUE inside the
 xQueueSendFromISR() function itself. */
        xQueueSendFromISR( xRxedChars, &cRxedChar, &xHigherPriorityTaskWoken );
    }

    /* Call portYIELD_FROM_ISR(), passing in xHigherPriorityTaskWoken. If
 xHigherPriorityTaskWoken was set to pdTRUE inside xQueueSendFromISR(), then
 calling portYIELD_FROM_ISR() here will cause the ISR
 to return directly to the newly unblocked task. If xHigherPriorityTaskWoken
 has retained its initialised value of pdFALSE, then calling
 portYIELD_FROM_ISR() here will have no effect. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```

### 安装并启用 ISR

以下函数分别用于安装、启用和禁用
中断（在中断控制器中）。具有类似功能的 Xilinx BSP 库函数
**不得**使用。

如何使用这些函数的示例包含在
vApplicationSetupTimerInterrupt() 的实现中，该实现位于 main.c 中。

```c

/*
 * Installs pxHandler as the interrupt handler for the peripheral specified by
 * the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have pxHandler assigned as its interrupt
 * handler. Peripheral IDs are defined in the xparameters.h header file, which
 * is itself part of the BSP project. For example, in the official demo
 * application for this port, xparameters.h defines the following IDs for the
 * three possible interrupt sources:
 *
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the Xilinx timer
 * XPAR_INTC_0_UARTLITE_0_VEC_ID - for the UART
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet controller
 *
 *
 * pxHandler:
 *
 * A pointer to the interrupt handler function itself. This must be a void
 * function that takes a (void *) parameter.
 *
 *
 * pvCallBackRef:
 *
 * The parameter passed into the handler function. In many cases this will not
 * be used and can be NULL. Some times it is used to pass in a reference to
 * the peripheral instance variable, so it can be accessed from inside the
 * handler function.
 *
 *
 * pdPASS is returned if the function executes successfully. Any other value
 * being returned indicates that the function did not execute correctly.
 */
BaseType_t xPortInstallInterruptHandler( unsigned char ucInterruptID,
                           XInterruptHandler pxHandler, void *pvCallBackRef );

/*
 * Enables the interrupt, within the interrupt controller, for the peripheral
 * specified by the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have its interrupt enabled in the
 * interrupt controller. Peripheral IDs are defined in the xparameters.h header
 * file, which is itself part of the BSP project. For example, in the official
 * demo application for this port, xparameters.h defines the following IDs for
 * the three possible interrupt sources:
 *
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the Xilinx timer
 * XPAR_INTC_0_UARTLITE_0_VEC_ID - for the UART
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet controller
 *
 */
void vPortEnableInterrupt( unsigned char ucInterruptID );

/*
 * Disables the interrupt, within the interrupt controller, for the peripheral
 * specified by the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have its interrupt disabled in the
 * interrupt controller. Peripheral IDs are defined in the xparameters.h header
 * file, which is itself part of the BSP project. For example, in the official
 * demo application for this port, xparameters.h defines the following IDs for
 * the three possible interrupt sources:
 *
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the Xilinx timer
 * XPAR_INTC_0_UARTLITE_0_VEC_ID - for the UART
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet controller
 *
 */
void vPortDisableInterrupt( unsigned char ucInterruptID );

```

### 异常处理（仅适用于高级用户）

要启用 FreeRTOS 异常处理，首先必须将 MicroBlaze 本身
配置为包含异常处理功能，其次
必须在 FreeRTOSConfig.h 中将 configINSTALL_EXCEPTION_HANDLERS 设置为 1。
将 configINSTALL_EXCEPTION_HANDLERS 设置为 1 会
导致 RTOS 内核消耗的代码和数据空间增加。

提供以下函数来安装 FreeRTOS 异常处理程序，
并在发生异常时分别处理。的功能
FreeRTOS 异常处理程序
本身的功能在 portmacro.h 中的函数原型上方的注释中进行了描述，复制如下：

在 main-full.c 和 main-blinky.c 中
都提供了 vApplicationExceptionRegisterDump() 的示例实现。

```c

/*
 * vPortExceptionsInstallHandlers() is only available when the MicroBlaze
 * is configured to include exception functionality, and
 * configINSTALL_EXCEPTION_HANDLERS is set to 1 in FreeRTOSConfig.h.
 *
 * vPortExceptionsInstallHandlers() installs the FreeRTOS exception handler
 * for every possible exception cause.
 *
 * vPortExceptionsInstallHandlers() can be called explicitly from application
 * code. After that is done, the default FreeRTOS exception handler that will
 * have been installed can be replaced for any specific exception cause by using
 * the standard Xilinx library function microblaze_register_exception_handler().
 *
 * If vPortExceptionsInstallHandlers() is not called explicitly by the
 * application, it will be called automatically by the RTOS kernel the first time
 * xPortInstallInterruptHandler() is called. At that time, any exception
 * handlers that may have already been installed will be replaced.
 *
 * See the description of vApplicationExceptionRegisterDump() for information
 * on the processing performed by the FreeRTOS exception handler.
 */
void vPortExceptionsInstallHandlers( void );

/*
 * The FreeRTOS exception handler fills an xPortRegisterDump structure (defined
 * in portmacro.h) with the MicroBlaze context, as it was at the time the
 * exception occurred. The exception handler then calls
 * vApplicationExceptionRegisterDump(), passing in a reference to the completed
 * xPortRegisterDump structure as its parameter.
 *
 * The FreeRTOS kernel provides its own implementation of
 * vApplicationExceptionRegisterDump(), but the RTOS kernel provided implementation
 * is declared as being 'weak'. The weak definition allows the application
 * writer to provide their own implementation, should they wish to use the
 * register dump information. For example, an implementation could be provided
 * that writes the register dump data to a display, or a UART port.
 */
void vApplicationExceptionRegisterDump( xPortRegisterDump *xRegisterDump );

```

### RTOS 移植特定配置

RTOS 内核和演示行为可使用
文件 FreeRTOS/Demo/MicroBlaze_Kintex7_EthernetLite/RTOSDemo/src/FreeRTOSConfig.h中包含的配置常量进行自定义。
这些配置常量大多数用于所有 FreeRTOS 移植，
并在本网站的[自定义](/Documentation/02-Kernel/03-Supported-devices/02-Customization)页面
和 [FreeRTOS 参考手册](/Documentation/02-Kernel/06-Books-and-manual/01-RTOS_book)中进行了介绍。

以下常量特定于此移植：

```c

/* If configINSTALL_EXCEPTION_HANDLERS is set to 1, then the RTOS kernel will
automatically install its own exception handlers before the RTOS kernel is started,
if the application writer has not already caused them to be installed using the
vPortExceptionsInstallHandlers() API function. vPortExceptionsInstallHandlers()
is described on this web page. */
#define configINSTALL_EXCEPTION_HANDLERS 1

/* configINTERRUPT_CONTROLLER_TO_USE must be set to the ID of the interrupt
controller that is going to be used directly by FreeRTOS itself. Most hardware
designs will only include on interrupt controller, so can use the same setting
as shown here. XPAR_INTC_SINGLE_DEVICE_ID is itself defined in the xparameters.h
header file, which is part of the Xilinx BSP library project. */
#define configINTERRUPT_CONTROLLER_TO_USE XPAR_INTC_SINGLE_DEVICE_ID

```
