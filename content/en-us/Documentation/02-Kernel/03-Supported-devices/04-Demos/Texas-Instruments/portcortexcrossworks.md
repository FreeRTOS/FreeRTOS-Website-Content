---
title: "Cortex-M3/CrossStudio Port for Luminary Micros Stellaris microcontrollers"
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
| <br />![lm3s102.gif](/media/2018/lm3s102.gif)<br /> |

There are currently four FreeRTOS ports for [Luminary Micro](http://www.luminarymicro.com/) Stellaris Cortex based embedded microcontrollers - one that uses the [Sourcery G++ (GCC) tools](http://www.codesourcery.com/),
one that uses the [ARM Keil tools](portcortexkeil), another for the [IAR tools](http://www.iar.com/), and the port presented on this page which uses
[Rowley CrossWorks](http://www.rowley.co.uk/).

Three demo applications are provided for the CrossWorks port, two targeted for the DK-LMS102 development board from Luminary Micro, and one targeted at
the low cost [CrossFire LM3S102 board](http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm) from Rowley Associates. The CrossFire LM3S102 connects
directly to the host computer via the built in USB connector and does not require the use of a separate JTAG interface.

[![](/media/2018/lm3s102_crossfire.gif)](http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm)
CrossFire LM3S102 development board

Stellaris is a new range of microcontrollers - the first to be commercially available with a Cortex-M3 core. The LM3S102 is a low cost, low pin count device. It has
2KBytes of RAM and 8KBytes of ROM on chip. An ideal candidate to demonstrate the new co-routine functionality included with FreeRTOS V4.0.0.

The CrossWorks Cortex-M3 demos rely on a driver library and makefile which is licensed separately from FreeRTOS. The license conditions are included within the comments at the
top of the library header files located in the Demo/CORTEX\_LM3S102\_ROWLEY/hw\_include directory. A full copy of the license is available in the same directory.

**Upgrading to FreeRTOS V5.0.3:** FreeRTOS V5.0.3 introduced the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY configuration option to the Cortex-M3 port. See
the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on this feature.

**Upgrading to FreeRTOS V4.8.0:**  Prior to V4.8.0 the FreeRTOS kernel did not make use of the SVCall interrupt. From V4.8.0 onwards it does.
Therefore, to upgrade an older project to the V4.8.0 standard, a small edit to the startup code is required. To do this, simply install
vPortSVCHandler() in the SVCall position within the interrupt vector table (contained in the startup source file). The demo projects included in the
FreeRTOS download have already been updated so these can be used as an example.

---

### IMPORTANT! Notes on using the ARM Cortex-M3 CrossWorks port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Applications](#the-demo-applications)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The CrossWorks solution (workspace) for the Luminary Micro port is located in the FreeRTOS/Demo/CORTEX\_LM3S102\_ROWLEY directory.

---

### The Demo Applications

The FreeRTOS source code download includes three demo applications for the port. These include both fully preemptive tasks and co-routines. Demo-1 creates 3 tasks (including the idle task)
and 6 co-routines. Demo-2 creates 2 tasks and 7 co-routines. Both of these demos are configured to execute on the DK-LMS102 development board.
Demo-3 creates 4 co-routines and the idle task, and is configured to execute on the CrossFire LM3S102 board.

Due to the ROM and RAM constraints the standard demo tasks are not used.

---

### Demo application hardware setup, Demo1 and Demo2

The LINK\_RST jumper must be in position on the DK-LMS102 target board, all other jumpers can remain in their default positions.

The demo application includes an interrupt driven UART test where a co-routine transmits characters that are then received by a task. For correct operation
of this functionality a loopback connector must be fitted to the SER0 connector of the DK-LMS102 prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

A [CrossConnect JTAG interface](http://www.rowley.co.uk/arm/CrossConnect.htm) is used to interface the host PC with the target board.

### Functionality, Demo1 and Demo2

When executing correctly the Demo-1 application will behave as follows:
* LEDs marked LED0 to LED4 are under control of the 'flash' co-routines. Each will flash at a constant frequency, with LED0 being
 the fastest and LED 4 being the slowest.
* LED5 will flash each time a character is transmitted on the serial port.
* LED6 will flash each time a character is received and validated on the serial port (though the loopback connector).
* LED7 is used to indicate an error has been detected and should remain off.
* The LCD will display a rotating message indicating which demo is executing.

The demo includes functionality that checks all the tasks and co-routines are executing as expected. If an error is located in any task or co-routine
LED7 will come on. This functionality can be tested by removing the loopback connector while the demo is executing.

The Demo-2 application has similar functionality but tests different features of the RTOS port.

---

### Demo application hardware setup, Demo3

The CrossFire LM3S102 board does not require any special setup. It connects directly to the host PC via the built in USB connection and does not require
an external JTAG interface.

### Functionality, Demo3

When executing correctly the Demo-3 application will flash the three coloured LEDs in a rotation pattern, the speed of which is set by the potentiometer.

---

### Building and executing the demo applications

The CrossWorks solution FreeRTOS/Demo/CORTEX\_LM3S102\_Rowley/RTOSDemo.hzp contains all three demo projects and two configurations. The 'Flash Debug' configuration
must be selected for debug sessions. The 'Flash Release' configuration must be selected for running the demo stand alone (not through the debugger).

![](/media/2018/selectconfig.gif)
Selecting the build configuration

To build the application.

1. Select the project you wish build from the drop down list in the IDE![](/media/2018/selectproject.gif)
Selecting the project to build
2. Select "Rebuild Demox" from the "Build" menu. The project should build with no errors or warnings.

To download then execute the demo:
1. Connect your host computer to the target board either directly if using the CrossFire LM3S102, or using the CrossConnect JTAG interface if using the Luminary Micro
 development board.
2. Select the appropriate connection from the "Target" menu for your setup.![](/media/2018/connectjtag.gif)
Selecting target
3. Select "Start Debugging" from the "Debug" menu. The LM3S10x flash memory will be programmed and the debugger will stop at the beginning of main().

---

### Configuration and Usage Details

### RTOS port specific configuration

Configuration items specific to these demos are contained in the respective FreeRTOS/Demo/CORTEX\_LM3S102\_ROWLEY/Demox/FreeRTOSConfig.h files. The
constants defined in these file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Also note configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.

Attention please!: Remember that Cortex-M3 cores use numerically low priority numbers to represent HIGH
priority interrupts, which can seem counter-intuitive and is easy to forget! If you wish to assign an interrupt a low priority do NOT assign it a
priority of 0 (or other low numeric value) as this can result in the interrupt actually having the highest priority in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

The lowest priority on a Cortex-M3 core is in fact 255 - however different Cortex-M3 vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. Use the supplied examples as a reference.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Interrupt service routines

The interrupt vector table is contained within FreeRTOS/Demo/CORTEX\_LM3S102\_ROWLEY/demox/vectors.s and can be populated as required. In the demo applications
the vector table remains in flash.

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR. This mechanism is demonstrated by the UART ISR defined within
main.c (see the function vUART\_ISR()). Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_LM3S102\_ROWLEY/Demox/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The demo application will only execute correctly with configUSE\_PREEMPTION set to 0 if configIDLE\_SHOULD\_YIELD is set to 1.

### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimized solution.
