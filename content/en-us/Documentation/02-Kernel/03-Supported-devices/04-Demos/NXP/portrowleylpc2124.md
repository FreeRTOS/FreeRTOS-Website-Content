---
title: "Embedded Web Server Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: All Demos
    link: /Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview
---

### Using the FreeRTOS ARM7 GCC Port

![lpc-e2124.gif](/media/2018/lpc-e2124.gif)

**From FreeRTOS V4.0.3, this demo requires CrossWorks V1.6 or higher.**

## Introduction

This demo application uses the [FreeRTOS GCC ARM7 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106) 
along with the [Rowley Associates](http://www.rowley.co.uk/) CrossWorks integrated development tools to create a multitasking 
embedded web server example. 

The example executes 12 of the standard demo application tasks, the idle task, and a task containing
[Adam Dunkels uIP (�IP) embedded TCP/IP stack and sample small web server](http://www.sics.se/~adam/uip/).

FreeRTOS has made some modifications to the uIP stack since this demo was created. See the 
[Embedded Ethernet Examples List](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp) page for more 
information.

The demo is preconfigured to execute on the LPC-E2124 embedded Ethernet development board 
([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use 
an alternative development board), for which the uIP TCP/IP stack port and embedded Ethernet device drivers were provided by 
[Paul Curtis of Rowley Associates](http://www.rowley.co.uk/msp430/uip.htm).

## IMPORTANT! Notes on using the �IP demo

*Please read all the following points before using this Demo.*

### RTOS Configuration

This demo uses the [FreeRTOS GCC ARM7 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106) which is documented separately.
The file Demo/uIP\_Demo\_Rowley\_ARM7/FreeRTOSConfig.h is used to tailor the port for use with the LPC2124 development
board.

### Source Code Organization

* The FreeRTOS/Demo/uIP\_Demo\_Rowley\_ARM7 directory contains the Rowley CrossWorks project file - rtosdemo.hzp - and main.c.
* The directory FreeRTOS/Demo/uIP\_Demo\_Rowley\_ARM7/uip contains the uIP source code.
* Refer to the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of all the files contained in the standard FreeRTOS download.
* main.c contains the application entry point. It is responsible for creating all the tasks, then starting the real time kernel.

### Building the Demo Application

CrossWorks provides a user friendly interface to the GCC development tools - greatly
simplifying startup configuration, linking and debugging. To build the application:
1. Open the project file FreeRTOS/Demo/uIP\_Demo\_Rowley\_ARM7/rtosdemo.hzp from within the CrossWorks IDE.
2. Ensure "*Thumb FLASH Debug*" is the selected configuration (see picture below). This must be the
 selected configuration as currently it is the only configuration containing all the required settings.  
  

![](/media/2018/selectthumbflashdebug.jpg)  

Selecting the Thumb Flash Debug configuration
3. Select the "*Build Solution*" option from the "*Build*" menu within the IDE. The application should build with no warnings or errors.

### Loading and Executing the Demo Application

These instructions describe how a [J-Link USB JTAG debug interface](http://www.segger.com/jlink.html) can be used from within 
CrossWorks to program the flash and debug the application. CrossWorks also supports Wiggler (low cost) and CrossConnect JTAG interfaces. 
If you do not have access to one of these JTAG interfaces refer to the main GCC ARM7 port pages for information on using the free flash programming
software from Philips. 

1. Connect your chosen JTAG interface to the embedded computer and power on.
2. From the "*Target*" menu select the appropriate "*Connect To*" option for your debug interface.
3. Select "*Start Debugging*" from the "*Debug*" menu.

### Connecting to the Demo Application

To connect to the embedded computer you must set a compatible IP address and use an appropriate cable.

The IP address is configured within the file FreeRTOS/Demo/uIP\_Demo\_Rowley\_ARM7/uip/uipopt.h. This must be set to
be on the same subnet as your host computer, and must not conflict with any other IP address on the same subnet. 

A standard CAT5 Ethernet cable can only be used if a HUB is placed between the embedded computer and your host. A cross over (or point to point)
cable is required if you want to connect directly (without a HUB).

Once correctly configured use any HTTP client (such as Internet Explorer) to make a connection by typing 'http://nnn.nnn.nnn.nnn'
into the address bar - obviously replacing the nnn's with the correct IP address.

### Demo Application Functionality

The demo application creates 12 of the [standard demo application tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview). 
These are included to demonstrate and test the RTOS kernel functionality.
In addition a 'Check' task is created to ensure the standard demo tasks are executing correctly. Every three seconds the 'Check' task monitors the
standard demo tasks, then toggles the yellow LED. If the yellow LED is toggling every three seconds then the 'Check' task has not discovered
any errors. If the toggle rate increases to 500ms then an error has been discovered in at least one task.

A separate task is created to execute the uIP TCP/IP stack and web server. 
The uIP Ethernet driver can only poll the Ethernet interface. The LPC-E2124 8bit interface mode does not allow for interrupt operation
of the [CS8900](http://www.cirrus.com/en/products/pro/detail/P46.html) Ethernet controller. The uIP task therefore 
operates at a high
priority, yielding processing time to the other tasks when it finds nothing to do. 

To achieve this functionality a couple of small changes were required to the uIP code provided by Paul Curtis.

* The file main.c provided with uIP was renamed uIP\_Task.c so as not to conflict with the main.c
 of the demo application. Likewise the function main() within uIP\_Task.c was renamed vuIP\_TASK()
 as it is now created as a task rather than being the application entry point.
* The yellow LED is now used by the 'check' task, rather than the uIP task.
* The timer tick count used within the embedded TCP/IP drivers has been changed to use the RTOS tick count.
* Calls to vTaskDelay() have been added to the TCP/IP driver code to yield processor time when there are no actions for the TCP/IP
 task to perform.
* The maximum number of connections was increased from 10 to 20.

### **Execution Context**

The RTOS scheduler executes in supervisor mode, tasks execute in system mode.
NOTE! : 
 The processor MUST be in supervisor mode when the RTOS scheduler is started (vTaskStartScheduler is 
 called). The demo applications included in the FreeRTOS download switch
 to supervisor mode prior to main being called. If you are not using one of
 these demo application projects then ensure Supervisor mode is entered before calling vTaskStartScheduler().

See the [LPC2000 GCC documentation](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106#configuration-and-usage-details) for a lot more 
information on the RTOS scheduler setup and usage.

### **Licensing**

Please note that the uIP stack is licensed separately to FreeRTOS. 
[Users must familiarise themselves with the license conditions](http://www.sics.se/~adam/uip/).
