---
title: "Philips (now NXP) LPC2129 (ARM7) RTOS Port for the IAR Development Tools"
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

There are currently four FreeRTOS ports for the Philips LPC2000 ARM7 based embedded microcontroller.
This page relates only to the port for the [IAR development tools](http://www.iar.com/ewarm).

The port was developed on an [MCB2100 development/prototyping board](http://www.keil.com/mcb2100)
using a J-LINK USB JTAG interface ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

The MCB2100 is a fully featured and comprehensive prototyping board that allows easy access to the LPC2129 peripherals and
includes 8 built in LEDs which are utilised by the FreeRTOS demo application.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### *IMPORTANT! Notes on using the IAR LPC2000 RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so contains more files than used by this demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR Embedded Workbench project file for this demo can be found in the Demo/ARM7\_LPC2129\_IAR directory,
which also contains main.c, the source file containing the main() function.

The Demo/ARM7\_LPC2129\_IAR/SrcIAR and the Demo/ARM7\_LPC2129\_IAR/resource directories
contain support files for the IAR Philips build environment.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the IAR LPC2129 RTOS port.

#### Functionality

The demo applications can be built using the IAR development tools KickStart version - which has a file size limit
of 32K bytes.

Two configurations are provided within the project file - 'flash debug' with no optimisation, and 'flash bin' will full
optimisation (barring the static clustering option).

The demo application creates 25 of the standard demo tasks, the idle task, and a 'Check' task.
See the  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks.
When executing correctly the demo application will behave as follows:

* LEDs P1.16, P1.17 and P1.18 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED P1.16 being
 the slowest and LED P1.18 being the fastest.
* LED P1.19 will flash each time a character is transmitted on the serial port.
* LED P1.20 will flash each time a character is received on the serial port.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 LED P1.23 is under control of the 'Check' task. Every three seconds the 'Check' task examines all the tasks in the
 system to ensure they are executing without error. It then toggles LED P1.23. If LED P1.23 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error. This mechanism can be checked by removing the loopback connector from the serial port
 (described below), and in doing so deliberately generating an error.

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the P2 serial port connector of COM 0).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

#### Building the demo application

Simply open the RTOSDemo.ewp project workspace file from within the IAR IDE, select the required configuration,
then select 'Make' from the IDE 'Project'
menu. The application should build with no errors or warnings.

![](/media/2018/ewprojselect.jpg)
Selecting the 'Flash Debug' configuration

#### Running the demo application

The IAR port cannot be executed using the IAR simulator so must be executed on the target hardware:
1. Ensure the J-Link JTAG debug interface is connected and that the prototype board is power up.
2. Select 'Debug' from the IDE 'Project' menu.
3. The microcontroller Flash memory will automatically get programmed with the demo application, and if using the debug
 build the debugger
 will break at main(). Select 'Go' from the IDE 'Debug' menu to start the application executing.

An alternative JTAG interface
can be selected using the Debugger category within the project options dialogue box.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/ARM7\_LPC2129\_IAR/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

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

        /* End the interrupt in the VIC. */
        VICVectAddr = 0;
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

        /* End the interrupt in the VIC. */
        VICVectAddr = 0;
    }
```

See the function vSerialISR() defined in Demo/ARM7\_LPC2129\_IAR/serial/serial.c for a complete example.

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

See the file Demo/ARM7\_LPC2129\_IAR/serial/serialIAR.S79 for a complete example.

#### To use a part other than an LPC2129

The LPC2129 uses a standard ARM7 core with processor specific peripherals. The core real time kernel components should be
portable across all ARM7 devices - but the peripheral setup and memory requirements will require consideration.
Items to consider:
* prvSetupTimerInterrupt() in Source/portable/IAR/LPC2000/port.c configures the LPC2129 timer 0 to generate the RTOS tick.
* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/ARM7\_LPC2129\_IAR/main.c.
* The interrupt service routine setup and management assume the existence of the vectored interrupt controller.
* The serial port drivers.
* Register location definitions are provided the file iolpc2129.h which is included at the top of Demo/ARM7\_LPC2129\_IAR/FreeRTOSConfig.h.
* Startup code is contained within Demo/ARM7\_LPC2129\_IAR/SrcIAR/cstartup.s79. main() must be called
 with the processor in Supervisor mode.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/ARM7\_LPC2129\_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
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

Interrupt service routines always run in ARM mode. All other code will run in either ARM or THUMB mode depending on the build.
It should be noted that some of the macros defined in portmacro.h can only be called from ARM mode code, and use from THUMB code
will result in a compile time error. The Embedded Workbench project is configured for THUMB mode - see the LPC2006 GCC port for
an example of the configuration required to use just ARM mode.

Demo/ARM7\_LPC2129\_IAR/Startup.s configures stacks for system/user, IRQ and SWI modes only.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ARM7 demo application makefile to provide the memory allocation required
by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.
