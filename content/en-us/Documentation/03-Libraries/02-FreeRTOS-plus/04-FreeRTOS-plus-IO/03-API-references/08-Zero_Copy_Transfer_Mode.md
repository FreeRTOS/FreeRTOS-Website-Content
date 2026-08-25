---
title: Interrupt Driven Zero Copy Transfer Mode
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO Transfer Modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)]


### Data Direction

The interrupt driven zero copy transfer mode can be used with FreeRTOS_write().


### Description

ioconfigUSE\_ZERO\_COPY\_TX must be set to 1 in [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration)
for the zero copy transfer mode to be available. It must also be explicitly enabled for the peripheral
being used within the same configuration file.

When the zero copy transfer mode is selected, FreeRTOS\_write() does not write bytes directly to the
peripheral. Instead the total number of bytes to write and a pointer to the first byte are stored inside
the FreeRTOS-Plus-IO driver. The peripheral's interrupt service routine then uses these values to perform
the actual write operation. Bytes are copied directly from the supplied buffer to the peripheral's
registers, without being stored in any intermediary queue or buffer.

The FreeRTOS-Plus-IO driver creates and manages a mutex to ensure only one task can perform a zero copy
write at a time. The mutex must be obtained before a task can start a zero copy write. The mutex is
obtained using a [FreeRTOS\_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) call with the ioctlOBTAIN\_WRITE\_MUTEX request
code. The FreeRTOS\_ioctl() return value must be checked to see if the mutex was obtained successfully
before calling FreeRTOS\_write(). Calls to FreeRTOS\_write() will fail if they are made by a task that
is not the mutex holder.

Zero copy writes are performed by the FreeRTOS-Plus-IO interrupt service routine. It is likely that the
interrupt service routine will continue to access the buffer being written for a period of time after
the call to FreeRTOS\_write() that started the write operation has returned. The buffer must not be
reused or in any way corrupted until the interrupt service routine has completed the write operation.
The FreeRTOS\_ioctl() [ioctlOBTAIN\_WRITE\_MUTEX](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl#ioctlOBTAIN_WRITE_MUTEX)
and [ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl#ioctlWAIT_PREVIOUS_WRITE_COMPLETE)
request codes can be used for this purpose.

A task that holds the mutex, but does not perform a FreeRTOS\_write(), must manually release the mutex
by calling FreeRTOS\_ioctl() with the request code set to ioctlRELEASE\_WRITE\_MUTEX.

The interrupt service routine and write mutex are implemented by the FreeRTOS-Plus-IO code, and do not
need to be provided by the application writer.


**Interrupt Driven Zero Copy Transfer Mode**

- **Advantages**

  - Automatically places the calling task into 
    the [Blocked](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) state
    to wait for the write mutex to become available. This ensures the task calling FreeRTOS_write() only
    uses CPU time when it actually has access to the peripheral.

  - Calls to FreeRTOS\_write() return immediately, allowing the calling task to perform other operations
    while the transmission is in progress.

  - Bytes are moved directly from the buffer supplied as a parameter in the FreeRTOS\_write() call to
    the peripheral registers by the interrupt service routine. No additional RAM is required, and no
    additional copying of data is required, making this a very efficient write method.

  - The use of the write mutex means mutual exclusion is built into the FreeRTOS-Plus-IO driver.

- **Disadvantages**

  - More complex usage model.

The ioctlUSE\_ZERO\_COPY\_TX request code is used in a call to FreeRTOS\_ioctl() to configure a peripheral
to use the interrupt driven zero copy transfer mode for writes. Note this request code will result in the
peripheral's interrupt being enabled, and the peripheral's interrupt priority being set to the lowest
possible. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the peripheral's priority
if necessary.


### Example Usage

Examples are also provided on the [FreeRTOS\_write() API function documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/04-FreeRTOS_write).

```c
/* FreeRTOS-Plus-IO includes. */
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
           Change from the default to use the interrupt driven zero copy transfer
           mode for writing. The third FreeRTOS_ioctl() parameter is not used and
           can take any value - although it is recommended to set the value to NULL
           for future compatibility. A successful FreeRTOS_ioctl() call will return
           pdPASS, for simplicity, this example does not show the return value being
           checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_ZERO_COPY_TX, NULL );


        /***************** Use the port ***************************************/

        /* As the zero copy transfer mode is being used, the write mutex must
           be obtained before FreeRTOS_write() is called. The following call will
           attempt to obtain the mutex. If the mutex is not immediately available,
           then the calling task will be placed into the Blocked state to wait for
           it, but the task will not wait longer than 100ms. If the task is
           successful in obtaining the mutex in that time, FreeRTOS_ioctl() will
           return pdPASS, otherwise FreeRTOS_ioctl() will return pdFAIL. */
        xReturned = FreeRTOS_ioctl( xOpenedPort, ioctlOBTAIN_WRITE_MUTEX, ulMaxBlock100ms );

        if( xReturned == pdTRUE )
        {
            /* The mutex was successfully obtained, now a FreeRTOS_write() can
               be performed. This call will send 100 bytes from ucBuffer. ucBuffer
               is assumed to be defined outside of this function. */
            xReturned = FreeRTOS_write( xOpenedPort, ucBuffer, 100 );

            if( xReturned == 100 )
            {
                /* The write was successful BUT will not yet have completed. The
                   peripheral's interrupt service routine will be accessing ucBuffer,
                   but this task is free to do anything else it needs to do at this
                   point - provided the data in ucBuffer is not changed. */
            }
        }

        /* Some time later the task wants to update the data in ucBuffer, and
           perform another write. First it must ensure the previous write has
           completed. If it can successfully obtain the write mutex again then
           it knows it is safe to access ucBuffer. Again, a maximum block time of
           100ms is used. */
        xReturned = FreeRTOS_ioctl( xOpenedPort, ioctlOBTAIN_WRITE_MUTEX, ulMaxBlock100ms );

        if( xReturned == pdTRUE )
        {
            /* The mutex was obtained, so the task can go ahead and update the
               buffer. In this example, all it is going to do is clear it to zero. */
            memset( ucBuffer, 0, 100 );

            /* The task already holds the mutex, so can perform the write now. */
            xReturned = FreeRTOS_write( xOpenedPort, ucBuffer, 100 );

            /* Again - if at this point xReturned == 100, the write was successful,
               but will still be in progress. */
        }

        /* Before exiting the function, the task wants to ensure the write has
           completed, but this time it does not want to perform another write itself,
           so uses the ioctlWAIT_PREVIOUS_WRITE_COMPLETE request code in place of the
           ioctlOBTAIN_WRITE_MUTEX request code in a call to FreeRTOS_ioctl(). */
        FreeRTOS_ioctl( xOpenedPort, ioctlWAIT_PREVIOUS_WRITE_COMPLETE, ulMaxBlock100ms );
    }
}
```
