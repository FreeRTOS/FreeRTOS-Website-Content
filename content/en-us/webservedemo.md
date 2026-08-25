---
title: "WIZnet I2C TCP/IP Demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Embedded Ethernet Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/embeddedtcp)]


![WEBHW.jpg](/media/2018/WEBHW.jpg)


The embedded web server implementation presented here uses a hardware TCP/IP co-processor.
This demo is one of 4 embedded Ethernet demos currently available for download.

The standard FreeRTOS demo application is intended to be used as a reference and as a starting point
for new applications. This embedded web server demo is included in addition to the standard demo to
provide a more application orientated example.

This application does not include a fully featured web server but does provide a working, preemptive,
multitasking example that includes an interrupt driven I2C driver and an interrupt driven interface with a
WIZnet W3100A TCP/IP coprocessor.

---


## Implementation Details

### Embedded Computer

The TCP/IP and Ethernet interface board is a simple PCB that connects to the expansion port of the
LPC-P2106 ARM7 prototyping board.


### RTOS Port and ARM7 Development Tools

This embedded web server demo was written using [the standard FreeRTOS LPC2000 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106) with
the [GNUARM GCC open source development tools](http://www.GNUARM.com/).

The processor operates in THUMB mode wherever possible.


### Source Files

The project makefile is contained in the Demo/WizNET\_DEMO\_GCC\_ARM7 directory.

See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a full description of the FreeRTOS directory structure and the [ARM7 GCC port page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106)
for more information on using the development tools.

The download includes the following files:

* main.c - initialises the hardware, creates the demo application tasks, then starts the RTOS scheduler.
* http\_serv.c - handles the sequencing of the socket creation and incoming connections. This is a very simply file.
* tcp.c - handles all the messaging between the server task and the WIZnet module. Refer the to the WIZnet W3100A
  datasheet.
* tcpISR.c - contains the interrupt service routine that handles the external interrupts originating from the WIZNet TCP/IP events.
  This is in a separate file as it has to operate in ARM mode.
* i2c.c - the i2c driver implementation.
* i2cISR.c - the i2c interrupt service routine. This has to be in a separate file as it operates in ARM mode.
* html\_pages.h - contains the strings sent as the static part of the served page.

In addition the flash.c file from the standard demo application is required.

---


## Principle of Operation

### The demo application tasks.

The demo creates 18 tasks - 15 standard demo tasks, the embedded web server task, the error check task
and the idle task. The HTTP server task is the highest priority so will preempt any other task every time
there is either an I2C interrupt or an external interrupt from the WIZnet W3100A device.

The web server task:

1. Initialises the WIZnet registers.
2. Creates a socket.
3. Blocks listening for connections.
4. Processes a connection.
5. Closes the socket when the transaction has completed.
6. Then goes back to step 1 to start over.

The web server task spends most of its time blocked waiting for interrupts from either the WIZnet TCP/IP
processor or the I2C peripheral.

This is a very basic implementation that allows a single connection at a time, and closes the connection
as soon as the HTML page transmission has completed.


### I2C interface

The HTTP server task communicates with the WIZnet TCP/IP processor via the I2C bus.

The I2C driver manages a pool of 'messages' (see the xI2CMessage structure defined in i2c.h). When an
application task calls i2cMessage() the I2C driver fills an xI2CMessage structure with the message details -
then places the new xI2CMessage structure into a queue of messages waiting to be actioned. This way the
application task can continue executing without having to wait for the I2C message to be transacted.

The I2C interrupt routines handles the peripheral generated events to send/receive data over the I2C bus.
When a message has completed it checks the queue to see if any further message are waiting to be transmitted.
If so the next message is removed from the queue and transmission starts immediately.

By using the xMessageCompleteSemaphore parameter of the i2cMessage() function an application task can optionally
wait (block) until the I2C message has been completely transacted. While it is blocked the other tasks will
execute. This is particularly relevant when reading data over the I2C bus as the application task needs to know
when the data has been received.


### WIZnet interface

The WIZnet device asserts external interrupt EINT0 when it requires attention, however the I2C interface
complicates the EINT0 interrupt processing.

The C0\_ISR register within the WIZnet device is used to determine the cause of the interrupt, but the I2C
interface means that C0\_ISR cannot be read from within the interrupt service routine. In addition the assertion
of the interrupt cannot be cleared as this too requires writing to the WIZnet device, again over the I2C bus.

With the interrupt (EINT0) still being asserted the only way of leaving the interrupt service routine
is to disable the I2C interrupt within the microcontroller (otherwise the interrupt service routine would be
immediately re-entered). After disabling the interrupt the service routine unblocks the web server task -
which must then immediately read the C0\_ISR register, clear the interrupts, then re-enable the I2C interrupts
in the microcontroller. It is important therefore that the web server task is the highest priority task - thus
ensuring that it always executes immediately following an EINT0 interrupt.

The comments in the source code provide more details.
