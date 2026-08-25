---
title: "FreeRTOS for Renesas RX71M (RXv2) Supporting GCC, IAR and Renesas compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Renesas RX71M RSK](/media/2018/rsk_rx71m.jpg)

### Introduction

This page documents the RTOS demo applications that targets the
[Renesas RX71M](http://www.renesas.eu/products/mpumcu/rx/rx700/rx71m/index.jsp)
microcontroller, which has an RXv2 core.

Three projects are provided:

1. An [e2studio](http://www.renesas.com/e2studio) project
 that uses the GCC compiler.
2. An [e2studio](http://www.renesas.com/e2studio) project
 that uses the Renesas compiler.
3. An [IAR Embedded Workbench](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rx/)
 project that uses the IAR compiler.

All three projects include build options that allow the creation of a simple blinky demo
or a comprehensive demo, and target the
[RX71M RSK](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/rx-32-bit-performance-efficiency-mcus/rx71m-starter-kit-plus-renesas-starter-kit-rx71m)
(Renesas Start Kit) evaluation board. The comprehensive demo includes a command
line interface implemented with
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI).

---

#### *IMPORTANT! Notes on using the RX71M RTOS demo projects*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#demo-application-functionality)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the RTOS ports, so
contains lots more files than are required by the RX71M projects.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section of this website for more information.

The IAR project is called RTOSDemo.eww, and is located in the
/FreeRTOS/Demo/RX700\_RX71M\_RSK\_GCC\_e2studio\_IAR directory.

The e2studio projects have the usual Eclipse project name .project.
The project that uses the GCC compiler is also located in the
/FreeRTOS/Demo/RX700\_RX71M\_RSK\_GCC\_e2studio\_IAR directory, and the
project that uses the Renesas compiler is located in the
/FreeRTOS/Demo/RX700\_RX71M\_RSK\_Renesas\_e2studio directory. These are
the directories that must be selected when importing the
projects into the e2studio Eclipse workspace.

---

### Building and Running the Renesas RX71M RTOS Demo

The RTOS demo projects can be configured to build either
a simple blinky project, or a comprehensive test and demo project.
The constant
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the top of main.c, is used
to switch between the two. The comprehensive project is created when
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0. The simple demo is created when
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1.

The demos use an LED and the UART to USB converter built onto the RSK development board, so no hardware
set up is required.

#### Building with e2studio (GCC and Renesas compilers)

**Note:** Some of the C source files built by the e2studio projects are included
in the project using a
[project relative path](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse),
so the project will fail to build if the FreeRTOS directory structure has been
altered from that provided in the official .zip file download.

1. Start the e2studio Eclipse IDE, and either create a new or select an existing
 workspace when prompted.
2. Select "Import" from the IDE's "File" menu. The dialogue box shown below
 will appear. Select "General->Existing Project into Workspace", as shown
 below.

![Importing the RX71M project into the e2studio Eclipse IDE](/media/2018/E2Studio_import.jpg)

**The dialogue box that appears when "Import" is first clicked**
3. In the next dialogue box, select /FreeRTOS/Demo/RX700\_RX71M\_RSK\_GCC\_e2studio\_IAR
 as the root directory if you are using the GCC compiler, or
 /FreeRTOS/Demo/RX700\_RX71M\_RSK\_Renesas\_e2studio if you are using
 the Renesas compiler.
4. Make sure the RTOSDemo project is checked in the "Projects" area,
 and that the Copy Projects Into
 Workspace check box is not checked, before clicking
 the Finish button (see the image below for the correct check box states).

![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/Import_RX64M_Project.png)

**Make sure RTOSDemo is checked, and "Copy projects into workspace" is not checked**
5. Open main.c and locate the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY definition,
 which is near the top of the file. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 1 to
 build the simply blinky style (starter) project. Set
 mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0 to build the comprehensive test
 and demo application.
6. Select "Build All" from the e2studio Eclipse "Project" menu to build
 the demo project, and wait for the build to complete.
7. Ensure the E1 debug adapter (which comes with the RSK starter kit) is
 connected between the RX71M RSK board and the computer running e2studio.
 If you configure the launch configurations as per the images below then there is
 no need for a separate power supply.
8. Select "Debug Configurations" from the Eclipse "Run"
 menu to configure a launch configuration that can be used to program the
 microcontroller flash memory, and start a debug session. Configure
 the debug launch configuration as shown in the images below.

|  |  |  |  |
| --- | --- | --- | --- |
| [![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [![](/media/2018/RX71M_Launch_Configuration_2.png)](/media/2018/RX71M_Launch_Configuration_2.png) | [![](/media/2018/RX71M_Launch_Configuration_3.png)](/media/2018/RX71M_Launch_Configuration_3.png) | [![](/media/2018/RX71M_Launch_Configuration_4.png)](/media/2018/RX71M_Launch_Configuration_4.png) |

**Click images to enlarge**

### Demo Application Functionality

#### The simply blinky example

The blinky example is built when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 1 in main.c. When this is done, main() calls main\_blinky():
* **The main\_blinky() Function:**

 main\_blinky() creates an RTOS queue, a queue send task, and a queue receive
 task, then starts the scheduler.
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

![RTOS CLI](/media/2018/Renesas_CLI_Session.jpg)
The comprehensive example is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 0 in main.c. When this is done, main() calls main\_full():
* **The main\_full() Function:**

 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
 test tasks, a command line interface (CLI) task, a pseudo randomiser task, and
 then starts the scheduler.
 The pseudo randomiser task is just used to ensure some variation is
 added to the sequence in which the test tasks execute, and in so doing,
 improve the test coverage.
* **The command line interface (CLI)**

 The CLI is implemented using the [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 extensible command line interface, and uses SCI1 at 19200 baud
 for its input and output. As always with FreeRTOS-Plus-CLI, type "help" to
 see a list of registered commands.
* **The "Reg Test" Tasks:**

 The reg test tasks test the context switching mechanism by filling each
 MCU register with a known value, then continuously checking that each
 register maintains its expected value for the lifetime of the task.
* **The "Check" Task:**

 The "Check" task monitors the status of all the other tasks in
 the system, looking for a task either stalling, or reporting an error.
 It toggles LED 0 each time it iterates around its implementing loop.

 If the LED is toggling every three seconds then the check task has not
 detected any stalled tasks, or detected any errors. If the LED
 is toggling every 200ms then at least one error has been found.

---

### RTOS Configuration and Usage Details

#### RX71M RTOS port specific configuration

Configuration items specific to this demo are contained in /FreeRTOS/Demo/RX700\_RX71M\_RSK\_GCC\_e2studio\_IAR/src/FreeRTOSConfig.h
for the IAR and GCC projects, and /FreeRTOS/Demo/RX700\_RX71M\_RSK\_Renesas\_e2studio/src/FreeRTOSConfig.h for the Renesas compiler
project. The
constants defined in these files can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick. The supplied value of 1KHz is useful for
 testing the RTOS kernel functionality but is faster than most applications need. Lowering this frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY**
 This defines the interrupt priority used by the RTOS kernel for the RTOS tick
 timer and software interrupts. This should always be set to
 the lowest interrupt priority, which is 1 for the RX71M. See [the configuration pages](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) for more information.
* **configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**
 This defines the maximum interrupt priority from which RTOS API functions
 can be called. Interrupts at or below this priority can call FreeRTOS API
 functions **provided that** the API function ends in 'FromISR'.
 Interrupts above this priority cannot call any FreeRTOS API functions but
 will not be effected by anything the RTOS kernel is doing. This makes them
 suitable for functionality that requires very high temporal accuracy (motor
 control for example).

The RXv2 port layer #defines 'BaseType\_t' to 'long'.

#### Writing interrupt service routines (ISRs)

Interrupts can be written using the standard compiler syntax. Examples for all
three supported compilers are provided below.

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
| <br/>```c<br/><br/>/* Pragma used to install the interrupt. The 'enable' used in the pragma<br/>tells the compiler to enable interrupts before executing the user code. */<br/>#pragma interrupt ( Excep_PERIB_INTB128( vect = 128, enable ) )<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Interrupts are already enabled here. See comment above. */<br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**An example interrupt service routine using the Renesas compiler syntax** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* Pragma used to install the interrupt. */<br/>#pragma vector = VECT_TMR0_CMIA0<br/><br/>/* Function definition. */<br/>__interrupt void vT0_1_InterruptHandler( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __enable_interrupt();<br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**An example interrupt service routine using the IAR compiler syntax** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* The function prototype uses the interrupt attribute. The function<br/>must be manually inserted into the interrupt vector table. */<br/>static void vT0_1_InterruptHandler( void ) __attribute__((interrupt));<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __asm volatile( "SETPSW	I" );<br/><br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**An example interrupt service routine using the GCC compiler syntax** <br/><br/> |

#### Generating the RTOS tick interrupt

FreeRTOS requires exclusive use of a timer that is capable of generating the tick interrupt - but
it is up to the application writer to define which timer is used. To do this,
the application must define a function called vApplicationSetupTimerInterrupt() that
configures a timer to generate an interrupt at the frequency specified by the
[configTICK\_RATE\_HZ](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtick_rate_hz)
setting in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization), then install the RTOS tick interrupt
handler in the corresponding location within the interrupt vector table.

When using the IAR and Renesas compilers the RTOS tick handler is installed
simply by defining configTICK\_VECTOR to the appropriate vector number in
FreeRTOSConfig.h.

When using the GCC compiler the RTOS tick handler and RTOS software interrupt handler
must be manually added to the appropriate vectors in the vector table definition.
The RTOS tick handler is called vPortTickISR(), and the RTOS software interrupt
handler is called vPortSoftwareInterruptISR(). See the source file vector\_table.c
in the GCC project for an example.

It is suggested that a compare match timer is used to generate the tick interrupt, and an example
implementation of vApplicationSetupTimerInterrupt() that uses compare match timer 0 is
included in main.c within each RX700 demo application.

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the software interrupt.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the RX71M demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
