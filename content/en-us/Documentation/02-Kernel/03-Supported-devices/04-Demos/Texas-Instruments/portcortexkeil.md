---
title: "Luminary Micro Stellaris/Cortex-M3 Port for the ARM RVDS/Keil development tools"
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

There are currently four FreeRTOS ports for [Luminary Micro](http://www.luminarymicro.com/) Stellaris M3 based embedded microcontrollers - one that
uses the ARM Keil tools, one for [Rowley CrossWorks](http://www.rowley.co.uk/), one using the [IAR tool suite](http://www.iar.com/), and
[one that uses GCC](portcortexgcc).
This page relates only to the ARM Keil based port for which two demos are provided. The demo presented on this page is targeted at the DK-LMS102 development board.
See also the [LM3S811 Keil RVDS demo application](portlm3s811keil).

 The LM3S102 is a low cost, low pin count device. It has
 2KBytes of RAM and 8KBytes of ROM on chip. An ideal candidate to demonstrate the co-routine functionality included from FreeRTOS V4.0.0 onwards.

**Upgrading to FreeRTOS V5.0.3:** FreeRTOS V5.0.3 introduced the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY configuration option to the ARM Cortex-M3 port. See
the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on this feature.

**Upgrading to FreeRTOS V4.8.0:**  Prior to V4.8.0 the FreeRTOS kernel did not make use of the SVCall interrupt. From V4.8.0 onwards it does.
Therefore, to upgrade an older project to the V4.8.0 standard, a small edit to the startup code is required. To do this, simply install
vPortSVCHandler() in the SVCall position within the interrupt vector table (contained in the startup source file). The demo projects included in the
FreeRTOS download have already been updated so these can be used as an example.

---

### IMPORTANT! Notes on using the [Luminary Micro LM3S102](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) port

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

The Keil/RVDS demo application project for the Stellaris LM3S102 port is called FreeRTOS.Uv2 and can be
located in the FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL directory.

---

### The Demo Application

The FreeRTOS source code download includes two demos for this port which include both fully preemptive tasks and co-routines. Demo-1 creates 3 tasks (including the idle task)
and 6 co-routines. Demo-2 creates 2 tasks and 7 co-routines. Due to the ROM and RAM constraints the standard demo tasks are not used.

### Demo application hardware setup

All the DK-LMS102 jumpers can remain in their default positions.

The demo application includes an interrupt driven UART test where a co-routine transmits characters that are then received by a task. For correct operation
of this functionality a loopback connector must be fitted to the SER0 connector of the DK-LMS102 prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

### Functionality

When executing correctly the Demo-1 application will behave as follows:
* LEDs marked LED0 to LED4 are under control of the 'flash' co-routines. Each will flash at a constant frequency, with LED0 being
 the fastest and LED 4 being the slowest.
* LED5 will flash each time a character is transmitted on the serial port.
* LED6 will flash each time a character is received and validated on the serial port (though the loopback connector).
* LED7 is used to indicate an error has been detected and should remain off.
* The LCD will display a rotating message indicating which demo is executing.

The demo includes functionality that checks all the tasks and co-routines are executing as expected. If an error is located in any task or co-routine
LED7 will come on. This functionality can be tested by removing the loopback connector while the demo is executing.

The Demo-2 application has similar functionality but tests different features of the RTOS port. To switch to Demo-2 simply copy the files from the
FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL/Demo2 into the FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL directory.

### Building and executing the demo application

1. Open the FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL/FreeRTOS.Uv2 project from within the uVision IDE.
2. Select "Rebuild all target files" from the "Project" menu. The project should build with no warning or errors.
3. Connect the ARM USB JTAG adapter between your host PC and the target hardware.
4. Select "Download" from the "Flash" menu. After a few seconds the build window should indicate that the device was erased, then programmed and finally verified.

![](/media/2018/cortex_compile.gif)
Confirmation that the hardware has been flashed
5. To debug the application select "Start/Stop Debug Session" from the "Debug" menu, then click "Run" from the same menu.

![](/media/2018/cortex_run.gif)
Running the application in the debugger
6. Alternatively, to just execute the application, the JTAG interface can be removed and the target board reset.

---

### Configuration and Usage Details

### RTOS port specific configuration

Configuration items specific to this port are contained in FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Also note configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

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

The interrupt vector table is contained within FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL/init/startup.s and can be populated as required. In the demo applications
the vector table remains in flash.

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR. This mechanism is demonstrated by the UART ISR defined within
main.c (see the function vUART\_ISR()).

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_LM3S102\_KEIL/FreeRTOSConfig.h to 1 to use pre-emption or 0
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
