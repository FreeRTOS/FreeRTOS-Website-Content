---
title: "Philips LPC2129 (ARM7) RTOS Port for the Keil/RVDS Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![mcb2100.gif](/media/2018/mcb2100.gif)<br /> |

***Please note:*** From FreeRTOS V5.1.0 the demo presented on this page has switched from using the old (and discontinued) Keil DKARM compiler to
instead use the latest Keil/RVDS/ARM compiler.

The port was developed on an [MCB2100 development/prototyping board](http://www.keil.com/mcb2100)
([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board)
using a ULINK USB JTAG adapter. The Keil simulator also proved very useful. A complete development kit can be obtained
from  [Hitex Development Tools](http://www.hitex.co.uk/).

The MCB2100 is a fully featured and comprehensive prototyping board that allows easy access to the LPC2129 peripherals and
includes 8 built in LEDs which are utilised by the FreeRTOS demo application.

The development tools include a compiler, assembler and linker tool chain along with an IDE and excellent device specific
simulator. The simulator includes a 'logic analyzer' feature that can be used to monitor the microcontroller IO - providing
the same visual feedback in the simulated environment that the LEDs do on the real target hardware. Unfortunately the evaluation
version of the tools are limited to a combined ROM and RAM image size of 16KBytes - which is too restrictive to run this demo (because
the FreeRTOS heap memory is included in the 16KBytes, even if it is not being used).

---

#### *IMPORTANT! Notes on using the Keil/ARM/RVDS LPC2129 RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than required to run this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The uVision project file for this demo is called RTOSDemo.Uv2 and can be located in the Demo/ARM7\_LPC2129\_Keil\_RVDS directory.
The project contains two configurations, one that uses the ARM instruction set and one that uses the THUMB instruction set.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the Keil LPC2000 RTOS port.

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the P1 serial port connector of COM 1 - a paper clip is usually sufficient for this purpose).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

#### Functionality

The demo application creates 25 tasks. When executing correctly the demo application will behave as follows:
* LEDs P1.16, P1.17 and P1.18 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED P1.16 being
 the slowest and LED P1.18 being the fastest (see the logic analyzer screen capture below).
* LED P1.19 will flash each time a character is transmitted on the serial port.
* LED P1.20 will flash each time a character is received on the serial port.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 LED P1.23 is under control of the 'Check' task. Every three seconds the 'Check' task examines all the tasks in the
 system to ensure they are executing without error. It then toggles LED P1.23. If LED P1.23 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error. This mechanism can be checked by removing the loopback connector from the serial port
 and in doing so deliberately generating an error.

See the  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks.

#### Building the demo application

1. Open the Demo/ARM7\_LPC2129\_Keil\_RVDS project file from within the Keil uVision3 IDE
2. Select either the ARM or THUMB configuration as depicted below:

![](/media/2018/Keil-uVision-RTOS-Demo-Select-Configuration.jpg)

Selecting either the ARM or THUMB configuration

4. Select 'Built Target' from the IDE 'Project' Menu.

The application should build with no errors or warnings.

#### Running the demo application

The demo application can be executed in the simulator or on the target hardware.

To switch between the simulator and JTAG debugger:

1. Right click on the FreeRTOS\_ARM or FreeRTOS\_THUMB target within the 'Project Workspace' pane - depicted below.

![](/media/2018/keildebug1.gif)

Right click on the target within the 'Project Workspace' pane

3. From the resultant pop up menu select 'Options for Target FreeRTOS'.
4. A pop up window will appear. Select the 'Debug' tab.
5. Use the radio buttons to switch between the simulator and JTAG debugger - depicted below.

![](/media/2018/keildebug2.gif)

Switching between the simulator and ULINK JTAG debugger

#### Using the simulator and logic analyzer

The microcontroller IO ports can be monitored using the simulators 'logic analyzer' feature. Below
is a screen capture of the logic analyzer being used to monitor certain output pins
while the demo application is being simulated.

![](/media/2018/logicanalyzer.gif)

Monitoring the port pins in the logic analyzer

The red green and blue lines show pins P1.16, P1.17 and P1.18 respectively under control of the 'Flash' tasks. The black
line shows pin P1.19 which is toggled each time a character is transmitted. You would need to zoom much closer in to see the
line being toggled for each individual transmitted character.

When being simulated the 'Check' task will find an error in the 'ComTest' tasks. This is because the 'ComTest' tasks require
a loopback connector as described previously.

#### Programming the flash

The demo application can be programmed into the microcontroller flash from within the Keil IDE using the 'Flash' menu item.
The prototyping board must be reset to start the program executing.
The flash must be programmed before the JTAG debugger can be used.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/ARM7\_LPC2129\_Keil\_RVDS/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

A context switch might be required from within an interrupt service routine if the interrupt causes a task to unblock (through a queue or semaphore event),
and the unblocked task has a priority higher than the interrupted task.

An interrupt service routine that cannot cause a context switch has no special requirements and can be written as per the
normal RVDS syntax.
Interrupt service routines that can cause a context switch require an assembly file wrapper, as demonstrated below.

```c

    ;To define an interrupt service routine first we need an assembly file wrapper.
 ;The wrapper is installed in the interrupt controller as the interrupt entry
 ;point.

    ;portmacro.inc must be included within the assembly file as this defines
 ;the portSAVE\_CONTEXT and portRESTORE\_CONTEXT macros.
    INCLUDE portmacro.inc

    ;Here the C portion of the handler is imported so it can be called from this
 ;assembly file. The asm wrapper is exported so it can be installed in the
 ;interrupt controller.
    IMPORT vUART_ISRHandler
    EXPORT vUART_ISREntry

    ;Interrupt entry must always be in ARM mode.
    ARM
    AREA    |.text|, CODE, READONLY
    PRESERVE8

;Define the interrupt entry point.
vUART_ISREntry

    ;portSAVE\_CONTEXT must be the first thing called in the wrapper.
    portSAVE_CONTEXT

    ;The rest of the interrupt functionality can be implemented in a standard C
 ;function. Call the function now.
    LDR R0, =vUART_ISRHandler
    MOV LR, PC
    BX R0

    ;Finish off by restoring the context of the task that has been chosen to
 ;run next - which might be a different task to that which was originally
 ;interrupted.
    portRESTORE_CONTEXT

    END
```

See the file Demo/ARM7\_LPC2129\_Keil\_RVDS/serial/serialISR.s within the demo application for a full example.

The assembly file wrapper calls a C function (in the example above the C function is called vUART\_ISRHandler()) in which the main
interrupt functionality can be implemented. The C function has no special requirements and does not need any special function
qualifiers. See the function vUART\_ISRHandler() within Demo/ARM7\_LPC2129\_Keil\_RVDS/serial/serial.c for a full example.
vUART\_ISRHandler() also demonstrates the portEXIT\_SWITCHING\_ISR() macro, which is used to ensure the correct task is selected to
run once the interrupt exits.

#### To use a part other than an LPC2129

The LPC2129 uses a standard ARM7 core with processor specific peripherals. The core real time kernel components should be
portable across all ARM7 devices - but the peripheral setup and memory requirements will require consideration.
Items to consider:
* prvSetupTimerInterrupt() in Source/portable/Keil/ARM7/port.c configures the LPC2129 timer 0 to generate the RTOS tick.
* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/ARM7\_LPC2129\_Keil\_RVDS/main.c.
* The interrupt service routine setup and management assume the existence of the vectored interrupt controller.
* The serial port drivers.
* Register location definitions are provided the file lpc21xx.h which is included at the top of Demo/ARM7\_LPC2129\_Keil\_RVDS/FreeRTOSConfig.h.
* Startup code, memory map and vector table setup is contained within Demo/ARM7\_LPC2129\_Keil\_RVDS/Startup.s.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/ARM7\_LPC2129\_Keil\_RVDS/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project file - as described in the [Source Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section.

#### Execution Context

The RTOS scheduler executes in supervisor mode, tasks execute in system mode.
NOTE! :
 The processor MUST be in supervisor mode when the RTOS scheduler is started (vTaskStartScheduler is
 called). The demo applications included in the FreeRTOS download switch
 to supervisor mode prior to main being called. If you are not using one of
 these demo application projects then ensure Supervisor mode is entered before calling vTaskStartScheduler().

Interrupt service routines always run in ARM mode.

Demo/ARM7\_LPC2129\_Keil\_RVDS/Startup.s configures stacks for system/user, IRQ and SWI modes only.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM7 demo application makefile to provide the memory allocation required
by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.
