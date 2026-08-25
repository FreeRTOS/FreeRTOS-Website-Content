---
title: "FreeRTOS_SetAddressConfiguration()"
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
void FreeRTOS_SetAddressConfiguration( const uint32_t * pulIPAddress,
                                       const uint32_t * pulNetMask,
                                       const uint32_t * pulGatewayAddress,
                                       const uint32_t * pulDNSServerAddress );
```

This function can be used to update the IPv4 address and netmask, the gateway address, and the DNS server address 
used by the FreeRTOS-Plus-TCP device after the TCP stack has already been initialized with a call to 
[FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit).


**Parameters:**

+ *`pulIPAddress`*

  A pointer to the 32-bit IPv4 address, in network endian order, that the device should use. 
  This pointer can be NULL if you want to leave the IP Address unchanged.
  
+ *`pulNetMask`*

  A pointer to the 32-bit IPv4 netmask, in network endian order, that the device should use. 
  This pointer can be NULL if you want to leave the IP netmask unchanged.
  
+ *`pulGatewayAddress`* 

  A pointer to the 32-bit IPv4 [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router) address, in network endian order, that the device 
  should use. This pointer can be NULL if you want to leave the device gateway address unchanged.
  
+ *`pulDNSServerAddress`*

  A pointer to the 32-bit IPv4 DNS server address that the device should use. This pointer 
  can be NULL if you want to leave the DNS server IP Address in use unchanged.
  

**Caution:**

This function is not thread safe and should be used with the `taskENTER_CRITICAL/taskEXIT_CRITICAL` 
pair. A call to this function should be made only when there is no active connection (either UDP or TCP), 
or else that connection might be severed.


**Example usage:**

```c
    void vUserTask( void *pvParameters )  
    {  
        /* 32-bit representation of 192.168.1.12. */  
        uint32_t ulHostEndianIPAddress = 0xC0A8010C;  
        uint32_t ulNetworkEndianIPAddress = FreeRTOS_htonl( ulHostEndianIPAddress );  
        /* 32-bit representation of 192.168.1.1. */  
        uint32_t ulHostEndianGatewayAddress = 0xC0A80101;  
        uint32_t ulNetworkEndianGatewayAddress = FreeRTOS_htonl( ulHostEndianGatewayAddress );  
        /* 32-bit representation of OpenDNS server address 208.67.222.222 */  
        uint32_t ulHostEndianDNSServerAddress = 0xD043DEDE;  
        uint32_t ulNetworkEndianDNSServerAddress = FreeRTOS_htonl( ulHostEndianDNSServerAddress );  
        BaseType_t xUserWantsToUpdateConfiguration = pdFALSE;  
          
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
            if( xUserWantsToUpdateConfiguration == pdTRUE )  
            {  
                /* Make sure that no other task can the current task while the  
                 * IP-address is being set. */  
                taskENTER_CRITICAL();  
                {  
                    /* Update the IP address, gateway address and the DNS server address of  
                     * this device but leave the netmask unchanged by passing NULL. */  
                    FreeRTOS_SetAddressConfiguration( &ulNetworkEndianIPAddress ,  
                                                      NULL,  
                                                      &ulNetworkEndianGatewayAddress,  
                                                      &ulNetworkEndianDNSServerAddress );  
                }  
                /* Exit critical section. */  
                taskEXIT_CRITICAL();  
            }  
        }  
    }  
```
