---
title: "Infineon XMC4000 ARM Cortex-M4F Demo Supporting IAR, Keil, GCC and Tasking compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[XMC4000](http://www.infinion.com/xmc4000/)]
[[Cortex-M4F](http://www.arm.com/products/processors/cortex-m/cortex-m4-processor.php)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Infineon XMC4500 Hexagon Development Kit CPU board](/media/2018/Infineon-XMC4000-Cortex-M4-Hexagon-kit.jpg)

### Introduction

This page documents the demo application that targets the Infineon XMC4000 range
of ARM Cortex-M4F microcontrollers.

Pre-configured projects are provided for each of the following ARM Cortex-M4 compilers:

* [Tasking VX-toolset for ARM](http://www.tasking.com/products/arm/)
* [IAR](http://www.iar.com/ewarm)
* [GCC](https://launchpad.net/gcc-arm-embedded) (using an [DAVE](https://www.infineon.com/cms/en/product/microcontroller/legacy-microcontroller/xc800-development-tools-software-and-kits/) Eclipse project)
* [ARM Keil](http://www.keil.com/arm/mdk.asp)

Each of the four projects contains three build configurations, one build configuration
targeting one of the following XMC4000 Hexagon Application Kits:

* [XMC4500 Hexagon](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc4000-industrial-microcontroller-arm-cortex-m4/)
* [XMC4400 Hexagon](http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433cd75ebf013cf6cc170d2ddd)
* [XMC4200 Hexagon](http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433cd75ebf013cf6e3d83c2e88)

Each build configuration can be compiled to create either a simple blinky demo,
or a comprehensive test and demo application. Build instructions are provided
below.

![FreeRTOS kernel aware debugger used with the IAR compiler](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 Screen shot of the FreeRTOS state viewer plug-in

 that ships with the IAR IDE

**Note 1:** The projects in the FreeRTOS download include special settings to
workaround an XMC4000 silicon errata. Please see the
[build instructions](#building-and-running-the-arm-cortex-m4f-rtos-application) for the
individual compilers below for more information.

**Note 2:** The IAR project will fail to build and be corrupted (so it can no longer
be used with any IAR version) if it is opened
in a version of EWARM that is older than the version that was used to originally
create the project.

---

#### *IMPORTANT! Notes on using the XMC4000 ARM Cortex-M4F Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#demo-application-functionality)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so
contains many more files than are needed by the XMC4000 demos.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

* The IAR Embedded Workspace project is called RTOSDemo.eww and is located in the
 FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_IAR directory.
* The Keil project is called RTOSDemo.uvproj and is located in the
 FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_Keil directory.
* The Dave project has the usual Eclipse project name .project and
 is located in the FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Dave
 directory.
* The Tasking project has the usual Eclipse project name .project and
 is located in the FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Tasking
 directory.

---

### Building and Running the ARM Cortex-M4F RTOS Application

The RTOS demo projects can be configured to build either
a simple blinky project, or a comprehensive test and demo application. The constant
mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the top of main.c, is used
to switch between the two. The simple demo is created if mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY
is set to 1. The comprehensive demo is created if mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 0.

The demo uses the LED built onto each Hexagon Application Kit board, so no
hardware setup is required.

The XMC4200 and XMC4400 Hexagon kits have a built in J-Link debugger interface. These boards
can be connected directly to the host computer using a USB cable with no other
connections required. These Hexagon boards each have two USB connectors, so
be careful to use the one marked "Debug USB".

The XMC4500 Hexagon kit does not have a build in J-Link, and therefore
requires two connections:

1. To provide an interface to the debugger:
 
 Connect an external debugger interface between the host computer
 and one of the two debug ports provided on the XMC4500 Hexagon PCB. As supplied the
 projects are configured to use a J-Link, so the use of any other
 compatible device will require the project options to be updated
 as appropriate.
2. To provide power to the hardware:
 
 Connect a USB cable between the USB OTG connector on the XMC4500 Hexagon PCB
 and any convenient USB host.

The following sub-sections provide instructions on using each of the four
supported ARM Cortex-M4 compilers.

1. [Building with the IAR Embedded Workbench](#building-with-iar-embedded-workbench)
2. [Building with ARM Keil](#building-with-arm-keil)
3. [Building with ARM GCC using the DAVE Eclipse IDE](#building-with-arm-gcc-using-the-dave-eclipse-ide)
4. [Building with Tasking ARM VX-toolset](#building-with-the-tasking-arm-vx-toolset)

#### Building with IAR Embedded Workbench

**Note:** If the XMC4000 device you are using includes errata number PMC\_001
then WORKAROUND\_PMU\_CM001 must be #define'ed to 1 in FreeRTOSConfig.h, and likewise
be set in the start-up files. The project in the FreeRTOS download already contains
these settings.
1. Open FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_IAR/RTOSDemo.eww in the
 IAR Embedded Workbench IDE.
2. Set the build configuration to the correct option for your target hardware.
 Build configurations are provided for the XMC4200, XMC4400 and XMC4500
 Hexagon Application kits. The active build configuration is set using the drop down list
 at the top of the EWARM IDE's Workspace window.
3. Select "Rebuild All" from the IAR Embedded Workbench "Project" menu (or press F7) to build
 the demo project.
4. Select "Download and Debug" from the IAR Embedded Workbench "Project"
 menu to program the microcontroller flash memory and start a debug
 session.

#### Building with ARM Keil

**Note:** If the XMC4000 device you are using includes errata number PMC\_001
then WORKAROUND\_PMU\_CM001 must be #define'ed to 1 in FreeRTOSConfig.h, and likewise
be set in the start-up files. The project in the FreeRTOS download already contains
these settings.
1. Open FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_Keil/RTOSDemo.uvproj in the
 Keil IDE.
2. Set the build configuration (called the *Target* in the Keil IDE)
 to the correct option for your target hardware.
 Build configurations are provided for the XMC4200, XMC4400 and XMC4500
 Hexagon Application kits. The active build configuration is normally
 shown in a drop down list in the IDE's menu tool bar.
3. Select "Rebuild Target" from the Keil "Project" menu (or press F7) to build
 the demo project.
4. Select "Start/Stop Debug Session" from the Keil "Project"
 menu to program the microcontroller flash memory and start a debug
 session.

#### Building with ARM GCC, using the DAVE Eclipse IDE

**Note:** If the XMC4000 device you are using includes errata number PMC\_001
then WORKAROUND\_PMU\_CM001 must be #define'ed to 1 in FreeRTOSConfig.h, and likewise
be set in the start-up files. The project in the FreeRTOS download already contains
these settings.
1. Execute the CreateProjectDirectoryStructure.bat
 batch file located in the FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Dave
 directory **before opening the project**.
 This will copy the required files into local directories.
2. Start the DAVE Eclipse IDE and either create a new or select an existing
 workspace when prompted.
3. Select "Import" from the IDE's "File" menu. The dialogue box shown below
 will appear. Select "General->Existing Project into Workspace", as shown below.

![Importing the ARM Cortex-M4 RTOS demo project into the DAVE Eclipse IDE](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**The dialogue box that appears when "Import" is first clicked**
4. In the next dialogue box, select FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Dave
 as the root directory. Make sure the RTOSDemo project is checked in the "Projects" area,
 **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states).

![Selecting the RTOS source code when importing into Eclipse CDT](/media/2018/Selecting_RTOSDemo_In_Eclipse.jpg)

**Make sure RTOSDemo is checked, and "Copy projects into workspace" is not checked**
5. After the project has been imported, right click on the project name in the DAVE
 Eclipse project explorer window, then on the pop-up menu select
 "Build Configurations->Set Active" to set
 the build configuration to the correct option for your target hardware.
 Build configurations are provided for the XMC4200, XMC4400 and XMC4500
 Hexagon Application kits.
6. Select "Rebuild Project" from the DAVE Eclipse "Project" menu to build
 the demo project.
7. Select "Debug" from the Eclipse "Run"
 menu to configure a launch configuration that can be used to program the
 microcontroller flash memory and start a debug session.
 
**Note:** 
 At the time of writing each build configuration within a DAVE project
 must target the exact same microcontroller part number. The delivered build configurations
 are however configured to selectively include and exclude chip specific
 files, so the projects will be built correctly, although an additional step
 is required when starting a debug session; Check the Debug launch
 configuration to ensure it is configured to target the hardware actually
 being used (see image below). It is likely that the debugger will also issue a warning
 when a debug session is launched - the warning can be ignored
 providing the launch configuration is configured correctly for the hardware
 in use.

![Selecting the ARM core in DAVE](/media/2018/Selecting_The_Target_In_DAVE.jpg)

**Selecting the target in the debug launch configuration**

#### Building with the Tasking ARM VX-toolset

**Note:** If the XMC4000 device you are using includes errata number PMC\_001
then the linker macro SILICON\_BUG\_PMC\_CM\_001 must be in the project settings.
The project in the FreeRTOS download already contains this setting.

1. Execute the CreateProjectDirectoryStructure.bat
 batch file located in the FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Tasking
 directory **before opening the project**.
 This will copy the required files into local directories.
2. DAVE and Tasking both use the Eclipse IDE, so you can
 [follow the instructions provided for building the application with DAVE](#building-with-arm-gcc-using-the-dave-eclipse-ide),
 just ensure to import the project into Eclipse from the
 FreeRTOS/Demo/CORTEX\_M4F\_Infineon\_XMC4000\_GCC\_Tasking
 directory.

### Demo Application Functionality

#### The simply blinky example

The simple blinky example is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 1. mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c

main() calls main\_blinky():

* **The main\_blinky() Function:** 
 
 main\_blinky() creates a queue, a queue send task, and a queue receive
 task, before starting the scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main\_blinky.c.

 prvQueueSendTask() sends the value 100 to the queue every 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c.

 prvQueueReceiveTask() blocks to wait for data to arrive on the queue.
 Each time the value 100 is received from the queue it toggles the LED.
 As data is sent to the queue every 200ms, the LED will toggle every
 200ms.

#### The comprehensive test and demo application

The comprehensive example is created when mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set
to 0. mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is defined in main.c.

main() calls main\_full():

* **The main\_full() Function:** 
 
 main\_full() creates a set of [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), some application specific
 test tasks, and a timer, before starting the scheduler.
* **The "Reg Test" Tasks:** 
 
 The reg test tasks test the context switching mechanism by filling each
 MCU register with a known value, then continuously checking that each
 register maintains its expected value for the lifetime of the task.
* **The "Check" software Timer:** 
 
 The "Check" software timer monitors the status of all the other tasks in
 the system, looking for a task either stalling or reporting an error.
 It toggles an LED each time it is called.

 If the LED is toggling every three seconds then the check task has not
 detected any stalled tasks or received any error reports. If the LED
 is toggling every 200ms then at least one error has been found.

---

### RTOS Configuration and Usage Details

#### Interrupt service routines

Interrupt service routines that cause a context switch have
no special requirements.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

An example interrupt handler
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
 portEND\_SWITCHING\_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND\_SWITCHING\_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}
```

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
on Infineon ARM Cortex-M4 microcontrollers, the lowest priority you can specify is in fact 63 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits, as they are in the provided
demo.

Note that the following lines are included in FreeRTOSConfig.h to map the FreeRTOS
interrupt handler function names onto the CMSIS interrupt handler function names.
This allows the linker scripts provided by the compiler tool vendors to be used
without modification.

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler
```

#### RTOS port specific configuration

Configuration items specific to these demos are contained in the FreeRTOSConfig.h
file located in the same directory as the project file. The
constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 500Hz is useful for
 testing the RTOS kernel functionality, but is faster than most applications require.
 Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. All ARM Cortex-M4F ports define BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M4F demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
