---
title: "Spansion (was Fujitsu) MB91460 demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/SK-91F467-FLEXRAY.jpg)

This page presents the FreeRTOS demo application for the 32bit Spansion MB91460 series RTOS port.

The demo is pre-configured to run on the SK-91F467-FLEXRAY starter kit from Spansion, and uses the
Softune compiler, debugger and IDE - which come on the kit CD. The starter
kit is fitted with a MB91467D MCU.

---

#### *IMPORTANT! Notes on using the Spansion MB91460 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The Softune workspace for the MB91460 demo is called 91467d\_FreeRTOS.wsp and can be located in the Demo/MB91460\_Softune directory.
The FreeRTOS zip file download contains files for all the ports and demo application projects. It therefore contains many more files
than used by this demo. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

---

### The Demo Application

#### Demo application setup

The starter kit jumpers must be set correctly for successful RS232 communication with the Softune IDE. The exact jumper settings required depends
on your individual set up. Please refer to the starter kit manual for more information.

The demo application includes an interrupt driven UART test where one task transmits characters that are then received by another task. For correct operation
of this functionality a loopback connector must be fitted to the UART 2 (X1) connector of the SK-91F467-FLEXRAY board (pins 2 and 3
must be connected together on the 9Way connector).

The demo uses the LEDs that are built onto the starter kit so no further specific hardware setup is required.

#### Building the demo application

1. Open the Demo/MB91460\_Softune/91467d\_FreeRTOS.wsp workspace from within the Softune IDE.
2. Select 'Build' from the IDE Project menu - the demo application should compile with no errors or warnings.

#### Starting a debug session

The instructions provided on this page utilise the Spansion debug monitor - which should already be programmed into the starter kit external Flash memory.
If you have erased or overwritten the Flash memory then you will first need to restore the debug monitor. Instructions for doing this are provided
in the starter kit manual.

To start the debug monitor:

1. Locate S5 on the starter kit board - this is a bank of 5 micro switches. Ensure switch 1 is in the On position, and the remaining 4 switches are in the Off position.
2. Power up or reset the starter kit. If LEDs D2, D4 and D8 are illuminated then the debug monitor is ready to receive the demo application download.

To download the demo application:

1. Ensure the debug monitor is running as described above.
2. Connect the starter kit supplied RS232 cable between port UART 4 (X4) on the starter kit and your host computer.
3. Select 'Setup Project' from the Softune 'Project' menu to bring up the project settings dialogue box.
4. In the project settings dialogue box, select the 'Debug' tab, 'Setup' category, and ensure the selected setup name is correct for you host computer.
 The image below demonstrates the setup used to communicate with the debug monitor using COM1 at 57K6 baud.

![](/media/2018/fujitsu-SK-91F467-FLEXRAY-debug-settings.jpg)  
Setting the method of communicating with the Spansion debug monitor.
5. Select 'Start Debug' from the Softune 'Debug' menu. The RTOS demo application will be downloaded to the starter kit RAM and execute up to the start of main().

Controlling a debug session:

1. Softune provides the expected step into, step over, watchpoint, breakpoint, etc. debugger functionality.
2. The Softune IDE cannot be used to pause a program that is free running on the starter kit hardware. An application that is free
 running can be interrupted by pressing button INT 0 (SW2) on the starter kit board - this will pause the program execution and return control to the
 Spansion debug monitor.

#### Demo Application Functionality

The demo application creates 8 co-routines, 44 persistent tasks, and periodically dynamically creates and destroys another 2 tasks. These tasks consist predominantly of the standard
demo application tasks (see the  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).

The following tasks and tests are created in addition to the standard demo tasks:

* Register test tasks
 This is a set of two tasks, each of which fill the MCU registers with known values, then immediately check that the registers
 contain the expected (written) value - an unexpected value being indicative of an error in the RTOS context switch mechanism.
 Each task uses different values, and as low priority tasks will regularly get interrupted.
* Check task
 The 'check' task is responsible for ensuring that all the standard demo tasks are
 executing as expected. It normally only executes every three seconds, but has the highest
 priority within the system so is guaranteed to get execution time. Any errors
 discovered by the check task are latched until the processor is reset. At the end
 of each cycle the check task toggles an LED. The LED will toggle every 3 seconds so long as all tasks
 are executing without error - the toggle rate increasing to 500ms should any task
 report an error at any time [this mechanism can be tested by removing the loopback connector
 while the demo is executing, and in so doing deliberately generating an error within the
 'com test' tasks].
* The trace task
 The trace task is a user interactive task that writes execution trace and task state information to UART 5. To view the menu and provided information connect UART 5 (X8) to a terminal
 program (such as Hyperterminal) on your host PC. 9600 baud is used.

When executing correctly the demo application will behave as follows:

* The 'check' function will toggle LED D8 every 3 seconds.
* The trace task will send menu options to a terminal program via UART 5.
* LEDs D1, D2 and D3 are under the control of the standard 'flash' tasks. Each will toggle at a fixed but
 different frequency, with LED D1 being the fastest and LED D3 being the slowest.
* LEDs D9 to D16 are under the control of the 'flash' co-routines. Again each will toggle at a fixed but different frequency.
* LED D5 is under control of the 'ComTest' Tx task. It will toggle each time a character is transmitted.
* LED D6 is under control of the 'ComTest' Rx task. It will toggle each time a character is received.

---

### RTOS Configuration and Usage Details

#### Resources used by the RTOS

The RTOS tick is generated by reload timer 0.
The RTOS yield function uses software interrupt 64 (0x40).

The RTOS yield from ISR functionality utilises the delayed interrupt.

#### Watchdog

The demo application demonstrates three methods of servicing the watchdog, these are:

1. Clearing the watchdog from within the tick interrupt.
2. Clearing the watchdog from within a dedicated watchdog task.
3. Clearing the watchdog from within the idle task.

The settings within Demo/MB91460\_Softune/SRC/watchdog/watchdog.h allow the selection of the method to use.

**NOTE:** These three methods are provided for demonstration purposes only - all three implementations are too simple to provide a secure watchdog mechanism.
A more secure mechanism would require various system checks to be performed prior to the watchdog timer being reset.

#### RTOS port specific configuration

Configuration items specific to this demo are contained in Demo/MB91460\_Softune/Src/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY**
 This sets the interrupt priority used by the RTOS kernel.
 The RTOS kernel should use a low interrupt priority (high numeric value), allowing higher priority interrupts to be unaffected by the
 kernel entering critical sections. Instead of critical sections globally disabling interrupts, they only disable interrupts that
 are below the RTOS kernel interrupt priority.

 This permits very flexible interrupt handling:

	1. At the RTOS kernel priority level interrupt handling 'tasks' can be written and prioritised
	 as per any other task in the system. These are tasks that are woken by an interrupt. The interrupt service routine (ISR) itself should be written to be as short
	 as it possibly can be - it just grabs the data then wakes the high priority handler task. The ISR then returns directly into the
	 woken handler task - so interrupt processing is contiguous in time just as if it were all done in the ISR itself. The benefit of this is that
	 all interrupts remain enabled in the handler task. The Ethernet driver within the Ethernet enabled demos uses a handler task to demonstrate the mechanism.
	2. ISR's running above the RTOS kernel priority are never masked out by the RTOS kernel itself, so their responsiveness is not effected by the RTOS kernel functionality.
	 However, such ISR's cannot use the FreeRTOS API functions. The fast timer interrupt test demonstrates this behaviour.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long (32 bits).

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portYIELD\_FROM\_ISR() can be used to request a context switch from within an ISR. See Demo/MB91460\_Softune/Src/serial/serial.c
for an example.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/MB91460\_Softune/Src/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project.

#### Memory allocation

Source/Portable/MemMang/heap\_3.c is included in the demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial driver

Please note that the example serial driver supplied is intended to demonstrate some of the RTOS kernel features and is not intended to represent an optimal solution.
