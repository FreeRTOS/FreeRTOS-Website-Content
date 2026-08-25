---
title: "ColdFire V2 (MCF52221) RTOS Demo Using the CodeWarrior Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/FreeScale-ColdFire-M52221DEMO.jpg)

This page presents the FreeRTOS CodeWarrior port and demo application for the
[V2 ColdFire](http://www.freescale.com/webapp/sps/site/taxonomy.jsp?nodeId=0162468rH3YTLC00M95448) core
from Freescale.

Port highlights include full interrupt nesting support and no special coding requirements when writing interrupt service routines.

The port and demo are preconfigured to use:

* An [MCF52221 ColdFire MCU](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=MCF5222X&webpageId=1113331549638725695448&nodeId=0162468rH3YTLC00M95448&fromPage=tax).
* The [M52221DEMO evaluation board](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M52221DEMO) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board).
* The free [CodeWarrior for ColdFire Special Edition](http://www.freescale.com/webapp/sps/site/overview.jsp?nodeId=01272600610BF1) tool chain.

---

#### IMPORTANT! Notes on using the CodeWarrior V2 ColdFire RTOS port

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

The CodeWarrior project for the ColdFire MCF52221 demo is contained in the FreeRTOS/Demo/ColdFire\_MCF52221\_CodeWarrior directory. Note that this is a
project file, not a workspace file.

---

### The Demo Application

#### Demo application hardware setup

The M52221DEMO hardware includes a PE Micro BDM interface circuit allowing the evaluation board to be
connected directly via a USB cable to the host PC. Power can be sourced from the same USB connection by
setting the jumper marked PWR\_SEL to VB.

The demo application includes an interrupt driven UART test where one task transmits characters that are then
received by another task. For correct operation of this functionality a loopback connector must be fitted to the
COM connector of the M52221DEMO hardware (pins 2 and 3 must be connected together on the 9Way connector - a paper
clip is normally sufficient for the purpose).

The demo application uses the LEDs built onto the evaluation board so no further hardware setup is required.

#### Functionality

The demo project creates 24 tasks and 3 co-routines before starting the RTOS scheduler. These tasks do not perform
any particular function other than to demonstrate and test the ColdFire / CodeWarrior port.

When executing correctly the demo will behave as follows:

* LEDs marked LED1, LED2 and LED3 are under control of the very simple 'flash' co-routines. Each
 will flash at a constant frequency, with LED1 being the fastest and LED3 being the slowest. The co-routines
 are scheduled from within the idle task hook function.
* Most of the tasks do not update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the
 other tasks. The check task only executes every few seconds, but has a high priority so is guaranteed to get
 processing time when required. The check task will toggle the LED marked LED4 once every 5 seconds if all the
 demo tasks are executing as expected. The toggle rate will increase to 500ms should an error be detected in
 any task. This mechanism can be tested by removing the loopback connector from the COM connector to deliberately
 generate an error.

More information is provided within the comments of the source code.

The provided demo is configured with the RTOS kernel using interrupt priority 1 and the UART using interrupt priority 3 so
UART interrupts can nest within kernel interrupts. The deeper the nesting depth you permit the greater the stack size
consumed - configCHECK\_FOR\_STACK\_OVERFLOW needs to be set to 2 to catch overflows caused by deep nesting, but this should
be used for debug purposes only as it will slow down the context switch operation. The demo application dumbly assigns the
same stack size to each task rather tuning each stack to ensure RAM is not wasted.

#### Building the demo application

1. Open the DemoColdFire\_MCF52221\_CodeWarriorRTOSDemo.mcp project file from within the CodeWarrior IDE (note this
 is a project file not a workspace file so should be opened using "File | Open" menu item, NOT the "File | Open Workspace" menu item).
2. Press F7 - the project should build with no errors or warnings.

CodeWarrior has been known to randomly change the port.c and portasm.S files included in the project to the PC versions.
If you find you are receiving lots of errors and warnings from these two files then ensure the port.c and portasm.S files
actually being built are those located in the FreeRTOSSourceportableCodeWarriorColdFire\_V2 directory.

#### Programming the microcontroller flash memory

1. Open the flash programming utility by selecting "Flash Programmer" from the IDE "Tools" menu.
2. Click the "Load Settings" button (highlighted in red below) to open a list of XML files that
 describe each supported device. Select the XML file called MCF52221\_INTFLASH.xml - assuming the
 MCF52221 microcontroller is being used.

![](/media/2018/CodeWarrior-flash-programmer-load-settings.jpg)

 Opening the MCF52221 configuration xml file
3. Click "Erase / Blank Check" within the flash programming window (highlighted in red below) to reveal the "Erase" button.

![](/media/2018/CodeWarrior-flash-programmer-erase.jpg)

 Clicking "Erase / Blank Check" to reveal the "Erase" button
4. Click the "Erase" button - after a few seconds you should receive a message stating that the Erase was successful.
5. Click "Program / Verify" (highlighted in red below) to reveal the "Program" button.

![](/media/2018/CodeWarrior-flash-programmer-program.jpg)

 Clicking "Program / Verify" to reveal the "Program" button
6. Click the "Program" button - after a few seconds you should receive a message stating that the
 demo application has been correctly programmed into the ColdFire flash memory.

#### Starting a debug session

Having first followed the instructions to program the flash memory and closed the flash programming window - click the "Run" speed button,
highlighted below. The standard CodeWarrior debug window will open, from where all the standard debugging actions can be performed.

![](/media/2018/CodeWarrior-run-speed-button.jpg)

 The "Run" speed button used to start a debug session

---

### Configuration and Usage Details

#### RTOS port specific configuration

Configuration items specific to this demo are contained in [FreeRTOS/Demo/ColdFire\_MCF52221\_CodeWarrior/sources/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization). The
constants defined in this file can be edited to suit your application. In particular -

* **configKERNEL\_INTERRUPT\_PRIORITY** and **configMAX\_SYSCALL\_INTERRUPT\_PRIORITY**
See the [interrupt configuration](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) section of the RTOS kernel configuration documentation for full information on
 these options.

 configKERNEL\_INTERRUPT\_PRIORITY sets the interrupt priority used by the RTOS kernel itself. configMAX\_SYSCALL\_INTERRUPT\_PRIORITY sets the highest interrupt priority
 from which queue and semaphore API functions can be called (note that only API functions that end in FromISR() can be called from within an ISR).

 configKERNEL\_INTERRUPT\_PRIORITY should be set to the lowest priority.

 Interrupts above configMAX\_SYSCALL\_INTERRUPT\_PRIORITY will not be masked out by RTOS kernel critical sections and will therefore be unaffected
 by RTOS kernel activity - within the limitations imposed by the hardware itself.

 By way of demonstration, the demo application defines configMAX\_SYSCALL\_INTERRUPT\_PRIORITY to be 4 and configKERNEL\_INTERRUPT\_PRIORITY to be 1.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type long.

Note that vPortEndScheduler() has not been implemented.

#### Writing interrupt service routines

Interrupt service routines can be written in C using the standard CodeWarrior \_\_declspec(interrupt) function qualifier.
The macro portEND\_SWITCHING\_ISR() is provided to allow an interrupt routines to request a context switch to be performed.
The code below demonstrates an example UART interrupt handler. Note this example is not intended to demonstrate an efficient interrupt implementation!

---

```c

/* The \_\_declspec qualifier is used to tell the compiler the function is an ISR. */
__declspec(interrupt:0) void vUART0InterruptHandler( void )
{
unsigned char ucChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE, xDoneSomething = pdTRUE;

  while( xDoneSomething != pdFALSE )
  {
    xDoneSomething = pdFALSE;

    /* Does the tx buffer contain space? */
    if( ( MCF_UART0_USR & MCF_UART_USR_TXRDY ) != 0x00 )
    {
      /* Are there any characters queued to be sent? */
      if( xQueueReceiveFromISR( xCharsForTx, &ucChar, &xHigherPriorityTaskWoken )
                                                                      == pdTRUE )
      {
        /* Send the next char. */
        MCF_UART0_UTB = ucChar;
        xDoneSomething = pdTRUE;
      }
      else
      {
        /* Turn off the Tx interrupt until such time as another character
 is being transmitted. */
        MCF_UART0_UIMR = serRX_INT;
        xTxHasEnded = pdTRUE;
      }
    }

    if( MCF_UART0_USR & MCF_UART_USR_RXRDY )
    {
      ucChar = MCF_UART0_URB;
      xQueueSendFromISR( xRxedChars, &ucChar, &xHigherPriorityTaskWoken );
      xDoneSomething = pdTRUE;
    }
  }

  /* If using the xQueueReceiveFromISR() or xQueueSendFromISR() API
 functions caused to be unblocked, and the unblocked task has a higher priority than
 the interrupted task, then a context switch should be performed.
 portEND\_SWITCHING\_ISR() is used for this purpose. */
  portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );
}
```

---

#### Resources used by the RTOS kernel

The RTOS kernel uses the PIT0 timer to generate the RTOS tick. The function vApplicationSetupInterrupts() can be altered to use any convenient timer source.

In RTOS addition the RTOS kernel requires one additional interrupt vector. As delivered vector 16 on interrupt controller 0 is used as on the MCF5222x vector 16
is not used by any peripherals and is therefore spare. The RTOS kernel uses this vector in conjunction with the Interrupt Force Register 0 (INTFRCL0).
For reasons of efficiency the RTOS kernel assumes it has exclusive access to the INTFRCL0 register and therefore does not attempt to maintain its state - although this
behaviour can be easily altered by using bitwise sets and clears on the register rather than writing to the register in its entirety.

To allow users the flexibility to change vector assignments both the PIT0 and vector 16 configuration is performed in a file called FreeRTOS\_tick\_setup.c
which is included as part of the user application, rather than part of the fixed RTOS kernel code.

#### Critical sections

Exiting a critical section will always set the interrupt priority such that all interrupts are enabled, no matter what its level when the critical section
was entered. FreeRTOS API functions themselves will use critical sections.

#### Execution context

For reasons of efficiency, tasks run with Supervisor privileges.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/ColdFire\_MCF52221\_CodeWarrior/sources/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative. The demo application will only execute correctly with configUSE\_PREEMPTION set to 0 if configIDLE\_SHOULD\_YIELD is set to 1.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application files.

#### Memory allocation

Source/Portable/MemMang/heap\_2.c is included in the ColdFire demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
