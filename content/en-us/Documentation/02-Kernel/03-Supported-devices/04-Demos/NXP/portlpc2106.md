---
title: "Philips LPC2106 (ARM7) RTOS Port"
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
| <br /><br />![olimex.gif](/media/2018/olimex.gif)<br /> |

There are currently four FreeRTOS ports for the Philips LPC2000 ARM7 based embedded microcontroller - this page relates only to
the GCC port. Both ARM and THUMB modes are supported.

The port was developed on a LPC-P2106 low cost prototyping board
([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board) and uses the open source
[GNUARM development tools](http://www.gnuarm.com/) (compiler and debugger).

The FreeRTOS download includes a comprehensive ARM7 RTOS port demo application that creates and executes 32 real time tasks.
There are also two separate [embedded Ethernet TCP/IP web server example applications](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp).

---

#### IMPORTANT! Notes on using the [LPC2106](http://www.semiconductors.philips.com/pip/LPC2106BBD48.html) RTOS port

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

The LPC2106 GCC demo application makefile is contained in the FreeRTOS/Demo/ARM7\_LPC2106\_GCC directory.

The directory FreeRTOS/Demo/ARM7\_LPC2106\_GCC/Serial contains a sample interrupt driven serial port driver.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the LPC2000 GCC RTOS port.

#### ARM, THUMB, ROM and RAM builds

The following batch files are provided to build the demo application. The batch files set the environment
variables necessary for the relevant built before calling make.

* ROM\_ARM.bat - Creates an ARM mode release build suitable for programming into flash.
* RAM\_ARM.bat - Creates an ARM mode debug build suitable for execution from RAM.
* ROM\_THUMB.bat - Creates a THUMB mode release build suitable for programming into flash.
* RAM\_THUMB.bat - Creates a THUMB mode debug build suitable for execution from RAM.

The batch files are contained in the Demo/ARM7\_LPC2106\_GCC directory. Switching from one batch file to the other requires a complete
rebuild. To force a complete rebuild 'touch' the makefile.

#### RTOS Demo application hardware setup

The demo application includes the ComTest tasks - where one task transmits RS232 characters to another. For correct operation
of this real time task a loopback connector must be fitted to the RS232 port of the prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

There are three "flash" real time tasks which assume LEDs are fitted to pins P0.10, P0.11 and P0.12. Omitting these LEDs will
not cause the RTOS demo application to fail, but will remove some visual feedback that everything is working as expected.
In addition, every character transmitted by the ComTest Tx task toggles pin P0.13.

Not all the tasks update an LED so have no visible indication that they are operating correctly.
Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.
The on board LED is under control of the 'Check' task and is used to indicate the status of the RTOS demo application.
It will toggle every three seconds if all real
time tasks are executing as expected and no errors have occurred. An increase in the toggle rate to 500ms indicates that an
error has occurred in at least one task. An error can be deliberately created to test this mechanism by removing the
loopback connector.

Please read the Demo Application section of this site for more information on the RTOS demo application tasks.

#### Building and executing the RTOS demo application - Standalone from flash

The RTOS demo application can be executed either from flash or from RAM. This section provides instructions on creating and
programming a release build into the LPC2106 flash memory. It is assumed that the [GNUARM and UNXUTILS development tools](#win32-gnu-development-tools) are
already installed correctly and included in your PATH (to make them available from a Windows DOS prompt).

*To build the application*:

1. Open a DOS prompt, and navigate to the Demo/ARM7\_LPC2106\_GCC directory.
2. Type "rom\_arm" (or "rom\_thumb") to execute the rom\_arm.bat batch file. The batch file sets up the environment necessary for a release build then
 calls *make*. The build should complete with no errors or warnings.

*To prepare the prototyping board for download*:

1. Remove power from the prototyping board.
2. Install the BSL jumper (so BSL is shorted). The jumper causes the bootloader built into
 the LPC2106 to wait for a connection on the RS232 port.
3. Connect the prototyping board to your host using an RS232 cable.
4. Power up the prototyping board.

*To download the RTOS demo to flash*:

1. [Download and install the flash programming utility from Philips](http://www.semiconductors.philips.com/files/products/standard/microcontrollers/utilities/lpc2000_flash_utility.zip).
2. Execute then configure the flash programming utility as follows:
	1. Set the Device to LPC2106.
	2. Set the XTAL frequency to 14746KHz
	3. Set the COM port to the correct port for your host machine.
	4. Ensure the "Use DTS/CTS" check box is not checked.
 The bootloader will automatically detect the baud rate used so the exact baud setting is not important - but do not
 set it too high.
3. Select the "Flash Buffer Operations" menu item found on the "Buffer" menu. This will cause a new window to open.
4. In the new window:
	1. Use the "Load Hex File" button to load the hex file generated from the build. It is called rtosdemo.hex
	 and is in the Demo/ARM7\_LPC2106\_GCC directory.
	2. Click the "Vector Calc" button. This will change one of the entries in the vector table to ensure the bootloader
	 recognises that a valid program exists.
	3. Finally, click "Upload To Flash".
 A prompt will appear requesting that the prototyping board is reset - but this may not be necessary if the bootloader
 is already waiting for a connection. Once the programming utility has connected to the prototyping board it expects the connection
 to be maintained. This means that if you reset the prototyping board then attempt to program it again the programming utility will
 complain that it cannot communicate with the target. If this happens simply acknowledge the error, then repeat the step.

*To execute the RTOS demo application once programmed*:

1. Remove power from the prototyping board.
2. Remove the RS232 cable from the prototyping board and replace it with a loopback connector.
3. Remove the BSL jumper - so the boot loader does not wait for a connection on the RS232 port.
4. Apply power

#### Building and executing the demo application - Debug via JTAG

This section provides instructions on using the debugger with the low cost WIGGLER
compatible JTAG interface. A utility called OCDLibRemote is used to interface between the debugger and the JTAG WIGGLER.
Again, it is assumed that
the [GNUARM and UNXUTILS development tools](#win32-gnu-development-tools) are already installed correctly and included in your PATH (to make them available
from a Windows DOS prompt).

*To build the application*:

1. Open a DOS prompt, and navigate to the Demo/ARM7\_LPC2106\_GCC directory.
2. Type "ram\_arm" (or "ram\_thumb") to execute the ram\_arm.bat batch file. The batch file sets up the environment necessary for a debug build then
 calls *make*. The build should complete with no errors or warnings.

*To prepare the prototyping board for debugging*:

1. Remove the BSL jumper.
2. Install the JTAG jumper.
3. Connect the JTAG WIGGLER between the JTAG port on the prototyping board and the parallel port on your host.

*To setup OCDLibRemote*:

1. Download and install OCDLibRemote, a link to which can be found on  [this
 page](http://www.macraigor.com/full_gnu.htm).
2. Start OCDLibRemote using the command "OCDLibRemote --cpu ARM7 --device WIGGLER 1" in a DOS prompt.
 I find that the command to start OCDLibRemote may have to be repeated several times in order to establish a connection with
 the JTAG WIGGLER.

*Using the debugger*:

1. Open another DOS prompt, and navigate to the Demo/ARM7\_LPC2106\_GCC directory.
2. Start the graphical debugger with the command "arm-elf-insight rtosdemo.elf".
3. Configure the debugger:
	1. Select the "Target Settings" menu option from the "File" menu. This will open a new window.
	2. Use the Target drop down list to select GDBServer/TCP. OCDLibRemote is acting as the GDB server in this case.
	3. Set the Hostname to "localhost".
	4. Set the Port to 8888 - the default for OCDLibRemote.
	5. Ensure the "Breakpoint at 'main'" check box is checked.
4. Download the code to the prototyping board by [these steps can be automated, but are best carried out individually the
 first time to familiarise yourself with the process]:
	1. Select the "Connect To Target" menu item from the "Run" menu. You should receive a message acknowledging that
	 a connection with OCDLibRemote has been established.
	2. Select the "Download" menu item from the "Run" menu. You should see a blue status bar indicate the download
	 progress. Once downloaded the program will execute up to the breakpoint at main.
5. To execute the program click the "Continue" speed button.

**Tip:** The debugger works very well except for the Registers menu item - which causes an error. To view the register contents, open
a console (CTRL+N), then in the console type "info registers".

### Configuration and Usage Details

#### Win32 GNU Development Tools

The GNU ARM7 development tools can be obtained pre-built from a number of locations.
I used the build available from [http://www.gnuarm.com](http://www.gnuarm.com/) on a Win2K host. The binary
distribution includes a convenient installation program that installs everything required. Some GNU development tool
distributions require Cygwin to be installed separately which is less convenient.

A *GNU make* compatible utility is also required. I use the [UNXUTILS](http://unxutils.sourceforge.net/) version.

#### RTOS port specific configuration

Configuration items specific to this port are contained in Source/Demo/ARM7\_LPC2106\_GCC/FreeRTOSConfig.h. The constants defined in
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

See vUART\_ISR() defined in Demo/ARM7\_LPC2106\_GCC/serial/serial.c for a full example.

#### To use a part other than an LPC2106

The LPC2106 uses a standard ARM7 core with processor specific peripherals. The core real time kernel components should be portable
across all ARM7 devices - but the peripheral setup and memory requirements will require consideration. Items to consider:
* prvSetupTimerInterrupt() in Source/portable/GCC/ARM7\_LPC2000/port.c configures the LPC2106 timer 0 to generate the RTOS tick.
* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/ARM7\_LPC2106\_GCC/main.c.
* The interrupt service routine setup and management assume the existence of the vectored interrupt controller.
* The serial port drivers.
* Register location definitions are provided by the file lpc210x.h which is included at the top of Demo/ARM7\_LPC2106\_GCC/FreeRTOSConfig.h.
* Startup code, memory map and vector table setup is contained within Demo/ARM7\_LPC2106\_GCC/boot.s.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/ARM7\_LPC2106\_GCC/FreeRTOSConfig.h to 1 to use pre-emption or 0
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

Demo/ARM7\_LPC2106\_GCC/boot.s configures stacks for system/user, IRQ and SWI modes only.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the LPC2000 demo application makefile to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

#### Notes for Linux users

I have only tested the makefile with Win32 builds of the GNUARM development tools.
