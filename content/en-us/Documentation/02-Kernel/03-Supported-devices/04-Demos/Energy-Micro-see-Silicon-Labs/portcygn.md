---
title: "Cygnal (Silicon Labs) 8051 Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![cygnal.jpg](/media/2018/cygnal.jpg)

The Cygnal port was developed on a [C8051F120-TB](https://www.silabs.com/products/mcu/Pages/C8051F120DK.aspx)
prototyping board ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board)
fitted with a [8051F120](https://www.silabs.com/products/mcu/mixed-signalmcu/Pages/C8051F12x3x.aspx) microcontroller.
The freeware [SDCC](http://sdcc.sourceforge.net/) compiler was used along with the Cygnal IDE.

The included demo application creates 21 real time tasks and uses an LED array wired to port 3 for eight 'flash' tasks.

---

#### IMPORTANT! Notes on using the 8051 RTOS port

*Please read all the following points before using this port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The SDCC makefile, and Cygnal IDE project file are located in the Demo/Cygnal directory.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the 8051 SDCC RTOS port.

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the serial port connector).

The standard 8 LED "flash" tasks assume LEDs are fitted to port 3. Omitting these LEDs will not cause the RTOS demo application
to fail, but will remove some visual feedback that everything is working as expected.

#### Building and executing the RTOS demo application

1. Ensure [SDCC](http://sdcc.sourceforge.net/) is installed correctly and in your PATH. See the notes on obtaining the correct SDCC version below.
2. Ensure you also have a GNU *make* compatible utility in your path. I use the [http://unxutils.sourceforge.net](http://unxutils.sourceforge.net) version. Alternatively you could convert the makefile into a batch file.
3. Unzip FreeRTOS, then in a DOS window move to the Demo/Cygnal directory and type "make". The source files should build with no errors or warnings.
4. Connect the prototyping board to your host PC using the Cygnal JTAG serial interface and apply power.
5. **Using a text editor** - open the Cygnal IDE project file (called sdcc.wsp and found in the Demo/Cygnal directory) and
 replace all the file path names with the correct FreeRTOS path for your installation. To find all the places that
 require changing perform a search on the string "E:devFreeRTOS" - this is where FreeRTOS is installed on my host computer.
6. Start the Cygnal IDE then select "Open Project" from the "Project" menu, and open "sdcc.wsp", which will now contain the correct paths for your system.
7. The IDE will connect to the prototyping board. Download the OMF file created from the build process, which is simply called "main" with no extension.

Once the OMF file has been downloaded you should be able to use the JTAG debugger to run/halt the application and inspect all the memory and
registers. If you experience any problems check the "Tool Vendor" is set to Dunfield. This option is accessed from the "Project | Tool Chain Integration" menu.

Using a batch file in place of the makefile allows builds to be performed from within the IDE, but I prefer to keep this separate.

#### Demo application functionality

The RTOS demo application creates 21 of the standard  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) tasks:
* The 8 LEDs on port 3 are under control of the standard 'flash' tasks. These should flash in the pattern described in
 standard  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.
 The built in green LED is under control of the 'check' task. The green LED toggling every 5 seconds indicates that
 all the demo application tasks are running without error. The toggle rate increasing to 500ms indicates an error has been
 detected in at least one of the standard demo application tasks. An error can be deliberately created to test this mechanism by
 removing the loopback connector.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/Cygnal/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type char.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/Cygnal/FreeRTOSConfig.h to 1 to use pre-emption or 0 to use
co-operative.

#### Development tools options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application makefile.

#### Stack start constant

Demo/Cygnal/FreeRTOSConfig.h contains the definition 'configSTACK\_START'. This is defined correctly for the
demo application, but will require updating should your application declare any variables qualified with the "data" keyword.

The correct configSTACK\_START value can be obtained from the .mem file which is output by SDCC during the build process.
For example, if the .mem file
contains the line

```c
"Stack starts at: 0x0e (sp set to 0x0d) with 242 bytes available"
```

then configSTACK\_START
should be set to 0x0e.

#### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the Cygnal demo application makefile to provide the memory allocation required
by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Compiler, header file and library versions

SDCC is an versatile compiler that is still undergoing development.
The version 2.4.0 release of SDCC does not support all the addressing modes required by the RTOS port. Instead the latest stable snapshot should be
used, this can be obtained from the SDCC link given above. The port was tested with the May 4 2004 snapshot.

In support of the new compiler version an updated c8051f120.h header file is required. This is **included** in the FreeRTOS distribution
and is located in the Demo/Cygnal directory. The version of this file supplied with the May 2004 Cygnal tools must **not** be used, although
later SDCC versions can.

The libraries supplied when you download SDCC are not built to be re-entrant, but are required to be so if used with the RTOS (this includes the libraries
to perform 16, 32 and floating point operations). You can easily re-build the libraries yourself, but as I have already done so I have made them
available here. The files in [this zip](/media/2018/reentrant_lib.zip) file should be unzipped into your sdcc/lib/large directory.
Please pay attention to the copyright and license notes within the library source files, and note that the vprintf library is **not**
re-entrant.

#### Deviations from standard 8051 architecture

I have attempted where possible to keep Cygnal specific code out of the RTOS source code. Instead the majority of Cygnal specific hardware
configuration is performed in the main.c file of the demo application.

The RTOS tick interrupt is generated from timer 2. This is the 16bit timer present on 8052 compatible devices, but not available on the
standard 8051.

256 bytes are available for the stack.

#### Speed and resource usage

Each real time task requires its own stack, but the 8051 architecture only allows a stack to reside in the small internal RAM. When a task is swapped
out it is therefore necessary to copy its entire stack from RAM to XRAM, and vice versa (this process is transparent to an application
writer/user). The Cygnal microcontroller, being exceptionally fast for an 8051, can cope with this without any problem (the demo
application sets the system clock to 98MHz). However, slower
processors may struggle. The demo application has a tick rate of 1000Hz. This high frequency is used for testing purposes, but can be made
much slower if your application allows.

Where possible, minimise stack usage.

#### Optimisation

There are many simple ways in which the RTOS could be tailored to the 8051 architecture and thus made more efficient. These require the use of special SDCC/8051 keywords. The RTOS source
code is supplied to be portable, and as such can be compiled with several different development tool suites - I have therefore not included
any 8051 specific optimisations in the distribution as downloaded.

Ways to optimise include:

* Use the 'data' qualifier in the declaration of the file scope variables within tasks.c. This will hold the variables
in internal RAM where they can be accessed much faster.
* Use the 'data' qualifier in other relevant places.
* Currently the task context is pushed onto the stack and the stack then copied to XRAM *before* checking to see if a higher
 priority task is ready to run. This could be modified so the context is pushed onto the stack, but the stack only copied to XRAM if
 necessary. If no context switch is required the original task would just pop its context off the stack and continue. This change would
 make the code very 8051 specific (which is why I have not done it).

#### Interrupt service routines

If an ISR causes a task to unblock it may be desirable for the ISR to return to the unblocked task rather than the interrupted task.
This can be done by calling taskYIELD() from within the ISR. When this is done it is essential to place the ISR code within a critical
region. Please see the code for vSerialISR() Demo/Cygnal/serial/serial.c for a full example, below is an outline:

```c

void ISRRoutine( void )
{
    /* Routine within critical region. */
    portENTER_CRITICAL();

    .
    . ISR Code Here
    .

    /* Switch to another task if necessary. */
    taskYIELD();

    portEXIT_CRITICAL();
}
```

#### The included makefile

It was tricky to get SDCC to output object files into a directory that allows the makefile to operate correctly. I found a mechanism for
doing this but am not happy with the syntax - I am not an expert on make but the command line I found worked the best appears to instruct
SDCC to overwrite the C files! To be safe I have commented out the line within the makefile.

The makefile therefore contains two sets of commands which can be selected between by commenting/uncommenting within the makefile.
The first are the commands I use and work very well with the UnxUtils make utility
but are commented out in case problems are caused with other systems. The second (uncommented) set will build the project without any problem,
but will rebuild the entire project even if only one source file has changed. You can choose which to use - see the comments within the makefile
(found in the Demo/Cygnal directory) for more information.

#### Serial port baud rates

The serial driver included with the RTOS demo application uses the baud rate calculation as detailed in the Cygnal manual. This works fine at
some baud rates, but others require slight adjustment. The serial port loopback test does not care if the baud rate is not quite correct as both
the sender and receiver use the same source.

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

#### SFR paging

The Cygnal microcontroller operates an SFR paging scheme. Some non 8051 standard peripherals require an SFR page to be selected before access
to the peripheral control registers can be obtained. Once the RTOS scheduler has been started the SFR page register must only be accessed from
within a critical section as it is not stored as part of a task context. If such a peripheral is used as an interrupt source the SFR page must
be reset to its original value before the end of the ISR or a call to taskYIELD() is made.

#### Linux users

I have only tested the makefile with Win32 builds of SDCC.
