---
title: "Infineon XMC1000 ARM Cortex-M0 Demo Supporting IAR, Keil and GCC compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[XMC1000](http://www.infinion.com/xmc1000/)]
[[Cortex-M0](http://www.arm.com/products/processors/cortex-m/cortex-m0.php)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ARM Cortex-M0 RTOS](/media/2018/XMC1300.jpg)

**The XMC1300 boot kit** 

## Introduction

This page describes a demo application for the Infineon XMC1000 range of ARM Cortex-M0
microcontrollers.

Pre-configured projects are provided for each of the following ARM Cortex-M0 compilers:

* [IAR](http://www.iar.com/ewarm)
* [GCC](https://launchpad.net/gcc-arm-embedded) (using 
  an [Atollic TrueSTUDIO](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html) Eclipse project)
* [ARM Keil](http://www.keil.com/arm/mdk.asp)

Each project contains three build configurations, with a build configuration
for each of the following three XMC1000 evaluation boards:

* [Boot Kit XMC1100](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)
* [Boot Kit XMC1200](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)
* [Boot Kit XMC1300](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc1000-industrial-microcontroller-arm-cortex-m0/)

Each build configuration can be further configured through the use of a #define
to create either a simply blinky style application, or a comprehensive test and demo
application.

![FreeRTOS kernel aware debugger used with the IAR compiler](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)   
*Screen shot of the FreeRTOS state viewer plug-in that ships with the IAR IDE*

**Note:** If the IAR project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state from the main FreeRTOS zip file download before it
can be built even after the EWARM version has been updated.

---

### *IMPORTANT! Notes on using the XMC1000 ARM Cortex-M0 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#demo-application-functionality)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so
contains many more files than are needed by the XMC1000 demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

Project files for all three supported compilers are located in the
FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC directory.

* The IAR Embedded Workspace project is called RTOSDemo.eww.
* The Keil project is called RTOSDemo.uvproj.
* The Atollic TrueSTUDIO project has the usual Eclipse project name .project.

---

## Building and Running the ARM Cortex-M0 RTOS Application

The RTOS demo projects can be configured to run
a simple blinky style project, or a more comprehensive test and demo application. The
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY setting at the top of main.c is used to select
between the two.

Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to one to create the
basic Blinky demo. Set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0 to create
the more comprehensive test and demo application. Ensure to set the
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY constant before building the project.

The demo uses the LEDs that are built onto the boot kit's PCB, so no
hardware setup is required. Any jumpers and switches should be left in their
default position.

The following sub-sections provide instructions on using each of the three
supported ARM Cortex-M0 compilers and tool chains.

1. [Building with the IAR Embedded Workbench](#building-with-iar-embedded-workbench)
2. [Building with ARM Keil](#building-with-arm-keil)
3. [Building with ARM GCC with the Atollic TrueSTUDIO Eclipse IDE](#building-with-arm-gcc-using-the-atollic-truestudio-eclipse-ide)

#### Building with IAR Embedded Workbench

1. Open FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC/RTOSDemo.eww in the
   IAR Embedded Workbench IDE.
2. Set the build configuration to the correct option for your target hardware.
   Build configurations are provided for the XMC1100, XMC1200 and XMC1300
   boot kits. The active build configuration is set using the drop down list
   at the top of the EWARM IDE's Workspace window.
3. Select "Rebuild All" from the IAR Embedded Workbench "Project" menu (or press F7) to build
   the demo project.
4. Connect a USB cable between the USB port on the selected XMC1000 boot kit and the host computer.
5. Select "Download and Debug" from the IAR Embedded Workbench "Project"
   menu to program the microcontroller flash memory and start a debug
   session.

#### Building with ARM Keil

1. Open FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC/RTOSDemo.uvproj in the
   Keil IDE.
2. Set the build configuration (called the *Target* in the Keil IDE)
   to the correct option for your target hardware.
   Build configurations are provided for the XMC1100, XMC1200 and XMC1300
   boot kits. The active build configuration is normally shown in a drop
   down list in the IDE's menu tool bar.
3. Select "Rebuild Target" from the Keil "Project" menu (or press F7) to build
   the demo project.
4. Connect a USB cable between the USB port on the selected XMC1000 boot kit and the host computer.
5. Select "Start/Stop Debug Session" from the Keil "Project"
   menu to program the microcontroller flash memory and start a debug
   session.

#### Building with ARM GCC, using the Atollic TrueSTUDIO Eclipse IDE

Note the Eclipse project uses file references that are relative to the project's location.
The project, or any files it references, **must not be
moved from their default positions** in the FreeRTOS directory structure
(the directory structure that is created when the FreeRTOS download is unzipped).

1. Start the Eclipse IDE and either create a new or select an existing
   workspace when prompted.

2. Select "Import" from the IDE's "File" menu. The dialogue box shown below
   will appear. Select "General->Existing Project into Workspace", as shown below.

   ![Importing the Cortex-M0 RTOS demo project into the Atollic TrueSTUDIO Eclipse IDE](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)   
   *The dialogue box that appears when "Import" is first clicked*

3. In the next dialogue box, select FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC
   as the root directory. Make sure the RTOSDemo project is checked in the "Projects" area,
   **and that the Copy Projects Into Workspace box is not checked**, before clicking
   the Finish button (see the image below for the correct check box states).

   ![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/Selecting_RTOSDemo_In_Eclipse.jpg)   
   *Make sure RTOSDemo is checked, and "Copy projects into workspace" is not checked*

4. After the project has been imported, right click on the project name in the Eclipse project explorer window,
   then use the "Build Configurations->Set Active" pop up menu item to set
   the build configuration to the correct option for your target hardware.
   Build configurations are provided for the XMC1100, XMC1200 and XMC1300
   boot kits.

5. Select "Rebuild Project" from the Eclipse "Project" menu to build
   the demo project.

6. Connect a USB cable between the USB port on the selected XMC1000 boot kit and the host computer.

7. Select "Debug" from the Eclipse "Run"
   menu to configure a launch configuration that can be used to program the
   microcontroller flash memory and start a debug session.

## Demo Application Functionality

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

Building with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1 causes main() to call
main\_blinky(). main\_blinky() sets up a very simple demo, as
described below.

* **The main\_blinky() Function:** 
 
  main\_blinky() creates one queue, and two tasks. It then starts the scheduler.

* **The Queue Send Task:** 
 
  The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.
  prvQueueSendTask() sits in a loop that causes it to repeatedly block for
  200 milliseconds before sending the value 100 to the queue that was created
  within main\_blinky().

* **The Queue Receive Task:** 
 
  The queue receive task is implemented by the prvQueueReceiveTask() function
  in main\_blinky.c. prvQueueReceiveTask() sits in a loop repeatedly blocking on
  an attempt to read data from the queue that was created within main\_blinky(). When data
  arrives the task automatically unblocks, checks the value of the data, and if the value equals
  the expected 100, toggles an LED.

  The 'block time' parameter passed to
  the queue receive function specifies that the task should be held in the Blocked
  state indefinitely to wait for data to be available on the queue. The queue
  receive task will only leave the Blocked state when the queue send task writes
  to the queue. As the queue send task writes to the queue every 200
  milliseconds, the queue receive task leaves the Blocked state every 200
  milliseconds, and therefore toggles the LED every 200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

Building with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0 causes main() to call
main\_full(). main\_full() sets up a more comprehensive test and demo application,
as described below.

* **The main\_full() Function:** 
 
  main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), 
  some application specific test tasks, and a timer. It then starts the scheduler.

* **The "Reg Test" Tasks:** 
 
  These fill the registers with known values, then check
  that each register maintains its expected value for the lifetime of the
  task. Each task uses a different set of values. The reg test tasks execute
  with a very low priority, so get preempted very frequently. A register
  containing an unexpected value is indicative of an error in the context
  switching mechanism.

* **The "Interrupt Semaphore Take" Task** 
 
  This task does nothing but block on a semaphore that
  is 'given' from the tick hook function (which is defined in main.c). It
  toggles LED 4 each time it receives the semaphore. The Semaphore is
  given every 50ms, so LED 4 toggles every 50ms.

* **The "Check" software Timer:** 
 
  The check software timer period is initially set to three
  seconds. Its callback function checks that all the standard demo tasks, and
  the register check tasks, are not only still executing, but are executing
  without reporting any errors. If the check timer callback discovers that a
  task has either stalled, or reported an error, then it changes the period of
  the check timer from the initial three seconds, to just 200ms. The callback
  function also toggles LED 5 each time it is called. This provides a visual
  indication of the system status: **If LED 5 toggles every three seconds,
  then no issues have been discovered. If the LED toggles every 200ms, then
  an issue has been discovered with at least one task**.

---

## RTOS Configuration and Usage Details

### Interrupt service routines

Interrupt service routines that cause a context switch have
no special requirements.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

A dummy interrupt handler
called Dummy\_IRQHandler() is provided at the end of main.c as a reference implementation.
Dummy\_IRQHandler() is also replicated below.

```c
void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
       task with an interrupt. A semaphore is used for this purpose. Note
       lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
       that end in "FromISR" can be called from an ISR! */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
       semaphore caused the task to unblock, and the unblocked task has a priority
       higher than the current Running state task (the task that this interrupt
       interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
       internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
       portEND_SWITCHING_ISR() macro will result in a context switch being pended to
       ensure this interrupt returns directly to the unblocked, higher priority,
       task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}
```

Note that the following lines are included in FreeRTOSConfig.h to map the FreeRTOS
interrupt handler function names onto the CMSIS interrupt handler function names.
This allows the linker scripts provided by the compiler tool vendors to be used
without modification.

```c
	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler
```

### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC/FreeRTOSConfig.h. 
The constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**

  This sets the frequency of the RTOS tick interrupt. The supplied value of 500Hz is useful for
  testing the RTOS kernel functionality, but is faster than most applications require.
  Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. All ARM Cortex-M0 ports define BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_M0\_Infineon\_XMC1000\_IAR\_Keil\_GCC/FreeRTOSConfig.h 
to 1 to use pre-emption or 0 to use co-operative.

### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M0 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for full information.

