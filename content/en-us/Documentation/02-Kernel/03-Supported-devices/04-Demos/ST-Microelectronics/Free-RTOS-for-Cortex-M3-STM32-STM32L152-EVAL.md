---
title: "FreeRTOS Demo for the ST STM32L152 ARM Cortex-M3 Microcontroller"
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
| <br />![](/media/2018/FreeRTOS-running-on-an-STM32L154-EVAL-evaluation-board.jpg)<br /> |

### Introduction

 [[Also see the project that demonstrates how the FreeRTOS tickless mode can
 be used to minimise the power consumption of an application running on an
 STM32L](STM32L-discovery-low-power-tickless-RTOS-demo)]

This page documents the FreeRTOS demo application for the low power [STM32L152 microcontroller](http://www.st.com/internet/mcu/product/248824.jsp) from
[STMicroelectronics](http://www.st.com/). The demo uses the [IAR Embedded Workbench for ARM V6.10](http://www.iar.com/ewarm)
from IAR Systems, and targets the official [STM32L152-EVAL](http://www.st.com/internet/com/TECHNICAL_RESOURCES/TECHNICAL_LITERATURE/USER_MANUAL/CD00288880.pdf)
evaluation board from STMicroelectronics ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)
are provided should you wish to use an alternative development board).

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

The FreeRTOS state viewer plug-in is pre-installed in version 6.10, removing
the requirement to install it manually.

#### FreeRTOS features demonstrated by the project presented on this page

The project demonstrates the following FreeRTOS features and techniques:
* The 'gatekeeper' task design pattern

 The demo LCD task is the only task that is permitted to access the LCD.
 Other tasks and interrupts that want to write messages to the LCD do
 not do so directly, but instead by sending the message to the LCD task.
* The 'controller' task design pattern

 The demo LCD task also demonstrates the 'controller' task concept.
 Messages that are sent to the LCD contain both a message type and a
 message value parameter. The LCD task knows what to do with the message
 value (which can be an integer, character pointer, or anything else) by
 interpreting at the message type.
* Controlled (not free running) polling of an input

 A demo button polling task uses the time delaying features of FreeRTOS
 to control the rate at which it reads a button input state. This
 removes the need for complex button debouncing, and prevents the task
 from utilising all of the available CPU time.
* (Effectively and indirectly) Writing to the LCD from an interrupt service routine

 Slow output devices such as LCDs cannot normally be used efficiently from an
 interrupt service routine. In this demo the joystick select button is
 used to generate an external interrupt, and the interrupt service routine
 sends a string to the LCD indirectly by sending it to the LCD task on
 a message queue.
* Gathering and displaying run time statistics

 Run time statistics provide information on the amount of time each task
 has spent in the Running state. Times are given as an absolute value,
 and as a percentage of the total run time.
* Interrupt nesting

 The priority of the USART3 Rx and Tx interrupts are set above the
 priority of any other interrupt used in the system (including the
 interrupts used by the RTOS kernel itself). The USART3 interrupts will therefore
 interrupt (nest with) any other interrupt.
* An Idle task hook function

 The idle task hook is used to place the processor into a low power
 state. Note however that the demo is implemented using standard
 task implementations that are used by many different demos, and is
 therefore not optimised for low power operation. Lower power consumption
 would be achieved by converting polling tasks into event driven tasks,
 and slowing the tick interrupt frequency.
* A tick interrupt hook function

 The tick interrupt hook is used to implement 'watchdog' type functionality.
 It monitors all the other tasks in the system to look for any unexpected
 behaviour. It then sends either a PASS or an error code status message
 to the LCD/Controller demo task. The LCD/Controller demo task uses the
 message type member of its received message to interpret the message as
 a status message, then uses the message value member of its received
 message to determine the status string to write to the LCD.
* A malloc() failed hook function

 The malloc() failed hook will trap calls to pvPortMalloc()
 that fail because there is not enough FreeRTOS heap memory available
 for the allocation to complete.
 pvPortMalloc() can be called from application tasks, but is also called
 from FreeRTOS API functions that create tasks, queues and semaphores.
* Querying the amount of FreeRTOS heap memory that remains unallocated

 xPortGetFreeHeapSize() is called from a task (after the RTOS scheduler has been
 started), and outputs the amount of FreeRTOS heap memory that remains
 unallocated (and therefore available) to the terminal IO window within
 the IAR Embedded Workbench IDE.

---

#### *IMPORTANT! Notes on using the STM32 ARM Cortex-M3 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports so
includes many more files than are required for this demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The IAR workspace file for the STM32L152 demo is called RTOSDemo.eww
and is located in the FreeRTOS/Demo/CORTEX\_STM32L152\_IAR directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes an interrupt driven UART test. This creates two
tasks, a transmit task and a receive task. The transmit task transmits characters
on USART3, and the receive task receives characters on USART3. The receive task
expects to receive the characters transmitted by the transmit task, so for correct
operation a loopback connector must be fitted to the USART3/CN5 connector of the
STM32L152-EVAL evaluation board (pins 2 and 3 must be connected together on
the CN5 9Way connector). Further, the USART3 related jumpers JP5, JP7 and JP8
must be set to short the jumper pins 2 and 3 (not set to
short pins 1 and 2).

The demo application also uses all four LEDs that are built onto the STM32L152-EVAL
board. Jumpers JP18 and JP19 must be closed (shorted) for LED3 and LED4 to be
functional.

The port was developed and tested using a J-Link USB JTAG interface connected to
CN8 on the target hardware. The evaluation hardware also provides a
built in ST-Link debug interface that can be accessed using the USB connector
marked ST-Link/CN11.

#### Building and running the demo application

1. Open the FreeRTOS/Demo/CORTEX\_STM32L152\_IAR/RTOSDemo.eww project from within the Embedded Workbench IDE.
2. Select 'Rebuild All' from the IDE 'Project' menu. The project should build with no errors or warnings.
3. Select 'Debug' from the IDE 'Project' menu. The microcontroller flash memory will be programmed with the newly built binary and the debugger will break on
 the entry to main().

#### Functionality

The top of this documentation page lists the FreeRTOS features that are demonstrated
by the STM32L152 demo project. The comments contained in the main.c
source file provide more information on how this functionality is implemented
and achieved.

The following behaviour will be observed when the demo is executing normally:

* LEDs LED1, LED2 and LED3 are under the control of the standard 'flash'
 tasks. Each will toggle with a fixed but different frequency. LED1
 will toggle with the highest frequency and LED3 with the lowest
 frequency.
* LED 4 will toggle each time the COM test transmit task transmits a
 character.
* Every 5 seconds a status message will be written to the LCD. If the
 demo is executing without error then the status will be reported as
 PASS. In all other cases the status message will indicate which task
 or test has reported an error. This functionality can be tested
 by removing the loopback connector from the USART3/CN5 connector, and
 in so doing deliberately generating an error in the COM test tasks.
* Pressing or releasing the joystick 'up' button will result in a message
 being displayed on the LCD that indicates the button state (0 for
 pressed and 1 for released).
* Pressing the joystick select button (pressing the joystick button
 directly downward toward the PCB on which it is mounted) will result
 in a message being displayed on the LCD indicating that a button interrupt
 has been generated. It will also result in run time statistics (the
 amount of time each task has spent in the Running state since the demo
 was booted) being output to the terminal IO window of the Embedded
 Workbench IDE (see the screen shot below).

The image below is a screen shot taken during a debugging session. The FreeRTOS
state viewer Tasks and Queues windows can be seen at the bottom of the
screen shot. Run time statistics information can be see in the terminal IO
window.

![FreeRTOS STM32L152 Debug Session Screen Shot](/media/2018/FreeRTOS-STM32L152-Debug-Session-Screen-Shot.jpg)

**Screen shot taken during a FreeRTOS debugging session.
The FreeRTOS
 state viewer plug in windows can be seen at the bottom of the screen shot.

 Run time statistics information can be seen in the terminal IO window.**

---

### RTOS Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_STM32L154\_IAR/FreeRTOSConfig.h. The
constants defined in this file can be edited to meet the needs of your application. In particular -

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
on the STM32 the lowest priority you can specify in an ST driver library call
is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all four priority bits are assigned as
being preemption priority bits. This can be ensured by passing
"NVIC\_PriorityGroup\_4" into the ST library function NVIC\_PriorityGroupConfig().
In the demo project this is done from the function prvSetupHardware(), which is
itself defined in main.c.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

This demo project provides examples of FreeRTOS interrupt service routines -
namely TIM6\_IRQHandler() defined in main.c and USART3\_IRQHandler() defined in
serial.c. Note that USART3\_IRQHandler() is implemented to stress the port and
demonstrate queues being used from interrupts - it is not intended to be a demonstration
of an efficient interrupt service routine!

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_STM32L154\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
