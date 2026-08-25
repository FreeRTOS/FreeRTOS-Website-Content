---
title: "vApplicationIPNetworkEventHook_Multi()"
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
void vApplicationIPNetworkEventHook_Multi( 
                                           eIPCallbackEvent_t eNetworkEvent,  
                                           struct xNetworkEndPoint * pxEndPoint 
                                         );
```

`vApplicationIPNetworkEventHook_Multi()` 是由应用程序定义的钩子（或回调）函数， 
由 TCP/IP 堆栈在网络连接或断开连接时调用。由于该函数 
由 TCP/IP 堆栈调用，因此 TCP/IP 堆栈负责设置该函数的参数值。

回调函数由应用程序编写者实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上述原型（包括函数名称）完全匹配。


**参数：**

+ *eNetworkEvent*

  如果 IP 堆栈因网络连接而调用 
  vApplicationIPNetworkEventHook_Multi()，则 eNetworkEvent 的参数值将等于 eNetworkUp。在这种情况下：

  - 如果 ipconfigUSE_DHCP 或 ipconfigUSE_DHCPv6 服务器在 FreeRTOSIPConfig.h 中设置为 1，则 
    在从 DHCP 服务器获取 IP 地址或者之前已从 DHCP 服务器获取的 IP 地址租期已续时，调用 vApplicationIPNetworkEventHook_Multi 
    （eNetworkUp、struct xNetworkEndPoint *pxEndPoint） 
    。

  - 如果 ipconfigUSE_DHCP 或 ipconfigUSE_DHCPv6 服务器在 FreeRTOSIPConfig.h 中设置为 0，则 
    在网络已通过静态 IP 地址初始化时调用 vApplicationIPNetworkEventHook_Multi 
    （eNetworkUp、struct xNetworkEndPoint * pxEndPoint）。

  如果 IP 堆栈因网络断开连接而调用 
  vApplicationIPNetworkEventHook_Multi()，则 eNetworkEvent 的参数值将等于 eNetworkDown。在这种情况下：

  - TCP/IP 堆栈调用 `vApplicationIPNetworkEventHook_Multi( eNetworkDown, struct xNetworkEndPoint * pxEndPoint )` 的条件是
    网络驱动程序（以太网外设接口）通知此堆栈网络连接已丢失 
    。并非所有驱动程序都能实现这一功能。

+ *pxEndPoint*

  pxEndPoint 的值代表调用 vApplicationIPNetworkEventHook_Multi 的端点。


应用程序仅在以下情况下才会调用 vApplicationIPNetworkEventHook_Multi()：ipconfigUSE_NETWORK_EVENT_HOOK 
在 FreeRTOSIPConfig.h 中设置为 1。

网络事件钩子能确保在 TCP/IP 堆栈准备就绪之前不会创建任务，因此很适合创建使用 IP 堆栈的任务。


**用法示例：**

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
*vApplicationIPNetworkEventHook_Multi() 定义示例*

