---
title: "TI Hercules Safety MCUs RTOS DemoRM48 and TMS570 (Cortex-R4F) Using Code Composer Studio 5"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RM48 TMDXRM48USB USB stick and TMS570 TMDX570LS31USB USB stick](/media/2018/Free-RTOS-Hercules.jpg)

### Introduction

This page documents the FreeRTOS demo applications for the
[RM4](http://www.ti.com/mcu/docs/mcuproductcontentnp.tsp?sectionId=95&familyId=2056&tabId=2841)
and [TMS570](http://www.ti.com/mcu/docs/mcuproductcontentnp.tsp?sectionId=95&familyId=1870&tabId=2824)
safety microcontrollers from [Texas Instruments](http://www.ti.com/).
The demo application uses the FreeRTOS Cortex-R4 Code Composer Studio (CCS) port,
and targets the [TMDXRM48USB](http://www.ti.com/tool/tmdxrm48usb)
and TMS570 [TMDX570LS31USB](https://www.ti.com/product/TMS570LS3137-EP)
USB stick evaluation boards. The project was created using CCS5.

The Hercules RM4x and TMS570 safety microcontroller family enables customers to easily
develop safety-critical products that need to meet the
requirements of the ISO 26262 and IEC 61508 safety standards. These ARM Cortex-R4 based
microcontrollers offer several options of performance, memory and peripherals. Dual-core
lockstep CPU architecture, hardware BIST, MPU, ECC and on-chip clock and voltage
monitoring are some of the key functional safety features available to meet the
needs of transportation, industrial, and medical applications. For safety critical
applications there is an easy
migration path from FreeRTOS to WITTENSTEIN high integrity systems' fully safety
certified [SAFERTOS](http://www.safertos.com/) kernel.

---

#### *IMPORTANT! Notes on using the FreeRTOS Cortex-R4 CCS demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-ti-cortex-r4f-demo-applications)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The [Preparing the Project Directory Structure](#importing-the-demo-application-project-into-the-ccs-eclipse-workspace) section
of this page contains important information on preparing the project directory.

The FreeRTOS zip file contains the source files for all the FreeRTOS
ports, and all the demo applications. Only a subset of the files are required
by the RM48 and TMS570 demo application.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The RM48 and TMS570 RTOS demo project is contained in the
FreeRTOS/Demo/CORTEX\_R4\_RM48\_TMS570\_CCS5 directory. The project
contains four build configurations as follows:

1. An RM48 project that uses emulated (software) floating point.
2. An RM48 project that uses hardware floating point.
3. A TMS570 project that uses emulated (software) floating point.
4. A TMS570 project that uses hardware floating point.

![Selecting the RTOS build](/media/2018/selecting-a-build-configuration-in-CCS.jpg)

**To select a build configuration, right click the project in the project
 explorer, then select the "Build Configurations->Set Active" menu item.** 

---

### The TI Cortex-R4F Demo Applications

The RM48 and TMS570 demo applications have identical functionality.

#### Hardware set up

The demo applications use the LEDs that are built onto the USB stick evaluation
boards, and the com test tasks (described below) use the UART in loopback mode.
Therefore, no hardware setup is required.

#### Functionality

The behaviour of the demo depends on the setting of mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY,
which is defined in main.c.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main() will
call main\_blinky(). main\_blinky() creates a very simple demo as follows:

* **The main\_blinky() Function:** 
 
 main\_blinky() creates one queue, and two tasks. It then starts the
 RTOS scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.
 It sends the value 100 to the queue every 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c. It repeatedly reads from the queue with a non zero block time
 specified. This results in the task entering the
 [Blocked state](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)
 if the queue is empty. The task toggles the red LED each time the value 100 is
 received from the queue, therefore, because the queue send task sends to
 the queue every 200 milliseconds, the queue receive task exits
 the Blocked state and toggle the red LED every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main() will
call main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:

* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* UART interrupts used to demonstrate task to interrupt and interrupt
 to task communications, and context switching from an interrupt service
 routine.

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

main() creates 43 tasks and 2 software timers before
starting the RTOS scheduler. The demo then dynamically and continuously creates and
deletes a further two tasks while it is running.

In addition to the standard demo tasks, the following tasks and tests are
defined and/or created within main\_full():

"Check" timer - The check software timer period is set to three seconds.
The callback function associated with the check software timer checks that
all the standard demo tasks are not only still executing, but are executing
without reporting any errors. If the check software timer discovers that a
task has either stalled, or reported an error, then the error is logged and
the check software timer toggles the red LEDs. If an error has never been
latched, the check software timer toggles the green LEDs. Therefore, if the
system is executing correctly, the green LEDs will toggle every three
seconds, and if an error has ever been detected, the red LEDs will toggle
every three seconds.

"Reg test" tasks - These fill both the core and floating point registers
with known values, then check that each register maintains its expected
value for the lifetime of the tasks. Each task uses a different set of
values. The reg test tasks execute with a very low priority, so get
preempted very frequently. A register containing an unexpected value is
indicative of an error in the context switching mechanism, and will result in
the check timer (described above) toggling the red LEDs.

"LED" software timer - The callback function associated with the LED
software time maintains a pattern of spinning white LEDs.

---

#### Importing the demo application project into the CCS Eclipse workspace

To import the Cortex-R4F project into an existing or new Eclipse Workspace:
1. Select "Import" from the CCS "File" menu. The dialogue box shown below
 will appear. Select "Existing Projects into Workspace".  

![Importing the Cortex-R4 CCS5 projects into the Eclipse workspace](/media/2018/CCS5_import.jpg)

**The dialogue box that appears when "Import" is first clicked**
2. In the next dialogue box, select FreeRTOS/Demo/CORTEX\_R4\_RM48\_TMS570\_CCS5
 as the root directory. Then, make sure the CORTEX\_R4\_RM48\_TMS570\_CCS5
 project is checked in the "Projects" area, **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states,
 the finish button is not visible in the image).

![Selecting the FreeRTOS Cortex-R4 project to import into Eclipse](/media/2018/Code_Composer_Studio_Cortex-R4_Project_Selection.jpg)

**Make sure that two projects are checked, and "Copy projects into workspace" is not checked**

### RTOS Configuration and Usage Details

#### Cortex-R4 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_R4\_RM48\_TMS570\_CCS5/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ** 

 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications need.
 Lowering the frequency will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Interrupt service routines

Unlike many FreeRTOS ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

The following snippet of source code, taken from serial.c in the demo application,
provides an example. **NOTE:** The serial driver in the demo application is
provided to test the port and demonstrate task to interrupt and interrupt to
task communication. It is not intended to provide an example of an efficient
implementation. Production implementations should not pass individual characters
on queues, and should make use of hardware features such as DMAs and FIFOs.

---

```c

/* The interrupt implementation uses the standard \_\_interrupt compiler keyword. */
__interrupt void vSCIInterruptHandler( void )
{
/* xHigherPriorityTaskWoken must be initialised to pdFALSE. */
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
char cChar;
BaseType_t xVectorValue = serialSCI_INTVEC0_REG;

    switch( xVectorValue )
    {
        case serialRECEIVE_BUFFER_FULL:
            /* Receive buffer full interrupt, send received char to a queue.
 The address of xHigherPriorityTaskWoken is used as a parameter. */
            cChar = serialSCI_RD_REG;
            xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );
            break;
    }

    /* If calling xQueueSendFromISR() above caused a task to leave the blocked
 state, and the task that left the blocked state has a priority above the
 task that this interrupt interrupted, then xHighPriorityTaskWoken will have
 been set to pdTRUE. If xHigherPriorityTaskWoken equals true then calling
 portYIELD\_FROM\_ISR() will result in this interrupt returning directly to the
 unblocked task. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```

---

**An example interrupt service routine demonstrating the use of the
 portYIELD\_FROM\_ISR() macro.** 

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine.

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of RTI channel 0, SWI instructions, and
System Software Interrupt (SSI) 0.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the Cortex-R4 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
