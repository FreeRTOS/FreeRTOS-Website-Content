---
title: "Motorola ColdFire"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
Motorola ColdFire 移植最初由 Jimmie Alam 和 Brian Birtles
在悉尼科技大学工程学院学习期间创建。该报告为那些希望为不同处理器创建新移植的人员 
提供了极好的参考。

随后，Vladimir Lasky 便开始对该移植进行维护更新，而最近 Christian Walter 对该移植进行了重大升级。

我本人没有使用过该移植，但 Christian Walters 在将该移植升级到 FreeRTOS 版本并对其进行测试方面的工作，
让人对其稳定性充满信心。

Christian Walters 除了对源代码做出贡献，还十分贴心地提供了下列文档。*我要感谢 Christian为 
FreeRTOS.org 做出的巨大贡献。*

Christian 提供的文档如下：

---

### Coldfire MCF523x / GCC 移植

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![M5235BCC Business Card Computer](/media/2018/m5235bcc.jpg)

本页介绍了适用于 Freescale/Motorola Coldfire 系列微控制器的 FreeRTOS 移植。演示应用程序本身是专为 [M5235BCC Business Card Computer](http://www.freescale.com/) 这一物美价廉功能强大的开发平台定制的。该平台具有高达 150MHz 的 V2 Coldfire 核心、16MB SDRAM、2MB 闪存以及一个 10/100 MBit 的以太网控制器。

此演示应用程序的下载文件中包含用于 FreeRTOS 的功能齐全的 [lwIP 1.1.1](http://savannah.nongnu.org/projects/lwip/) 移植以及 MCF523x 以太网接口的驱动程序，此外还包括 FreeRTOS 移植常用的典型功能，如串行驱动程序示例和演示任务。下方截图显示了 HTTP 客户端连接到目标系统时嵌入式 HTTP 服务器应返回的输出。

![在 MCF523x 目标系统上运行的 HTTP 服务器](/media/2018/m5235-lwip-http.png)

---

### 重要！Coldfire MCF523x RTOS 移植使用说明

*在使用此移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和用法详情](#配置和使用详情)
4. [补充说明](#补充说明)
5. [致谢](#致谢)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件远多于此演示所需的文件。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，了解下载文件的描述以及有关创建新项目的信息。

该移植包含 lwIP TCP/IP 协议栈，因此相当之大。如果无需协议栈，则可以使用 FreeRTOS/Demo/MCF5235_GCC 中的裸移植。

1. FreeRTOS/Demo/lwip_MCF5235_GCC：此目录包含演示应用程序代码。文件 demo.c 中包含创建任务和启动 RTOS 调度器的启动代码，而 Web 服务器和 lwIP 初始化代码则位于 web.c 中。此外，该目录还包含 Makefile、GNU LD 的链接器脚本和 GDB 初始化脚本。
2. FreeRTOS/Demo/lwip_MCF5235_GCC/include/arch：此目录包含 Freescale MCF5235 支持页面的处理器头文件。如需替换提供的文件，可以下载页面底部的 MCF523XSC 包。
3. FreeRTOS/Demo/lwip_MCF5235_GCC/system：此目录包含系统启动文件。如果使用的不是 MCF5235 处理器，则需要进行一些更改，包括 crt0.S、init.c、vector.S 和 serial.c。文件 mcf5xxx.S 和 newlib.c 无需修改即可使用。
4. FreeRTOS/Demo/lwip_MCF5235_GCC/include：此目录包含处理器特定的头文件。这些文件从 [Freescale](http://www.freescale.com/) 网站下载并导入，可以使用关键字 MCF523XSC 进行查找。此目录中的文件也应根据目标系统进行相应替换。
5. FreeRTOS/Demo/lwip_MCF5235_GCC/lwip：此目录包含 [lwIP](http://www.sics.se/~adam/lwip/) 协议栈。该移植使用于 2006 年 3 月 15 日发布的 lwIP 1.1.1。
6. FreeRTOS/Demo/lwip_MCF5235_GCC/lwip/contrib/port/FreeRTOS/MCF5235：此为 lwIP 移植。文件 sys_arch.c 为 FreeRTOS 所特有，无需更改。如果使用其他控制器，则应替换 netif/fec.c 中的网络接口驱动程序。

---

### 演示应用程序

#### 要求

要在不修改的情况下使用演示应用程序，至少必须具有以下硬件和软件包：
* 来自 Freescale 的 5235BCC Business Card Computer 套件。
* 连接到计算机并行端口的 P & E BDM 线缆（如果购买 5235BCCKIT，则随附该线缆）。
* 安装在 /opt/gcc-m68k 中的 m68k-elf-gcc 目标的 GNU C 编译器。如果安装在其他位置，请更改 Makefile。
* 应用了 Coldfire 补丁的 Linux 或 WIN32 版 [BDM 工具](http://sourceforge.net/projects/bdm/)。您可以使用我编写的补丁，详见本网站的“补丁”选项卡。如果需要使用图形调试器，则还应对 Insight 应用补丁，否则，请编辑 Makefile，将 Insight 变量更改为 m68k-bdm-elf-gdb。

确保目标硬件可以正常工作。在验证此步骤之前，**请勿**继续操作。如果已针对调试器应用了我提供的补丁，则在测试配置时，可执行 bdmchk /dev/bdmcf0 或 bdmchk /dev/bdmcf20。输出结果如下所示：

```c
wolti@pcno-4:$ /opt/gcc-m68k/bin/bdm-chk /dev/bdmcf20
BDM Check for Coldfire processors.
Device: /dev/bdmcf20
trying kernel driver: /dev/bdmcf20
trying bdm server: localhost:/dev/bdmcf20
Driver Ver : 2.12
Processor  : Coldfire2
Interface  : P&E Coldfire
Target status: 0x2 -- NOT RESET, HALTED, NOT STOPPED, POWER ON, CONNECTED.
Register test,    1 of    1 :
   D00 : ........................................
   D01 : ........................................
...
01001054: FFFFFFFF
wolti@pcno-4:$

```

#### 构建配置

演示应用程序提供了两种构建配置。配置 1 位于目标内存中，用于调试，使用的是 m5235-ram.ld 链接器脚本。配置 2 用于闪存执行，使用的是 m5235-rom.ld 链接器脚本。如需更改配置，请编辑文件 Makefile。确保在更改此设置后执行 make clean 命令，然后执行 make all debug。构建完成后，应启动 Insight 调试器。在菜单中选择 "Run/Download"。

首次启动 Insight 时，系统会显示配置对话框，您可在其中选择目标设备。确保输入正确的设备名称（与 bdm-chk 工具同名）：

![设置 Insight 调试器](/media/2018/m5235-insight-setup.png)
配置对话框。

上传完成后，使用 "View" 菜单打开 Insight 控制台，然后输入 GDB 命令 execute。定义见随移植提供的 m5235.gdb 脚本，可设置程序计数器。接下来输入 continue，执行应该在 main 中的临时断点处停止。下图仅用于演示目的。

![启动程序执行](/media/2018/m5235-insight-execute.png)
在 Insight 控制台中输入命令。

如果更喜欢使用命令行，则可以使用 GDB ，无需用到 Insight。步骤如下所示：

```c
$ /opt/gcc-m68k/bin/m68k-bdm-elf-gdb --command=m5235.gdb --se=demo.elf
GNU gdb 6.0
Copyright 2003 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "--host=i686-pc-linux-gnu --target=m68k-bdm-elf"...
(gdb) target bdm /dev/bdmcf20
trying kernel driver: /dev/bdmcf20
trying bdm server: localhost:/dev/bdmcf20
using coldfire 2 core
Remote bdm connected to /dev/bdmcf20
 Coldfire debug module version is 0 (5206(e)/5272/5282/5235)
(gdb) setup-and-load
(gdb) load demo.elf
Loading section .text, size 0x1f470 lma 0x0
Loading section .data, size 0x8b0 lma 0x1f470
Start address 0x408, load size 130336
Transfer rate: 130336 bits/sec, 509 bytes/write.
(gdb) execute
Current language:  auto; currently asm
Breakpoint 1 at 0x117c: file demo.c, line 67.
(gdb) c
Continuing.
[New process 42000]
[Switching to process 42000]
main (argc=0, argv=0x0) at demo.c:67
67          asm volatile    ( "move.w  #0x2000, %srnt" );
Current language:  auto; currently c
(gdb)

```

#### 功能

演示应用程序包含以下任务：
* **一组标准演示任务**
包括轮询队列、阻塞队列、信号量、数学任务和动态优先级任务。有关详细信息，请参阅 [RTOS 演示页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)。
* **检查任务**
 检查任务定期执行。监控标准演示任务：如果所有任务都执行无误，则（通过打印任务）向终端 IO 写入 "."；如果检测到错误，则写入 "E"。
* **lwIP 任务**
 lwIP 有多项任务运行。一项任务属于 lwIP 本身，处理 TCP/IP 连接。另一项任务用于以太网驱动程序，处理接收的以太网帧。该任务可由 ISR 中发出的信号量解除阻塞。第三项任务属于 Web 服务器，处理 HTTP 请求。

### 配置和使用详情

要想让一切正常运行，基本步骤是检查抢占式定时器是否按预期工作。为此，应检查函数 xPortStartScheduler 是否适用于目标体系结构。建议在 ISR 中设置断点或切换 LED。此外，还应验证 Coldfire 是否使用单堆栈模式（而不是在 USP 和 SSP 之间切换） ，平台默认使用此模式。在启用 RTOS 调度器之前，还必须检查处理器是否处于监管模式。完成上述步骤之后，不带 lwIP 的 MCF5235 移植应可正常运行。

本文假定您已非常熟悉 lwIP，并且已准备好以太网驱动程序。添加 lwIP 时，只需将文件复制到相应的目录中，然后更改 Makefile 即可。请务必确保上一步正常工作，因为在此级别调试操作系统或移植相关问题非常困难。

### 补充说明

#### 线程安全 Newlib（提示）

为确保 Newlib 线程安全，必须为每项任务分配新的 struct _reent。此操作在 pxPortInitialiseStack 中完成。此外，还应修改函数 portSAVE_CONTEXT 和 portRESTORE_CONTEXT，以将 __impure_ptr 替换为任务特定指针。移植尚未提供此功能，但作者将尽快添加。接下来，不妨阅读一下 Bill Gatliff 撰写的文章“[嵌入 GNU：Newlib 第 2 部分](http://www.embedded.com/story/OEG20020103S0073)”。

#### Coldfire 堆栈布局和上下文切换

本节仅适用于对 Coldfire 移植内部运作感兴趣的人员。我将就堆栈布局、portSAVE_CONTEXT 和 portRESTORE_CONTEXT 上下文宏以及 portYIELD 宏展开探讨。
每当执行上下文切换时，Coldfire CPU 核心将在堆栈中创建*异常帧*。之后，必须立即执行 portSAVE_CONTEXT 中定义的汇编程序函数，步骤如下：

1. 在堆栈上为数据寄存器 %d0-%d7 和地址寄存器 %a0-%a6 预留空间，这会占用 60 字节。此外，必须将 ulCriticalNesting 的值压入 vPortEnterCritical 和 vPortExitCritical 函数的堆栈，这需要额外 4 个字节。
2. 预留空间后，寄存器会压入堆栈。
3. 至此，堆栈指针前进 60 字节，变量 ulCriticalNesting 压入堆栈。
4. 接下来，将堆栈指针的值存储在任务控制块 pxCurrentTCB中。

汇编程序代码位于 portmacro.h 中。调试示例如下所示。只需在定时器 ISR 中放置断点，然后与此示例进行比较。

![Coldfire 栈帧](/media/2018/m5235-stackframe.jpg)
栈帧

不难发现，在异常之前，SP 指向 0x002ac30，可在其中找到返回地址 0x00017896、异常帧以及处理器状态寄存器 0x41902004。地址 0x002ac2c 中存储了 ulCriticalNesting 的值。下文所述为地址寄存器和数据寄存器。堆栈 0x0002abec 的新顶部也存储在关联的 TCB pxCurrentTCB 中。

要恢复上下文，请执行以下步骤：

1. 取消引用指针 pxCurrentTCB，将其加载到堆栈指针寄存器 %sp 中，以此恢复堆栈顶部。
2. 重新加载数据和地址寄存器，将堆栈指针增加 60 字节。
3. 恢复 ulCriticalNesting 计数器，增加堆栈指针一次，现在指针指向 Coldfire 异常帧。
4. 执行 rte 指令，继续执行任务。

Coldfire 还有一项非常有趣的功能，即软件中断。portYIELD 宏由陷阱实现，该陷阱经过初始化，与定时器滴答 ISR 具有相同的函数。

#### 使用此移植的软件

最后，本文作者希望针对使用此移植的部分应用程序提供相应链接。
* [FreeModbus](http://freemodbus.berlios.de/) 提供可移植 Modbus ASCII/RTU 模式和 TCP 实现，Coldfire 平台可提供一流目标板。

### 致谢

诚挚感谢以下人员，排名不分先后。
* 非常感谢 Richard Barry 提供如此出色的操作系统和支持。
* 非常感谢我的同事 P. Puffler 分享自己的见解。
* 非常感谢 Janusz Uzycki 报告 FreeRTOS/lwIP 层中的一些错误。

FreeRTOS 移植版权所有 2006：Christian Walter

