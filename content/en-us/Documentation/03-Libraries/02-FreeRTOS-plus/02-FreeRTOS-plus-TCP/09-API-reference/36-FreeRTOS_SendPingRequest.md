---
title: "FreeRTOS_SendPingRequest()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h
 
```c
BaseType_t FreeRTOS_SendPingRequest( uint32_t ulIPAddress,
                                        size_t xNumberOfBytesToSend,
                                        TickType_t xBlockTimeTicks );
```

Send a ping [(ICMP echo)](http://en.wikipedia.org/wiki/Ping_(networking_utility)) request to a remote computer.
 
ipconfigSUPPORT\_OUTGOING\_PINGS must be set to 1 in FreeRTOSIPConfig.h for FreeRTOS\_SendPingRequest() to be available.
 
The TCP/IP stack calls the application defined [vApplicationPingReplyHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/59-vApplicationPingReplyHook)
hook (or *callback*) function when it receives a reply to an outgoing ping request.
 

**Parameters:** 

+ *ulIPAddress* 
  
  The IP address to which the ping request is sent.
 
  The IP address is expressed as a 32-bit number in network byte order.
 
+ *xNumberOfBytesToSend* 
  
  The number of data bytes to send in the ping request.
 
+ *xBlockTimeTicks* 
  
  The maximum time the calling RTOS task is prepared to wait for a network buffer if one is not immediately 
  available.
 
  If a network buffer is not available then the calling RTOS task will be held in the Blocked state (so 
  other tasks can execute) until either a buffer becomes available and therefore the ping request transmitted, 
  or the block time expires.
 
  The block time is specified in ticks. Milliseconds can be converted to ticks by dividing the time in 
  milliseconds by portTICK\_PERIOD\_MS.
 
 
**Returns:** 

+ If a ping request is successfully sent then the sequence number sent in the ping message is returned 
  to allow the application writer to match ping requests transmitted with ping replies received. See the 
  example below.
 
+ If a ping request could not be sent then pdFAIL is returned.
 

**Example usage:** 

This example defines two functions. vSendPing() transmits 8 bytes to a remote IP address.
vApplicationPingReplyHook() is the standard FreeRTOS-Plus-TCP ping reply callback function.
vApplicationPingReplyHook() receives the ping reply, then sends the received sequence number
to vSendPing() where it is compared to the sequence number from the ping request.

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
/* This example code snippet assumes the queue has already been created! */  
QueueHandle_t xPingReplyQueue;  
  
/* If ipconfigSUPPORT_OUTGOING_PINGS is set to 1 in FreeRTOSIPConfig.h then  
   vApplicationPingReplyHook() is called by the TCP/IP stack when the stack receives a  
   ping reply. */
void vApplicationPingReplyHook( ePingReplyStatus_t eStatus, uint16_t usIdentifier )  
{  
    switch( eStatus )  
    {  
        case eSuccess    :  
            /* A valid ping reply has been received. Post the sequence number  
               on the queue that is read by the vSendPing() function below. Do  
               not wait more than 10ms trying to send the message if it cannot be  
               sent immediately because this function is called from the TCP/IP  
               RTOS task - blocking in this function will block the TCP/IP RTOS task. */  
            xQueueSend( xPingReplyQueue, &usIdentifier, 10 / portTICK_PERIOD_MS );  
            break;  
  
        case eInvalidChecksum :  
        case eInvalidData :  
            /* A reply was received but it was not valid. */  
            break;  
    }  
}  
  
  
BaseType_t vSendPing( const int8_t *pcIPAddress )  
{  
uint16_t usRequestSequenceNumber, usReplySequenceNumber;  
uint32_t ulIPAddress;  
  
    /* The pcIPAddress parameter holds the destination IP address as a string in  
       decimal dot notation (for example, "192.168.0.200"). Convert the string into  
       the required 32-bit format. */  
    ulIPAddress = FreeRTOS_inet_addr( pcIPAddress );  
  
    /* Send a ping containing 8 data bytes. Wait (in the Blocked state) a  
       maximum of 100ms for a network buffer into which the generated ping request  
       can be written and sent. */  
    usRequestSequenceNumber = FreeRTOS_SendPingRequest( ulIPAddress, 8, 100 / portTICK_PERIOD_MS );  
  
    if( usRequestSequenceNumber == pdFAIL )  
    {  
        /* The ping could not be sent because a network buffer could not be  
           obtained within 100ms of FreeRTOS\_SendPingRequest() being called. */  
    }  
    else  
    {  
        /* The ping was sent. Wait 200ms for a reply. The sequence number from  
           each reply is sent from the vApplicationPingReplyHook() on the  
           xPingReplyQueue queue (this is not standard behaviour, but implemented in  
           the example function above). It is assumed the queue was created before  
           this function was called! */  
        if( xQueueReceive( xPingReplyQueue,  
                           &usReplySequenceNumber,  
                           200 / portTICK_PERIOD_MS ) == pdPASS )  
        {  
            /* A ping reply was received. Was it a reply to the ping just sent? */  
            if( usRequestSequenceNumber == usReplySequenceNumber )  
            {  
                /* This was a reply to the request just sent. */  
            }  
        }  
    }  
}  
```
*Example use of the FreeRTOS\_SendPingRequest() API function*
