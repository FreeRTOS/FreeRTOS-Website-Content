---
title: "Renesas RX200 DemoUsing the Renesas Compiler and HEW IDE"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/Renesas-RSKRX210.jpg)  
Renesas RX210 Starter Kit (RSK)

This page documents the [Renesas RX210](http://www.renesas.eu/products/mpumcu/rx/rx200/rx210/rx210_root.jsp)
FreeRTOS port and demo application that uses the [Renesas RX](http://www.renesas.com/compiler) compiler,
and [HEW IDE](http://www.renesas.com/hew). The project is pre-configured to run on the RSKRX210 starter kit.

This demo application demonstrates:

* A high frequency interrupt that uses an interrupt priority that is [**never**
 disabled by the RTOS kernel](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority).
* Interrupts nesting to a depth of 4.
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* Malloc failed, stack overflow and idle [hook functions](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions).

---

#### *IMPORTANT! Notes on using the Renesas RX200 port and demo application*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#important-notes-on-using-the-renesas-rx200-port-and-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The HEW workspaces for the RSK development board is called RTOSDemo.hws and is located in the
FreeRTOS/Demo/RX200\_RX210-RSK\_Renesas directory.

The FreeRTOS zip file download contains the implementation of all the FreeRTOS ports, and every single official
demo application project. It therefore contains many more files than used by this demo. See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
of the downloaded files and information on creating a new project.

---

### RX210 Demo Application

#### Functionality

The project includes three build configurations:

|  |  |
| --- | --- |
| **Build configuration** | **Description** |
| <br /> Blinky<br />  | <br /> This is a **very simple example** that creates two tasks and<br /> one queue. The tasks communicate with each other via the queue,<br /> and an LED is toggled on each successful queue receive. The main()<br /> function used by the Blinky build configuration is defined in<br /> main-blinky.c. The main() function used by the other two<br /> build configurations is defined in main-full.c.<br />  |
| <br /> Debug<br />  | <br /> This is a very comprehensive demo that creates nearly 50 tasks before<br /> starting the RTOS scheduler, then continuously dynamically creates and<br /> deletes another two tasks as the application executes. It also creates<br /> many queues and different types of semaphore. The tasks consist<br /> mainly of the [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) tasks - which don't perform any<br /> particular functionality other than testing the port and demonstrating how the FreeRTOS API can be used.<br /> Information on additional tasks that are created is provided immediately below this table.<br /> The Debug build configuration includes standard demo tasks that demonstrate<br /> interrupt nesting, but does not include the high frequency timer interrupt.<br />  |
| <br /> Debug\_with\_optimisation<br />  | <br /> This is similar to the Debug build configuration, but includes the<br /> high frequency timer interrupt. The build configuration also has<br /> compiler optimisation turned up to maximum.<br />  |

The Debug and Debug\_with\_optimisation build configurations create the following tasks, timers, and tests, in addition to the standard demo tasks:

* Check timer and callback function
 
 The Check timer is an example of a very simple watchdog type timer. It monitors
 all the other standard demo tasks, and the register test tasks (described below),
 and provides visual feedback of the system status using an LED.

 The period of the check timer is initially set to five seconds. The check
 timer callback function checks that all the standard demo tasks, and the
 register test tasks, are not only still executing, but are executing without
 reporting any errors, then toggles an LED.

 If the check timer discovers that a task has either stalled, or reported an
 error, then it changes its own period from the initial five seconds, to just
 200ms. Therefore, if the LED toggles every five seconds, no issues have been
 discovered, whereas, if the LED toggles every 200ms, an issue has been
 discovered in at least one task.

 The check timer uses LED marked LED3 on the RSK silkscreen.
* Reg test tasks
 
 These two tasks test the RTOS kernel context switch mechanism by first filling
 each RX200 register with a known and unique value, then repeatedly checking
 that the value originally written to the register is maintained in the
 register, for the lifetime of the task. The tasks execute at the lowest
 possible priority (the idle priority), so are preempted frequently. The
 nature of these tasks necessitates that they are written in assembly.
* High frequency timer test
 
 This test configures a timer to generate an interrupt at 20KHz. The interrupt priority is above
 [configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority), so will never
 be disabled by the RTOS kernel. The jitter experienced in the interrupt timing is measured and
 stored in a variable that can be inspected using the debugger.
* Button input interrupts and LCD demo
 
 This demo defines three IRQ interrupt handlers that are triggered by
 button presses, a task that controls the top line of the LCD, a task that
 controls the bottom line of the LCD, and a queue that is used to communicate
 between the interrupt handlers and one of the tasks.

 The task that controls the top line of the LCD simply scrolls a message
 back and forth, with the scroll direction changing each time the message
 reaches the end of the LCD.

 The task that controls the bottom line of the LCD acts just like the one
 controlling the top line, until button SW2 is pressed. Pressing button
 SW2 causes and interrupt to be generated. The interrupt handler uses
 the queue to send a command to the task instructing it to halt or restart
 the scrolling motion. While the scrolling
 is halted, the interrupts generated by pressing buttons SW3 and SW1 result
 in commands being sent to the task, on the same queue, instructing the
 task to nudge the message left and right respectively, one character at
 a time.

When executing, the demo application will behave as follows:

* LEDs LED0, LED1 and LED2 are under the control of the standard 'flash' tasks. Each will toggle at a fixed but different frequency, with LED0
 using the highest frequency, and LED 2 using the lowest.
* LED3 is under the control of the 'check' timer. It will toggle every five seconds if all the other tasks are reporting their status as
 healthy. It will toggle every 200ms if any task has ever reported an error.
* "http://www.FreeRTOS.org" will continuously scroll left to right, then back right to left, along the top line of the LCD.
* A long string that describes the features available on the RX210 will scroll left to right, then back right to left,
 along the bottom line of the LCD, until button SW2 is pressed. Pressing button SW2 will cause the scrolling to halt, pressing
 button SW2 again will start the string scrolling again. While the string is stationary, pressing button SW3 will nudge the string
 to the left, one character at a time, and pressing button SW1 will nudge the string to the right, one character at a time.

#### Building and executing the demo application

1. Before opening the project - connect the RX210 RSK to the host computer using an [E1 FINE interface](http://www.renesas.com/e1),
 which is provided in the RSK kit. Once connected, apply power to the development board.
2. Open the FreeRTOS/Demo/RTOSDemo.hws workspace from within the HEW IDE - following the prompts
 to connect to the target interface as the project opens.
3. Select "Build" from the HEW "Build" menu - the demo application should build without any genuine errors or warnings,
 although dependency errors are produced as the pre-processor [inexplicable] looks for header files that omitted
 from the build by preprocessor directives - these erroneous errors will not effect the build.
4. When the build has completed, a dialogue box will appear that asks if you want the produced binary to be downloaded to the
 RX210 microcontroller - select "yes" to program the flash, and start a debug session. The debugger will break on entry
 to the main() function.

---

### RTOS Configuration and Usage Details

#### FreeRTOS RX200 RTOS port specific configuration

Configuration items specific to this demo are defined in FreeRTOS/Demo/RX200\_RX210-RSK\_Renesas/RTOSDemo/FreeRTOSConfig.h. The
constants can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ** 

 Sets the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality, but is faster than needed by most applications.
 Lowering this frequency will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY** 

 Defines the interrupt priority used for by the tick and yield interrupts
 (the RTOS kernel interrupts). configKERNEL\_INTERRUPT\_PRIORITY should normally be set to
 the lowest interrupt priority, which is 1 on an RX200 core. See
 [the customization pages](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) for more information.
* **configMAX\_SYSCALL\_INTERRUPT\_PRIORITY** 

 Defines the maximum interrupt priority from which FreeRTOS API functions
 can be called. Interrupts at or below this priority can call FreeRTOS
 API functions **provided that** the API function ends in 'FromISR'.
 Interrupts above this priority cannot call any FreeRTOS API functions,
 but will never be disabled by the RTOS kernel. Interrupts that have a priority
 above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY are therefore suitable for
 functionality that requires very high timing accuracy. The high
 frequency timer test included in this demo uses a priority that is above
 configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. See [the configuration pages](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) for more information.

The RX200 port layer #defines 'BaseType\_t' to 'long'.

#### Writing interrupt service routines (ISRs)

Interrupt service routines can be implemented using the standard Renesas compiler
syntax. For example, the demo application defines the high frequency timer using:

```c

/* The 'enable' in the following line causes the compiler to generate code that
re-enables interrupts on function entry. This will allow interrupts to nest
(although in this case the high frequency timer interrupt is the highest priority
interrupt in the demo). */
#pragma interrupt ( prvTimer2IntHandler( vect = _VECT( _CMT2_CMI2 ), enable ) )
static void prvTimer2IntHandler( void )
{
    /* ISR implementation goes here. */
}
```

See the examples provided by Renesas and the compiler documentation for full details.

Often an ISR wants to cause a context switch, so the task that the ISR returns to when
the ISR processing is completed is different from the task that the ISR originally
interrupted. This would be the case if the ISR caused a task to unblock, and the task
that was unblocked has a priority above the task in the Running state (the task
that was interrupted). The macro portYIELD\_FROM\_ISR() is provided for this
purpose. portYIELD\_FROM\_ISR() takes a single parameter: If the parameter is
zero, a context switch is not performed, if the parameter is non-zero, a context
switch is performed. This is demonstrated in the code below - which is
part of the RX210 demo, and implemented in
FreeRTOS/Demo/RX200\_RX210-RSK\_Renesas/RTOSDemo/ButtonAndLCD.c.

```c

/* The 'enable' in the following line causes the compiler to generate code that
re-enables interrupts on function entry. This will allow interrupts to nest. */
#pragma interrupt ( prvIRQ1_Handler( vect = 65, enable ) )

static void prvIRQ1_Handler( void )
{
static TickType_t xTimeLastInterrupt = 0UL;
static const unsigned char ucCommand = lcdSHIFT_BACK_COMMAND;
BaseType_t xHigherPriorityTaskWoken;

  /* prvSendCommandOnDebouncedInput() returns true or false, depending on
 whether the function unblocked a task that has equal or higher priority than the task
 that is already in the running state. */
  xHigherPriorityTaskWoken = prvSendCommandOnDebouncedInput( &xTimeLastInterrupt,
                                                             ucCommand );
  portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```

#### Resources used by FreeRTOS

FreeRTOS requires exclusive use of the software interrupt.
FreeRTOS also requires exclusive use of a timer that is capable of generating the tick interrupt - but
it is up to the application writer to define which timer is used.

The application must define a function called vApplicationSetupTimerInterrupt() to
configure the tick interrupt, then define configTICK\_VECTOR to be the interrupt vector
number associated with the chosen timer source.

It is suggested that a compare match timer is used to generate the tick interrupt, and an example
implementation of vApplicationSetupTimerInterrupt() that uses compare match timer 0 is
included in both main-full.c and main-blinky.c in this demo application.
The demo application defines configTICK\_VECTOR within FreeRTOSConfig.h to be \_CMT0\_CMI0 (the compare
match 0 interrupt vector number). The provided example implementations can be used
in any application that does not itself need to use the compare match 0 timer/interrupt.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within RTOSDemo/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The full demo application may not execute correctly when the co-operative RTOS scheduler is
selected.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the RX210 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
