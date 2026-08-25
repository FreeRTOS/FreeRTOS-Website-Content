---
title: "Freescale (Motorola) HCS12 (MC9S12C32) small memory model"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/softec.jpg)

From FreeRTOS V3.1.1 the HCS12 port supports both the small and banked memory models. This page demonstrates the usage of the small
memory model on an MC9S12C32 processor. See the [MC9S12DP256B RTOS port](port68hcs12) page
for an example that uses the banked memory model.

The port was developed on a [PK-HCS12C32](http://www.softecmicro.com/products.html?type=detail&title=PK-HCS12C32)
starter kit from [SofTec Microsystems](http://www.softecmicro.com/) ([instructions](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) are provided should you wish to use an alternative development board). It uses the
[CodeWarrior HC(S)12 Development Tools](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm).

---

#### *IMPORTANT! Notes on using the Freescale (Motorola) HCS12 RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS source code download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The HCS12 CodeWarrior small memory model demo application project file is located in the FreeRTOS/Demo/HCS12\_CodeWarrior\_small directory
and is called RTOSDemo.mcp.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the small model HCS12 RTOS port.

#### Demo application hardware setup

The demo application utilises the LEDs and buttons built onto the prototyping board and requires no special considerations.

#### Functionality

The demo application creates 13 tasks - 11 standard demo application tasks, a 'Button Push' task (see below) and the idle
task. Functionality is included in the idle task by way of an idle task hook. See the
 [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the standard demo real time tasks.

The demo applications included with other FreeRTOS ports make use of the
standard ComTest tasks. These use a loopback connector to transmit and
receive RS232 characters between two tasks. The test is important for two
reasons:

1. It tests the mechanism of context switching from within an application interrupt service routine.
2. It randomises execution timing and sequencing.

The prototyping board used to develop the HCS12 port cannot easily include an RS232 interface
so the ComTest tasks are not used. Instead the ISR context switching and randomisation elements are
introduced using a simple 'Button Push' task.

The 'Button Push' task blocks on a queue, waiting for data to arrive. A
simple interrupt routine connected to the PP0 input on the starter kit board places
data in the queue each time the PP0 button is pushed (this button is built
onto the starter kit board). As the 'Button Push' task is created with a
relatively high priority it will unblock and want to execute as soon as data
arrives in the queue - resulting in a context switch within the PP0 input
interrupt service routine. If the data retrieved from the queue is that expected the 'Button Push'
task toggles LED PB5.

When executing correctly the demo application will behave as follows:

* LEDs PB0, PB1 and PB2 are under control of the 'flash' tasks. Each will flash at a constant frequency, with LED PB0
 being the fastest and LED PB2 being the slowest.
* LED PB5 should toggle each time the button connected to input PP0 is pressed - as described above.
* Not all the tasks update an LED so have no visible indication that they are operating correctly.
 Therefore a 'Check' task is created whose job it is to ensure that no errors have been detected in any of the other tasks.

 LED PB7 is under control of the 'Check' task. Every three
 seconds the 'Check' task examines all the tasks in the system to ensure they are executing without error. It
 then toggles LED PB7. If LED PB7 is toggling every three seconds then no errors have ever been detected.
 The toggle rate increasing to 500ms indicates that the 'Check' task has
 discovered at least one error.

#### Building the demo application

The RTOSDemo.mcp project file (located in the FreeRTOS/Demo/HCS12\_CodeWarrior\_small directory) should be opened from within
the CodeWarrior IDE.

The project was originally created using the [UNIS Processor Expert](http://www.processorexpert.com/) configuration
utility - resulting in a lot of automatically generated files and folders being included in the project.
The FreeRTOS real time kernel
source files are contained in the 'Source->Kernel Source' project folder, highlighted in red in the diagram below.
The demo application source files are contained in the 'Source->RTOS Demo' project folder highlighted in green
in the diagram below.

![](/media/2018/cwproject.gif)

CodeWarrior project window showing the RTOSDemo source files

The demo application project contains two build configurations:

1. **Simulator build**
 To simulate the RTOSDemo project first select the 'Simulator' configuration from the drop down list highlighted in blue
 within the diagram above. Following a successful build selecting Debug from the Project menu will automatically open
 the simulator and start a debug session.
2. **Remote debugging build**
 The project can be executed and debugged directly on the HCS12 microcontroller using the USB BDM interface. To start
 a remote debugging session first select 'SofTec' from the drop down list highlighted in blue within the diagram above.
 Following a successful build selecting Debug from the Project menu will automatically load the program into the microcontroller
 flash memory and start a debug session (assuming you have the target board connected using the provided USB cable!).

---

### Configuration and Usage Details

#### Memory Model

As downloaded the MC9S12C32 demo uses the small memory model. See the MC9S12DP256B documentation for information on using
the banked memory model.

#### RTOS port specific configuration

Configuration items specific to this port are contained in FreeRTOS/Demo/HCS12\_CodeWarrior\_small/FreeRTOSConfig.h. The
constants defined in this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is
used to set the frequency of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality
but is faster than most applications require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type char.

Note that vPortEndScheduler() has not been implemented.

#### Interrupt service routines

The interrupt vector table is contained within the Vectors.c source file. Vectors.c was originally
created by the Processor Expert utility - but then manually modified to tailor it for use with the real time kernel and
the demo application. If the Processor Expert is used again it will recreate the file and overwrite these modifications.
It is therefore advisable to keep Vectors.c write protected and only update it manually.

An interrupt service routine that does not cause a context switch has no special requirements and can be written as per the
normal CodeWarrior syntax.

Often you will require an interrupt service routine to cause a context switch. For example a serial port character being
received may wake a high priority task that was blocked waiting for the character. If the ISR interrupted a lower priority
task then it should return immediately to the woken task. A macro portTASK\_SWITCH\_FROM\_ISR() is provided to permit
this functionality. Note that portTASK\_SWITCH\_FROM\_ISR() should only ever be used at the very end of an ISR and only when
the ISR does not declare any non static local variables. If the ISR does use local variables then a call to portYIELD() can
be used in place of the portTASK\_SWITCH\_FROM\_ISR() macro.

As an
example here is the function vButtonPush() from the demo application:

```c

/* ISR connected to PP0 button input. */
void interrupt vButtonPush( void )
{
    static UBaseType_t uxValToSend = 0;

    /* Send an incrementing value to the button push
    task each time the button is pushed. */
    uxValToSend++;

    /* Clear the interrupt flag. */
    PIFP = 1;

    /* Send the incremented value down the queue.  The
    button push task is blocked waiting for the data.
    As the button push task is high priority it will
    wake and a context switch should be performed before
    leaving the ISR. */
    if( xQueueSendFromISR( xButtonQueue, &uxValToSend, pdFALSE ) )
    {
        /* Posting the message caused a higher priority
        task to unblock.  This is the end of the ISR so
        we can perform the task switch here.  This can be
        used as the only local variable is static. */
        portTASK_SWITCH_FROM_ISR();
    }
}
```

See the interrupt function vCOM0\_ISR() within FreeRTOS/Demo/HCS12\_CodeWarrior\_banked/serial/serial.c for a full
example that uses local stack variables.

#### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within FreeRTOS/Demo/HCS12\_CodeWarrior\_small/FreeRTOSConfig.h to 1 to use pre-emption or 0
to use co-operative.

#### Compiler options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided demo application project file - as described in the [Source Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section.

#### SWI instructions

The SWI instruction is utilised by the RTOS kernel and cannot be used by application code.

#### Timer usage

The configuration of the timer used to generate the RTOS tick can be viewed in the TickTimer.c Processor Expert
generated source file.

#### Memory allocation

FreeRTOS/Source/Portable/MemMang/heap\_1.c is included in the HCS12 demo application project to provide the
memory allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.
