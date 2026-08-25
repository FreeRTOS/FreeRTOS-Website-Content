---
title: vApplicationIPNetworkEventHook()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent );
```

vApplicationIPNetworkEventHook() 是由应用程序定义的钩子（或*回调*）函数， 
TCP/IP 堆栈会在网络连接或断开连接时调用该函数。该函数 
由 TCP/IP 堆栈调用，因此 TCP/IP 堆栈负责设置该函数的参数值。

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。

如果 IP 堆栈因网络连接而调用 vApplicationIPNetworkEventHook()， 
则 eNetworkEvent 参数的值将等于 eNetworkUp：

* 如果 ipconfigUSE_DHCP 服务器在 FreeRTOSIPConfig.h 中设置为 1，则调用 vApplicationIPNetworkEventHook( eNetworkUp ) 的 
  前提是从 DHCP 服务器获取 IP 地址，**并且** 
  先前从 DHCP 获取的 IP 地址租约已续订。

* 如果 ipconfigUSE_DHCP 服务器在 FreeRTOSIPConfig.h 中设置为 0，则调用 vApplicationIPNetworkEventHook( eNetworkUp ) 的 
  前提是已使用[静态 IP 地址](FreeRTOS_IPInit)对网络进行初始化。

如果 IP 堆栈因网络断开连接而调用 vApplicationIPNetworkEventHook()， 
则 eNetworkEvent 参数的值将等于 eNetworkDown：

* 网络驱动程序（以太网外设接口）通知网络连接已丢失时，TCP/IP 堆栈将调用 vApplicationIPNetworkEventHook( eNetworkDown ) 
  。并非所有驱动程序都会 
  实现此功能。

应用程序调用 vApplicationIPNetworkEventHook() 的前提是 ipconfigUSE_NETWORK_EVENT_HOOK 
在 FreeRTOSIPConfig.h 中设置为 1。

网络事件钩子很适合创建使用 IP 堆栈的任务， 
因为它能确保在 TCP/IP 堆栈准备就绪之前不会创建任务。


**用法示例：** 

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
*vApplicationIPNetworkEventHook() 定义示例*

