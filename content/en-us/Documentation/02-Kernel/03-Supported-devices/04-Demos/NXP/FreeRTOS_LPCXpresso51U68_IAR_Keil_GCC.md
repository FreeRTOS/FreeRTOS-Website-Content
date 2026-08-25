---
title: "Low Power RTOS Demo - NXP LPCXpresso51U68 Including ports for MCUXpressoIDE with GCC, IAR, and Keil"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

 

![](/media/2019/OM40005-BD-300x184.png) 

 **NXP OM40005: LPCXpresso51U68 for the LPC51U68 MCUs**
 

### Introduction

The application documented on this page demonstrates how the FreeRTOS [tick suppression](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) features can be used to minimise the power consumption of an application running on the LPC51U68 ARM Cortex-M0+ microcontroller from [NXP](https://www.nxp.com/). The LPC51U68 is designed for use in applications that are cost sensitive and require low power consumption.

Pre-configured projects that build the demo are provided for the following development tools:

1. [MCUXpresso IDE](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE)
2. [IAR Embedded Workbench](https://www.iar.com/products/architectures/nxp)
3. [ARM Keil MDK](http://www2.keil.com/NXP/)

---

#### *IMPORTANT!* Notes on using the FreeRTOS LPCXpresso51U68 low power demo project

*Please check [OM40005: LPCXpresso51U68 for the LPC51U68 MCUs](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpcxpresso51u68-for-the-lpc51u68-mcus:OM40005) for general information about this board, and*[Getting Started with LPCXpresso51U68](https://www.nxp.com/document/guide/get-started-with-the-lpcxpresso51u68:GS-LPCXpresso51U68) *for board out-of-box demo.*

*This demo assumes the user is able to setup the IDE and toolchain. Please consider reading all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The NXP LPCXpresso51U68 Demo Applications](#nxp-lpcxpresso51u68demo-applications)
3. [RTOS Configuration and Usage Details](#lpcxpresso51u68-rtos-demo-specific-configuration)

 

---

 

### Source Code Organisation

FreeRTOS source code can be downloaded from [official channels](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/). See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for an overall description of the downloaded files and information on creating a new project. Project files for this demo are located in the FreeRTOS/Demo/CORTEX\_M0+\_LPC51U68\_GCC\_IAR\_KEIL/ directory, which contains the following files: 

```c
CORTEX_M0+_LPC51U68_GCC_IAR_KEIL
	|
	+- /app    Contains demo application code and FreeRTOSConfig.h.
	+- ...     Vendor code.
	+- .project, .cproject    MCUXpresso IDE project.
	+- CORTEX_M0+_LPC51U68_IAR.{ewd, ewp, ewt, ew}   IAR project.
	+- CORTEX_M0+_LPC51U68_Keil.{uvoptx, uvprojx}    Keil project.
```

---

 

### NXP LPCXpresso51U68 Demo Applications

#### Setup

The demos use the on-board tri-color LED and UART, so no hardware setup is required.  The UART is configured to use 115200 baud, 8 data bits, no parity bit and 1 stop bit.

#### Functionality

The behaviour of the demo is controlled by the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY and mainNO\_TASK\_NO\_CHECK macros, which are defined in FreeRTOSConfig.h, as follows.  Note only option three is demonstrating tickless mode:

1. To create a simple Blinky demo build the project with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1. The blinky project creates two tasks and a queue. One task periodically sends a value to the other over the queue. The receiving task toggles an LED each time the value is received.
2. To create a project that runs a subset of the standard demo tasks build the project with both mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY and mainNO\_TASK\_NO\_CHECK set to 0. The standard demo tasks are tasks executed by all the RTOS port demo applications and serve no particularly purpose other than to demonstrate the RTOS API and test the RTOS port.
3. To experiment with tickless idle mode, set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to 0, and mainNO\_TASK\_NO\_CHECK to 1. Then try running the demo application after first building with [configUSE\_TICKLESS\_IDLE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_tickless_idle) set to 1, and then with configUSE\_TICKELSS\_IDLE set to 0 - watching the output of the UART in both cases. More information is provided in the next section.

The following sections only describe the tickless low power demo.

 

#### Low Power Demo

Setting mainNO\_TASK\_NO\_CHECK to 1 prevents any demo application tasks from being created - leaving the kernel's [Idle](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task) and [Timer Service](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task) tasks as the only tasks running.  The [tick hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) function is used to count the number of tick interrupts, and a software timer is used to toggle the LED and output the counted number of tick interrupts to the UART.  The timer's callback function is called prvCheckTimerCallback(), and its period is set by the mainCHECK\_TIMER\_PERIOD\_MS constant defined in main.c. 

When configUSE\_TICKLESS\_IDLE is set to 1 the kernel enters tickless idle mode, stopping the RTOS tick interrupt, whenever there are no tasks other than the Idle task that are able to execute. On exiting tickless mode the tick count is stepped forward by however many tick periods occurred while the kernel was in tickless mode. However, although the RTOS tick count is adjusted to the correct time, the tick interrupts never actually occurred, so the count of the number of times the tick hook function (which is called from the RTOS tick interrupt) executed is lower then the tick count - as shown in the diagrams below. See [FreeRTOS Low Power Support](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) for more information.

 

The MCUXpresso IDE provides a [power measurement tool](https://community.nxp.com/t5/LPC-Microcontrollers-Knowledge/IDE-Tool-Energy-Measurement-in-MCUXpresso-IDE/ta-p/1444553) which is used to quantify the power saved by the tickless idle feature, but note this demo does not attempt to maximise power saving - to do that it would be necessary to use a low power clock, turn off peripherals such as the UART, and disconnect the debugger.

![](/media/2020/power_tickless_enabled.png) 

**Power measurement — configUSE\_TICKLESS\_IDLE set to 1**
 

![](/media/2020/power_no_tickless.png) 

**Power measurement — configUSE\_TICKLESS\_IDLE set to 0**
 

![](/media/2020/serial_tickless_enabled.png) 

**Serial output — configUSE\_TICKLESS\_IDLE set to 1**
 

![](/media/2020/serial_no_tickless.png) 

**Serial output — configUSE\_TICKLESS\_IDLE set to 0**
 

Power measurement shows 0.8mA difference in the target current between tickless idle mode enabled and disabled.  As just noted, this demo does not attempt to maximise power saving as it does not use a low power clock or disable peripherals or the debugger, the power saving will be much greater if that were done.   The measurement was taken using the LPC51U68 VDD vsense 4.12Ω resistor. The difference between how many times tick ISR is triggered when tickless idle mode is enabled and disabled is quite obvious in the serial output.

---

 

### Build and Running FreeRTOS Demo Applications

#### MCUXpresso IDE Setup

1. Launch the MCUXpresso IDE. The screenshots on this page are taken with MCUXpresso IDE version 11.0.1.
2. Choose an existing or new workspace directory and click "Launch".

  [![MCUXpresso IDE Launcher.](/media/2020/step2-launch.png)](/media/2020/step2-launch.png)

MCUXpresso IDE Launcher. Click to enlarge
3. Import the MCUXpresso IDE project by clicking "File -> Open Projects from File System...". In Import Source, update directory to the project folder path FreeRTOS-root\FreeRTOS\Demo\CORTEX\_M0+\_LPC51U68\_GCC\_IAR\_KEIL.

  [![MCUXpresso IDE Import Projects.](/media/2020/step3-open-project-redbox.png)](/media/2020/step3-open-project-redbox.png)

MCUXpresso IDE Import Projects. Click to enlarge.
4. Build the project by clicking "Project -> Build All". The project should build with no warnings or errors.

  [![MCUXpresso IDE Console Build Result.](/media/2020/step4-build-all.png)](/media/2020/step4-build-all.png)

MCUXpresso IDE Console Build Result. Click to enlarge.

 To program the microcontroller flash and start a debug session using the CMSIS-DAP debug interface that is built into the evaluation board:
1. Ensure both the Link2 and LPC51U68 target sides of the board are powered, and the debug USB cable is connected to your host computer. (For Rev A boards, connect a micro USB cable to J6, not J5).
2. In IDE's Project Explore window, right click on project name, and select "Debug As -> MCUXpresso IDE LinkServer (inc. CMSIS-DAP) probes". LPC-LINK2 CMSIS-DAP is shown as available if the evaluation board was detected successfully. Click OK to enter the MCUXpresso debug perspective.

  [![MCUXpresso IDE Debug Probes.](/media/2020/step5-debug.png)](/media/2020/step5-debug.png)

MCUXpresso IDE Debug Probes. Click to enlarge.
3. MCUXpresso IDE includes handy tools for measuring average power, and observing FreeRTOS task/queue/memory usage at runtime. Check [MCUXpresso IDE User Guide](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/mcuxpresso-ide/9289/1/MCUXpresso_IDE_User_Guide.pdf) for details.

#### Other IDEs

The IAR Embedded Workbench and ARM Keil MDK projects can be opened directly in their respective IDEs, or simply by double clicking the project file within the directory structure. Please refer to [Getting Started with the LPCXpresso51U68](https://www.nxp.com/document/guide/get-started-with-the-lpcxpresso51u68:GS-LPCXpresso51U68) by NXP for details.

---

### LPCXpresso51U68 RTOS demo specific configuration

 Configuration items specific to this demo are contained in FreeRTOSConfig.h. The constants defined in that file can be edited to suit your application. Please refer to the Customization for more information. In particular about kernel port and memory management —
Kernel Port

 The ARM Cortex M0(+) ports for GCC, IAR and Keil do not implement the vPortEndScheduler() function. 

Memory Allocation

 Source/Portable/MemMang/heap\_5.c is used in the LPCXpresso51U68 demo application projects to support memory allocation across memory banks. Please refer to the Memory Management. Compiler specific attribute to place the second FreeRTOS heap memory region in the second memory bank is defined in compiler\_attributes.h.

 

 

 
