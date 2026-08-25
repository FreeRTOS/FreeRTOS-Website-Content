---
title: "FreeRTOS Windows 移植适用于 Visual Studio 或 Eclipse 和 MingW"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

---

[\![](/media/2018/platform_toolset_small.jpg)](/media/2018/platform_toolset.jpg)

**注意！**在
FreeRTOS 中分布的 Visual Studio 项目创建时间不一，因此使用了不同的
[Visual Studio for C/C++ 工具免费版本](https://visualstudio.microsoft.com/vs/community/)。一般来说，您使用的 Visual Studio 版本不必与用于创建项目的版本完全相同，
并且如果存在版本不一致导致的问题，
Visual Studio 会提供对项目进行重定向的指导。但是，如果存在向后兼容的问题，
可能需要将您的 Visual Studio 更新至最新版本。

---

### 序言——适用于初学者

如果您刚接触 FreeRTOS，建议在浏览此页面之前，先查看
[通过简单的 FreeRTOS 项目入门](simple-freertos-demos.md)
文档（其中还说明了如何使用 FreeRTOS 的
Windows 移植）。

### 简介

此页面展示了 FreeRTOS 的 Windows 移植层，
使用 [Visual Studio 社区版](https://visualstudio.microsoft.com/vs/express/)
和[适用于 C 与 C++ 开发者的 Eclipse IDE](http://www.eclipse.org/downloads/)进行开发和测试，
后者安装了基于 [MingW](https://sourceforge.net/projects/mingw/files/) GCC 的编译器。
为两组工具链均提供了演示项目。这两组工具链也是免费的，
不过必须先注册，才能将 Visual Studio 用于
非评估目的。

此移植在运行 32 位 Windows XP 系统的双核 Intel 处理器上开发，
现在运行 64 位 Windows 10 系统的四核 Intel 处理器上维护
（但项目会创建一个 32 位二进制）。

---

### *使用 Windows FreeRTOS 移植的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [操作原理](#操作原理)
2. [使用移植前的注意事项](#使用-windows-freertos-移植的注意事项)
3. [源代码组织](#源代码组织)
4. [使用 Eclipse / MingW (GCC) 演示](#eclipse-和-mingw-gcc)
5. [演示应用程序](#演示应用程序)
6. [定义和使用模拟中断服务程序](#定义和使用模拟中断服务程序)

---

### 操作原理

#### 运行任务的线程

Windows 移植层为创建的每个 FreeRTOS 任务创建一个低优先级 Windows 线程，
这些任务由 FreeRTOS 应用程序创建。然后，所有低优先级的 Windows 线程都会保持在
挂起状态，运行 FreeRTOS 任务的 Windows 线程除外，
FreeRTOS 调度器将这些任务指定为运行状态。这样，FreeRTOS 调度器
根据它的调度策略来选择运行哪个
低优先级的 Windows 线程。其他所有低优先级的 Windows 线程都被挂起，因此无法运行。

在微控制器上运行的 FreeRTOS 移植必须在任务进入和离开运行状态时，
执行复杂的上下文切换
来保存和还原微控制器上下文（寄存器等）。与此不同，Windows 模拟器层
只需在 Windows 线程代表的任务进入和离开运行状态时，
挂起或恢复 Windows 线程。Windows 负责执行实际的上下文切换。

#### 模拟滴答中断

滴答中断生成由一个高优先级的 Windows 线程模拟，
该线程会定期抢占正在运行任务的低优先级线程。可实现的滴答
速度受 Windows 的系统时钟限制，对于 FreeRTOS 而言，
这个速度比较慢，精度非常低。因此，它无法
实现真正的实时行为。

#### 模拟中断处理

模拟的中断处理由第二个具有更高优先级的 Windows 线程执行，
此线程的优先级使其能够抢占
正在运行 FreeRTOS 任务的低优先级线程。模拟中断处理的线程
处于等待状态，直到系统中的另一个线程通知它
有一个待定的中断。例如，模拟滴答中断生成的线程
设置一个中断待定位，然后向模拟正在处理的中断的 Windows 线程
发出通知，告知有一个中断处于待定状态。然后，
模拟的中断处理线程会执行，并查看所有可能的中断待定位
- 根据需要来执行任何模拟的中断处理，以及清除中断待定位。

---

### 使用模拟器之前的注意事项

#### 嵌入式工程师的 Windows 编程

在使用提供的 Windows 项目之前，请注意我（
Windows 模拟器的作者）是嵌入式程序员，而不是 Windows 程序员。
因此，实现可能比较粗糙。任何来自更了解 Windows 编程的人士针对此实现提供的[反馈](/Why-FreeRTOS/Support-options)，
我都会
心怀感激地接受。

#### 在 Windows 上删除任务

删除一个 FreeRTOS 任务时，Windows 移植会终止
负责运行该任务的线程。但在 Windows 中，
在一个线程内终止另一个线程不会导致
被终止的线程正在使用的资源被返回到系统。这意味着
在运行时，FreeRTOS 的 vTaskDelete() API 函数的可调用次数
有限。此限制非常高（几千次），
但确实可以防止 
[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/) 
在开始报错之前无限期执行。

#### 对 Windows 主机 CPU 的占用

运行
一个 FreeRTOS 应用程序时，对 Windows 主机的 CPU 占用会非常高。但这不会对响应能力有太大影响，
因为只使用了低优先级线程，但是 CPU 核心温度
会上升，并且散热风扇会呈现对应的反应。

如果您担心自己的电脑无法应对温度升高，
那么我建议
使用一个程序来显示当前 CPU 核心温度，
以及当前温度与您的 CPU 能够承受的最高温度
之间的差距。我个人使用
免费的 [Core Temp](http://www.alcpu.com/CoreTemp/)
用于此功能。

---

### 源代码组织

#### Eclipse 和 MingW (GCC)

FreeRTOS 模拟器演示应用程序的 Eclipse 项目
位于 FreeRTOS/Demo/WIN32-MingW 目录，
在主 FreeRTOS 下载中。需要将其导入到 Eclipse 工作区中
以构建项目。

#### Visual Studio

FreeRTOS 模拟器演示应用程序的 Visual Studio 解决方案
名称是 WIN32.sln，位于 FreeRTOS/Demo/WIN32-MSVN 目录，
在主 FreeRTOS 下载中。

---

### 使用 Eclipse 和 MingW (GCC) 演示

#### 获取编译器

[MingW](https://sourceforge.net/projects/mingw/files/) 编译工具
不包含在 Eclipse 分布中，需要
单独下载。

#### 将 FreeRTOS 模拟器项目导入 Eclipse 工作区

将 FreeRTOS 模拟器项目导入 Eclipse 的操作如下：
1. 启动 Eclipse IDE，然后转到 Eclipse Workbench。
2. 在 Eclipse 的 "File" 菜单中选择 "Import"。将出现
 一个对话框。
3. 在对话框中选择 "General | Existing Projects into Workspace"。
 将出现另一个对话框允许您导航到
 并选择一个根目录。
4. 选择 FreeRTOS/Demo/WIN32-MingW
 目录，然后将出现一个名为 RTOSDemo 的项目，
 这就是应该导入的项目。

---

### 演示应用程序

#### 功能

常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 使用 #define 在 main.c 的顶部定义，用于在简单的 Blinky 样式演示和更全面的测试和演示应用程序之间切换。接下来两部分将对此进行说明。

##### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将调用
main_blinky()，此函数在 main_blinky.c 中实现。

main_blinky() 创建一个非常简单的演示，包括两个任务和一个队列。
一个任务反复将值 100 通过队列发送到另一个任务。接收任务每次
收到队列上的值时，都显示一条消息。

##### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将调用
main_full()，此函数在 main_full.c 中实现。

main_full() 创建的演示非常全面。它创建的任务
主要包括[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)——
此任务不执行其他功能，仅用于测试移植
并演示 FreeRTOS API 的使用方法。

##### main_full() 创建的 "check"（检查）任务

完整演示除了创建标准演示任务以外，还创建一个 "check" 检查任务。此任务
每（模拟）5 秒钟执行一次，但拥有最高的优先级
以确保其拥有处理时间。它的主要功能是检查
所有标准演示任务是否仍可使用。

检查任务维护一个状态字符串，每次执行时
都将字符串输出到控制台。如果所有标准演示任务都运行正常，没有错误，那么
将呈现 "OK" 字符串和当前的滴答数。如果检测到错误，
字符串将显示一条信息，指明报错的
任务。

#### 查看控制台输出

Eclipse 项目会向内建的控制台输出字符串。要查看这些字符串，
必须选择 "RTOSDemo.exe" 控制台，
可以通过点击图标为电脑显示器的快速按钮，从下拉菜单中选择。
如下图所示。

Visual Studio 控制台输出将显示在命令提示符窗口中。

![在 Eclipse 中查看 FreeRTOS 模拟器输出](/media/2018/Viewing-The-FreeRTOS-Simulator-Output-In-Eclipse.jpg)

 在一个 Eclipse 调试会话中选择 "RTOSDemo.exe" 控制台

---

### 定义和使用模拟中断服务程序

#### 为模拟中断服务程序定义一个处理程序

中断服务程序必须包含以下原型文件：

**unsigned long ulInterruptName( void );**

"ulInterruptName" 可以是任何合适的函数名称。

如果执行中断服务程序导致上下文切换，
那么中断函数必须返回 pdTRUE。否则，中断函数
应返回 pdFALSE。

#### 为模拟中断服务程序安装一个处理程序

要为模拟中断服务程序安装处理程序，可以
使用在 Win32 移植层中定义的 vPortSetInterruptHandler() 函数
。包含以下原型文件：

**void vPortSetInterruptHandler( unsigned long ulInterruptNumber, unsigned long (*pvHandler)( void ) );**

ulInterruptNumber 必须是一个 3 至 31（包含 31）之间的值，并且
是应用程序中唯一的（即任何应用程序中
都有 29 个可定义的模拟中断）。号码
0 至 2（包含 2）之间的值由模拟器使用。

pvHandler 应指向要安装到的中断号码
的处理程序函数。

#### 触发一个模拟中断服务程序

可以通过调用 vPortGenerateSimulatedInterrupt() 函数
（该函数也被定义为 Win32 移植层的一部分）来将中断设置为挂起，
并在适当情况下执行中断。其原型如下：

**void vPortGenerateSimulatedInterrupt( unsigned long ulInterruptNumber );**

ulInterruptNumber 是设置为待定的中断的编号，
与 vPortSetInterruptHandler() 的 ulInterruptNumber 参数相对应。

#### 安装和触发中断的示例

模拟器本身使用三个中断，分别用于一个 yield 任务、
模拟滴答、终止原本在执行一个 FreeRTOS任务的 Windows 线程
（此任务已被删除）。以下简单的示例
是 yield 中断的代码。

中断函数的唯一功能是请求上下文切换，
所以只返回 pdTRUE。它使用以下代码定义：

```c
**static unsigned long prvProcessYieldInterrupt( void )
{
 /* There is no processing to do here, this interrupt is just used to cause
 a context switch, so it simply returns pdTRUE. */
 return pdTRUE;
}**
```

然后，使用以下调用安装模拟中断处理程序，
portINTERRUPT_YIELD 定义为 2：

**vPortSetInterruptHandler( portINTERRUPT_YIELD, prvProcessYieldInterrupt );**

此中断应在 taskYIELD()/portYIELD() 被调用时执行，
所以 Win32 移植版本的 portYIELD() 定义如下：

**#define portYIELD() vPortGenerateSimulatedInterrupt( portINTERRUPT_YIELD )**

