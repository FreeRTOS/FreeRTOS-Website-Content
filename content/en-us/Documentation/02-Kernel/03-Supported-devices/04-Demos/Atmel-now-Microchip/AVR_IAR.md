---
title: "Atmel AVR (MegaAVR) / IAR RTOS Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![STK500.jpg](/media/2018/STK500.jpg)

There are currently two ports for the ATmega323/ATmega32 and ATmega128 - one using the [IAR Embedded WorkbenchTM](http://www.iar.com/) for AVR,
and one using [WinAVR (GCC)](http://winavr.sourceforge.net/). This page provides information on the IAR Embedded Workbench for AVR (EWAVR) port only.

There are also ports available for the [ATmega320x/480x](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-atmega-0-demo) and
the [AVR Dx](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-avr-dx-demo), for WINAVR (AVR GCC), MPLAB XC8 and IAR Embedded Workbench for AVR.

The AVR IAR demo application is configured to run on an Atmel
[STK500](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500)
prototyping board using an AVR ATMega323 embedded processor running at 8MHz ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)
are provided should you wish to use an alternative development board). If an
ATMega32 is used the frequency can be increased to 16MHz. The port is also being used with ATMega128 processors.

The 2KBytes of RAM on the ATMega323 is enough to run 10 real time tasks - including the idle task.

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### IMPORTANT! Notes On Using The AVR/IAR RTOS Port:

_Please read all the following points before using this port._

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organization

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The AVR WinAVR demo application makefile is located in the Demo/AVR_ATMega323_IAR directory.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the Mega AVR IAR RTOS port.

#### Demo application hardware setup

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

1. In IAR Embedded Workbench, open the project Demo/AVR_ATMega323_IAR/rtosdemo.eww.

2. From the Project menu select Options - the project options dialogue box will open.

3. In the project options dialogue box, select the XLINK category. If you want to create a debug build select
   the Debug Info radio button. If you want to create a release build select the "other" radio button and ensure the
   output is set to Intel-Extended.

4. Close the options dialogue, then select Make from the Project menu.

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

Configuration items specific to this port are contained in Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h.
The constants defined in this file can be edited to suit your application. In particular - the definition
configTICK_RATE_HZ is used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for
testing the RTOS kernel functionality but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType_t' to equal the most efficient data type for that processor. This port defines
BaseType_t to be of type char.

#### Using the Embedded Workbench simulator

The Embedded Workbench simulator requires interrupt sources to be configured through the Simulator menu item,
or by the use of a macro. If you want to run the demo application in the simulator you must first manually "install" the
timer 1 compare match A interrupt by using the Simulator | Interrupts menu item.

#### To use a part other than an AVR ATMega323

1. Change the MCU definition within the Embedded Workbench project file.

2. Set the correct clock frequency in Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h

3. The tick ISR is generated from a compare match on timer 1. Timer configuration is not identical
   across all AVR devices. Check the function prvSetupTimerInterrupt() in Source/portable/IAR/ATMega323/port.c to see
   if any modifications are required for your chosen device.

4. Ensure the configTOTAL_HEAP_SIZE definition is set to fit within the available RAM.

5. Replace the inclusion of the iom323.h header file within Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h **and**
   Source/portable/IAR/ATMega323/portmacro.s90 with the correct header for your chosen microcontroller.

Whichever part is used, ensure the MCU fuses are blown to provide the correct clock frequency (this can be done from the
AVR Studio development tools).

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE_PREEMPTION within Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Memory management

Source/Portable/MemMang/heap_1.c is included in the MegaAVR demo application makefile to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Development tools

The IAR port is adapted from the WinAVR port. As a more specialised and targeted product the IAR compiler does not have the same
flexibility as the more generic GCC based WinAVR compiler. Adapting the code has therefore resulted in the following points to
be taken into consideration:

1. **Dual Task Stacks**
   The IAR compiler assumes the existence of two stacks. The "hardware" stack is used as the call stack, and the "software"
   stack is used for local variables and function parameters.

   The stack of each task is split into two sections. The size of the hardware stack section is set by the definition
   configCALL_STACK_SIZE found in the file Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h. The remaining space is used for the
   software stack. Care must be taken when deciding the stack sizes! Further comments on this can be found at the
   bottom of this page.

2. **Locked Register (R15)**
   Register R15 is defined in the project file as "locked" - making it unavailable to the compiler. R15 should also not
   be used by any application assembly code. See the comments at the bottom of the page for a method of removing this
   restriction.

3. **Assembly File**
   The IAR inline assembler is limited in function. This has resulted in the port source code requiring an
   assembler file. This is called portmacro.s90 and can be found in the Source/portable/IAR/ATMega323 directory.

4. **Interrupt Vector Table**
   Ideally the preemptive tick ISR would be defined using both the \_\_task and \_\_interrupt keywords - but the use of these
   keywords is mutually exclusive. The tick ISR is therefore defined using just the \_\_task keyword, and
   the interrupt vector populated manually. This unfortunately means that all ISR's must be added to the vector table manually
   and the '#pragma vector="ISRName"' directive cannot be used.

   To write an ISR, declare the ISR using the \_\_interrupt keyword
   then populate the vector table defined within Source/portable/IAR/ATMega323/portmacro.s90 with the ISR name.
   Instructions for doing this can be found at the top of the portmacro.s90 file. The serial ISR's included in the
   demo application can be used as an example.

5. **Compiler Warnings**
   The FreeRTOS source code has to be built with lots of different compilers. The IAR compiler has particularly strong
   (pedantic) source checking and generates several warnings when compiling the FreeRTOS source code.

   Unfortunately these warning cannot be fixed by modifying the source code as they predominantly relate to benign code that was
   added in order to fix warnings generated by other compilers (mainly relating to type casting).
   Some warnings have therefore been disabled in the project file.

   - The supplied standard libraries expect char parameters to be unsigned (in functions such as strncpy(), etc.).
     It may be possible to recompile the libraries with signed plain char's.
   - The linker complains (perhaps correctly) about the two definitions of QueueHandle_t - used for data hiding.
   - No interrupt vector being explicitly assigned to a function that uses the \_\_interrupt keyword. This warning
     has been switched off in the project file for the reasons mentioned above.

   - The use of the 'volatile' keyword within pointer casting. This warning has also been switched off in the project file.
     This is just a quirk caused by another compiler that complains if you omit the keyword.

#### Development tool options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project.

#### Demo application serial driver

The serial driver included with the demo application uses the calculation detailed in the AVR ATMega323 manual to set the baud
rate registers. At some baud rates I have found it necessary to adjust the calculated setting slightly. I suspect this is due
to an inaccuracy in the 8MHz crystal installed in my reference board and rounding errors in the calculation.

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

---

### Comments:

It is not necessary to read this section in order to use the port!

#### More on dual stacks

Two approaches could have been taken to implement the dual stack requirements. The chosen method maintains two stacks per task.
This has the following advantages ... :

- Faster context switch time.

... and the following disadvantages:

- More complex. Two stack size requirements must be calculated.
- All tasks have the same hardware stack size.
- Less memory efficient - a safety margin has to be built into two separate stack areas, rather than one.

The alternative would be to include a single hardware stack area that was shared by all the tasks. During a context switch
the hardware stack would be copied to and restored from the software stack.
This alternative method would have the following advantages ... :

- Simpler to setup.
- More memory efficient.

... and the following disadvantages:

- Slower context switch time.
- The hardware stack would require a separate memory allocation. The stack used by main() cannot be used as the
  location of its start point cannot be determined.

#### The locked R15 register

The RTOS scheduler uses R15 as per the \_\_tmp_reg\_\_ available with the WinAVR compiler. It is used as a scratch register when entering
a critical region.

The requirement to lock R15 could be removed by saving the interrupt flags onto the hardware stack instead of the software stack
(R15 could then be saved and restored to/from the software stack during the operation). This would however mean using the
hardware stack as a software stack - removing the clean separation between the two.
