---
title: "ST STM32 Primer ARM Cortex-M3 Demo"
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
| <br /><br />![](/media/2018/STM32_Primer.jpg)<br /> |

This page describes the FreeRTOS demo application for the [STM32 Primer](http://www.stm32circle.com/) - a novel
evaluation platform for the [STMicroelectronics STM32 ARM Cortex-M3 microcontroller](http://www.st.com/internet/mcu/subclass/1169.jsp). 
The demo uses the GCC compiler with the [Raisonance Ride V7](http://www.raisonance.com/) IDE.

The demo utilises drivers and other source files from CircleOS (which, unlike FreeRTOS.org, is not a real time kernel). These files are licensed separately from
FreeRTOS.org. Users must familiarise themselves with the [CircleOS](http://www.stm32circle.com/circleos_doc/index.html) license. Please note that
the FreeRTOS demo is not itself a CircleOS application and will overwrite CircleOS on the STM32 Primer. The batch files 
located in the [Program Files]RaisonanceRideLibARMCircleOS directory of your Raisonance Ride distribution can be used to restore CircleOS to the STM32 Primer hardware.

**Using RIDE version 7:** FreeRTOS V5.1.1 will not build with the latest versions of the RIDE libraries. The head revision in the FreeRTOS SVN
repository has already been fixed - the necessary changes will be included in the next release.

**Upgrading to FreeRTOS V5.0.3:** FreeRTOS V5.0.3 introduced the configMAX\_SYSCALL\_INTERRUPT\_PRIORITY configuration option to the ARM Cortex-M3 port. See
the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on this feature.

**Upgrading to FreeRTOS V4.8.0:**  Prior to V4.8.0 the FreeRTOS kernel did not make use of the SVCall interrupt. From V4.8.0 onwards it does. 
Therefore, to upgrade an older project to the V4.8.0 standard, a small edit to the startup code is required. To do this, simply install
vPortSVCHandler() in the SVCall position within the interrupt vector table (contained in the startup source file). The demo projects included in the 
FreeRTOS download have already been updated so these can be used as an example.

---

#### *IMPORTANT! Notes on using the STM32 Primer ARM Cortex-M3 Demo*

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

The Ride workspace file for the STM32F103 Primer Ride demo is called RTOSDemo.rprj and is located in the FreeRTOS/Demo/CORTEX\_STM32F103\_Primer\_GCC 
directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application uses the LED and display built onto the evaluation board so no specific hardware setup is required. 

A USB interface is used to connect directly between the STM32 Primer and the host PC.

#### Building and running the demo application

Connect the USB port marked "Debug" on the STM32 Primer to the host PC.

1. Open the FreeRTOS/Demo/CORTEX\_STM32F103\_Primer\_GCC/RTOSDemo.rprj project from within the Ride IDE.
2. Select 'Make Project' from the IDE 'Project' menu. The project should build with no errors or warnings.
3. Select 'Start' from the IDE 'Debug' menu. The microcontroller flash memory will be programmed with the newly built binary and the debugger will break on
 the entry to main().

The project includes a bitmap that is built into the binary. This increases the binary size and at some optimisation levels will make the resultant binary too
large for the microcontroller flash. If this becomes an issue then the code size can be reduced by excluding the bitmap from the 
build by simply setting the definition mainINCLUDE\_BITMAP within main.c to 0.

#### Functionality

The demo application creates 22 real time tasks. These tasks consist 
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
 for messages - waking when messages arrive.

 Two types of message are received by the LCD task. The first type contain strings for
 display on the LCD. The second type contains an instruction to update the LCD in accordance
 with the current MEMS input as described [below](#demo-application-hardware-setup) (the MEMS functionality is from the CircleOS demo).
* Check task
 This only executes every five seconds but has the highest
 priority so is guaranteed to get processor time. Its main function is to
 check that all the standard demo tasks are still operational. Should any
 unexpected behaviour within a demo task be discovered the 'check' task will
 write an error to the LCD (via the LCD task). If all the demo tasks are
 executing with their expected behaviour then the check task writes PASS
 along with the max jitter time to the LCD (again via the LCD task), as
 described above.
* Tick hook
 This is a basic Tick Hook that periodically sends a message to the LCD task to request that the MEMS input be updated.
* Flash task
 This is a very basic task that does nothing but wake every second, then flash an LED. It is used for timing validation only.

When executing correctly the demo application will behave as follows:

* The green LED is under control of the 'flash' task and will toggle every second.
* The MEMS input is used to control the position of a little ball on the LCD. The ball can be moved about the LCD by tilting the STM32 Primer.
 45% is set as the neutral position. This functionality is taken from the CircleOS demo, but in this case executed from within its own autonomous task.
* The 'check' task will write "PASS" and the jitter time in nanoseconds to the display every 5 seconds.

---

### RTOS Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_STM32F103\_Primer\_GCC/FreeRTOSConfig.h. The 
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
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR. The interrupt driven UART demo in the STM32/IAR demo can be
used as an example. See the file FreeRTOS/Demo/CORTEX\_STM32F103\_IAR/serial/serial.c for a full example, but note that this example is intended to
demonstrate the mechanisms required only and should not be used as an example of an optimal UART driver.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_STM32F103\_Primer\_GCC/FreeRTOSConfig.h to 1 to use pre-emption or 0 
to use co-operative. Note that demo tasks that measure their own timing characteristics can report errors when executed using the co-operative RTOS scheduler.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM Cortex-M3 demo application project to provide the memory 
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for 
full information.
