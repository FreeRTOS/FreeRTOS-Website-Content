---
title: "Industrial PC Port"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

This RTOS port was developed on a very old laptop making use of the parallel port to drive digital IO. 
It has since been used on both low end 486 based and high end Pentium based industrial single board computers for a motor 
control application using an ISA CANBus interface. Any x86 based PC single board computer can be used.
See the FAQ *"Will FreeRTOS run under Windows"* for information on how this port can be tested from a Windows DOS box. 

[FreeDOS](http://www.freedos.org/)
 provides a convenient, reliable and royalty free boot system, along with file and console IO. The usual 16bit DOS 
 restrictions apply, a little wasteful on a Pentium system!

If your chosen target single board computer includes a network adapter then freely available [packet drivers](http://www.crynwr.com/) 
can be used to map a drive from your host system onto your target. The application under development can then be executed and 
debugged from the mapped drive - removing the requirement to download the application after each compilation.

The PC compatible architecture allows the use of the [Open Watcom development tools](http://www.openwatcom.org/)
 both directly on the target single board computer should space 
allow, or via the remote debugging utilities. Although not open source, the Borland development tools have also proved 
reliable.

From V4.0.0 the PC demo has been updated to demonstrate the use of co-routines. See the [co-routine documentation](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/14-Standard-demo-examples) 
page for more information.

---

### *IMPORTANT! Notes on using the industrial PC RTOS port*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-demo-application)
3. [Configuration and Usage Details](#configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### Source Code Organisation

The FreeRTOS download contains the source code for all the FreeRTOS ports.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) section for a description of the
downloaded files and information on creating a new project.

The PC target project files (Open Watcom and Borland) are contained in the 
Demo/PC directory.

---

### The Demo Application

The FreeRTOS source code download includes a fully preemptive multitasking demo application for the PC RTOS port.

### Demo application hardware setup

The demo application includes tasks that send and receive characters over the serial port. The characters sent by one task
need to be received by another - if any character is missed or received out of sequence an error condition is flagged. A
loopback connector is required on the serial port for this mechanism to operate (simply connect pins 2 and 3 together on 
the serial port connector).

The demo application utilises the standard parallel port to control 8 LEDs. Omitting these LEDs will not cause the RTOS 
demo application to fail, but will remove some visual feedback that everything is working as expected. 

The RTOS kernel does not maintain the context of the floating point registers. When using Open Watcom, the NO87 environment variable 
must be defined to force the use of floating point emulation.

The Borland floating point emulation is not re-entrant - 
but tricks for making it so are quite well documented.

### Building the RTOS demo application

Both Borland V4.52 and Open Watcom development tools are supported. 
Project files that can be opened from within the respective IDE's can be found in the Demo/PC directory.

### Functionality

The demo application creates all of the standard demo application real time tasks and co-routines (see the 
 [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) section for details of the individual tasks).

The LEDs connected to the parallel port are under control of the 'flash' co-routines. Each will flash at a constant 
but different frequency as described in the demo application documentation. Each LED is controlled by a different co-routine.

A check task is included that monitors all the real time tasks and co-routines. An error occurring in any task or co-routine will wake the 'Check' task
and cause an error message to be output to the display. In addition, every five
seconds the 'Check' task examines all the tasks in the system to ensure they are executing without error then outputs a 
status message. An 'OK' status message indicates that no errors have been detected. This mechanism can be checked by 
removing the loopback connector from the serial port
 (described above), and in doing so deliberately generating an error.

---

### Configuration and Usage Details

### RTOS port specific configuration

Configuration items specific to this port are contained in Demo/PC/FreeRTOSConfig.h (or
Demo/PC/FRConfig.h if the Borland compiler is being used). The constants defined in
this file can be edited to suit your application. In particular - the definition configTICK\_RATE\_HZ is used to set the frequency
of the RTOS tick. The supplied value of 1000Hz is useful for testing the RTOS kernel functionality but is faster than most applications
require. Lowering this value will improve efficiency.

Each port #defines 'BaseType\_t' to equal the most efficient data type for that processor. This port defines
BaseType\_t to be of type short.

### Switching between the pre-emptive and co-operative RTOS kernels

Set the definition configUSE\_PREEMPTION within Demo/PC/FreeRTOSConfig.h (or
Demo/PC/FRConfig.h if the Borland compiler is being used) to 1 to use pre-emption or 0 to use
co-operative.  

### Development tool options

As with all the ports, it is essential that the correct compiler options are used. The best way to ensure this is to base your
application on the provided RTOS demo application projects.

### RTOS Demo application serial port driver

The serial port driver is written to test some of the RTOS kernel features - and is not intended to represent an optimised 
solution.
