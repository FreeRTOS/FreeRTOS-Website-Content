---
title: "Philips LPC2106 (ARM7) RTOS 移植"
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
| <br /><br />![olimex.gif](/media/2018/olimex.gif)<br /> |

目前，基于 Philips LPC2000 ARM7 的嵌入式微控制器包含四个 FreeRTOS 移植，本页
仅涉及 GCC 移植。此演示同时支持 ARM 和 THUMB 模式。

此移植使用 LPC-P2106 低成本原型板进行开发
（如果希望使用其他开发板，可参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)），并使用开源
[GNUARM 开发工具](http://www.gnuarm.com/)（编译器和调试器）。

FreeRTOS 下载包括一个全面的 ARM7 RTOS 移植演示应用程序，可创建并执行 32 个实时任务；
还包括两个单独的[嵌入式以太网 TCP/IP Web 服务器示例应用程序](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)。

---

### 重要！关于使用 [LPC2106](http://www.semiconductors.philips.com/pip/LPC2106BBD48.html) RTOS 移植的注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

LPC2106 GCC 演示应用程序 makefile 位于 FreeRTOS/Demo/ARM7_LPC2106_GCC 目录中。

目录 FreeRTOS/Demo/ARM7_LPC2106_GCC/Serial 中包含中断驱动的串行端口驱动程序示例。

---

### 演示应用程序

FreeRTOS 源代码下载包含用于 LPC2000 GCC RTOS 移植的完全抢占式多任务演示应用程序。

#### ARM、THUMB、ROM 和 RAM 构建

以下批处理文件可用于构建演示应用程序。这些批处理文件可在调用 make 之前
设置相关构建所需的环境变量。

* ROM_ARM.bat：创建适合闪存编程的 ARM 模式发布版本。
* RAM_ARM.bat：创建适合在 RAM 执行的 ARM 模式调试版本。
* ROM_THUMB.bat：创建适合闪存编程的 THUMB 模式发布版本。
* RAM_THUMB.bat：创建适合在 RAM执行的 THUMB 模式调试版本。

这些批处理文件位于 Demo/ARM7_LPC2106_GCC 目录中。要切换批处理文件，
需要进行完整的重建。要强制进行完整的重建，请使用 touch 命令更新 makefile。

#### RTOS 演示应用程序硬件设置

演示应用程序包括 ComTest 任务，其中一个任务会向另一个任务传输 RS232 字符。要正确执行此实时任务，
必须将环回连接器安装到原型板的 RS232 端口
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

有三个 "flash"（闪烁）实时任务，假定 LED 安装到引脚 P0.10、P0.11 和 P0.12。忽略这些 LED
不会导致 RTOS 演示应用程序失败，但会移除一些表明一切都按预期运行的视觉反馈。
此外，ComTest Tx 任务发送的每个字符都会切换引脚 P0.13。

并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。
因此，系统创建了一个 "check"（检查）任务，用于确保所有其他任务中没有检测到任何错误。
板载 LED 由检查 "check" 任务控制，用于指示 RTOS 演示应用程序的状态。
如果所有实时任务都按预期执行并且没有发生错误，
则此 LED 将每 3 秒切换一次。如果切换速率增加到 500 毫秒，
则表示至少有一个任务发生错误。可通过移除环回连接器故意创建一个错误，
来测试此机制。

有关 RTOS 演示应用程序任务的更多信息，请参阅本网站的演示应用程序部分。

#### 构建和执行 RTOS 演示应用程序 - 单独运行于闪存

RTOS 演示应用程序在闪存和 RAM 都能执行。本节介绍如何创建
发布版本并将其写入 LPC2106 闪存。假设 [GNUARM 和 UNXUTILS 开发工具](#win32-gnu-开发工具)
已正确安装并包含在 PATH 中（以便在 Windows DOS 提示符中可用）。

*要构建应用程序*：

1. 打开 DOS 提示符，并转到 Demo/ARM7_LPC2106_GCC 目录。
2. 输入 "rom_arm"（或 "rom_thumb"），执行 rom_arm.bat 批处理文件。批处理文件会为发布版本设置必要的环境变量，然后
 调用 *make*。在构建过程中不应报错或出现警告。

*要准备原型板供下载*：

1. 断开原型板的电源。
2. 安装 BSL 跳线（因此 BSL 短路）。跳线使内置于 LPC2106 中的引导加载程序
 等待 RS232 端口上的连接。
3. 使用 RS232 电缆将原型板连接到主机。
4. 接通原型板的电源。

*要将 RTOS 演示下载到闪存*：

1. [从 Philips 下载并安装闪存编程实用程序](http://www.semiconductors.philips.com/files/products/standard/microcontrollers/utilities/lpc2000_flash_utility.zip)。
2. 运行并配置闪存编程实用程序，如下所示：
	1. 将 "Device" 设置为 LPC2106。
	2. 将 "XTAL frequenc" 设置为 14746KHz。
	3. 将 "COM port" 设置为主机的正确端口。
	4. 确保未勾选 "Use DTS/CTS" 复选框。
 引导加载程序将自动检测所使用的波特率，因此无需精确设置波特率，
 但不要设置得太高。
3. 选择 "Buffer" 菜单上的 "Flash Buffer Operations" 菜单项。此时会打开一个新的窗口。
4. 在新窗口中：
	1. 使用 "Load Hex File" 按钮加载从构建生成的十六进制文件。该文件名为 rtosdemo.hex，
	 位于 Demo/ARM7_LPC2106_GCC 目录。
	2. 单击 "Vector Calc" 按钮。此操作会更改矢量表中的一个条目，以确保引导加载程序
	 确认存在有效的程序。
	3. 最后，点击 "Upload To Flash"。
 此时会出现一条提示，要求重置原型板，但如果引导加载程序已经在等待连接，
 则可能不需要重置原型板。编程实用程序连接到原型板后，
 需保持连接状态。这意味着，如果重置原型板，然后尝试再次对其进行编程，
 编程实用程序将提示无法与目标通信。如果发生这种情况，只需确认错误，然后重复此步骤。

*要在编程后运行 RTOS 演示应用程序*：

1. 断开原型板的电源。
2. 从原型板上取下 RS232 电缆，并将其替换为环回连接器。
3. 移除 BSL 跳线，这样引导加载程序就不会等待 RS232 端口上的连接。
4. 接通电源。

#### 构建和执行演示应用程序——通过 JTAG 调试

本节介绍了如何使用
低成本 WIGGLER 兼容 JTAG 接口的调试器。调试器和 JTAG WIGGLER 之间的接口使用名为 OCDLibRemote 的实用程序。
同样，
假定 [GNUARM 和 UNXUTILS 开发工具](#win32-gnu-开发工具)已正确安装
并包含在 PATH 中（以便在 Windows DOS 提示符中可用）。

*要构建应用程序*：

1. 打开 DOS 提示符，并转到 Demo/ARM7_LPC2106_GCC 目录。
2. 输入 "ram_arm"（或 "ram_thumb"），执行 ram_arm.bat 批处理文件。批处理文件会为调试构建设置必要的环境变量，然后
 调用 *make*。在构建过程中不应报错或出现警告。

*要准备原型板以供调试*：

1. 移除 BSL 跳线。
2. 安装 JTAG 跳线。
3. 将 JTAG WIGGLER 连接到原型板上的 JTAG 端口和主机上的并行端口之间。

*要设置 OCDLibRemote*：

1. 下载并安装 OCDLibRemote，相关链接  见[此页面
 ](http://www.macraigor.com/full_gnu.htm)。
2. 使用 DOS 提示符中的命令 "OCDLibRemote --cpu ARM7 --device WIGGLER 1" 启动 OCDLibRemote。
 可能需要重复几次启动 OCDLibRemote 的命令，
 才能 JTAG WIGGLER 建立连接。

*使用调试器*：

1. 打开另一个 DOS 提示符，并转到 Demo/ARM7_LPC2106_GCC 目录。
2. 使用命令 "arm-elf-insight rtosdemo.elf" 启动图形调试器。
3. 配置调试器：
	1. 从 "File" 菜单中选择 "Target Settings" 菜单选项。此时会打开一个新的窗口。
	2. 使用 "Target" 下拉列表选择 GDBServer/TCP。在此示例中，OCDLibRemote 充当 GDB 服务器。
	3. 将 "Hostname" 设置为 "localhost"。
	4. 将 "Port" 设置为 "8888" - OCDLibRemote 的默认值。
	5. 确保选中 "Breakpoint at 'main'" 复选框。
4. 通过以下方式将代码下载到原型板 [这些步骤可以自动执行，
 但建议第一次独立执行，以便熟悉该流程]：
	1. 从 "Run" 菜单中选择 "Connect To Target" 菜单项。系统会发送一条消息，
	 确认已与 OCDLibRemote 建立连接。
	2. 从 "Run" 菜单中选择 "Download" 菜单项。系统会显示一个蓝色的状态栏，
	 指示下载进度。下载后，程序将一直执行到 main 中的断点。
5. 要执行程序，请单击 "Continue" 速度按钮。

**提示：**调试器运行良好，而 "Registers" 菜单项出现错误。要查看寄存器内容，
请打开控制台 (CTRL+N)，然后在控制台中键入 "info registers"。

### 配置和用法详情

#### Win32 GNU 开发工具

预构建的 GNU ARM7 开发工具可以从多个位置获取。
我在 Windows 2000 主机上使用从 [http://www.gnuarm.com](http://www.gnuarm.com/) 获取的开发工具。二进制
发行版包括便捷安装程序。安装程序会安装所需的一切。一些 GNU 开发工具
的发行版需要单独安装 Cygwin，相比之下不太方便。

此外，还需要 *GNU make* 兼容实用程序，我使用的是 [UNXUTILS](http://unxutils.sourceforge.net/) 版本。

#### RTOS 移植特定配置

此移植的特定配置项位于 Source/Demo/ARM7_LPC2106_GCC/FreeRTOSConfig.h 中。可编辑此文件中定义的常量，
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS 滴答的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

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

要编写可以引起上下文切换的中断服务程序：

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

请参阅 Demo/ARM7_LPC2106_GCC/serial/serial.c 中定义的 vUART_ISR()，获取完整示例。

#### 使用 LPC2106 以外的部件

LPC2106 使用标准 ARM7 内核，并配备处理器特定外围设备。核心实时内核组件应该
能够在所有 ARM7 设备上移植，但需要考虑外围设备的设置和内存要求。注意事项：
* Source/portable/GCC/ARM7_LPC2000/port.c 中的 prvSetupTimerInterrupt() 可用于配置 LPC2106 定时器 0以生成 RTOS 滴答。
* 端口、内存访问和系统时钟由 Demo/ARM7_LPC2106_GCC/main.c 中的 prvSetupHardware() 配置。
* 中断服务程序设置和管理假设存在矢量中断控制器。
* 串口驱动程序。
* 文件 lpc210x.h 提供了寄存器位置定义，该文件位于 Demo/ARM7_LPC2106_GCC/FreeRTOSConfig.h 的顶部。
* 启动代码、内存映射和矢量表设置位于 Demo/ARM7_LPC2106_GCC/boot.s。
* RAM 大小：参见下文“内存分配”部分。

#### 在抢占式和协作式 RTOS 内核之间切换

将 Demo/ARM7_LPC2106_GCC/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式内核；
设置为 0，可使用协同式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序生成文件构建应用程序。

#### 执行上下文

RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意：
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。

中断服务程序总是在 ARM 模式下运行。其他所有代码将运行在 ARM 或 THUMB 模式，这取决于构建。
应该注意的是，portmacro.h 中定义的一些宏只能从 ARM 模式代码调用，而且如果从 THUMB 代码
调用会导致编译时错误。

Demo/ARM7_LPC2106_GCC/boot.s 仅为系统/用户、IRQ 和 SWI 模式配置堆栈。

SWI 指令由实时内核使用，因此应用程序代码不能使用。

#### 内存分配

LPC2000 演示应用程序生成文件包含 Source/Portable/MemMang/heap_2.c，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。

#### Linux 用户注意事项：

我仅使用 GNUARM 开发工具的 Win32 版本测试了生成文件。
