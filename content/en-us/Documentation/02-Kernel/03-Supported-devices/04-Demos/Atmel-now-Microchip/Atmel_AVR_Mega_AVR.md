---
title: "Atmel AVR (MegaAVR) / WinAVR Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Atmel AVR (MegaAVR) / WinAVR Port

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![STK500.jpg](/media/2018/STK500.jpg)

There are currently two ports for the ATmega323/ATmega32 and ATmega128 - one which uses the [IAR Embedded WorkbenchTM](https://www.iar.com/) for AVR, and one using [WinAVR (GCC)](http://winavr.sourceforge.net/). This page provides information on the WinAVR port only.

There are also ports available for the [ATmega320x/480x](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-atmega-0-demo) and the [AVR Dx](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-avr-dx-demo), for WINAVR (AVR GCC), MPLAB XC8 and IAR Embedded Workbench for AVR.

The AVR WinAVR demo application is configured to run on an Atmel
[STK500](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500)
prototyping board using an AVR ATMega323 embedded processor running at 8MHz ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board). If an
ATMega32 is used the frequency can be increased to 16MHz. The port is also being used with ATMega128 processors.

The 2KBytes of RAM on the ATMega323 is enough to run 10 real time tasks - including the idle task.

From V4.1.0 the AVR demo application demonstrates the use of co-routines.

---

#### IMPORTANT! Notes On Using The AVR/WinAVR RTOS Port:

*Please read all the following points before using this port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The AVR WinAVR demo application makefile is located in the Demo/AVR\_ATMega323\_WinAVR directory.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the Mega AVR GCC RTOS port.

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the serial port connector).

For best effect LEDs should be connected to the eight data lines on the standard PC parallel port.
Omitting these LEDs will not cause the RTOS demo application
to fail, but will remove some visual feedback that everything is working as expected.

The following links must be in place on the STK500 prototyping board for the demo application to operate - these can be
seen on the photograph above:

1. PORTB to LEDS
2. PORTD bits 0 and 1 to RS
3. SPROG3 to ISP6PIN (correct link to program an AVR ATMega323)

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on
the serial port connector).

#### Building the RTOS demo application

FreeRTOS V3.0.0 has replaced the batch files previously used to build the demo application with a single makefile. This
was made possible by improvements in ELF and COFF format support in the later versions of WinAVR.

To build the demo application:

1. Ensure that WinAVR is correctly installed and accessible from your PATH environment.
2. Open a command prompt and navigate to the Demo/AVR\_ATMega323\_WinAVR directory.
3. Type 'make' to build the project. The project should build with no errors or warnings.
4. To force a complete rebuild type 'make clean'
5. The optimisation level (option -O) and debug level (option -g) can be adjusted within the makefile to
 suit your application requirements.

The build process will generate a file called RTOSDemo.elf which is suitable for executing and debugging within the
free Atmel AVR Studio IDE, and a file called RTOSDemo.hex which is suitable for burning into the processor.

Ensure the -g option is used within the makefile when generating files for debug and simulation.

#### Functionality

The RTOS demo application creates 10 of the standard demo tasks.
 1. LEDs 0 to 2 are under control of the standard 'flash' co-routines and flash at a regular rate.
 Each LED is flashed by a separate task.
2. LEDs 4 and 5 are under control of the standard 'comtest' tasks. LED 4
 toggles every time an RS232 character is transmitted. LED 5 toggles
 every time an RS232 character is received and verified.
3. Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the
 other tasks.
 LED 7 is under control of the 'check' task. LED 7 will flash every few seconds provided no errors have been
 detected in any of the other real time tasks. If an error is detected in any other task then LED 7 will
 stop flashing.

See the [standard demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for full details of the
demo application tasks.

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/AVR\_ATMega323\_WinAVR/FreeRTOSConfig.h.
The constants defined in this file can be edited to suit your application. In particular - the definition
configTICK\_RATE\_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type char.

#### To use a microcontroller other than an AVR ATMega323

1. Change the MCU definition at the top of the makefile.
2. Set the correct clock frequency in Demo/AVR\_ATMega323\_WinAVR/FreeRTOSConfig.h
3. Ensure the configTOTAL\_HEAP\_SIZE definition is set to fit within the available RAM.
4. The tick ISR is generated from a compare match on timer 1. Timer configuration is not identical
 across all AVR devices. Check the function prvSetupTimerInterrupt() in Source/portable/GCC/ATMega323/port.c to see
 if any modifications are required for your chosen device.

Whichever part is used, ensure the MCU fuses are blown to provide the correct clock frequency (this can be done from the
AVR Studio development tools).

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/AVR\_ATMega323\_WinAVR/FreeRTOSConfig.h to 1
to use pre-emption or 0 to use co-operative.

#### Memory management

Source/Portable/MemMang/heap\_1.c is included in the MegaAVR demo application makefile to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Development tool options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application makefile.

#### RTOS Demo application serial port driver

The serial port driver included with the demo application uses the calculation detailed in the AVR ATMega323 manual to set the baud
rate registers. At some baud rates I have found it necessary to adjust the calculated setting slightly. I suspect this is due
to an inaccuracy in the 8MHz crystal installed in my prototyping board and rounding errors in the baud calculation.

It should also be noted that the serial drivers are written to test some of the RTOS kernel features - and they are not
intended to represent an optimised solution.

#### Notes for Linux users

I have only tested the makefile from a Win2K host but hopefully it is also compatible with Linux builds of GCC.
