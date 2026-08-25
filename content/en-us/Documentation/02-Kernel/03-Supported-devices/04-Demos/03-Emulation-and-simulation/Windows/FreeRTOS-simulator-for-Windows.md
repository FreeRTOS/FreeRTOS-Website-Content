---
title: "Win32 Simulator for FreeRTOS Using Visual C++"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

|  |
| --- |
| <br />**This page relates to an older contributed simulator. Please see the <br /> [official FreeRTOS Windows simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)<br /> that can be build using Visual Studio 2010 Express and Eclipse with MingW (GCC).**<br /> |

The Win32 FreeRTOS simulator was kindly provided by Dushara Jayasinghe.
I have used it with [Visual Studio 2008 Express Edition](https://visualstudio.microsoft.com/vs/express/)
 (which can be downloaded for free) under WinXP and found it to be a very valuable tool.

The simulator source code is included as a [FreeRTOS contributed port](http://interactive.freertos.org/attachments/token/iyn818tg7jjehoi/?name=x86_VisualStudio8_DJ.zip). Below are
some usage notes from Dushara.

---

### Introduction

The FreeRTOS WIN32 port allows your embedded application to be simulated on a PC with Microsoft windows XP (may work on NT as well).

The source code is available in the [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS), but requires unzipping
separately from the main FreeRTOS code. Once unzipped you will find the Visual Studio project in the FreeRTOS/Demo/Win32 directory.

To enable compilation, the following Pre-processor definitions must be present:

```c

    WIN32
    _WIN32_WINNT=0x0400
    WINVER=0x400
```

Each FreeRTOS task that you create is wrapped by a Windows thread. This has a significant implication:
The stack size argument in 'xTaskCreate' is ignored (meaning you won't catch stack overflow errors via the simulator).

### Interrupts

The simulator provides 30 interrupt sources (1 - 30). These are defined in cpuemu.h
The following API calls are useful for interrupt handling:

iPortSetIsrHandler - Set the interrupt handler.

vPortEnableInt - enable the specified interrupt.

vPortDisableInt - disable the specified interrupt.

Interrupt generation is simulated using separate threads.

Create the interrupt generator thread as follows:

SetThreadPriority(CreateThread(NULL, 0, irq\_generator, NULL, 0, NULL), THREAD\_PRIORITY\_ABOVE\_NORMAL);

Sample interrupt generator:

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

tick\_generator in port.c can be used as a good example.

### Important Notes

* System ticks occur approx every 15ms.
* Your vApplicationIdleHook() should include a Sleep(0) call. If the only thing your IDLE thread does is pat the watchdog, you can use Sleep(INFINITE).
 Note added by RB: I found Sleep(Infinite) upset the debugger when stepping through the code and removed it for debugging.
