---
title: "Tern E-Engine 80x186 RTOS port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Embedded Ethernet Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]
[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/ternee.jpg)

This page describes the FreeRTOS port for the [Tern](http://www.tern.com/) range of x186 based controllers, with the Tern [E-Engine controller](http://tern.com/products-2/186-processor-boards/ethernet-engine/) (Ethernet Engine)
chosen as the target for the pre-configured demo
application ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board). The E-Engine control board includes an i2chip based WizNET embedded TCP/IP processor which the demo application uses via a (currently) simple HTTP interface to
display RTOS status information.

The demo application is limited to the small memory model to enable it to be build and debugged using the evaluation version of the [Paradigm C/C++ compiler](http://www.devtools.com/) - Tern edition delivered with
the controller kit.

The E-Engine interfaces to the i2chip through a memory mapped interface. A [separate FreeRTOS demo application](/webservedemo)
demonstrates interfacing to the same TCP/IP co-processor via an I2C interface using an ARM7 processor.

*Please note the files socket.c, i2chip\_hw.c and associated headers and libraries are included with kind permission of Tern Inc. These files are copyright Tern Inc
and are not covered by the modified GPL.*

**Note for Paradigm C/C++ Version 7 Users:** Version 7 uses a slightly different stack frame and therefore requires a few modifications to the RTOS kernel port
files. Dave Lyneham has generously provided a project that contains the changes necessary, along with a readme.txt file to explain why they are needed.
The files can be obtained from the [FreeRTOS Interactive x86 forum](http://interactive.freertos.org/entries/139169-freertos-port-for-paradigm-c-v5-v7-for-tern-modules).
Thanks Dave!

---

### *IMPORTANT! Notes on using the Tern Inc. 80x186 RTOS Demo*

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

The E-Engine demo application can be built using the preconfigured Paradigm Tern Edition compiler project file which is called RTOSDemo.ide and is located in the
FreeRTOS/Demo/WizNET\_DEMO\_TERN\_186 directory.

---

### The Demo Application

### Demo application setup

Connect the E-Engine controller board to a computer running a web browser either directly using a point to point (crossover)
cable, or via a hub/router using a standard Ethernet cable.

The IP address used by the demo is set by the constant "ucIPAddress" defined at the top of FreeRTOS/Demo/WizNET\_DEMO\_TERN\_186/HTTPTask.c.
The IP addresses used by the web browser computer and the controller board must be compatible.
This can be ensured by making the first three octets of both IP addresses identical.
For example, if the web browser computer uses IP address
192.168.100.1, then the controller board can be given any address in the range 192.168.100.2 to 192.168.100.254 (barring
any addresses already present on the network).

The MAC address used by the demo is set by the constant "ucMacAddress" within the same file.
You must ensure that the configured MAC address is unique on the network to which the controller board is being connected.

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate. The serial port test is preconfigured to use COM2 on the controller board as
the debugger interface defaults to use COM1. The simplest way of looping the COM2 Tx pin to the COM2 Rx pin on the E-Engine board is to place a jumper
on pins 2 and 3 of the COM2 connector, so that the two pins are shorted together.

### Building and executing the demo application

The Tern edition of the Paradigm development tools permits remote debugging directly from within the Paradigm IDE. These instructions assume that the
Tern debug monitor is already programmed into the controller board flash - the default for newly purchased controller boards.

1. Connect the E-Engine to your host PC using the RS232 ribbon cable provided with the control board. COM1 should be used on the controller board.
2. Open up the RTOSDemo.ide project file from within the Paradigm IDE.

![](/media/2018/ternproj.gif)
The demo project shown in the Paradigm IDE.

 The project is partitioned as follows:

	* i2chip\_src - source pool containing the i2chip driver. The majority of this code is provided by and copyright to Tern Inc.
	* FreeRTOS\_source - source pool containing the FreeRTOS kernel source code.
	* DemmoApp\_source - source pool containing the standard FreeRTOS demo application files.
	* RTOSDemo - this is the project which contains references to the three source pools described above. It also contains main.c and httptask.c. main.c
	 is the program entry point. It creates all the demo application tasks then starts the RTOS scheduler. httptask.c contains the simple http service.
3. In the project window (as per the image above), right click on the "RTOSDemo [.axe]" line, then select "Edit local options" from the pop up menu. The
 project options dialogue will be displayed, as shown below.
4. In the project options window, select the "Directories" topic, then edit the include and library path names to point be correct for your Paradigm C/C++
 installation (my installation being in the c:devtoolsparadigm directory as per the image below).

![](/media/2018/paraopts.gif)
5. Close the project options windows, then select "Build All" from the IDE's "Project" menu. The source should build and link with no errors or warnings.
6. Finally select "Run" from the IDE's "Debug" menu. The IDE should connect to the target board, download the executable, and start the application running.
 Note that when using this method the program is executing from RAM and will be lost should the target board be power cycled.
7. Open a web browser, and in the address bar type "http://192.168.0.23", replacing this IP address with that set by the ucIPAddress constant.

![](/media/2018/enterurl.gif)
Entering the IP address into the web browser
(obviously use the correct IP address for your system)

### Functionality

|  |  |
| --- | --- |
| <br />![](/media/2018/servedpage.jpg)<br /> | <br /><br /> The demo application creates twenty five tasks - consisting predominantly of the standard demo application tasks (see the <br />  [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).<br /> In addition a further four tasks are repeatedly dynamically created and deleted (by the standard "death" demo).<br /><br /> <br /><br /> When executing correctly the demo application will serve the web page shown on the left. The page will automatically refresh every second.<br /><br /> <br /><br /> The table lists each task under control of the RTOS scheduler, along with the tasks:<br /> * State (see the trace visualisation documentation page for a key).<br />* Priority<br />* The amount of unused stack space remaining (from the high water mark).<br />* The tasks number.<br /><br /><br /><br /> The count of the number of idle task execution loops originates from the [idle task hook](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task), which is defined in HTTPTask.c.<br /> <br /> The tick count should increment at the rate specified by the configTICK\_RATE\_HZ constant, defined in FreeRTOSConfig.h.<br /> <br /> Finally, main() also creates a "check" task. The check task monitors all the other tasks in the system. If the check task discovers a potential error in any<br /> other task a red error message will be displayed. If no errors have ever been detected "No errors detected" is displayed. This mechanism can be tested by<br /> removing the loopback connector on COM2, and in so doing deliberately generating an error.<br /> <br /> |

---

### Configuration and Usage Details
### Task status table

The table displayed on the served web page is interesting for demonstration purposes, but as it is necessary to leave the RTOS scheduler disabled for an extended
period during its creation it is not recommended for use in production applications.

### Interrupt service routines

For simplicity the RTOS scheduler context switching mechanism relies on the compiler generated interrupt service routine prologue and epilogue code. It is therefore
essential that each ISR that can cause a context switch has identical entry and exit code. As a result of this an ISR that can cause a context switch cannot
define any stack variables directly in the ISR function. A simple way around this is to have the top level ISR function call another lower level function, for
example:

```c

/* This is the lower level function called from the top level
ISR function. */
int iCalledFunction( void )
{
/* Variables can be declared here. */
int iSwitchRequired = false;

    /* ... ISR code goes here ... */

    /* Assume the ISR code necessitates a context switch. */
    iSwitchRequired = true;

    return iSwitchRequired;
}

/* This is the top level function in which variables cannot be
declared on the stack.  This is the function installed on the
vector. */
void __interrupt prvISRFunction( void )
{
/* Variables cannot be declared here! */

    /* Call the lower level function to do the work. */
    if( iCalledFunction() )
    {
        /* If the called function necessitates a context switch
        then call portEND_SWITCHING_ISR() immediately prior to
        exiting. */
        portEND_SWITCHING_ISR();
    }
}
```

This mechanism is demonstrated by the serial port and WIZnet drivers included in the E-Engine demo application.

Declaring variables used by the ISR as static would probably have the same effect.

Interrupt service routines that do not cause a context switch have no special requirements.

### i2Chip Driver

The i2chip driver included in the download is a slightly modified version of the driver supplied by Tern Inc (the modification being the inclusion of the
semaphore in the interrupt service routine used to unblock the HTTPTask). This driver was not written for a multitasking system and is therefore not
optimised for use with FreeRTOS.org. Efficiency gains could be obtained by:
* Selecting which interrupts should wake the HTTPTask, and which should not. Currently any event wakes the HTTPTask, even if there is no processing
 to be performed.
* Removing the polling of status bits within the driver code that is outside of the ISR, and instead using a more state machine orientated organisation
 between the ISR and task code.

### Floating point

The Borland floating point libraries are not reentrant and should not be used with the RTOS scheduler. Information on how to make them reentrant is fairly well documented,
information on which can be found on the web.

### RTOS port specific configuration

Configuration items specific to this port are contained in Source/Demo/WizNET\_DEMO\_TERN\_186/FreeRTOSConfig.h. The constants defined in this file can be
edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz
is useful for testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines BaseType\_t to be of type short (16 bits).

Note that vPortEndScheduler() has not been implemented.

The RTOS Tick interrupt uses timers 1 and 2. Using a fast tick rate will remove the requirement to prescale the timer, and therefore use only timer 2.

### Optimisation

The 'Global Register Allocation' optimisation option appears to break the code.
