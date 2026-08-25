---
title: Polled Transfer Mode
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO Transfer Modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)]


### Data Direction

Polled mode can be used with both FreeRTOS_read() and FreeRTOS_write().


### Description

In polled mode, data transfers are performed by busy waiting on peripheral status bits. Interrupts are
not used.

**Polled Transfer Mode**

- **Advantages**

  - Very simple usage model

  - In most cases, the FreeRTOS_read() or FreeRTOS_write() operation will only return after all the
    data has been read or written respectively.

  - The FreeRTOS-Plus-IO driver does not need any RAM for data buffering.

- **Disadvantages**

  - The task performing the read or write remains in 
    the [Ready or Running](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)
    state for the duration of the read or write operation - even when there are no actions to perform
    because the peripheral's status bits have not changed since they were last polled. The result is CPU
    time being wasted by the polling task at the expense of another task that could have performed its
    processing immediately.

  - There is no in-built mutual exclusion method. The application writer must ensure mutual exclusion (for
    example by using a mutex) if more than one task needs to access the same peripheral.

  - There is not (yet) the possibility to change the read or write timeout.

Polling is the default mode when a peripheral is opened. Not all peripherals provide a method to return
to polled mode once it has been exited.

Polled writes will only return after all the bytes have been written to the peripheral, unless an error
occurs.

Polled reads will only return after the requested number of bytes have been read from the peripheral,
unless an error occurs.


### Example Usage

```c
/* FreeRTO+IO includes. */
#include "FreeRTOS_IO.h"

void vAFunction( void )
{
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */
Peripheral_Descriptor_t xOpenedPort;
BaseType_t xBytesTransferred;

    /* Open the SPI port identified in the board support package as using the
       path string "/SPI2/". The second parameter is not currently used and can
       be set to anything, although, for future compatibility, it is recommended
       that it is set to NULL. */
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );

    if( xOpenedPort != NULL )
    {
        /* xOpenedPort now contains a valid descriptor that can be used with
           other FreeRTOS-Plus-IO API functions.

           Peripherals default to using Polled mode for both reads and writes, so
           the following FreeRTOS_write() call will write 10 bytes from the
           ucBuffer array to the SPI2 peripheral. The ucBuffer declaration is not
           shown, and assumed to be outside of this example function. */
        xBytesTransferred = FreeRTOS_write( xOpenedPort, ucBuffer, 10 );

        /* As polled mode is being used, xBytesTransferred should be 10, unless
           an error occurred. */
        configASSERT( xBytesTransferred == 10 );

        /* The transfer mode has not been changed, so the following read will
           also use polled mode. It will read 10 bytes into ucBuffer. */
        xBytesTransferred = FreeRTOS_read( xOpenedPort, ucBuffer, 10 );

        /* Again, as polled mode is used, the call to FreeRTOS_read() will have
           returned all of the 10 requested bytes unless an error occurred. */
        configASSERT( xBytesTransferred == 10 );
    }
    else
    {
        /* The port was not opened successfully. */
    }
}
```
