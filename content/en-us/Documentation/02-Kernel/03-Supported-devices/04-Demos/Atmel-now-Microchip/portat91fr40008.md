---
title: "Atmel AT91FR40008 (ARM7) RTOS Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Atmel AT91FR40008 (ARM7) RTOS Port

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/embestboard.jpg)

The port was developed by John Feller on an [ATEB40X prototyping board](http://www.embedinfo.com/English/Product/ateb40x.asp)
from Embest (Atmel AT91EB40 clone) using the open source GCC development tools ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

The development board came with a parallel port JTAG interface and flash programming utility.

---

#### IMPORTANT! Notes on using the [AT91R40008](http://www.microchip.com/wwwproducts/en/AT91R40008) RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The AT91R40008 GCC demo application makefile is contained in the FreeRTOS/Demo/ARM7\_AT91FR40008\_GCC directory.

The directory FreeRTOS/Demo/ARM7\_AT91FR40008\_GCC/Serial contains a sample interrupt driven serial port driver.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the AT91 GCC RTOS port.

#### ARM, THUMB, ROM and RAM builds

The following batch files are provided to build the demo application. The batch files set the environment
variables necessary for the relevant built before calling make.

* ROM\_ARM.bat - Creates an ARM mode release build suitable for programming into flash.
* RAM\_ARM.bat - Creates an ARM mode debug build suitable for execution from RAM.
* ROM\_THUMB.bat - Creates a THUMB mode release build suitable for programming into flash.
* RAM\_THUMB.bat - Creates a THUMB mode debug build suitable for execution from RAM.

The batch files are contained in the Demo/ARM7\_AT91FR40008\_GCC directory. Switching from one batch file to
the other requires a complete rebuild. To force a complete rebuild 'touch' the makefile.

#### RTOS Demo application hardware setup

The demo application includes the ComTest tasks - where one task transmits RS232 characters to another. For correct operation
of this real time task a loopback connector must be fitted to the RS232 port 0 of the Embest prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

The demo application uses the LEDs built onto the prototyping board so no further hardware setup is required.

#### Building and executing the RTOS demo application - Standalone from flash

The RTOS demo application can be executed either from flash or from RAM. This section provides instructions on creating and
programming a release build into the AT91FR40008 flash memory. It is assumed that the [GNUARM and UNXUTILS development tools](#win32-gnu-development-tools) are
already installed correctly and included in your PATH (to make them available from a Windows DOS prompt).

*To build the application*:

1. Open a DOS prompt, and navigate to the Demo/ARM7\_AT91FR40008\_GCC directory.
2. Type "rom\_arm" (or "rom\_thumb") to execute the rom\_arm.bat batch file. The batch file sets up the environment necessary for a release build then
 calls *make*. The build should complete with no errors or warnings.

*To download the RTOS demo to flash*:

1. Connect the parallel port JTAG interface between your host computer and the target hardware.
2. Open the Embest flash programming utility.
3. From within the flash programming utility, open the ATEB40x.cfg configuration file. This will setup all the
 necessary flash parameters for the target board.
4. Still within the flash programming utility, set the file to be programmed to Demo/ARM7\_AT91FR40008/rtosdemo.hex.
 This is the hex file output from the build process described above.

![](/media/2018/embestselectfile.gif)
Selecting the file to download
5. Erase the flash contents by pressing the Erase button, then reprogram the flash by pressing the Program button.

*Executing the demo application*:

Power down the prototyping board, remove the JTAG interface, then apply power again. The demo application will start to
execute.

#### Building and executing the RTOS demo application - Debug from RAM

The port authour has also tested and provided linker scripts for RAM execution.

See the corresponding section on the [LPC2106 ARM7 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106) port
documentation page for details of using the GCC debug tools.

#### Functionality

The demo application creates all of the standard minimal demo application real time tasks (see the
 [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).

When executing correctly the demo application will behave as follows:

* LEDs D3, D4 and D5 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED D3
 being the fastest and LED D5 being the slowest.
* When the loopback connector is in place every character transmitted by the ComTest Tx task is received by the ComTest
 Rx task. Each transmitted character causes LED D8 to toggle, each correctly received character causes LED D7 to
 toggle. LED D7 will only toggle if the received character matches the character the ComTest Rx task expected to receive.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 LED D10 is under control of the 'Check' task. Every three
 seconds the 'Check' task examines all the tasks in the system to ensure they are executing without error. It
 then toggles LED D10. If LED D10 is toggling every three seconds then no errors have ever been detected.
 The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error. This mechanism can be checked by removing the loopback connector from the serial port
 (described above), and in doing so deliberately generating an error.

### Configuration and Usage Details

#### Win32 GNU Development Tools

The GNU ARM7 development tools can be obtained pre-built from a number of locations.
I used the build available from [http://www.gnuarm.com](http://www.gnuarm.com/) on a Win2K host. The binary
distribution includes a convenient installation program that installs everything required. Some GNU development tool
distributions require Cygwin to be installed separately which is less convenient.

A *GNU make* compatible utility is also required. I use the [UNXUTILS](http://unxutils.sourceforge.net/) version.

#### RTOS port specific configuration

Configuration items specific to this port are contained in Source/Demo/ARM7\_AT91FR40008\_GCC/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

An interrupt service routine that does not cause a context switch has no special requirements and can be written as normal. For
example:

```c

    void vASimpleISR( void ) __attribute__((interrupt("IRQ")));

    void vASimpleISR( void )
    {
        /* ISR code goes here. */
    }
```

**Note:** The method of forcing a context switch from within an ISR has changed since FreeRTOS V4.5.0. Unfortunately the new method
requires different syntax, but is no longer dependent on the version of the compiler used, the command line switches, or the optimisation level.
Changing to the method described here should therefore remove the need to make any further alterations in the future.

The example here assumes that the interrupt handler is vectored to directly - that is, there is no entry code that is common to all
interrupts. Some of the other FreeRTOS demo applications are configured to use a common entry point as an alternative to this method.

To write an interrupt service routine that can cause a context switch:

1. Write a handler function. This will do the actual ISR processing. The handler function is a standard C function that has no
special requirements.
2. Write a wrapper function. This is the ISR entry point and must be declared using the "naked" attribute. The wrapper function
is the function that must be installed as the interrupt handler. It must call the actual handler function between calls to portSAVE\_CONTEXT()
and portRESTORE\_CONTEXT(). As with all ISR functions, the wrapper must be compiled to ARM code (as opposed to THUMB code).
3. Performing a context switch from within the ISR means that the task that executes when the ISR completes will not necessarily
be the task that was executing when the interrupt was taken. Such a context switch can be performed by calling portYIELD\_FROM\_ISR().

For example:

```c

    /* Declare the wrapper function using the naked attribute.*/
    void vASwitchCompatibleISR_Wrapper( void ) __attribute__ ((naked));

    /* Declare the handler function as an ordinary function.*/
    void vASwitchCompatibleISR_Handler( void );

    /* The handler function is just an ordinary function. */
    void vASwitchCompatibleISR_Handler( void )
    {
        long lSwitchRequired = pdFALSE;

        /* ISR code comes here. If the ISR wakes a task then
 lSwitchRequired should be set to 1. */

        /* If the ISR caused a task to unblock, and the priority
 of the unblocked task is higher than the priority of the
 interrupted task then the ISR should return directly into
 the unblocked task. portYIELD\_FROM\_ISR() is used for this
 purpose. */
        if( lSwitchRequired )
        {
            portYIELD_FROM_ISR();
        }
    }

    void vASwitchCompatibleISR_Wrapper( void )
    {
        /* Save the context of the interrupted task. */
        portSAVE_CONTEXT();

        Call the handler function. This must be a separate
 function unless you can guarantee that handling the
 interrupt will never use any stack space. */
        vASwitchCompatibleISR_Handler();

        /* Restore the context of the task that is going to
 execute next. This might not be the same as the originally
 interrupted task.*/
        portRESTORE_CONTEXT();
    }
```

See vUART\_ISR() defined in Demo/ARM7\_AT91FR40008\_GCC/serial/serialISR.c for a full example.

#### To use a part other than an AT91R40008

The AT91R40008 uses a standard ARM7 core with processor specific peripherals. The core real time kernel components should be portable
across all ARM7 devices - but the peripheral setup and memory requirements will require consideration. Items to consider:
* prvSetupTimerInterrupt() in Source/portable/GCC/ARM7\_AT91R40008/port.c configures the AT91R40008 timers to generate the RTOS tick.
* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/ARM7\_AT91FR40008\_GCC/main.c.
* The interrupt service routine setup and management assume the existence of the interrupt controller.
* The serial port drivers.
* Register location definitions are provided by the file AT91R40008.h which is included at the top of Demo/ARM7\_AT91FR40008\_GCC/FreeRTOSConfig.h.
* Startup code, memory map and vector table setup is contained within Demo/ARM7\_AT91FR40008\_GCC/boot.s.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/ARM7\_AT91FR40008\_GCC/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application makefile.

#### Execution Context

The RTOS scheduler executes in supervisor mode, tasks execute in system mode.

NOTE! :
 The processor MUST be in supervisor mode when the RTOS scheduler is started (vTaskStartScheduler is
 called). The demo applications included in the FreeRTOS download switch
 to supervisor mode prior to main being called. If you are not using one of
 these demo application projects then ensure Supervisor mode is entered before calling vTaskStartScheduler().

Interrupt service routines always run in ARM mode. All other code will run in either ARM or THUMB mode depending on the build.
It should be noted that some of the macros defined in portmacro.h can only be called from ARM mode code, and use from THUMB code
will result in a compile time error.

Demo/ARM7\_AT91FR40008\_GCC/boot.s configures stacks for system/user, IRQ and SWI modes only.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the AT91FR40008 demo application makefile to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

#### Notes for Linux users

I have only tested the makefile with Win32 builds of the GNUARM development tools.
