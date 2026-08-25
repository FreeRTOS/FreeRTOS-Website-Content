---
title: "Renesas RZ/T RTOS Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Including FreeRTOS-Plus-CLI,
Using IAR and GCC embedded compilers

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Renesas RZ/T1 RSK used for the RTOS demo](/media/2018/rsk_rzt1.jpg)

## Introduction

This page documents a FreeRTOS demo application for the
[Renesas RZ/T embedded processor](http://www.renesas.eu/products/mpumcu/rz/rzt/index.jsp), which has an ARM Cortex-R4F core. Two projects
are provided, allowing the demo to be built with the
[IAR Embedded Workbench](http://www.iar.com/ewarm) or
GCC embedded development tools. The demo targets the Renesas
[RZT1 RSK](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/rz-cortex-a-mpus/rzt1-starter-kit-plus-renesas-starter-kit-rzt1)
(Renesas Starter Kit).

Both projects include build options that allow the creation of a simple blinky demo
or a comprehensive demo, and use:

- The FreeRTOS Cortex-R4F kernel port (the version for embedded processors
  that do not also include the ARM Generic Interrupt Controller, or GIC),
  which supports interrupt nesting.
- Either the IAR Embedded Workbench or e2studio IDE (depending on the
  project file used)
- The [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
  command line interface.
- The standard demo tasks - including the tasks that test interrupt nesting

---

### _IMPORTANT! Notes on using the RTOS Renesas RZ/T demo project_

_Please read all the following points before using this RTOS port._

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application Functionality](#the-renesas-rzt-arm-cortex-r4-demo-application)
3. [Build Instructions (for both Embedded Workbench and e2studio)](#build-instructions)
4. [RTOS Configuration and Usage Details, in particular:](#rtos-configuration-and-usage-details)
   - [Writing interrupts](#interrupt-service-routines)
   - [Generating the RTOS tick interrupt](#generating-the-rtos-tick-interrupt)
   - [Including the IRQ handler](#including-the-irq-handling-function)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## Source Code Organisation

The FreeRTOS zip file contains source code for all the RTOS ports and all the
RTOS demo applications. Only a small subset of these files are required by the
Renesas RZ/T ARM Cortex-R4F demo. The [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page describes
the structure of the FreeRTOS zip file download, and provides information on
creating a new RTOS project.

The e2studio Eclipse project file used to build the demo with GCC, and the IAR
Embedded Workbench project file used to build the demo with the IAR compiler, are
both located in the FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR
directory.

The e2studio GCC and IAR projects build the same RTOS demo application, and both include
files that are contained in the /FreeRTOS-Plus directory, so the projects will
not build if the /FreeRTOS-Plus directory has been deleted or moved from
its default location.

---

## The Renesas RZ/T ARM Cortex-R4 Demo Application

### Hardware and software set up

The demo documented on this page uses the UART to USB converter and LEDs built
onto the RZT1 RSK, so no hardware setup is required.

### Functionality

#### The simply blinky example

The blinky example is built when mainCREATE_SIMPLE_BLINKY_DEMO_ONLY is set
to 1 in main.c. When this is done, main() calls main_blinky():

- **The main_blinky() Function:**

main_blinky() creates an RTOS queue, a queue send task, and a queue receive
task, then starts the scheduler.

- **The Queue Send Task:**

The queue send task is implemented by the prvQueueSendTask() function in main_blinky.c.

prvQueueSendTask() sends the value 100 to the RTOS queue every 200 milliseconds.

- **The Queue Receive Task:**

The queue receive task is implemented by the prvQueueReceiveTask() function
in main_blinky.c.

prvQueueReceiveTask() blocks to wait for data to arrive on the RTOS queue.
Each time the value 100 is received from the queue it toggles LED 0.
As data is sent to the queue every 200ms, the LED will toggle every
200ms.

#### The comprehensive test and demo application

![RTOS CLI](/media/2018/Renesas_CLI_Session.jpg)
The comprehensive example is created when mainCREATE_SIMPLE_BLINKY_DEMO_ONLY is set
to 0 in main.c. When this is done, main() calls main_full():

- **The main_full() Function:**

main_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
test tasks, a command line interface (CLI) task, a pseudo randomiser task, and
then starts the scheduler.
The pseudo randomiser task is just used to ensure some variation is
added to the sequence in which the test tasks execute, and in so doing,
improve the test coverage.

- **The command line interface (CLI)**

The CLI is implemented using the [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
extensible command line interface, and uses the UART to USB converter
connector (J8) at 19200 baud
for its input and output. As always with FreeRTOS-Plus-CLI, type "help" to
see a list of registered commands.

- **The "Reg Test" Tasks:**

The reg test tasks test the context switching mechanism by filling each
embedded processor register with a known value, then continuously checking that each
register maintains its expected value for the lifetime of the task.

- **The "Check" Task:**

The "Check" task monitors the status of all the other tasks in
the system, looking for a task either stalling, or reporting an error.
It toggles LED 0 each time it iterates around its implementing loop.

If the LED is toggling every three seconds then the check task has not
detected any stalled tasks, or detected any errors. If the LED
is toggling every 200ms then at least one error has been found.

---

## Build Instructions

### Building and executing the demo application - IAR Embedded Workbench

Note that the IAR project references common files from both the /FreeRTOS-Plus
and /FreeRTOS/Demo/Common directories, so the project will not compile
if either directory has been deleted or moved.

1. Open FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/RTOSDemo.eww
   from within the IAR Embedded Workbench IDE.
2. Open the project's main.c file, and set mainCREATE_SIMPLE_BLINKY_DEMO_ONLY to generate either
   the simple blinky demo, or the full test and demo application, as
   required.
3. Select "Build All" from the IDE's "Project" menu to build the RTOS demo.
4. Ensure the target hardware is connected to the host computer using an
   appropriate debug interface (J-Link, I-Jet, etc.).
5. Select "Options" from the IDE's "Project" menu. The options window will
   appear. In the options window first select the "Debugger" category, then ensure
   the "driver" setting is correct for your debugger connection (J-Link, I-Jet, etc.).
   Close the Options window when the setting is correct.
6. Select "Download and Debug" from the IDE's "Project" window to download
   the built executable to the ARM Cortex-R4F, and start a debug session.

### Building and executing the demo application - e2studio

Note that the e2studio Eclipse project [uses both virtual folders and links](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse) that reference files from both the /FreeRTOS-Plus and /FreeRTOS/Demo/Common
directories. The [virtual] file structure viewed in the Eclipse project explorer will
not match the [actual] file structure viewed on the disk, and the project will not
built if either referenced directory is missing or has been moved.

1. Open e2studio and either create a new workspace or select an existing
   workspace when prompted.
2. Select "Import" from the IDE's "File" menu to bring up the import
   dialog box.
3. In the Import dialog box, select "General->Existing Projects Into Workspace"
   then browse to and select the FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR
   directory. A project called "RTOSDemo" will be visible.
4. Ensure RTOSDemo is checked **and that Copy Projects Into Workspace is
   not checked** before clicking "Finish".

![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/Import_RX64M_Project.png)

Import FreeRTOS_Demo into the Eclipse workspace **without**
copying it into the workspace. 5. Open main.c and set mainCREATE_SIMPLE_BLINKY_DEMO_ONLY to generate either
the simple blinky demo, or the full test and demo application, as
required. 6. Ensure the target hardware is connected to the host computer using an
appropriate debug interface, for example, a J-Link. 7. Select "Build All" from the IDE's "Project" menu. 8. After the build completes, select "Debug Configurations..." from the
IDE's "Debug" menu, and configure and run a debug configuration that is
appropriate for your selected connection method.
The clickable screenshots below show a configuration that is using a J-Link
JTAG interface.

|                                                                                                   |                                                                                               |                                                                                               |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [![](/media/2018/RZT_Launch_Configuration_2.jpg)](/media/2018/RZT_Launch_Configuration_2.jpg) | [![](/media/2018/RZT_Launch_Configuration_3.jpg)](/media/2018/RZT_Launch_Configuration_3.jpg) |

**Click images to enlarge**

---

## RTOS Configuration and Usage Details

### Interrupt service routines

When an interrupt occurs, the RZ/T real time embedded processor hardware will
vector directly to a peripheral specific interrupt handler, rather than to the
ARM Cortex-R IRQ vector. Therefore, each interrupt handler installed by the
application must include an assembly file wrapper that performs some house keeping,
then branches to the FreeRTOS interrupt entry code. The FreeRTOS interrupt entry
code manages interrupt entry, including interrupt nesting, before calling a
standard C function in which the interrupting peripheral is serviced.

For the purpose of this example, assume the C portion of the interrupt handler
is called InterruptHandler() - as shown below. A full example is provided after
the sections that demonstrate how to write the assembly file wrappers:

```c

void InterruptHandler( void )

{

    /* Write the interrupt handler code here. */

}

		The C portion of the interrupt handler - this is where the interrupting peripheral is serviced
```

For the purposes of this
example, assume the assembly wrapper is called InterruptHandlerWrapper(). The
wrapper must save a pointer to the C portion of the handler function into a
variable called pxISRFunction, then branch to a function called
FreeRTOS_IRQ_Handler (which is provided by the RTOS).

The syntax required to add the assembly file wrapper to each C interrupt handler
function is dependent on the compiler used (IAR or GCC). Examples and further
references are provided below.

#### Writing an assembly wrapper for an ISR: IAR

When using the IAR tools, the assembly wrapper must be implemented in an assembly
file. A generic example is provided below. Further examples can be
found in /FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/System/IAR/Interrupt_Entry_Stubs.asm.

```c

    SECTION intvec:CODE:ROOT(2)

    ARM

    /* Variables and functions from the RTOS port. */

    EXTERN pxISRFunction

    EXTERN FreeRTOS_IRQ_Handler

    /* The C portion of the interrupt handler. */

    EXTERN InterruptHandler

    /* Functions implemented in this file. */

    PUBLIC InterruptHandlerEntry

    /* The implementation of InterruptHandlerEntry. */

InterruptHandlerEntry:

    /* Save used registers (probably not necessary). */

    PUSH    {r0-r1}

    /* Save the address of the C portion of this handler into pxISRFunction. */

    LDR     r0, =pxISRFunction

    LDR     R1, =InterruptHandler

    STR     R1, [r0]

    /* Restore used registers. */

    POP     {r0-r1}

    Branch to the RTOS IRQ handler. */

    B        FreeRTOS_IRQ_Handler

The assembly wrapper for the C interrupt handler function - IAR
```

#### Writing an assembly wrapper for an ISR: GCC

When using the GCC tools, the GCC inline assembler and the 'naked' function attribute
can be used to include the assembly wrapper in a C file. A generic example is
provided below. Further examples can be
found in the /FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c,
/FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/cg_src/r_cg_scifa_user.c and
/FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/full_demo/IntQueueTimer.c
source files.

```c

#include "FreeRTOS.h"

/* The prototype for the function that implements the assembly file wrapper must

use the naked attribute - which prevents the compiler from adding any function

prologue or epilogue assembly code. */

void InterruptHandlerWrapper( void ) __attribute__((naked));

/* The implementation of InterruptHandlerEntry. This is a naked function and

must not include and C code! */

void InterruptHandlerWrapper( void )

{

    __asm volatile (

        /* Save used registers (probably not necessary). */

        "PUSH   {r0-r1}                               tn"

        /* Save the address of the C portion of this handler in pxISRFunction. */

        "LDR    r0, =pxISRFunction                    tn"

        "LDR    r1, =InterruptHandler                 tn"

        /* Restore used registers. */

        "STR    r1, [r0]                              tn"

        "POP    {r0-r1}                               tn"

        Branch to the RTOS IRQ handler. */

        "B       FreeRTOS_IRQ_Handler                     "

    );

}

The assembly wrapper for the C interrupt handler function - GCC
```

#### Writing the C portion of an ISR: IAR and GCC

If an ISR causes a task of equal or higher priority than the currently executing
task to leave the Blocked state then the ISR must request a context switch before
the ISR exits. When this is done the interrupt will interrupt one RTOS task,
but return to a different RTOS task.

The macros portYIELD_FROM_ISR() (or portEND_SWITCHING_ISR()) can be used to
request a context switch from within an ISR.
The following source code snippet is provided as an example. The example ISR
uses a [direct to task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
to synchronise with a task (not shown), and calls portYIELD_FROM_ISR()
to ensure the interrupt returns directly to the task.

```c

void InterruptHandler(void)

{

long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */

    Dummy_ClearPendingInterrupt();

    /* This interrupt does nothing more than demonstrate how to synchronise a

 task with an interrupt. A task notification is used for this purpose. Note

 lHigherPriorityTaskWoken is initialised to zero. */

    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification

 then sending the notification will have removed the task from the Blocked

 state. If the task left the Blocked state, and if the priority of the task

 is higher than the current Running state task (the task that this interrupt

 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE

 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the

 portEND\_SWITCHING\_ISR() macro will result in a context switch being pended to

 ensure this interrupt returns directly to the unblocked, higher priority,

 task. Passing pdFALSE into portEND\_SWITCHING\_ISR() has no effect. */

    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );

}

The C portion of an interrupt service routine
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine.

### Generating the RTOS tick interrupt

The RTOS Cortex-R port is a generic port that is tailored to specific embedded
processor implementation using macros and callback functions. The RTOS tick
interrupt is configured using the following two macros, which are defined in
the [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) file supplied with the RTOS demo application:

1. **configSETUP_TICK_INTERRUPT()**

This must call the function that configures a timer to generate the
tick interrupt, and install FreeRTOS_Tick_Handler() as the timers interrupt
service routine (via an assembly wrapper, as described above).

In the
provided demo application the macro is set to call
vConfigureTickInterrupt(), which is defined in
FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c,
and configures the compare match timer 5 (CMT5) to generate the RTOS
tick. 2. **configCLEAR_TICK_INTERRUPT()**

This must clear pending interrupts in whichever timer is used to
generate the RTOS tick.

In the provided demo application the macro is set to clear the interrupt
in CMT5, as the RTOS tick interrupt is generated by CMT5.

### Including the IRQ handling function

The RTOS Cortex-R port is a generic port that is tailored to a specific embedded
processor implementation using macros and callback function. In the RZ/T RTOS port
the generic IRQ handling code (the code that manages interrupt entry) calls
vApplicationIRQHandler(), and vApplicationIRQHandler() must be provided by the
application.

In the provided demo application vApplicationIRQHandler() is implemented in
FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c, and
replicated below:

```c

/* The function called by the FreeRTOS IRQ handler, after it has managed

interrupt entry. This function creates a local copy of pxISRFunction before

re-enabling interrupts then calling the handler pointed to by pxISRFunction.

pxISRFunction is set by the assembly wrapper added to each interrupt handler. */

void vApplicationIRQHandler( void )

{

ISRFunction_t pxISRToCall = pxISRFunction;

	portENABLE_INTERRUPTS();

	/* Call the installed ISR. */

	pxISRToCall();

}

The implementation of vApplicationIRQHandler() for the RZ/T RTOS port
```

### FreeRTOS ARM Cortex-R4F port demo application specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization).

### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the SVC interrupt.

### Memory allocation

Source/Portable/MemMang/heap_4.c is included in the ARM Cortex-R4 RTOS demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
