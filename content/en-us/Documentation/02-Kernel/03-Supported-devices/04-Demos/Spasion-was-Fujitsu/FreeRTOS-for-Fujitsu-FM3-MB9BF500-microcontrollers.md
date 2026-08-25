---
title: "Spansion (was Fujitsu) FM3 DemoUsing the Keil and IAR development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Fujitsu SK-FM3-100PMC MB9BF506 development and evaluation board](/media/2018/Fujitsu-SK-FM3-100PMC-MB9BF506-development-and-evaluation-board.jpg)  
Spansion SK-FM3-100PMC MB9BF506 starter kit board,  
a project is also provided for the SK-FM3-64PMC1 starter kit

This page documents a FreeRTOS ARM Cortex-M3 demo application that targets a Spansion
[FM3 microcontroller](http://www.spansion.com/Products/microcontrollers/32-bit-ARM-Core/fm3/Pages/overview_32fm3.aspx).
IAR and Keil projects are provided that are already pre-configured to run on both the
SK-FM3-100PMC and
SK-FM3-64PMC1
starter kit evaluation boards. The evaluation boards are fitted with a
MB9BF506N
and a MB9AF314 microcontroller respectively.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the FreeRTOS Keil and IAR FM3 example projects*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-spansion-fm3-mb9bf500mb9af300-demo-applications)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS zip file download contains source code for all the FreeRTOS ports,
and every demo application project.
It therefore contains many more files than are required to build and run the FM3 MB9BF500 demo. See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
of the downloaded files, and information on creating a new project.

The table below provides information on locating the relevant FM3 projects
within the official FreeRTOS download:

|  |  |  |  |
| --- | --- | --- | --- |
| **Compiler**  | **Target**  | **Project name**  | **Project file location in the FreeRTOS source tree**  |
| <br /> IAR<br />  | <br /> MB9B500<br />  | <br /> RTOSDemo\_IAR.eww<br />  | <br /> FreeRTOS/Demo/CORTEX\_MB9B500\_IAR\_Keil<br />  |
| <br /> IAR<br />  | <br /> MB9A300<br />  | <br /> RTOSDemo\_IAR.eww<br />  | <br /> FreeRTOS/Demo/CORTEX\_MB9A310\_IAR\_Keil<br />  |
| <br /> ARM/Keil<br />  | <br /> MB9B500<br />  | <br /> RTOSDemo\_Keil.uvproj<br />  | <br /> FreeRTOS/Demo/CORTEX\_MB9B500\_IAR\_Keil<br />  |
| <br /> ARM/Keil<br />  | <br /> MB9A300<br />  | <br /> RTOSDemo\_Keil.uvproj<br />  | <br /> FreeRTOS/Demo/CORTEX\_MB9A310\_IAR\_Keil<br />  |

---

### The Spansion FM3 MB9BF500/MB9AF300 Demo Applications

#### Functionality

The IAR and Keil projects each contain three build configurations:

|  |  |
| --- | --- |
| **Build configuration** | **Description** |
| <br /> Blinky<br />  | <br /> This is a **very simple configuration**. It creates two tasks,<br /> one software timer, and also uses a button interrupt.<br /> <br /> The two tasks communicate via a queue, with the receiving task<br /> toggling one of the seven segment display LEDs each time a value is<br /> received. The ["Blinky demo functionality"](#visible-blinky-demo-functionality)<br /> section of this documentation page highlights the LED used.<br /> <br /> Pressing user button SW2 generates an interrupt, the service routine<br /> for which resets a software timer before turning an LED on.<br /> The software timer has a five second period, and when the five<br /> seconds expire, the timer callback function turns the LED off again.<br /> Therefore, pressing SW2 will turn the LED on, and the LED will<br /> remain on until a full five seconds pass without the button being<br /> pressed again.<br /> <br /> The Blinky build configuration uses the<br /> main-blinky.c source file. The other two build configurations use<br /> the main-full.c source file.<br /> <br /> |
| <br /> Full<br />  | <br /> This is a comprehensive configuration that creates lots of tasks,<br /> queues, semaphores (of various types) and software timers.<br /> <br /> The Full configuration creates the same tasks and timers that are<br /> created by the Blinky build configuration. In addition to these,<br /> the Full configuration also creates a lot of tasks from the set of<br /> [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)<br /> tasks.<br /> <br /> The standard demo tasks don't perform any particular function.<br /> Their purpose is firstly to test the FreeRTOS port, and secondly to<br /> provide examples of how to use the FreeRTOS API functions.<br /> <br /> The Full build configuration creates yet more timers that are neither<br /> part of the Blinky configuration, or the set of standard demo tasks.<br /> These additional tasks are described briefly below this table.<br /> <br /> In total, the full configuration creates approximately 45 tasks!<br /> Use the blinky build configuration if a simpler demo is required.<br /> <br /> |
| <br /> Full\_with\_optimisation<br />  | <br /> The functionality of the Full\_with\_optimisation configuration<br /> is identical to that of the Full configuration. The compiler<br /> optimisation setting is the only difference between the two.<br /> Full uses no optimisation, while Full\_with\_optimisation uses high<br /> optimisation.<br /> <br /> |

Software timers that are created by both Full build configurations, that are
not part of either the Blinky demo, or the standard demo tasks, include:

* A "Check" software timer and callback
 Each time the check timer expires, its associated callback function
 queries the status of all the running standard demo tasks. If a status is
 returned as 'failed', then the period of the Check timer is shortened
 to 500ms, from its original setting of 3 seconds.

 The check timer callback toggles an LED within the seven segment display
 each time it executes. The ["Blinky demo functionality"](#visible-blinky-demo-functionality)
 and [Full demo functionality](#visible-full-demo-functionality) sections of this
 documentation page highlight the LEDs used. If the LED toggles every three seconds, then no errors
 have been reported. If the LED toggles every 500ms, then at least one
 standard demo task has reported an error. The name of the standard demo task
 that reported the error is logged in the pcStatusMessage variable, which is
 defined in main-full.c.
* A "Digit Counter" software timer and callback
 This controls the display of an incrementing number on one of the two
 seven segment displays.

#### Hardware set up

The demo application includes tasks that send and receive characters over UART0.
The characters sent by one task are received by another - with an error condition
being flagged if any character is missed or received out of order. A loopback
connector is required on the 9way D socket marked X4 on the SK-FM3-100PMC development
board for this test to function (pins 2 and 3 the socket should be connected
together - a paper-clip is normally adequate for the purpose). Further, the jumpers
marked JP4 and JP5 must be set to route the UART0 signals to the X4 connector.
This requires them to be turned 90 degrees from their default position. JP4 and
JP5 are adjacent to the X4 connector, and their required position is visible in
the image at the top of this file (the jumpers should point to, and not be parallel
with, the connector).

Note that the UART driver in this demo uses queues to send each
character into an interrupt service routine, and out of an interrupt service routine,
individually. This is done to demonstrate queues being used in an interrupt,
and to deliberately load the system to test the FreeRTOS port. It is not meant
to be an example of an efficient driver implementation. An efficient
implementation should use FIFOs or DMA if available, and only use FreeRTOS API
functions when enough data has been received to warrant a task being unblocked to
process the data.

#### Building and executing the demo application, using the IAR tools

1. Open the [RTOSDemo\_IAR.eww](#source-code-organisation) Embedded Workbench workspace
 from within the Embedded Workbench IDE.
2. Select the required build configuration.
3. Select "Build All" from the Embedded Workbench "Project" menu - the demo
 application should build without errors.
4. When the build completes, select "Download and Debug" from the Embedded Workbench
 "Project" menu (or just press CTRL+D) to program the microcontroller flash memory,
 and start a debug session. The application will start to run, and then
 break on entry to the main() function.

#### Building and executing the demo application using Keil tools

1. Open the [RTOSDemo\_Keil.uvproj](#source-code-organisation) project from within
 the Keil IDE.
2. Select the required build configuration. Build configurations are
 called 'targets' in the uVision IDE.
3. Select "Build Target" from the IDE's "Project" menu - the demo application should
 build without errors.
4. When the build complete, select "Start/Stop Debug Session" from the IDE's
 "Debug" menu (or just press CTRL+F5) to program the microcontroller flash memory,
 and start a debug session.

#### Visible blinky demo functionality

![Spansion FM3 FreeRTOS blinky demo led assignment](/media/2018/FM3-blinky-demo-led-assignment.jpg)

 The LED assignment used by the "blinky" build configuration

When the "blinky" build configuration is executing correctly:

* The LED marked 'A' in the image above is used by the LED timer. This is
 the LED that will turn on when user button SW2 is pressed, and then turn
 off when SW2 has not been pressed for a full five seconds.
* The LED marked 'B' in the image above is used by the queue receive task.
 This is the LED that will toggle each time an item is received on the
 queue (and therefore toggle every 200ms).

#### Visible full demo functionality

![Spansion FM3 FreeRTOS full demo led assignment](/media/2018/FM3-full-demo-LED-assignment.jpg)

 The LED assignment used by the "full" build configurations

Only a few of the many tasks and timers that are created by the full demo have
externally observable behaviour. When the "full" build configurations are executing correctly,
the following behaviour will be observed:

* The LEDs marked A in the image above are under the control of the
 'digit counter' timer. These are the LEDs that will show a digit that
 repeatedly increments from 0 to 9.
* The LED marked B in the image above is under the control of the 'check' software timer.
 This is the LED that will toggle every 3 seconds if no errors have been reported,
 or every 500ms if a standard demo task has ever reported an error.
 This mechanism can be tested by removing the loopback connector, and in so doing
 deliberately generating an error in the standard demo 'comtest' tasks.
* The LEDs marked C in the image above are under the control of the standard
 demo 'comtest' tasks. One will toggle each time a character is transmitted,
 and the other each time the same character is received. The toggle rate
 is very rapid, and only just visible to the naked eye.
* The LED marked D in the image above is used by the LED timer. This is
 the LED that will turn on when user button SW2 is pressed, and then turn
 off when SW2 has not been pressed for a full five seconds.
* The LEDs marked E in the image above are under the control of the standard demo
 'flash' tasks. Each will toggle at a fixed frequency, with each of the
 three LEDs using a different frequency.
* The LED marked F in the image above is under the control of queue receive task.
 This is the LED that will toggle each time an item is received on the
 queue (and therefore toggle every 200ms).

---

### RTOS Configuration and Usage Details

#### Cortex-M3 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_MB9B500\_IAR\_Keil/FreeRTOSConfig.h (or
FreeRTOS/Demo/CORTEX\_MB9A310\_IAR\_Keil/FreeRTOSConfig.h)
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.

Attention please!: Remember that ARM Cortex-M3 cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0
and therefore the highest priority possible.

The lowest priority on a ARM Cortex-M3 core is in fact 255 - however different
Cortex-M3 vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on FM3 microcontrollers the lowest priority you can specify is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all four priority bits are assigned as
being preemption priority bits, and none as sub priority bits.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

This demo project provides examples of FreeRTOS interrupt service routines -
namely INT0\_7\_Handler() defined in main-full.c and main-blinky.c, and the
two UART interrupt handlers MFS0RX\_IRQHandler() and MFS0TX\_IRQHandler() defined in
serial.c.

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
configuration constant.

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the SysTick and PendSV interrupts. SVC number #0 is also used.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within RTOSDemo/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the FM3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
