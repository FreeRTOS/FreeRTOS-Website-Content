---
title: "Microchip PIC18 Port using wizC or fedC"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

*The PICmicro wizC port and this documentation page were kindly provided by Marcel van Lieshout.*

The port is created using the
 wizC Integrated Development Environment from
 [Forest Electronic Developments](http://www.fored.co.uk/). The port can also be used
 with the FED C-compiler, also from
 Forest Electronic Developments. The difference between
 these two environments is the absence in fedC of the Rapid Application Development front end.
 This front end, however, is not used with this port. The port has been successfully tested using version 11 (min. 11.04c)
 and version 12 (min 12.02e) of wizC and fedC.

Initially, the port and the demo applications were developed completely using only the wizC simulator. Hardware tests
 on real silicon did not start until all simulations ran without any problem. The final hardware tests turned out
 to be nothing more than a verification: All tests ran successfully on the
 [PIC18F4620](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1335&dDocName=en010304).

WizC and fedC are not free or open source products, but they do offer a very good price/performance. WizC
 professional also comes in a lite edition with attractive advantages for educational use.

The FreeRTOS source code download includes a comprehensive set of demo applications for the wizC/PIC18 port which
 are primarily designed to test the reliability and demonstrate the capabilities of this port.

---

#### IMPORTANT! Notes on the Microchip PIC18 wizC/fedC RTOS port

*Please read all the following points before using this RTOS port.*
1. [Source Code Organisation](#source-code-organisation)
2. [Notes on using the wizC or fedC IDE](#notes-on-using-freertos-with-wizc-or-fedc)
3. [The Demo Applications](#the-demo-applications)
4. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

 The FreeRTOS source code download contains the source code for all the FreeRTOS ports.
 See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description
 of the downloaded files and information on creating a new project.

 The Microchip PIC18 wizC/fedC port can be found in the FreeRTOS/Source/portable/WizC/PIC18
 directory. In this directory you will find an installation script (install.bat). Please read the notes below
 before running this script.

Unlike the RTOS demo applications supplied with the other ports, the demo for this port is split into
 several smaller programs. This enables the demo's to be executed on the RAM challenged PIC18 devices.
 The demo applications can be found in the FreeRTOS/Demo/PIC18\_WizC directory. Every application
 has its own subdirectory. To load a demo-application into the IDE, double click the project file (eg. Demo1.pc).

---

### Notes on using FreeRTOS with wizC or fedC

1. **Additional fedC or wizC libraries may need to be installed**
FedC/wizC version 11: These libraries can be found in the directory Libraries/LibExt
 on the fedCwizC CD. Follow the directions in the pdf-file that comes with the libraries:
 Running the setup is not all, some changes have to be made in the IDE. Especially mem.c must be
 added as a library to the "16 Bit Core" tab in the IDE File/Libraries menu.

 FedC/wizC version 12: The libraries are already installed and ready to use.
2. **Malloc library needs to be installed**
The port needs the malloc-library that is freely available from the
 [user page](http://www.fored.co.uk/html/user_page.html)
 on the [Forest Electronic Developments](http://www.fored.co.uk/) website.
 The download file comes with its own installation instructions and documentation.
3. **ANSI header files needs to be installed**
The port needs the ANSI header files that are freely available from the
 [user page](http://www.fored.co.uk/html/user_page.html)
 on the [Forest Electronic Developments](http://www.fored.co.uk/) website.
 The download file comes with its own installation instructions and documentation.
4. **FreeRTOS needs to be installed**
The Microchip PIC18 wizC/fedC FreeRTOS port is designed to be a library in the wizC or fedC development
 environment. The library files need to be installed. The port source directory
 FreeRTOS/Source/portable/WizC/PIC18 contains a file called install.bat.
 This script will install all files needed to use the port in the LibsUser directory of your fedC or wizC
 installation. Double click the script to run it.
5. **WizC and fedC project settings**
WizC and fedC have several optimization options in the project dialog box. Unless stated otherwise below, all
 options may be changed as desired.

	* **Use PIC Call Stack (Quick Call)**
	The compiler can be instructed to use its software stack or the PIC call stack to store the
	 return address when a function is called. The FreeRTOS port requires the compiler to use the PIC
	 call stack. When this option is not enabled, an error will be flagged during compilation. The call
	 stack limits the calling depth to 32 levels. With FreeRTOS, every task has its own 32 level call
	 stack making PIC call stack overflows very unlikely.
	* **Local Optimise Bytes**
	The compiler can set global memory aside to be used for storing local variables and for
	 passing parameters during function calls. This reduces the use of the software stack and,
	 therefore, improves performance. With this port of FreeRTOS, the local optimise bytes can
	 be freely used (or disabled). It is important, however, to realise that every task that runs
	 under the RTOS has its own copy of these local optimise bytes. At task switch, the
	 'locopt' area is saved to the task's stack. Thus, the size of the area affects the performance
	 of task switches.
6. **Heap usage with WizC and fedC**
The compiler uses a heap to pass function return values larger than four bytes back to the calling function.
 For performance reasons, this port does not preserve the heap between task switches. It is therefore not
 allowed to have functions that return variables larger than four bytes. To help you avoid such functions,
 the FreeRTOS header contains a pragma to inform the compiler about this restriction. The compiler will then
 issue a warning when it encounters a function that uses the heap. Although only a warning is issued,
 you should not ignore this message because unexpected behaviour will occur. When you need to return
 variables (eg a structure) larger than four bytes, you should use a pointer to the structure instead.
7. **WizC and the Application Designer**
The difference between wizC and fedC is the presence of a rapid application development front-end in wizC.
 This so-called Application Designer cannot be used with FreeRTOS and should be switched off for any
 project that makes use of this FreeRTOS port.
8. **Minimal StackSize**
The FreeRTOSConfig.h file contains a definition called configMINIMAL\_STACKSIZE to define the minimal size
 in bytes the stack for a minimal task should contain. By default for this port, configMINIMAL\_STACKSIZE
 is defined as portMINIMAL\_STACKSIZE. When you look for portMINIMAL\_STACKSIZE in portmacro.h, you will
 find that the minimal stacksize is calculated during runtime upon the first reference of
 configMINIMAL\_STACKSIZE. This is done because the minimal stacksize depends on several optimisation settings
 within your project. It is advised not to change the definition of configMINIMAL\_STACKSIZE. If a larger
 stack is needed for one or more tasks in your project, use configMINIMAL\_STACKSIZE as a base value:

```c
// MyTask needs 20 extra bytes
#define MyStackSIZE  ( configMINIMAL_STACKSIZE + 20 )
```

 This way the automatic adjustment of your larger stack to the optimisation settings within your
 project still takes place. See the demo applications for examples of this feature.

---

### The Demo Applications

#### Demo application hardware setup

Although, the PIC18 wizCfedC port was developed entirely in the simulator, the anticipated hardware
 to run the demo applications was the 40 pin PICmicro
 prototyping board from Forest Electronic Developments.
 A [PIC18F4620](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1335&dDocName=en010304) embedded microcontroller was installed. This prototyping board allows for in system
 flash programming (ICSP) by means of the PicProg utility, also supplied by
 Forest Electronic Developments.

When using a different hardware platform, it is not very likely that this alternative board would have LEDs
 connected in the same configuration as the development board used to create the port. The LED routines are
 contained within FreeRTOS/Demo/PIC18\_WizC/ParTest/ParTest.c and might require modification.
 
#### Demo application projects

* **Demo1**
The first demo is merely included to test the correct installation of FreeRTOS. It is meant to be run
 only in the simulator because it blinks eight LEDs where the development board only has four. It can,
 of course, be run on an alternative board which has eight LEDS on portD.  

 Eight tasks are created. Each task blinks a LED on portD. The blink rate of each task is chosen
 in such a way that portD seems to be a binary counter. It are however eight independent tasks that
 have been given convenient blink rates. This project is a good example of a minimal FreeRTOS project.
* **Demo2**
Includes the standard minimal "integer", "pollQ", "SemTest" and "Flash" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 To ensure the target is not unexpectedly resetting a single "X" is transmitted from the USART when the
 application boots. When operating correctly Demo2 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. A total of 12 tasks are created.
* **Demo3**
Includes the standard minimal "integer", "BlockQ" and "Flash" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 To ensure the target is not unexpectedly resetting a single "X" is transmitted from the USART when the
 application boots. When operating correctly Demo3 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. A total of 12 tasks are created.
* **Demo4**
Includes the standard minimal "integer", "dynamic" and "Flash" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 To ensure the target is not unexpectedly resetting a single "X" is transmitted from the USART when the
 application boots. When operating correctly Demo4 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. A total of 11 tasks are created.
* **Demo5**
Includes the standard minimal "flop" and "Flash" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 To ensure the target is not unexpectedly resetting a single "X" is transmitted from the USART when the
 application boots. When operating correctly Demo5 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. A total of 13 tasks are created.
* **Demo6**
Includes the standard minimal "ComTest" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 When operating correctly Demo6 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. A total of 4 tasks are created.  

**Note:** A loopback connector on the serial port is required to run this demo successfully.
* **Demo7**
Includes the standard minimal "Death" and "Flash" tasks, along with a "check" task
 that periodically checks that the other tasks are operating without error, and flashes a LED accordingly.
 To ensure the target is not unexpectedly resetting a single "X" is transmitted from the USART when the
 application boots. When operating correctly Demo7 will cause LED 4 to toggle every 10 seconds. If an error
 has occurred in any task the toggle rate will increase to 1 second. Demo7 repeatedly creates and
 deletes tasks up to a maximum of 10 tasks at one time.

#### Building the demo applications

Each demo application directory contains its own project file. A project is loaded into the wizC or fedC IDE
 by double clicking the project (.pc) file. After loading is complete, you can compile the project in the normal
 way.

A project consists of several files:

* **Main.c**
This file contains the main application code for the demo, including the main() entry point.
* **Fuses.c**
The configuration settings for the chip this demo will run on.
* **Interrupt.c**
The PIC18 MCU supports only a single interrupt vector (priority interrupts are not used by the port).
 All interrupt handling is therefore concentrated in a single Interrupt() function which is located in
 this file. If additional handlers are needed, they can be added to this file. Several demo's make use
 of this facility.
* **FreeRTOSConfig.h**
The FreeRTOS configuration settings for this project. 
 See the [Customisation section](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
 for an explanation of all the settings.
* **MallocConfig.h**
The malloc library also has a configuration file. Things like the private malloc heap size are defined
 here. Refer to the documentation that accompanies the malloc library for more details.
* **WIZCmake.h**
Most demo applications use additional code from the FreeRTOS/Demo/Common/Minimal directory. To 
 enable the compiler to locate the header files in FreeRTOS/Demo/Common/Include, WIZCmake.h
 contains a search path setting to this directory (If WIZCmake.h exists in the project directory, it is
 automatically included by the compiler as first header file with every compile).

#### How to create a new project

The demo project in the FreeRTOS/Demo/PIC18\_WizC/Demo1 directory is a very minimal project. The most simple
 way to start a new project is to copy all files from this directory to your new project directory.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in FreeRTOSSourceportableWizCPIC18portmacro.h.
 The constants defined in this file do normally not require any modification.

Application specific configuration items can be found in the FreeRTOSConfig.h file within each project directory.
 All definitions in this file may be modified.

The definition configTICK\_RATE\_HZ is used to set the frequency
 of the RTOS tick. The supplied value of 250Hz is useful for testing the RTOS kernel functionality but might be faster
 than your applications require. Lowering this value will improve efficiency. When a too low value is used, the
 compiler will flag an error. Using an MCU frequency of 40MHz (10MHz xtal with pll), the minimum rate is 20Hz.
 Lower MCU-frequencies allow for even lower tick rates.

Because it is unlikely that the RTOS scheduler for the PIC port will get stopped once running, vPortEndScheduler()
 will perform a MCU reset.

#### Interrupt service routines

Only the GIE bit in the INTCON register is used. This means that the port does not currently support high/low
 priority interrupts.

Every project contains an interrupt.c file. The routines to test each interrupt flag can be added to the
 Interrupt() function in this file. It is also possible to #include these routines. Study the demo projects
 for more information.

Upon entering the ISR, the current context is always saved. It is, therefore, allowed to use the entire
 spectrum of the C language inside an ISR (exception: local variables, see below). If a context switch is
 desired, set uxSwitchRequested to pdTRUE. This makes the task with the highest priority that is ready to
 run candidate to be restored (activated) at ISR exit. See FreeRTOS/Demo/PIC18\_WizC/serial for
 an example of ISR routines.

In the ISR, it is not allowed to use local variables. To overcome this limitation, use one of the following
 alternatives:

* Use static variables. Global RAM usage increases.
* Call a function. Additional cycles are needed.
* Map your variables to currently unused SFR's. This method is preferred because there is no additional
 overhead. See FreeRTOS/Demo/PIC18\_WizC/serial/isrSerialTx.c for an example of this method.

#### To use a processor other than the PIC18F4620

Selecting a different MCU from the Microchip PIC18 family is an easy task:

* Make sure the new MCU has enough RAM, ROM and peripherals.
* Use the project options in the wizC or fedC IDE to select the new MCU.
* Verify that the MCU configuration settings in fuses.c are still valid. Change if needed.
* (Re-)compile the project.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within the FreeRTOSconfig.h file in the project directory to 1
 (to use pre-emption) or 0 (to use co-operative).

#### Timer usage

The port uses a compare match on timer 1 to generate the RTOS tick. During compilation, the timer and compare
 values are automatically calculated to match the MCU clock speed.

#### Memory allocation

The port uses the malloc library that can be freely downloaded from the
 [Forest Electronic Developments](http://www.fored.co.uk/) website. See the documentation
 of this library for detailed API-specifications.

#### Serial port driver

It should be noted that the serial drivers are written to test some of the real time kernel features.
 They are not intended to represent an optimised solution. The bit rate register settings are 
 automatically adjusted according to the frequency the MCU runs on.

Copyright (C) Amazon Web Services, Inc. or its affiliates. All rights reserved. 
