---
title: "TI MSP430 (MSP430F449) RTOS Port for the CrossWorks Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ES449.gif](/media/2018/ES449.gif)

This demo was produced on an [ES449](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449) evaluation board
from [SoftBaugh](http://www.softbaugh.com/) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board),

using the [IAR Embedded Workbench for MSP430](https://www.iar.com/) development tools
and a SoftBaugh [FETP parallel
port JTAG interface](http://www.softbaugh.com/ProductPage.cfm?strPartNo=FETP)

The port and demo permit tasks to use the MSP430 low power modes 1 to 3.

---

##### IMPORTANT! Notes on using the IAR MSP430 RTOS port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)
4. [Selecting the Port to Use](#versions-of-freertos-prior-to-v510-included-two-separate-sets-of-port-layer-files-for-the-msp430)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## Source Code Organization

### The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than required to run just this demo.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The IAR workspace used to build the MSP430 FreeRTOS demo is called RTOSDemo.eww and can be located in the
Demo/msp430\_IAR directory.

---

### The Demo Application

##### Functionality

The ES449 prototyping board includes a built in LCD display and a single built in user
LED. To make use of this hardware, the standard demo tasks that would normally flash an LED, instead flash
'*' characters on the LCD. The left most '*' represents LED 0, the
next LED 1, etc.

The single on board LED is used by one of the ComTest tasks. It is toggled every time a character is received on the
serial port.

The demo application creates 10 tasks - 9 of the [standard demo application tasks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
and the idle task. When executing
correctly the demo application will behave as follows:

* The first three '*' characters on the LCD are under control of the 'flash' tasks. Each will
 flash at a constant frequency, with the first '*' being the slowest and the third being the
 fastest.
* The on board LED will flash each time a character is received on the serial port (see the hardware setup section below).
* Not all the tasks update the LCD so have no visible indication that they are operating correctly. Therefore a 'Check'
 task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 The '*' in the fifth position on the LCD is under control of the 'Check' task. Every
 three seconds the 'Check' task examines all the tasks in the system to ensure they are executing without error. It
 then toggles '*' 5. If '*' 5 is toggling every three seconds
 then no errors have ever been detected. The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error.

##### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters are transmitted by
one task and received by another - if any character is missed or received out of sequence an error condition is flagged.
Normally a loopback connector is required for this mechanism to work (so each character transmitted by the UART is also received
by the UART). In this case the 'loopback' mode of the MSP430 UART is used and no external connector is required.

The demo application uses the LCD in place of LEDs so no other hardware setup is required.

##### Building

To build the demo application:
1. Open the workspace file FreeRTOS/Demo/MSP430\_IAR/RTOSDemo.eww from within the Embedded Workbench IDE.
2. Select the required build (Debug or Release).![](/media/2018/crossstudio.gif)

 Selecting the required build

- Select "Build Solution" from the CrossStudio project menu or simply press F7.

##### Downloading and executing

To download the application to the target hardware:

	1. Connect the FETP JTAG interface between the target and host. The target will be powered via the FETP JTAG interface and no other
	 power source should be connected.
	2. Select "Connect MSP430 Flash Emulation Tool" from the CrossStudio Target menu.
	3. Select "Start Debugging" from the CrossStudio Debug menu. The MSP430 Flash will be automatically programmed
	 with the demo application.

Once the application has been programmed into flash it can executed within the CrossStudio debugger. Alternatively, stop the
debugger (to power down the target), remove the FETP JTAG interface, then supply the target with an external power
source.

---

### Configuration and Usage Details

###### Serial port driver

As provided the serial port drivers are configured for loopback mode. This enables the demo application to execute but
switch loopback mode off for any other use.

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution.

##### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/MSP430\_CrossWorks/FreeRTOSConfig.h. The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type short.

Note that vPortEndScheduler() has not been implemented.

##### To use a part other than an MSP430F449

The core real time kernel components should be
portable across all MSP430F4xx devices - but the peripheral setup and memory requirements will require consideration.
Items to consider:

	* prvSetupTimerInterrupt() in Source/portable/Rowley/MSP430F449/port.c configures the microcontroller timer to generate
	 the RTOS tick.
	* Port, memory access and system clock configuration is performed by prvSetupHardware() within Demo/MSP430\_CrossWorks/main.c.
	* The serial port drivers.
	* Register location definitions are provided by the file msp430x44x.h which is included at the top of
	 Demo/MSP430\_CrossWorks/FreeRTOSConfig.h.
	* RAM size - see Memory Allocation below.
##### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/MSP430\_CrossWorks/FreeRTOSConfig.h to 1 to use pre-emption or 0 to use
co-operative.

##### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project.

##### Memory allocation

Source/Portable/MemMang/heap\_1.c is included in the MSP430 demo project to provide the memory allocation required
by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

---

## Interrupt Service Routines

### Versions of FreeRTOS prior to V5.1.0 included two separate sets of port layer files for the MSP430:

	1. The officially supported version that uses the extensions provided by the Rowley compiler to implement interrupt service routines completely in C.
	2. A contributed port that required interrupt service routines to have assembly function wrappers.

FreeRTOS V5.1.0 only includes the officially supported version but introduces a pre-processor macro and a new header file that allows the users to define
which method of writing interrupt service routines will be used. The following sections describe the steps required to use both methods.
The UART driver within the supplied demo application also demonstrates both methods.

Method 1 only requires C code so is simpler to implement than method 2. It only saves and restores the task context when a context switch is actually
required, so can also be more efficient. However - a context switch being performed within the interrupt will result in some processor registers being
saved twice (once on interrupt entry, and then again for the context switch). This means the stack allocated to each task will need to be larger when
using method 1 compared to that required when using method 2.

##### Writing ISRs - Method 1

To use method 1:

	1. Set the pre-processor macro configINTERRUPT\_EXAMPLE\_METHOD to 1. The supplied demo application defines configINTERRUPT\_EXAMPLE\_METHOD within FreeRTOSConfig.h.
	2. Use the \_\_interrupt[ ] function qualifier to implement interrupt service routines within C files.
	3. If using low power modes - ensure \_\_bic\_SR\_register\_on\_exit(SCG1 + SCG0 + OSCOFF + CPUOFF) is called prior to exiting the interrupt service routine.
	4. Use the standard taskYIELD() macro should a context switch be required from within the interrupt routine.

Below is an example UART Rx interrupt written using method 1.

---

```c

void vRxISR( void ) __interrupt[ UART1RX_VECTOR ]
{
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Get the character from the UART and post it on the queue of Rxed
 characters. */
    cChar = U1RXBUF;

    xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );

    if( xHigherPriorityTaskWoken )
    {
        /*If the post causes a task to wake force a context switch
 as the woken task may have a higher priority than the task we have
 interrupted. */
        taskYIELD();
    }

    /* Make sure any low power mode bits are clear before leaving the ISR. */
    __bic_SR_register_on_exit( SCG1 + SCG0 + OSCOFF + CPUOFF );
}
```

---

Writing an ISR using method 1
##### Writing ISRs - Method 2

To use method 2:

	1. Set the pre-processor macro configINTERRUPT\_EXAMPLE\_METHOD to 2. The supplied demo application defines configINTERRUPT\_EXAMPLE\_METHOD within FreeRTOSConfig.h.
	2. Provide an assembly function that will be installed as the interrupt handler routine. The required format of this function is demonstrated below. Note the assembly file must include the portasm.h header file to gain access to the required portSAVE\_CONTEXT and portRESTORE\_CONTEXT assembly macros.
	3. Provide a standard C function that is called by the assembly file wrapper to perform the actual interrupt handling work - again see below for an example.
	4. Use the portYIELD\_FROM\_ISR() macro should a context switch be required from within the interrupt routine.

Below are examples of both the assembly file wrapper and C function portions of the interrupt implementation.

---

```c

/* Ensure the required header files are included. */
### include "FreeRTOSConfig.h"
### include "portasm.h"

.CODE

/* Example wrapper for the Rx UART interrupt. */
_vUARTRx_Wrapper:

    /* portSAVE\_CONTEXT must be the first macro to be called. This is defined within
 portasm.h. */
    portSAVE_CONTEXT

    /* Following portSAVE\_CONTEXT the C portion of the handler can be called. */
    call #_vRxISR

    /* Finally portRESTORE\_CONTEXT must be called at the end of the wrapper. This too
 is defined within portasm.h. */
    portRESTORE_CONTEXT

/*******************************************************************************************/

    /* The wrapper must be installed as the interrupt handler. */

    .VECTORS
    .KEEP

    ORG    UART1RX_VECTOR
    DW    _vUARTRx_Wrapper

    END
```

---

The assembly file portion of the ISR

---

```c

/* This is the standard C function called by the assembly file wrapper. */
void vRxISR( void )
{
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Get the character from the UART and post it on the queue of Rxed
 characters. */
    cChar = U1RXBUF;

    xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );

    /*If the post causes a task to wake force a context switch
 as the woken task may have a higher priority than the task we have
 interrupted. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```

---

The C function called from the assembly file wrapper