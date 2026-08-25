---
title: "FreeRTOS_SetIPAddress()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_IP.h

```c
void FreeRTOS_SetIPAddress( uint32_t ulIPAddress );
```

This function can be used to update the IPv4 address used by the FreeRTOS-Plus-TCP device after 
the TCP stack has already been initialized with a call to [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit).


**Parameters:**

+ *ulIPAddress*

  The 32-bit IPv4 address, in network endian order, which the device should use. [FreeRTOS\_htonl](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl) 
  can be used to get the network endian representation of the 32-bit IP address.


**Caution:**

This function is not thread safe and should be used with the `taskENTER_CRITICAL/taskEXIT_CRITICAL` 
pair. A call to this function should be made only when there is no active connection (either UDP or 
TCP), or else that connection will be severed.


**Example usage:**

The following code snippet shows how to use `FreeRTOS_SetIPAddress`.

```c
    void vUserTask( void *pvParameters )  
    {  
        /* 32-bit representation of 192.168.1.12. */  
        uint32_t ulHostEndianIPAddress = 0xC0A8010C;  
        uint32_t ulNetworkEndianIPAddress = FreeRTOS_htonl( ulHostEndianIPAddress );  
        /* 32-bit representation of 192.168.1.1. */  
        uint32_t ulHostEndianGatewayAddress = 0xC0A80101;  
        uint32_t ulNetworkEndianGatewayAddress = FreeRTOS_htonl( ulHostEndianGatewayAddress );  
        uint32_t ulHostEndianNetmask = 0xFFFFFF00;  
        uint32_t ulNetworkEndianNetmask = FreeRTOS_htonl( ulHostEndianNetmask );  
        BaseType_t xUserWantsToUpdateIP = pdFALSE;  
        BaseType_t xUserWantsToUpdateNetmask = pdFALSE;  
        BaseType_t xUserWantsToUpdateGateway = pdFALSE;  
      
        /* Ignore compiler warnings about unused variables. */  
        ( void )  pvParameters;  
      
        for( ; ; )  
        {  
            /* Execute some code. */  
            /* .
             * .  
             * .  
             */  

            /* Note: Make sure that there are no active UDP/TCP connections. */  
      
            /* Check whether the user wants to update the IP address. */  
            if( xUserWantsToUpdateIP == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP address of this device. */  
                    FreeRTOS_SetIPAddress( ulNetworkEndianIPAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
              
            /* Check whether the user wants to update the IP netmask. */  
            if( xUserWantsToUpdateNetmask == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP netmask of this device. */  
                    FreeRTOS_SetNetmask( ulNetworkEndianNetmask );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
              
            /* Check whether the user wants to update the gateway address. */  
            if( xUserWantsToUpdateGateway == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Set the IP netmask of this device. */  
                    FreeRTOS_SetGetwayAddress( ulNetworkEndianGatewayAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
        }  
    }  
```
