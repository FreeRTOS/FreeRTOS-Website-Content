---
title: "Xilinx Microblaze Port on a Virtex-4 FPGA"
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

The port and demo documented on this page are now deprecated.
A link to the latest demo can be found
[here](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#XILINX).

The Microblaze port was developed using the [PowerPC & MicroBlaze Virtex-4 FX12 Edition Development Kit](http://www.xilinx.com/products/devkits/HW-V4-ML403-UNI-G.htm). This is a very comprehensive kit that
includes:

* An [ML403 development board](http://www.xilinx.com/products/boards/ml403/docs.htm) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).
* All the required hardware development tools.
* All the required software development tools (EDK and ISE).
* A JTAG interface.
* All the required cables.

Note: Check the license conditions of each development tool individually, some are open source,
some are for evaluation only, others are licensed annually.

The Microblaze port is intended to be as generic and widely applicable as possible. Therefore, even though the
ML403 is a comprehensive development platform (including Ethernet, USB, audio, etc.), the FreeRTOS kernel
places as little reliance as possible on hardware outside of the core FPGA component. The demo application that accompanies
the port is configured to execute entirely from BRAM and only makes use of a basic UART component.

**Note:** Xilinx have continued to work on both the Microblaze core and their own tool chain since the port presented on this page was originally created. Tyrel Newton has been
good enough to update the port to use V14.4 of the Xilinx tool chain, and [post the resultant modifications](http://interactive.freertos.org/entries/200807-up-to-date-gcc-microblaze-port)
to the FreeRTOS Interactive section of this site. Thanks Tyrel!

As downloaded this demo application does not demonstrate the use of co-routines. See the [co-routine documentation](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/14-Standard-demo-examples)
page for information on how co-routine functionality can be quickly added to this demonstration.

---

### IMPORTANT! Notes on using the [Microblaze soft processor core](http://www.xilinx.com/products/design_resources/proc_central/microblaze.htm) RTOS port

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

The Platform Studio/GCC demo application project for the Microblaze FreeRTOS port is called system.xmp and can be
located in the FreeRTOS/Demo/Microblaze directory.

The directory FreeRTOS/Demo/Microblaze/Serial contains a sample interrupt driven serial port driver for the basic UART
peripheral.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the Microblaze GCC RTOS port.

The demo application creates 23 of the standard demo application tasks, a 'Check' task, two Microblaze specific
test tasks and the idle task - 27 tasks in total.
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
* LEDs 1, 2 and 3 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED 1 being
 the slowest and LED 3 being the fastest.
* The LED above SW4 will flash each time a character is transmitted on the serial port.
* The LED above SW5 will flash each time a character is received and validated on the serial port.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 LED 0 is under control of the 'Check' task. Every three seconds the 'Check' task examines all the tasks in the
 system to ensure they are executing without error. It then toggles LED 0. If LED 0 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error. This mechanism can be tested by removing the loopback connector from the serial port
 (described above), and in doing so deliberately generating an error.

### Building and executing the demo application

As the Microblaze is a soft processor core the initial build will generate both the FPGA and software images. **This can be
a lengthy process!** Providing the hardware configuration is not altered, compilation and download cycles subsequent to
the initial build can be completed in a matter of seconds.

The Xilinx Platform Studio project is aware of the dependencies between each component of the build. If you attempt to download
a bitstream it will first check that all components of the bitstream are up to date, and if not ensure they are built in the
correct order. The easiest way of performing a complete build is therefore to simply click the 'Download' speed button
within the Platform Studio IDE:

1. Connect the ML403 development board to your host computer using the JTAG adaptor. If using the parallel port
 version then ensure to connect both the parallel connector and the PS/2 connector to your host.
2. Power up the ML403.
3. Open the Demo/Microblaze/system.xmp file within the Platform Studio IDE.
4. Click the Download speed button ![](/media/2018/downloadsb.gif).
5. If this is the first build - go and do something else for a while as the build will take some time.

The demo application will automatically start executing when the build and download procedure has completed.

The project is executed from the BRAM so will be lost if power is removed.

### Using the debugger

Once the FPGA has been programmed, software builds can be modified and executed using the Insight debugger:

1. Follow steps 1 to 4 as above in order to ready the development environment.
2. Start the XMD interface by clicking the XMD speed button ![](/media/2018/xmdsb.gif).
 This is necessary for the host debugger to communicate with the development board.
3. Build the software source files using the Build All User Applications speed button ![](/media/2018/buildsb.gif).
4. Start the Insight debugger using the Software Debugger speed button ![](/media/2018/debuggersb.gif).
5. From within the Insight IDE, select Target Settings from the File menu and ensure the configuration is as per the
 following image:![](/media/2018/xmdtarget.gif)
Insight target settings
6. Again from within the Insight IDE, select the Run speed button ![](/media/2018/runsb.gif).
7. Insight will connect to the target, download the executable, then execute to and break at the start of main(). From
 then on Insight can be used to step through the code and inspect system resources as normal.

---

### Configuration and Usage Details

### Hardware Components

With the aim of providing the minimum necessary, the build configuration includes only:
* A basic Microblaze configuration with no cache or floating point support, and no external memory interfaces.
* A debug module.
* The LED outputs required by the demo application.
* A basic UART (included in order to test the interrupt mechanisms).
* A single interrupt controller.
* A timer that is used to generate the RTOS tick.
* The necessary bus interfaces.

### Notes on the GCC project

1. The definition XILINX\_EDK\_DIR within Demo/MicroBlaze/System\_incl.make may require updating manually to ensure it contains
 the correct path to your xilinx/EDK directory.
2. I have found the tools will fail to build if the project is located in a directory path that contains a space (' ').

### RTOS port specific configuration

Configuration items specific to this port are contained in Source/Demo/MicroBlaze/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

### Interrupt service routines

The FreeRTOS kernel installs its own interrupt handler when the RTOS scheduler is started. This uses the same data structures
and indirection mechanism as the peripheral library and requires no special consideration.

An interrupt service routine that does not cause a context switch has no special requirements and can be written as a normal
function.

Often you will require an interrupt service routine to cause a context switch. For example a serial port character being
received may wake a high priority task that was blocked waiting for the character. If the ISR interrupted a lower priority
task then it should return immediately to the woken task. Placing a call to the macro portYIELD\_FROM\_ISR() at the end
of an interrupt function will ensure that the highest priority task that is able to run is the task executed immediately
upon leaving the interrupt function. See the function vSerialISR() within Demo/MicroBlaze/serial/serial.c for an example
of how portYIELD\_FROM\_ISR() can be used in conjunction with xQueueSendFromISR() and xQueueReceiveFromISR().

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/MicroBlaze/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the Microblaze demo application makefile to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimized solution.
**NOTE:** The baud rate used by the basic UART is fixed once the hardware image has been generated. The baud rate parameter
passed to the serial port initialisation routine has no effect. As downloaded, the baud rate is set to 9600.
