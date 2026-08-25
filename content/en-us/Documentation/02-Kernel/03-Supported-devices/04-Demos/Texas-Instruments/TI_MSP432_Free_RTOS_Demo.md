---
title: "TI MSP432 ARM Cortex-M4F RTOS Demo Supporting IAR, ARM (Keil), and TI (CCS) compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[ARM Cortex-M4F](http://www.arm.com/products/processors/cortex-m/cortex-m4-processor.php)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Texas Instruments MSP432 Launchpad Development Kit](/media/2018/MSP432_Launchpad_Development_Kit.jpg)

 The MSP-EXP432P401R LaunchPad Development Kit

### Introduction

This page documents the demo application that targets the
[Texas Instruments MSP432 microcontroller](http://www.ti.com/MSP432)
 - which is a variant of the MSP430 low power microcontroller
that uses an ARM Cortex-M4F core.

Pre-configured MSP432 projects that target the MSP432P401R Launchpad Development
Kit are provided for each of the following three ARM Cortex-M4 compilers:

* [IAR](http://www.iar.com/ewarm) using the Embedded Workbench for ARM IDE
* [ARM](http://www.keil.com/arm/mdk.asp) using the uVision IDE
* [TI](http://www.ti.com/tool/ccstudio) using the Code Composer Studio Eclipse based tools

Each project can be compiled to create either a simple blinky demo,
or a comprehensive test and demo application.

The comprehensive demo uses [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
to create a simple command line interface through a UART.

The blinky demo uses FreeRTOS's tickless idle mode to reduce power consumption.

### "Tickless" Low Power Operation

Stopping the RTOS tick interrupt allows the microcontroller to remain in a deep power
saving state until either an interrupt occurs, or it is time for the RTOS kernel
to transition a task into the Ready state.

Note that only the generic ARM Cortex-M tickless implementation is demonstrated,
which prevents any of the advanced MSP432 low power modes from being entered, and
therefore does not get close to demonstrating the power saving that could otherwise
be achieved.

FreeRTOS is designed to allow the generic tickless mode to be overridden by an
application specific implementation. Providing a target specific tickless
implementation allows the RTOS tick interrupt to be
generated from a low power clock, instead of the ARM Cortex-M SysTick clock. The
application writer can then tailor the implementation to be specific to the
application through the use of pre and post sleep macros. Tailoring a tickless
implementation specifically to the MSP432 will allow significantly
greater power savings to be achieved.

See the [Low Power Support](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
and the [Low Power RTOS For ARM Cortex-M MCUs](/low-power-ARM-cortex-rtos)
pages for further information.

![FreeRTOS kernel aware debugger used with the IAR compiler](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 Screen shot of the FreeRTOS state viewer plug-in

 that ships with the IAR IDE

---

### *IMPORTANT! Notes on using the TI MSP432 ARM Cortex-M4F Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#demo-application-functionality)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for every FreeRTOS port and
all the demo applications, so contains a lot more files than are required by the MSP432
demos. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section of this website for a description of the downloaded files.

The IAR, Keil uVision and CCS projects are all located in the
/FreeRTOS/Demo/CORTEX\_M4F\_MSP432\_LaunchPad\_IAR\_CCS\_Keil directory:

* The IAR Embedded Workbench for ARM (EWARM) project is called RTOSDemo.eww
* The Keil uVision project is called RTOSDemo.uvproj
* The CCS project has the usual Eclipse project name .project

---

### Building and Running the MSP432 ARM Cortex-M4F RTOS Application

The RTOS demo projects can be configured to build either
a simple blinky project that also demonstrates FreeRTOS's generic tickless low
power mode, or a comprehensive test and demo application. The constant
configCREATE\_SIMPLE\_TICKLESS\_DEMO, which is defined at the top of the
projects' FreeRTOSConfig.h file, is used
to switch between the two.

* The simple tickless demo is created if configCREATE\_SIMPLE\_TICKLESS\_DEMO
 is set to 1.
* The comprehensive demo is created if configCREATE\_SIMPLE\_TICKLESS\_DEMO
 is set to 0.

Note the [comments at the top of this page](#tickless-low-power-operation) about the
difference in power saving that can be achieved by the demonstrated generic
tickless implementation when compared to what could be achieved using an MSP432
specific tickless implementation.

The demo uses an LED built onto the Launchpad development kit, so no
hardware setup is required.

The following sub-sections provide instructions on using each of the ARM
Cortex-M4 toolchains.

1. [Building with the IAR Embedded Workbench](#building-with-iar-embedded-workbench)
2. [Building with ARM Keil](#building-with-arm-keil)
3. [Building with Code Composer Studio](#building-with-ti-eclipse-based-code-composer-studio-ccs)

#### Building with IAR Embedded Workbench

1. IAR Embedded Workbench should be able to use the CMSIS DAP debug interface
 accessible via the Launchpad hardware's USB connector, but for the
 fastest and most reliable debugging experience it is recommended to
 connect a JLINK Lite to the Launchpad hardware's external JTAG connector.
 If you are using the external JTAG connector then the Launchpad
 hardware's "JTAG Switch" must be set to "Ext".
2. Open FreeRTOS/Demo/CORTEX\_M4F\_MSP432\_LaunchPad\_IAR\_CCS\_Keil/RTOSDemo.eww in the
 IAR Embedded Workbench IDE.
3. Select "Rebuild All" from the IAR Embedded Workbench "Project" menu (or press F7) to build
 the demo project.
4. Select "Download and Debug" from the IAR Embedded Workbench "Project"
 menu to program the microcontroller flash memory and start a debug
 session.

**Note:** The IAR project can fail to build and get corrupted (so it can no longer
be used with any IAR version) if it is opened in a version of EWARM that is older
than the version that was used to originally create the project.

#### Building with ARM Keil

1. Keil uVision should be able to use the CMSIS DAP debug interface
 accessible via the Launchpad hardware's USB connector, but for the
 fastest and most reliable debugging experience it is recommended to
 connect a UINK ME to the Launchpad hardware's external JTAG connector.
 If you are using the external JTAG connector then the Launchpad
 hardware's "JTAG Switch" must be set to "Ext".
2. Ensure the MSP432 pack has been installed and is available for use by
 the uVision IDE.
3. Open FreeRTOS/Demo/CORTEX\_M4F\_MSP432\_LaunchPad\_IAR\_CCS\_Keil/RTOSDemo.uvprojx in the
 Keil IDE.
4. Select "Rebuild Target" from the Keil "Project" menu (or press F7) to build
 the demo project.
5. Select "Start/Stop Debug Session" from the Keil "Project"
 menu to program the microcontroller flash memory and start a debug
 session.

#### Building with TI Eclipse based Code Composer Studio (CCS)

1. Connect the Launchpad development kit directly to the host computer
 (the computer running CCS) using the hardware's USB connector - no other debug
 interface is required. Ensure the Launchpad hardware's "JTAG Switch" is
 set to "XDS".
2. Start the CCS Eclipse IDE, and either create a new or select an existing
 workspace when prompted.
3. Select "Import" from the IDE's "File" menu. The dialogue box shown below
 will appear. Select "Code Composer Studio->CCS Projects", as shown below.

![Importing the ARM Cortex-M4 RTOS demo project into the CCS Eclipse IDE](/media/2018/import_code_composer_studio.jpg)

**The dialogue box that appears when "Import" is first clicked**
4. In the next dialogue box, select /FreeRTOS/Demo/CORTEX\_M4F\_MSP432\_LaunchPad\_IAR\_CCS\_Keil
 as the root directory. Make sure the RTOSDemo project is checked in the "Projects" area,
 **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states).

![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/import_CCS_project.jpg)

**Make sure RTOSDemo is checked, and "Copy projects into workspace" is not checked**
5. Select "Build All" from the CCS Eclipse "Project" menu to build
 the demo project.
6. Select "Debug" from the Eclipse "Run"
 menu to program the microcontroller's flash memory and start a debug
 session.

**Note 1:** The projects for all the compilers are contained in the same directory
within the FreeRTOS .zip file download. Code Composer Studio (CCS) will fail to build
the project if the directory already contains object files that were generated
by a different compiler. It is necessary to delete all intermediary files from the
directory, and its sub-directories, before it is possible to switch to using the
Code Composer Studio project after either the IAR or uVision projects have already
been used.

**Note 2:** The CCS project references files using relative paths, including
FreeRTOS-Plus-CLI files from the /FreeRTOS-Plus directory. The project may
fail to build if a directory path is changed or if a file is moved. Eclipse's
'export' features can be used to convert the project into a stand-alone project
that only uses directories under the directory in which the .project file is located.

### Demo Application Functionality

####  The simply blinky example, using tick-less operation

The simple tickless example is created when configCREATE\_SIMPLE\_TICKLESS\_DEMO is set
to 1. configCREATE\_SIMPLE\_TICKLESS\_DEMO is defined at the top of FreeRTOSConfig.h.

The FreeRTOS tickless idle mode stops the periodic RTOS tick interrupt during
idle periods (periods when there are no application tasks that are able to execute).
The blinky example creates two tasks that only unblock once every second, so the
tick interrupt is stopped for the majority of the execution time.

Stopping the RTOS tick interrupt allows the microcontroller to remain in a deep power
saving state until either an interrupt occurs, or it is time for the RTOS kernel
to transition a task into the Ready state.

Note the [comments at the top of this page](#tickless-low-power-operation) about the
difference in power saving that can be achieved by the demonstrated generic
tickless implementation when compared to what could be achieved using an MSP432
specific tickless implementation.

Setting configCREATE\_SIMPLE\_TICKLESS\_DEMO to 1 results in main() calling
main\_blinky():

* **The main\_blinky() Function:**

 main\_blinky() creates a queue, a queue send task, and a queue receive
 task, before starting the scheduler.
* **The Queue Send Task:**

 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.

 prvQueueSendTask() sends the value 100 to the queue every second.
* **The Queue Receive Task:**

 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c.

 prvQueueReceiveTask() blocks to wait for data to arrive on the queue.
 Each time the value 100 is received from the queue it flashes the LED.
 As data is sent to the queue every second, the LED will flash every
 second.

####  The comprehensive test and demo application

![](/media/2018/MSP432_CLI.jpg)

 Sample CLI session

The comprehensive example is created when configCREATE\_SIMPLE\_TICKLESS\_DEMO is set
to 0. configCREATE\_SIMPLE\_TICKLESS\_DEMO is defined in FreeRTOSConfig.h.

The comprehensive demo includes a
[command line interface](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
(CLI) on which both task and run-time statistics can be viewed. Instructions on
connecting to and using the CLI are provided below.

Setting configCREATE\_SIMPLE\_TICKLESS\_DEMO to 0 results in main() calling
main\_full():

* **The main\_full() Function:**

 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview),
 the CLI, the Check task, the Register Test tasks, and starts the
 scheduler.
* **The "Reg Test" Tasks:**

 The reg test tasks test the context switching mechanism by filling each
 MCU register with a known value, then continuously checking that each
 register maintains its expected value for the lifetime of the task.
* **The "Check" Task:**

 The "Check" task monitors the status of all the other tasks in
 the system, looking for a task either stalling or reporting an error.
 It toggles an LED each time it is called.

 If the LED is toggling every three seconds then the check task has determined
 the demo is running as expected. If the LED
 is toggling every 200ms then at least one error has been found.

To connect to the CLI:

1. Power the Lauchpad hardware through the hardware's USB connector.
2. Run the comprehensive demo. A UART on the MPS432 will enumerate
 as a virtual COM port called "XDS110 Class Application/User UART" on the
 host computer.
3. Open a dumb terminal program, such as Tera Term or Hyper Terminal, and
 connect to the enumerated COM port at 19200 baud.
4. As always with FreeRTOS-Plus-CLI - type "help" into the console to see a
 list of registered commands. An example CLI session is shown on the right.

---

### RTOS Configuration and Usage Details

### Interrupt service routines

####  Priority assignment

Attention please!: See the [page dedicated to setting interrupt priorities on ARM Cortex-M devices](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4). Remember that ARM Cortex-M cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0
and therefore the highest priority possible.

The lowest priority on a ARM Cortex-M core is in fact 255 - however different
ARM Cortex-M microcontroller manufacturers implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
the TI MSP432 ARM Cortex-M4 microcontrollers implements 3 priority bits, which
allows for a maximum of 8 different priority levels (0 to 7 inclusive). The lowest priority being
the highest number. Some library functions will use the numeric value 7 as the
lowest priority, while others will use the numeric value 224 as the lowest (which
is 7 \<\< 5, and how the ARM Cortex-M sees the value internally in the interrupt controller).
These two numbers are defined by configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and
configKERNEL\_INTERRUPT\_PRIORITY respectively in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits.

####  Implementing interrupt service routines

Interrupt service routines that cause a context switch have
no special requirements. The function vUART\_Handler(), defined in
/FreeRTOS/Demo/CORTEX\_M4F\_MSP432\_LaunchPad\_IAR\_CCS\_Keil/Full\_Demo/serial.c
can be used as an example. Another example is provided below:

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A [task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for a notification,
 and giving the notification caused the task to unblock, and the unblocked
 task has a priority higher than the current Running state task (the task that
 this interrupt interrupted), then lHigherPriorityTaskWoken will have been set
 to pdTRUE internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into
 the portYIELD\_FROM\_ISR() macro will result in a context switch being pended
 to ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD\_FROM\_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}
```

### RTOS port specific configuration

[Configuration items](/Documentation/02-Kernel/03-Supported-devices/02-Customization) specific to these demos are contained in the FreeRTOSConfig.h
file located in the same directory as the project file. The
constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 500Hz is useful for
 testing the RTOS kernel functionality, but is faster than most applications require.
 Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. All ARM Cortex-M4F ports define BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M4F demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
