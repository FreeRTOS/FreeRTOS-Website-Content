---
title: "Atmel AVR32 AT32UC3A0512 and AT32UC3B0256 Demos"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Atmel AVR32 AT32UC3A0512 and AT32UC3B0256 ports including an lwIP TCP/IP example application

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)][[Embedded Ethernet Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]

![](/media/2018/evk1100.jpg)
The EVK1100 development system (Ethernet cable not shown)

**Note:** The AVR32 port in the FreeRTOS download works with the ES marked chips. See the
[Atmel Software Framework](https://www.microchip.com/avr-support/advanced-software-framework-(asf)) for the latest port for the latest chips.

This page presents the FreeRTOS AVR32 UC3A and UC3B ports and demo application for the [AVR32 AT32UC3](https://www.microchip.com/wwwproducts/en/AT32UC3C1512C) range of microcontrollers.

Instructions are provided for building the standard demo application with both the AVR32 GCC and
[IAR](https://www.iar.com/ja/products/architectures/microchip/iar-embedded-workbench-for-avr32)(V2.21A or higher required) development tools. For the UC3A port an[embedded TCP/IP example](#lwip-embedded-tcpip-example) is also provided.
The TCP/IP demo uses the [lwIP TCP/IP stack](http://savannah.nongnu.org/projects/lwip/) and includes a basic web and TFTP server implementation.

The demo application was developed on and targeted at the [EVK1100](https://www.microchip.com/webdoc/evk1100/evk1100.Introduction.html) and
[EVK1101](https://www.microchip.com/webdoc/evk1101/pr01.html) evaluation boards for the AVR32UC3A and AVR32UC3B demos respectively ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

*Thanks to the Atmel engineers for their large contribution in the development of this port!*

There is also a separate [port under development](http://sourceforge.net/projects/ap7x-freertos/) for the AVR32 AP7000 series.

---

#### IMPORTANT! Notes on using the Atmel AVR32 port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

This section described the standard demo application. Information on the TCP/IP demo can be found [at the bottom of this page](#lwip-embedded-tcpip-example).

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The AT32UC3A demo makefile for the GCC tools can be located in the FreeRTOS/Demo/AVR32\_UC3/AT32UC3A/GCC directory.

The AT32UC3B demo makefile for the GCC tools can be located in the FreeRTOS/Demo/AVR32\_UC3/AT32UC3B/GCC directory.

The AT32UC3A demo project file for the IAR tools is called RTOSDemo.eww and can be
located in the FreeRTOS/Demo/AVR32\_UC3/AT32UC3A/IAR directory.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes an interrupt driven UART test where one task transmits characters that are then received by
another task. For correct operation of this functionality a loopback connector must be fitted to the UART\_0 connector of the EVK1100 or USART1 of the EVK1101
development board (pins 2 and 3 must be connected together on the 9Way connector).

The demo application makes use of the LEDs that are built onto the EVK1100 / EVK1101 so no further hardware setup is required.

#### Functionality

main() simply sets up the hardware, creates all the demo application tasks,
then starts the RTOS scheduler. The [Demo Application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section of the FreeRTOS website provides
more information on the standard demo tasks.

In addition to a subset of the standard demo application tasks, main.c also
defines a 'check' task.

The check task only executes every three seconds but has a
high priority so is guaranteed to get processor time. Its function is to
check that all the other tasks are still operational and that no errors have
been detected at any time. In addition the 'check' task exercises the memory
allocator by repeatedly allocated and freeing blocks of memory.

When executing correctly (without the 'check' task having detecting any errors) the demo application will behave as follows (note that LED assignments are
correct for the EVK1100. Not all the LEDs are present on the EVK1101):

* LED1, LED2 and LED3 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED1 being the fastest and LED3 the slowest.
* LED4 and LED5 are controlled by the standard ComTest tasks. LED4 will toggle each time the ComTest Tx task transmits a character over the RS232 port.
 LED5 will toggle each time the ComTest Rx task receives a character over the RS232 port and verifies that the received character is that expected.
* LED 6 (red half) is under control of the 'check task'. A toggle rate of three seconds indicates that no errors have been detected. A toggle rate of
 500ms indicates that an error has been detected in at least one other task [this
 mechanism can be checked by removing the loopback connector from the RS232 port, and in so doing deliberately creating an error].
* LED 6 (green half) will also be illuminated should the check task detect an error in any other task or the memory allocator.

In total the demo application creates 35 tasks.

#### Building and executing the demo application - IAR

1. Open the FreeRTOS/Demo/AVR32\_UC3/AT32UC3A/IAR/RTOSDemo.eww project from within the Embedded Workbench IDE.
2. Select "Rebuild all" from the "Project" menu. The project should build with no warning or errors.
3. Connect the EVK1100 development board JTAG to your host PC using the Atmel [JTAG ICE mk-II](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATJTAGICE2).
4. Power up the EVK1100. This can be done either by connecting the EVK1100 to you host PC via a USB cable, or using the EVK1100 power jack. Take care
 with the power polarity when using the latter!
5. Select "Debug" from the "Project" menu. The AVR32 flash memory will be programmed and the debugger started.

The IAR project workspace is divided into a number of separate folders to facilitate navigation. It also contains two configurations - Debug and Release.

![](/media/2018/avr32iarproject.gif)
The AVR32 project workspace

#### Building and executing the demo application - GCC

A comprehensive makefile is provided to facilitate build, download and debug management.

##### To build the project:

1. Open a command prompt (Cygwin or Windows) and navigate to the FreeRTOS/Demo/AVR32\_UC3/AT32UC3A/GCC or FreeRTOS/Demo/AVR32\_UC3/AT32UC3B/GCC directory
 for the UC3A and UC3B demos respectively.
2. Enter the command 'make'.

##### To program the AVR32 UC3A or AVR32 UC3B flash memory:

1. Connect the EVK1100 or EVK1101 development board JTAG to your host PC using the Atmel [JTAG ICE mk-II](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATJTAGICE2).
2. Power up the EVK1100 or EVK1101. This can be done either by connecting the EVK1100 or EVK1101 to you host PC via a USB cable, or using the power jack. Take care
 with the power polarity when using the latter!
3. Following a successful build (instructions above), remain in the same directory and enter 'make program'. Below is the output that should be obtained -

```c

$ make program

Programming MCU memory from `uc3a0512-rtosdemo.elf'.
Connected to JTAGICE mkII version 4.7, 4.20 at USB.
     Unlocking flash: ================================================== 100.0%
       Erasing flash: done
Writing 46736 bytes from uc3a0512-rtosdemo.elf to memory at 0x80000000.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Writing 2992 bytes from uc3a0512-rtosdemo.elf to memory at 0x8000b690.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Writing 4096 bytes from uc3a0512-rtosdemo.elf to memory at 0x8000c240.
   Programming flash: ================================================== 100.0%
       Reading flash: ================================================== 100.0%
     Verifying flash: ================================================== 100.0%
Verification succeeded.
Resetting CPU.
```

##### Other commands:

Having programmed the flash, to start the program executing simply enter the command 'make run'.

If you have [Doxygen](http://www.stack.nl/~dimitri/doxygen/) installed then the HTML documentation can be created using the command 'make doc'.

Commands can be combined onto a single line. For example, to build the files,
program the flash, then start the program executing from a single line enter the command 'make program run'.

##### Starting the GDB debugger:

1. First the GDB proxy must be started:

	1. Open another command prompt.
	2. In the new command prompt window, enter the command 'avr32gdbproxy -finternal@0x80000000,512Kb -a extended-remote:4242'. This starts avr32gdbproxy and
	 connects it to a host called 'extended-remote' with port number '4242'.
2. Back in the original command prompt, build and download the FreeRTOS demo using the instructions above.
3. Enter the command 'avr32-gdb' to start the GDB client.
4. Next, start a debug session by connecting to the GDB proxy using the command 'target extended-remote:4242'.
5. Load the symbol table using the command 'sym uc3a0512-rtosdemo.elf' or 'sym uc3b0256-rtosdemo.elf' for the UC3A or UC3B respectively.
6. Finally, start the program executing by entering the command 'cont'. Below is the output from a sample session:

```c

$ avr32-gdb

GNU gdb 6.4.atmel.1.0.0
Copyright 2005 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "--host=i686-pc-cygwin --target=avr32".

(gdb) target extended-remote:4242
Remote debugging using :4242
0x80000000 in ?? ()

(gdb) sym uc3a0512-rtosdemo.elf
Reading symbols from /cygdrive/c/e/dev/FreeRTOS/Demo/AVR32_UC3/AT32UC3A/GCC/
                                                  uc3a0512-rtosdemo.elf...done.

(gdb) cont
Continuing.
```

See the [GDB manual](http://www.gnu.org/software/gdb/documentation/) for full information on using the GDB debugger.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in FreeRTOS/Demo/AVR32\_UC3/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Note that as by default the AVR32 port permit's interrupts to be nested, calls made to API functions from within an ISR must be contained within a critical section.

An interrupt service routine that does not cause a context switch has no special requirements and can be written as per the compiler documentation.

Special syntax is required if you wish your interrupt service routine to cause a context switch. That demonstrated here is for the GCC compiler. See the file
FreeRTOS/Demo/AVR32\_UC3/serial/serial.c for an example of both the GCC and IAR syntax.

To write an ISR from which a context switch can be performed:

1. Declare the ISR using the "naked" attribute.
2. The first statement in the ISR must be a call to the portENTER\_SWITCHING\_ISR() macro. This must be before any local variable declarations.
3. The last statement in the ISR must be a call to the portEXIT\_SWITCHING\_ISR( bool ) macro. A boolean is passed to the macro to indicate whether a
context switch is required or not.

For example:

```c

    void vASwitchCompatibleISR( void ) __attribute__ ((naked));

    void vASwitchCompatibleISR( void )
    {
        /* Macro must be called first. */
        portENTER_SWITCHING_ISR();

        /* Variables declarations can come next. */
        long lSwitchRequired = 0L;

        /* ISR code comes here.  If the ISR wakes a task then
        lSwitchRequired should be set to 1. */

        /* Final statement is the closing macro. */
        portEXIT_SWITCHING_ISR( lSwitchRequired );
    }
```

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The demo application will only execute correctly with configUSE\_PREEMPTION set to 0 if configIDLE\_SHOULD\_YIELD is set to 1.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_3.c is included in the AVR32 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimized solution.

---

### lwIP Embedded TCP/IP example

The embedded Ethernet example uses the FreeRTOS GCC and IAR ports described above. The build, download, debug and configuration instructions documented above for the
standard demo are also relevant for the TCP/IP example. This section provides some additional information that is specific to the TCP/IP example only.

### Source Code Organization

The makefile/project file for the embedded TCP/IP example is located in the FreeRTOS/Demo/lwIP\_AVR32\_UC3/GCC or FreeRTOS/Demo/lwIP\_AVR32\_UC3/IAR directory for GCC and IAR respectively.
The makefile provides the same facilities as those
described for the standard demo.

### TCP/IP Software Setup

The IP address used by the demo is set by the constants emacIPADDR0 to emacIPADDR3 within the file FreeRTOS/Demo/lwIP\_AVR32\_UC3Demo/conf\_eth.h.
The IP addresses used by the web browser computer and the prototyping board must be compatible. This can be ensured by making the first three octets of both
IP addresses identical. For example, if the web browser computer uses IP address 192.168.100.1, then the prototyping board can be given any address in the range
192.168.100.2 to 192.168.100.254 (barring any addresses already present on the network).

conf\_eth.h also contains constants to configure the MAC address, gateway address and network mask. The MAC address **must** be unique for the network
on which the development board is to be connected.

### Hardware Setup

Connect the EVK1100 prototyping board to a computer running a web browser either directly using a point to point (crossover) cable, or via a hub/router using a
standard Ethernet cable. The prototyping board may also allow the use of a standard Ethernet cable when connecting point to point, but I have not tested this
configuration.

### Demo Application Functionality

##### LED Flash Tasks

The demo application includes the standard flash tasks (as described for the standard demo application above). This provides visual feedback that the demo is running.

##### Web Server

The EVK1100 will serve a web page containing FreeRTOS task information to a standard web browser. The page will automatically update every few seconds.
To connect to the target:

1. Open a web browser on the connected computer.
2. Type "HTTP://" followed by the target IP address into the browsers address bar.

![](/media/2018/enterurl.gif)
Entering the IP address into the web browser
(obviously use the correct IP address for your system)
##### TFTP Server

The basic TFTP server permits a single small file to be sent to, then retrieved from the demo application. Below is the output from an example TFTP session that sends then receives
the file samplefile.txt to an EVK1100 running with IP address 172.25.218.100:

```c

    C:tftp 172.25.218.100 put samplefile.txt
    Transfer successful: 19 bytes in 1 second, 19 bytes/s

    C:>tftp 172.25.218.100 get samplefile.txt
    Transfer successful: 19 bytes in 1 second, 19 bytes/s

    C:>
```
