---
title: "Texas Instruments MSP430 (MSP430F449) RTOS移植，适用于 MSPGCC (GCC) 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ES449.gif](/media/2018/ES449.gif)

该移植在 [ES449开发/原型开发板](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449)上开发
（来自 [SoftBaugh](http://www.softbaugh.com/)）上开发而成（如果您希望使用其他开发板，请参阅此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)），
使用免费[MSPGCC 开发工具链](http://mspgcc.sourceforge.net/)和 SoftBaugh
[FETP 并行端口 JTAG 接口](http://www.softbaugh.com/ProductPage.cfm?strPartNo=FETP)

ES449 是一款小巧的、基于 MSP430F449 的原型板，可用于轻松访问 MSP430 外设，随附
LCD 显示屏，非常适合调试！

还有一个适用于[基于 Olimex MSP430F149 的 EasyWEB2
开发板()http://www.olimex.com/dev/msp-easyweb2.html] 请参阅本页底部的“MSP430F149 EasyWeb2 移植”部分。

FreeRTOS V5.1.0 升级了此移植和演示，允许任务使用 MSP430 低功耗模式 1 至 3，要求中断服务程序使用
"wakeup" 关键字才能符合要求。演示应用程序中的 UART 驱动程序提供了一个示例。

---

### 重要提示！MSPGCC MSP430 RTOS 移植使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [安装编译器](#安装编译器工具链)
3. [演示应用程序](#演示应用程序)
4. [配置和使用详情](#配置和用法详情)

另请参阅常见问题: [我的应用程序未运行，哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅 [源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization) 章节，获取
查看下载文件的描述和有关创建新项目的信息。

用于构建 MSP430 FreeRTOS 演示项目的 makefile 位于
Demo/msp430 目录。

---

### 安装编译器工具链

要获取并安装编译器，请执行以下步骤：
1. 前往[MSPGCC 下载页面](http://sourceforge.net/project/showfiles.php?group_id=42303)，
 获取最新的 MSPGCC 安装文件。我使用了 'mspgcc-20040723.exe' 下载，它安装了
 Win32 设置所需的一切文件。
2. 仅当您希望使用 GDB 的图形版本时，才需要执行此步骤。

 最新的 MSPGCC 下载仅包括命令行 GDB 调试器。我更喜欢使用名为
 Insight 的图形版本。可以使用稍早一些的[Insight 预建版本](http://prdownloads.sourceforge.net/mspgcc/msp430-insight-win32-20021222.exe?download)。此旧版本的 Insight 安装目录要不同于
 最新的 MSPGCC 安装所选目录，因为您不想覆盖在第 1 步中获得的文件。

 您现在应该有两个安装版本。在第 1 步安装的最新版本的 MSPGCC ，以及第 2 步中
 稍早一些的 Insight 版本。这两种版本的 GDB 调试器都被称为 msp430-gdb.exe，因此其中一种需要重命名。
 从此步骤安装的文件中找到旧版本的 msp430-gdb.exe，然后将其重命名为 msp430-insight.exe。
3. 确保第 1 步安装的文件的 BIN 目录和第 2 步安装的文件的 BIN 目录
 均包含在您的 PATH 环境变量中。

---

### 演示应用程序

### 功能

演示应用程序包括一些通常会闪烁 LED 的任务。
ES449 原型板有一个内置的 LCD 显示屏和一个内置的用户
LED 灯。因此，这类任务不是闪烁 LED，而是
在 LCD 显示屏上闪烁 '*' 字符。最左边的 '*' 代表 LED 0，
往右一个是 LED 1，以此类推。

其中一个 ComTest 任务会使用板载 LED。每次串行端口上接收到一个字符时，
LED 就切换一次。

如果该演示应用程序正确执行，其实现以下效果:

* LCD 显示屏上的前三个 '*' 字符受 'flash' 任务的控制。每个字符
 以固定频率闪烁，第一个 '*' 闪烁最慢，第三个
 最快。
* 串行端口上收到字符时，原型版中内置的 LED 便会闪烁（请参阅下文“硬件设置”部分）。
* 并非所有的任务都会更新 LCD，因此没有可见的迹象表明它们是否正常运行。因此，我们创建了一项 'Check' 任务，
 旨在确保在所有其他任务中都未检测到错误。

 LCD 显示屏上第五个 '*' 受 'Check' 任务的控制。
 'Check' 任务每 3 秒钟便会检查一次系统中的所有任务，确保任务正确执行，没有出现错误。
 然后切换 '*' 5。如果 '*' 5 每 3 秒切换一次，
 那么就说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 发现了至少一个错误。

### 演示应用程序硬件设置

演示应用程序需执行通过串行端口发送和接收字符的任务。字符由
一项任务发送，被另一项任务接收。如有字符丢失或接收顺序不正确，则会标记错误状态。
通常情况下，此机制需要环回连接器才能运行（这样才能保证 UART 发送的所有字符也能
由其接收）。这种情况下会使用 MSP430 UART  的 'loopback' 模式，不需要其他外部连接器。

演示应用程序使用 LCD 显示屏代替 LED 灯，因此不需要其他硬件设置。

### 构建演示应用程序

确保您在 PATH 环境中安装并可访问所有工具（如上所述）。打开命令提示符
（DOS 框），导航到 FreeRTOS/Demo/MSP430 目录，然后只需键入“make”即可。项目构建时应该没有
错误或警告，并生成名为 "a.out" 的可执行文件。

### 从 FLASH 执行 RTOS 演示

MSPGCC 下载包括一个名为 msp430-jtag.exe 的闪存编程实用程序，
使用该程序可以将 a.out 下载到 MSP430 闪存。要对闪存进行编程：
1. 断开 ES449 原型板的电源。
2. 使用提供的并行端口电缆将 FETP JTAG 适配器连接到 ES449。
3. 从构建目录 (FreeRTOS/Demo/MSP430) 键入以下命令...

```c
msp430-jtag -ep a.out
```

 ...这将擦除闪存，然后用 a.out 进行编程。
4. 移除 FETP JTAG 适配器，为 ES449 通电。演示应用程序将执行。

### 使用 JTAG 调试器执行 RTOS 演示

FreeRTOS 下载内容中包含/Demo/MSP430FreeRTOS目录中名为 'gdb.ini' 的文件。每次
GDB 启动时，GDB 都会处理此文件，这是正确操作所必需的。它告诉 GDB 如何连接到远程目标硬件，
然后在 main() 的顶部设置一个断点。如果您没有使用 Win32 主机系统，您可能需要将 'gdb.ini' 重命名为
'.gdbinit'。

要使用 GDB 图形调试器运行应用程序：
1. 断开 ES449 原型板的电源。
2. 使用提供的并行端口电缆将 FETP JTAG 适配器连接到 ES449。
3. MSPGCC 下载包含一个名为 msp430-gdbproxy.exe 的程序。这会拦截 GDB TCP 命令并将它们重定向到
 并行端口。启动 msp430-gdbproxy（安装
 MSPGCC 时会将其快捷方式添加到开始菜单中）。默认情况下，msp430-gdbproxy 使用端口 3333 - 不要更改此设置。
4. 按照上节中的说明对闪存进行编程。闪存可以从 GDB 内进行编程，但
 提前分开做要快得多。
5. 启动调试器时使用以下命令……

```c
msp430-insight a.out
```

 ……gdb.ini 文件中的命令将执行其余操作。如果您更喜欢使用命令行调试器，仅需
 将 msp430-insight 替换为 msp430-gdb。
6. 在main() 中的断点，Insight 将启动，程序将停止，如下所示。

![](/media/2018/insightmsp.gif)

调试器在大多数情况下运行良好，但存在一些问题，如 MSPGCC 网站所示。另请注意
以下几点：

* 使用 FETP JTAG 适配器时，请勿向 ES449 目标硬件提供任何其他电源。我发现，
 那样做会使微控制器的定时器无法工作。
* 当在断点停止时，微控制器定时器似乎会继续计数，而不是停止在
 命中断点时所包含的值。由于使用定时器比较匹配中断，逐步执行
 代码可能会导致中断连续触发（当定时器继续计数时，总有一个中断
 挂起，所以当您离开一个中断时，就会进入下一个中断）。因此，使用抢占式内核时，
 一旦 RTOS 调度程序启动，就很难逐步执行代码，最好在调试时使用协作式内核
 。

---

### 配置和用法详情

### 串行端口驱动程序

根据规定串口驱动程序是为环回模式所配置。因此，虽然演示应用程序能够执行，但
如有其他用途，则需关闭环回模式。

此外还应注意，编写串行驱动程序是为了测试部分实时内核功能，而不是
提供优化解决方案。

### RTOS 移植特定配置

此移植的特定配置项目位于 Demo/MSP430/FreeRTOSConfig.h。可以编辑此文件中定义的常量
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本端口将
BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

### 使用 MSP430F449 以外的部件

核心实时内核组件应
可在所有 MSP430F4xx 设备上移植，但需要考虑外接设备的设置和内存要求。
需要考虑的事项：
* Source/portable/GCC/MSP430F449/port.c 中的 prvSetupTimerInterrupt() 负责配置微控制器定时器，以
 生成 RTOS tick。
* 端口、内存访问和系统时钟配置由 Demo/MSP430/main.c 中的 prvSetupHardware() 执行。
* 串口驱动程序。
* 文件 msp430x44x.h 提供寄存器位置定义，该文件位于
 FreeRTOSConfig.hDemo/MSP430/ 的顶部。
* RAM 大小：参见下面的内存分配部分。

### 在抢占式和协同式 RTOS 内核之间切换

将Demo/MSP430/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，即可使用抢占式内核，设置为 0 可使用
协同式内核。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
基于提供的演示应用程序生成文件构建应用程序。
不要将优化级别降低到 O2 以下，因为这会改变参数传递给函数的方式，阻止
实时内核正确运行。

### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 MSP430 演示生成文件中，提供实时内核所需的内存分配
。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 章节，
获取完整信息。

---

### MSP430F149 EasyWeb2 移植

此移植由 aLUNZ（电子邮件：alunz AT users.sourceforge.net）提供。我无法直接支持它，因为我没有目标开发板，
但它与 ES449 演示非常相似。[在此处下载 MSP430F149
源代码](http://www.realtimeengineers.com/MSP149_EasyWeb.zip)。Zip 文件包含一个带有安装说明的 readme 文件。

请注意，此移植尚未升级为使用FreeRTOS V3.0.0 API。
