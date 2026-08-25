---
title: "Microchip AVR Dx Port Demos"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS Demo for the Microchip AVR Dx Port 
using the XC8, AVR-GCC and IAR EWAVR compilers

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


![[TOD Describe image]](/media/2020/Screen-Shot-2020-08-21-at-12.20.42-PM.png)


There are multiple FreeRTOS ports for the Microchip AVR microcontrollers. This page describes the ports for the AVR Dx 
families, which include the [AVR DA](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-da) and the [AVR DB](https://www.microchip.com/wwwproducts/en/AVR128DB64) families. Ports are available for Atmel AVR-GCC, XC8 and 
[IAR Embedded 
 Workbench for AVR](https://www.iar.com/iar-embedded-workbench/#!?architecture=AVR) (IAR EWAVR) compilers.

#### Devices supported

These demos and examples are configured for the AVR128DA48, which has 128 KB Flash and 16 KB SRAM--enough memory for 
applications with a high number of real time tasks. The size of the FreeRTOS demo depends on the compiler used, but in the 
[Full Demo](#full-demo) configuration it requires around 15 KB of program memory or less. Running 10 real-time tasks, 
in addition to the idle task, requires approximately 2 KB of SRAM. So there is more than enough SRAM left for communication 
buffering, advanced algorithms and other SRAM intensive parts of the application.

#### Compilers and IDEs supported

Ports are available for three different compilers. The versions used to develop the ports are shown in parentheses:

* XC8 (v2.20)
* AVR-GCC (build 3.6.2.1778)
* IAR EWAVR (7.30)

The following IDE versions were used to develop and test the ports:

* [Microchip MPLAB X](https://www.microchip.com/mplab/mplab-x-ide)
 (5.40 with device pack AVR-Dx\_DFP 1.2.52)

for the XC8 port
* [Atmel Studio 7](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio) 
 (7.0.2397 with device pack AVR-Dx\_DFP 1.1.45)

for the AVR-GCC port and the demo application projects

The XC8 and AVR-GCC compilers are integrated into the Microchip MPLAB X and the Atmel Studio 7 IDEs.

#### Demo applications

The FreeRTOS demo applications for the AVR DA microcontroller (blinky demo, minimal demo, full demo) all target the 
[AVR128DA48 Curiosity Nano evaluation kit](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151). The demo applications can be built with either MPLAB X (XC8), Atmel Studio 
(AVR-GCC), or IAR EWAVR. 

A more advanced example application is available from Atmel START. That example targets a combination of three boards: the 
[Curiosity 
 Nano Base for Click boards](https://www.microchip.com/developmenttools/ProductDetails/AC164162), the [AVR128DA48 Curiosity Nano evaluation kit](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151), and the 
[OLED1 
 Xplained Pro board](https://www.microchip.com/developmenttools/ProductDetails/atoled1-xpro).


---

#### IMPORTANT! Notes on using the Microchip AVR Dx port

*Please read all the following points before using this RTOS port.*

* [Source code organisation](#source-code-organization)
* [The demo application functionality](#demo-applications)
* [Building and running the RTOS demo application using Microchip AVR Dx in the QEMU 
 emulator](#building-the-rtos-demo-application)
* [RTOS configuration and usage details](#configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Source Code Organization

The code of the FreeRTOS kernel and demos is available to download from the [main download page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) on FreeRTOS.org. The FreeRTOS zip file download contains the source code for all the FreeRTOS ports and demo applications – it therefore contains many more files than are needed for this project. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of 
the directory structure and information on creating a new FreeRTOS project.

The MPLAB X project for the AVR128DA48 demo application is in the `FreeRTOS/Demo/AVR_Dx_MPLAB.X` directory. The 
Atmel Studio 7 project for the AVR128DA48 demo application is called `RTOSDemo.atsln` and is located in the 
`FreeRTOS/Demo/AVR_Dx_AtmelStudio` directory.

The MPLAB X project for the AVR128DA48 demo application is in the `FreeRTOS/Demo/AVR_Dx_MPLAB.X` directory.

The Atmel Studio 7 project for the AVR128DA48 demo application is called `RTOSDemo.atsln` and is located in the 
`FreeRTOS/Demo/AVR_Dx_AtmelStudio` directory. 

The IAR EWAVR project for the AVR128DA48 demo application is called `RTOSDemo.eww` and is located in the 
`FreeRTOS/Demo/AVR_Dx_IAR` directory. 

---


### The Microchip AVR Dx Demo Application

#### Functionality

Each port comes with three different demos selectable by a define (`#define mainSELECTED_APPLICATION`) in the 
`main.c` file. Each demo has its own `main-<demo-name>.c` file. This structure is used for all 
three IDEs (Atmel Studio 7, MPLAB X and IAR EWAVR). All of them use an identical `FreeRTOSConfig.h` file that 
accommodates the most comprehensive demo ([Full Demo](#full-demo)). 

##### Blinky Demo

If `mainSELECTED_APPLICATION` is set to 0 then `main()` calls `main_blinky()` that creates 
a simple demo as follows:

1. `The main_blinky()` function creates one queue and two tasks, then starts the RTOS scheduler.
2. The Queue Send Task is implemented by `prvQueueSendTask()` in `main_blinky.c`. It sends a fixed 
 value (100) to the queue every 200 milliseconds.
3. The Queue Receive Task is implemented by `prvQueueReceiveTask()` in `main_blinky.c`. It blocks 
 on queue reads, unblocking and toggling an LED each time the message from the queue send task is received. The queue 
 send task sends to the queue every 200 milliseconds, so the queue receive task leaves the Blocked state and toggles 
 the LED every 200 milliseconds.

##### Minimal Demo

If `mainSELECTED_APPLICATION` is set to 1 then `main()` calls `main_minimal()` that creates 
the following tests tasks: 

* The Integer Math Test is implemented by `vStartIntegerMathTasks()` in `integer.c`. It creates a 
 task function that repeatedly performs a 32-bit calculation, checking the result against the expected one.
* The Register Test is implemented by `vStartRegTestTasks()` in `regtest.c`. It creates two tasks 
 that write different values in all registers and verify that the content is kept during the context switch.
* The Polled Queue Test is implemented by `vStartPolledQueueTasks()` in `PollQ.c`. It creates two 
 tasks that communicate over a single queue. One task acts as a producer, the other as a consumer. All queue accesses are
 performed without blocking.
* The Serial Communication Test is implemented by `vAltStartComTestTasks()` in `comtest.c`. It 
 creates two tasks that operate on an interrupt driven serial port. A loopback connector should be used so that 
 everything that is transmitted is also received.

Finally, the Check Task implemented by `vErrorChecks()` is created to periodically inspect the standard demo 
tasks to ensure all the tasks are functioning as expected. The Check Task also toggles an LED to give visual feedback of 
the system status. If the LED toggles every 3 seconds, then the check task has not discovered any problems. If the LED stops
toggling, then the check task has discovered a problem in one or more tasks.

The minimal demo project files are provided to demonstrate the use of the RTOS kernel and are not intended to provide an 
optimized solution. This is particularly true for `comtest.c` which uses an example interrupt-driven UART driver 
(`serial.c`). This is written with the intent of stressing (and therefore testing) the RTOS kernel implementation 
rather than providing an example of an optimal solution.

##### Full Demo

If `mainSELECTED_APPLICATION` is set to 2, then `main()` calls `main_full()` to create a 
comprehensive demo that demonstrates and tests several FreeRTOS features, including [tasks](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview), 
[direct to task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications), [queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/), 
[semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/), [software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers), and 
more. The following tests are created: 

* The Semaphore Test Task, implemented by `vStartSemaphoreTasks()` in `semtest.c`, creates two sets 
 of two tasks each. The tasks within a set share a variable, whose access is guarded by a semaphore.
* The Direct to Task Notification Task, implemented by `vStartTaskNotifyTask()` in `TaskNotify.c` 
 file, creates a task that performs some tests by itself, then loops around, being notified by both a software timer 
 and an interrupt.
* The Register Test Task, implemented by `vStartRegTestTasks()` in `Regtest.c`, creates two tasks 
 that write different values in all registers and verify that their contents are preserved during the context switch.
* The Recursive Mutex Task, implemented by `vStartRecursiveMutexTasks()` in `RecMutex.c`, 
 demonstrates the use of recursive mutexes. It creates three tasks that all access the same recursive mutex.

The Check Task, implemented by `vErrorChecks()`, is then created to periodically inspect the standard demo tasks 
to ensure all the tasks are functioning as expected. The Check Task also toggles an LED to give visual feedback of the system 
status. If the LED toggles every 3 seconds, then the check task has not discovered any problems. If the LED stops toggling, 
then the check task has discovered a problem in one or more tasks. 

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) tasks. Standard demo tasks are used by all 
FreeRTOS port demo applications and have no specific functionality. They are used to demonstrate how to use the FreeRTOS API, 
and to test the RTOS port. 

#### Building the RTOS demo application

##### Development tools options

The demo applications are available for Atmel Studio, MPLAB X and IAR EWAVR. This implies three compilers: AVR-GCC, XC8 and 
IAR EWAVR. From the demo-code point of view, all three demo projects are identical. The porting files are also identical for 
Atmel Studio and MPLAB X, but the porting files for IAR EWAVR are different.

##### Preparing project files

To start, first get the FreeRTOS kernel and demos code by downloading (or recursively cloning) the GitHub 
repository [https://github.com/FreeRTOS/FreeRTOS](https://github.com/FreeRTOS/FreeRTOS). The FreeRTOS download 
includes source code for multiple processor ports, and demo applications, but each supported processor 
architecture requires a small amount of architecture-specific RTOS code. This is the RTOS portable layer, 
and it is located in the `FreeRTOS/Source/Portable/<compiler>/<architecture>` sub directories, where `<compiler>` 
and `<architecture>` are the compiler used to create the port, and the architecture on which the port runs, 
respectively. Please see 
the [FreeRTOS source code organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) 
page for a full explanation of the FreeRTOS directory structure. 

Note: The port files for GCC and XC-8 compilers are identical, so the MPLAB-X projects use files located in the
`.../Portable/GCC/AVR_AVR_Dx` folder.

For the AVR Dx devices, all necessary port files and demos can be found in the following folders:

![](/media/2020/Screen-Shot-2020-08-21-at-2.38.12-PM.png)
Folder Structure.

The next step is to open the application from its project folder within `FreeRTOS/Demo`. The projects for each 
IDE/compiler already have all the necessary files linked.

##### Building with MPLAB X and XC8

To compile the demo project using MPLAB X, follow these steps:

1. Start MPLAB-X
2. From the start menu, select File -> Open Project and browse to the folder where the project is located:

![](/media/2020/Screen-Shot-2020-08-21-at-2.44.20-PM.png)
3. Select "AVR\_Dx\_MPLAB.X" and open it.
4. Build the project.

##### Building with Atmel Studio 7 and AVR-GCC

To compile the demo project using Atmel Studio 7, follow these steps:

1. Start Atmel Studio.
2. In the tool menu, select File -> Open -> Project/Solution. Browse to the folder where the project is located:

![](/media/2020/Screen-Shot-2020-08-21-at-2.44.33-PM.png)
3. Select "RTOSDemo.asln" and open the project.
4. Build the project.

##### Building with IAR EWAVR

To compile the demo project using IAR EWAVR, follow these steps:

1. Start IAR Embedded Workbench.
2. In the menu, select File -> Open Workspace and browse to the project location.

![](/media/2020/Screen-Shot-2020-08-21-at-2.42.12-PM.png)
3. Select "RTOSDemo.eww" and open it.
4. Build the project.

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to FreeRTOS demos are in the `FreeRTOSConfig.h` file located in each project folder. 
The following are few define examples. All constants defined in this file can be edited to suit a specific application. 

* `#define configCPU_CLOCK_HZ` - microcontroller clock, used by timers and to calculate delays and baud-rates 
 for communications.
* `#define configTICK_RATE_HZ` – used to set the frequency of the RTOS tick. All demos use a value of 1000Hz 
 to test the RTOS kernel functionality.
* `#define configUSE_PREEMPTION` - used to switch between the preemptive and cooperative FreeRTOS kernels.
* `#define configUSE_TIMER_INSTANCE` - the port allows the user to select which timer used for the RTOS tick. 
 The list of available options is detailed in the `FreeRTOS_Config.h` file, and the support functions/macro's 
 are located in the `porthardware.h` file.

Each port also defines the type '`BaseType_t`' to be equal to the most efficient data type for that processor. 
The AVR Dx port defines '`BaseType_t`' as char (8 bits): 

* `#define portBASE_TYPE char`

Note: The tick timer options list contains options that are available on the larger members of AVR Dx family. Please refer to 
the specific device datasheet for a list of available options.

##### Memory areas used by the compiler

The FreeRTOS port requires you to define the heap and stack used by compiler. Those are defined to accommodate the more 
comprehensive demo example ([Full Demo](#full-demo)), but the size is customizable and depends only on the 
implementation of your application. The current port uses the following defines (these are similar for all tools/compilers):

* `#define configTOTAL_HEAP_SIZE 0x1000`
* `#define configMINIMAL_STACK_SIZE 120`

Note: The IAR compiler requires two stacks (`CSTACK` and `RSTACK`); the `CSTACK` is 
configured to 120 bytes and the `RSTACK` to 30 bytes. 

##### Memory allocation

`Source/Portable/MemMang/heap_1.c` is included in the AVR Dx demo application project to provide the memory 
allocation required by the RTOS kernel. Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the 
API documentation for complete information.

##### Demo application USART and port drivers

The `demos` application folder contains examples for two drivers.
* The USART driver is included in the `serial.c` file. It is an interrupt-based driver that uses the USART 
 instance connected to the onboard debugger USART. This way, the messages sent by the Serial Communication Test 
 (`ComTest`) task can be viewed on the PC without requiring any special hardware other than the board itself 
 and a USB cable. The USART driver enables the internal loopback connection between the RX and TX signals, because the 
 `ComTest` verifies the sent data is received back without error.
* The demo applications include a file called `partest.c` that is a driver for a whole port of the MCU. 
 (The name is historic and has since lost its meaning, but it is derived from 'parallel port test'.) The file contains 
 the interface functions for setting LEDs, clearing LEDs and toggling LEDs. In these examples, port C was chosen as the 
 port where the onboard LED is connected. The LED pin is chosen because getting the LED output working is the first step 
 when porting a demo from one hardware platform to another. For the selected hardware platform (AVR128DA48 Curiosity 
 Nano), the other LED pins controlled by `partest.c` are not physically connected to an LED.

 

#### Other notes

It is not necessary to read this section in order to use the port.

##### Using an alternative hardware platform

The AVR128DA48 Curiosity Nano board was chosen for its easy-to-get-started features, but any other hardware platform can 
be used with minimal additional effort. The multiple options available for the tick timer and the available demos facilitate 
the development of FreeRTOS applications on any device in the AVR Dx family.

##### Using an alternative AVR Dx device

The FreeRTOS demo port can run on any device in this family. Simply change the device type in the development tool 
configuration window and then re-compile the project.

##### Tick timer selection

All available demo ports use TCB0 as the default tick timer (`#define configUSE_TIMER_INSTANCE 0`). This timer 
is available on all AVR Dx devices. Other timers can be selected using `configUSE_TIMER_INSTANCE` as follows (refer 
to the `FreeRTOS_Config.h` file for available options):

* `#define configUSE_TIMER_INSTANCE 0 - use TCB0 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 1 - use TCB1 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 2 - use TCB2 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 3 - use TCB3 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 4 - use TCB4 as the tick timer`
* `#define configUSE_TIMER_INSTANCE 5 - use RTC as the tick timer`

##### Clock configuration

The AVR Dx ports use an on-chip oscillator as the main clock. Because of its internal architecture, only certain 
predefined values can be used for the internal clock. To ensure an easy start-up with the AVR Dx platform, an additional 
`clk_config.h` file is provided. This file contains a list of supported clock configurations, clock initialization 
procedures (`clk_init()`), and uses `#define configCPU_CLOCK_HZ` (in file `FreeRTOS_Config.h`) 
as input.

##### Serial port configuration

When `mainSELECTED_APPLICATION` is set to 1, the project includes an example of an interrupt-driven driver for 
serial communication that uses the USART1 instance (file `serial.c`). Any other available USART instance (USART0-5) 
can be used as a direct replacement if necessary. In addition, the USART Rx and Tx pins should be configured. For the current demo 
this is done in the hardware initialization procedure:

```c
void init_minimal( void ) 
{ 
    /* Configure UART pins: PC1 Rx, PB0 Tx */ 
    PORTC.DIR &= ~PIN0_bm; 
    PORTC.DIR |= PIN1_bm;

    ... 
} 
```

##### LED port configuration

LEDs provide the easiest method of getting visual feedback that the demo application is running, so it is useful to get 
the LEDs on the new hardware platform working as soon as possible.

It is unlikely that the hardware platform to which the demo is ported has LEDs on the same IO ports as the hardware 
platform on which the demo was developed – so some minor modifications will be required.

The function `vParTestInitialise()` in the `partest.c` file contains the IO port mode and direction 
configuration. The function `prvSetupHardware()` in `main.c` contains additional generic hardware 
configurations and may also require some modifications, depending on the port being used.

Make any changes necessary to the two functions referred to in the paragraph above, then write a very simple program to 
check that the LED outputs are working.

##### Using interrupts

The interrupts that are not used for context switching can be used without special requirements. The method used to install 
the interrupt vectors depends on the port and compiler used. Refer to the existing demo for the port you are using. If an 
interrupt is used for the context switch, it requires special handling. Refer to `serial.c` and the porting files 
for examples of using interrupts for the context switch.

 
