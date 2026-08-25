---
title: "FreeRTOS_read()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO API](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions)]

FreeRTOS_IO.h

```c
size_t FreeRTOS_read( Peripheral_Descriptor_t const pxPeripheral,
                      void * const pvBuffer,
                      const size_t xBytes );
```

Reads one or more bytes from an open peripheral.

The [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages)
defines the peripherals that are available to be opened. [FreeRTOS_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl)
is used to select between interrupt driven and polled read modes.

**Parameters:**

- *pxPeripheral*

  The descriptor associated with the peripheral from which bytes are being read. The descriptor will
  have been returned from the [FreeRTOS_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open) call used to open the peripheral.

- *pvBuffer*

  The buffer into which read data are placed.

- *xBytes*

  The total number of bytes requested. When an interrupt driven [transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)  
  is used, the total number of bytes actually read will be less than the total number requested if the
  total number requested are not available before the peripheral's read timeout
  expires. [FreeRTOS_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) is used to set the read timeout value.


**Returns:**

The total number of bytes read. This will be less than the number of bytes requested by the xBytes parameter
if the requested number of bytes cannot be read before the peripheral's read timeout
expires. [FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) is used to set the read timeout value.


**Example usage:**

The example 1 code snippet demonstrates how to perform a read when a peripheral
is configured to use the [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes). Peripherals
default to polled mode when they are opened.

```c
/* By default the port is opened in polled mode. Read sizeof( ucBuffer ) bytes into
   ucBuffer using polled mode. */
xBytesRead = FreeRTOS_read( xPort, ucBuffer, sizeof( ucBuffer ) );

/* The port is currently in polled mode, so FreeRTOS_read() will only have
   returned once all the requested bytes had been read (barring any errors on
   the peripheral). Note that, because polling mode is being used, the task
   making the FreeRTOS_read() call will not have entered the Blocked
   state if it had to wait for the requested number of bytes. */
configASSERT( xBytes == sizeof( ucBuffer ) );
```
*Example 1: Reading bytes from a peripheral that is configured to use the polled transfer mode.*


The example 2 code snippet demonstrates how to perform a read when a peripheral is configured to use
either the interrupt driven character queue [transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes), or the
interrupt driven circular buffer transfer mode. In these modes, the task making the FreeRTOS_read()
call is held in the [Blocked state](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) (not using any CPU time) until
either the requested number of bytes have been read, or the read timeout expires. FreeRTOS_ioctl()
is used with the [iocltSET_RX_TIMEOUT](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) request code to configure the read timeout.

```c
/* Read some bytes in one of the interrupt driven transfer modes. If the
   character queue transfer mode is being used, this will remove bytes from the
   queue that had previously been placed into the queue by the FreeRTOS-Plus-IO interrupt
   service routine. If the circular buffer transfer mode is being used, this will
   remove bytes from the circular buffer that had previously been placed into the
   buffer by the FreeRTOS-Plus-IO interrupt service routine. In both cases, read bytes
   are placed in ucBuffer. */
xBytesRead = FreeRTOS_read( xPort, ucBuffer, sizeof( ucBuffer ) );

if( xBytesRead < sizeof( ucBuffer ) )
{
    /* The Rx timeout must have expired before sizeof( ucBuffer ) bytes could
       be read. xBytesRead number of bytes will have been placed into ucBuffer. */
}
else
{
    /* The requested number of bytes were read before the read timeout expired.
       All the requested bytes have been placed in ucBuffer. */
}
```
*Example 2: Reading bytes from a peripheral that is configured to used either the  
interrupt driven character queue transfer mode, or the interrupt driven circular  
buffer transfer mode.*
