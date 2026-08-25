---
title: FreeRTOS_GetAddressConfiguration()
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
void FreeRTOS_GetAddressConfiguration( uint32_t *pulIPAddress,
                                       uint32_t *pulNetMask,
                                       uint32_t *pulGatewayAddress,
                                       uint32_t *pulDNSServerAddress );
```

从 TCP/IP 堆栈获取网络地址配置。


**参数：** 

+ *pulIPAddress* 
  
  用于返回 IP 堆栈使用的 IP 地址。

  IP 地址是一个按网络字节顺序排列的 32 位数字。

+ *pulNetMask* 
  
  用于返回 IP 堆栈使用的网络掩码。

  网络掩码是一个按网络字节顺序排列的 32 位数字。

+ *pulGatewayAddress* 
  
  用于返回 IP 堆栈使用的网关 IP 地址。

  IP 地址是一个按网络字节顺序排列的 32 位数字。

+ *pulDNSServerAddress* 
  
  用于返回 IP 堆栈使用的 DNS 服务器的 IP 地址。

  IP 地址是一个按网络字节顺序排列的 32 位数字。


**用法示例：** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )  
{  
uint32_t ulIPAddress, ulNetMask, ulGatewayAddress, ulDNSServerAddress;  
int8_t cBuffer[ 16 ];  
  
    if( eNetworkEvent == eNetworkUp )  
    {  
        /* The network is up and configured. Print out the configuration  
           obtained from the DHCP server. */  
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
*FreeRTOS_GetAddressConfiguration() API 函数用法示例*

