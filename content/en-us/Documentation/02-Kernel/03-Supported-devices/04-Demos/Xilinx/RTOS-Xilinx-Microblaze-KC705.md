---
title: "Xilinx MicroBlaze Port Demonstrated on a KC705 evaluation kit for the Kintex FPGA"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Xilinx KC705 Kintex FPGA evaluation kit](/media/2018/KC705_Kintex_FPGA.jpg)

This MicroBlaze demo was produced using Xilinx's
[Vivado Design Suite](http://www.xilinx.com/products/design-tools/vivado.html/),
supports version 8.x of the [MicroBlaze soft processor core](http://www.xilinx.com/tools/microblaze.htm),
and was developed and tested on a Kintex FPGA on a
[KC705 Evaluation Kit](http://www.xilinx.com/products/boards-and-kits/ek-k7-kc705-g.html) board.

The demo includes an embedded web server implementation that uses version 1.4.0
of the [lwIP TCP/IP stack](http://savannah.nongnu.org/projects/lwip/).
The web server's server side include (SSI) functionality is used to serve pages that include
dynamic task and run-time statistic information. Currently both FreeRTOS and lwIP
are built as part of the application (rather than part of the BSP).

---

### IMPORTANT! Notes on using the KC705 MicroBlaze RTOS demo

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organization)
2. [The Demo Application Functionality](#importing-the-demo-application-project-into-the-sdk-eclipse-workspace)
3. [Building and Running Instructions](#build-instructions)
	1. [Importing the projects into the SDK](#build-instructions)
	2. [Building the demo application](#building-the-demo-application)
	3. [Programming the Kintex FPGA](#programming-the-kintex-fpga)
	4. [Starting a Debug Session](#starting-a-debug-session)
4. [RTOS Configuration and Usage Details](#rtos-kernel-configuration-and-usage-details)
	1. [Callback functions that must be supplied by the application](#callback-functions-that-must-be-supplied-by-the-application)
	2. [Implementing an interrupt service routines (ISR)](#implementing-an-interrupt-service-routines-isr)
	3. [Context switching from an ISR](#context-switching-from-an-isr)
	4. [Installing and enabling an ISR](#installing-and-enabling-an-isr)
	5. [Exception handling (for advanced users only)](#exception-handling-for-advanced-users-only)
	6. [RTOS demo specific configuration](#rtos-port-specific-configuration)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports, and
every demo application. That means it contains many more files than are required
to use the MicroBlaze port, or the KC705 demo application.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section of this web site for a description of the downloaded files, and
information on creating a new project.

The directory structure used by the demo application is shown and described
below. The root MicroBlaze\_Kintex7\_EthernetLite directory is itself
located in /FreeRTOS/Demo.

```c

MicroBlaze_Kintex7_EthernetLite
    |
    +-RTOSDemo  Contains the SDK project and C files specific to the demo.
    |
    +-BSP       Contains the hardware BSP.
    |
    +-Hardware  Contains the hardware description.
```

**Note**:
The RTOSDemo directory only contains the source files that are specific
to the KC705 MicroBlaze demo. The RTOS source files, lwIP source files,
CLI source files, and the source files that
implement tasks that are common to all demo applications, are located
[elsewhere in the directory tree](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization).
The project may not build if the default directory structure
has been changed - including the /FreeRTOS-Plus directory (which contains
the CLI source files).

Also see the page that describes
[how to use virtual and linked paths in
the Eclipse project explorer](Project_Workspace_Relative_File_Paths_Eclipse).

---

The Xilinx MicroBlaze KC705### Demo Application

### Functionality

The constant mainSELECTED\_APPLICATION, which is #defined at the top
of main.c, is used to switch between a simply Blinky style demo, a more
comprehensive test and demo application, and an lwIP demo, as described in the
next three sections.

### Functionality with mainSELECTED\_APPLICATION set to 0

If mainSELECTED\_APPLICATION is set to 0 then main() will call
main\_blinky(), which is implemented in main\_blinky.c.

main\_blinky() creates a basic starter demo that creates two tasks and one queue.
One task uses the queue to periodically send the value 100 to the other task.
The receiving task toggles an LED each time the message is received. The message
is sent every 200 milliseconds, so the LED toggles every 200 milliseconds.

### Functionality with mainSELECTED\_APPLICATION set to 1

If mainSELECTED\_APPLICATION is set to 1 then main() will call main\_full(),
which is implemented in main\_full.c.

![Free RTOS running on Xilinx Microblaze](/media/2018/Microblaze_CLI.png)

**An example CLI session**

main\_full() creates a comprehensive test and demo application
that demonstrates:
* The [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 command line interface.
* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications).
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).

Connect to FreeRTOS-Plus-CLI though the USB connector marked "USB UART J6" on the KC705
board. The USB port will enumerate on the host computer as a COM port called
"Silicon Labs CP210x USB to UART bridge", which can then be connected to at 115200
baud using a dumb terminal such as Teraterm, or HyperTerminal. Type 'help' in
the CLI to see a list of the registered commands.

The majority of tasks created by the comprehensive demo are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. These are used by all FreeRTOS demo applications, and
have no specific functionality or purpose other than to demonstrate the FreeRTOS
API being used, and test the RTOS port.

The following tasks are created in addition to the standard demo tasks:

* Register test tasks

 These tasks test the RTOS kernel context switch mechanism by
 filling each MicroBlaze register
 with a known unique value, then repeatedly checking that the value
 originally written to the register is maintained for
 the lifetime of the task. The tasks execute at the idle priority, so are
 preempted regularly. The nature of
 these tasks necessitates that they are written in assembly.
* A 'check' task

 The check task periodically queries the standard demo tasks and the
 register test tasks to ensure they are functioning as expected. The
 check task also toggles LED 7 to give a visual indication of the system
 status.
 **If LED 7 toggles every 3 seconds then the check task has not found
 any problems with the demo. If LED 7 toggles every 200 milliseconds
 then the check task has discovered a [potential] problem in at least one
 task.**.

### Functionality with mainSELECTED\_APPLICATION set to 2

If mainSELECTED\_APPLICATION is set to 2 then main() will call main\_lwIP(),
which is implemented in main\_lwIP.c.

The lwIP example is configured to use a static IP address. The static IP
address is set by the constants configIP\_ADDR0 to configIP\_ADDR3
at the bottom of FreeRTOSConfig.h. Constants used to define
a netmask are also located at the bottom of FreeRTOSConfig.h. The
selected IP address and netmask must be compatible with the network to
which the MicroBlaze target is being connected. This can normally be achieved
by setting the first three octets of the target's IP address and netmask
to match the first three octets of the host computer's IP address and
netmask respectively. The chosen IP address must be unique on the network.

A cross over (point to point) Ethernet cable must be used if the target and
host systems are connected directly (without going through a hub or switch). A
standard Ethernet cable must be used if the target and host systems are connected
through a hub or switch.

When connected correctly the demo uses the lwIP sockets API to create
a FreeRTOS-Plus-CLI command console, and the lwIP raw API to create a
basic HTTP web server. Server side includes (SSI) are used to generate dynamic
data in the served web pages.
To connect to the http server simply type the IP address of the target into
the address bar of a web browser.

To connect to FreeRTOS-Plus-CLI, open a command prompt and enter `telnet <ipaddr>`
where `<ipaddr>` is the IP address of the target. Once connected type "help"
to see a list of registered commands. Note this example does not implement
a real telnet server, it just uses the telnet port number to allow easy
connection using telnet tools.

---

### Build Instructions

### Importing the demo application project into the SDK Eclipse workspace

To import the Xilinx Software Development Kit (SDK) project into an existing or new Eclipse Workspace:

1. Select "Import" from the SDK "File" menu. The dialogue box shown below
 will appear. Select General->Existing Project into Workspace, as shown in the image.

![Importing the Xilinx MicroBlaze RTOS demo project into the SDK](/media/2018/Importing-the-Xilinx-MicroBlaze-RTOS-demo-project-into-the-SDK.jpg)

**The dialogue box that appears when "Import" is first clicked**
2. In the next dialogue box, select /FreeRTOS/Demo/MicroBlaze\_Kintex7\_EthernetLite
 as the root directory. Then, make sure the RTOSDemo, BSP and
 Hardware projects are checked in the "Projects" area,
 **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states).

![Importing the free ARM Cortex-A9 RTOS Demo Source project into the Xilinx SDK](/media/2018/import_KC705_projects.png)

**Make sure all three projects are checked, and "Copy projects into workspace" is not checked**
3. Once all three projects have been imported, the project explorer window of the SDK IDE
 will appear as below.

 The Hardware and BSP projects are dependencies of the
 RTOSDemo project, so only the RTOSDemo project needs to be built explicitly.

![The MicroBlaze KC705 RTOS projects viewed in the Eclipse project explorer.](/media/2018/KC705_Project_Explorer.png)

**All three projects imported into the workspace**

### Building the demo application

1. Open the project's main.c file, and set mainSELECTED\_APPLICATION
 to generate the simple blinky demo, the full test and demo
 application, or the lwIP Ethernet example, as required.
2. Select 'Rebuild All' from the IDE's 'Project' menu. The application should
 build without any errors or warnings.

**Note:** At the time of writing there is a bug in
the dependency management in the SDK. If a header file is edited then it is necessary
to perform a complete clean and re-build of the entire project for the change to take effect. Failure
to do this will result in seemingly inexplicable run-time behaviour.

### Programming the Kintex FPGA

The Kintex FPGA must be programmed before the application can be downloaded to
the MicroBlaze softcore microcontroller. This step only needs to be performed
once on each power cycle.
1. Ensure the KC705 hardware is powered up and connected to the host
 computer using its JTAG USB connection.
2. Select 'Program FPGA' from the IDE's 'Xilinx Tools' menu. The
 Program FPGA window will appear.
3. Configure the Program FPGA window as shown below before clicking "Program".
 The base\_microblaze\_design\_wrappers files are located in the Hardware
 project within the workspace.

![programming the Kintex FPGA ready to run the RTOS demo on the MicroBlaze](/media/2018/programming-the-Kintex-FPGA.png)

**The configuration necessary to program the Kintex FPGA**

### Starting a debug session

1. Ensure the Kintex FPGA has been programmed as described above, and is
 still connected to the host computer using the hardware's JTAG USB
 connector.
2. Select 'Debug Configurations...' from the IDE's 'Run' menu. The
 Debug Configurations dialogue box will appear. Double click
 'Xilinx C/C++ application (System Debugger)' to create a new debug
 configuration. **Note**: Use the GDB option in place of the System Debugger
 option if you intend using the FreeRTOS kernel aware state viewer plug-in.
3. Configure the 'Target Setup' tab as shown in the image below.

![Kintex FPGA MicroBlaze RTOS target setup tab](/media/2018/Kintex_FPGA_Debug_Configuration.png)

**The required settings on the Target Setup tab**
4. Configure the 'Application' tab as shown in the image below.

![Kintex FPGA MicroBlaze RTOS application tab](/media/2018/Kintex_FPGA_Application_Tab.png)

**The required settings on the Application tab**

 All the other tabs in the 'Debug Configurations' dialogue can be left
 with their default settings.
5. Click the "Debug" button to commence debugging. The application will be
 downloaded to RAM and the debugger will break on entry to main().

---

### RTOS Kernel Configuration and Usage Details

### Callback functions that must be supplied by the application

* void vApplicationSetupTimerInterrupt( void );

 This is an application defined callback function used to install the tick
 interrupt handler. It is provided as an application callback, rather
 than being an integral part of the RTOS kernel port layer, because the RTOS kernel
 will run on lots of different MicroBlaze and FPGA configurations - not all of
 which will have the same timer peripherals defined or available.

 vApplicationSetupTimerInterrupt() must install the RTOS kernel defined
 function vPortTickISR() as the tick interrupt handler.

 The official demo application includes an example implementation of
 vApplicationSetupTimerInterrupt() in main.c.
 The example implementation uses the a Xilinx Timer/Counter as the
 tick interrupt source. If this peripheral is available on
 your hardware platform, then the example implementation can be used
 without modification.
* void vApplicationClearTimerInterrupt( void );

 This is an application defined callback function used to clear whichever
 interrupt was installed by the vApplicationSetupTimerInterrupt() callback
 function. It is
 provided as an application callback because the RTOS kernel will run on lots of
 different MicroBlaze and FPGA configurations - not all of which will have the
 same timer peripherals defined or available.

 The official demo application includes an example implementation of
 vApplicationClearTimerInterrupt() in main.c.
 The example implementation complements the example implementation
 of vApplicationSetupTimerInterrupt() found in the same files by
 clearing the interrupt generated by the Xilinx Timer/Counter peripheral.
 If your application does not modify the provided example implementation
 of vApplicationSetupTimerInterrupt(), then the provided example
 implementation of vApplicationClearTimerInterrupt() can also be used
 without any modification.

### Implementing an interrupt service routines (ISR)

Functions that implement ISRs are normal C functions, but must conform to the following
prototype.

```c

void ISRFunctionName( void *ISRParameter );
```

### Context switching from an ISR

It is common for an ISR to cause a task to leave the Blocked
state. For example, consider the case where a task processes data that arrives
on a queue. When the queue is empty, there is no data to process, and the task
might opt to enter the Blocked state to wait for more data to become available.
If an ISR then sends data to the queue, the task would
automatically leave the Blocked state as the queue would no longer be empty.

If an ISR causes a task to leave the Blocked state, and
the task that leaves the Blocked state has a priority that is higher than or
equal to the currently executing task (the task that was interrupted), then a
context switch should be performed in the ISR to ensure
the ISR returns directly to the newly unblocked, higher
priority task. The ISR will have interrupted one task, but
returned to another.

The macro portYIELD\_FROM\_ISR() is an interrupt safe version of taskYIELD(). It
takes a single parameter that, if none zero, will indirectly cause a context
switch to occur. Below is an example use of portYIELD\_FROM\_ISR(), which is taken
from the file serial.c in the official demo application:

```c

/* Note that this function is called from the UART interrupt handler, it is not
itself an interrupt handler, so its prototype does not have to match that
required by all interrupt handlers. */
static void prvRxHandler( void *pvUnused, UBaseType_t uxByteCount )
{
signed char cRxedChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* While there are characters to process. */
    while( XUartLite_IsReceiveEmpty( xUartLiteInstance.RegBaseAddress ) == pdFALSE )
    {
        /* Obtain the next character. */
        cRxedChar = XUartLite_ReadReg( xUartLiteInstance.RegBaseAddress,
                                       XUL_RX_FIFO_OFFSET);

        /* Place the received character in the received queue. If writing to the
 queue causes a task to leave the Blocked state, and the task has a
 priority equal to or above the priority of the interrupted task, then
 xHigherPriorityTaskWoken will automatically get set to pdTRUE inside the
 xQueueSendFromISR() function itself. */
        xQueueSendFromISR( xRxedChars, &cRxedChar, &xHigherPriorityTaskWoken );
    }

    /* Call portYIELD\_FROM\_ISR(), passing in xHigherPriorityTaskWoken. If
 xHigherPriorityTaskWoken was set to pdTRUE inside xQueueSendFromISR(), then
 calling portYIELD\_FROM\_ISR() here will cause the ISR
 to return directly to the newly unblocked task. If xHigherPriorityTaskWoken
 has retained its initialised value of pdFALSE, then calling
 portYIELD\_FROM\_ISR() here will have no effect. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```

### Installing and enabling an ISR

The following functions are provided for installing, enabling and disabling
interrupts (in the interrupt controller) respectively. The Xilinx BSP library
functions that have similar functionality must **not** be used.

An example of how to use these functions is contained in the implementation of
vApplicationSetupTimerInterrupt(), which is contained in main.c.

```c

/*
 * Installs pxHandler as the interrupt handler for the peripheral specified by
 * the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have pxHandler assigned as its interrupt
 * handler. Peripheral IDs are defined in the xparameters.h header file, which
 * is itself part of the BSP project. For example, in the official demo
 * application for this port, xparameters.h defines the following IDs for the
 * three possible interrupt sources:
 *
 * XPAR\_INTC\_0\_TMRCTR\_0\_VEC\_ID - for the Xilinx timer
 * XPAR\_INTC\_0\_UARTLITE\_0\_VEC\_ID - for the UART
 * XPAR\_INTC\_0\_EMACLITE\_0\_VEC\_ID - for the Ethernet controller
 *
 *
 * pxHandler:
 *
 * A pointer to the interrupt handler function itself. This must be a void
 * function that takes a (void *) parameter.
 *
 *
 * pvCallBackRef:
 *
 * The parameter passed into the handler function. In many cases this will not
 * be used and can be NULL. Some times it is used to pass in a reference to
 * the peripheral instance variable, so it can be accessed from inside the
 * handler function.
 *
 *
 * pdPASS is returned if the function executes successfully. Any other value
 * being returned indicates that the function did not execute correctly.
 */
BaseType_t xPortInstallInterruptHandler( unsigned char ucInterruptID,
                           XInterruptHandler pxHandler, void *pvCallBackRef );

/*
 * Enables the interrupt, within the interrupt controller, for the peripheral
 * specified by the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have its interrupt enabled in the
 * interrupt controller. Peripheral IDs are defined in the xparameters.h header
 * file, which is itself part of the BSP project. For example, in the official
 * demo application for this port, xparameters.h defines the following IDs for
 * the three possible interrupt sources:
 *
 * XPAR\_INTC\_0\_TMRCTR\_0\_VEC\_ID - for the Xilinx timer
 * XPAR\_INTC\_0\_UARTLITE\_0\_VEC\_ID - for the UART
 * XPAR\_INTC\_0\_EMACLITE\_0\_VEC\_ID - for the Ethernet controller
 *
 */
void vPortEnableInterrupt( unsigned char ucInterruptID );

/*
 * Disables the interrupt, within the interrupt controller, for the peripheral
 * specified by the ucInterruptID parameter.
 *
 * ucInterruptID:
 *
 * The ID of the peripheral that will have its interrupt disabled in the
 * interrupt controller. Peripheral IDs are defined in the xparameters.h header
 * file, which is itself part of the BSP project. For example, in the official
 * demo application for this port, xparameters.h defines the following IDs for
 * the three possible interrupt sources:
 *
 * XPAR\_INTC\_0\_TMRCTR\_0\_VEC\_ID - for the Xilinx timer
 * XPAR\_INTC\_0\_UARTLITE\_0\_VEC\_ID - for the UART
 * XPAR\_INTC\_0\_EMACLITE\_0\_VEC\_ID - for the Ethernet controller
 *
 */
void vPortDisableInterrupt( unsigned char ucInterruptID );
```

### Exception handling (for advanced users only)

To enable FreeRTOS exception handling, first the MicroBlaze itself must be
configured to include exception handling functionality, and second
configINSTALL\_EXCEPTION\_HANDLERS must be set to 1 in FreeRTOSConfig.h.
Setting configINSTALL\_EXCEPTION\_HANDLERS to 1 will cause both the code and
data space consumed by the RTOS kernel to increase.

The following functions are provided to install the FreeRTOS exception handler,
and process an exception when it occurs, respectively. The functionality of
the FreeRTOS exception handler itself is described in the comments above the
function prototypes found in portmacro.h, and replicated below.

An example implementation of vApplicationExceptionRegisterDump() is provided
in both main-full.c and main-blinky.c.

```c

/*
 * vPortExceptionsInstallHandlers() is only available when the MicroBlaze
 * is configured to include exception functionality, and
 * configINSTALL\_EXCEPTION\_HANDLERS is set to 1 in FreeRTOSConfig.h.
 *
 * vPortExceptionsInstallHandlers() installs the FreeRTOS exception handler
 * for every possible exception cause.
 *
 * vPortExceptionsInstallHandlers() can be called explicitly from application
 * code. After that is done, the default FreeRTOS exception handler that will
 * have been installed can be replaced for any specific exception cause by using
 * the standard Xilinx library function microblaze\_register\_exception\_handler().
 *
 * If vPortExceptionsInstallHandlers() is not called explicitly by the
 * application, it will be called automatically by the RTOS kernel the first time
 * xPortInstallInterruptHandler() is called. At that time, any exception
 * handlers that may have already been installed will be replaced.
 *
 * See the description of vApplicationExceptionRegisterDump() for information
 * on the processing performed by the FreeRTOS exception handler.
 */
void vPortExceptionsInstallHandlers( void );

/*
 * The FreeRTOS exception handler fills an xPortRegisterDump structure (defined
 * in portmacro.h) with the MicroBlaze context, as it was at the time the
 * exception occurred. The exception handler then calls
 * vApplicationExceptionRegisterDump(), passing in a reference to the completed
 * xPortRegisterDump structure as its parameter.
 *
 * The FreeRTOS kernel provides its own implementation of
 * vApplicationExceptionRegisterDump(), but the RTOS kernel provided implementation
 * is declared as being 'weak'. The weak definition allows the application
 * writer to provide their own implementation, should they wish to use the
 * register dump information. For example, an implementation could be provided
 * that writes the register dump data to a display, or a UART port.
 */
void vApplicationExceptionRegisterDump( xPortRegisterDump *xRegisterDump );
```

### RTOS port specific configuration

The RTOS kernel and demo behaviour can be customised using the configuration constants
contained in the file FreeRTOS/Demo/MicroBlaze\_Kintex7\_EthernetLite/RTOSDemo/src/FreeRTOSConfig.h.
The majority these configuration constants are used for all FreeRTOS ports, and are
described on the [Customisation](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
page of this web site, and in the [FreeRTOS Reference Manual](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book).

The following constants are specific to this port:

```c

/* If configINSTALL\_EXCEPTION\_HANDLERS is set to 1, then the RTOS kernel will
automatically install its own exception handlers before the RTOS kernel is started,
if the application writer has not already caused them to be installed using the
vPortExceptionsInstallHandlers() API function. vPortExceptionsInstallHandlers()
is described on this web page. */
#define configINSTALL_EXCEPTION_HANDLERS 1

/* configINTERRUPT\_CONTROLLER\_TO\_USE must be set to the ID of the interrupt
controller that is going to be used directly by FreeRTOS itself. Most hardware
designs will only include on interrupt controller, so can use the same setting
as shown here. XPAR\_INTC\_SINGLE\_DEVICE\_ID is itself defined in the xparameters.h
header file, which is part of the Xilinx BSP library project. */
#define configINTERRUPT_CONTROLLER_TO_USE XPAR_INTC_SINGLE_DEVICE_ID
```
