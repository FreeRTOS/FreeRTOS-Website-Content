---
title: "FreeRTOS Demo Applications"
created: 2018-09-20
categories:
  - kernel
description: An introduction to FreeRTOS Demo applications
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

### Introduction

The RTOS source code download includes a pre-configured
demonstration project for each RTOS port. The demo targets the evaluation board used for that port's development.
At the time of its creation, each preconfigured project built directly as downloaded without any warnings or errors, although subsequent
tooling changes may mean that is no longer the case. There is also a [separate page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/Hardware-independent-RTOS-example)
that describes how to create a hardware independent demo project.

The demonstration projects are provided as:

1. **An aid to learning how to use FreeRTOS** - each source file demonstrates a component of the RTOS.
2. **A preconfigured starting point for new applications** - to ensure the correct development tool setup (compiler switches,
   debugger format, etc) it is recommended that new applications are created by
   [modifying the existing demo projects](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization/#creating-your-own-application). Once you have the demo application running,
   incrementally remove the demo functions and source files and replace them with your own application code. Note: it is best
   to set [configUSE_TICK_HOOK](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_tick_hook) to 0 in FreeRTOSConfig.h when removing demo functions.
   Stopping execution of the tick hook may make some demos fail, but will
   prevent an example tick hook function attempting to interact with a demo that has been removed from the project
   (which could otherwise result in a crash).

### Locating a demo application

Each demo project has a [documentation page](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices) that details the location of the project within the FreeRTOS download,
as well as other demo specific important and time saving information (such as how to set up the hardware, and how to build the project).

All the RTOS kernel only demos (demos that do not demonstrate any other libraries) are in subdirectories of the
[FreeRTOS/Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo) directory.
The name of the subdirectory identifies the target device and the compiler used to build the project it contains. Please see the
[FreeRTOS source code organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for a full explanation of the FreeRTOS directory structure,
and the [quick start guide](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide) for further practical information.

<p className="tips">
  <span className="display-6">Tip</span>
  <span className="content">
    Port documentation pages are grouped by device manufacturer. Expand the list of supported devices, then click the manufacturer of interest to be taken to a list of demo documentation pages.
    <br />
    ![](/media/2024/supported-demo-list.png)
  </span>
</p>

### The structure of a demo application

Most demo applications use a #define in the project's main.c file to select between
building a basic "blinky" style project and building a comprehensive test and demo project.

#### Simple "blinky" demo configuration

Blinky demo projects are contained in a single source file and implement a subset of
the functionality described on the [hardware independent demo functions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/Hardware-independent-RTOS-example)
page.

As a minimum the Blinky project will demonstrate how to use a [FreeRTOS queue](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/) to pass a value between two tasks - toggling an
LED or printing output each time the value is received. Many blinky projects also demonstrate a single [software timer](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers) that uses
the same queue.

#### Comprehensive test/demo configuration

Comprehensive demo projects create all or a subset of the
"[common demo tasks](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Common/Minimal)" -
so called because the tasks are common to all comprehensive demos. The number of tasks created depends on the resources
available on the target hardware (microcontroller or microprocessor) - the amount of RAM available for task stacks
being the limiting factor.

The older common demo tasks only contain demonstrations of how to use the RTOS features.
Newer common demo tasks contain integration tests - making their implementation more complex.

Comprehensive demo applications create a 'check' task, or more rarely, a 'check'
function called from the [tick hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions). Each common demo task contains self monitoring code, and
it is the job of the check task to periodically (normally every three or five seconds, depending on the demo) query
each task to first ensure the task is still executing, and second determine if the task detected
any errors. The check task then reports the system status by either toggling an LED or printing
out a message. If the check task toggles an LED then the toggle rate will be the
task's original period (three or five seconds, depending on the demo) if no errors are present,
and increase to toggle many times a second if an error is reported by any task.

**Note:** The self monitoring code in common demo tasks may report errors purely because
the tasks are competing with each other for processing time. That is avoided by tuning the task
priorities relative to each other.

The pseudocode below shows the structure of a comprehensive demo.

```c
/* main_full() is called from main() if the #define in main.c is set to create
   the comprehensive demo, rather than simple blinky demo. */
int main_full( void )
{
    /* Setup the microcontroller hardware for the demo. */
    prvSetupHardware();

    /* Create the common demo application tasks, for example: */
    vStartInterruptQueueTasks();
    vStartMessageBufferAMPTasks()
    vCreatePollQTasks();
    Etc.

    /* Create any tasks defined within main.c itself, or otherwise specific to the
       demo being built. */
    xTaskCreate( vCheckTask, "check", STACK_SIZE, NULL, TASK_PRIORITY, NULL );
    Etc.

    /* Start the RTOS scheduler, this function should not return as it causes the
       execution context to change from main() to one of the created tasks. */
    vTaskStartScheduler();

    /* Should never get here! */
    return 0;
}
```

Notes:

- The demo projects often use all the available RAM on the target processor, requiring some tasks to be
  removed before any more can be added.
- The majority of projects building the standard demo tasks only demonstrate and test the kernel. There are
  separate projects that demonstrate additional libraries such as the [TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP),
  or [FreeRTOS core](/Security/01-Security-overview) libraries.
- The standard demo project files are provided for the purpose of demonstrating the use of and testing the RTOS kernel. They are not
  intended to provide examples of optimised solutions. This is particularly true of comtest.c (which uses an example UART driver), which
  is generally written with the intent of stressing (and therefore testing) the RTOS kernel implementation rather than
  providing an example of an optimal integration (normally a UART interface would use a [stream buffer](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
  rather than a queue).

### Legacy information

#### Partest.c, accessing LEDs

Older demo applications includes a file called partest.c (the name is historic and since lost its meaning, but is derived
from 'parallel port test'). The file contains the interface functions for setting LEDs, clearing LEDs and toggling
LEDs. It is mentioned here because the function of the file is not obvious from its name.

#### "Full" vs "Minimal" demo application files

There are two directories that contain source files that implement common demo tasks. Files located in the
FreeRTOS/Demo/Common/Full directory assume a hosted environment and are only used by demos that run
on top of old DOS systems (which is also why the Partest.c filename is cryptic - it could only use short filenames in 8.3 format).
All the other demo projects build the common demo source files from the FreeRTOS/Demo/Common/Minimal
directory, none of which assume a hosted environment.

#### Common demo task functionality

There is [old documentation](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/06-GCC-naked-attributes) that outlines the behaviour of the original
common demo tasks. Recent common demo tasks are designed more for integration testing than purely for
demonstration. That means they can be complex, and so are not documented outside of the source files
themselves.
