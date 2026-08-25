---
title: "AT91SAM3U ARM Cortex-M3 FreeRTOS demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### Using the IAR compiler

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/SAM3U-EK.jpg)

The demo application presented on this page is pre-configured to execute on the official SAM3U-EK evaluation kit from Atmel.
The demo uses the FreeRTOS IAR ARM Cortex-M3 port and can be compiled and debugged directly from the [IAR Embedded Workbench](http://www.iar.com/ewarm) for ARM.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

The FreeRTOS ARM Cortex-M3 port includes a full interrupt nesting model. Interrupt priorities must be set in accordance with the
[instructions on the Customisation page](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) for correct operation.

Atmel also provide a comprehensive demo project
for their [SAM3S-EK evaluation kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAM3S-EK2)
that uses the FreeRTOS port. This includes GUI, QTouch, FAT file system and USB functionality.

---

#### _IMPORTANT! Notes on using the Atmel ARM Cortex-M3 Demo_

_Please read all the following points before using this RTOS port._

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The IAR workspace file for the SAM3 FreeRTOS demo is called RTOSDemo.eww and is located in the FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR directory.

The FreeRTOS zip file download contains the files for all the ports and demo application projects. It therefore contains many more
files than used by this demo. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
of the downloaded files and information on creating a new project.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes an interrupt driven UART test where one task transmits characters that are then received by another task.
For correct operation of this functionality a loopback connector must be fitted to the UART1 9 way connector on the evaluation board (pins 2 and 3 must be connected together
on the 9 way connector - normally a paper clip is sufficient for this purpose).

The demo application uses the LEDs and LCD built onto the prototyping board so no other hardware setup is required.

#### Building and executing the demo application

1. Open the FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/RTOSDemo.eww project from within the
   Embedded Workbench IDE.

2. Select 'Rebuild All' from the IDE 'Project' menu. The project should build with no errors or warnings.

3. Connect the host machine (the computer running the IAR IDE) to the target using a J-Link JTAG interface.

4. Select 'Debug' from the IDE 'Project' menu. The microcontroller flash memory will be programmed with the demo application, and the debugger
   will break at the start of the main() function.

#### Functionality

The demo application creates 33 tasks prior to starting the RTOS scheduler. These tasks consist predominantly of the standard
demo application tasks (see the [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).
Their only purpose is to test the RTOS kernel port and provide a demonstration of how to use the various API functions.

The following tasks and tests are created in addition to the standard demo tasks:

- LCD task

  The LCD task is a 'gatekeeper' task. It is the only task that
  is permitted to access the LCD directly. Other tasks or interrupts wishing to write a
  message to the LCD send the message on a queue to the LCD task instead of
  accessing the LCD themselves. The LCD task just blocks on the queue waiting
  for messages - waking and displaying the messages as they arrive.

- Check function - called from the [tick hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)

  This only executes every five seconds. Its main function is to
  check that all the standard demo tasks are still operational. Should any
  unexpected behaviour within a demo task be discovered the 'check' function will
  write an error to the LCD (via the LCD task). If all the demo tasks are
  executing with their expected behaviour then the check task writes PASS
  to the LCD (again via the LCD task), as
  described above. This mechanism can be tested by removing the loopback connector
  from UART1, and in so doing deliberately generating an error in the COMTest tasks.

  The check function executes within the context of an interrupt service routine so is a good
  example of how using a gatekeeper task to control the LCD permits even interrupts to output
  LCD messages.

When executing correctly the demo application will behave as follows:

- The 'check' function will write "PASS" to the display every 5 seconds.

- LEDs D2, D3 and D4 are under the control of the simple 'flash' tasks. Each LED will toggle at a different but fixed frequency.

---

### RTOS Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular -

- **configTICK_RATE_HZ**

  This sets the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
  testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

- **configKERNEL_INTERRUPT_PRIORITY and configMAX_SYSCALL_INTERRUPT_PRIORITY**

  See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.

Attention please!: Remember that ARM Cortex-M3 cores use numerically low priority numbers to represent HIGH
priority interrupts, which can seem counter-intuitive and is easy to forget! If you wish to assign an interrupt a low priority do NOT assign it a
priority of 0 (or other low numeric value) as this can result in the interrupt actually having the highest priority in the system - and therefore potentially make your system crash if this
priority is above configMAX_SYSCALL_INTERRUPT_PRIORITY.

The lowest priority on a ARM Cortex-M3 core is in fact 255 - however different ARM Cortex-M3 vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. Use the supplied examples as a reference.

Each port #defines 'BaseType_t' to equal the most efficient data type for that processor. This port defines
BaseType_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

In the demo application the vector table remains in flash.

Unlike most ports, interrupt service routines that cause a context switch have no special requirements and can be written as per the compiler documentation.
The macro portEND_SWITCHING_ISR() can be used to request a context switch from within an ISR. An example ISR called vSerialISR() is provided in
FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/serial/serial.c, this should be used as a reference example.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap_2.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the real time RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
