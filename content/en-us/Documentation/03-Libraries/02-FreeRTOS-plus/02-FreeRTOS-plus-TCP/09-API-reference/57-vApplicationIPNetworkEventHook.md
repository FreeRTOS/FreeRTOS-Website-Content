---
title: "vApplicationIPNetworkEventHook()"
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
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent );
```

vApplicationIPNetworkEventHook() is an application defined hook (or *callback*) function that is called 
by the TCP/IP stack when the network either connects or disconnects. As the function is called by the 
TCP/IP stack the TCP/IP sets the value of the function's parameter.
 
Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name).
 
The value of the eNetworkEvent parameter will equal eNetworkUp if the IP stack called vApplicationIPNetworkEventHook() 
because the network connected:
 
* If ipconfigUSE\_DHCP server is set to 1 in FreeRTOSIPConfig.h then vApplicationIPNetworkEventHook( eNetworkUp ) 
  is called when an IP address is obtained from a DHCP server **and** when the lease for an IP address 
  previously obtained from a DHCP is renewed.

* If ipconfigUSE\_DHCP server is set to 0 in FreeRTOSIPConfig.h then vApplicationIPNetworkEventHook( eNetworkUp ) 
  is called when the network has been initialised with a [static IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit).

The value of the eNetworkEvent parameter will equal eNetworkDown if the IP stack called vApplicationIPNetworkEventHook() 
because the network disconnected:
 
* The TCP/IP stack calls vApplicationIPNetworkEventHook( eNetworkDown ) when it is informed by the network 
  driver (the interface to the Ethernet peripheral) that network connectivity has been lost. Not all drivers 
  will implement this functionality.

The application will only call vApplicationIPNetworkEventHook() if ipconfigUSE\_NETWORK\_EVENT\_HOOK 
is set to 1 in FreeRTOSIPConfig.h.
 
The network event hook is a good place to create tasks that use the IP stack as it ensures the tasks 
are not created until the TCP/IP stack is ready.
 

**Example usage:** 

```c
/* Defined by the application code, but called by FreeRTOS-Plus-TCP when the network  
   connects/disconnects (if ipconfigUSE_NETWORK_EVENT_HOOK is set to 1 in  
FreeRTOSIPConfig.h). */  
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )  
{  
uint32_t ulIPAddress, ulNetMask, ulGatewayAddress, ulDNSServerAddress;  
static BaseType_t xTasksAlreadyCreated = pdFALSE;  
int8_t cBuffer[ 16 ];  
  
    /* Check this was a network up event, as opposed to a network down event. */  
    if( eNetworkEvent == eNetworkUp )  
    {  
        /* Create the tasks that use the TCP/IP stack if they have not already been  
           created. */  
        if( xTasksAlreadyCreated == pdFALSE )  
        {  
            /*  
             * Create the tasks here.  
             */  
  
            xTasksAlreadyCreated = pdTRUE;  
        }  
  
        /* The network is up and configured. Print out the configuration,  
           which may have been obtained from a DHCP server. */  
        FreeRTOS_GetAddressConfiguration( &ulIPAddress,  
                                          &ulNetMask,  
                                          &ulGatewayAddress,  
                                          &ulDNSServerAddress );  
  
        /* Convert the IP address to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulIPAddress, cBuffer );  
        printf( "IP Address: %srn", cBuffer );  
  
        /* Convert the net mask to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulNetMask, cBuffer );  
        printf( "Subnet Mask: %srn", cBuffer );  
  
        /* Convert the IP address of the gateway to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulGatewayAddress, cBuffer );  
        printf( "Gateway IP Address: %srn", cBuffer );  
  
        /* Convert the IP address of the DNS server to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulDNSServerAddress, cBuffer );  
        printf( "DNS server IP Address: %srn", cBuffer );  
    }  
}  
```
*Example vApplicationIPNetworkEventHook() definition*
