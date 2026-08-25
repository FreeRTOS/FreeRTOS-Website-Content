---
title: "STM32F100 ARM Cortex-M3 FreeRTOS Demo Using GCC and the Atollic TrueStudio Eclipse based IDE"
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
| <br />![](/media/2018/FreeRTOS-running-on-a-SMT32-value-line-STM32F100-discovery-board.jpg)<br /> |

### Introduction

This simple demo project runs on the [STM32 Discovery board](http://www.st.com/stm32-discovery), which is
populated with an [STM32F100RB](http://www.st.com/internet/mcu/product/216844.jsp)
Cortex-M3 microcontroller from [STMicroelectronics](http://www.st.com/).

Its low cost makes the discovery board an ideal evaluation platform, but the 8K
of RAM available also means there is a limit to the number of FreeRTOS kernel
features that can be demonstrated. Therefore, this simple demo only actively
demonstrates task, queue, software timer and interrupt functionality. The demo is also
configured to include malloc failure, idle, and stack overflow hook
functions.

The FreeRTOS download includes other, more fully featured, demonstration applications
for larger parts in the STM32 microcontroller family.

The demo is pre-configured to use the free version of the

[Atollic TrueStudio for STM32](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html) Eclipse based
IDE, along with the FreeRTOS GCC port.

---

#### *IMPORTANT! Notes on using the STM32F100 ARM Cortex-M3 Demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does
not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports so
includes many more files than are required for this demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the downloaded files and information on creating a
new project.

The TrueStudio project for the FreeRTOS STM32 Discovery Board demo is located in the
FreeRTOS/Demo/CORTEX\_STM32F100\_Atollic directory. This is the project
that should be imported into the TrueStudio workspace. The
[Preparing the Eclipse Project](#building-and-running-the-demo-application) section below contains
important information on setting up the demo project directory, and importing
the demo project into TrueStudio.

---

### The Demo Application

#### Demo application hardware set up

The demo uses the LEDs and buttons that are integrated onto the STM32 Discovery
board hardware. Therefore, no hardware set up is required.

#### Preparing the TrueStudio (Eclipse) project directory

Eclipse projects can be either standard makefile projects, or managed make projects.
The STM32F100 project uses a managed make project. This in turn means that
either:

1. All the source files needed to build the project must be located under
 the folder/directory that contains the project file itself, or
2. The Eclipse workspace (note workspace, not project) needs to be
 configured to locate the files elsewhere on the hard disk.

Option 1 is used in this case. To that end, the directory FreeRTOS/Demo/CORTEX\_STM32F100\_Atollic
contains a batch file called CreateProjectDirectoryStructure.bat that
will copy all the required FreeRTOS source files into sub directories inside the
demo project directory.

**CreateProjectDirectoryStructure.bat must be executed before the TrueStudio
project is imported into the Eclipse workspace**. 

CreateProjectDirectoryStructure.bat cannot be
executed from within the TrueStudio Eclipse IDE.

#### Importing the demo application project into the TrueStudio Eclipse workspace

To import the STM32 TrusStudio project into an existing or new Eclipse Workspace:
1. Select "Import" from the TrueStudio "File" menu. The dialogue box shown below
 will appear. Select "Existing Projects into Workspace".  

![Importing the STM32 TrueStudio project into the Eclipse workspace](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**The dialogue box that appears when "Import" is first clicked**
2. In the next dialogue box, select FreeRTOS/Demo/CORTEX\_STM32F100\_Atollic
 as the root directory. Then, make sure the FreeRTOS-Simple-Demo
 project is checked in the "Projects" area, **and that the Copy Projects Into
 Workspace box is not checked**, before clicking
 the Finish button (see the image below for the correct check box states,
 the finish button is not visible in the image).

![Selecting the FreeRTOS STM32 project to import into Eclipse](/media/2018/selecting-the-FreeRTOS-STM32-project-to-import-into-Eclipse.jpg)

**Make sure that FreeRTOS-Simple-Demo is checked, and "Copy projects into workspace" is not checked**

#### Building and running the demo application

1. Connect the STM32 Discovery board to your host computer using a standard USB cable. You may be prompted to install some USB drivers.
2. Ensure that CreateProjectDirectoryStructure.bat has been executed,
 and that the project has been correctly imported into the Eclipse workspace.
3. Select 'Rebuild All' from the IDE 'Project' menu.
4. Select 'Debug' from the IDE 'Run' menu. If a debug session starts, the process is complete. If a debug session does not start, follow the remaining instructions in this list.
5. Sometimes a debug configuration needs to be created before debugging for the first time. Select 'Debug Configurations...' from the IDE 'Run' menu.
6. In the dialogue box that appears, click the "New Launch Configuration" speed button, highlighted in red in the image below.
7. A new debug configuration will be created, and the dialogue box should appear as shown in the image below. Click the "Debug" button to commence debugging.

![Creating the STM32 Value Line Discovery board debug configuration](/media/2018/Creating-the-STM32-Discovery-board-debug-configuration.jpg)

**The dialogue box used to create a debug launch configuration after the  
"New Launch Configuration" speed button (highlighted in red) has been pressed.**

#### Functionality

* **The idle hook function:** 
 
 The idle hook function queries the amount of FreeRTOS heap space that is
 remaining (see vApplicationIdleHook() defined in main.c). The demo
 application is configured to use 7K of the available 8K of RAM as the FreeRTOS heap.
 Memory is only allocated from this heap during initialisation, and this demo
 only actually uses 1.6K bytes of the configured 7K available - leaving 5.4K
 bytes of heap space unallocated.
* **The main() Function:** 
 
 main() creates one software timer, one queue, and two tasks. It then starts the
 scheduler.
* **The Queue Send Task:** 
 
 The queue send task is implemented by the prvQueueSendTask() function in main.c.
 prvQueueSendTask() sits in a loop that causes it to repeatedly block for
 200 milliseconds, before sending the value 100 to the queue that was created
 within main(). Once the value is sent, the task loops back around to block for
 another 200 milliseconds.
* **The Queue Receive Task:** 
 
 The queue receive task is implemented by the prvQueueReceiveTask() function
 in main\_blinky.c. prvQueueReceiveTask() sits in a loop where it repeatedly blocks on
 attempts to read data from the queue that was created within main(). When data
 is received, the task checks the value of the data, and if the value equals
 the expected 100, toggles the green LED. The 'block time' parameter passed to
 the queue receive function specifies that the task should be held in the Blocked
 state indefinitely to wait for data to be available on the queue. The queue
 receive task will only leave the Blocked state when the queue send task writes
 to the queue. As the queue send task writes to the queue every 200
 milliseconds, the queue receive task leaves the Blocked state every 200
 milliseconds, and therefore toggles the green LED every 200 milliseconds.
* **The LED Software Timer and the Button Interrupt:** 
 
 The user button B1 is configured to generate an interrupt each time it is
 pressed. The interrupt service routine switches the red LED on, and resets the
 LED software timer. The LED timer has a 5000 millisecond (5 second) period, and
 uses a callback function that is defined to just turn the red LED off.
 Therefore, pressing the user button will turn the red LED on, and the LED will
 remain on until a full five seconds pass without the button being pressed.

---

### RTOS Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to these demos are contained in FreeRTOS/Demo/CORTEX\_STM32F100\_Atollic/Simple\_Demo\_Source/FreeRTOSConfig.h. The
constants defined in FreeRTOSConfig.h can be edited to meet the needs of your application. In particular -

* **configTICK\_RATE\_HZ**
 This sets the frequency of the RTOS tick interrupt. The supplied value of 1000Hz is useful for
 testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**

 See the [RTOS kernel configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) documentation for full information on these configuration constants.

Attention please!: Remember that ARM Cortex-M3 cores use
numerically low priority numbers to represent HIGH priority interrupts. This
can seem counter-intuitive and is easy to forget! If you wish to assign an
interrupt a low priority do NOT assign it a priority of 0 (or other low numeric
value) as this will result in the interrupt actually having the highest priority
in the system - and therefore potentially make your system crash if this
priority is above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY. Also, do not leave
interrupt priorities unassigned, as by default they will have a priority of 0
and therefore the highest priority possible.

The lowest priority on a ARM Cortex-M3 core is in fact 255 - however different
Cortex-M3 vendors implement a different number of priority bits and supply library
functions that expect priorities to be specified in different ways. For example,
on the STM32 the lowest priority you can specify in an ST driver library call
is in fact 15 - this is defined by the constant
configLIBRARY\_LOWEST\_INTERRUPT\_PRIORITY in FreeRTOSConfig.h. The highest priority
that can be assigned is always zero.

It is also recommended to ensure that all four priority bits are assigned as
being preemption priority bits. This can be ensured by passing
"NVIC\_PriorityGroup\_4" into the ST library function NVIC\_PriorityGroupConfig().
In the demo project this is done from the function prvSetupHardware(), which is
itself defined in main.c.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that
processor. This port defines BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Unlike most ports, interrupt service routines that cause a context switch have
no special requirements and can be written as per the compiler documentation.
The macro portEND\_SWITCHING\_ISR() can be used to request a context switch from within an ISR.

Note that portEND\_SWITCHING\_ISR() will leave interrupts enabled.

This demo project provides an example interrupt service routines -
namely EXTI0\_IRQHandler() defined in main.c.

Note that the following lines are included in FreeRTOSConfig.h:

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler
```

These definitions map the FreeRTOS kernel interrupt handler function names onto
the CMSIS interrupt handler functions names - and in so doing, allow the
Atollic provided linker script and start up files to be used without modification.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/CORTEX\_STM32F100\_Atollic/Simple\_Demo\_Source/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the ARM Cortex-M3 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
