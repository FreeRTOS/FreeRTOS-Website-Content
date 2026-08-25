---
title: "Texas Instruments MSP430 (MSP430F449) RTOS Port for the MSPGCC (GCC) Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ES449.gif](/media/2018/ES449.gif)

The port was developed on an [ES449 development/prototyping board](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449)
from [SoftBaugh](http://www.softbaugh.com/) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board),
using the free [MSPGCC development tool chain](http://mspgcc.sourceforge.net/) and a SoftBaugh
[FETP parallel port JTAG interface](http://www.softbaugh.com/ProductPage.cfm?strPartNo=FETP)

The ES449 is a neat little MSP430F449 based prototyping board. It allows easy access to the MSP430 peripherals and includes
an LCD display - great for debugging!

There is also a port to the [Olimex MSP430F149 based EasyWEB2
development board](http://www.olimex.com/dev/msp-easyweb2.html). See the 'MSP430F149 EasyWeb2 Port' section at the bottom of this page.

FreeRTOS V5.1.0 upgraded this port and demo to permit tasks to use the MSP430 low power modes 1 to 3 - requiring interrupt service routines to be qualified
with the "wakeup" keyword. The UART driver in the demo application provides an example.

---

### IMPORTANT! Notes on using the MSPGCC MSP430 RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [Installing the Compiler](#installing-the-compiler-tool-chain)
3. [The Demo Application](#the-demo-application)
4. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The makefile used to build the MSP430 FreeRTOS demo project is located in the
Demo/msp430 directory.

---

### Installing the Compiler Tool Chain

To obtain and install the compiler:
1. Go to the [MSPGCC download page](http://sourceforge.net/project/showfiles.php?group_id=42303)
 and obtain the latest MSPGCC installation. I used the 'mspgcc-20040723.exe' download which installed
 everything I needed for a Win32 setup.
2. This step need only be performed if you wish to use the graphical version of GDB.

 The latest MSPGCC download only includes the command line GDB debugger. I prefer to use the graphical version called
 Insight. A slightly older [prebuilt version of Insight](http://prdownloads.sourceforge.net/mspgcc/msp430-insight-win32-20021222.exe?download) can be used. Install this older version of insight into a different directory to that
 chosen for the latest MSPGCC installation as you don't want to overwrite the files obtained in step 1.

 You should now have two installations. The latest version of MSPGCC installed during step 1, and a slightly older version
 of Insight from step 2. Both versions of the GDB debugger are called msp430-gdb.exe so one needs to be renamed.
 Locate the older version msp430-gdb.exe from the files installed during this step and rename it msp430-insight.exe.
3. Ensure the BIN directory from the files installed during step 1 and the BIN directory from the files installed during
 step 2 are included in your PATH environment variable.

---

### The Demo Application

### Functionality

The demo application includes some tasks that would normally flash LEDs.
The ES449 prototyping board has a built in LCD display and a single built in user
LED. Therefore, in place of flashing an LED, the tasks flash
'*' characters on the LCD. The left most '*' represents LED 0, the
next LED 1, etc.

The single on board LED is used by one of the ComTest tasks. It is toggled every time a character is received on the
serial port.

When executing correctly the demo application will behave as follows:

* The first three '*' characters on the LCD are under control of the 'flash' tasks. Each will
 flash at a constant frequency, with the first '*' being the slowest and the third being the
 fastest.
* The on board LED will flash each time a character is received on the serial port (see the hardware setup section below).
* Not all the tasks update the LCD so have no visible indication that they are operating correctly. Therefore a 'Check'
 task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 The '*' in the fifth position on the LCD is under control of the 'Check' task. Every
 three seconds the 'Check' task examines all the tasks in the system to ensure they are executing without error. It
 then toggles '*' 5. If '*' 5 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error.

### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters are transmitted by
one task and received by another - if any character is missed or received out of sequence an error condition is flagged.
Normally a loopback connector is required for this mechanism to work (so each character transmitted by the UART is also received
by the UART). In this case the 'loopback' mode of the MSP430 UART is used and no external connector is required.

The demo application uses the LCD in place of LEDs so no other hardware setup is required.

### Building the demo application

Ensure you have all the tools installed and accessible in your PATH environment as detailed above. Open a command prompt
(DOS box), navigate to the FreeRTOS/Demo/MSP430 directory, then simply type "make". The project should build with no
errors or warnings and produce an executable called 'a.out'.

### Executing the RTOS demo from FLASH

The MSPGCC download includes a flash programming utility called
msp430-jtag.exe that can be used to download a.out to the MSP430 flash. To program the flash:
1. Remove power from the ES449 prototyping board.
2. Connect the FETP JTAG adapter to the ES449 using the provided parallel port cable.
3. From your build directory (FreeRTOS/Demo/MSP430) type the command ...

```c
msp430-jtag -ep a.out
```

 ... this will erase the flash then program it with a.out.
4. Remove the FETP JTAG adaptor and power up the ES449. The demo application will execute.

### Executing the RTOS demo using the JTAG debugger

The FreeRTOS download includes a file called 'gdb.ini' in the FreeRTOS/Demo/MSP430 directory. This file is processed by
GDB every time GDB starts and is necessary for correct operation. It tells GDB how to connect to the remote target hardware
and then sets a breakpoint at the top of main(). If you are not using a Win32 host system you may need to rename 'gdb.ini'
to '.gdbinit'.

To run the application using the GDB graphical debugger:
1. Remove power from the ES449 prototyping board.
2. Connect the FETP JTAG adapter to the ES449 using the provided parallel port cable.
3. The MSPGCC download includes a program called msp430-gdbproxy.exe. This intercepts the GDB TCP commands and redirects
 them to the parallel port. Start msp430-gdbproxy (a shortcut to this will have been placed on the start menu when
 MSPGCC was installed). By default msp430-gdbproxy uses port 3333 - do not change this.
4. Program the flash as per the instruction in the section above. The flash can be programmed from within GDB but it is
 much faster to do it separately and beforehand.
5. Start the debugger using the command ...

```c
msp430-insight a.out
```

 ... the commands in the gdb.ini file will do the rest. If you prefer to use the command line debugger simply
 replace msp430-insight with msp430-gdb.
6. Insight will start at and the program will stop at the breakpoint in main() as shown below.

![](/media/2018/insightmsp.gif)

The debugger works well in most instances but suffers from a few problems - as noted on the MSPGCC website. Also note
the following points:

* When using the FETP JTAG adapter do not provide any other power source to the ES449 target hardware. I have found
 that doing so prevents the microcontroller timers from operating.
* When stopped on a breakpoint it appears as if the microcontrollers timers continue counting rather than stopping at
 the value they contained when the breakpoint was hit. As a timer compare match interrupt is used stepping through the
 code can result in the interrupt firing continuously (as the timer continues counting there is always an interrupt
 pending so as soon as you leave one you enter the next). It is therefore difficult when using the preemptive kernel
 to step through the code once the RTOS scheduler has been started and it is best to use the cooperative kernel when
 debugging.

---

### Configuration and Usage Details

### Serial port driver

As provided the serial port drivers are configured for loopback mode. This enables the demo application to execute but
switch loopback mode off for any other use.

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/MSP430/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type short.

Note that vPortEndScheduler() has not been implemented.

### To use a part other than an MSP430F449

The core real time kernel components should be
portable across all MSP430F4xx devices - but the peripheral setup and memory requirements will require consideration.
Items to consider:
* prvSetupTimerInterrupt() in Source/portable/GCC/MSP430F449/port.c configures the microcontroller timer to generate
 the RTOS tick.
* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/MSP430/main.c.
* The serial port drivers.
* Register location definitions are provided by the file msp430x44x.h which is included at the top of
 Demo/MSP430/FreeRTOSConfig.h.
* RAM size - see Memory Allocation below.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/MSP430/FreeRTOSConfig.h to 1 to use pre-emption or 0 to use
co-operative.

### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application makefile.
Do not lower the optimisation level below O2 as this changes the way parameters are passed to functions and will prevent
the real time kernel operating correctly.

### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the MSP430 demo makefile to provide the memory allocation required
by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

---

### MSP430F149 EasyWeb2 Port

This port was kindly provided by aLUNZ (email: alunz AT users.sourceforge.net). I am not able to support it directly as I do not have the target development board,
but it is very similar to the ES449 demo. [Download the MSP430F149
source code here](http://www.realtimeengineers.com/MSP149_EasyWeb.zip). The zip file contains a readme with installation instructions.

Please note that this port has not yet been upgraded to use the FreeRTOS V3.0.0 API.
