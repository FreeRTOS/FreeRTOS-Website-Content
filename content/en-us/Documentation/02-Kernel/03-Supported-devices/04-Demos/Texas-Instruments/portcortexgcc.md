---
title: "Cortex-M3/GCC Port for Luminary Micros Stellaris microcontrollers"
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

 There are currently four FreeRTOS ports for [Luminary Micro](http://www.luminarymicro.com/) Stellaris Cortex based embedded microcontrollers - one that uses
 the [Sourcery G++ (GCC) tools](http://www.codesourcery.com/), one for [Rowley CrossWorks](http://www.rowley.co.uk/),
 another for the [IAR tools](http://www.iar.com/), and one that uses the
 [ARM Keil tools](portcortexkeil).
 This page relates only to the GCC based port. It is very similar to the page relating to the ARM Keil port down to the section providing build
 instructions.

 The LM3S102 is a low cost, low pin count device. It has
 2KBytes of RAM and 8KBytes of ROM on chip. An ideal candidate to demonstrate the co-routine functionality included from FreeRTOS V4.0.0.

The Cortex GCC demo relies on a driver library and makefile which is licensed separately from FreeRTOS. The license conditions are included within the comments at the
top of the library header files located in the Demo/CORTEX\_LM3S102\_GCC/hw\_include directory.

As per the Keil port, the GCC port was developed using the DK-LMS102 development board.

**Upgrading to FreeRTOS V5.0.3:** FreeRTOS V5.0.3 introduced the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY configuration option to the ARM Cortex-M3 port. See
the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on this feature.

**Upgrading to FreeRTOS V4.8.0:**  Prior to V4.8.0 the FreeRTOS kernel did not make use of the SVCall interrupt. From V4.8.0 onwards it does.
Therefore, to upgrade an older project to the V4.8.0 standard, a small edit to the startup code is required. To do this, simply install
vPortSVCHandler() in the SVCall position within the interrupt vector table (contained in the startup source file). The demo projects included in the
FreeRTOS download have already been updated so these can be used as an example.

|  |  |
| --- | --- |
|  |  |

---

### IMPORTANT! Notes on using the ARM Cortex-M3 GCC port

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

The GCC makefile for the Luminary Micro port is located in the FreeRTOS/Demo/CORTEX\_LM3S102\_GCC directory.

---

### The Demo Application

The FreeRTOS source code download includes two demos for this port which include both fully preemptive tasks and co-routines. Demo-1 creates 3 tasks (including the idle task)
and 6 co-routines. Demo-2 creates 2 tasks and 7 co-routines. Due to the ROM and RAM constraints the standard demo tasks are not used.

### Demo application hardware setup

All the DK-LMS102 jumpers can remain in their default positions.

The demo application includes an interrupt driven UART test where a co-routine transmits characters that are then received by a task. For correct operation
of this functionality a loopback connector must be fitted to the SER0 connector of the DK-LMS102 prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

The USB enable jumper must be connected in order to use the direct USB debug facility.

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
FreeRTOS/Demo/CORTEX\_LM3S102\_GCC/Demo2 into the FreeRTOS/Demo/CORTEX\_LM3S102\_GCC directory.

### Building and executing the demo application

These instructions assume the GCC compiler and related tools (make.exe, etc.) have been previously installed and their location included in the PATH
environment variable.

To build the application.

1. Using a command prompt, navigate to the FreeRTOS/Demo/CORTEX\_LM3S102\_GCC directory.
2. Type "make" to build the application using the existing makefile and linker script. The application
 should build with no warnings or errors as below:

```c

$ make
  CC    init/startup.c
  CC    main.c
  CC    hw_include/pdc.c
  CC    ../../Source/list.c
  CC    ../../Source/queue.c
  CC    ../../Source/tasks.c
  CC    ../../Source/portable/GCC/ARM_CM3/port.c
  CC    ../../Source/portable/MemMang/heap_1.c
  CC    ParTest/ParTest.c
  CC    ../Common/Minimal/crflash.c
  CC    ../../Source/croutine.c
  LD    gcc/RTOSDemo.axf
```
The build files are placed into a subdirectory called GCC.

The DK-LMS102 evaluation board contains a USB interface that allows the application to be downloaded to the target flash directly. The Sourcery G++ manual
provides further details. To debug the application:
1. In the command prompt navigate to the FreeRTOS/Demo/CORTEX\_LM3S102\_GCC/GCC directory.
2. Start the debugger by typing "arm-stellaris-eabi-gdb RTOSDemo.axf"
3. Connect to the target board by typing "(gdb) target extended-remote | armswd -s 2 -f lmi.dll stdio" (where "(gdb)" is the command prompt).
4. Download the RTOSDemo.axf file by simply typing "(gdb) load". Output similar to that shown below should be observed.
```c

Loading section .text, size 0x1fd4 lma 0x0
Loading section .data, size 0x10 lma 0x1fd4
Start address 0x61, load size 8164
Transfer rate: xxxxx bits/sec, xxx bytes/write.
```
5. After downloading the image, type "run" to start the application. GDB asks you if you
want to start from the beginning, enter "y" to continue. You will then be stopped at
ResetISR, which is the entry point for the application.
```c

The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program:c:FreeRTOS/Demo/CORTEX_LM3S102_GCC/gcc/RTOSDemo.axf
Reloaded SP/PC from 0, reset xPSR and LR
Stopped at entry.
Program received SIGTRAP, Trace/breakpoint trap.
0x00000060 in ResetISR()
```
6. The demo can now be executed by typing "continue".

More information on using GDB can be found in the [GDB user manual](http://www.gnu.org/software/gdb/documentation/).

---

### Configuration and Usage Details

### RTOS port specific configuration

Configuration items specific to this port are contained in FreeRTOS/Demo/CORTEX\_LM3S102\_GCC/FreeRTOSConfig.h. The
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

The interrupt vector table is contained within FreeRTOS/Demo/CORTEX\_LM3S102\_GCC/init/startup.c and can be populated as required. In the demo applications
the vector table remains in flash.

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR. This mechanism is demonstrated by the UART ISR defined within
main.c (see the function vUART\_ISR()).

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_LM3S102\_GCC/FreeRTOSConfig.h to 1 to use pre-emption or 0
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
