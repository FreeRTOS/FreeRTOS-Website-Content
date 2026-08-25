---
title: "Xilinx PowerPC (PPC405) Port on a Virtex-4 FPGA"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ml403.jpg](/media/2018/ml403.jpg)
Image reproduced with permission of Xilinx Inc

The PPC405 port was developed using the [PowerPC & MicroBlaze Virtex-4 Embedded Development Kit](http://www.xilinx.com/products/devkits/DO-ML403-EDK-ISE-USB-UNI-G.htm). This is a very comprehensive kit that
includes:

* An [ML403 development board](http://www.xilinx.com/products/boards/ml403/docs.htm) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).
* All the required hardware development tools.
* All the required software development tools (EDK and ISE).
* A JTAG interface.
* All the required cables.

From FreeRTOS V5.0.2 two PowerPC projects are provided - the original project and an alternative that includes the optional floating point unit (FPU).
The [Configuration and Usage Details](#configuration-and-usage-details) of this page provides further information on using the FPU.

---

### IMPORTANT! Notes on using the Virtex4 PowerPC RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than used by this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The Platform Studio/GCC demo application project for the PowerPC without the FPU is called system.xmp and can be
located in the FreeRTOS/Demo/PPC405\_Xilinx\_Virtex4\_GCC directory. The alternative demo that uses the FPU
is located in the FreeRTOS/Demo/PPC405\_FPU\_Xilinx\_Virtex4\_GCC directory.

The directory FreeRTOS/Demo/PPC405\_Xilinx\_Virtex4\_GCC/RTOSDemo/Serial contains a sample interrupt driven serial port driver for the basic UART
peripheral.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the Virtex4 PPC405 RTOS port.

The demo application creates 40 static real time tasks and then dynamically creates and deletes another two. Most of these
tasks are not specific to the PPC405/Virtex4 application. In addition to the standard demo tasks, the follow demo specific tasks are created:

* The "Check" task.

 This only executes every three seconds but has the highest priority so is guaranteed to get processor time. Its main function
 is to check that all the other tasks are still operational.

 Most tasks maintain a unique count that is incremented each time the task successfully completes its function. Should any
 error occur within such a task the count is permanently halted. The check task inspects the count of each task to ensure
 it has changed since the last time the check task executed. If all the count variables have changed all the tasks are still
 executing error free. The check task then toggles LED DS15. If no errors have ever been detected then the toggle period
 will be 3 seconds. Should any task have ever reported an error the toggle period will be 500 milliseconds.
* The "Register Check" tasks.

 These tasks fill the CPU registers with known values, then check that each register still contains the expected value. The
 discovery of an unexpected value is indicative of an error in the RTOS context switch mechanism. The register check tasks operate
 at low priority so are preempted regularly.
* Optional floating point tasks.

 The alternative project that includes the FPU also creates register check tasks that test the floating point register context switching,
 along with a set of 8 tasks to test and demonstrate the use of floating point operations.

The [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section of this site provides more information on the
function of the standard demo tasks.

### Demo application hardware setup

All the ML403 jumpers can remain in their default positions.

The demo application includes the ComTest tasks - where one task transmits RS232 characters to another. For correct operation
of this real time task a loopback connector must be fitted to the RS232 port of the ML403 prototyping board (pins 2 and 3
must be connected together on the 9Way connector).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

### Functionality

When executing correctly the demo application will behave as follows:
* LEDs DS6, DS5 and DS4 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED DS6 being
 the fastest and DS4 being the slowest.
* The LED above SW4 will flash each time a character is received and validated on the serial port. The LED above SW5 will
 flash each time a character is transmitted on the serial port (the toggle rate is rapid and not too easy to see).
* LED DS15 is under control of the 'Check' task. If LED DS15 is toggling every three seconds then no errors have ever been
 detected. The toggle rate increasing to 500ms indicates that the 'Check' task has discovered at least one error. This
 mechanism can be tested by removing the loopback connector from the serial port (described above), and in doing so deliberately
 generating an error.

### Generating and downloading the bitstream

The Xilinx Platform Studio project is aware of the dependencies between each component of the build. If you attempt to download
a bitstream it will first check that all components of the bitstream are up to date, and if not ensure they are built in the correct
order. The easiest way of performing a complete build is therefore to select "Download Bitstream" from the Platform Studios
"Device Configuration" menu:
1. Connect the ML403 development board to your host computer using the JTAG adaptor. If using the parallel port version then ensure
 to connect both the parallel connector and the PS/2 connector to your host.
2. Power up the ML403.
3. Open the Demo/ PPC405\_Xilinx\_Virtex4\_GCC/system.xmp file within the Platform Studio IDE.
4. Select "Download Bitstream" from the Platform Studios "Device Configuration". The initial build will take somewhere between 10
 minutes and 30 minutes depending on the host PC, and once complete should be downloaded to the ML403.

The project is executed from RAM so will be lost if power is removed.

### Building the demo application

To build the demo application, right click on the project within the Platform Studio "Applications" window and then select
"Build Project" from the resultant pop up menu.

![](/media/2018/building-PowerPC-project.jpg)
Using the pop-up menu to build the PowerPC demo application.

**NOTE**: The file system\_incl.make contains the line "XILINX\_EDK\_DIR = C:/devtools/XilinxEDK". It might be necessary to update this file
to be correct for your Xilinx tool installation prior to building the RTOSDemo application.

### Using the debugger

Once the FPGA has been programmed, software builds can be modified and executed using the Insight debugger:

1. Follow the steps above in order to build the application and ready the development environment.
2. Start the XMD interface by clicking the XMD speed button ![](/media/2018/xmdsb.gif), or by selecting "Launch XMD" from the Platform Studio "Debug" menu.
 This is necessary for the host debugger to communicate with the development board.
3. Start the Insight debugger using the Software Debugger speed button ![](/media/2018/debuggersb.gif), or by selecting "Launch Software Debugger" from the Platform Studio "Debug" menu.
4. From within the Insight IDE, select Target Settings from the File menu and ensure the configuration is as per the
 following image:![](/media/2018/xmdtarget.gif)
Insight target settings
5. Again from within the Insight IDE, select the Run speed button ![](/media/2018/runsb.gif).
6. Insight will connect to the target, download the executable, then execute to and break at the start of main(). From
 then on Insight can be used to step through the code and inspect system resources as normal.

---

### Configuration and Usage Details

### Notes on the GCC project

1. The definition XILINX\_EDK\_DIR within Demo/MicroBlaze/System\_incl.make may require updating manually to ensure it contains
 the correct path to your xilinx/EDK directory.
2. I have found the tools will fail to build if the project is located in a directory path that contains a space (' ').

### Initialising the interrupt controller

vPortSetupInterruptController() must be called prior to either the installation of any interrupt
service routines or vTaskStartScheduler() being called. The demo application called vPortSetupInterruptController()
as the first line within main(). vPortSetupInterruptController() has the following prototype:

```c
void vPortSetupInterruptController( void );
```

It is assumed that, as per the demo application, one interrupt controller is being used.

### Installing an interrupt handler

Interrupt handlers should be installed using xPortInstallInterruptHandler(). The source file serial.c includes an example usage of the function.
xPortInstallInterruptHandler() has the following prototype:

```c

BaseType_t xPortInstallInterruptHandler( unsigned char ucInterruptID,
                                            XInterruptHandler pxHandler,
                                            void *pvCallBackRef );
```

Where:
* ucInterruptID is the ID assigned to the peripheral within the Xilinx generated "xparameters.h" header file.
 For example, in the RTOS demo application the ID XPAR\_OPB\_INTC\_0\_RS232\_UART\_INTERRUPT\_INTR is assigned to the UART.
* pxHandler is a pointer to a C interrupt handler function.
* pvCallBackRef is a pointer to the parameter that will be passed into the C interrupt handler function.
 Interrupt handler functions must accept a single void * parameter - even if this parameter is not used.
 The function vSerialISR() within serial.c can be used as an example.

### Maths libraries

The (emulated floating point) maths libraries supplied with GCC are not re-entrant and must not be used without taking appropriate mutual exclusion precautions.
It is preferable therefore to make use of the floating point unit as described below.

### Project settings required in order to use the APU FPU

The example project within the FreeRTOS/Demo/PPC405\_FPU\_Xilinx\_Virtex4\_GCC directory is provided completely configured
for floating point operation. These are the relevant settings:

* configUSE\_FPU is set to 1 within FreeRTOSConfig.h.
* configUSE\_APPLICATION\_TASK\_TAG is set to 1 within FreeRTOSConfig.h.
* FreeRTOSConfig.h contains the line #include "FPU\_Macros.h". FPU\_Macros.h contains the required traceTASK\_SWITCHED\_IN() and
 traceTASK\_SWITCHED\_OUT() definitions. The include file ordering is critical - including FPU\_Macros.h from within FreeRTOSConfig.h
 ensures the order is correct.
* Incorporating the APU FPU into your FPGA design should automatically set the compiler options to be correct for hardware as
 opposed to emulated floating point operation, "-mfpu=sp\_full" being the required option.

### Specifying that a task uses floating point operations

The best way to familiarize yourself with the floating point requirements is to view the examples provided within
FreeRTOSRTOS/Demo/PPC405\_FPU\_Xilinx\_Virtex4\_GCC/RTOSDemo/flop/flop.c and FreeRTOS/Demo/PPC405\_FPU\_Xilinx\_Virtex4\_GCC/RTOSDemo/flop/flop-reg-test.c.
This sub-section provides a brief explanation of the code.

Associated with each task is a tag value. This is not used by the RTOS kernel itself so can be used by either the port layer or the
application for any purpose it wishes. The port described by this page uses the tag value to indicate whether or not the task
requires a floating point context. The traceTASK\_SWITCHED\_OUT() and traceTASK\_SWITCHED\_IN() macros are defined to perform the
actual context saving and restoring respectively.

The tag value must either be NULL or point to a buffer that is large enough to hold the floating point context. NULL is the default
when a task is created and indicates that the task does not require a floating point context.

The function:

void vTaskSetApplicationTaskTag( TaskHandle\_t xTask, TaskHookFunction\_t pxTagValue );

is used to associate a tag value of pxTagValue with the task whose handle is equal to xTask.
The constant portNO\_FLOP\_REGISTERS\_TO\_SAVE indicates how many 32bit registers make up the floating point context.
As an example, a buffer large enough to hold the floating point context can be allocated using:

unsigned long ulFlopContext[ portNO\_FLOP\_REGISTERS\_TO\_SAVE ];

This buffer can then be assigned to the tag value of a task using the following call:

vTaskSetApplicationTaskTag( xTask, ( void * ) ulFlopContext );

Again, please refer to the provided examples.

### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/PPC405\_Xilinx\_Virtex4\_GCC/RTOSDemo/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Requesting a context switch within an ISR

The macro portYIELD\_FROM\_ISR() can be called from within an ISR to request that a new task be selected to run prior to the ISR terminating.
This would normally be done where the ISR caused a task to unblock - and the unblocked task has a priority higher than the currently
executing task.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/MicroBlaze/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the PowerPC demo application to provide the memory
allocation required by the RTOS kernel.
This is a very basic scheme that allocates memory blocks from a large array. The size of the array is set by the constant configTOTAL\_HEAP\_SIZE within FreeRTOSConfig.h.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

### Serial port driver

It should also be noted that the serial port driver is written to demonstrate and test some of the real time kernel features - and is not intended to represent an optimized solution.
**NOTE:** The baud rate used by the basic UART is fixed once the hardware image has been generated. The baud rate parameter
passed to the serial port initialisation routine has no effect.
