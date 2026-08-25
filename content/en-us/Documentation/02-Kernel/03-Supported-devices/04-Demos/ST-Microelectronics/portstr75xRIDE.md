---
title: "ST Microelectronics STR75x Port for the GCC based Raisonance RIDE ARM Development Tools"
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
| <br />![](/media/2018/str750.jpg)STR750 Evaluation Board<br /> |

This STR750 ARM7 demo application is pre-configured for execution on the [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) evaluation
board from [ST Microelectronics](http://www.st.com/) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).

The RTOS port and demo application presented on this page require the Raisonance RIDE
IDE interface to the [GNUARM GCC toolchain](http://www.gnuarm.org/). An RLink In-circuit debugger and programmer
is required to program the microcontroller flash directly from the RIDE IDE.

The processor peripheral library provided by ST was used to facilitate development.

---

#### *IMPORTANT! Notes on using the STR750 GCC ARM RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by the
STR750 port or demo application.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the directory structure
and information on creating a new project.

The demo RIDE project included for the STR75x GCC ARM7 port is called RTOSDemo.prj and can be found in the Demo/ARM7\_STR75x\_GCC directory.
This file should be opened directly from within the RIDE IDE.

The Demo/ARM7\_STR75x\_GCC/ST library directory contains the components of the ST peripheral library that are used by the
demo application.

---

### The Demo Application

The demo application is configured to create 22 fully preemptive tasks.

#### Demo application hardware setup

JP13 must be removed from the STR75x-EVAL board prior to using the RLink JTAG interface.

The standard 'ComTest' tasks send and receive characters on UART0. The characters sent by one task
need to be received by the another - an error being flagged if a character is received out of sequence or missed all together. A
loopback connector is required on UART0 of the evaluation board for this functionality to operate (simply connect pins 2 and 3 together on
the serial port connector labelled CN4).

The demo application utilises the LEDs built onto the evaluation board so no further hardware setup is required.

#### The RIDE project

![](/media/2018/str750ride.gif)
The RIDE demo application project

The project contains 4 folders:

1. **Demo Source**

 Contains the source files for the demo application.
2. **Library Source**

 Contains the components of the ST peripheral library that are utilised by the RTOS kernel and the demo application.
3. **RTOS Source**

 Contains the source files for the FreeRTOS real time kernel.
4. **System Files**

 Contains the startup code and interrupt vector table definition.
IMPORTANT NOTE: The startup files and linker scripts utilised by this project have been modified from those contained in the
 Raisonance RIDE distribution. Only the files contained in the Demo/ARM7\_STR75X\_GCC/SystemFiles directory should be used.

#### Building the demo application - THUMB mode

The project in the FreeRTOS download has been preconfigured to use THUMB mode. To build the project to use THUMB mode simply select 'Build all' from the RIDE
'Project' menu.

The two files serialISR.c and portISR.c
contain interrupt service routines and therefore must be compiled into ARM mode. All other files will be compiled into THUMB mode.

IMPORTANT NOTE:
To achieve this the project options applied to serialISR.c and portISR.c are different from those applied to all other files. If you edit the global project options (using the
'Options' | 'Project' menu option) then the special options applied to these two files will be lost and must be reset manually. Failure to do this will *prevent the project from building*.

To ensure portISR.c and serialISR.c are compiled into ARM mode:

1. Right click on the file within the project workspace, a pop up menu will appear.
2. From the pop up menu, select 'Options', then 'Local Options'.![](/media/2018/ridelocaloptions.gif)
Setting the local options of
 a file
3. From the pop up window select 'ARM Specific Options', and ensure 'Generate THUMB Code' is not selected.![](/media/2018/ridespecificoptions.gif)

 Ensuring ARM code is generated for this file

#### Building the demo application - ARM mode

The following modifications to the project options will cause all the files to use ARM mode:

	1. Open the project options dialogue, and select 'Defines'. Remove the definition 'THUMB\_INTERWORK', leaving STR75X\_GCC as the only definition remaining.

	![](/media/2018/ridearmbuild1.gif)
	Deleting the THUMB\_INTERWORK definition.
	2. In the same project options dialogue, select 'ARM Specific Options', and ensure 'Generate THUMB Code' is not selected. Note this time we are setting the global project options, not options local to a single file
	 as described previously.![](/media/2018/ridespecificoptions.gif)

	 Ensuring ARM code is generated for this project.

Select 'Build all' from the RIDE 'Project' menu to rebuild the entire project into ARM code.

#### Programming the STR750 FLASH and starting the debugger

	1. Ensure the RLink JTAG interface is correctly connected to the STR75x-EVAL.
	2. Apply power to the target board.
	3. Ensure the Debug options are configured as depicted below.![](/media/2018/ridedebugoptions.gif)
	Debug interface options
	- Select 'Start rtosdemo.elf' from the RIDE 'Debug' menu.

### Functionality

	The demo application creates 19 of the [standard demo tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview), a 'check' task, a 'print' task
	and the idle task.

	The 'print' task is the LCD 'gatekeeper'. That is, it is the only task that should access the LCD directly so is always guaranteed exclusive (and
	therefore consistent) access. The print task simply blocks on a queue to wait for messages from other tasks that wish to display text on the LCD.
	An arriving message unblocks the task, which writes the message contents to the LCD, before blocking once again. This functionality is included for demonstration
	purposes even though in this application there is actually only one task that generates display text.

	The 'check' task is responsible for ensuring that all the standard demo tasks are executing as expected. It only executes every three seconds, but
	has the highest priority within the system so is guaranteed to get execution time. Any errors discovered by the check task are latched until the
	processor is reset. At the end of each cycle the check task sends either a pass or fail message to the 'print' task for display on the LCD.

	When executing correctly the demo application will behave as follows:

		* The LEDs LD2 to LD4 are under control of the 'flash' tasks.
		 Each will flash at a constant frequency, with LD2 being the fastest and LD4 being the slowest.
		* The LED LD5 is under control of the standard ComTest Tx task. Its state will toggle each time
		 the ComTest Tx task transmits a character over the RS232 port.
		* Most of the standard demo tasks do not update an LED so have no visible indication that they are operating correctly, and are therefore
		 monitored by the 'check' task.

		 "Pass" being displayed on the LCD indicates that the check task has never detected an error occurring in any task. The position of the
		 text is shifted slightly each time it is displayed to provide a visual indication that the check task itself is still executing.
		 The error detection mechanism can be tested by removing the loopback connector from the serial port while the demo is running, following
		 which the "Pass" message should change to "Fail".

	---

### Configuration and Usage Details

#### RTOS port specific configuration

	Configuration items specific to this port are contained in Demo/ARM7\_STR75x\_GCC/FreeRTOSConfig.h. The constants
	defined in this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to
	set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is
	faster than most applications require. Lowering this value will improve efficiency.

	Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
	BaseType\_t to be of type long.

	Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

	The STR75x demo saves and restores the task context automatically prior to calling the user defined interrupt service routine C code. This is
	contrary to the STR71x port, where the context is saved and restored within the C code via the FreeRTOS provided
	macros. This alternative method is provided for demonstration purposes. It has the advantage of simplified syntax from a users perspective, but the
	disadvantage of slightly longer execution time for those interrupts in which a context switch is not performed.

	An interrupt service routine must be written as an ARM mode C function.
	For example:

	```c

	    void vAnISR( void )
	    {
	        /* ISR C code goes here. */

	        /* Clear the interrupt within the peripheral here. */
	    }
	```

	Often you will require an interrupt service routine to cause a context switch. For example a serial port character being
	received may wake a high priority task that was blocked waiting for the character. If the ISR interrupted a lower priority
	task then it should return immediately to the woken task. This can be performed by simply calling the macro portEND\_SWITCHING\_ISR() from
	within the service routine, as demonstrated below:

	```c

	    void vAnISR( void )
	    {
	        /* ISR C code goes here. */

	        /* Clear the interrupt within the peripheral here. */

	        /* Pass in true to cause a context switch, or false to return
	        to the interrupted task. */
	        portEND_SWITCHING_ISR( pdTRUE );
	    }
	```

	See the function vSerialISR() within Demo/ARM7\_STR75x\_GCC/serial/serialISR.c for a complete example.

	User defined interrupt routines must replace the ST provided stubs within Demo/ARM7\_STR75x\_GCC/SystemFiles/ctr0\_str75x\_FreeRTOS.s.

#### Switching between the pre-emptive and co-operative RTOS kernels

	Set the definition configUSE\_PREEMPTION within Demo/ARM7\_STR75x\_GCC/FreeRTOSConfig.h to 1 to use pre-emption or 0
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

	The stack size of each necessary operating mode is configured using constants defined within Demo/ARM7\_STR75x\_GCC/SystemFiles/STR75x\_COMMON\_FreeRTOS.ld. It is not necessary to
	configure a stack for User/System mode.

	SWI instructions are used by the real time kernel and can therefore not be used by the application code.

#### Memory allocation

	Source/Portable/MemMang/heap\_1.c is included in the ARM7 demo application project to provide the memory allocation
	required by the real time kernel.
	Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
	full information.

#### Serial port driver

	It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
	intended to represent an optimised solution. In particular they do not make use of the FIFO.

#### Tick Interrupt

	The Time Base (TB) peripheral is used to generate the tick interrupt.
