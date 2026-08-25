---
title: "FreeRTOS Demo for the TI MSP430F5438 (MSP430X) Microcontroller Using the IAR Embedded Workbench"
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
| <br />![FreeRTOS running on an MSP 430F5438 Experimenter board](/media/2018/FreeRTOS-running-on-an-MSP-430F5438-Experimenter-board.jpg)<br /> |

### Introduction

This page documents the FreeRTOS demo application for the [MSP430X / MSP430F5438 microcontroller](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html) from
[Texas Instruments](http://www.ti.com/). The demo uses the [IAR Embedded Workbench for MSP430](https://www.iar.com/products/architectures/iar-embedded-workbench-for-msp430/)
from IAR Systems, and targets the official [MSP-EXP430F5438](http://focus.ti.com/docs/toolsw/folders/print/msp-exp430f5438.html)
experimenter board from TI ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)
are provided should you wish to use an alternative development board).

It is recommended **not** to attempt to open the demo project in an IAR Embedded Workbench
version that is earlier than V5.20 as to do so can silently corrupt the project file.

The port and demo project were developed and tested using both the 'Large' and 'Small' data models. The [build configurations table](#building-and-running-the-demo-application) below contains important information
on using the small data model.

#### Features of FreeRTOS that are demonstrated by this demo project

The project demonstrates the following FreeRTOS features and techniques:
* The 'gatekeeper' task design pattern

 The demo LCD task is the only task that is permitted to access the LCD,
 so is the LCD 'gatekeeper'. Other tasks **and interrupts** that want
 to write strings to the LCD do not access the LCD directly, but instead
 send the string they wish to display to the LCD task using a FreeRTOS
 queue.
* The 'controller' task design pattern

 The LCD task also demonstrates the 'controller' task design pattern.
 Messages that are sent to the LCD are structures that contain both a
 message type and a message value parameter. The LCD task knows what to
 do with the message value (which can be an integer, character pointer,
 or anything else) by first inspecting the message type.
* Controlled (not free running) polling of an input

 A button polling task uses the vTaskDelay() FreeRTOS API function
 to control the rate at which it reads a button input. This
 removes the need for complex button debouncing, as well as preventing
 the task from utilising all of the available processing time.
* (Effectively and indirectly) Writing to the LCD from an interrupt service routine

 Slow output devices such as LCDs cannot normally be accessed efficiently from an
 interrupt service routine. In this demo the joystick select button is
 used to generate an external interrupt, and the interrupt service routine
 sends a string to the LCD indirectly by sending it to the LCD task on
 a message queue. This is using the LCD task as a 'gatekeeper' task as
 described above.
* Gathering and displaying run time statistics

 Run time statistics provide information on the amount of processing time
 allocated to each task since the embedded target was booted. Times are
 provided both as an absolute value and as a percentage of the total run
 time.
* An Idle task hook function

 The demo makes use of the idle task hook to place the processor into a
 low power state. Note however that the demo is implemented using standard
 task implementations that are used by many different demos, and is
 therefore not optimised for low power operation. Lower power consumption
 would be achieved by converting polling tasks into event driven tasks,
 and slowing the tick interrupt frequency.
* A tick interrupt hook function

 The demo makes use of the tick interrupt hook to implement 'watchdog'
 type functionality. It monitors all the other tasks in the system to
 look for any unexpected behaviour. It then sends either a PASS or an
 error code status message to the LCD/Controller task. The LCD/Controller
 demo task uses the message type member of the message it receives to
 interpret the message as a status message, then uses the message value
 member of the same message to determine which status string it should
 write to the LCD.
* A malloc() failed hook function

 The malloc() failed hook will be called when a call to pvPortMalloc()
 fails because there is not enough FreeRTOS heap memory available
 for the allocation to complete.
 pvPortMalloc() can be called from application tasks, but is also called
 from FreeRTOS API functions that create tasks, queues and semaphores.
* Querying the amount of FreeRTOS heap memory that remains unallocated

 xPortGetFreeHeapSize() is called from a task after the RTOS scheduler has been
 started and outputs the amount of FreeRTOS heap memory that remains
 unallocated (the amount of heap memory that is still available) to the
 terminal IO window of the IAR Embedded Workbench IDE.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the MSP430X IAR Demo*

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

The IAR workspace file for the MSP430F5438 demo is called RTOSDemo.eww
and is located in the FreeRTOS/Demo/MSP430X\_MSP430F5438\_IAR directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes an interrupt driven UART test. This creates two
tasks, a transmit task and a receive task. The transmit task transmits characters
on UCA1, and the receive task receives characters on the same UCA1 peripheral. The receive task
expects to receive the characters transmitted by the transmit task, but as there
is no external 9 way connector, the hardware is internally configured to use a
loopback mode. Therefore, unlike other FreeRTOS demos, it is not necessary to
fit an external loopback connector to the UART for the COM port test to work.

**Note** that the implementation of the UART interrupt service routine is provided to demonstrate the use
of queues from inside an interrupt service routine. It is **not** intended to
be an example of an efficient interrupt implementation. A real application should make use
of the DMA. Or, as a minimum, transmission and reception could use a simple
RAM ring buffer, and synchronise with a task using a semaphore when a complete
message has been received or transmitted.

The port was developed and tested using a Texas Instruments MSP-FET430UIF USB
debug interface.

#### Building and running the demo application

The IAR project contains three build configurations. All the build configurations
demonstrate the same functionality, but with different run time models and optimisation
settings as described in the table below.

|  |  |
| --- | --- |
| **Build configuration** | **Description** |
| <br /> Debug\_Large\_Data\_Model<br />  | <br /> Configured to use the large data model with zero optimisation<br />  |
| <br /> Release\_Large\_Data\_Model<br />  | <br /> Configured to use the large data model with maximum optimisation.<br />  |
| <br /> Debug\_Small\_Data\_Model<br />  | <br /> Configured to use the small data model with zero optimisation.<br /> <br />**Note:** The small data model is selected using the usual IAR<br /> project target configuration options. **In addition to this**,<br /> FreeRTOS is configured to use the small data model by defining<br /> the assembler preprocessor symbol "\_\_DATA\_MODEL\_SMALL\_\_". This is<br /> an assembler preprocessor symbol, not a compiler preprocessor<br /> symbol.<br />  |

1. Open the FreeRTOS/Demo/MSP430X\_MSP430F5438\_IAR/RTOSDemo.eww workspace from within the Embedded Workbench IDE.
2. Select 'Rebuild All' from the IDE 'Project' menu. The project should build with no errors or warnings.
3. Select 'Debug' from the IDE 'Project' menu. The MSP430X flash memory will be programmed with the newly built binary. The debugger will then start and run to the main() function.

#### Functionality

The top of this web page lists the FreeRTOS features that are demonstrated
by the MSP430X5438 demo project. The comments contained in the main.c
source file provide more information on how this functionality is implemented
and achieved.

The following behaviour will be observed when the demo is executing correctly:

* LED 2 will toggle each time the COM test transmit task transmits a
 character.
* LED 1 is controlled from the tick interrupt hook function and is used
 to indicate that the tick interrupt is running. It will toggle every
 0xFF milliseconds.
* A status message will be displayed on the LCD every 5 seconds. If the
 demo is executing without error then the status will be displayed as
 PASS. In all other cases the status message will indicate which task
 or test has reported an error.
* Pressing or releasing the joystick 'up' button will cause a string
 to be displayed on the LCD. The string will indicate the button state.
* Pressing the joystick select button (pressing the joystick button
 directly downward toward the PCB on which it is mounted) will result
 in a message being displayed on the LCD indicating that a button interrupt
 has been generated. It will also result in run time statistics (the
 amount of time each task has spent in the Running state since the demo
 was booted) being output to the terminal IO window of the Embedded
 Workbench IDE (see the screen shot below).

**Note:** Writing the run time statistics to the IAR Embedded Workbench
 terminal IO window can take several seconds. The demo application will
 be halted during this period, and the LCD message will not appear until
 after the demo application resumes.

The image below is a screen shot taken during a debugging session. The FreeRTOS
state viewer Tasks and Queues windows can be seen at the bottom of the
screen shot. Run time statistics information can be see in the terminal IO
window.

![FreeRTOS MSP430X Debug Session Screen Shot](/media/2018/FreeRTOS-MSP430X-Debug-Session-Screen-Shot.jpg)

**Screen shot taken during a FreeRTOS debugging session.
The FreeRTOS
 state viewer plug in windows can be seen at the bottom of the screen shot.

 Run time statistics information can be seen in the terminal IO window.**

---

### RTOS Configuration and Usage Details

#### Configuring the RTOS tick interrupt

FreeRTOS requires exclusive use of a timer that is capable of generating a fast
periodic interrupt called the RTOS 'tick' interrupt. The timer is configured in
a user definable hook (or callback) function, so giving the application writer
the flexibility to decide which timer peripheral is actually used. The name and
prototype of the hook function is shown below:

void vApplicationSetupTimerInterrupt( void );

The constant configTICK\_VECTOR must be set to the interrupt vector number of the
chosen peripheral. configTICK\_VECTOR is defined in the FreeRTOSConfig.h header
file. This demo project includes an implementation of
vApplicationSetupTimerInterrupt() that configures time TA0 to generate the tick
interrupt and therefore sets configTICK\_VECTOR to TIMER0\_A0\_VECTOR. The provided
code will have to be modified only if the application being developed needs TA0
to be free for some other purpose.

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/MSP430X\_MSP430F5438\_IAR/FreeRTOSConfig.h. The
constants defined in this file can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type short.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements and can be written as per the compiler documentation.
The macro portYIELD\_FROM\_ISR() can be used to request a context switch from within an ISR.
Note that portYIELD\_FROM\_ISR() **must** be the last statement in the ISR.

This demo project provides examples of FreeRTOS interrupt service routines -
namely prvSelectButtonInterrupt() defined in main.c and prvUSCI\_A0\_ISR() defined in
serial.c. Note that prvUSCI\_A0\_ISR() is implemented to stress the port and
demonstrate queues being used from interrupts - it is not intended to be a demonstration
of an efficient or a generic interrupt service routine!

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/MSP430X\_MSP430F5438\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
