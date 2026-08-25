---
title: "适用于 FreeRTOS 的 Win32 模拟器 使用 Visual C++"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


|  |
| --- |
| <br />**本页信息适用于贡献的旧版模拟器。请参阅<br /> [官方 FreeRTOS Windows 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)<br />，该模拟器可以使用 Visual Studio 2010 速成版和带有 MinGW (GCC) 的 Eclipse 构建。**<br /> |

Win32 FreeRTOS 模拟器由 Dushara Jayasinghe 友情提供。 
我曾在 WinXP 环境中将该模拟器与 [Visual Studio 2008 速成版](https://visualstudio.microsoft.com/vs/express/)
 （可免费下载）搭配使用，发现这一工具非常实用。

模拟器源代码作为 [贡献的 FreeRTOS 移植](http://interactive.freertos.org/attachments/token/iyn818tg7jjehoi/?name=x86_VisualStudio8_DJ.zip)随附其中。以下是
Dushara 提供的一些用法注意事项。

---

### 引言

借助 FreeRTOS WIN32 移植，可在装有 Microsoft Windows XP 的计算机上模拟嵌入式应用程序（同样也适用于 Windows NT）。

源代码位于 [FreeRTOS 下载内容](RTOS-contributed-ports.md)中，但需要
与主 FreeRTOS 代码分开解压缩。解压缩后，您将在 FreeRTOS/Demo/Win32 目录中找到 Visual Studio 项目。

要启用编译，必须存在以下预处理器定义：

```c

    WIN32
    _WIN32_WINNT=0x0400
    WINVER=0x400

```

创建的所有 FreeRTOS 任务都由 Windows 线程封装。这会产生重大影响：
"xTaskCreate" 中的堆栈大小实参会遭到忽略（这意味着无法通过模拟器捕获堆栈溢出错误）。

### 中断

模拟器提供 30 个中断源 (1 - 30)。这些中断源在 cpuemu.h 中定义。
可调用以下 API ，用于处理中断：

iPortSetIsrHandler - 设置中断处理程序。  

vPortEnableInt - 启用指定的中断。  

vPortDisableInt - 禁用指定的中断。

可使用单独的线程模拟中断生成。

创建中断生成器线程，如下所示：

SetThreadPriority(CreateThread(NULL, 0, irq_generator, NULL, 0, NULL), THREAD_PRIORITY_ABOVE_NORMAL);

示例中断生成器：

```c

DWORD WINAPI irq_generator(LPVOID lpParameter) 
{
    for(;;)
    {
            // wait for some windows event.
            __generate_interrupt(IRQ_NO);
    }
}

```

port.c 中的 tick_generator 可以作为典型示例。

### 重要提示

* 系统大约每 15 毫秒滴答一声。
* vApplicationIdleHook() 应包含 Sleep(0) 调用。如果闲置线程只是定期唤醒看门狗定时器，则可以使用 Sleep(INFINITE)。
 RB 添加的注释：我发现 Sleep(Infinite) 在单步执行代码时会扰乱调试器，为了方便调试，我删除了该函数。

