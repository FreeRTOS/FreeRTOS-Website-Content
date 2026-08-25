---
title: "PIC24 MCU and dsPIC® DSC RTOS ports"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2024/boardDebugger.jpg)

This page presents the FreeRTOS port and demo application for
[Microchip's dsPIC microcontroller](https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/dspic-dscs) and
[Microchip's PIC24 microcontroller](https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/16-bit-mcus) offerings.

Multiple demo applications are provided for different family of devices. Majority of demos are targeted at the Explorer16 Development Board
(instructions are provided should you wish to use an alternative development board) and utilise the Microchip's [XC16 or XC-DSC](https://www.microchip.com/xc).
Some demos use other development boards(Curiosity Platform Development boards), please refer the individual demo README file for board and compiler details.

---

#### IMPORTANT! Notes on using the PIC24 and dsPIC33 ports

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

The demo code for different device variants can be located in the  PIC24_DSPIC_MPLABX\Demo directory.

Device and project specific files are placed under each separate folder and common folder contains the common code.

---

### The Demo Application

This section relates to both the PIC24 and dsPIC33 demo applications.

#### Demo application hardware setup

All the Explorer 16 jumpers can remain in their default positions - in particular, JP2 should be fitted to ensure correct operation of the LEDs.

The demo application includes tasks that send and receive characters over UART. The characters sent by one task are received by another - with an error condition being flagged
should any characters be missed or received out of order. UART TX and RX pins needs to be shorted, for the exact pin numbers please refer the readme inside individual projects.

For device specific hardware setup please refer the readme available in each project directory.

### Functionality

The demo application creates fourteen tasks (including the idle task), five co-routines, and a high frequency interrupt test. When executing correctly the demo will behave as follows:
* LEDs marked D3 to D7 are under control of the 'flash' co-routines. Each will flash at a constant frequency, with LED D3 being the fastest and LED D7 being the slowest.
 This provides a basic example of how co-routines can be mixed with tasks.
* LED D9 will toggle each time a character is transmitted on the serial port. The frequency is such that you cannot distinguish the individual toggles between characters,
 although the spacing between complete message transfers can be viewed.
* LED D10 will flash each time a character is received and validated on the serial port (though the loopback connector).
 Again the frequency is too fast to distinguish the individual toggles.
* Most of the tasks do not update an LED so have no visible indication that they are operating correctly. Therefore a 'Check' task is created whose job it is to ensure that
 no errors have been detected in any of the other tasks or co-routines. The check task monitors the system operation every 3 seconds then writes a PASS or FAIL message to the LCD.
 Any failures are latched, and the message displayed indicates in which task the failure was detected (this functionality can be tested by removing the loopback connector
 while the demo is executing). The PASS message is a time measurement in nano seconds, as described in the next bullet point.
* A high frequency periodic interrupt is generated using a free running timer to demonstrate the use of the configKERNEL_INTERRUPT_PRIORITY configuration constant.
 The interrupt service routine measures the number of processor clocks that occur between each interrupt - and in so doing measures the jitter in the interrupt timing.
 The maximum measured jitter time is latched in the usMaxJitter variable, and displayed on the LCD by the 'Check' task as just described. The interrupt frequency is set to 20KHz.
 This test demonstrates how the RTOS kernel can be configured such that is has no impact on the latency of interrupt service routines.
* The application also demonstrates the use of a 'gatekeeper' task, in this case an LCD gatekeeper. The LCD task is the only task that is permitted to access the LCD directly.
 Other tasks wishing to write a message to the LCD send the message on a queue to the LCD task instead of accessing the LCD themselves. 
 The LCD task just blocks on the queue waiting for messages - waking and displaying the messages as they arrive.

Note: On devices with less memory will have less number of tasks.

### Building and executing the demo application

These instructions assume you have MPLABX and the XC16 or XC-DSC compiler correctly installed on your host computer.

To build the application:

1. Open the demo application workspace from within the MPLABX IDE.
2. Right click on the project and click on "Clean and Build" or You can also go to "Production" and click on "Clean and Build Main Project"

To run the application in the MPLABX simulator:

1. Right click and select Project Properties. In the "Connected Hardware Tool" drop down select the "simulator"
2. Set a break point on the first instruction within the main() function (contained within main.c).
3. From the 'Debug' menu, select 'Debug Main Project'(Make sure you set the project as the main project, right click on project then select "Set as Main Project").
 The application will start executing, stopping when the break point is reached. The application can then be manipulated using the standard debugger commands.

When executing within the simulator, the standard ComTest receive task will not receive any characters (there is no loopback connector),
 causing the 'check' task to detect an error within the communications test tasks.

To debug the application on the Explorer 16 using the [ICD or PICKit](https://www.microchip.com/en-us/tools-resources/debug/programmers-debuggers) interface:

1. Connect the ICD or PICKit to the Explorer 16/32 development board or the any other applicable board as described in the board manual.
2. Right click and select Project Properties. In the "Connected Hardware Tool" drop down select the listed ICD or PICKit device.
3. Again from the 'Debug' menu, select 'Debug Main Project'.
4. Set a break point on the first instruction within the main() function (contained within main.c).
5. From the 'Debug' menu, select 'Continue'. The application will start executing, stopping when the break point is reached.
 The application can then be manipulated using the standard debugger commands.

To run the application stand alone from the microcontroller flash:

1. Connect the ICD or PICKit to the Explorer 16/32 development board or the any other applicable board as described in the board manual.
2. From the 'Production' menu within the MPLABX IDE, select 'Make and Program Device Main Project'.
3. Remove power from the board, then remove the ICD or PICKit interface cable.
4. Finally, apply power again to start the application executing.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in PIC24_DSPIC_MPLABX/Demo/[dspic33c-client-freertos-demo | dspic33c-host-freertos-demo |
 dspic33e-freertos-demo | dspic33f-freertos-demo | pic24-freertos-demo]/FreeRTOSConfig.h. The constants defined in this file can be edited to suit your application.
 In particular -

* **configTICK\_RATE\_HZ**
  This sets the frequency of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications require.
  Lowering this value will improve efficiency.
* **configKERNEL\_INTERRUPT\_PRIORITY**
  This sets the interrupt priority used by the RTOS kernel. The RTOS kernel should use a low interrupt priority, allowing higher priority interrupts
  to be unaffected by the RTOS kernel entering critical sections. Instead of critical sections globally disabling interrupts, they only disable interrupts
  that are below the RTOS kernel interrupt priority.

  This permits very flexible interrupt handling:

    1. At the RTOS kernel priority level interrupt handling 'tasks' can be written and prioritised as per any other task in the system.
     These are tasks that are woken by an interrupt. The interrupt service routine (ISR) itself should be written to be as short as it possibly can be
     - it just grabs the data then wakes the high priority handler task. The ISR then returns directly into the woken handler task - so interrupt processing is contiguous
     in time just as if it were all done in the ISR itself. The benefit of this is that all interrupts remain enabled while the handler task executes.
    2. ISR's running above the RTOS kernel priority are never masked out by the RTOS kernel itself, so their responsiveness is not effected by the RTOS kernel functionality.
     However, such ISR's cannot use the FreeRTOS API functions. The fast timer interrupt test within this demo demonstrates this configuration.

    Unfortunately, due to limitations in the GCC inline assembler, modifications to this value will necessitate a small update to the port source code
     with respect to the interrupt mask value (accessed by inline assembler instructions). A #error directive has been included in the port source code
     to indicate the location of the required update, and provide instruction on the update that is required. 

Each port #defines 'BaseType_t' to equal the most efficient data type for that processor. This port defines BaseType_t to be of type short.

Note that vPortEndScheduler() has not been implemented.

### Device specific configuration

xc.h is included at the top of FreeRTOSConfig.h which will include the associated device header file.

#### Interrupt service routines

Interrupt service routines that cannot cause a context switch have no special requirements and can be written as per the compiler documentation.

Interrupt service routines that can cause a context switch must execute with priority portKERNEL_INTERRUPT_PRIORITY, and only call taskYIELD()
at the very end of the service routine after the interrupt source has been cleared. See the file serial.c included in the demo application for an example.

#### Critical sections

Exiting a critical section will always set the interrupt priority mask to zero (all interrupts enabled), no matter what its level when the critical section
was entered. FreeRTOS API functions themselves will use critical sections.

#### Shadow registers

The shadow registers are not saved as part of the task context.

#### PSV bit handling

The PSV bit within CORCON register must be set identically for every task. If it is necessary to change the default bit setting this must be done prior to any tasks being created.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE_PREEMPTION within PIC24_DSPIC_MPLABX/Demo/[dspic33c-client-freertos-demo | dspic33c-host-freertos-demo | dspic33e-freertos-demo | dspic33f-freertos-demo | pic24-freertos-demo]/FreeRTOSConfig.h to 1 to use pre-emption or 0 to use co-operative. The demo application will only execute correctly with configUSE_PREEMPTION set to 0 if configIDLE_SHOULD_YIELD is set to 1.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap_1.c is included in the PIC24 and dsPIC33 demo application projects to provide the memory allocation required by the RTOS kernel.
Please refer to the Memory Management section of the API documentation for full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not intended to represent an optimized solution.

