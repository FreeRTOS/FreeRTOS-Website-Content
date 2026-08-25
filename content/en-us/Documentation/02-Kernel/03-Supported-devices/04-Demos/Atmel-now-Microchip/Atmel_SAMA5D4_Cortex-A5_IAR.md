---
title: "SAMA5D4 (ARM Cortex-A5) RTOS Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 SAMA5D4 (ARM Cortex-A5) RTOS Demo

 Including FreeRTOS-Plus-CLI, and Using the IAR Embedded Compiler

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Atmel Cortex-A5 RTOS](/media/2018/SAMA5D4_EK.jpg)

### Introduction

This page documents the FreeRTOS demo for the
Atmel ATSAMA5D4 embedded processor, which has an ARM Cortex-A5 core, and uses the
Atmel Advanced Interrupt Controller (AIC). A pre-configured RTOS example
project that targets the
[SAMA5D4-EK](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D4-EK)
evaluation hardware is provided for the
[IAR Embedded Workbench for ARM](http://www.iar.com/ewarm)
embedded development tools.

[![Atmel Cortex-A5 RTOS](/media/2018/SAMA5_ARM_Cortex-A5.png)](/media/2018/SAMA5_ARM_Cortex-A5.png)

**The RTOS State Viewer Windows in EWARM Running the SAMA5 RTOS Demo

 Click to Enlarge**

---

#### *IMPORTANT! Notes on using the ARM Cortex-A5 RTOS demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application Functionality](#the-atmel-sama5d4-arm-cortex-a5-demo-application)
3. [Build Instructions](#build-instructions)
4. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also:
* The FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)
* Instruction on using the RTOS on
 [ARM Cortex-A processors that don't use a Generic Interrupt Controller (GIC)](/Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller).

---

### Source Code Organisation

The official FreeRTOS zip file download includes source files for all the RTOS
ports, and all the RTOS demo projects. Only a small subset of the files are
required by this Atmel SAMA5D4 ARM Cortex-A5 RTOS demo application. The
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page describes
the structure of the FreeRTOS zip file download, and provides information on
creating a new RTOS project.

The IAR Embedded Workbench project used to build this demo is located in the
FreeRTOS/Demo/CORTEX\_A5\_SAMA5D4x\_EK\_IAR directory. The project includes
source files from the /FreeRTOS-Plus/Source directory, so will not build
if the /FreeRTOS-Plus directory has been moved from its default location,
or deleted.

---

### The Atmel SAMA5D4 ARM Cortex-A5 Demo Application

#### Hardware and software set up

No hardware configuration specific to this demo is required.

#### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is used to switch between a
basic 'blinky' style demo, and a larger test and demo application.
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined at the top of main.c.

#### Functionality when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 main() calls main\_blinky().

main\_blinky() creates a very basic demo that creates just two
tasks and one queue. The first task (the queue send task) repeatedly sends the
number 100 to the second task (the queue receive task) over the queue. The
queue receive task toggles an LED each time it receives
the data. The data is sent to the queue every 200 milliseconds, so the queue
receive task will toggle the LED every 200 milliseconds.

#### Functionality when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

[![Atmel Cortex-A5 RTOS](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

**Run-time stats viewed in the CLI

 Click to Enlarge**

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().

main\_full() creates a comprehensive demo and test application that demonstrates:

* The [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 command line interface and interpreter.
* Atmel's own USB CDC driver - which provides the input and output for the CLI.
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).

The .inf file necessary to install the CDC virtual COM port on a Windows computer is
called 6119.inf, and is located in the same directory as the IAR project.
A dumb terminal program, such as
[Tera Term](http://en.sourceforge.jp/projects/ttssh2/releases/)
or Hyperterminal, can be used to connect to the CLI via the enumerated virtual
COM port. 115200 baud is used.
As always with FreeRTOS-Plus-CLI, type 'help' in the CLI to see a list of the
registered commands.

The USB CDC device will enumerate as soon as the RTOS demo application starts
executing, and will re-enumerate each time the RTOS demo application is restarted.
That means a terminal program cannot be connected to the virtual COM port until
the RTOS application is actually running, and must be disconnected from, and then
reconnected to, the CDC virtual COM port each time the RTOS demo is re-started.
If the dumb terminal is not disconnected from the CDC port before the RTOS demo
is stopped or restarted then it might be necessary to shut down and restart the
dumb terminal program before another connection can be created.

Many of the other tasks created in the full demo are from the set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview).
The standard demo tasks are used by the RTOS demos applications for every RTOS port,
and have no specific functionality. Their purpose is to demonstrate the RTOS
API functions being used, and test the RTOS architecture port.

The demo also creates a 'check' task. The check task periodically inspects the
status of the standard RTOS demo tasks to ensure they are functioning as expected.
The check task toggles an LED to give a visual indication of the system status;
**If the LED is toggling every 3 seconds then all the tasks are executing as
expected. If the LED is toggling every 200ms then the check task has detected
a possible error in one or more of the demo tasks.**.

**NOTE:** Some of the standard demo tasks check their own timing, and the timing
checks will fail (resulting in an error being reported to the 'check' task)
if excessive time is spent processing USB interrupts.

---

### Build Instructions

#### Building and executing the RTOS demo application

Note the RTOS demo project references common files from the /FreeRTOS-Plus
and /FreeRTOS/Demo/Common directories and will not compile
if either of these directories have been deleted or moved from their default
locations.
1. Open FreeRTOS/Demo/CORTEX\_A5\_SAMA5D4x\_EK\_IAR/RTOSDemo.eww
 in the IAR Embedded Workbench (EWARM) IDE.
2. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY at the top of main.c to generate either
 the simple blinky demo, or the full test and demo application, as
 described above.
3. Select "Build All" from the IDE's "Project" menu, or press F7, to build
 the RTOS demo.
4. Ensure the target hardware is powered, and connected to the host computer
 using both the target's J-Link USB connection for the debugger, and (if running the full
 demo with CLI), the target's USB-A connection.
5. Select "Download and Debug" from the IDE's "Project" window. The
 built executable with be downloaded to the ARM Cortex-A5 RAM before a
 debug session is started.

---

### RTOS Configuration and Usage Details

#### FreeRTOS ARM Cortex-A port specific configuration

Attention please!:

The SAMA5D4 uses a proprietary Atmel interrupt controller, rather than ARM's own
Generic Interrupt Controller (GIC). Separate web pages
provide instruction on using the RTOS in both scenarios. When using the SAMA5D4
please refer to the web page that provides
[instruction
on using the RTOS on ARM Cortex-A embedded processors that do not incorporate
an ARM GIC](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller).

Configuration items specific to this demo are contained in the
FreeRTOS/Demo/CORTEX\_A5\_SAMA5D4x\_EK\_IAR/FreeRTOSConfig.h header
file.

#### Resources used by FreeRTOS

The RTOS demo is configured to generate the RTOS tick interrupt from the PIT (Periodic
Interrupt Controller). Other resources used by the RTOS are documented on the
page that provides
[instruction
on using the RTOS on ARM Cortex-A embedded processors that do not incorporate
ARM's Generic Interrupt Controller](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller), as already referenced.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-A demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
