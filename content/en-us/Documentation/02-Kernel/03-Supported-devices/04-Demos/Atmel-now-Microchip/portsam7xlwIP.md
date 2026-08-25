---
title: "lwIP Embedded Web Server Demo using CrossStudio and GCC on an AT91SAM7X256"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

lwIP Embedded Web Server Demo using CrossStudio and GCC on an AT91SAM7X256

[[Embedded Ethernet Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]

|  |
| --- |
| <br />![](/media/2018/sam7xek.gif)<br />*Studio Cadrage*<br /> |

This page describes one of the FreeRTOS SAM7X embedded Ethernet sample applications. The demo creates a simple web server
using:
* The FreeRTOS GCC SAM7 ARM port.
* The [Rowley CrossStudio IDE](http://www.rowley.co.uk/arm/index.htm) and [CrossConnect USB JTAG debug interface](http://www.rowley.co.uk/arm/CrossConnect.htm). The demo can
 also alternatively be built using [standard (command line) GCC](#building-the-demo-using-gcc-command-line-version).
* Adam Dunkels open source [lwIP embedded TCP/IP stack](http://www.sics.se/~adam/lwip/).
* An Atmel AT91SAM7X-EK development board ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

This demo -

* Consists entirely of open source software.
* Includes a more comprehensive driver for the SAM7X integrated EMAC (Ethernet Media Access Controller) peripheral.
* Demonstrates the integration of lwIP with FreeRTOS.
* Demonstrates the creation of dynamic data.
* Includes a sample interrupt driven USB Serial CDC driver (thanks to Scott Miller for providing this adaptation of
 the FreeRTOS HID class USB driver).

Please note that lwIP is licensed separately from FreeRTOS. Users must familiarise themselves with the [lwIP license](http://savannah.nongnu.org/projects/lwip).

From FreeRTOS V4.0.3 onwards the demo project file includes a kernel aware window in the debugger. This provides useful information on the state of each
task in the system, but can slow down the debugger performance. Closing this window will permit faster debug operations.

---

#### *IMPORTANT! Notes on using the SAM7X Web Server Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [EMAC and USB Drivers](#emac-and-usb-drivers)
4. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)
5. [Building the Demo Using GCC (command line)](#building-the-demo-using-gcc-command-line-version)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports, so contains more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The lwIP CrossStudio demo project *rtosdemo.hzp* can be
found in the Demo/lwIP\_Demo\_Rowley\_ARM7 directory and should be opened from within the CrossWorks IDE.

Adam Dunkels lwIP code is located in the Demo/lwIP\_Demo\_Rowley\_ARM7/lwip-1.1.0 directory.

The Demo/lwIP\_Demo\_Rowley\_ARM7/EMAC directory contains the EMAC driver, and finally the Demo/lwIP\_Demo\_Rowley\_ARM7/USB
directory contains the USB CDC driver source code.

---

### The Demo Application

#### Demo application setup

Connect the AT91SAM7X-EK prototyping board to a computer running a web browser either directly using a point to point (crossover)
cable, or via a hub/router using a standard Ethernet cable. The prototyping board should also allow the use of a standard
Ethernet cable when connecting point to point, but I have not tested this configuration.

The IP address used by the demo is set by the constants emacIPADDR0 to
emacIPADDR3 within the file Demo/lwIP\_Demo\_Rowley\_ARM7/EMAC/SAM7\_EMAC.h.
The IP addresses used by the web browser computer and the prototyping board must be compatible.
This can be ensured by making the first three octets of both IP addresses identical.
For example, if the web browser computer uses IP address
192.168.100.1, then the prototyping board can be given any address in the range 192.168.100.2 to 192.168.100.254 (barring
any addresses already present on the network).

SAM7\_EMAC.h also contains constants that define the gateway address, the network mask, and the MAC address.
You must ensure that the configured MAC address is unique on the network to which the prototyping board is being connected.

Demo/lwIP\_Demo\_Rowley\_ARM7/EMAC/SAM7\_EMAC.c contains the definition USE\_RMII\_INTERFACE. This must be set appropriately
for your hardware. Setting USE\_RMII\_INTERFACE to 1 configures the MAC to operate in RMII mode. Setting
USE\_RMII\_INTERFACE to 0 configures the MAC to operate in MII mode.

A USB connection between the target hardware and a Windows host is required if you wish to test the USB CDC driver. The target
board can source its power through the same cable. The USB device will identify itself to the host as a serial COM port, then
when connected continuously stream a string of characters at 115,200 baud. The data is sent to the CDC driver from an idle
task hook.

The demo application uses the LEDs built onto the prototyping board so no other hardware setup is required.

#### Building the demo application for debug

Two project configurations are provided. "THUMB Flash Debug" uses minimal optimisation and can easily be used with the CrossConnect JTAG
debug interface. "THUMB Flash Release" has more optimisation and consequently is less debugger friendly.

Simply open the rtosdemo.eww workspace file from within the CrossWorks IDE, ensure *THUMB flash debug* is the selected
configuration (see picture below), then select 'Build Solution' from the IDE 'Build' menu.

![csselectbuild.gif](/media/2018/csselectbuild.gif)

Selecting the *THUMB flash debug* configuration

#### Running the demo application

1. Ensure the CrossConnect JTAG debug interface is connected and that the prototype board is power up.
2. Ensure an Ethernet cable is connected as described above.
3. Connect the CrossConnect JTAG interface to the target by selecting 'Connect USB CrossConnect for ARM' from the
 'Target' menu.
4. Select 'Start Debugging' from the IDE 'Debug' menu.
5. The embedded microcontroller Flash memory will automatically get programmed with the demo application, and the debugger
 will break at the start of the main() function. Select 'Go' from the IDE 'Debug' menu to start the application
 executing.

#### Functionality

The demo application creates 21 tasks - consisting predominantly of the standard demo application tasks (see the
 [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).
In addition the tasks associated with the lwIP TCP/IP stack and embedded web server, an example USB CDC task, a
'Check' task and the idle task are all created.

When executing correctly the demo application will behave as follows:

* LEDs DS1, DS2 and DS3 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED DS1 being
 the fastest and LED DS3 being the slowest.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other
 standard demo tasks.

 LED DS4 is under control of the 'Check' task. Every three seconds the 'Check' task examines all the standard demo tasks in the
 system to ensure they are executing without error. It then toggles LED DS4. If LED DS4 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error.
* The target hardware will serve a web page containing the TCP/IP statistics to a standard web browser. The page will
 automatically update every second. To connect to the target:

	1. Open a web browser on the connected computer.
	2. Type "HTTP://" followed by the target IP address into the browsers address bar.

	![](/media/2018/enterurl.gif)
	Entering the IP address into the web browser
	(obviously use the correct IP address for your system)
* The demo application will also identify itself to the USB host as a "FreeRTOS Demo CDC Driver", and the host "Found new
 hardware" wizard will prompt for the location of a suitable driver for the device.

![](/media/2018/foundnewcdc.gif)
Windows 'Found new hardware' message when the USB connection is detected.

 Direct the wizard to the directory FreeRTOS/Demo/lwIP\_Demo\_Rowley\_ARM7/USB where the file FreeRTOSCDC.inf
 will instruct Windows how to communicate with the CDC device.

 Once the driver has been successfully installed the SAM7X target will appear as serial COM port and continuously stream
 data bytes to the host.

![](/media/2018/devman.gif)
The 'FreeRTOS CDC Demo' shows as a COM port in the Windows device manager.

 The transmitted data can be viewed using any dumb terminal program (for example HyperTerminal) set to 115200 baud, with 8 data bits, no parity, one
 stop bit and no flow control.

![](/media/2018/hyperterm.gif)
Data transmitted through the USB port being viewed on HyperTerminal.

---

### EMAC and USB Drivers

#### Web Server and EMAC Operation

The very basic web server functionality is contained within the file Demo/lwIP\_Demo\_Rowley\_ARM7/BasicWEB.c. Each
HTTP connection is immediately serviced and then closed. A more complete implementation could spawn a new task for each
connection, then wait for data to arrive - deleting the task when the connection is closed.

The chained memory buffer implementation within the lwIP stack results in data being sent to and from the EMAC driver
in multiple segments of variable length. This is in contract to the uIP stack where only a single buffer exists, and all
data can be copied to and from the EMAC driver in a single segment. The EMAC driver used by the lwIP demo therefore
includes more comprehensive management of EMAC peripheral than the equivalent driver used by the uIP project.

Data received by the EMAC is buffered under control of the DMA. When a buffer is available for processing an EMAC interrupt
is generated. All the interrupt service routine does is signal to the EMAC driver via a semaphore that data is available for
processing. The semaphore immediately unblocks the interface task which processes the data, and if necessary either generates
a response or passes the data to the TCP/IP stack.

The driver blocks on the semaphore with a timeout. Therefore should no data become available for processing, the task
will periodically unblock to carry out the periodic processing required by the TCP/IP stack.

The number of receive buffers available to the EMAC is set by the constant NB\_RX\_BUFFERS within the file
Demo/lwIP\_Demo\_Rowley\_ARM7/EMAC/emac.h. Each receive buffer is 128 bytes, this size is specific to the hardware
and must not be altered.

The number of transmit buffers available to the EMAC is set by the constant NB\_TX\_BUFFERS also within emac.h.

#### EMAC Driver Re-entrancy

The EMAC driver can be accessed by more than one task. It is not inherently re-entrant and therefore access is guarded by
a semaphore at the network interface level (within the file ethernetif.c. This is in contrast to the uIP demo, where
only one task ever accesses the driver and explicit guarding is not required.

#### Modifications to the lwIP Code

The portable (non hardware specific) portions of the lwIP code remains fundamentally unmodified, with only a few minor edits
to remove benign compiler warnings.

#### USB Driver

The USB driver was provided by a third party as an adaptation of the original FreeRTOS HID class demo. It is included in the hope
that it will prove useful but cannot be directly supported. Note also that its heavy use of queues will be less efficient
than an alternative simpler circular buffer implementation.

---

### RTOS Configuration and Usage Details

This demo uses the FreeRTOS SAM7 GCC port.

#### RTOS port specific configuration

Configuration items specific to this port are contained in Source/Demo/lwIP\_Demo\_Rowley\_ARM7/FreeRTOSConfig.h. The constants defined in
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

See vEMACISR() defined in Demo/lwIP\_Demo\_Rowley\_ARM7/EMAC/SAM7\_EMAC\_ISR.c for a full example.

#### To use a part other than a SAM7

The SAM7 uses a standard ARM7 core with processor specific peripherals. The core real time kernel components should be portable
across all ARM7 devices - but the peripheral setup and memory requirements will require consideration. Items to consider:
* prvSetupTimerInterrupt() in Source/portable/GCC/ARM7\_AT91SAM7S/port.c configures the SAM7 timer to generate the RTOS tick.
* Port, memory access and system clock configuration is performed by the startup files and by prvSetupHardware() within Demo/lwIP\_Demo\_Rowley\_ARM7/main.c.
* The interrupt service routine setup and management assume the existence of the AIC (interrupt controller) peripheral.
* The serial, USB and Ethernet drivers.
* Register location definitions are provided by the Atmel supplied header files located in FreeRTOS/Source/portable/GCC/ARM7\_AT91SAM7S.
* RAM size - see Memory Allocation below.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/lwIP\_Demo\_Rowley\_ARM7/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project file.

#### Execution Context

The RTOS scheduler executes in supervisor mode, tasks execute in system mode.
NOTE! :
 The processor MUST be in supervisor mode when the RTOS scheduler is started (vTaskStartScheduler is
 called). The demo applications included in the FreeRTOS download switch
 to supervisor mode prior to main being called. If you are not using one of
 these demo application projects then ensure Supervisor mode is entered before calling vTaskStartScheduler().

Interrupt service routines always run in ARM mode. All other code will run in either ARM or THUMB mode depending on the build.
It should be noted that some of the macros defined in portmacro.h can only be called from ARM mode code, and use from THUMB code
will result in a compile time error. Please note that this particular demo has only been tested using THUMB mode.

Stacks have only been allocated for system/user, IRQ and SWI modes.

SWI instructions are used by the real time kernel and can therefore not be used by the application code (without modification
of the RTOS kernel code).

#### MAC Interface

Ensure USE\_RMII\_INTERFACE is configured appropriately for your hardware. See the Demo Application Hardware Setup notes above.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the SAM7X demo application to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

---

### Building the Demo Using GCC (command line version)

A makefile and linker script is provided that allows the lwIP Web Server demo to also be built using the standard command line
version of GCC. The makefile is located in the Demo/lwIP\_Demo\_Rowley\_ARM7 directory.

Note that, depending on the version of GCC used, the makefile may require the optimisation level to be set to a minimum of O1. Alternatively the -fomit-frame-pointer option can be added to the CFLAGS.

Linux users please note that as I don't have access to a Linux host the makefile has only been tested on a case insensitive Win32 host. Any build problems experienced on a Linux host are likely to
be the result of a file name having incorrect capitalisation. Please let me know if any such issues are encountered so they can be rectified in future releases.
