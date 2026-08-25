---
title: "FreeRTOS_write()"
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
size_t FreeRTOS_write( Peripheral_Descriptor_t const pxPeripheral,
                       const void *pvBuffer,
                       const size_t xBytes );
```

Writes one or more bytes to an open peripheral.

The [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages) defines the peripherals that are available to
be opened. [FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) is used to select between interrupt driven and polled
write modes.

**Parameters:**

- *pxPeripheral*

  The descriptor associated with the peripheral to which bytes are being written. The descriptor will
  have been returned from the [FreeRTOS_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open) call used to open the peripheral.

- *pvBuffer*

  A pointer to the first byte of data to write.

- *xBytes*

  The total number of bytes to write. When an interrupt driven [transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)
  is being used, the actual number of bytes written to a peripheral may be less than the requested number
  if not all the bytes could be written before the peripheral's write timeout
  expired. [FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) is used to set the write timeout value.

**Returns:**

- When the [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode) is used, the returned value is the total
  number of bytes actually written to the peripheral. This will be the total number requested assuming
  no errors occurred.

- When the interrupt driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode) is used,
  the returned value is the total number of bytes actually written to the write queue. This will be less
  than the requested number of bytes if there was not enough space in the queue for all the bytes to be
  written immediately, and the peripheral's write timeout expired before enough space became available.
  The actual transmission of data is controlled by the FreeRTOS-Plus-IO interrupt service routine, and
  may complete after the call to FreeRTOS_write() has returned.

- When the interrupt driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode) is used, then:

  - If the task calling FreeRTOS_write() holds the write mutex, the returned value will be the total number
    of bytes to transmit, assuming no errors occurred. The actual transmission of data is controlled by the
    FreeRTOS-Plus-IO interrupt service routine, and may complete after the call to FreeRTOS_write() has
    returned.

  - If the task calling FreeRTOS\_write() does not hold the write mutex, or
    if [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) is not configured to include the zero copy
    write transfer mode for the peripheral, then zero is returned.

[FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) is used to set the write timeout value.


**Example usage:**

The example 1 code snippet demonstrates how to perform a write when a peripheral is configured to
use the [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes). Peripherals default to polled mode
when they are opened.

```c
/* By default the port is opened in polled mode. Write some bytes in polled
   mode. */
xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );


/* The port is currently in polled mode, so FreeRTOS_write() will only have
   returned once all the requested bytes had been written (barring any errors on
   the peripheral). Note that because polling mode is being used, the task
   making the FreeRTOS_write() call will not have entered the Blocked
   state during the write process. The bytes written to the peripheral come from
   the ucBuffer buffer. */
configASSERT( xBytes == sizeof( ucBuffer ) );
```
*Example 1: Writing bytes to a peripheral that is configured to use the polled transfer mode.*

The example 2 code snippet demonstrates how to perform a write when a peripheral is configured to use
the interrupt driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes). In this mode, the
task making the FreeRTOS_write() call is held in 
the [Blocked](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)
state (not using any CPU time) until either all the requested number of bytes have been sent to the
queue, or the write timeout expires. FreeRTOS_ioctl() is used with
the [ioctlSET_TX_TIMEOUT](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) request code to configure the write timeout, and the
ioctlWAIT_PREVIOUS_WRITE_COMPLETE request code wait for the write queue to be empty.

```c
/* Write some bytes in interrupt driven character queue Tx mode. */
xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );

if( xBytesWritten < sizeof( ucBuffer ) )
{
    /* The Tx timeout must have expired before sizeof( ucBuffer ) bytes could
       be written to the write queue. */
}
else
{
    /* The requested number of bytes were sent to the write queue before
       the write timeout expired. */
}
```
*Example 2: Writing bytes to a peripheral that is configured to use the interrupt driven character queue
transfer mode.*

The example 3 code snippet demonstrates how to perform a write when a peripheral is configured to use
the interrupt driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes). In this mode, the task
making the FreeRTOS_write() call will always return immediately. If the returned value equals the number
of bytes that are to be written, then the FreeRTOS_write() call successfully started the interrupt driven
transmission. If the returned value equals zero, then the FreeRTOS_write() call could not start the
transmission, either because it did not hold the write mutex, or
because [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) was not configured to support it.

```c
/* As zero copy Tx is being used, a mutex must be obtained before a write can
   be requested. This call requests the mutex, and will wait a maximum of 50
   milliseconds for the mutex to be obtained. FreeRTOS_ioctl() will return pdPASS
   or pdFAIL. */
xMutexObtained = FreeRTOS_ioctl( xPort,
                                 ioctlOBTAIN_WRITE_MUTEX,
                                 ( void * ) ( 50 / portTICK_PERIOD_MS ) );

if( xMutexObtained != pdFAIL )
{
    /* The mutex was obtained, so a write can be performed. This
       time bytes are written directly from ucBuffer. */
    xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );

    /* Interrupt driven zero copy Tx is being used, so FreeRTOS_write() should
       return the number of requested bytes, even though the FreeRTOS-Plus-IO interrupt
       service routine might still be sending the data. */
    configASSERT( xBytesWritten == sizeof( ucBuffer ) );

    /* The mutex will only be available again after all the data has been
       transmitted by the peripheral. Attempting to obtain the mutex again is therefore
       a good way of knowing when all the data has been sent, and when the buffer being
       written can be updated without corrupting the data transmission. The FreeRTOS_ioctl()
       ioctlWAIT_PREVIOUS_WRITE_COMPLETE and ioctlOBTAIN_WRITE_MUTEX can both
       be used for this purpose - the difference between the two being that
       ioctlWAIT_PREVIOUS_WRITE_COMPLETE will not result in the calling task holding
       the mutex if the FreeRTOS_ioctl() call is successful. */
    xMutexObtained = FreeRTOS_ioctl( xPort,
                                     ioctlOBTAIN_WRITE_MUTEX,
                                     ( void * ) ( 50 / portTICK_PERIOD_MS ) );
    /* Or xMutexObtained = FreeRTOS_ioctl( xPort,
                                           ioctlWAIT_PREVIOUS_WRITE_COMPLETE,
                                           ( void * ) ( 50 / portTICK_PERIOD_MS ) ); */

    if( xMutexObtained != pdFAIL )
    {
        /* If another write is going to be performed, it can be performed now,
           as the write mutex is already held. If a write is not going to be
           performed, and another task uses the same peripheral, then the mutex
           should be returned, and ioctlWAIT_PREVIOUS_WRITE_COMPLETE would have been
           a better request code to use. The second parameter is not used in the
           following call. */
        FreeRTOS_ioctl( xPort, ioctlRELEASE_WRITE_MUTEX, NULL );
    }
}
```
*Example 3: Writing bytes to a peripheral that is configured to use the interrupt  
driven zero copy transfer mode.*
