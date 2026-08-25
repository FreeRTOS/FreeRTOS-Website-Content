---
title: "Cortex-M3/IAR Port for Luminary Micro Stellaris microcontrollers"
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
| <br />![lm3s316.gif](/media/2018/lm3s316.gif)<br /> |

The port was developed using the [DK-LM3S316](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) development kit.

The [LM3S316](https://www.ti.com/lit/ml/spmu145/spmu145.pdf?ts=1719575549427) is a
low cost, low pin count device. It has
4KBytes of RAM and 16KBytes of ROM on chip. The demo
application code size has been deliberately limited to ensure it builds using the code size limited KickStart version of the IAR tools.

The IAR ARM Cortex-M3 demo relies on a driver library file which is licensed separately from FreeRTOS.org. A full copy of the license applicable to this library is
contained in the EULA.txt file located in the Demo/CORTEX\_LM3S316\_IAR/hw\_include directory within the FreeRTOS download.

There are currently four FreeRTOS ports for [Luminary Micro](http://www.luminarymicro.com/) Stellaris ARM Cortex-M3 based microcontrollers -
 one that uses the [Sourcery G++ (GCC) tools](http://www.codesourcery.com/), one that uses the
 [ARM Keil tools](portcortexkeil), one for [Rowley CrossWorks](http://www.rowley.co.uk/),
 and the port presented on this page which uses the [IAR Embedded Workbench](http://www.iar.com/) tool chain.

**Note:** If this project fails to build using the IAR tools then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

### IMPORTANT! Notes on using the ARM Cortex-M3 IAR port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR workspace for the Luminary Micro port is located in the FreeRTOS/Demo/CORTEX\_LM3S316\_IAR directory and is called RTOSDemo.eww.

---

### The Demo Application

The FreeRTOS source code download includes a preconfigured demo applications for the IAR port. This demonstrates both fully preemptive tasks and co-routines - with 8
co-routines and 5 tasks being created (including the idle task).

### Demo application hardware setup

Most of the DK-LM3S316 jumpers can remain in their default positions. For the ADC to correctly read the light sensor ensure jumper 0 is also in position on
the ADC connector JP2.

The demo application includes an interrupt driven UART test where a co-routine transmits characters that are then received by a task. For correct operation
of this functionality a loopback connector must be fitted to the SER0 connector of the DK-LM3S316 target board (pins 2 and 3
must be connected together on the 9Way connector).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

A J-Link JTAG interface is used to interface the host PC with the target.

### Functionality

See the comments at the top of Demo/CORTEX\_LM3S316\_IAR/main.c for a detailed explanation of the demo functionality.

When executing correctly the demo application will behave as follows:

* The top row of the LCD will display a rotating message - originating from the 'LCD Message' demo task.
* The bottom row of the LCD will display the ADC 0 value, which can be connected to the DK-LM3S316 light sensor as described by the "hardware setup" section above. This
 originates from the 'ADC' demo co-routine.
* LEDs marked LED0 to LED4 are under control of the 'flash' co-routines. Each will flash at a constant frequency, with LED0 being
 the fastest and LED 4 being the slowest.
* LED5 will flash each time a character is transmitted on the serial port.
* LED6 will flash each time a character is received and validated on the serial port (though the loopback connector).
* LED7 is used to indicate an error has been detected and should remain off.

The demo includes functionality that checks all the tasks and co-routines are executing without error. If an error is located in any co-routine or task
LED7 will be turned on. This functionality can be tested by removing the loopback connector while the demo is executing and in so doing deliberately generating
an error.

### Building and executing the demo application

To build the application simply open RTOSDemo.eww from within the Embedded Workbench IDE, then select "Rebuild all" from the "Project" menu.

To download then execute the demo:

1. Connect your host computer to the target board using the J-Link J-TAG interface.
2. Click the "Debug" speed button, or simply press CTRL D.
3. The LM3S31x flash memory will be programmed and the debugger will stop at the beginning of main().

---

### Configuration and Usage Details

### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_LM3S316\_IAR/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.

Attention please!: Remember that ARM Cortex-M3 cores use numerically low priority numbers to represent HIGH
priority interrupts, which can seem counter-intuitive and is easy to forget! If you wish to assign an interrupt a low priority do NOT assign it a
priority of 0 (or other low numeric value) as this can result in the interrupt actually having the highest priority in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

The lowest priority on a ARM Cortex-M3 core is in fact 255 - however different ARM Cortex-M3 vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. Use the supplied examples as a reference.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Interrupt service routines

The interrupt vector table is contained within FreeRTOS/Demo/CORTEX\_LM3S316\_IAR/hw\_include/startup.c and can be populated as required.
In the demo application the vector table remains in flash.

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR. This mechanism is demonstrated by the UART ISR called vUART\_ISR() and
defined within commtest.c.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_LM3S316\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
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
