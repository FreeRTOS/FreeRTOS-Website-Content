---
title: "FreeRTOS for the Renesas RL78 Microcontroller Using the IAR compiler"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR compiler](https://www.iar.com/products/iar-embedded-workbench-for-renesas-78k)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/Renesas-RL78-YRPBRL78G13-promo-board.jpg)  

 The RL78/G13 Promotion Board (YRPBRL78G13)

|  |
| --- |
| [**This demo has been superseded with one that supports more RL78<br /> part numbers and evaluation boards. Click to view the documentation<br /> page.**](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RTOS_RL78_IAR_Demos) |

**The project requires IAR Embedded Workbench for the RL78 (EWRL78) version 1.10 or higher. A free KickStart edition of EWRL78 is
 [available for download from the IAR web site](http://www.iar.com/ewrl78/).**

This page documents an application that demonstrates the use of FreeRTOS on
a [Renesas RL78 16-bit microcontroller](http://www.renesas.com/pr/mcu/rl78/index.html).

The demo is configured to run on the RL78/G13 Promotion Board
([YRPBRL78G13](http://am.renesas.com/products/tools/introductory_evaluation_tools/renesas_demo_kits/yrpbrl78g13/yrpbrl78g13.jsp)),
which is fitted with a R5F100LEA microcontroller. The R5F100LEA provides the software
application with a little under 4K bytes of usable RAM, which is not
enough for all the FreeRTOS features to be fully demonstrated in this single application.
The RL78 range does, however, include parts with up to 32K bytes of RAM, some eight
times more RAM than that available on the R5F100LEA. The R5F100LEA demo creates
13 tasks, 4 queues and two timers.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### IMPORTANT! Notes on using the Renesas RL78 RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports,
so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR Embedded Workbench workspace for the Renesas RL78 Promo Board demo is called
RTOSDemo.eww, and is located in the FreeRTOS/Demo/RL78\_RL78G13\_Promo\_Board\_IAR
directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application makes use of an LED that is mounted directly onto the promo
board hardware, so no additional hardware setup is required.

#### Functionality

This section describes the functionality of the RL78G13 demo. In all, thirteen
tasks, four queues and two timers are used. Some of the tasks are from the
set of 'standard demo' tasks. These are common to all FreeRTOS demos, so are not
RL78 specific. They have no other purpose than to demonstrate use of the FreeRTOS
API, and to test the core FreeRTOS functionality.

The following demo specific tasks are created in addition to the standard demo tasks:

* **Register Test Tasks** 

 These two tasks test the RTOS kernel context switch mechanism by first filling
 each RL78 register with a known and unique value, then repeatedly
 checking that the value originally written to the register is maintained
 in the register, for the lifetime of the task. The tasks execute at the
 lowest possible priority (the idle priority), so are preempted
 frequently.

 The nature of these tasks necessitates that they are written in assembly.
* **A "Check" software timer and callback** 

 The Check timer is an example of a very simple watchdog type timer. It
 monitors all the other standard demo tasks, the register check tasks,
 and the demo software timer, and provides visual feedback as to the system status
 using an LED.

 The period of the check timer is initially set to three seconds. The
 check timer callback function checks that all the standard demo tasks,
 the register check tasks, and the demo timer are not only still executing,
 but are executing without reporting any errors, then toggles an LED.

 If the check timer discovers that a task or timer has either stalled, or
 reported an error, then it changes its own period from the initial three
 seconds, to just 200ms. Therefore, if the LED toggles every three seconds,
 no issues have been discovered. If the LED toggles every 200ms, an issue
 has been discovered in at least one task or the demo timer.
* **A "demo" software timer and callback** 

 The demo timer callback function does nothing more than increment a variable.
 The period of the demo timer is set relative to the period of the check timer.
 This allows the check timer to know how many times the
 demo timer callback function should execute between each execution of the
 check timer callback function. The variable incremented in the demo timer
 callback is used by the check timer to determine if the demo timer callback
 is being executed at the expected rate.

main.c also includes example stack overflow, idle, and malloc files hook functions.

When executing correctly, the demo application will toggle the user LED every three seconds.

#### Building the demo application

1. Open the FreeRTOS/DemoRL78\_RL78G13\_Promo\_Board\_IAR/RTOSDemo.eww workspace from within the IAR Embedded Workbench IDE.
2. Press F7 to build the project. The project should build without any
 errors or warnings being generated.

#### Programming the microcontroller and debugging

1. Ensure the YRPBRL78G131 Demo Board is connected to the host computer, and
 that the required USB drivers have been installed correctly (a prompt to
 install the drivers will be shown the first time the hardware is connected)
2. Select "Download and Debug" from the Embedded Workbench "Project" menu.
 There will be a short delay while the flash memory is programmed before
 the debugger breaks on entry to the main() function.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this demo are contained in
[FreeRTOS/DemoRL78\_RL78G13\_Promo\_Board\_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization). The
constants defined in this file can be edited to suit your application.

There is also a constant that is specific to the Renesas RL78 port and demo:

* **configCLOCK\_SOURCE**
 Set configCLOCK\_SOURCE to 0 to use an external clock source, or 1 to use the high speed internal clock source.
 Ensure configCPU\_CLOCK\_HZ is also set correctly when altering any clock configuration.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type short.

Note that vPortEndScheduler() has not been implemented.

#### Memory models

The FreeRTOS port will automatically switch between the near and far memory models,
depending on the settings in the IAR project options. The port has been tested with
two memory model combinations, which are:

1. The data and code models both set to near.
2. The data and code models both set to far.

#### Writing interrupt service routines

Interrupt service routines that cannot cause a context switch have no special requirements and can be written as described by the
IAR compiler documentation.

Often you will require an interrupt service routine to cause a context switch.
For example a serial port character being received may unblock a high priority
task that was blocked waiting for the character to arrive. If the unblocked task
has a higher priority than the current task, then the ISR should return directly
to the unblocked task. Limitations in the IAR inline assembler necessitate such
interrupt service routines are entered using an assembly file wrapper. An
example is provided below. First the assembly file wrapper.

---

```c

; ISR\_Support.h defines the portSAVE\_CONTEXT and portRESTORE\_CONTEXT
; macros.
#include "ISR\_Support.h"

 ; The wrapped implemented in the assembly file.
 PUBLIC vISRWrapper

 ; The portion of the handler that is implemented in an external C file.
 EXTERN vISRHandler

 ; Ensure the code segment is used. 
 RSEG CODE:CODE

; The wrapper is the interrupt entry point.
vISRWrapper:

 ; The ISR must start with a call to the portSAVE\_CONTEXT() macro to save
 ; the context of the currently running task.
 portSAVE\_CONTEXT

 ; Once the context is saved the C portion of the handler can be called.
 ; This is where the interrupting peripheral is actually serviced.
 call vISRHandler

 ; Finally the ISR must end with a call to portRESTORE\_CONTEXT() followed by
 ; a reti instruction to return from the interrupt to whichever task is
 ; now the task selected to run (which may be different to the task that
 ; was running before the interrupt started).
 portRESTORE\_CONTEXT
 reti

 ; The interrupt handler can be installed into the vector table in the same
 ;assembly file.

 ; Ensure the vector table segment is used. 
 COMMON INTVEC:CODE:ROOT(1)

 ; Place a pointer to the asm wrapper at the correct index into the vector
 ; table. Note 56 is used is purely as an example. The correct vector
 ; number for the interrupt being installed must be used. 
 ORG 56
 DW vISRWrapper
```

---

An example assembly file wrapper for an interrupt handler.

The C portion of the interrupt handler is just a standard C function.

---

```c

/* This standard C function is called from the assembly wrapper above. */
void vISRHandler( void )
{
short sHigherPriorityTaskWoken = pdFALSE;

 /* Handler code goes here, for purposes of demonstration, assume
 at some point the handler calls xSemaphoreGiveFromISR().*/
 xSemaphoreGiveFromISR( xSemaphore, &sHigherPriorityTaskWoken );

 /* If giving the semaphore unblocked a task, and the unblocked task has a
 priority that is higher than the currently running task, then
 sHigherPriorityTaskWoken will have been set to pdTRUE. Passing a pdTRUE
 value to portYIELD\_FROM\_ISR() will cause this interrupt to return directly
 to the higher priority unblocked task. */
 portYIELD\_FROM\_ISR( sHigherPriorityTaskWoken );
}
```

---

The C portion of the example interrupt handler.

#### Resources used by the RTOS kernel

The RTOS kernel uses the interval timer to generate the RTOS tick. The function prvSetupTimerInterrupts() in
FreeRTOSSourceportableIARRL78port.c can be altered to use any convenient timer source.

The RTOS kernel also requires exclusive use of the BRK software interrupt instruction.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

SourcePortableMemMangheap\_1.c is included in the demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
