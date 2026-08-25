---
title: "Atmel SAM4L Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Low Power RTOS Demo - Atmel SAM4L Using the free Atmel Studio 6 IDE, GCC, and the Atmel Software Framework

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


![SAM4L-EK microcontroller evaluation kit from Atmel](/media/2018/Atmel_SAM4L-EK.jpg)


### Introduction

The application documented on this page demonstrates how the FreeRTOS
[tick suppression](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
features can be used to minimise the power consumption of an
application running on a [SAM4L ARM Cortex-M4 microcontroller](http://www.microchip.com/wwwproducts/en/ATSAM4LC4C)
from Atmel. The SAM4L is
designed specifically for use in applications that require extremely low power
consumption.

The demo uses the FreeRTOS GCC ARM Cortex-M3/4 port, the free
[Atmel Studio 6 IDE](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio), and components
of the comprehensive [Atmel Software Framework](https://www.microchip.com/avr-support/advanced-software-framework-(asf))
(ASF). The project is pre-configured to run on the [SAM4L-EK](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=atsam4l-ek) evaluation kit.

---

#### *IMPORTANT! Notes on using the FreeRTOS SAM4L demo project*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-atmel-arm-cortex-m4-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS zip file contains the source files for all the FreeRTOS
ports, and all the demo applications, only a few of which are needed by this
project.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The Atmel Studio 6 Solution file for the ATSAM4L demo application is called
FreeRTOS\_Demo.atsln, and is located in the FreeRTOS/Demo/CORTEX\_M4\_ATSAM4L\_Atmel\_Studio
directory.


---

### The Atmel ARM Cortex-M4 Demo Application


#### Hardware set up

The demo uses the LEDs built onto the SAM4L-EK and no hardware setup is required.


#### Functionality

configCREATE\_LOW\_POWER\_DEMO is a constant that is defined at the top of
FreeRTOSConfig.h. The low power demo is created when the project is built with
configCREATE\_LOW\_POWER\_DEMO set to 1. A standard kernel only demo (without tick
suppression) is created when the project is built with configCREATE\_LOW\_POWER\_DEMO
set to 0.


#### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 1

When configCREATE\_LOW\_POWER\_DEMO is set to 1 main() calls main\_low\_power().
main\_low\_power() creates a very simple demo as follows:

* Two tasks are created, an Rx task and a Tx task.
* The Rx task blocks on a queue to wait for data, blipping an LED each time
 data is received (turning it on and then off again) before returning to
 block on the queue once more. The LED is only blipped on briefly so it
 does not effect the current reading too much.
* The Tx task repeatedly enters the Blocked state for 500ms. On exiting
 the blocked state the Tx task sends a value through the queue to the Rx
 task (causing the Rx task to exit the blocked state and blip the LED).


#### Observed behaviour when configCREATE\_LOW\_POWER\_DEMO is set to 1

**For optimum low power results the SAM4L-EK must be connected and powered using
only the JTAG USB connector, but the debugger must not be connected** (the
application must be executed 'stand alone').

The MCU spends most of its time in the Retention low power state (see the implementation
section below), during
which times the current reading displayed on the board monitor that
is built onto the SAM4L-EK will show a low
current reading.

Every 500ms the MCU will come out of the low power state to turn the LED on,
then return to the low power state for 20ms, before leaving the low power
state again to turn the LED off. This will be observed as a rapid blip on the LED
every 500ms, and two very brief dots appearing on the graph of current consumption
that is displayed by the board monitor
that is built onto the SAM4L-EK. The two dots will often be observed as a
single dot due to their speed.

![](/media/2018/SAM4L-EK_board_monitor-e1663867111377.jpg)


**Current readings as shown by the board monitor display when the
   

 tickless low power application is executing** 


#### RTOS implementation when configCREATE\_LOW\_POWER\_DEMO is set to 1

The SAM4L microcontroller has several different low power modes. The low power
mode that consumes the least energy without losing the contents of the static
RAM and the CPU registers is called Retention mode. The RTOS turns off the tick
interrupt and places the SAM4L into its Retention low power state whenever both
tasks are in the Blocked state (when only the Idle task is able to execute).
Turning the tick interrupt off allows the microcontroller to remain in Retention
mode until it is time for a task to leave the Blocked state and execute. If the
RTOS tick interrupt was not suppressed in this way the microcontroller would have to
exit Retention mode each time a tick interrupt occurred.

The standard RTOS Cortex-M port uses the Cortex-M SysTick timer to generate
the RTOS tick interrupt, but the SysTick timer is halted when the SAM4L enters
retention mode so it cannot be used in this demo. Instead the RTOS tick is
generated by the Asynchronous Timer (AST). The AST continues
running in Retention mode, and its full 32-bit width and slow clocking allows the
RTOS tick to be suppressed for vastly longer periods than possible when using
SysTick.


#### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 0

When configCREATE\_LOW\_POWER\_DEMO is set to 0 main()
calls main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:

* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' software timer is created that periodically inspects the standard
demo tasks to ensure all the tasks are functioning
as expected. The check software timer's
callback function toggles an LED on the SAM4L-EK hardware.
This gives visual feedback of the
system health. **If an LED is toggling every 3 seconds, then the
check software timer has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check software timer has
discovered a problem in one or more tasks.**


#### Building and executing the demo application

1. Open FreeRTOS/Demo/CORTEX\_M4\_ATSAM4L\_Atmel\_Studio/FreeRTOS\_Demo.atsln
 from within the Atmel Studio IDE.
2. Open FreeRTOSConfig.h, and set configCREATE\_LOW\_POWER\_DEMO to generate either
 the tickless low power demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer through the
 J-Link USB connector built onto the SAM4L-EK board.
4. Select 'Build Solution' from the IDE's 'Build' menu, the
 RTOSDemo project should build without any errors or warnings.
5. After the build completes, select "Start Debug and Break" from the IDE's Debug
 menu to program the SAM4L microcontroller flash memory, start a debug
 session, and have the debugger break on entry into the main() function.
 
 Two things can prevent the download:
 

	1. If the SAM4L-EK has not been connected before the J-Link driver
	 might open a window to ask if you want to update the J-Link
	 firmware - but the window (at least at the time of writing) will
	 appear **underneath** the Atmel Studio 6 window.
	2. The J-Link will default to using JTAG mode, but the SAM4L-EK
	 requires SWD mode as shown below:
	 
	
	
	
	![](/media/2018/selecting_swd_mode_in_atmel_studio.jpg)
	
	  
	
	**Ensure to use SWD mode**
6. Ensure the debugger is stopped (completely stopped, not just paused) and
 that the application is free running before taking current readings.


---

### RTOS Configuration and Usage Details


#### ARM Cortex-M4 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_M4\_ATSAM4L\_Atmel\_Studio/src/FreeRTOSConfig.h.
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
 are equivalents that are defined using just the 4 priority bits implemented in the SAM4
 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority()
 requires the un-shifted 4 bit format.

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
on Atmel SAM4 ARM Cortex-M4 microcontrollers, the lowest priority you can specify is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all priority bits are assigned as
being preemption priority bits, and none as sub priority bits, as they are in the provided
demo.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.


#### Interrupt service routines

Unlike many FreeRTOS ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

The following source code snippet is provided as an example. The interrupt
uses a semaphore to synchronise with a task (not shown), and calls portEND\_SWITCHING\_ISR()
to ensure the interrupt returns directly to the task if the task has an equal
or higher priority than the interrupted task. See the function
USART1\_Handler() in the file serial.c included in this demo project for another
example.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
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

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M4 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.


#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.


  


 
