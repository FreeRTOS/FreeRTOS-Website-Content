---
title: "Altera Cyclone V SoC RTOS Demo (ARM Cortex-A9)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Cyclone V SoC development kit](/media/2018/cyclonev_soc_with_Cortex-A9.jpg)

### Introduction

This page documents a FreeRTOS demo application for a Cortex-A9 core in the
[Altera Cyclone V SoC](https://www.intel.com/content/www/us/en/products/details/fpga/cyclone/v.html)
Hard Processing System (HPS).

The project builds using the free Altera edition of the ARM DS-5 Eclipse based
IDE and the GCC compiler, both of which come as part of
the [Embedded Software and Tools for Intel® SoC FPGA](https://www.intel.com/content/www/us/en/software/programmable/soc-eds/overview.html#tab-blade-1-1)
(EDS). Note only the DS-5 and compiler components of the EDS are used - it is
not necessary to install any FPGA tools to build or use this RTOS demo.

The project is pre-configured to execute on the
[Cyclone V SoC Development Kit](https://www.intel.com/content/www/us/en/products/details/fpga/development-kits/cyclone/v-sx.html)
hardware.

[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 is used to create a command console.

---

#### *IMPORTANT! Notes on using the FreeRTOS Cyclone V SoC ARM Cortex-A9 demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application Functionality](#the-altera-cyclone-v-soc-arm-cortex-a9-demo-application)
3. [Build Instructions](#build-instructions)
4. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting), and
the page that provides [instruction on using FreeRTOS on ARM Cortex-A embedded processors](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors).

---

### Source Code Organisation

Only a small subset of the files in the FreeRTOS .zip file download are
required by the Altera Cyclone V SoC demo. The [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page describes
the structure of the FreeRTOS zip file download.

The ARM DS-5 Eclipse project file is located in the FreeRTOS/Demo/CORTEX\_A9\_Cyclone\_V\_SoC\_DK
directory. Note the RTOS project includes files that are contained in the
/FreeRTOS-Plus directory, so the projects will not build if the
/FreeRTOS-Plus directory has been deleted or the directory structure has
been changed.

---

### The Altera Cyclone V SoC ARM Cortex-A9 Demo Application

#### Hardware and software set up

Although the RTOS demo presented on this page has been pre-configured to run
on the Altera Cyclone V SoC Development Kit it can be adapted easily to run on
any Cyclone V SoC evaluation board that provides access to one UART and one LED.
* **UART**

 A UART is used for console IO. The demo in the download uses UART 0 for
 this purpose. UART 0 uses a UART to USB converter, so is connected using
 a USB cable.

 If it is necessary to use a UART other than UART 0 then update the
 FreeRTOS/Demo/CORTEX\_A9\_Cyclone\_V\_SoC\_DK/Altera\_Code/SoCSupport/uart0\_support.c
 source file accordingly.
* **LED digital output**

 A digital output is used to toggle an LED. If it is necessary to use a
 different digital output then update FreeRTOS/Demo/CORTEX\_A9\_Cyclone\_V\_SoC\_DK/LEDs.c
 accordingly.

#### Functionality

The behaviour of the demo is defined by the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY
#define constant, which is declared at the top of main.c.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main() will
call main\_blinky().

main\_blinky() creates a very simple demo that includes two
[tasks](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview) and one [queue](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
One task repeatedly sends the value 100 to the other task
through the queue. The receiving task toggles an LED each time it receives
the message. The message is sent every 200 milliseconds, so the LED toggles
every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

![Using the RTOS CLI on an ARM Cortex-A9 MPU](/media/2018/ARM-Cortex-A5-RTOS-CLI.png)

 An example CLI session

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main() will
call main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:
* The [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 command line interface.
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Event Groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).

Connect to FreeRTOS-Plus-CLI though the UART using 115200 baud. Type 'help' in the
CLI to see a list of the registered commands.

Most of the RTOS tasks created by the demo are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
RTOS tasks. These are used by all FreeRTOS demo applications, and
have no specific functionality or purpose other than to demonstrate the FreeRTOS
API being used and test the RTOS kernel port.

A 'check' RTOS task is also created. The check task periodically queries the standard
demo tasks to ensure they are functioning as intended. The check task also
toggles an LED to give a visual indication of the system status.
**If the LED toggles every 3 seconds then the check task has not discovered
any problems with the executing demo. If the LED toggles every 200 milliseconds
then the check task has discovered a problem in at least one task.**.

---

### Build Instructions

Note that the ARM DS-5 Eclipse project [uses both virtual folders and links](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)
that reference files from both the /FreeRTOS-Plus and /FreeRTOS/Demo/Common
directories. The [virtual] file structure viewed in the Eclipse project explorer will
not therefore match the [actual] file structure viewed on the disk.
1. Open the ARM DS-5 Eclipse IDE and either create a new workspace or select an existing
 workspace when prompted.

2. Select "Import" from the IDE's "File" menu to bring up the import
 dialog box.

3. In the Import dialog box, select "General->Existing Projects Into Workspace"
 then browse to and select the FreeRTOS/Demo/CORTEX\_A9\_Cyclone\_V\_SoC\_DK
 directory. A project called "RTOSDemo" will be visible.

4. Ensure RTOSDemo is checked **and that Copy Projects Into Workspace is
 not checked** before clicking "Finish".
 ![Importing the RTOS demo project into ARM DS-5 Eclipse workspace](/media/2018/importing_RTOS_into_Altera_Eclipse.png)
 Import RTOSDemo into the Eclipse workspace **without**
 copying it into the workspace.

5. The GCC compiler used to build the project is installed when the
 [Altera EDS](https://www.intel.com/content/www/us/en/software-kit/665453/intel-soc-fpga-embedded-development-suite-soc-eds-pro-edition-software-version-18-1-for-windows.html)
 is installed. It is necessary to update the project to set the compiler's
 location.
 Select "Properties" from the IDE's "Project" menu to bring up the
 properties dialogue box. In the dialogue box select "C/C++Build->Settings->
 Cross Settings", then set the path to the compiler to be correct for your
 installation.
**Note:** If the dialogue box tab shown in the
 image below is missing, or contains an error message, then it is likely
 your version of DS-5 does not have the CDT cross compiler plug in installed.
 If this is the case the plug in can be installed manually by
 [following the instructions provided on the ARM website](http://ds.arm.com/developer-resources/tutorials/adding-custom-gcc-toolchains-to-ds-5/).
 It will be necessary to create a new workspace after the plug-in has been installed.
 ![Setting the path to the compiler that builds the RTOS](/media/2018/Setting_the_path_to_the_Altera_compiler.png)
 Setting the path to the compiler in the RTOS project's properties dialogue box

6. Open main.c and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simple blinky demo, or the full test and demo application, as
 required.

7. Ensure the target hardware is connected to the host computer using an
 appropriate debug interface. The Cycle V SoC Development Kit has a build
 it BitBlaster interface. Other debug interfaces, such as ARM's D-Stream,
 can also be used.

8. Select "Build All" from the IDE's "Project" menu.

9. After the build completes, select "Debug Configurations..." from the
 IDE's "Debug" menu, and configure and run a debug configuration that is
 appropriate for your selected connection method (BitBlaster, D-Stream, etc.).
 The clickable screenshots below show a configuration that is using the D-Stream
 debugger. **Note the selection of the preloader script in third screenshot.**

[![D-stream Cortex-A debug configuration](/media/2018/D-Stream_Cortex-A_CycloneV.jpg)](/media/2018/D-Stream_Cortex-A_CycloneV.jpg)
[![D-stream Altera Cortex-A debug configuration](/media/2018/D-Stream_Cortex-A_CycloneV_2.jpg)](/media/2018/D-Stream_Cortex-A_CycloneV_2.jpg)
[![Altera SoC debug using DS-5 from ARM](/media/2018/D-Stream_Cortex-A_Cyclone_3.jpg)](/media/2018/D-Stream_Cortex-A_Cyclone_3.jpg)

**Click Images to Enlarge**

---

### RTOS Configuration and Usage Details

#### FreeRTOS ARM Cortex-A port specific configuration

Attention please!: Refer to the page that provides
[instruction on using FreeRTOS on ARM Cortex-A embedded processors](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors),
paying particular attention to the value and meaning of the
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY setting.

In this demo configSETUP\_TICK\_INTERRUPT is defined to call vConfigureTickInterrupt(),
which in turn is implemented in main.c. vApplicationIRQHandler() is also implemented
in main.c.

Configuration items specific to this demo are contained in
[FreeRTOS/Demo/CORTEX\_A9\_Cyclone\_V\_SoC\_DK/FreeRTOSConfig.h](https://github.com/cjlano/freertos/blob/master/FreeRTOS/Demo/CORTEX_A9_Cyclone_V_SoC_DK/FreeRTOSConfig.h).
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization).

#### [Application Defined] Interrupt service routines

This demo uses drivers provided by Altera to configure the interrupt controller but,
because the driver's own interrupt table is not accessible outside of its defining
source file, a FreeRTOS specific function is used to actually register interrupt
handlers. vRegisterIRQHandler() is used for this purpose, and is implemented in
main.c.

```c

/*

 * ulID - the ID of the interrupt as defined in the Altera provided

 * alt\_interrupt\_common.h header file.

 *

 * pxHandlerFunction - the C function being registered to handle the interrupt.

 *

 * pvContext - a reference to additional data of the application writer's choice

 * that can be used from within the interrupt handler.

 */

void vRegisterIRQHandler( uint32_t ulID,

                          alt_int_callback_t pxHandlerFunction,

                          void *pvContext );

vRegisterIRQHandler() function prototype
```

The C handlers themselves have the following prototype;

```c

/*

 * ulICCIAR - the value of the generic interrupt controller's (GIC's) IAR register

 * at the time the handler is called.

 *

 * pvContext - the pointer to additional data for the handler that was passed into

 * the call to vRegisterIRQHandler() used to register the handler.

 */

void vAnISRHandlingFunction( uint32_t ulICCIAR, void *pvContext );

The prototype of an interrupt handling function that can be registered using vRegisterIRQHandler()
```

If an ISR causes an RTOS task of equal or higher priority than the currently executing
task to leave the Blocked state (see description of the pxHigherPriorityTaskWoken
parameter in the API documentation for functions such as
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR))
then the ISR must request a context switch before
the ISR exits. When this is done the interrupt will interrupt one RTOS task,
but return to a different RTOS task.

The macros portYIELD\_FROM\_ISR() (or portEND\_SWITCHING\_ISR()) can be used to
request a context switch from within an ISR.
The following source code snippet is provided as an example. The example ISR
uses a semaphore to synchronise with a task (not shown), and calls portYIELD\_FROM\_ISR()
to ensure the interrupt returns directly to the task.

```c

void Dummy_IRQHandler( uint32_t ulUnused, void *pvUnused )

{

long lHigherPriorityTaskWoken = pdFALSE;

    /* The parameter is not used. */

    ( void ) ulUnused;

    /* Clear the interrupt if necessary. */

    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a

 task with an interrupt. A semaphore is used for this purpose. Note

 lHigherPriorityTaskWoken is initialised to pdFALSE. */

    [xSemaphoreGiveFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the

 semaphore caused the task to unblock, and the unblocked task has a priority

 higher than or equal to the currently Running task (the task that this

 interrupt interrupted), then lHigherPriorityTaskWoken will have been set to

 pdTRUE internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the

 portYIELD\_FROM\_ISR() macro will result in a context switch being pended to

 ensure this interrupt returns directly to the unblocked, higher priority,

 task. Passing pdFALSE into portYIELD\_FROM\_ISR() has no effect. */

    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );

}

An example interrupt handler
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_API\_CALL\_INTERRUPT\_PRIORITY
configuration constant (meaning a numerically higher value).

#### Resources used by FreeRTOS

Information is provided on the [Using FreeRTOS on ARM Cortex-A Embedded Processors](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors) page.
This demo is configured to generate the tick interrupt from the Cortex-A9 core's
private timer.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-A demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
