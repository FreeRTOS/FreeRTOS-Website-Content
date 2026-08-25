---
title: "vApplicationIPNetworkEventHook_Multi()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
void vApplicationIPNetworkEventHook_Multi( 
                                           eIPCallbackEvent_t eNetworkEvent,  
                                           struct xNetworkEndPoint * pxEndPoint 
                                         );
```

`vApplicationIPNetworkEventHook_Multi()` is an application defined hook (or callback) function that 
is called by the TCP/IP stack when the network either connects or disconnects. As the function is called 
by the TCP/IP stack, the TCP/IP stack sets the value of the function's parameter.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name).


**Parameters:**

+ *eNetworkEvent*

  The value of the eNetworkEvent parameter will equal eNetworkUp if the IP stack called 
  vApplicationIPNetworkEventHook\_Multi() because the network connected. In this case:

  - If the ipconfigUSE\_DHCP or ipconfigUSE\_DHCPv6 server is set to 1 in FreeRTOSIPConfig.h then 
    vApplicationIPNetworkEventHook\_Multi( eNetworkUp, struct xNetworkEndPoint *pxEndPoint ) is called when 
    an IP address is obtained from a DHCP server and when the lease for an IP address previously obtained 
    from a DHCP server is renewed.

  - If the ipconfigUSE\_DHCP or ipconfigUSE\_DHCPv6 server is set to 0 in FreeRTOSIPConfig.h then 
    vApplicationIPNetworkEventHook\_Multi( eNetworkUp, struct xNetworkEndPoint * pxEndPoint ) is called 
    when the network has been initialised with a static IP address.

  The value of the eNetworkEvent parameter will equal eNetworkDown if the IP stack called 
  vApplicationIPNetworkEventHook\_Multi() because the network disconnected. In this case:

  - The TCP/IP stack calls `vApplicationIPNetworkEventHook_Multi( eNetworkDown, struct xNetworkEndPoint * pxEndPoint )`
    when it is informed by the network driver (the interface to the Ethernet peripheral) that network connectivity 
    has been lost. Not all drivers will implement this functionality.

+ *pxEndPoint*

  The value of pxEndPoint represents the end-point for which vApplicationIPNetworkEventHook\_Multi is called.


The application will only call vApplicationIPNetworkEventHook\_Multi() if ipconfigUSE\_NETWORK\_EVENT\_HOOK 
is set to 1 in FreeRTOSIPConfig.h.

The network event hook is a good place to create tasks that use the IP stack as it ensures the tasks are not created until the TCP/IP stack is ready.


**Example usage:**

```c
/* Defined by the application code, but called by FreeRTOS-Plus-TCP when the network
   connects/disconnects (if ipconfigUSE_NETWORK_EVENT_HOOK is set to 1 in
   FreeRTOSIPConfig.h). */

void vApplicationIPNetworkEventHook_Multi( eIPCallbackEvent_t eNetworkEvent, 
struct xNetworkEndPoint * pxEndPoint )
{
    static BaseType_t xTasksAlreadyCreated = pdFALSE;

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

        /* Print out the network configuration, which may have come from a DHCP
         * server. */
        showEndPoint( pxEndPoint );
    }
}
```
*Example vApplicationIPNetworkEventHook\_Multi() definition*

