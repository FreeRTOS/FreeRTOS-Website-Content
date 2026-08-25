---
title: "ST Microelectronics STR71x Port for the IAR ARM Development Tools"
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
| <br />![](/media/2018/strboard.jpg)KickStart board with LEDs and loopback connector<br /> |

The ST ARM7 port was developed on the prototyping board included in the
[STR712-SK/IAR KickStart development kit](http://www.st.com/internet/evalboard/product/152464.jsp)
([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

The STR712F is a peripheral rich (including CANBus), low pin count ARM7TDMI based flash embedded microcontroller.
The evaluation kit came with a non time limited evaluation version of the [IAR Embedded Workbench development
tools for ARM](http://www.iar.com/ewarm) (32KB limited), a J-Link USB JTAG debugger interface and a USB cable. The development board can be powered either through the USB JTAG connector
or using an external power supply.

The development tools include a compiler, assembler and linker tool chain along with an IDE and a limited
functionality simulator.

The processor peripheral library provided by ST was used to facilitate development.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the ST ARM7 RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

A THUMB mode sample project is included for the STR71x IAR ARM7 port. The workspace *rtosdemo.eww* can be
found in the Demo/ARM7\_STR71x\_IAR directory and should be opened from within the Embedded Workbench IDE.

The Demo/ARM7\_STR71x\_IAR/library directory contains the components of the ST peripheral library that are used by the
demo application.

The Demo/ARM7\_STR71x\_IAR/serial directory contains a sample
interrupt driven RS232 serial port driver.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the STR71x RTOS port.

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the serial port connector labelled RS232\_1). The demo application utilises UART 0. The jumpers on the KickStart development board should
remain in their default positions to ensure UART 0 is connected to the RS232\_1 connector.

The demo application utilises the LED built onto the prototyping board. This single LED is enough to check that
the demo is functioning correctly (see the description of the 'Check' task below), but for best effect an extra four LEDs are
required. These should be connected to the header pins marked T1\_OCMPA, T1\_OCMPB, T1\_ICAPB and T1\_ICAPA.
These pins are set as GPIO outputs when the application is executed.

#### The IAR workspace

![](/media/2018/str7proj.gif)
The demo application workspace

The IDE workspace contains 4 folders:

1. **Demo Source**

 Contains the source files for the demo application.
2. **Library Source**

 Contains the components of the ST peripheral library that are utilised by the RTOS kernel and the demo application.
3. **RTOS Source**

 Contains the source files for the FreeRTOS real time kernel.
4. **System Files**

 Contains the startup code, linker script and interrupt vector table definition.

#### Building the demo application

Two project configurations are provided. "Debug" contains minimal optimisation and can be used with the J-Link JTAG
debug interface. "Release" has full optimisation and contains no debug information.

Simply open the rtosdemo workspace file from within the IAR Embedded Workbench IDE, ensure *debug* or *release* is
selected as desired (as marked in red in the picture above), then select 'Rebuild All' from the IDE 'Project' menu.

#### Running the demo application

1. Ensure the J-Link JTAG debug interface is connected and that the prototype board is power up.
2. Select 'Debug' from the IDE 'Project' menu.
3. The microcontroller flash memory will automatically get programmed with the demo application, and the debugger
 will break at main() (C source debugging is only available if using the *debug* configuration).
 Select 'Go' from the IDE 'Debug' menu to start the application executing.

Once the demo has been programmed into the flash it can be executed without the debugger by simply removing the JTAG interface
and applying power.

#### Functionality

The demo application creates 25 tasks - 23 of the standard demo tasks, a 'check' task and the idle task. See the
 [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the standard demo tasks.

When executing correctly the demo application will behave as follows:

* The LEDs connected to the header pins marked T1\_ICAPA, T1\_ICAPB and T1\_OCMPB are under control of the 'flash' tasks.
 Each will flash at a constant frequency, with the LED on the T1\_ICAPA pin being the fastest and LED T1\_OCMPB
 being the slowest. Note these pins are set as GPIO outputs.
* The LED header pin marked T1\_OCMPA is under control of the standard ComTest Rx task. Its state will toggle each time
 the ComTest Rx task receives and verifies a character over the RS232 port. With the loopback connector in place the
 LED should flicker rapidly. Removing the loopback connector with cause the LED to be either permanently on or permanently
 off.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 The red LED built onto the KickStart development board is under control of the 'Check' task. Every three seconds the 'Check'
 task examines all the tasks in the
 system to ensure they are executing without error. It then toggles the red LED. If the red LED is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error. This mechanism can be checked by removing the loopback connector from the serial port
 (described above), and in doing so deliberately generating an error.

---

#### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/ARM7\_STR71x\_IAR/FreeRTOSConfig.h. The constants
defined in this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to
set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is
faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

An interrupt service routine that does not cause a context switch has no special requirements and can be written as per the
normal IAR syntax.
For example:

```c

    static __arm __irq void vAnISR( void )
    {
        /* ISR C code goes here. */

        /* End the interrupt in the EIC. */
        portCLEAR_EIC();
    }
```

Often you will require an interrupt service routine to cause a context switch. For example a serial port character being
received may wake a high priority task that was blocked waiting for the character. If the ISR interrupted a lower priority
task then it should return immediately to the woken task. Limitations in the IAR inline assembler necessitate such
interrupt service routines include an assembly file wrapper.

##### An example of an ISR with context switching capabilities

The main body of the ISR can be written in C within any source file as per the following template. This is just a normal
ARM mode function that includes a call to portEND\_SWITCHING\_ISR() at its end.

```c

    /* For simplicity the C function should operate in ARM mode.
       Note that the __irq modifier is NOT used. */

    __arm void vASwitchingISR( void )
    {
        char cContextSwitchRequired;

        /* Write the ISR body here as per normal.

        A boolean is used to say whether a context switch is required.
        In this example assume we posted onto a queue and this caused a
        task to be woken. */

        cContextSwitchRequired = pdTRUE;

        /* Immediately before the end of the ISR call the
        portEND_SWITCHING_ISR() macro. */

        portEND_SWITCHING_ISR( ( cContextSwitchRequired ) );

        /* End the interrupt in the EIC. */
        portCLEAR_EIC();
    }
```

See the function **vSerialISR()** defined in Demo/ARM7\_STR71x\_IAR/serial/serial.c for a complete example.

The entry point for the ISR has to be written in an assembly file. This just places a call to the C function between
calls to the portSAVE\_CONTEXT() and portRESTORE\_CONTEXT() macros respectively as per the following template:

```c

        EXTERN vASwitchingISR
        PUBLIC vASwitchingISREntry

    /* This header defines the save/restore macros. */
    #include "ISR_Support.h"

    vASwitchingISREntry:

        portSAVE_CONTEXT      ; Call portSAVE_CONTEXT macro first
        bl  vASwitchingISR    ; Then call the function written in the C file.
        portRESTORE_CONTEXT   ; Call portRESTORE_CONTEXT last.

        END
```

See the file Demo/ARM7\_STR71x\_IAR/serial/serialIAR.S79 for a complete example.

#### To use a part other than an STR712F

The STR71x family uses a standard ARM7 core so the main real time kernel components are
portable across all ARM7 devices - but the peripheral setup and memory requirements will require consideration.
Items to consider:

* prvSetupTimerInterrupt() in Source/portable/IAR/STR71x/port.c configures the watchdog peripheral
 to generate the RTOS tick.
* The interrupt service routine setup and management assume the existence of the interrupt controller.
* The serial port drivers.
* Register location definitions are provided by the library header files.
* Startup code and vector table setup is contained within Demo/ARM7\_STR71x\_IAR/SrcIAR/CStartup.s79.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/ARM7\_STR71x\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
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

Interrupt service routines always run in ARM mode. All other code executes in THUMB mode.

*Note*: The stack size of each necessary operating mode is configured using constants defined within the file
Demo/ARM7\_STR71x\_IAR/CStartup.s79. The IAR linker configuration utility is **not**
used, and stacks are **not** setup for all operating modes.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM7 demo application project to provide the memory allocation
required by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution. In particular they do not make use of the FIFO.

#### Tick Interrupt

The watchdog peripheral is used to generate the tick interrupt.

#### IAR compiler notes

The FreeRTOS source code has to be built with lots of different compilers. The IAR compiler has particularly strong
(pedantic) source checking and generates several warnings when compiling the FreeRTOS source code.

Unfortunately these warning cannot be fixed by modifying the source code as they predominantly relate to benign code that was
added in order to fix warnings generated by other compilers (mainly relating to type casting).
Some warnings have therefore been disabled in the project file.
