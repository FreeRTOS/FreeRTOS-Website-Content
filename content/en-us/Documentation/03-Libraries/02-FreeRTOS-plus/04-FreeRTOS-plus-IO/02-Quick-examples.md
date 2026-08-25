---
title: Quick FreeRTOS-Plus-IO Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

This page contains basic source code examples to demonstrate the FreeRTOS-Plus-IO concept. More detailed 
examples are provided in the [API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions) 
and [Transfer Mode section](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes) sections of this site. Comprehensive application 
examples are provided with board support packages, with notable projects documented on 
the [Featured Demos](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/04-Demos/01-NXP_LPC1769_Demo_Description) pages.
 
Example 1 demonstrates how to read bytes from a peripheral that has already been opened and configured. 
The example is valid for all the data transfer modes.
 

```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  

/* The size of the buffer into which data will be read. */  
#define BUFFER_SIZE        200  

/* The buffer itself. */  
const int8_t cBuffer[ 200 ] = { 0 };  

/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a  
   descriptor. */  
void vReadExample( Peripheral_Descriptor_t xOpenPort )  
{  
size_t xBytesTransferred;  

    /* The peripheral has already been opened and configured. Read BUFFER_SIZE  
       bytes into cBuffer. The syntax is the same here no matter which  
       transfer mode is being used. */  
    xBytesTransferred = FreeRTOS_read( xOpenPort, cBuffer, BUFFER_SIZE );  

    /* xBytesTransferred will now hold the number of bytes read, which could be  
       less than BUFFER_SIZE bytes if the configured read timeout expired before  
       the requested amount of data was available. */  
}  
```
*Example 1:  Reading bytes from a descriptor that has already been opened and configured.*


Example 2 demonstrates how to write bytes to a peripheral that has already been opened and configured to 
use the [interrupt driven zero copy write](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode) transfer mode.
 

```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  

/* The size of the buffer to read and write. */  
#define BUFFER_SIZE        200  

/* The buffer itself. */  
const int8_t cBuffer[ 200 ] = { 0 };  

/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a  
   descriptor. */  
void vWriteExample( Peripheral_Descriptor_t xOpenPort )  
{  
size_t xBytesTransferred;  
BaseType_t xReturn;  
  
    /* This port is configured to use the zero copy Tx transfer mode, so the   
       write mutex must be obtained before starting a new write operation. Wait   
       a maximum of 200ms for the mutex - this task will not consume any CPU time   
       while it is waiting. */  
    xReturn = FreeRTOS_ioctl( xOpenPort, iocltOBTAIN_WRITE_MUTEX, ( void * ) ( 200 / portTICK_PERIOD_MS ) );  
  
    if( xReturn != pdFAIL )  
    {  
        /* The write mutex was obtained, so it is safe to perform a write. This  
           writes BUFFER_SIZE bytes from cBuffer to the peripheral. */  
        xBytesTransferred = FreeRTOS_write( xOpenPort, cBuffer, BUFFER_SIZE );  
  
        /* The actual peripheral transmission is performed by an interrupt, so,   
           in the particular case of using a zero copy transfer, xBytesTransferred   
           will be either 0, if the transfer could not be started, or equal to   
           BUFFER_SIZE. Note however, that the interrupt may still be in the process   
           of actually transmitting the data, even though the function has returned.   
           The actual transmission of data will have completed when the mutex is  
           available again. */  
    }  
}  
```
*Example 2:  Writing bytes to a descriptor that has already been opened and configured to use the zero 
copy write transfer mode.*

Example 3 demonstrates how to open and configure a descriptor. First an I2C port is opened. Then, assuming 
the open was successful, the port is configured for zero copy write transfers and circular buffer read 
transfers. The read timeout and the write timeout are both set to 200ms.
 
```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  
  
Peripheral_Descriptor_t xOpenAndConfigureI2CPort( void )  
{  
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */  
Peripheral_Descriptor_t xI2CPort;  
  
    /* Open the I2C0 port, storing the returned value as the port's descriptor.  
       The peripherals that are actually available to be opened depends on the board  
       support package being used. The second parameter is not currently used and can  
       be set to anything, although, for future compatibility, it is recommended that  
       it is set to NULL. By default, the port is opened with its transfer mode set   
       to polling. */  
    xI2CPort = FreeRTOS_open( "/I2C0/", NULL );  
  
    /* FreeRTOS_open() returns NULL when the open operation cannot complete. Check   
       the return value is not NULL. */  
    configASSERT( xI2CPort );  
  
    /* Configure the port for zero copy Tx. The third parameter is not used in   
       this case. */  
    FreeRTOS_ioctl( xI2CPort, iocltUSE_ZERO_COPY_TX, NULL );  
  
    /* Configure the same port for circular buffer Rx. This time the third  
       parameter is used, and defines the buffer size.  
    FreeRTOS_ioctl( xI2CPort, iocltUSE_CIRCULAR_BUFFER_RX, ( void * ) 100 );  
  
    /* Set the read timeout to 200ms. This is the maximum time a FreeRTOS_read()   
       call will wait for the requested amount of data to be available. As the port   
       is configured to use interrupts, the task performing the read is in the   
       Blocked state while the operation is in progress, so not consuming any CPU time.   
       An interrupt driven zero copy write does not require a timeout to be set. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_RX_TIMEOUT, ( void * ) ( 200 / portTICK_PERIOD_MS ) );  
  
    /* Set the I2C clock frequency to 400000. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_SPEED, ( void * ) 400000 );  
  
    /* Set the I2C slave address to 50. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_I2C_SLAVE_ADDRESS, ( void * ) 50 );  
  
    /* Return a handle to the open port, which can now be used in FreeRTOS_read()  
       and FreeRTOS_write() calls. */  
    return xI2CPort;  
}  
```
*Example 3:  Opening and configuring a descriptor*
