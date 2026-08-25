---
title: "Infineon TriCore Demo Using the Free TriCore Entry Toolchain"
categories:
  - kernel
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Infineon TriBoard TC1782 Starter Kit](/media/2018/Infineon-TriBoard-TC1782-starter-kit-used-for-the-FreeRTOS-TriCore-Demo-Application.jpg)

### Introduction

This page documents the FreeRTOS demo application for the Infineon TriCore processor.
The demo application uses the [Free TriCore Entry Tool Chain](http://www.infineon.com/cms/en/product/channel.html?channel=db3a304326c2768b0126c28019610002#FreeTriCore),
which consists of the HighTec GCC build tools, and a debugger, both integrated into an Eclipse-based environment.

The demo project is pre-configured to run on the
[Infineon TriBoard TC1782 starter kit](https://www.infineon.com/evaluation-board/KIT-TC1782-SK),
which is fitted with a TC1782 processor.

The FreeRTOS TriCore port supports a full interrupt nesting model, and does not
completely disable interrupts, except where architectural constraints require it.

This demo application demonstrates:

* Interrupts nesting to a depth of 3.
* [Software timers](/RTOS-software-timer.html).
* [Queues](/Embedded-RTOS-Queues.html).
* [Mutexes](/Real-time-embedded-RTOS-mutexes.html).
* [Semaphores](/Embedded-RTOS-Binary-Semaphores.html).
* Malloc failed and idle [hook functions](/a00016.html).

*Thanks to William Davy for his assistance in the creation of this port.*

---

##### *IMPORTANT! Notes on using the Infineon TriCore port and demo application*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#important-notes-on-using-the-infineon-tricore-port-and-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting#freertos-faq---my-application-does-not-run-what-could-be-wrong)

---

### Source Code Organisation
<a name="SourceCodeOrg"></a>

The FreeRTOS download contains the source code for all the FreeRTOS ports and all demo applications.
That means it contains many more files than are required to use the TriCore port or this demo.
See the [Source Code Organization](/a00017.html) section for a description of the downloaded files
and information on creating a new project.

The TriCore demo Eclipse project is located in the `FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC`
directory, but the directory requires a preparation step before it can be imported into Eclipse.

#### Preparing the Eclipse project directory

Eclipse projects can be either standard makefile projects or managed make projects.
The official FreeRTOS TriCore demo project is a managed make project. This means:

1. All source files required to build the project must be located under the folder/directory
   that contains the project file itself, **or**
2. The Eclipse workspace must be configured to locate files elsewhere on the hard disk.

Option 1 is used, so all required source files must be copied from their default FreeRTOS
locations into the `FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC` directory.

The batch file  
`FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC/RTOSDemo/CreateProjectDirectoryStructure.bat`  
is provided for this purpose.

**_CreateProjectDirectoryStructure.bat must be executed before the FreeRTOS demo
project is imported into the Eclipse workspace._**

The files copied by the batch file are:

1. The core FreeRTOS kernel source files.
2. A set of standard demo task implementations.

---

### TriCore TC1782 Demo Application
<a name="DemoApp"></a>

#### Functionality

The demo application can be configured to provide either a simple ‘blinky’ style demo or a
comprehensive test and demonstration of FreeRTOS functionality.  
The macro `#define mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY` in *main.c*
selects between the two.

Demo tasks are divided between standard demo tasks and demo-specific tasks.
Standard demo tasks are used across all FreeRTOS ports; their purpose is to
demonstrate API usage and exercise the RTOS implementation.

| **mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY setting** | **Description** |
| --- | --- |
| Set to 1 | Creates a **simple example** with three standard demo flash tasks. Each toggles LEDs P5.0, P5.1, and P5.2 at different frequencies. |
| Set to 0 | Runs a **comprehensive demo** that:<br />• Creates 42 tasks before the scheduler starts, then dynamically creates/deletes 2 more.<br />• Creates many queues, software timers, and semaphores.<br />• Includes application-specific “register test” tasks that validate context switching by checking register integrity.<br />• Includes an interrupt nesting test task using a high-frequency interrupt and semaphores.<br />• Creates a “check” task that toggles LED P5.7 every 5 seconds if all tests pass, or every 500 ms if a problem is detected.<br />• Also creates the standard flash demo tasks (P5.0, P5.1, P5.2). |

#### Hardware setup

The demo includes tasks that send/receive characters over a UART.  
The UART operates in **internal loopback mode** to ensure each transmitted character is received.

Notes:

1. Baud rate configuration has not been validated with external equipment.
2. FreeRTOS queues are used to pass characters to/from the UART interrupt handlers.
   This is intentionally inefficient to stress-test the system and nested IRQ behaviour.

The LEDs used by the demo are on the TriBoard PCB, so no additional hardware setup is required.

#### Importing, building, and debugging the FreeRTOS demo application

1. Install the [required tools](http://www.infineon.com/cms/en/product/channel.html?channel=db3a304326c2768b0126c28019610002#FreeTriCore).
2. Ensure `CreateProjectDirectoryStructure.bat` has been executed.
3. Start Eclipse for TriCore and create/select a workspace.
4. Select **Import…** from the File menu.
5. Choose **Existing projects into Workspace** (General category).
6. Select `FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC` as the root directory, and choose **FreeRTOS_Demo**.
7. Click **Finish**.
8. Right-click the project → **Build Configurations → Set Active** to choose RAM-execution or Flash-execution builds.  
   *Note:* RAM build uses size optimization.
9. Build the project using **Project → Build Project**.
10. Ensure the TriBoard is powered and USB-connected, then click the **debug** button in Eclipse to start a session.

#### Runtime behaviour

* LEDs P5.0, P5.1, P5.2 toggle at different frequencies under the standard flash tasks.
* LED P5.7 toggles every 5 seconds when system health is good, or every 500 ms if an error is detected.
* LEDs P5.5 and P5.6 toggle rapidly during UART transmission/reception under the ComTest tasks.

---

### RTOS Configuration and Usage Details
<a name="ConfigAndUsage"></a>

#### FreeRTOS TriCore port-specific configuration

Configuration items specific to this demo are defined in:  
`FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC/RTOSDemo/FreeRTOSConfig.h`

In particular:

* **configTICK_RATE_HZ**  
  Sets the RTOS tick frequency. Default 1000 Hz is useful for testing but higher than most applications need.

* **configMAX_SYSCALL_INTERRUPT_PRIORITY**  
  Defines the highest interrupt priority from which FreeRTOS API functions may be called (only "FromISR" variants).  
  Interrupts above this priority **must not** call FreeRTOS API functions but are not disabled by the kernel.

The TriCore port defines `BaseType_t` as `long`.

#### TriCore resources used by FreeRTOS

FreeRTOS exclusively uses:

* Interrupt priority 1  
* Interrupt priority 2  
* Syscall trap number 0  
* The system timer (STM) frequency  
* STM compare match 0 and its interrupt  

#### Trap handlers

Default trap handlers are defined in:  
`Demo/TriCore_TC1782_TriBoard_GCC/RTOSDemo/FreeRTOS_Source/portable/GCC/TriCore_1782/portrap.c`

These are declared **weak**, allowing applications to override them.

The SysCall trap is defined in `port.c`.

#### Writing interrupt service routines (ISRs)

ISRs are written using standard compiler facilities (see `serial.c`, `InterruptNestTest.c`).

Interrupt priorities used by the kernel (1 and 2) **must not** be modified.

To request a context switch from an ISR, use `portYIELD_FROM_ISR( x )`.

Example:

```c
static void prvPortHighFrequencyTimerHandler( int iArg )
{
static volatile unsigned long ulExecutionCounter = 0UL;

/* Must be initialised to pdFALSE (0). */
unsigned long ulHigherPriorityTaskWoken = pdFALSE;

/* Clear interrupt. */
STM_ISRR.reg = 1UL << 2UL;

/* Reload Compare Match register. */
STM_CMP1.reg += ulCompareMatchValue;

/* Count executions. */
ulExecutionCounter++;

/* Give semaphore every 10ms. */
if( ulExecutionCounter >= ulInterruptsPer10ms )
{
    xSemaphoreGiveFromISR( xHighFrequencyTimerSemaphore,
                           &ulHigherPriorityTaskWoken );
    ulExecutionCounter = 0UL;
}

/* Context switch if required. */
portYIELD_FROM_ISR( ulHigherPriorityTaskWoken );
}
```

### Memory allocation

`Source/Portable/MemMang/heap_2.c` is included in the TriCore demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/a00111.html) section of the API documentation for
full information.

### Miscellaneous

Note that `vPortEndScheduler()` has not been implemented.