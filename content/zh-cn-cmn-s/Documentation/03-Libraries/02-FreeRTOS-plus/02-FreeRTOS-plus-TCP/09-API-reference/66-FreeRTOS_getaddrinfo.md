---
title: "FreeRTOS_getaddrinfo()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_DNS.h

```c
BaseType_t FreeRTOS_getaddrinfo( const char * pcName,
                                 const char * pcService,
                                 const struct freertos_addrinfo * pxHints,
                                 struct freertos_addrinfo ** ppxResult );
```        

该 API 用于查找主机的 IP 地址。它是 `FreeRTOS_gethostbyname()` 的替代品， 
支持 IPv6。如果定义了 "ipconfigUSE_IPv6"，那么在 
`pxHints→ai_family` 等于 `FREERTOS_AF_INET6` 时，此函数也会检索 IPv6 地址。当 `pxHints` 为 NULL 时，只会返回 IPv4 地址 
。


**参数：**

+ *pcName*

  节点或设备的名称。

+ *pcService*

  暂时忽略。

+ *pxHints*

  如果不为 NULL ，则可用于指示首选类型的 IP（v4 或 v6）。

+ *ppxResult*

  分配的结构体，包含结果。


**用法示例：**

```c
/* FreeRTOS-Plus-TCP DNS include. */
#include "FreeRTOS_DNS.h"


static void dnsTest( const char * pcHostName )
{
    BaseType_t rc;
    struct freertos_addrinfo xHints;
    struct freertos_addrinfo * pxResult = NULL;

    FreeRTOS_dnsclear();
    memset( &xHints, 0, sizeof xHints );
    xHints.ai_family = FREERTOS_AF_INET6;

    rc = FreeRTOS_getaddrinfo( pcHostName, NULL, &xHints, &pxResult );
    
    if( rc == 0 )
    {
        FreeRTOS_printf( ( "DNS result '%s': %xip\n", pcHostName, 
                                    pxIter->ai_addr->sin_address.ulIP_IPv4 ) );
    }
    else
    {
        FreeRTOS_printf( ( "DNS query : '%s' No results\n", pcHost ) );
     }
    
}
```
*FreeRTOS_getaddrinfo() API 函数的使用示例*

