---
title: "NEC V850ES RTOS Port Using the IAR compiler"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR compiler](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rh850/)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/NEC-V850ES-Target-Board.jpg)  

This page presents the FreeRTOS demo for the NEC V850ES 32bit microcontroller. 

The demo project contains configurations for:

* [V850ES/Fx3](http://www2.renesas.com/micro/en/promotion/v850/fx3.html) Application Board
* V850ES/Jx3 Target Board
* V850ES/Jx3L Target Board
* V850ES/Jx2 Target Board
* V850ES/Hx2 Target Board

The V850ES/Fx3 project is configured to use the 
[MINICUBE](http://www2.renesas.com/micro/en/development/tool-details.php?tool=QB-V850MINI) for both 
flash programming and as a debugging interface. All the other projects are configured to use the 
[MINICUBE2](http://www.renesas.com/minicube2).

The V850ES/Fx3 Application Board includes line drivers for numerous serial interfaces along with a limited
set of buttons inputs and LED outputs.

The V850ES target boards allow for easy evaluation of the microcontroller by including the microcontroller itself along with the necessary reset, clock, 
power and debug circuitry on a board that routes all the microcontroller pins to connector mounting points along the edge of the PCB. The target boards
themselves have very limited IO capabilities. 

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also 
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### IMPORTANT! Notes on using the NEC V850 RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR Embedded Workbench workspace for the NEC V850ES demo is called RTOSDemo.eww and can be located within the
FreeRTOS/Demo/NEC\_V850ES\_IAR directory. 

---

### The Demo Application

#### Demo application hardware setup - Application Board (V850ES/Fx3 port)

Link wires are required to link the Application Board LEDs to the microcontroller outputs. The wires can be seen in the image at the top of this page. 
The following links are required:

|  |  |  |
| --- | --- | --- |
| **Pin on connector CN24** |  | **Pin on connector CN50/CN51** |
| 1 | **links to** | CN51 pin 2 |
| 3 | **links to** | CN51 pin 4 |
| 5 | **links to** | CN50 pin 2 |
| 7 | **links to** | CN50 pin 4 |

Connecting the Application Board LEDs to the microcontroller outputs

The demo application includes an interrupt driven UART test where one task transmits characters that are then received 
by another task. For correct operation of this functionality a loopback connector must be fitted to the lower 9 way plug on CN 63
(pins 2 and 3 must be connected together on the 9Way connector). Also the low CN63 plug must be linked to microcontroller
using jumpers as described in the Application Board User Manual (NEC document number EASE-UM-0019-2.1).

#### Demo application hardware setup - Target Boards (all other ports)

The demo application makes use of the two LEDs that are mounted directly onto the target board, so no additional
hardware setup is required.

#### Functionality

This section describes the functionality of the full demo that runs on the V850ES/Fx3 Application Board. The target boards do not have
the IO interface or memory required for the full demo so only execute of subset of the described tasks.

The full demo project creates 32 tasks before starting the RTOS scheduler. Most of these tasks consist of the 'standard demo' tasks - the purpose
of these tasks is to both demonstrate the RTOS API and test the RTOS port. They do not in themselves perform any other useful function.

In addition to the standard demo tasks the demo creates two 'register test' tasks. These fill the microcontroller registers with 
known values, then continuously check that each register still contains its expected 
value - each task using different values. As the tasks run with very low 
priority they will get pre-empted regularly. A register test task finding an unexpected
value in one of its registers is indicative of an error in the pre-emption context switching
mechanism.

Finally, a 'check' task is used to give visible feedback of the system status. It only executes 
every three seconds but has a high priority so is guaranteed to get processing time. 
Each time it executes it inspects the status of all the other tasks in the system to see
if any of them are reporting an error. The check task will toggle an LED every 3 seconds
provided all the other tasks are running as expected. The toggle rate will change to 500ms
if an error is discovered in any task.

When executing correctly the demo will behave as follows: 

* LEDs D3 to D5 are under the control of the standard demo 'flash' tasks. Each LED is toggled by a different task. The LEDs will toggle 
 at a fixed frequency, with each LED using a different frequency.
* LED D2 is under control of the 'check' task. It will toggle every 3 seconds provided all
 the other tasks in the system continue to function as expected and never report any errors. This mechanism can be
 tested by removing the loopback connector from CN63, and in so doing deliberately causing the
 serial port tasks to flag an error.

More information is provided within the comments of the source code.

#### Building the demo application

1. Open the FreeRTOS/Demo/NEC\_V850ES\_IAR/RTOSDemo.eww workspace from within the IAR Embedded Workbench IDE.
2. Select the configuration that is correct for the application or target board being used, as demonstrated in the image below.

![](/media/2018/Selecting-the-V850-configuration.jpg)  

Selecting the configuration for the application or target board being used.
3. **Important!** Ensure the configDATA\_MODE setting within FreeRTOSConfig.h matches the compiler project options. 
 If the compiler options are set to use either the small or large memory model then configDATA\_MODE must be set to 0. 
 If the compiler options are set to use the tiny data model then configDATA\_MODE must be set to 1.
4. Press F7 - the project should build with no errors or warnings.

#### Programming the microcontroller and debugging

1. If using the MINICUBE2:
	* When using the V850ES/HG2 target board ensure the MINICUBE2 switches are set to "M2" and "5".
	* For all other target boards set the MINICUBE2 switches to "M2" and "3".
2. Connect the MINICUBE or MINICUBE2 between the target board and the host computer.
3. Select "Download and Debug" from the Embedded Workbench "Project" menu. There will be a short delay while the flash memory is programmed before
 the debugger breaks on entry to the main() function.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this demo are contained in [FreeRTOS/Demo/NEC\_V850ES\_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization). The 
constants defined in this file can be edited to suit your application.

The configDATA\_MODE configuration constant is specific to the V850ES port. If the compiler options are set to use either the small or large
memory model then configDATA\_MODE must be set to 0. If the compiler options are set to use the tiny data model then configDATA\_MODE must be set
to 1.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Writing interrupt service routines

Interrupt service routines that cannot cause a context switch have no special requirements and can be written as described by the
IAR compiler documentation.

Often you will require an interrupt service routine to cause a context switch. For example a serial port character being received may 
unblock a high priority task that was blocked waiting for the character to arrive. If the unblocked task has a higher priority than the current task
then the ISR should return 
directly to the unblocked task. Limitations in the IAR inline assembler necessitate such interrupt service routines use 
an assembly file wrapper. The UART driver is included in this demo to demonstrate the mechanism. The receive handler is
replicated below.

First the assembly file wrapper.

---

```c

; ISR\_Support.h defines the portSAVE\_CONTEXT and portRESTORE\_CONTEXT 
; macros.
#include "ISR\_Support.h"

 PUBLIC vUARTRxISRWrapper
 EXTERN vUARTRxISRHandler

 RSEG CODE:CODE
 
; The wrapper is the interrupt entry point.
vUARTRxISRWrapper:

 ; The ISR must start with a call to the portSAVE\_CONTEXT() macro to save 
 ; the context of the currently running task.
 portSAVE\_CONTEXT

 ; Once the context is saved the C portion of the handler can be called.
 ; This is where the interrupting peripheral is actually serviced.
 jarl vUARTRxISRHandler, lp

 ; Finally the ISR must end with a call to portRESTORE\_CONTEXT() to restore
 ; the context of which ever task is selected to run - which may be
 ; different to the task that was running before the interrupt started. 
 portRESTORE\_CONTEXT
```

---

An example assembly file wrapper for an interrupt handler.

The C portion of the interrupt handler is just a standard C function.

---

```c

/* This standard C function is called from the assembly wrapper above. */
void vUARTRxISRHandler( void )
{
char cChar;
long lHigherPriorityTaskWoken = pdFALSE;

 /* Send the received character to the Rx queue. */
 cChar = UD0RX;
 xQueueSendFromISR( xRxedChars, &cChar, &lHigherPriorityTaskWoken );

 /* If sending a character to the Rx queue caused a task to unblock, and
 the unblocked task has a priority higher than the currently running task,
 then lHigherPriorityTaskWoken will have been set to true and a context
 switch should occur now. */
 portYIELD\_FROM\_ISR( lHigherPriorityTaskWoken ); 
}
```

---

The C portion of the example interrupt handler.

#### Resources used by the RTOS kernel

The RTOS kernel uses TM0 to generate the RTOS tick. The function prvSetupTimerInterrupts() in
FreeRTOSSourceportableIARV850ESport.c can be altered to use any convenient timer source.

The RTOS kernel also requires exclusive use of the TRAP 0 instruction.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

SourcePortableMemMangheap\_2.c is included in the demo application project to provide the memory 
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for 
full information.
