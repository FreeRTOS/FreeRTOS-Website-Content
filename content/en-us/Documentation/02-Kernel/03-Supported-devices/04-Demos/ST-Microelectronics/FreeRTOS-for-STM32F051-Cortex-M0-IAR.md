---
title: "STM32F051 ARM Cortex-M0 Demo Using the IAR development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![](/media/2018/STM32_F0_generic.jpg)<br /> |

### Introduction

The project described on this page demonstrates the FreeRTOS ARM Cortex-M0 IAR port.
It is configured to run on the STM320518-EVAL evaluation board, which is fitted
with an STM32F051 microcontroller.

The project can be configured to
create either a basic blinky style demo, or a more comprehensive test and demo
application that includes some of the FreeRTOS standard demo tasks.

![FreeRTOS kernel aware debugger used with the IAR compiler](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 Screen shot of the FreeRTOS state viewer plug-in

 that ships with the IAR IDE as standard.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the IAR ARM Cortex-M0 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so
includes many more files than are needed by this demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The IAR EWARM workspace for the FreeRTOS STM32F0 demo application is called RTOSDemo.eww,
and is located in the FreeRTOS/Demo/CORTEX\_M0\_STM32F0518\_IAR directory. Note that
the workspace was created prior to STM32F0 support being included in EWARM, and as such, the
project is configured to use a generic ARM Cortex-M0 core, and the instructions provided on this
page describe the separate ST-Link utility being used to program the microcontroller flash
memory.

---

### The Demo Application

#### Demo application hardware set up

The demo uses the LEDs that are integrated onto the STM320518-EVAL board, so no
hardware setup is required.

#### Building and running the demo application

The single RTOSDemo project can be configured to run
a simple blinky style project, or a more comprehensive test and demo application. The
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY setting at the top of main.c is used to select
between the two. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to one to create the
basic Blinky style demo. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0 to create
the more comprehensive test and demo application.

1. Open FreeRTOS/Demo/CORTEX\_M0\_STM32F0518\_IAR/RTOSDemo.eww in the
 IAR Embedded Workbench IDE.
2. Set the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY constant to generate the required demo functionality (as
 noted above), before building the project.
3. Power up the STM320518-EVAL board, then connect a USB cable between the
 USB port labelled ST-LINK/V2 (SN3) and the host computer.
4. Open FreeRTOS/Demo/CORTEX\_M0\_STM32F0518\_IAR/Debug/RTOSDemo.bin
 in the ST-LINK utility program (a copy of which is provided on the CD that comes
 with the STM320518-EVAL hardware), then program the microcontroller flash
 memory. Later versions of the IAR Embedded Workbench will probably have
 the capability of programming the flash memory from within the IAR IDE,
 removing the need to use the separate ST-LINK utility.
5. **Select "Disconnect" from the ST-LINK utility's "Target" menu.** A debug
 session cannot be started from the IAR IDE while the ST-LINK utility is
 connected to the hardware.
6. Back in the IAR Embedded Workbench IDE - select "Debug without Downloading"
 from the IDE's "Project" menu to start a debug session.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

Setting mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 1 results in main() calling
main\_blinky(). main\_blinky() sets up a very simple demo, as
described below.

* **The main\_blinky() Function:** 
 
 main\_blinky() creates one queue, and two tasks. It then starts the
 scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.
 prvQueueSendTask() sits in a loop that causes it to repeatedly block for
 200 milliseconds, before sending the value 100 to the queue that was created
 within main\_blinky(). Once the value is sent, the task loops back around to block for
 another 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c. prvQueueReceiveTask() sits in a loop where it repeatedly blocks on
 attempts to read data from the queue that was created within main\_blinky(). When data
 is received, the task checks the value of the data, and if the value equals
 the expected 100, toggles LED LD1. The 'block time' parameter passed to
 the queue receive function specifies that the task should be held in the Blocked
 state indefinitely to wait for data to be available on the queue. The queue
 receive task will only leave the Blocked state when the queue send task writes
 to the queue. As the queue send task writes to the queue every 200
 milliseconds, the queue receive task leaves the Blocked state every 200
 milliseconds, and therefore toggles LED LD1 every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

Setting mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0 results in main() calling
main\_full(). main\_full() sets up a more comprehensive test and demo application,
as described below.

* **The main\_full() Function:** 
 
 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
 test tasks, and a timer. It then starts the
 scheduler.
* **The "Reg Test" Tasks:** 
 
 These fill the registers with known values, then check
 that each register maintains its expected value for the lifetime of the
 task. Each task uses a different set of values. The reg test tasks execute
 with a very low priority, so get preempted very frequently. A register
 containing an unexpected value is indicative of an error in the context
 switching mechanism.
* **The "Check" software Timer:** 
 
 The check software timer period is initially set to three
 seconds. Its callback function checks that all the standard demo tasks, and
 the register check tasks, are not only still executing, but are executing
 without reporting any errors. If the check timer callback discovers that a
 task has either stalled, or reported an error, then it changes the period of
 the check timer from the initial three seconds, to just 200ms. The callback
 function also toggles LED LD4 each time it is called. This provides a visual
 indication of the system status: **If LED LD4 toggles every three seconds,
 then no issues have been discovered. If the LED toggles every 200ms, then
 an issue has been discovered with at least one task**.

---

### RTOS Configuration and Usage Details

#### Interrupt service routines

Interrupt service routines that cause a context switch have
no special requirements.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

A dummy interrupt handler
called Dummy\_IRQHandler() is provided at the end of main.c as a reference implementation.
Dummy\_IRQHandler() is also replicated below.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portEND\_SWITCHING\_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND\_SWITCHING\_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}
```

Note that the following lines are included in FreeRTOSConfig.h.

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler
```

These definitions map the FreeRTOS kernel interrupt handler function names onto
the CMSIS interrupt handler functions names - and in so doing, allow the
ST or IAR provided linker scripts and start up files to be used without modification.

Attention please!: See the [page dedicated to setting interrupt priorities on ARM Cortex-M devices](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4). Remember that ARM Cortex-M cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0
and therefore the highest priority possible.

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_M0\_STM32F0518\_IAR/FreeRTOSConfig.h. The
constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality, but is faster than most applications require.
 Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_M0\_STM32F0518\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M0 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
