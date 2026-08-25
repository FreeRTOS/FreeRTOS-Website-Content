---
title: "SAMA5D3 (ARM Cortex-A5) RTOS Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 SAMA5D3 (ARM Cortex-A5) RTOS Demo

 Including FreeRTOS-Plus-CLI - Using the IAR Embedded Compiler

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Atmel Cortex-A5 RTOS](/media/2018/SAMA5D3_Xplained.jpg)

### Introduction

This page documents a FreeRTOS demo application for the
Atmel ATSAMA5D3 embedded processor, which has an ARM Cortex-A5 core and an
Atmel Advanced Interrupt Controller (AIC). The pre-configured RTOS example
project builds uses the [IAR Embedded Workbench for ARM](http://www.iar.com/ewarm)
compiler and IDE, and targets the [SAMA5D3 Xplained](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D3-XPLD) evaluation board.

[![Atmel Cortex-A5 RTOS](/media/2018/SAMA5_ARM_Cortex-A5.png)](/media/2018/SAMA5_ARM_Cortex-A5.png)

**The RTOS State Viewer Windows in EWARM Running the SAMA5 RTOS Demo

 Click to Enlarge**

---

#### *IMPORTANT! Notes on using the FreeRTOS Atmel SAMA5 demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application Functionality](#the-atmel-sama5-arm-cortex-a5-demo-application)
3. [Build Instructions](#build-instructions)
4. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting), and
the page that provides instruction on
[using FreeRTOS on ARM Cortex-A processors that don't incorporate
a GIC](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller) [the SAMA5 uses Atmel's own Advanced
Interrupt Controller (AIC) rather than ARM's Generic Interrupt Controller (GIC)].

---

### Source Code Organisation

The FreeRTOS zip file contains source code for all the RTOS ports and all the
RTOS demo applications. Only a small subset of these files are required by the
Atmel SAMA5 ARM Cortex-A5 RTOS demo application. The [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page describes
the structure of the FreeRTOS zip file download, and provides information on
creating a new RTOS project.

The IAR Embedded Workbench project file is located in the FreeRTOS/Demo/CORTEX\_A5\_SAMA5D3x\_Xplained\_IAR
directory.

The IAR project includes
files that are contained in the /FreeRTOS-Plus directory, so the project will
not build if the /FreeRTOS-Plus directory has been deleted or moved from
its default location.

---

### The Atmel SAMA5 ARM Cortex-A5 Demo Application

#### Hardware and software set up

No specific hardware configuration is required.

#### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY,
which is defined at the top of main.c, is used to switch between a very basic
'blinky' demo, and a comprehensive test and demo application.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main() will
call main\_blinky().

main\_blinky() creates a very simple demo that includes two
tasks and one queue. The first task (the queue send task) uses the queue to
repeatedly send the number
100 to the second task (the queue receive task). The receiving task toggles an
LED each time it receives
the message. The message is sent every 200 milliseconds, so the LED toggles
every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

[![Atmel Cortex-A5 RTOS](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

**Run Time Stats Viewed in the CLI

 Click to Enlarge**

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main() will
call main\_full().

main\_full() creates a comprehensive test and demo application
that demonstrates:

* The [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 command line interface.
* The Atmel USB device CDC driver.
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).

The virtual COM port created by the
USB CDC driver is used as the input and output interface for the CLI.
The .inf file required to install the virtual COM port on a Windows machine is
called 6119.inf, and is located in the same directory as the IAR project.
Use the enumerated
virtual COM port to connect to FreeRTOS-Plus-CLI through a dumb terminal program,
such as [Tera Term](http://en.sourceforge.jp/projects/ttssh2/releases/)
or Hyperterminal, at 115200 baud. As always with FreeRTOS-Plus-CLI, type 'help' in the
CLI to see a list of the registered commands.

The SAM5 ARM Cortex-A5 Xplained evaluation board is powered through its USB device port,
so the USB CDC device will enumerate as soon as the RTOS demo application starts
executing, and will re-enumerate each time the RTOS demo application is restarted.
This means a terminal program cannot be connected to the virtual COM port until
the RTOS application is running, and must be disconnected from and then reconnected
to the virtual COM port each time the RTOS demo application is stopped and re-started.

Most of the other tasks created by the full demo are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. These are used by all the RTOS demo applications for all compilers and
all architectures. They have no specific functionality, but do demonstrate the RTOS
API being used and test the RTOS kernel port.

Finally, a 'check' task is created. The check task periodically queries the standard RTOS
demo tasks to ensure the standard demo tasks are still executing and functioning as expected.
The check task also toggles an LED to give a visual indication of the system status.
**If the check task has not detected any potential errors then it will toggle
the LED every three seconds. If the check task has
detected a potential error then it will toggle the LED every 200ms**.

**NOTE:** Some of the standard demo tasks check their own timing, and the timing
checks will fail (resulting in an error being reported to the 'check' task)
if excessive time is spent processing USB interrupts.

---

### Build Instructions

#### Building and executing the demo application

Note that the RTOS demo project references common files from the /FreeRTOS-Plus
and /FreeRTOS/Demo/Common directories, so the project will not compile
if /FreeRTOS-Plus has been deleted or moved from its default location.
1. Open FreeRTOS/Demo/CORTEX\_A5\_SAMA5D3x\_Xplained\_IAR/RTOSDemo.eww
 from within the Embedded Workbench (EWARM) IDE.
2. Open main.c and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simple blinky demo or the full test and demo application as required.
3. Select "Build All" from the IDE's "Project" menu, or press F7, to build
 the demo. The demo should build without the FreeRTOS related files
 generating any errors or warnings.
4. Ensure the target hardware is connected to the host computer using the
 target's USB connector.
5. Select "Download and Debug" from the IDE's "Project" window to download
 the built executable to the ARM Cortex-A5 RAM and start a debug session.

---

### RTOS Configuration and Usage Details

#### FreeRTOS ARM Cortex-A port specific configuration

Attention please!: Some ARM Cortex-A processors
incorporate ARM's own Generic Interrupt Controller (GIC), while others, such as
the SAMA5D3, incorporate proprietary interrupt controllers. Separate web pages
are provided to give instructions on using the RTOS in both scenarios. In this
case please refer to the web page that provides
[instruction
on using the RTOS on ARM Cortex-A embedded processors that do not incorporate
ARM's Generic Interrupt Controller](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller).

Configuration items specific to this demo are contained in the
FreeRTOS/Demo/CORTEX\_A5\_SAMA5D3x\_Xplained\_IAR/FreeRTOSConfig.h header
file.

#### Resources used by FreeRTOS

This demo is configured to generate the RTOS tick interrupt from the PIT (Periodic
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
