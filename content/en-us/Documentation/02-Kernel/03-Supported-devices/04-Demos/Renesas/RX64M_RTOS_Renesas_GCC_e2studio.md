---
title: "FreeRTOS for Renesas RX64M Supporting Renesas and GCC compilers with e2studio"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### Introduction

This page documents the RTOS demo applications that targets the
[Renesas RX64M](http://www.renesas.com/products/mpumcu/rx/rx600/rx64m/index.jsp)
family of microcontrollers, which contain the RXv2 core.

Two [e2studio](http://www.renesas.com/e2studio)
projects are provided, one that is pre-configured to use the
[Renesas
compiler](http://am.renesas.com/products/tools/coding_tools/c_compilers_assemblers/rx_compiler/downloads.jsp), and one that is pre-configured to use the [GCC compiler](http://www.kpitgnutools.com/).

Both RTOS projects target the RX64M RSK (Renesas Start Kit) evaluation board.

---

#### *IMPORTANT! Notes on using the RX64M e2studio demo projects*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#building-and-running-the-renesas-rx64m-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so
contains many more files than are needed by the RX64M e2studio projects.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The e2studio projects have the usual Eclipse project name .project.
The project that uses the Renesas compiler is located in the
FreeRTOS/Demo/RX600\_RX64M\_RSK\_Renesas\_e2studio directory. The project
that uses the GCC compiler is located in the FreeRTOS/Demo/RX600\_RX64M\_RSK\_GCC\_e2studio
directory. These are the directories that must be selected when importing the
projects into the Eclipse workspace.

---

### Building and Running the Renesas RX64M Demo Application

The RTOS demo projects can be configured to build either
a simple blinky project, or a comprehensive test and demo application. The constant
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the top of main.c, is used
to switch between the two. The comprehensive demo is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 0.
The simple demo is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1.

The demos use the LEDs built onto the RSK development board, so no hardware
set up is required.

#### Building with e2studio

**Note:** Some of the source files built by the e2studio projects are included
in the project using a project relative path, so the project will fail to build
if the FreeRTOS directory structure has been altered from that found in the .zip file.

1. Start the e2studio Eclipse IDE and either create a new or select an existing
 workspace when prompted.
2. Select "Import" from the IDE's "File" menu. The dialogue box shown below
 will appear. Select "General->Existing Project into Workspace", as shown below.

**The dialogue box that appears when "Import" is first clicked**
3. In the next dialogue box, select FreeRTOS/Demo/RX600\_RX64M\_RSK\_Renesas\_e2studio
 as the root directory if you are using the Renesas compiler, or
 FreeRTOS/Demo/RX600\_RX64M\_RSK\_GCC\_e2studio if you are using
 the GCC compiler.
 Make sure the RTOSDemo project is checked in the "Projects" area,
 and that the Copy Projects Into
 Workspace box is not checked, before clicking
 the Finish button (see the image below for the correct check box states).

![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/Import_RX64M_Project.png)

**Make sure RTOSDemo is checked, and "Copy projects into workspace" is not checked**
4. Open main.c and locate the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY definition,
 which is near the top of the file. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 1 to
 build the simply blinky style (starter) project. Set
 mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0 to build the comprehensive test
 and demo application.
5. Select "Build All" from the e2studio Eclipse "Project" menu to build
 the demo project, and wait for the build to complete.
6. Ensure the E1 debug adapter (which comes with the RSK starter kit) is
 connected between the RX64M RSK hardware and the host computer. If you
 configure the launch configurations as per the images below then there is
 no need to supply any external power.
7. Select "Debug Configurations" from the Eclipse "Run"
 menu to configure a launch configuration that can be used to program the
 microcontroller flash memory and start a debug session. Configure
 the debug launch configuration as shown in the images below.

|  |  |  |  |
| --- | --- | --- | --- |
| [![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [![](/media/2018/RX64M_Launch_Configuration_2.png)](/media/2018/RX64M_Launch_Configuration_2.png) | [![](/media/2018/RX64M_Launch_Configuration_3.png)](/media/2018/RX64M_Launch_Configuration_3.png) | [![](/media/2018/RX64M_Launch_Configuration_4.png)](/media/2018/RX64M_Launch_Configuration_4.png) |

**Click images to enlarge**

### Demo Application Functionality

#### The simply blinky example

The simple blinky example is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 1. mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c

main() calls main\_blinky():

* **The main\_blinky() Function:** 
 
 main\_blinky() creates an RTOS queue, a queue send task, and a queue receive
 task, before starting the scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.

 prvQueueSendTask() sends the value 100 to the RTOS queue every 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c.

 prvQueueReceiveTask() blocks to wait for data to arrive on the RTOS queue.
 Each time the value 100 is received from the queue it toggles LED 0.
 As data is sent to the queue every 200ms, the LED will toggle every
 200ms.

#### The comprehensive test and demo application

The comprehensive example is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 0. mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c.

main() calls main\_full():

* **The main\_full() Function:** 
 
 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
 test tasks, and a pseudo randomiser task, before starting the scheduler.
 The pseudo randomiser task is just used to ensure some variation is
 added to the sequence in which the test tasks execute, and in so doing,
 improve the test coverage.
* **The "Reg Test" Tasks:** 
 
 The reg test tasks test the context switching mechanism by filling each
 MCU register with a known value, then continuously checking that each
 register maintains its expected value for the lifetime of the task.
* **The "Check" Task:** 
 
 The "Check" task monitors the status of all the other tasks in
 the system, looking for a task either stalling or reporting an error.
 It toggles LED 3 each time it is called.

 If the LED is toggling every three seconds then the check task has not
 detected any stalled tasks or received any error reports. If the LED
 is toggling every 200ms then at least one error has been found.
* **The Standard Flash Tasks:** 
 
 LED 0, LED 1, and LED 2 are controlled by the standard demo flash tasks. Each
 LED will toggle with a fixed but unique frequency.

---

### RTOS Configuration and Usage Details

#### RX64M RTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/RX600\_RX64M\_RSK\_Renesas\_e2studio/Source/FreeRTOSConfig.h or
FreeRTOS/Demo/RX600\_RX64M\_RSK\_GCC\_e2studio/src/FreeRTOSConfig.h for the Renesas compiler
and GCC compiler projects respectively. The
constants defined in these files can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick. The supplied value of 1KHz is useful for
 testing the RTOS kernel functionality but is faster than most applications need. Lowering this frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY**
 This defines the interrupt priority used by the RTOS kernel for the timer and software interrupts.
 This should always be set to
 the lowest interrupt priority, which is 1 for the RX64M. See [the configuration pages](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) for more information.
* **configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**
 This defines the maximum interrupt priority from which RTOS API functions
 can be called. Interrupts at or below this priority can call FreeRTOS API
 functions **provided that** the API function ends in 'FromISR'.
 Interrupts above this priority cannot call any FreeRTOS API functions but
 will not be effected by anything the RTOS kernel is doing. This makes them
 suitable for functionality that requires very high temporal accuracy (motor
 control for example).

The RX64M port layer #defines 'BaseType\_t' to 'long'.

#### Writing interrupt service routines (ISRs)

Interrupts can be written using the standard compiler syntax. Examples for both
the Renesas and GCC compilers are provided below.

Often an ISR wants to cause a context switch so the task that is returned to when
the ISR completes is different to the task that the ISR originally interrupted. This would
be the case if the ISR caused a task to unblock, and the unblocked task had a
priority above that of the task that was already in the Running state. This
can be achieved by calling portYIELD\_FROM\_ISR(), which takes a single parameter.
The parameter must be 0 if a context switch is not required, or non-zero if
a context switch is required. portYIELD\_FROM\_ISR() is used in the examples
below.

|  |
| --- |
| <br/>```c<br/><br/>/* Pragma used to install the interrupt. The 'enable' used in the pragma<br/>tells the compiler to enable interrupts before executing the user code. */<br/>#pragma interrupt ( Excep_PERIB_INTB128( vect = 128, enable ) )<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Interrupts are already enabled here. See comment above. */<br/><br/>    /* [xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the semaphore has already been created. If giving the semaphore<br/> unblocks a task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the xSemaphoreGiveFromISR()<br/> function. */<br/>    xSemaphoreGiveFromISR( xSemaphore, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**An example interrupt service routine using the Renesas compiler syntax** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* The function prototype uses the interrupt attribute. */<br/>static void vT0_1_InterruptHandler( void ) __attribute__((interrupt));<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __asm volatile( "SETPSW	I" );<br/><br/><br/>    /* [xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the semaphore has already been created. If giving the semaphore<br/> unblocks a task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the xSemaphoreGiveFromISR()<br/> function. */<br/>    xSemaphoreGiveFromISR( xSemaphore, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**An example interrupt service routine using the GCC compiler syntax** <br/><br/> |

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the software interrupt.
FreeRTOS also requires exclusive use of a timer that is capable of generating the tick interrupt - but
it is up to the application writer to define which timer is used. To do this
the application must define a function called vApplicationSetupTimerInterrupt() to
configure the tick interrupt using the chosen peripheral, then install vTickISR() in the corresponding
location within the interrupt vector table.

It is suggested that a compare match timer is used to generate the tick interrupt, and an example
implementation of vApplicationSetupTimerInterrupt() that uses compare match timer 0 is
included in main.c within this demo application.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the RX64M demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
