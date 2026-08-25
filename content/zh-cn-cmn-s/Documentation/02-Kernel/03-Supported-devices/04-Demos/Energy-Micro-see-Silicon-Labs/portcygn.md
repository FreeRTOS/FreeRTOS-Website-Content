---
title: "Cygnal (Silicon Labs) 8051 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![cygnal.jpg](/media/2018/cygnal.jpg)

该 Cygnal 移植是在 [C8051F120-TB](https://www.silabs.com/products/mcu/Pages/C8051F120DK.aspx) 原型板
（如果希望使用其他开发板，请参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）上开发的，
此原型板配有 [8051F120](https://www.silabs.com/products/mcu/mixed-signalmcu/Pages/C8051F12x3x.aspx) 微控制器。
所用编译器为免费版的 [SDCC](http://sdcc.sourceforge.net/)，配合 Cygnal IDE 一起使用。

附带的演示应用程序创建了 21 个实时任务，并使用连接到端口 3 的 LED 阵列来运行八个 'flash' 任务。

---

### 重要！8051 RTOS 移植使用说明

*使用此移植前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

SDCC makefile 和 Cygnal IDE 项目文件位于 Demo/Cygnal 目录中。

---

### 演示应用程序

FreeRTOS 源代码下载文件包括一个用于 8051 SDCC RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3
连接在一起）。

标准的 8 LED "flash" 任务假设 LED 安装在端口 3 上。忽略这些 LED 不会导致 RTOS 演示应用程序
失败，但会删除一些视觉反馈，表明一切都按预期运行。

#### 构建并执行 RTOS 演示应用程序

1. 确保 [SDCC](http://sdcc.sourceforge.net/) 安装正确且在您的路径中。请参阅下文关于获取正确 SDCC 版本的说明。
2. 确保您的路径中还有 GNU *make* 兼容实用程序。我使用 [http://unxutils.sourceforge.net](http://unxutils.sourceforge.net) 版本。或者，您可以将生成文件转换为批处理文件。
3. 解压 FreeRTOS，然后在 DOS 窗口中移动到 Demo/Cygnal 目录并键入 "make"。成功的源文件构建应该不会报错或出现警告。
4. 使用 Cygnal JTAG 串行接口将原型板连接至您的主机，并接通电源。
5. **使用文本编辑器** - 打开 Cygnal IDE 项目文件（名为 sdcc.wsp，可在 Demo/Cygnal 目录中找到），
 并将所有文件路径名替换为正确的 FreeRTOS 安装路径。要找到所有
 需要改变的地方，请搜索 "E:devFreeRTOS" 字符串——这是 FreeRTOS 在我的主机上的安装位置。
6. 启动 Cygnal IDE，然后从 "Project" 菜单中选择 "Open Project"，然后打开 “sdcc.wsp” ，其中将包含系统的正确路径。
7. IDE 将连接到原型板。下载从构建过程中创建的 OMF 文件，该文件名为 “main” ，没有扩展名。

下载 OMF 文件后，您应能使用 JTAG 调试器运行/停止应用程序，并检查所有的内存和
寄存器。如果您遇到任何问题，请检查 "Tool Vendor" 是否设置为 Dunfield。此选项可通过 "Project | Tool Chain Integration" 菜单访问。

使用批处理文件代替生成文件允许在 IDE 内执行构建，但我更喜欢将其分开。

#### 演示应用程序功能

RTOS 演示应用程序创建了 21 个标准  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务：
* 端口 3 上的 8 个 LED 灯处于标准 'flash' 任务的控制之下。它们以
 标准  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分所描述的模式进行闪烁。
* 并非所有任务都会更新 LED 的状态，所以没有可见的指示表明它们运行正常。
 因此，要创建了一个 "Check" 任务，确保在其他任务中没有检测到错误。
 内置的绿色 LED 由 'check' 任务控制。每 5 秒切换一次的绿色 LED 表示
 所有演示应用程序任务都运行无误。如果切换速度增加到 500 毫秒，则表示
 至少在一个标准演示应用程序任务中检测到错误。可以通过移除环回连接器故意创建一个错误，用来测试此机制
 。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项位于 Demo/Cygnal/FreeRTOSConfig.h 中。可以编辑此文件中定义的常量，
以适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。所提供的值 1000 Hz 可用于测试 RTOS 内核功能，但其比大多数应用程序的频率都要高。
降低此值可提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。此移植将
BaseType_t 定义为 char 类型。

#### 在抢占式和协作式 RTOS 内核之间切换

将 Demo/Cygnal/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 ，即可使用抢占式内核，将其设置为 0 即可使用
协作式内核。

#### 开发工具选项

与所有的移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序生成文件构建应用程序。

#### 堆栈启动常量

DEMO/CYGNAL/FreeRTOSConfig.h 包含定义 'configSTACK_START'。它已被正确定义以适用于
演示应用程序，但如果您的应用程序声明任何变量符合“数据”关键字，则需要更新。

正确的 configSTACK_START 值可以从 SDCC 在构建过程中输出的 .mem 文件获取。
例如，如果 .mem 文件
包含该行，

```c
"Stack starts at: 0x0e (sp set to 0x0d) with 242 bytes available"
```

则 configSTACK_START
应设置为 0x0e。

#### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 Cygnal 演示应用程序生成文件中，用于提供
实时内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
以获取完整信息。

#### 编译器、头文件和库版本

SDCC 是一个多功能编译器，仍在开发中。
SDCC 2.4.0 版本不支持 RTOS 移植所需的所有寻址模式。应使用最新的稳定快照，
相关快照可从上面给出的 SDCC 链接获取。此移植已使用 2004 年 5 月 4 日的快照测试过。

为支持新的编译器版本，还需更新过的 c8051f120.h 头文件。此头文件**包含**在 FreeRTOS 发行版中，
并位于 Demo/Cygnal 目录中。请千万**不要**使用 2004 年 5 月版 Cygnal 工具提供的 SDCC 版本 ，不过
您可以使用之后的 SDCC 版本。

下载 SDCC 时所提供的库没有被构建为可重入，但如果与 RTOS 一起使用，那这些库必须具有可重入性（这包括
执行 16 位文件、32 位文件和浮点操作的库）。重新构建这些库很容易，我已经这么做过，并在此页面提供我重新构建过的库
可点击此处查看相关文档。应将[此 zip](/media/2018/reentrant_lib.zip) 文件夹中的文件解压到 sdcc/lib/large 目录中。
请留意库源文件中的版权和许可注释， 并请注意 vprintf 库是**不可**
重入的。

#### 偏离标准 8051 架构

我已尽力将 Cygnal 特定代码从 RTOS 源代码中剔除。而 Cygnal 的大多数特定硬件
配置都在演示应用程序的 main.c 文件中执行。

RTOS 滴答中断由定时器 2 生成，这是 8052 兼容设备上的 16 位定时器，
但在标准的 8051 设备中不可用。

此堆栈有 256 个字节可用。

#### 速度和资源使用

每个实时任务都需要自己的堆栈，但 8051 架构只允许内部小 RAM 中存在一个堆栈。当任务被切换出时，
有必要将其整个堆栈从 RAM 复制到 XRAM，反之亦然（此过程对应用程序编写者/用户来说清晰易懂）
。Cygnal 微控制器速度对 8051 来说异常快，可以准确无误地处理此问题（演示
应用程序将系统时钟设置为 98MHz）。然而，
速度较慢的处理器在处理此问题时可能会有困难。演示应用程序的嘀嗒频率 1000Hz。如此高的频率是为进行测试而设置的，
如果您的应用程序允许，您可大幅度降低它的频率。

若有可能，尽量少用堆栈。

#### 优化

可以通过多种简单的方法调整 RTOS，使其适应 8051 架构，从而提高效率。这需要使用特殊的 SDCC/8051 关键字。提供的 RTOS 源
代码是可移植的，所以可以使用几种不同的开发工具套件对其进行编译 - 因此，我没有
在下载的发行版中包含任何特定的 8051 优化。

优化方法包括：

* 在 tasks.c 中的文件范围变量的声明中使用 'data' 限定符。这会将变量
保存在内部 RAM 中，从而可以更快地访问它们。
* 在其他相关地方使用“数据”限定符。
* 目前，任务上下文被推入堆栈，然后在检查是否有更高优先级任务准备运行*之前*将堆栈复制到 XRAM
 。这些操作步骤可以修改，这样上下文被推送至堆栈后，堆栈只有在必要的时候才会被复制到 XRAM
 。如果不需要进行上下文切换，则原始任务将从堆栈中弹出其上下文并继续运行。这样的更改会
 使得代码非常具有 8051 特色（这就是我为什么没有这么做的原因）。

#### 中断服务例程

如果 ISR 导致任务被解除阻塞，那么 ISR 可能希望返回被解除阻塞的任务而不是被中断的任务。
这可通过在 ISR 内部调用 taskYIELD() 来完成。完成此步骤后，必须将 ISR 代码放置在
临界区。请参阅 vSerialISR() Demo/Cygnal/serial/serial.c 代码获取完整示例，以下为大纲内容：

```c

void ISRRoutine( void )
{
    /* Routine within critical region. */
    portENTER_CRITICAL();

    .
    . ISR Code Here
    .

    /* Switch to another task if necessary. */
    taskYIELD();

    portEXIT_CRITICAL();
}
```

#### 包含的生成文件

要让 SDCC 将对象文件输出到一个允许生成文件正常运行的目录中，是很棘手的。我找到了执行此操作的机制，
但对语法不满意 - 我不是生成方面的专家，但我发现
指示 SDCC 覆盖 C 文件的命令行似乎效果最好！为了安全起见，我已经在文档中注释了该行。

因此，生成文件包含两组命令，可以通过生成文件中的注释/取消注释进行选择。
第一组命令就是我使用的命令，与 UnxUtils make 实用程序配合得非常好，
但为防出现其他系统问题，这组命令被注释掉。第二组命令（未注释）可成功构建项目，不会出现任何问题，
但即使只有一个源文件被更改，它都会重建整个项目。您可以选择使用哪组命令——查看生成文件中的注释
(可在 Demo/CYGNAL 目录中找到)以获取详细信息。

#### 串行端口波特率

RTOS 演示应用程序中包含的串行驱动程序使用 Cygnal 手册中详细描述的波特率计算。在某些波特率下，串行端口运行良好，
但在另一些波特率下则不然，需要将这些波特率稍作调整。串行端口环回测试并不在意波特率是否完全正确，
因为发送方和接收方使用相同的源。

此外还应注意的是，串行驱动程序是为测试一些实时内核功能而编写的 - 它们并不
用于表示优化过的解决方案。

#### SFR 分页

Cygnal 微控制器运行 SFR 分页方案。一些非 8051 标准的外设要求访问
外设控制寄存器之前选择并获取 SFR 分页。一旦启动 RTOS 调度器， 就只能从临界区访问 SFR 分页寄存器，
因为它不是作为任务上下文的一部分被存储的。如果此类外设被用作中断源，
则必须在 ISR 结束或调用 taskYIELD() 之前将 SFR 分页重置为其原始值。

#### Linux 用户

我只在 SDCC 的 Win32 版本中测试了该生成文件。

