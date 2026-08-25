---
title: "Low Power RTOS Demo - ST STM32LUsing IAR and the STM32L-Discovery Board"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![STM32L Discovery board from ST for low power applications](/media/2018/stm32l-discovery_board.jpg)

**The STM32L Discovery Board** 

### Introduction

The demo application documented on this page demonstrates how the FreeRTOS
[tick suppression](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) (tickless idle mode)
features can be used to minimise the power consumption of an
application running on a [STM32L152 ARM Cortex-M3 microcontroller](http://www.st.com/web/catalog/mmc/FM141/SC1544/SS1374/LN1041/PF248820)
from [ST](http://www.ST.com/). The STM32L is
designed specifically for use in applications that require extremely low power
consumption.

The demo uses the FreeRTOS IAR ARM Cortex-M3/4 port, the
[IAR Embedded Workbench for ARM](http://www.iar.com/ewarm/) IDE (EWARM),
and components of the [STM32L Standard Peripheral Library](http://www.st.com/web/en/catalog/tools/PF257913).
The project is pre-configured to run on the very low cost [STM32L Discovery board](http://www.st.com/web/en/catalog/tools/PF250863).

![](/media/2018/FreeRTOS-STM32L152-Debug-Session-Screen-Shot.jpg)

**EWARM Ships with a FreeRTOS Kernel Aware Plug-in** 

---

|  |
| --- |
| *IMPORTANT! Notes on using the STM32L RTOS demo*<br/>*Please read all the following points before using this RTOS port.*<br/><br/>1. [Source Code Organisation](#source-code-organisation)<br/>2. [The Demo Application](#the-st-stm32-arm-cortex-m3-demo-application)<br/>3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)<br/><br/><br/> See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting) |

---

### Source Code Organisation

The official FreeRTOS zip file download contains the source files for all the RTOS
ports, and all the demo applications, only a few of which are needed by this
project.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The IAR project file for the STM32L152 demo application is called
RTOSDemo.eww, and is located in the FreeRTOS/Demo/CORTEX\_STM32L152\_Discovery\_IAR
directory.

---

### The ST STM32 ARM Cortex-M3 Demo Application

#### Hardware set up

The demo uses the LED built onto the STM32L Discovery Board and no hardware setup is required.

#### Functionality

The single project file can be configured to create either a low power demo, or
a standard RTOS demo. The configCREATE\_LOW\_POWER\_DEMO constant is used to switch between
the two. configCREATE\_LOW\_POWER\_DEMO is defined at the top of FreeRTOSConfig.h
(FreeRTOS/Demo/CORTEX\_STM32L152\_Discovery\_IAR/include/FreeRTOSConfig.h, and included in
the IAR project).

##### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 1

If configCREATE\_LOW\_POWER\_DEMO is set to 1 then main() calls main\_low\_power().
main\_low\_power() is implemented in the main\_low\_power.c C source file.

Low power modes are entered when the RTOS tick is stopped (suppressed).
Deeper low power modes have longer wake up periods that lighter low power
modes, and power is also used simply entering and especially exiting the low
power modes. How the low power modes are used therefore requires careful
consideration to ensure power consumption is truly minimised and that the
embedded device meets its real time requirements.

The low power demo is configured to
select between four different modes depending on the anticipated idle period.
Note the time thresholds used to decide which low power mode to enter are
purely for convenience of demonstration, and are not intended to represent
optimal values for any particular application.

The STM32L specific part of the tickless operation is implemented in the
STM32L\_low\_power\_tick\_management.c C source file. Tick interrupts are generated from the TIM2
peripheral so a slow input clock can be used and the timer can be configured to
carry on running when the STM32 is in the lighter of the used low power modes.

**Implementation:** 

* Two tasks are created, an Rx task and a Tx task. A queue is created to
 pass a message from the Tx task to the Rx task.
* The Rx task blocks on a queue to wait for data, blipping an LED each time
 data is received (turning it on and then off again) before returning to
 block on the queue once more.
* The Tx task repeatedly blocks on an attempt to obtain a semaphore, and
 unblocks if either the semaphore is received or its block time expires.
 After leaving the blocked state the Tx task uses the queue to send a
 value to the Rx task, which in turn causes the Rx task to exit the
 Blocked state and blip the LED. The rate at which the LED is seen to blip
 is therefore dependent on the block time.
* The Tx task's block time is changed by the interrupt service routine that
 executes when the USER button is pressed. The low power mode entered
 depends on the block time (as described in the Observed Behaviour section
 below). Four block times are used: short, medium, long and infinite.

**Low Power Behaviour:** 

1. The block time used by the Tx task is initialised to its 'short' value,
 so when the Tx task blocks on the semaphore it times-out quickly, resulting
 in the LED toggling rapidly. The timeout period is less than the value of
 configEXPECTED\_IDLE\_TIME\_BEFORE\_SLEEP (set in FreeRTOSConfig.h), so the
 initial state does not suppress the tick interrupt or enter a low power mode.
2. When the button is pressed the block time used by the Tx task is increased
 to its 'medium' value. The longer block time results in a slowing of the
 rate at which the LED toggles. The time the Tx task spends in the blocked
 state is now greater than configEXPECTED\_IDLE\_TIME\_BEFORE\_SLEEP, so the tick
 is suppressed. The MCU is placed into the 'Sleep' low power state while the
 tick is suppressed.
3. When the button is pressed again the block time used by the Tx task is
 increased to its 'long' value, so the rate at which the LED is observed to
 blip gets even slow. When the 'long' block time is used the MCU is placed
 into its 'Low Power Sleep' low power state.
4. The next time the button is pressed the block time used by the Tx task is
 set to infinite, so the Tx task does not time out when it attempts to obtain
 the semaphore, and therefore the LED stops blipping completely. Both tasks
 are now blocked indefinitely and the MCU is placed into its 'Stop' low power
 state.
5. Pressing the button one final time results in the semaphore being 'given'
 to unblock the Tx task, the CPU clocks being returned to their pre-stop
 state, and the block time being reset to its 'short' time. The system is
 then back to its initial condition with the LED blipping rapidly.

##### Functionality with configCREATE\_LOW\_POWER\_DEMO set to 0

If configCREATE\_LOW\_POWER\_DEMO is set to 0 then main() calls main\_full().
main\_full() is implemented in the main\_full.c C source file.

main\_full() creates a comprehensive test and demo application
that demonstrates:

* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all RTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' software timer is created that periodically inspects the standard
demo tasks to ensure all the tasks are functioning
as expected. The check software timer's
callback function toggles the LED on the STM32L Discovery Board.
This gives a visual feedback of the
system health. **If the LED is toggling every 3 seconds, then the
check software timer has not discovered any problems. If the LED is
toggling every 200 milliseconds, then the check software timer has
discovered a potential problem in at least one task.**

#### Building and executing the demo application

1. Open FreeRTOS/Demo/CORTEX\_STM32L152\_Discovery\_IAR/RTOSDemo.eww
 from within the IAR IDE.
2. Open FreeRTOSConfig.h, and set configCREATE\_LOW\_POWER\_DEMO to generate either
 the tickless low power demo, or the full test and demo application, as
 required.
3. Ensure the target hardware is connected to the host computer using a suitable
 USB cable.
4. Press F7 to build the project. The demo should build without any errors
 or warnings.
5. After the build completes, press CTRL+D to program the STM32L microcontroller
 flash memory, start a debug session, and have the debugger break on entry
 into the main() function.

---

### RTOS Configuration and Usage Details

#### ARM Cortex-M3 FreeRTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_STM32L152\_Discovery\_IAR/include/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization). In particular -

* **configTICK\_RATE\_HZ** 

 This sets the frequency of the RTOS tick interrupt. The setting used by
 this demo depends on the configCREATE\_LOW\_POWER\_DEMO setting.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.
* **configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 Whereas configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are full eight bit shifted values, defined to be used as raw numbers directly
 in the ARM Cortex-M3 NVIC registers, configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY
 and configLIBRARY\_MAX\_SYSCALL\_INTERRUPT\_PRIORITY
 are equivalents that are defined using just the 4 priority bits implemented in the STM32L
 NVIC.
 These values are provided because the CMSIS library function NVIC\_SetPriority() and
 STM32 standard peripheral library functions requires the un-shifted 4 bit format.

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
on ST STM32 ARM Cortex-M3 microcontrollers, the lowest priority you can specify is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

NVIC\_PriorityGroupConfig( NVIC\_PriorityGroup\_4 ) must the called before
any other interrupt priority related functions from the STM32 Standard peripheral
library, as it is in the demo provided.

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
EXTI0\_IRQHandler() in the file main\_low\_power.c included in this demo project for another
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

When configCREATE\_LOW\_POWER\_DEMO is set to 0 the standard FreeRTOS Cortex-M port is
used, which requires exclusive use of the SysTick and PendSV interrupts. SVC number #0 is also used.

When configCREATE\_LOW\_POWER\_DEMO is set to 1 exclusive access to the TIM2
peripheral is required.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
