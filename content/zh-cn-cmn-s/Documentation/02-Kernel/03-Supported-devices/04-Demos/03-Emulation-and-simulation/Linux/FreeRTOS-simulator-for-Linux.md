---
title: "适用于 FreeRTOS 的 Posix/Linux 模拟器演示 使用 GCC"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

本页记载的 FreeRTOS 移植允许 FreeRTOS 在 Linux 上运行，
 就像 [FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)（通常 
 称为 FreeRTOS Windows 模拟器）始终允许 FreeRTOS 在 Windows 上运行那样。该移植由 David Vrabel 开发， 
 灵感来自 William Davy 在 2008 年开发的 Linux 移植。 

移植层的实现使用 POSIX 线程，因此该移植也称为 POSIX 移植。请不要将其与 
 [FreeRTOS-Plus-POSIX 库](FreeRTOS-Plus/FreeRTOS_Plus_POSIX/index.md)混淆，两者的作用完全相反。 
 FreeRTOS-Plus-POSIX 为原生 FreeRTOS API 提供 POSIX 线程包装器，使用 POSIX API 编写的应用程序因此可以在 
 FreeRTOS 上运行，而 Linux/POSIX FreeRTOS 移植则让 FreeRTOS 应用程序可以在 POSIX 操作系统上运行。

就像 Windows 移植一样，FreeRTOS Linux 移植提供了一个方便的环境， 
 您可以在其中试验 FreeRTOS 并开发 FreeRTOS 应用程序，以便之后将其移植到真正的嵌入式硬件上，但 FreeRTOS 应用程序
 （使用 Linux 移植）不会表现出实时行为。

---

#### 重要！适用于 FreeRTOS 的 Posix/Linux 模拟器演示使用说明

*在使用模拟器演示之前，请阅读以下所有要点。*

* [源代码组织](#源代码组织)
* [FreeRTOS Linux 移植演示应用程序](#posixlinux-模拟器演示)
* [构建并运行适用于 FreeRTOS 的 Posix/Linux 模拟器演示](#构建-posixlinux-模拟器演示)
* [GDB 调试技巧](#gdb-调试技巧)
* [移植层设计说明](#移植层设计说明)
* [已知问题](#已知问题)
* [常见问题和解决方案](#常见问题和解决方案)

另请参阅常见问题：[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

[FreeRTOS zip 文件下载内容](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)包含所有 FreeRTOS 移植和演示应用程序的源代码，因此它所包含的文件要远多于构建并运行使用 FreeRTOS Linux 移植的预配置演示所需的文件。有关此 zip 文件目录结构的信息，请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面。 

* 适用于 Linux (POSIX) 的 RTOS 移植层位于 \`[FreeRTOS/Source/portable/ThirdParty/GCC/Posix](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/master/portable/ThirdParty/GCC/Posix)\` 目录中。
* 共有两个演示项目：一个是仅有内核的演示，位于  \`[FreeRTOS/Demo/POSIX_GCC](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC) 目录中，另一个是网络演示，位于 ` directory, and a networking demo which is located in the  `[FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)\` 目录中。

### Posix/Linux 模拟器演示

#### \`[内核演示项目](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Posix_GCC)\`

 此项目演示了使用 Linux (POSIX) 移植的 FreeRTOS 内核功能。此项目可配置为运行简单的 Blinky 演示 (`BLINKY_DEMO`) 或更全面的演示 (`FULL_DEMO`)，只需设置 `mainSELECTED_APPLICATION` 常量  （在 \`[main.c](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC/main.c)\` 顶部定义）即可。

* Blinky 演示

如果 `mainSELECTED_APPLICATION` 设置为 `BLINKY_DEMO`，则 `main()` 将调用 `main_blinky()`，该函数在 \`[main_blinky.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Posix_GCC/main_blinky.c) 中实现。`. `main_blinky()\` 会创建一个非常简单的演示，其中包括两项任务、一个软件定时器和一个队列。其中一项任务通过队列以 200 毫秒的频率向另一项任务反复发送值 100，而定时器则每 2000 毫秒就向同一队列发送值 200。接收任务每次从队列接收到任一值时都会打印出一条消息。
* 完整演示

如果 `mainSELECTED_APPLICATION` 设置为 `FULL_DEMO`，则 `main()` 将调用 `main_full()`，该函数在 \`[main_full.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Posix_GCC/main_full.c) 中实现。`. The demo created by `main_full()\` 创建的演示主要由标准演示任务组成，这些任务除了测试 RTOS 移植和演示如何使用 FreeRTOS API 之外，不执行其他特定功能。

完整演示包含一项“检查”任务，每 10 秒（模拟时间） 执行一次，但拥有最高优先级，以确保获得处理时间。它的主要功能就是检查所有标准演示任务是否仍在运行。此检查任务会维护其每次执行时向控制台输出的状态字符串。如果所有标准演示任务都运行正常，没有错误，则此字符串会包含 "OK" 和当前滴答计数。如果检测到错误，则此字符串会包含一条信息，指明报告错误的任务。

#### \`[网络演示项目](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)\`

此项目演示了如何使用 [FreeRTOS-Plus-TCP](FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md) TCP/IP 堆栈在 Linux 上进行网络连接。它会重新使用原来为使用 FreeRTOS-Plus-TCP 和 Windows RTOS 移植而编写的 TCP 回显客户端演示。

 TCP 回显演示使用 FreeRTOS-Plus-TCP TCP/IP 堆栈 
连接至 TCP 端口 7 上的[标准 TCP 回显服务器](https://en.wikipedia.org/wiki/Echo_Protocol)，并与其进行通信。
适用于 Linux 的 FreeRTOS-Plus-TCP 网络接口使用 libpcap 访问网络。

 要配置用于演示的 TCP/IP 堆栈，请执行下列操作：

* 请按照 
 [软件设置 #1、软件设置 #2 和软件设置 #4 部分](FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)的说明进行操作，
 详见描述在 Windows 主机上使用 FreeRTOS-Plus-TCP 的页面（无需执行软件设置 #3 部分的步骤）。
* 将 `configECHO_SERVER_ADDR0` 至 `configECHO_SERVER_ADDR3` 常量设置为 
 `FreeRTOSConfig.h` 中的回显服务器地址。

防火墙经常拦截 TCP 端口 7（标准回显端口）。如果遇到这种情况，将 FreeRTOS 应用程序和回显服务器使用的端口号改成
有效的大数字（例如 50000）即可。FreeRTOS 应用程序使用的端口号由 echoECHO_PORT 常量
（位于 [TCPEchoClient_SingleTasks.c](https://github.com/FreeRTOS/FreeRTOS/blob/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix/TCPEchoClient_SingleTasks.c) 中）设置。
如果在 Linux 中使用 `nc` 命令创建 TCP 回显服务器，请使用 `-l` 开关设置端口号：

```c
$ sudo nc -l 7
```

在 macOS 上，回显服务器可以通过以下方式启动：
```c
$ sudo nc -l -p 7
```

#### 网络故障排除

如果回显服务器与 FreeRTOS 演示在同一台计算机上运行，则可能无法发送 [ARP](FreeRTOS-Plus/FreeRTOS_Plus_TCP/ARP.md) 响应，从而导致演示无法连接到回显服务器。如果出现此问题，切勿在执行 RTOS 演示的计算机上运行回显服务器，请换台计算机。

### 构建 Posix/Linux 模拟器演示

* 前提条件（下列输出结果显示了测试期间使用的版本）：
	1. gcc

	

	```c
	$ gcc --version
	gcc (GCC) 9.2.0
	```
	2. make
	
	

	```c
	$ make --version
	GNU Make 3.81
	Copyright (C) 2006  Free Software Foundation, Inc.
	```
	3. [libpcap](https://www.tcpdump.org/)（用于网络支持）
	 
	

	```c
	$ version: libpcap-devel-1.5.3-11.x86_64 
	```

	 要在 ubuntu 上安装，请运行 
	```c
	$ sudo apt-get install libpcap-dev
	```

	 要在基于 rpm 的系统上安装，请运行 
	```c
	$ sudo yum install libpcap-devel
	```
	 或 
	```c
	$ sudo dnf install libpcap-devel
	```

	 要在 MacOS 上安装，请运行 
	```c
	$ brew install libpcap
	```

	 或者也可通过[源代码](https://github.com/the-tcpdump-group/libpcap)安装，请按照 [INSTALL.md](https://github.com/the-tcpdump-group/libpcap/blob/master/INSTALL.md) 中的说明进行操作
* 构建源代码：
	1. 导航到 
	 [内核演示源代码](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS/Demo/Posix_GCC)或[网络演示源代码](https://github.com/FreeRTOS/FreeRTOS/tree/master/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix)中的演示目录 

	

	```c
	 $ cd FreeRTOS/Demo/Posix_GCC/
	```

	或 
	```c
	 $ cd FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Echo_Posix
	```
	2. 要构建源代码，请运行：
	```c
	$ make
	```
	3. 要清理源代码，请运行： 
	```c
	$ make clean
	```
* 运行演示（请查看上文有关如何在可用演示之间进行选择的说明）：

	1. 导航到新建的 "build" 目录

	```c
	$ cd build 
	```
	2. 运行内核演示（Blinky 演示或完整演示）

	

	```c
	$ ./posix_demo
	```
	3. 运行网络演示
	- 在另一台机器上运行回显服务器
	 ```c
	 $ sudo nc -l 7
	 ```
	- 在你的机器上运行
	 ```c
	 $ sudo ./posix_tcp_demo
	 ```


### GDB 调试技巧

本节假设您已安装并熟悉 [gdb](https://www.gnu.org/software/gdb/)。 
 如需查找 gdb 文档，请点击[此处](https://www.gnu.org/software/gdb/documentation/)。

移植层使用两个进程信号：`SIGUSR1` 和 `SIGALRM`。如果 pthread 没有等待信号， 
 则 GDB 会在收到信号时暂停进程。必须告知 GDB 忽略（且不打印） 
 信号 `SIGUSR1`，因为每个线程会异步接收该信号。在 GDB 中，输入：

```c
$ handle SIGUSR1 nostop noprint pass
```

 以确保调试不会被信号中断。请参阅：

```c
$ man signal
```

了解更多信息。

或者，在主目录中创建一个名为 `.gdbinit` 的文件，并放入下列两行指令：

```c
handle SIGUSR1 nostop noignore noprint
handle SIGALRM nostop noignore noprint
```

将这两行指令添加至 `.gdbinit` 文件后，它会告诉 GDB 不要在接收到这些信号时中断程序的执行。

用于系统滴答的定时器共有三种：`ITIMER_REAL`、`ITIMER_VIRTUAL` 
 和 `ITIMER_PROF`。`ITIMER_VIRTUAL` 是默认定时器，因为它仅在进程 
 在用户空间中执行时计时，遇到断点便会停止计时。`ITIMER_PROF` 等同于 
 `ITIMER_VIRTUAL`，但包括执行系统调用所花费的时间。`ITIMER_REAL` 
 即使在进程完全没有执行时也会继续计时，因此是实时计时。`ITIMER_REAL` 是唯一 
 可用的选项，因为其他定时器只有在进程实际运行时才会计时。因此， 
 如果在空闲任务钩子中调用 `nanosleep`，非实时定时器报告的时间几乎不会 
 增加。

### 移植层设计说明

简单的 FreeRTOS 模拟器实现只需封装平台原生线程，并在所有切换任务 
 上下文的调用中调用 OS 挂起和恢复线程 API。此模拟器使用 Posix 条件变量和信号 
 来控制底层 Posix 线程的执行。信号可以异步传递给线程， 
 从而中断目标线程的执行，而挂起线程则需等待条件变量才能恢复。

在设计多线程进程时，我们通常会使用多个线程以实现并发执行， 
 并在 IO 任务上实现一定程度的非阻塞。此模拟器使用线程并不是为了实现并发执行， 
 而是用来存储执行上下文。信号、互斥锁和条件变量用于同步上下文切换， 
 但是否要切换上下文最终由 FreeRTOS 调度器决定。

创建新任务时，会创建一个 pthread 作为该任务执行的上下文。pthread 会立即 
 挂起自己，并将执行权交还给创建者。挂起时，pthread 会在 
 调用 `pthread_cond_wait` 的过程中处于等待状态，直到收到恢复信号 `pthread_cond_signal` 才会解除阻塞。

FreeRTOS 任务可以通过两种方式进行切换：一种是通过调用 `taskYIELD()` 进行协同式切换，另一种则是作为 
 RTOS 系统滴答的一部分进行抢占式切换。在此模拟器中，任务上下文的切换通过恢复下一个任务上下文 
 （由 FreeRTOS 调度器决定）并挂起当前上下文（两者之间有短暂的握手）来实现。

RTOS 系统滴答通过 `ITIMER` 生成，并且信号会传递至（仅传递至）当前正在执行的 
 pthread。RTPS 系统滴答信号处理程序会递增滴答计数并选择下一个 RTOS 任务上下文。它会恢复线程， 
 并向自己发送一个挂起信号。只有当 TOS 系统滴答信号处理程序退出时才会处理挂起，因为信号也要 
 排队。

### 已知问题

`pthread_create` 和 `pthread_exit/cancel` 是系统密集型调用，可能会迅速耗尽 
 处理时间。

如果调用了阻塞的系统和库函数（如 printf），可能会导致整个进程停止。如果必须 
 进行系统调用，则必须屏蔽该线程上的所有信号，然后在系统调用执行完毕后重新允许这些信号。
 您还可以创建额外的线程来模拟中断，但也需屏蔽这些线程上的信号， 
 使它们不会接收信号，从而可以由 FreeRTOS 调度器安排执行，并成为 FreeRTOS 
 常规任务的一部分。

为防止进程窃取主机操作系统的所有空闲执行时间，可以使用 `nano_sleep()`。该函数的实现 
 不使用任何信号，但会立即中断睡眠/挂起进程来处理信号。 
 因此，使用该函数的最佳方式就是设置一个比 FreeRTOS 执行时间切片更长的睡眠时间， 
 并从空闲任务中调用该函数，这样进程就会处于挂起状态，直至下一个滴答。

### 常见问题和解决方案

#### 创建线程

**问题**  

使用 `pthread_create` 创建外部线程（例如模拟中断）可能会影响 FreeRTOS 调度任务的方式，因为底层 RTOS 移植需要接收某些信号后才能运行。创建的线程可能会收到信号，但调度器可能会劫持该线程，改变其原本的用途，让其执行特定的 FreeRTOS 任务。这可能导致系统崩溃甚至处于死锁状态。

**解决方案**  

使用 pthread_create 创建线程时，应在线程中屏蔽信号，可以通过在线程主体中添加类似以下内容来实现：

 \`sigset_t set;  

 sigfillset( &set );  

 pthread_sigmask( SIG_SETMASK, &set, NULL );\`

或者，在创建线程之前屏蔽信号，这种解决方案虽然更有效，但不可移植：

\`void * args;  

 sigset_t set;  

 pthread_t tid;  

 pthread_attr attr;  

 sigfillset( &set );  

 pthread_attr_init( &attr );  

 pthread_attr_setsigmask_np( &attr, &set );  

 pthread_create( &tid, &attr, start_routine, args );\`

#### 创建新任务

使用 \`[xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)\` 创建的 RTOS 任务会将创建的堆栈传递至 port.c，确保 pthread 库可以使用此堆栈和 pthread_attr_setstack。可创建的最小堆栈大小存在限制。此限制取决于平台，最小堆栈大小为 PTHREAD_STACK_MIN。因此，pthread_create() 会创建自己的堆栈，而忽略 FreeRTOS 传递的堆栈。如果发生这种情况，请不要担心，运行时系统不会出现问题，但某些使用 FreeRTOS 调试工具来显示堆栈信息或其他 FreeRTOS 变量的用户可能会遇到一些不一致问题。 

解决方法是在 Posix 移植上运行时，如果所需堆栈小于 PTHREAD_STACK_MIN，则始终传递大小为 PTHREAD_STACK_MIN 的堆栈。 

