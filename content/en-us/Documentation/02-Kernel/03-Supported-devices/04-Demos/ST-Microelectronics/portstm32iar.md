---
title: "STMicroelectronics STM32F103 ARM Cortex-M3 Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![](/media/2018/stm32.jpg)<br /> |

This page describes the FreeRTOS demo application for the [STMicroelectronics STM32 ARM Cortex-M3 microcontroller](http://www.st.com/internet/mcu/subclass/1169.jsp). The demo uses the IAR Embedded Workbench
development tools for ARM, and is preconfigured to run on the STM32 evaluation board from ST ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).
The evaluation board is fitted with an STM32F103VB microcontroller that
contains 128KBytes of on board flash and 20KBytes of on board RAM. The STM32F103VB also includes both USB and CANbus peripherals.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the STM32 ARM Cortex-M3 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download includes the source code for all the FreeRTOS ports and therefore contains many more files than are required for this demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR workspace file for the STM32F103 demo is called RTOSDemo.eww and is located in the FreeRTOS/Demo/CORTEX\_STM32F103\_IAR directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes an interrupt driven UART test where one task transmits characters that are then received by another task. For correct
operation of this functionality a loopback connector must be fitted to the UART00 connector of the STM32 evaluation board (pins 2 and 3 must be
connected together on the 9Way connector).

The demo application uses the LEDs and display built onto the prototyping board so no other hardware setup is required.

A J-Link USB JTAG interface is used to interface the host PC with the target.

#### Building and running the demo application

1. Open the FreeRTOS/Demo/CORTEX\_STM32F103\_IAR/RTOSDemo.eww project from within the Embedded Workbench IDE.
2. Select 'Rebuild All' from the IDE 'Project' menu. The project should build with no errors or warnings.
3. Select 'Debug' from the IDE 'Project' menu. The microcontroller flash memory will be programmed with the newly built binary and the debugger will break on
 the entry to main().

The project includes a bitmap that is built into the binary. This increases the binary size and at some optimisation levels will take the build size above the
32K limit of the Embedded Workbench Kickstart edition. If this becomes an issue then the code size can be reduced by excluding the bitmap from the
build (by removing the pcBitmap array from lcd\_message.h, and commenting out the call to LCD\_DrawMonoPict() within the same file).

#### Functionality

The demo application creates 24 persistent tasks, and periodically dynamically creates and destroys another 4. These tasks consist
predominantly of the standard demo application tasks (see the  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details
of the individual tasks).

The following tasks and tests are created in addition to the standard demo tasks:

* High priority interrupt test
 A high frequency periodic interrupt is generated
 using a free running timer to demonstrate the use of the
 'configKERNEL\_INTERRUPT\_PRIORITY' configuration constant. The interrupt
 service routine measures the number of processor clocks that occur between
 each interrupt - and in so doing measures the jitter in the interrupt timing.
 The maximum measured jitter time is latched in the ulMaxJitter variable, and
 displayed on the LCD display by the 'Check' task as described below. The
 fast interrupt is configured and handled in the timertest.c source file. This
 demonstrates how the RTOS kernel can be configured so as to have no impact on higher
 priority interrupt processing.

 The ARM Cortex-M3 core has the ability to hasten the entry into an interrupt service routine
 (and therefore reduce latency) by up to 8 cycles should a high priority interrupt occur
 while a lower priority interrupt is already being serviced. The measured jitter time should
 therefore be no more than 8 clock cycles.
* LCD task
 The LCD task is a 'gatekeeper' task. It is the only task that
 is permitted to access the display directly. Other tasks wishing to write a
 message to the LCD send the message on a queue to the LCD task instead of
 accessing the LCD themselves. The LCD task just blocks on the queue waiting
 for messages - waking and displaying the messages as they arrive.
* Check task
 This only executes every five seconds but has the highest
 priority so is guaranteed to get processor time. Its main function is to
 check that all the standard demo tasks are still operational. Should any
 unexpected behaviour within a demo task be discovered the 'check' task will
 write an error to the LCD (via the LCD task) (this mechanism can be tested by
 removing the loopback connector on UART0, and in so doing deliberately generating
 an error). If all the demo tasks are
 executing with their expected behaviour then the check task writes PASS
 along with the max jitter time to the LCD (again via the LCD task), as
 described above.

When executing correctly the demo application will behave as follows:

* LEDs LED1, LED2 and LED3 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED1 being
 the fastest and LED3 being the slowest.
* LED4 is under controlled by the standard ComTest Tx task. LED4 will toggle each time the ComTest Tx task transmits a
 character over the RS232 port.
* The 'check' task will write "PASS" and the jitter time in nanoseconds to the display every 5 seconds.

---

### RTOS Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_STM32F103\_IAR/FreeRTOSConfig.h. The
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
functions that expect priorities to be specified in different ways. For example, on the STM32 the lowest priority you can specify in an ST driver library call
is in fact 15 - and the highest priority you can specify is 0. This is defined by the constant configLIBRARY\_KERNEL\_INTERRUPT\_PRIORITY in
FreeRTOSConfig.h.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_STM32F103\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
