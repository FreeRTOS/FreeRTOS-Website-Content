---
title: "Microchip ARM Cortex-M4F CEC1302 Low Power RTOS Demo - Using the Keil, GCC and MikroC development tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### Introduction

This page documents an RTOS demo application for the ARM Cortex-M4F based
[CEC1302 microcontroller
from Microchip](http://ww1.microchip.com/downloads/en/DeviceDoc/00002022B.pdf). Pre-configured projects are provided for the following
compiler and tool combinations:
* Keil uVision, using the ARM compiler
* Keil uVision, using the [GCC](https://launchpad.net/gcc-arm-embedded) compiler
* [mikroC Pro](http://www.mikroe.com/mikroc/arm/) for ARM

The project can be configured to create either a simple blinky style project
that demonstrates how power can be saved by using the
[RTOS's tickless idle feature](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support),
or a more comprehensive test and demo application that tests the port's integrity
and demonstrates many RTOS features.

---

#### *IMPORTANT! Notes on using the FreeRTOS CEC1302 demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-microchip-arm-cortex-m4-rtos-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting),
noting in particular the recommendation to develop with
[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) defined
in FreeRTOSConfig.h.

---

### Source Code Organisation

The FreeRTOS zip file contains the source files for all the FreeRTOS
ports, and all the demo applications. Only a few of these files are needed by this
project.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

* The Keil uVision project that uses the ARM compiler is called
 RTOSDemo.uvprojx, and is located in the
 FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_Keil\_GCC/Keil\_Specific
 directory of the main [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).
* The Keil uVision project that uses the GCC compiler is also called
 RTOSDemo.uvprojx, and is located in the
 FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_Keil\_GCC/GCC\_Specific
 directory of the main [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).
* The MikroC Pro for ARM project is called
 RTOSDemo.mcpar, and is located in the
 FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_MikroC/MikroC\_Specific
 directory of the main [FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).

**Caution:** The MikroC compiler will leave many temporary files
throughout your project directory structure, the built in editor
is not compatible with the formatting conventions used by the RTOS source files,
and to allow the FreeRTOS source files to be built the FreeRTOS MikroC port layer
#defines the 'const' keyword away to nothing.

---

### The Microchip ARM Cortex-M4 RTOS Demo Application

#### Hardware set up - uVision projects

Normally RTOS demo applications indicate their status by controlling the rate at
which an LED is toggled. However, the uVision demos do not target any specific
hardware, so are not configured to toggle any specific LED on any particular IO
port. Instead, a variable called ulLED is incremented each time an LED would
otherwise be toggled.

The ulLED variable is incremented by the macro configTOGGLE\_LED(), which is
defined in FreeRTOSConfig.h. If your target hardware has a spare LED, then
configTOGGLE\_LED() can be updated to make use of the LED. Otherwise ulValue can
be added to the uVision IDE's data watch window, where its value will be seen to
updated as the RTOS demo application executes (provided a capable debug interface
is used, such as a ULINK).

The ARM compiler and GCC compiler versions of the uVision projects can also
be executed on the Clicker hardware described in the next section by creating an
adapter cable that maps the Mikro mProg cable to a standard ARM JTAG connector.
The required pin-out is detailed in the table below (assumes a 20-pin JTAG connector).

|  |  |  |
| --- | --- | --- |
| **Signal Names**  | **ARM 20 Pin #**  | **mPROG Pin #**  |
| <br /> VCC +3.3V<br />  | <br /> 1<br />  | <br /> 1<br />  |
| <br /> Ground<br />  | <br /> 20<br />  | <br /> 9<br />  |
| <br /> JTAG\_TDI<br />  | <br /> 5<br />  | <br /> 8<br />  |
| <br /> JTAG\_TMS<br />  | <br /> 7<br />  | <br /> 2<br />  |
| <br /> JTAG\_TCLK<br />  | <br /> 9<br />  | <br /> 4<br />  |
| <br /> JTAG\_TDO<br />  | <br /> 13<br />  | <br /> 6<br />  |
| <br /> RTCK<br />  | <br /> 11 and 12<br />  | <br /> Ground<br />  |

#### Hardware set up - MikroC Pro for ARM project

The MikroC project is pre-configured to run on a
[CEC1302 Clicker board](http://www.mikroe.com/clicker/), and uses
the LED built onto that hardware.

#### Functionality

The project provides two RTOS demo applications. A simple blinky style project
that demonstrates low power tickless functionality, and a more comprehensive
test and demo application. The configCREATE\_LOW\_POWER\_DEMO setting, which is
defined in FreeRTOSConfig.h, is used to select between the two.

#### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 1

When configCREATE\_LOW\_POWER\_DEMO is set to 1 main() calls main\_low\_power(), which
creates a very simple demo as follows:

* Two tasks are created, an Rx task and a Tx task.
* The Rx task blocks on a queue to wait for data, blipping (turning on then
 off again) an LED (or toggling
 the ulLED variable) each time data is received. The LED is only blipped
 on briefly so it does not effect current consumption too much.
* The Tx task sends a value through the queue to the Rx
 task every 1000ms (resulting in the Rx task exiting the blocked state to blip
 the LED).

#### Observed behaviour when configCREATE\_LOW\_POWER\_DEMO is set to 1

Both tasks spend most of their time in the Blocked state, during which periods
the RTOS tick is turned off, and the ARM Cortex-M4F is placed into a low power state.
Every 1000ms the MCU will come out of the low power state, turn the LED on,
return to the low power state for 10ms, before leaving the low power
state again to turn the LED off. This will be observed as a short blip on the LED
every 1000ms.

#### RTOS implementation when configCREATE\_LOW\_POWER\_DEMO is set to 1

The demo is provided with a [low power tickless implementation](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
that uses the CEC1302 hibernation timer to generate the RTOS tick interrupt.

This CEC1302 specific
tickless implementation includes the same configPRE\_SLEEP\_PROCESSING() and
configPOST\_SLEEP\_PROCESSING() macros that are described on
[the page that documents
the generic Cortex-M tickless implementation](low-power-ARM-cortex-rtos.md#using_mcu_specific_features). The pre sleep macro can be
defined to take additional application specific actions to improve energy efficiency
before entering the low power state, and the post sleep macro can be defined to
reverse any of the actions taken by the pre sleep macro. For example, if the
pre-sleep macro is defined to turn a peripheral off, and the post sleep macro is
defined to turn the peripheral on again, then the peripheral will automatically
be turned off prior to each entry into the sleep mode, and automatically turned back
on again on each exit from the sleep mode.

#### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 0

When configCREATE\_LOW\_POWER\_DEMO is set to 0 main()
calls main\_full(), which creates a comprehensive test and demo application
that demonstrates:

* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
* [Statically allocated RTOS objects](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' task is created that periodically inspects the standard
demo tasks to ensure all the tasks are functioning
as expected. The check task toggles an LED (or increments the ulLED variable).
This gives a visual feedback of the
system health. **If an LED is toggling every 3 seconds, then the
check task has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check task has
discovered a problem in one or more tasks.**

#### Building and executing the demo application

##### Using the uVision project with the GCC compiler

1. Ensure a suitable GCC compiler is installed on the host computer. The
 project was created and tested with the arm-none-eabi-gcc compiler,
 pre-built binaries for which are freely available from the
 [launchpad.net](https://launchpad.net/gcc-arm-embedded)
 website.
2. Open FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_Keil\_GCC/GCC\_Specific/RTOSDemo.uvprojx
 from within the Keil IDE.
3. Open the Manage Project Items window within the uVision IDE ("Project->Manage->Project Items" menu item)
 and set the GCC prefix and installation folder to be correct for your
 host computer.

![setting the path to the GCC compiler in Keil uVision](/media/2018/Setting_GCC_Path_In_Keil_uVision.png)

**Setting the path to the GCC compiler binary

 Note the path does not include the training "/bin"**
4. Open FreeRTOSConfig.h, and set configCREATE\_LOW\_POWER\_DEMO to generate either
 the tickless low power demo, or the full test and demo application, as
 required.
5. Ensure the target hardware is connected to the host computer through a
 suitable debug connector, such as a ULINK2.
6. Select 'Rebuilt All Target Files' from the IDE's 'Project' menu, the
 RTOSDemo project should compile without any errors or warnings.
7. After the build completes, select "Start/STOP Debug Session" from the IDE's Debug
 menu to download the application to the CEC1302 ARM Cortex-M4F microcontroller RAM memory,
 start a debug session, and have the debugger break on entry into the main() function.
 If the debug session does not start as expected then ensure the debug options,
 and in particular the "Connect & Reset Options" section of the debug options,
 are set as shown below.

![configuring a debug session to connect to the ARM Cortex-M processor](/media/2018/CEC1302_ARM_Cortex_RTOS_Connect.jpg)

**The required connect and reset options**

##### Using the uVision project with the ARM compiler

1. Open FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_Keil\_GCC/Keil\_Specific/RTOSDemo.uvprojx
 from within the Keil IDE.
2. Open FreeRTOSConfig.h, and set configCREATE\_LOW\_POWER\_DEMO to generate either
 the tickless low power demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer through a
 suitable debug connector, such as a ULINK2.
4. Select 'Rebuilt All Target Files' from the IDE's 'Project' menu, the
 RTOSDemo project should compile without any errors or warnings, although
 a warning may be generated by the linker as, to enable the maximum number
 of tests to be added to the comprehensive demo, the linker script is
 configured to place both code and data in the same named section.
5. After the build completes, select "Start/STOP Debug Session" from the IDE's Debug
 menu to download the application to the CEC1302 ARM Cortex-M4F microcontroller RAM memory,
 start a debug session, and have the debugger break on entry into the main() function.
 If the debug session does not start as expected then ensure the debug options,
 and in particular the "Connect & Reset Options" section of the debug options,
 are set as shown by the image provided as part of the GCC instructions
 above.

##### Using the MikroC Pro compiler for ARM and the [Clicker](http://www.mikroe.com/clicker/) hardware

**Caution:** The MikroC compiler will leave many temporary files
throughout your project directory structure, the built in editor
is not compatible with the formatting conventions used by the RTOS source files,
and to allow the FreeRTOS source files to be built the FreeRTOS MikroC port layer
#defines the 'const' keyword away to nothing.

1. Open FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_MikroC/MikroC\_Specific/RTOSDemo.mcpar
 from within the MikroC Pro IDE.
2. Open the Search Paths window ("Projects->Edit Search Paths" menu item)
 and update the paths to the source files and header files to be correct
 for your host computer.

![setting the path to the free RTOS source files and header files](/media/2018/Setting_MikroC_Paths.png)

**Setting the path to source and header files**
3. As provided, the MikroC demo uses the [FreeRTOS/Source/portable/MemMang/heap\_4.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
 memory allocator, and a [malloc failed hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) is
 defined. It is necessary to make a small edit to the heap\_4.c source file
 to make it compatible with the MikroC compiler. Open heap\_4.c and locate
 the following code:

```c

#if( configUSE_MALLOC_FAILED_HOOK == 1 )
{
    if( pvReturn == NULL )
    {
        extern void vApplicationMallocFailedHook( void ); /* Move this line. */
        vApplicationMallocFailedHook();
    }
    else
    {
        mtCOVERAGE_TEST_MARKER();
    }
}
#endif
```

 Move the line highlighted (the line starting 'extern') from its current
 position to the top of the source file so it has file scope rather than
 block scope.
4. Open FreeRTOSConfig.h, and set configCREATE\_LOW\_POWER\_DEMO to generate either
 the tickless low power demo, or the full test and demo application, as
 required.
5. Select 'Build' from the IDE's 'Build' menu to create an executable image.
6. Ensure the Clicker hardware is powered through its USB port, and connected
 using a MikroProg flash programmer, before selecting "mE Programmer"
 from the "Tools" menu to download the executable image to the CEC1302 ARM Cortex-M4F
 microcontroller. If the download does not start as expected then ensure
 the Programmer/Debugger Options are as shown in the image below
 ("Tools->Programmer/Debugger Options" menu item).

![setting the MikroC Pro compiler debug options for the ARM Cortex-M processor](/media/2018/MikroC-clicker-ARM-CortexM-debug-options.png)

**The required programmer and debug options**
7. After the download completes, select "Start Debugger" from the "Debug"
 menu to start a debug session, and run the application.
 If the debugger does not start as expected then ensure
 the Programmer/Debugger Options are as shown in the image above
 ("Tools->Programmer/Debugger Options" menu item).

---

### RTOS Configuration and Usage Details

#### ARM Cortex-M4 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in /FreeRTOS/Demo/CORTEX\_M4F\_CEC1302\_Keil\_GCC/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ**

 This sets the frequency of the RTOS tick interrupt. The setting used by
 this demo depends on the configCREATE\_LOW\_POWER\_DEMO setting.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M4 NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents that are defined using just the 3 priority bits implemented in the CEC1302
 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority()
 requires the un-shifted 3 bit format.

Attention please!: See the [page dedicated to setting interrupt priorities on ARM Cortex-M devices](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4). Remember that ARM Cortex-M cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0,
and therefore the highest priority possible.

The lowest priority on a ARM Cortex-M core is in fact 255 - however different
ARM Cortex-M microcontroller manufacturers implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on Microchip CEC1302 ARM Cortex-M4 microcontrollers, the lowest priority you can specify is in fact 7 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

#### Aggregated and disaggregated interrupts

The CEC1302 can route groups of interrupt sources to the same interrupt
vector (aggregated interrupts), or route all interrupt sources to their own unique interrupt
vector (disaggregated interrupts). The RTOS itself only uses ARM Cortex-M system interrupts,
which are always routed to the standard ARM Cortex-M system vectors, but the demo
application also makes
use of btimer (basic timer) and htimer (hibernation timer) interrupts, both of
which can be aggregated or disaggregated. In order to
demonstrate both methods, the tickless low power demo is configured to use
aggregated interrupts and the comprehensive demo is configured to use disaggregated
interrupts (note the comprehensive demo uses disaggregated interrupts as the
interrupt nesting test cannot function if all the timer interrupts are routed
through the same vector).

#### Interrupt service routines

Unlike many FreeRTOS ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portYIELD\_FROM\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portYIELD\_FROM\_ISR() will leave interrupts enabled.

The following source code snippet is provided as an example. The interrupt
uses a [direct to task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
to synchronise with a task (not shown), and calls portYIELD\_FROM\_ISR()
to ensure the interrupt returns directly to the task if the task has an equal
or higher priority than the interrupted task.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose.
 Note lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)( xHandlingTask, &xHigherPriorityTaskWoken );

    /* If the notified task was blocked waiting for the notification, and the
 task has a priority higher than the current Running state task (the task
 that this interrupt interrupted), then lHigherPriorityTaskWoken will have
 been set to pdTRUE internally within vTaskNotifyGiveFromISR(). Passing
 pdTRUE into the portYIELD\_FROM\_ISR() macro will result in a context
 switch being pended to ensure this interrupt returns directly to the
 unblocked, higher priority, task. Passing pdFALSE into portYIELD\_FROM\_ISR()
 has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
configuration constant (or configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY).

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the SysTick and PendSV interrupts. SVC number #0 is also used.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

[configSUPPORT\_STATIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
and [configSUPPORT\_DYNAMIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) are
both set to 1, allowing RTOS objects to be
[created statically or dynamically](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation).
Source/Portable/MemMang/heap\_4.c is used to provide the
RAM required by dynamically allocated RTOS objects.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
