---
title: "Xilinx使用XilinxISE Design Suite（嵌入式版）在 Spartan-6 FPGA 上演示的 MicroBlaze 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Xilinx Spartan 6 SP605 开发板](/media/2018/Xilinx-Spartan-6-SP605-development-board.jpg)

**本页记录的演示已过时，
 已由[使用更高硬件和工具版本的演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#XILINX)所取代。**

该 MicroBlaze 移植是使用 13.1 版
[Xilinx ISE 设计套件（嵌入式版）](http://www.xilinx.com/products/design-tools/ise-design-suite/)制作的，
支持 8.10 版本的[MicroBlaze 软核处理器](http://www.xilinx.com/tools/microblaze.htm)，
并在基于 Spartan-6 FPGA  的
[SP605 评估工具套件](http://www.xilinx.com/products/boards-and-kits/EK-S6-SP605-G.htm)上开发和测试。
它代表了 FreeRTOS 移植的一次重大升级，
并取代了[先前存在、在 Virtex-4 FPGA 上开发的旧移植](portmicroblaze)
。

该演示包括一个使用 1.4.0 版[lwIP TCP/IP堆栈](http://savannah.nongnu.org/projects/lwip/)的嵌入式 Web 服务器实现。
Web 服务器的服务器端包含 (SSI) 功能用于
为包含动态任务和运行时统计信息的页面提供服务。

在 Xilinx SDK 环境中使用 FreeRTOS 有两种方式：

1. 使用独立的 BSP

 独立的板级支持包 (BSP) 是由 SDK生成的
 特定于硬件设计（FPGA 配置）。该库
 包含 MicroBlaze 软核处理器本身的软件驱动程序以及设计中包含的
 所有外设，但它无法识别FreeRTOS。
 FreeRTOS 可以通过构建 FreeRTOS 源文件
 作为引用 BSP 库的应用程序的一部分，与独立的 BSP 一起使用。此
 页面上描述的演示应用程序就是使用的这种方式。
2. 使用 FreeRTOS BSP

 FreeRTOS BSP 扩展了上述独立的 BSP，纳入了
 FreeRTOS 源文件。FreeRTOS 可以与 FreeRTOS BSP 一起使用，
 而无需将 FreeRTOS 源文件作为引用 BSP 库的
 应用程序的一部分。本页所描述的演示程序
 并没有使用 FreeRTOS BSP，
 [另行提供一个
 文档页面，](Integrating-FreeRTOS-Library-and-Project-Creation-into-the-Xilinx-SDK)描述如何FreeRTOS生成和使用  BSP，
 以及 SDK 如何自动生成一个完整（但简单）的 FreeRTOS
 使用FreeRTOS BSP 库的应用程序。

![在 FreeRTOS SDK Xilinx ](/media/2018/Creating-FreeRTOS-BSP-packages-and-applications-in-the-Xilinx-SDK.jpg中创建)BSP 包和应用程序

 使用 Xilinx SDK 创建一个 Hello World 样式的 FreeRTOS 应用程序，
 该应用程序使用 FreeRTOS BSP

最后，[FreeRTOS Eclipse 内核感知调试器插件](http://www.highintegritysystems.com/down-loads/stateviewer-plug-in/)
可与 XilinxSDK 一起使用，以协助调试 FreeRTOS 应用。

![FreeRTOS Eclipse RTOS内核感知调试器插件](/media/2018/FreeRTOS-kernel-aware-debugger-plug-in-viewed-in-the-Xilinx-SDK.jpg)

 在FreeRTOS SDK 中查看 Xilinx 内核感知调试器插件

---

### 重要提示！Microblaze 软核处理器RTOS移植使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

- [\[RTOS 移植\]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)
    - [重要提示！Microblaze 软核处理器移植使用说明RTOS](#重要提示microblaze-软核处理器rtos移植使用说明)
  - [源代码组织](#源代码组织)
    - [准备Xilinx软件开发工具包（SDK）项目目录](#准备-xilinx-软件开发工具包-sdk-项目目录)
  - [MicroBlaze 演示应用程序](#microblaze-演示应用程序)
    - [功能](#功能)
    - [硬件设置](#硬件设置)
    - [网络设置](#网络设置)
    - [将演示应用程序项目导入 SDK Eclipse 工作区](#将演示应用程序项目导入-sdk-eclipse-工作区)
    - [构建演示应用程序](#构建演示应用程序)
    - [使用 SDK 工具运行演示应用程序](#使用-sdk-工具运行演示应用程序)
    - [预期行为](#预期行为)
    - [Web 服务器的使用](#web-服务器的使用)
    - [提供的网页](#提供的网页)
  - [FreeRTOS 内核配置和使用详细信息](#freertos-内核配置和使用详细信息)
    - [应用程序须提供的回调函数](#应用程序须提供的回调函数)
    - [实现中断服务程序 (ISR)](#实现中断服务程序-isr)
    - [ISR 的切换上下文](#isr-的切换上下文)
    - [安装并启用 ISR](#安装并启用-isr)
    - [异常处理（仅适用于高级用户）](#异常处理仅适用于高级用户)
    - [RTOS 移植特定配置](#rtos-移植特定配置)
    - [内存分配](#内存分配)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码及
演示应用程序。这意味着它包含的文件数量比
使用 MicroBlaze 移植或官方 MicroBlaze 演示应用程序所需的文件多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
获取关于已下载文件的说明
和新项目创建的信息。

演示应用程序使用的目录结构如下所示
。MicroBlaze_Spartan-6_EthernetLite 根目录本身
位于 FreeRTOS/{'/'}Demo 中。

```c

MicroBlaze_Spartan-6_EthernetLite
    |
    +-KernelAwareBSPRepository   File repository used to integrate FreeRTOS into the SDK
    |
    +-PlatformStudioProject      The XPS project used to create the hardware bitstream
    |
    +-SDKProjects                The various SDK projects
        |
        +-RTOSDemo                   The demo application project itself
        |
        +-StandAloneBSP              The BSP library code
        |
        +-HardwareWithEthernetLite   The hardware project


```

与目录结构体有关的注意事项：

* 用于构建演示应用程序的 SDK 项目存储在
 SDKProjects/RTOSDemo 目录中。这是为了生存生成演示项目可执行文件，
 唯一需要明确构建的项目。另外
 两个 SDK 项目（BSP 库和硬件项目）
 是 RTOSDemo 项目的附属项目，
 所以会在需要时自动构建。
* StandAloneBSP 库项目由 SDK
 专门为硬件配置创建。由于它是一个独立的库，
 所以它不包括 FreeRTOS 源文件，而 FreeRTOS 源文件
 则是作为 RTOSDemo 应用程序的一部分。
 [我们提供了一个单独的网页](Integrating-FreeRTOS-Library-and-Project-Creation-into-the-Xilinx-SDK)
 来介绍 FreeRTOS BSP的使用，它确实包括 FreeRTOS 源文件，
 因此不再需要将 FreeRTOS 文件
 直接包含在正在构建的应用程序中。
* 无需打开或修改 PlatformStudioProject 目录下包含的 XPS（硬件）项目，
 除非您特别想
 改变硬件配置。RTOSDemo SDK（软件）项目确实依赖于
 从硬件项目导出的文件，
 但导出过程已经完成，而且导出的文件已经存储在
 SDKProjects{'/'}HardwareWithEthernetLite 目录中。

### 准备 Xilinx 软件开发工具包 (SDK) 项目目录

Eclipse 项目既可以是标准 makefile 项目，也可以是托管 make 项目。
此演示应用程序中提供的项目是托管 make 项目。因此意味着
以下两种情况：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录下，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

本示例采用第一种。为此，FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/SDKProjects/RTOSDemo 目录
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件会将所有必需的 FreeRTOS 源文件复制到
演示项目目录内的子目录中。该批处理文件用于 Windows 主机。 Linux
用户将需要创建一份同等的脚本文件，或检查所提供的批处理文件，
以便随后手动执行相同的复制操作。
**CreateProjectDirectoryStructure.bat 必须在将 SDK
项目导入 Eclipse 工作区之前执行**。

---

### MicroBlaze 演示应用程序

### 功能

SDK 项目包含两项构建配置，一个称为 Blinky，
负责创建一个非常简单的入门示例，另一个称为 Full，
负责创建一个全面示例：

|  |  |
| --- | --- |
| **构建配置** | **描述** |
| <br /> Blinky<br />  | <br /> 该示例为**非常简单的入门示例**。此配置会创建两项任务，<br /> 一项为创建软件定时器，另一项为使用按钮中断。<br /> <br /> 两项任务通过队列进行通信，包括队列发送任务和<br /> 队列接收任务。队列接收任务<br /> 每次接收到值时都会切换一次 LED。<br /> <br /> 按下任何用户按钮（SW4、SW5、SW7 或 SW8）都会产生中断,<br /> 中断的服务例程在打开 LED 之前<br /> 会重置一个软件定时器。软件定时器的周期为 5 秒，<br /> 5 秒过后，软件定时器回调函数<br /> 会再次关闭 LED。因此，按下按钮将打开 LED ，<br /> 而且如果没有再次按下按钮，整个 5 秒钟内，<br /> LED 都会保持亮起状态。<br /> <br /> Blinky 构建配置使用<br /> main-blinky.c 源文件。<br /> <br /> |
| <br /> Full<br />  | <br /> 这是一个全面的演示，会创建许多任务、<br /> 队列、（各种类型的）信号量和软件定时器。该演示<br /> 还包括嵌入式 Web 服务器。<br /> <br /> Full 构建配置<br /> 从[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务集中创建了很多任务<br /> 。标准演示任务并不执行任何特定函数。<br /> 其目的首先是测试 FreeRTOS 移植，其次是<br /> 举例说明如何使用 FreeRTOS API 函数。<br /> <br /><br /> 由 Full 构建配置创建的其他任务包括：<br /> \*寄存器检查任务<br /> <br /> 这两项任务会测试 RTOS 内核上下文切换机制：<br /> 首先用一个已知的唯一值填充各个 MicroBlaze 寄存器，<br /> 然后重复检查写入寄存器的原始值<br /> 是否在整个任务周期内均保持在寄存器中。这些任务以尽可能低的优先级执行<br /> （空闲优先级），因此经常被抢占<br /> 。这些任务的性质决定了它们必须用汇编语言编写<br /> 。<br />\* “检查”软件定时器和回调<br /> <br /> 检查定时器是一种非常简单的监视定时器。它<br /> 会监视所有其他标准演示任务、寄存器检查任务<br /> 并使用 LED 为系统状态提供视觉反馈。<br /> <br /> 检查定时器的周期最初设置为 5 秒。<br /> 检查定时器回调函数会检查所有标准演示任务<br /> 及寄存器检查任务是否仍在执行，<br /> 而且执行时没有报告任何错误，然后会切换 LED。<br /> <br /> 如果检查定时器发现某项任务<br /> 已停顿，或报告了错误，则会自行将周期<br /> 从最初的 5 秒更改为仅 200 毫秒。因此，如果 LED<br /> 每 5 秒切换一次，则表明没有发现问题，然而，<br /> 如果 LED 每 200 毫秒切换一次，则表示至少有一项任务中<br /> 发现了一个问题。上次报告的问题会锁定到 pcStatusMessage<br /> 变量中。<br />* lwIP 任务<br /> <br /> lwIP 任务会执行 lwIP TCP/IP 堆栈，并执行嵌入式<br /> Web 服务器。使用嵌入式 Web 服务器所需的网络配置，<br /> 请参阅本页面的[网络设置](#网络设置)章节。<br /> 本页面的<br /> [预期行为章](#预期行为) 节描述了由嵌入式 Web 服务器服务的页面。<br /><br /><br /> |

### 硬件设置

演示应用程序包含通 UART 发送和接收字符的任务。
一个任务发送的字符必须由另一个任务接收。如果任何字符丢失或接收顺序错误，
则会标记错误情况。

有两种常见方法
可以确保所发送的每个字符均能被收到。第一种是
使用环回连接器，将发送引脚链接到接收引脚。第二种是
将 UART 连接到回显服务器。SP605 硬件使用 UART 到 USB
转换器，因而无法安装环回连接器。因此，
在这种情况下，UART 必须连接到外部回显服务器。在开发过程中，
可使用免费 (Windows) Comm Echo 实用程序实现此目的。Comm Echo
可从 [http://www.serialporttool.com/CommEcho.htm](http://www.serialporttool.com/CommEcho.htm)下载。

下一节描述了所需的网络设置。

此演示应用程序使用内置于 SP605 硬件的 LED 和按钮，
因此无需其他硬件设置。

### 网络设置

分配给 SP605 硬件的 IP 地址
由 configIP_ADDR0 到 configIP_ADDR3 之间的常量进行设置。这些常量
位于 FreeRTOSConfig.h 标头文件（位于 FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/SDKProjects/RTOSDemo 目录中）底部。
定义 MAC 地址和网络掩码的常量位于同一
文件的同一位置。

Web 浏览器和 SP605 硬件使用的 IP 地址必须
兼容。为此，可以将二者 IP 地址中的前三个八进制数
设置成相同的值。例如，如果运行 Web 浏览器的计算机所用 IP 地址是
192.168.0.1，则可以为 SP605 开发板指定
192.168.0.2 到 192.168.0.254 范围内的任何地址
（同一网络上已经存在的地址除外）。

分配给 SP605 的 MAC 地址
在其所连接的网络上必须具有唯一性。

### 将演示应用程序项目导入 SDK Eclipse 工作区

要将 Xilinx 软件开发套件 (SDK) 项目导入现有或全新 Eclipse 工作区，请执行以下操作：
1. 从 SDK 的 "File" 菜单中选择 "Import"。将出现如下所示的
 对话框。如图所示，选择 "General->Existing Project into Workspace"。

![将 Xilinx MicroBlaze RTOS 演示项目导入 SDK](/media/2018/Importing-the-Xilinx-MicroBlaze-RTOS-demo-project-into-the-SDK.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/SDKProjects
 作为根目录。然后，确保 RTOSDemo、StandAloneBSP 和 HardwareWithEthernetLite
 项目复选框在 “Projects” 区勾选，**并确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图，查看正确的复选框状态）。

![在  SDK 导入过程中选择RTOS演示源项目](/media/2018/Selecting-the-RTOS-Demo-Source-project-during-the-SDK-import-process.jpg)

**确保已勾选 "RTOSDemo"，且未勾选 "Copy projects into workspace"**
3. 导入全部三个项目后， SDK IDE 的项目资源管理器窗口
 将如下图所示。

 请记住，只有 RTOSDemo 项目需要明确构建，
 用于生成硬件项目的 XPS 项目也在
 FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/PlatformStudioProject 目录下提供。

![在 项目资源管理器窗口中查看的 RTOS演示和两个附属项目](/media/2018/The-RTOSDemo-and-two-dependent-projects-viewed-in-the-project-explorer-window.jpg)

**导入工作区的全部三个项目**

### 构建演示应用程序

1. 确保 CreateProjectDirectoryStructure.bat 已执行，
 并确保项目已正确导入到 Eclipse 工作区。
2. 选择所需的构建配置。要选择活动的构建配置（实际将被构建的构建配置），
 首先在 SDK IDE 的 Project Explorer 窗口中右击 RTOSDemo 项目名称，
 然后选择所需的弹出菜单项，如下图所示
 。

![在 XilinxSDK IDE](/media/2018/selecting-a-build-configuration-in-the-Xilinx-sdk-ide.jpg)中选择构建配置

**使用 Xilinx SDK IDE**中的弹出菜单选择活动的构建配置

**注意：**
 这两种构建配置在各自的构建中都包括和排除了不同的文件
 。例如，Full 构建配置构建了
 main-full.c，而 Blinky 构建配置则构建勒 main-blinky.c。
 Eclipse Project Explorer 窗口应该显示一个带十字的图标，
 以表明哪些文件被排除在活动构建配置之外。
 但是，此特定功能似乎无法正常使用。
 改变构建配置将确保构建正确的文件，
 排除正确的文件，
 但 Project Explorer 窗口不一定会正确更新其图标。
3. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。应用程序应
 两个项目应能成功构建，没有任何错误或警告。StandAloneBSP 项目也将被构建，
 因为它是 RTOSDemo 项目的一个依赖项。

### 使用 SDK 工具运行演示应用程序

1. 确保 SP605 硬件已通电，
 且其 JTAG 端口与主机相连。
2. 在下载软件项目之前，
 需用 SDK 硬件项目的比特流对 Spartan-6 FPGA 进行编程。要将
 比特流编程到 FPGA 中，首先需从 SDK IDE 的 “Xilinx Tools” 菜单中选择 “Program FPGA”，
 然后在 Program FPGA 对话框中选择 SDKProjects/HardwareWithEthernetLite 目录中的 .bit 和 .bmm 文件
 。如下图所示。

![将比特流编程到 Spartan-6 FPGA 中](/media/2018/Programming-the-bitstream-into-the-Spartan-6-FPGA.jpg)

**用于对 FPGA 进行编程的对话框**
3. 在对 FPGA 进行编程后，从 IDE “Run” 菜单中选择 “Debug Configurations...”。
4. 在出现的对话框中，在左侧的目标树中突出显示 "Xilinx C/C++ ELF"，
 然后点击
 "New Launch Configuration" 加速按钮。加速按钮
 在下图中以红色正方形突出显示。
5. 此时将创建一个新的调试配置，该配置的名称
 与正在使用的构建配置相匹配。自动生成的名称
 在下图中以黄色矩形突出显示。
6. 确保使用正确的应用程序文件——Blinky/RTOSDemo.elf
 用于 Blinky 构建配置，Full/RTOSDemo.elf 用于 Full 构建配置。
 应用程序文件条目在下图中由绿色矩形突出显示
 。
7. 单击 "Debug" 按钮开始调试。

![在 XilinxSDK IDE](/media/2018/Creating-an-Eclipse-debug-build-configuration-in-the-Xilinx-SDK-IDE.jpg)中创建 Eclipse 调试构建配置

**创建调试配置**

 Blinky 和 Full 构建配置需要单独的调试配置，
 并且每次启动新的调试会话时，
 必须注意选择正确的调试配置。

### 预期行为

Full 构建配置的行为如下：

* 标记为 DS4、DS5 和 DS6 的 LED 由标准演示控制
 “flash” 任务控制。每个 LED 都将以固定频率切换，其中 LED DS6
 的频率最快，LED DS4 的频率最慢。
* 标记为 DS3 的 LED 处于“检查”软件定时器的控制之下。
 如果没有报错，DS3 将每 3 秒切换一次，
 如果标准演示任务报错，则每 200 毫秒切换一次
 。可以通过关闭 comm echo 服务器
 或拔掉 UART 电缆来测试该机制，
 这样做是为了故意使 comm 测试任务失败。
* 下一节将介绍嵌入式 Web 服务器的行为。

Blinky 构建配置的行为如下：

* 标记为 DS6 的 LED 处于队列接收任务的控制之下。每次
 队列接收任务收到一个值，它都将按照
 200 毫秒一次的频率切换。
* 按下任何用户按钮 SW4、SW5、SW8 或 SW9 时，标有 DS5 的 LED 将亮起
 （假设尚未亮起）。在最后一次按下其中一个按钮 5 秒后，
 LED 软件定时器
 将再次关闭 LED DS5。

### Web 服务器的使用

提供的每个页面顶部都有一个菜单，内含指向其他各页面的链接。

1. 在连接的计算机上打开浏览器。
2. 先在浏览器地址栏中输入 "HTTP://"，再输入目标 IP 地址。

![](/media/2018/enterurl.gif)
在 web 浏览器中输入 IP 地址
（当然，根据您的系统，使用正确的 IP 地址）

### 提供的网页

![由 Spartan 6 FPGA 上的 lwIP 嵌入式 Web 服务器提供的任务统计页面](/media/2018/task-stats-page-served-by-the-lwIP-embedded-web-server-on-the-Spartan-6-FPGA.jpg)

 提供的任务统计页面 - 显示
系统中运行的每项任务的状态 - 包括
任务堆栈高水位线时使用的类型。

![由 Xilinx SP605 上的 lwIP 嵌入式 Web 服务器提供的任务运行时间统计信息页面](/media/2018/task-run-time-stats-page-served-by-the-lwIP-embedded-web-server-on-the-Xilinx-SP605.jpg)

 所提供的 [运行时间统计](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics) 页面 - 显示
每项任务消耗的 CPU 时间量

所提供的第三个页面显示一张大 JPG 图像。

---

### FreeRTOS 内核配置和使用详细信息

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
 包括在 main-full.c 和 main-blinky.c 中的 vApplicationSetupTimerInterrupt() 示例实现。
 示例实现使用 AXI 定时器 0
 作为滴答中断源。如果您的硬件平台
 包含 AXI 定时器 0 外围设备，
 则无需修改即可使用示例实现。
* void vApplicationClearTimerInterrupt( void );

 这是应用程序定义的回调函数，用于清除
 vApplicationSetupTimerInterrupt() 回调函数安装的任何
 中断。它是
 该函数作为应用程序回调，因为 RTOS 内核
 将在许多不同的 MicroBlaze 和 FPGA 配置上运行，
 并非所有配置都定义或提供相同的定时器外围设备。

 官方演示应用程序
 包括在 main-full.c 和 main-blinky.c 中的 vApplicationClearTimerInterrupt() 示例实现。
 该示例实现补充了相同文件中
 的 vApplicationSetupTimerInterrupt() 示例实现，
 方法是：清除由 AXI 定时器 0 外围设备生成的中断。
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
vApplicationSetupTimerInterrupt() 的实现中，该实现位于 main-full.c
和 main-blinky.c 中。另一个示例包含在
main-blinky.c 中 prvSetupHardware() 的实现中。

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
 * four possible interrupt sources:
 *
 * XPAR_INTC_0_UARTLITE_1_VEC_ID - for the UARTlite peripheral.
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the AXI Timer 0 peripheral.
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet lite peripheral.
 * XPAR_INTC_0_GPIO_1_VEC_ID - for the button inputs.
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
 * the four possible interrupt sources:
 *
 * XPAR_INTC_0_UARTLITE_1_VEC_ID - for the UARTlite peripheral.
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the AXI Timer 0 peripheral.
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet lite peripheral.
 * XPAR_INTC_0_GPIO_1_VEC_ID - for the button inputs.
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
 * the four possible interrupt sources:
 *
 * XPAR_INTC_0_UARTLITE_1_VEC_ID - for the UARTlite peripheral.
 * XPAR_INTC_0_TMRCTR_0_VEC_ID - for the AXI Timer 0 peripheral.
 * XPAR_INTC_0_EMACLITE_0_VEC_ID - for the Ethernet lite peripheral.
 * XPAR_INTC_0_GPIO_1_VEC_ID - for the button inputs.
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
FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/SDKProjects/RTOSDemo/FreeRTOSConfig.h 文件中包含的配置常量进行定制。
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

### 内存分配

Source/Portable/MemMang/heap_3.c 包含在 MicroBlaze 演示应用程序的 makefile 中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

heap_3.c 使用
从 RTOS 调度程序锁定区中调用的标准 malloc() 和 free() 函数，从而保证线程安全。总可用堆
大小设在位于
DemoMicroBlaze_Spartan-6_EthernetLiteSDKProjectsRTOSDemosrc
目录的链接器脚本的顶部。
