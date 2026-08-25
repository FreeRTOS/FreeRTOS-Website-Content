---
title: "Atmel AT91SAM9 (ARM9) port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Using the [IAR Development Tools](http://www.iar.com/ewarm)

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/AT91SAM9XE-RTOS.jpg)

This page presents the demo application for the Atmel SAM9XE ARM9 microcontroller.

The demo is pre-configured to use the IAR Embedded Workbench development tool chain and run on the
[AT91SAM9XE-EK Evaluation Board](http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=AT91SAM9XE-EK).

**Note:** If this project fails to build then it is likely the version of IAR
Embedded Workbench being used is too old. If this is the case, then it is also
likely that the project file has been (silently) corrupted and will need to be
restored to its original state before it can be built even with an updated IAR version.

---

#### _IMPORTANT! Notes on using the Atmel ARM9 RTOS port_

_Please read all the following points before using this RTOS port._

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports so contains many more files than
required by this demo. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for
a description of the downloaded files and information on creating a new project.

The IAR workspace for the FreeRTOS AT91SAM9 demo is called RTOSDemo.eww and can be located in the
FreeRTOS/Demo/ARM9_AT91SAM9XE_IAR directory. The workspace contains a single project that has two configurations - one
to run the demo in ARM mode and the other to run the demo in THUMB mode.

---

### The Demo Application

#### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on UART0 for this mechanism to operate (simply connect pins 2 and 3 together on
connector J20).

The demo application uses the LEDs built into the prototyping board so no other hardware setup is required.

#### Functionality

The demo project creates 37 tasks before starting the RTOS scheduler. Most of these tasks consist of the 'standard demo' tasks - the purpose
of these tasks is to both demonstrate the RTOS API and test the RTOS port. They do not in themselves perform any other useful function.

A 'check' task is also created. This only executes
every three seconds but has a high priority so is guaranteed to get processing time.
Each time it executes it inspects the status of all the other tasks in the system to see
if any of them are reporting an error. The check task will toggle an LED every 3 seconds
provided all the other tasks are running as expected. The toggle rate will change to 500ms
if an error is discovered in any task.

When executing correctly the demo will behave as follows:

- LED DS1 is under the control of the 'check' task. It will toggle every three seconds provided all the other tasks are
  functioning correctly. If the toggle rate increases to 500ms then at least one task has reported an error. This
  mechanism can be tested by removing the loopback connector from the serial port - and in so doing deliberately introducing
  an error in the standard 'comtest' tasks.

- LED DS5 is under control of the standard 'comtest' transmit task. It will toggle each time a character is successfully transmitted.
  The toggle rate is too fast to be able to visually distinguish between each character, but the LED does provide some feedback as to
  when complete messages have been transmitted.

#### Building the demo application

1. Open the FreeRTOS/Demo/ARM9_AT91SAM9XE_IAR/RTOSDemo.eww workspace from within the IAR Embedded Workbench IDE.

2. Select either the ARM or THUMB configuration as required.

   ![](/media/2018/SAM9-Free-RTOS-Select_Configuration.jpg)

   Selecting between ARM and THUMB configurations.

3. Press F7 - the project should build with no errors or warnings.

#### Running the demo application

1. Ensure the J-Link JTAG debug interface is connected and that the prototype board is power up.

2. Select 'Download and Debug' from the IDE 'Project' menu.

3. The microcontroller SDRAM memory will automatically be programmed with the demo application, and the debugger
   will break at the start of main().

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this port are contained in DemoARM9_AT91SAM9XE_IARFreeRTOSConfig.h. The constants
defined in this file can be edited to suit your application. In particular - the definition configTICK_RATE_HZ is used to
set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is
faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType_t' to equal the most efficient data type for that processor. This port defines
BaseType_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

Often you will require an interrupt service routine to cause a context switch. For example a serial port character being
received may unblock a task that was blocked waiting for the character. If the task that was interrupted by the ISR has
a priority lower than the unblocked task then the ISR should return directly into the unblocked higher priority task. The
interrupt will have interrupted one task but returned to another.

FreeRTOS has two options to achieve this on the ARM7 and ARM9:

1. The IRQ vector can be configured to jump directly to the interrupting peripheral. When this is the case
   the context of the currently executing task must be saved on interrupt entry, and the context of the newly selected task
   must be restored on exit from the interrupt. The context saving and restoring has to be added to each interrupt that
   might want to perform a yield. Macros provided by FreeRTOS can be used to perform all the necessary actions.

2. The IRQ vector can be configured to always jump to a single interrupt entry point. When this is done the IRQ handler
   saves the context of the currently running task before calling the user defined interrupt handler code, and then restores
   the context of the next task to run when the user defined handler code returns. The user defined task is then just a
   standard C function that does not need to concern itself about context saving or restoring.

This demo is configured to use the second method. This means the central IRQ entry point takes care of the context switching
and the user supplied interrupt handler can be a standard ARM mode C function.

##### An example of an ISR with context switching capabilities

Below is a copy of the example UART driver provided with the demo (note this is intended to demonstrate the API functions
and is **not** an example of an efficient ISR implementation!).

This is just a normal ARM mode function. A call to portEND_SWITCHING_ISR() is used to inform the RTOS kernel that a different
task should be selected as the task to run when the interrupt exits. The actual saving and restoring of the task context
is done automatically outside of this function.

```c
/* This is a standard ARM mode function. Note that the __irq qualifier is not
   used. */
__arm void vSerialISR( void )
{
unsigned long ulStatus;
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* What caused the interrupt? */
    ulStatus = serCOM0->US_CSR;
    serCOM0->CSR &= serCOM0->US_IMR;

    if( ulStatus & AT91C_US_TXRDY )
    {
        /* The interrupt was caused by the THR becoming empty. Are there any
           more characters to transmit? */
        if( xQueueReceiveFromISR( xCharsForTx, &cChar, &xHigherPriorityTaskWoken )
                                                                       == pdTRUE )
        {
            /* A character was retrieved from the queue so can be sent to the
               THR now. */
            serCOM0->US_THR = cChar;
        }
        else
        {
            /* Queue empty, nothing to send so turn off the Tx interrupt. */
            vInterruptOff();
        }
    }

    if( ulStatus & AT91C_US_RXRDY )
    {
        /* The interrupt was caused by a character being received. Grab the
           character from the RHR and place it in the queue or received
           characters. */
        cChar = serCOM0->US_RHR;
        xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );
    }

    /* If a task was woken by either a character being received or a character
       being transmitted and the woken task has a higher priority than the current
       task then we need to switch to another task. xHigherPriorityTaskWoken will
        have automatically been set to pdTRUE if this is the case. */
    portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );

    /* End the interrupt in the AIC. */
    AT91C_BASE_AIC->AIC_EOICR = 0;
}
```

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project file - as described in the [Source Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section.

#### Execution Context

The RTOS scheduler executes in Supervisor mode, tasks execute in System mode.

**NOTE!**:
The processor MUST be in supervisor mode when the RTOS scheduler is started (vTaskStartScheduler is
called). The demo applications included in the FreeRTOS download switch
to supervisor mode prior to main() being called. If you are not using one of
these demo application projects then ensure Supervisor mode is entered before calling vTaskStartScheduler().

Interrupt service routines always run in ARM mode. All other code executes in ARM or THUMB mode depending on the configuration
selected.

SWI instructions are used by the real time kernel and can therefore not be used by the application code.

'System Interrupts' can be generated from more than one source. Currently all system interrupts are assumed to originate from
the PIT (periodic interval timer). The use of any other system interrupts will necessitate some wrapper code to ascertain the
interrupts origin.

#### Memory allocation

Source/Portable/MemMang/heap_1.c is included in the ARM7 demo application project to provide the memory allocation
required by the real time kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Serial port driver

It should also be noted that the serial drivers are written to test some of the real time kernel features - and they are not
intended to represent an optimised solution. In particular they do not make use of the Peripheral Data Controller.
