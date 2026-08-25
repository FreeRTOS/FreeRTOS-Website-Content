---
title: Interrupt Driven Circular Buffer Transfer Mode
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO Transfer Modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)]


### Data Direction

The interrupt driven circular buffer transfer mode can be used with FreeRTOS_read().


### Description

ioconfigUSE\_CIRCULAR\_BUFFER\_RX must be set to 1 in [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration)
for the circular buffer transfer mode to be available. It must also be explicitly enabled for the peripheral
being used within the same configuration file.

When the circular buffer transfer mode is selected, FreeRTOS\_read() does not read bytes directly from
the peripheral, but from a circular buffer that is filled by the FreeRTOS-Plus-IO interrupt service routine
as data is received.

The interrupt service routine, and the FreeRTOS circular buffer, are implemented by the FreeRTOS-Plus-IO
code, and do not need to be provided by the application writer.

**Interrupt Driven Circular Buffer Transfer Mode**

- **Advantages**

  - Simple usage model

  - Automatically places the calling task into 
    the [Blocked](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) state
    to wait for the read operation to complete - if it cannot complete immediately. This ensures the task
    calling FreeRTOS\_read() only uses CPU time when there are bytes in the circular buffer.

  - A read timeout can be set to ensure FreeRTOS\_read() calls do not block indefinitely.

  - A simple RAM buffer is used, resulting in a moderately efficient receive method - although a copy
    into the buffer and a copy out of the buffer are required.

  - Bytes received by the peripheral are automatically buffered, and not lost, even if a FreeRTOS\_read()  
    operation is not in progress when the bytes are received.

- **Disadvantages**

  - The FreeRTOS-Plus-IO driver requires RAM for the circular buffer. The buffer length is configured
    by the third parameter of the FreeRTOS\_ioctl() call used to select the transfer mode.

The ioctlUSE\_CIRCULAR\_BUFFER\_RX request code is used in a call to FreeRTOS\_ioctl() to configure a
peripheral to use the interrupt driven circular buffer transfer mode for reads. Note this request code
will result in the peripheral's interrupt being enabled, and the peripheral's interrupt priority being
set to the lowest possible. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the
peripheral's priority if necessary.


### Example Usage

```c
/* FreeRTO+IO includes. */
#include "FreeRTOS_IO.h"

void vAFunction( void )
{
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */
Peripheral_Descriptor_t xOpenedPort;
BaseType_t xReturned;
const uint32_t ulMaxBlock100ms = ( 100UL / portTICK_PERIOD_MS );

    /* Open the SPI port identified in the board support package as using the
       path string "/SPI2/". The second parameter is not currently used and can
       be set to anything, although, for future compatibility, it is recommended
       that it is set to NULL. */
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );

    if( xOpenedPort != NULL )
    {
        /***************** Configure the port *********************************/

        /* xOpenedPort now contains a valid descriptor that can be used with
           other FreeRTOS-Plus-IO API functions.

           Peripherals default to using Polled mode for both reads and writes.
           Change from the default to use the interrupt driven circular buffer
           transfer mode for reading. The third FreeRTOS_ioctl() parameter sets the
           buffer length. In this example, the length is set to 20. A successful
           FreeRTOS_ioctl() call will return pdPASS, for simplicity, this example
           does not show the return value being checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CIRCULAR_BUFFER_RX, ( void * ) 20 );

        /* By default, a peripheral configured to use an interrupt driven circular
           buffer transfer will have an infinite block time. Lower the block time
           to ensure FreeRTOS_read() calls will return, even in the presence of an
           error. In this example the read block time is set to 100ms. Again, for
           simplicity, this example does not show the return value being checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_RX_TIMEOUT, ( void * ) ulMaxBlock100ms );


        /***************** Use the port ***************************************/

        for( ;; )
        {
            /* Read 10 bytes from the port into ucBuffer. Note, this will
               not read the bytes from the peripheral directly, but from the circular
               buffer that is populated by the FreeRTOS-Plus-IO peripheral interrupt service
               routine. The calling task is held in the Blocked state to wait
               for 10 bytes to become available if they are not available immediately,
               but the task will not be held in the Blocked state for more than 100ms.
               ucBuffer is assumed to be defined outside of this function. */
            xBytesTransferred = FreeRTOS_read( xOpenedPort, ucBuffer, 10 );

            if( xBytesTransferred == 10 )
            {
                /* Ten bytes were read from the peripheral before the 100ms block
                   time expired. */
            }
            else
            {
                /* The block time must have expired before ten bytes could be
                   read from the peripheral. xBytesTransferred could be any value
                   from 0 to 9. */
            }
        }
    }
    else
    {
        /* The port was not opened successfully. */
    }
}
```
