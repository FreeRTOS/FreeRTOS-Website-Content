---
title: "Atmel SAMD20"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 Atmel [SAMD20](https://www.microchip.com/wwwproducts/en/ATSAMD20G18) ARM [Cortex-M0+](http://www.arm.com/products/processors/cortex-m/cortex-m0plus.php) Demo

FreeRTOS and FreeRTOS-Plus-CLI Built Using Atmel Studio and GCC

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


|  |
| --- |
| <br />![Atmel SAMD20 ARM Cortex-M0+ MCU](/media/2018/SAMD20.jpg)<br /><br /><br />**SAMD20 Xplained PRO** <br /><br /> |

### Introduction

This page describes a demo project that uses FreeRTOS and
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
on the SAMD20 Cortex-M0+ microcontroller from Atmel.

The project uses the FreeRTOS ARM Cortex-M0 GCC port, builds with the free
[Atmel Studio IDE](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio) (which uses the Visual Studio framework
and includes a kernel aware FreeRTOS plug-in), and targets the
very low cost [SAMD20 Xplained Pro](http://www.microchipdirect.comPartDetail.aspx/?q=p:10500351#tc:description)
evaluation board.

The command line interface character input and output uses drivers provided by
Atmel in their Atmel Software Framework ([ASF](https://www.microchip.com/avr-support/advanced-software-framework-(asf))).

A #define is used to switch the build between a simple blinky style application,
and a comprehensive test and demo application that incorporates the FreeRTOS-Plus-CLI
component.


![](/media/2018/Atmel_Studio_Plugin.png)
  

**The Atmel Studio IDE with Kernel Aware FreeRTOS Plug-in** 


---

#### *IMPORTANT! Notes on using the SAMD20 ARM Cortex-M0+ Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#demo-application-functionality)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)
  

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so
contains many more files than are needed by the SAMD20 demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the directory structure.

The Atmel Studio solution file is called RTOSDemo.atsln, and is located in the
FreeRTOS/Demo/CORTEX\_M0+\_Atmel\_SAMD20\_Xplained directory.


---

### Building and Running the ARM Cortex-M0+ RTOS Application

1. Open FreeRTOS/Demo/CORTEX\_M0+\_Atmel\_SAMD20\_Xplained/RTOSDemo.atsln in the
 Atmel Studio IDE.
2. Locate the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY definition at the top of
 main.c. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 1 to create the simple
 blinky demo, or 0 to create the comprehensive demo that also includes
 the command line interpreter.
3. Select "Rebuild RTOSDemo" from the Atmel Studio "Build" menu (or press F7) to build
 the demo project.
4. Connect a USB cable between the USB port on the SAMD20 Xplained Pro board
 and the host computer.
5. Select "Start Debugging and Break" from the Atmel Studio "Debug"
 menu to program the microcontroller flash memory and start a debug
 session.


### Demo Application Functionality

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

Building with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1 results in main() calling
main\_blinky(). The main\_blinky() demo is described below.

* **The main\_blinky() Function:** 
 
 main\_blinky() creates one queue, and two tasks. It then starts the
 scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by prvQueueSendTask() in main\_blinky.c.
 

 prvQueueSendTask() repeatedly blocks for 200 milliseconds before sending
 the value 100 to the queue that was created in main\_blinky().
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by prvQueueReceiveTask()
 in main\_blinky.c.
 

 prvQueueReceiveTask() repeatedly blocks on attempts to read from the queue
 that was created in main\_blinky(), toggling the LED each time data is
 received. The queue send task sends data to the queue every 200 milliseconds,
 so the LED will toggle every 200 milliseconds.


#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

Building with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0 results in main() calling
main\_full(). The main\_full() demo is described below.
* **The main\_full() Function:** 
 
 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
 test tasks, a task that manages FreeRTOS-Plus-CLI, and a timer. It then starts the
 scheduler.
* **FreeRTOS-Plus-CLI Task:** 

[![ARM Cortex-M0+](/media/2018/SAMD20_run_time_stats.png)](/media/2018/SAMD20_run_time_stats.png)
  

**Click to enlarge** 

 The SAMD20 Xplained Pro board connects to a host computer by a single
 USB cable. The USB connection provides both a debugger interface and
 a virtual COM port connection. The virtual COM port is used to provide
 the character input and output required by the command line interface
 (CLI). The CLI can therefore be accessed from any serial terminal program,
 such as Hyper Terminal, or as shown in the image on the right, Tera Term.
 
 The image shows COM 20 being used, but it is likely that the virtual
 COM port will enumerate to a different port number on your host computer.
 

 As always with FreeRTOS-Plus-CLI, the 'help' command will display a list of
 registered (and therefore available) commands. The image was captured
 after executing the 'run-time-stats' command, which generates a table
 showing the amount of CPU time that has been consumed by each RTOS task.
* **The "Reg Test" Tasks:** 
 
 These fill the registers with known values, then check
 that each register maintains its expected value for the lifetime of the
 task. Each task uses a different set of values. A register
 containing an unexpected value is indicative of an error in the context
 switching mechanism.
* **The "Check" software Timer:** 
 
 The check [software timer](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) period is initially set to three
 seconds. Its callback function checks that all the standard demo tasks, and
 the register check tasks, are not only still executing, but are executing
 without reporting any errors. If the check timer callback discovers that a
 task has either stalled, or reported an error, then it changes the period of
 the check timer from the initial three seconds, to just 200ms. The callback
 function also toggles the LED to give a visual
 indication of the system status: **If the LED is toggling every three seconds
 then no issues have been discovered. If the LED is toggling every 200ms, then
 a problem has been discovered in at least one task**.


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

Note that the following lines are included in FreeRTOSConfig.h to map the FreeRTOS
interrupt handler function names onto the CMSIS interrupt handler function names.
This allows the linker scripts provided by the compiler tool vendors to be used
without modification.

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler
```


#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_M0+\_Atmel\_SAMD20\_Xplained/RTOSDemo/src/config/FreeRTOSConfig.h. The
constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 500Hz is useful for
 testing the RTOS kernel functionality, but is faster than most applications require.
 Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. All ARM Cortex-M0+ ports define BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.


#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M0+ demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.


  


 
