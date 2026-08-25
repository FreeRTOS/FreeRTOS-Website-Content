---
title: Interrupt Driven Character Queue Transfer Mode
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-IO Transfer Modes](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)]


### Data Direction

The interrupt driven character queue transfer mode can be used with both FreeRTOS\_read() and FreeRTOS\_write().
 
  
### Description

ioconfigUSE\_TX\_CHAR\_QUEUE and/or ioconfigUSE\_RX\_CHAR\_QUEUE must be set to 1 
in [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) for the character queue transfer mode to be 
available for writes and reads respectively. It must also be explicitly enabled for the peripheral 
being used within the same configuration file.
 
When the character queue transfer mode is selected for writes, FreeRTOS\_write() does not write directly 
to the peripheral. Instead the bytes are sent to a transmit queue. The peripheral's interrupt service 
routine removes the bytes from the queue and sends them to the peripheral.
 
When the character queue transfer mode is selected for reads, FreeRTOS\_read() does not read bytes directly 
from the peripheral, but from a receive queue that is filled by the FreeRTOS-Plus-IO interrupt service 
routine as data is received.
 
The interrupt service routines, and the FreeRTOS queues, are implemented by the FreeRTOS-Plus-IO code, 
and do not need to be provided by the application writer.
 

**Interrupt Driven Character Queue Transfer Mode**

+ **Advantages** 

  * Simple usage model 

  * Automatically places the calling task into the Blocked state to wait for the read or write operation 
    to complete - if it cannot complete immediately. This  ensures the task calling FreeRTOS\_read() or 
    FreeRTOS\_write() only uses CPU time when there is actually processing that can be performed. 

  * A read and/or write timeout can be set to ensure FreeRTOS\_read() and FreeRTOS\_write() calls do not
    block indefinitely. 

  * Bytes received by the peripheral are automatically buffered, and not lost, even if a FreeRTOS\_read() 
    operation is not in progress when the bytes are received. 

  * Calls to FreeRTOS\_write() can occur at any time. There is no need to wait for a previous transmission 
    to complete, or for the peripheral to be free.

+ **Disadvantages**

  * The FreeRTOS-Plus-IO driver requires RAM for the queues. The queue length is configured by the third 
    parameter of the FreeRTOS\_ioctl() call used to select the transfer mode. 

  * Character queues are inefficient, so their use should be limited to applications that do not require 
    large amounts of data to be read or written. For example, character queues provide a very convenient  
    transfer mode for command line interfaces, where  characters are only received as quickly as somebody
    can type. 

  * FreeRTOS queues have an in-built mutual exclusion mechanism, but only at the single character level. 
    Therefore, it is guaranteed that the queue data structures will not become corrupt if two tasks attempting 
    to perform a FreeRTOS\_write() (or a FreeRTOS\_read()) at the same time, but there is no guarantee that 
    the data will not become interleaved if that happens. The application writer can guard against that 
    eventuality  using task priorities, or external mutual exclusion  (using a mutex for example) if it 
    is necessary.

The ioctlUSE\_CHARACTER\_QUEUE\_TX and ioctlUSE\_CHARACTER\_QUEUE\_RX request codes are used in calls 
to FreeRTOS\_ioctl() to configure a peripheral to use interrupt driven character queue writes and reads 
respectively. Note these request codes will result in the peripheral's interrupt being enabled, and the 
peripheral's interrupt priority being set to the lowest possible. The ioctlSET\_INTERRUPT\_PRIORITY 
request code can be used to raise the peripheral's priority if necessary.
 
 
### Example Usage

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
           Change from the default to use interrupt driven character queues for both  
           reading and writing. The third FreeRTOS_ioctl() parameter sets the  
           queue length. In this example, the length is set to 20 in both cases.  
           A successful FreeRTOS_ioctl() call will return pdPASS, for simplicity,  
           this example does not show the return value being checked. */  
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CHARACTER_QUEUE_RX, ( void * ) 20 );  
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CHARACTER_QUEUE_TX, ( void * ) 20 );  
                  
        /* By default, a peripheral configured to use an interrupt driven character  
           queue transfer will have an infinite block time. Lower the block time for  
           reading and writing to ensure FreeRTOS_read() and FreeRTOS_write() calls  
           will return, even in the presence of an error. In this example, both  
           the read and write block times are set to 100ms. Again, for simplicity,  
           this example does not show the return value being checked. */  
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_RX_TIMEOUT, ( void * ) ulMaxBlock100ms );  
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_TX_TIMEOUT, ( void * ) ulMaxBlock100ms );  
          
  
        /***************** Use the port ***************************************/  
          
          
        for( ;; )  
        {  
            /* Write 10 bytes from ucBuffer to the opened port. Note the   
               definition of ucBuffer is assumed to be outside of this function. */  
            xBytesTransferred = FreeRTOS_write( xOpenedPort, ucBuffer, 10 );  
              
            /* At this point, 10 bytes will have been written to the Tx queue,  
               but not necessarily written to the peripheral yet. Check all 10 bytes  
               were written to the queue - they should have been as the queue is  
               20 bytes long. */  
            configASSERT( xBytesTransferred == 10 );  
              
            /* Read 10 bytes from the same port into ucBuffer. Note, this will  
               not read the bytes from the peripheral directly, but from the Rx   
               queue that is populated by the FreeRTOS-Plus-IO peripheral interrupt service  
               routine. The calling task is held in the Blocked state to wait  
               for 10 bytes to become available if they are not available immediately,  
               but the task will not be held in the Blocked state for more than 100ms. */  
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
