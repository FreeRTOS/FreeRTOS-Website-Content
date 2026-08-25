---
title: Build your first FreeRTOS project
created: 2018-09-20
categories:
  - kernel
description: How to start your own project to build FreeRTOS
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS
  - title: FreeRTOS implementation tutorial
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS reference manual
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
  - title: Modifying a FreeRTOS demo
    link: /Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos/


previous:
  title: RTOS Fundamentals
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
next:
  title: FreeRTOS libraries and 3rd party tools
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools
---


## Introduction

FreeRTOS is designed to be simple and easy to use: Only 3 source files that are
common to all RTOS ports, and one microcontroller specific source file are
required, and its API is designed to be simple and intuitive.

FreeRTOS is [ported to many different microcontroller architectures](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices), and many
different compilers. Each official port comes with an official demo that (at
least at the time of its creation) compiles and executes on the hardware platform
on which it was developed without any modification.

The demo projects are provided to ensure new users can get started with FreeRTOS
in the quickest possible time, and with the minimum of fuss.

Each architecture supported by FreeRTOS is used in many different microcontrollers,
meaning FreeRTOS can be used with literally thousands of different microcontroller
part numbers. Multiplying this number by the number of supported compilers, and
then multiplying again by the ever increasing number of starter kits and evaluation boards
that are being brought to the market, and it is obvious that, despite our best
efforts, we can only provide official demo projects that exactly match a tiny
fraction of possible combinations.

**It is always recommended that a new FreeRTOS project is created by
[starting with, and then adapting, one of the provided pre-configured demos](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos).
Doing this ensures the new project includes all the necessary source and header files, and installs the necessary interrupt service
routines, with no effort on the part of the project's creator.**

Some FreeRTOS users also want to know how to create FreeRTOS projects by means
other than adapting an existing project. The procedure for doing this is
documented below.

## Getting Started with Simple FreeRTOS Demo Projects

[See also the [Quick Start Guide](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide) and the demo application [introduction page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview).]

### Try It Now, Using the Windows or Linux Port, or in QEMU

No hardware yet? Don't worry - you can run a simple blinky demo in a Windows or Linux environment using
free tools and the FreeRTOS Windows or Linux port - although neither of these RTOS ports will exhibit
true real time behaviour.
Alternatively [run the demo using the FreeRTOS Arm Cortex-M3 port in QEMU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model).

If you are a beginner, then don't read the main documentation pages for either
the [Windows](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
or [Linux](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux) RTOS ports yet, and start by configuring the example to use
the [blinky demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration) (ignore the [comprehensive demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)
for now). Detailed instructions for Windows follows.


### Instructions for Windows

![Simple FreeRTOS demo using Windows](/media/2018/FreeRTOS_Windows_Blinky.jpg)

1. If you don't already have it installed, download and install
   the [free version of Microsoft Visual Studio](https://visualstudio.microsoft.com/vs/community).
2. If you have not done so already, clone the [FreeRTOS/FreeRTOS repository](https://github.com/FreeRTOS/FreeRTOS).
3. Start Visual Studio, then use the File|Open|Project/Solution menu item
   to open the Win32.sln solution file, which is located in the
   FreeRTOS/Demo/WIN32-MSVC directory of the official FreeRTOS distribution.
4. Find the definition of mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY at the top of
   main.c, and make sure it is set to 1.
5. Read the comments at the top of main\_blinky.c, before compiling and then
   either debugging or running the application.

![Output generated by simple RTOS demo under Windows](/media/2018/RTOS_Windows_Output.jpg)   
*The output produced by the FreeRTOS Windows port simple blinky demo*

## Anatomy of a FreeRTOS Project

A FreeRTOS application will start up and execute just like a non-RTOS application
until [vTaskStartScheduler()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler) is called. vTaskStartScheduler()
is normally called from the application's main() function. The RTOS only controls
the execution sequencing after vTaskStartScheduler() has been called.

It is **highly recommended** to ensure that code is executing correctly
(correct start up code, correct linker configuration, etc.) on the chosen target
before attempting to use any RTOS functionality.


### Source Files

FreeRTOS is supplied as standard C source files that are built along with all
the other C files in your project. The FreeRTOS source files are distributed in
a zip file. The [RTOS source code organisation](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page
describes the structure of the files in the zip file.

As a minimum, the following source files must be included in your project:

* FreeRTOS/Source/tasks.c
* FreeRTOS/Source/queue.c
* FreeRTOS/Source/list.c
* FreeRTOS/Source/portable/[compiler]/[architecture]/port.c.
* FreeRTOS/Source/portable/MemMang/heap\_x.c [where 'x' is 1, 2, 3, 4 or 5](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).

If the directory that contains the port.c file also contains an assembly language file,
then the assembly language file must also be used.


### Optional Source Files

If you need [software timer](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) functionality, then add FreeRTOS/Source/timers.c to your project.

If you need [event group](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) functionality, then add FreeRTOS/Source/event\_groups.c to your project.

If you need [stream buffer or message buffer](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers) functionality, then add
FreeRTOS/Source/stream\_buffer.c to your project.

If you need co-routine functionality, then add FreeRTOS/Source/croutine.c to your project (note co-routines are deprecated
and not recommended for new designs).


### Header Files

The following directories must be in the compiler's include path (the compiler must be told to search these directories
for header files):

* FreeRTOS/Source/include
* FreeRTOS/Source/portable/[compiler]/[architecture].
* Whichever directory contains the FreeRTOSConfig.h file to be used - see the Configuration File paragraph below.

Depending on the port, it may also be necessary for the same directories to be in the assembler's include path.


### Configuration File

Every project also requires a file called [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization). FreeRTOSConfig.h
tailors the RTOS kernel to the application being built. It is therefore specific
to the application, not the RTOS, and should be located in an application directory,
not in one of the RTOS kernel source code directories.

If heap\_1, heap\_2, heap\_4 or heap\_5 is included in your project, then the FreeRTOSConfig.h
definition configTOTAL\_HEAP\_SIZE will dimension the FreeRTOS heap. Your application
will not link if configTOTAL\_HEAP\_SIZE is set too high.

The FreeRTOSConfig.h definition configMINIMAL\_STACK\_SIZE sets the size of the
stack used by the idle task. If configMINIMAL\_STACK\_SIZE is set too low, then
the idle task will generate stack overflows. It is advised to copy the
configMINIMAL\_STACK\_SIZE setting from an official FreeRTOS demo provided for the
same microcontroller architecture. The FreeRTOS demo
projects are stored in sub directories of the FreeRTOS/Demo directory.
Note that some demo projects are old, so they do not contain all the available
configuration options.

Application writers can use the [FreeRTOSConfig.h template](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/examples/template_configuration/FreeRTOSConfig.h)
as a starting point to create the FreeRTOSConfig.h file for their application.

### Interrupt Vectors

**[Cortex-M users: Information on installing interrupt handers is provided
in the "[The application I created compiles, but does not run](/Why-FreeRTOS/FAQs/Troubleshooting)" FAQ]**

Every RTOS port uses a timer to generate a periodic tick interrupt. Many ports use additional interrupts
to manage context switching. The interrupts required by an RTOS port are serviced by the provided RTOS
port source files.

The method used to install the interrupt handlers provided by the RTOS port is dependent on the port
and compiler being used. Refer to, and if necessary copy, the provided official demo application for
the port being used. Also refer to the [documentation page provided](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) for the official demo
application.
