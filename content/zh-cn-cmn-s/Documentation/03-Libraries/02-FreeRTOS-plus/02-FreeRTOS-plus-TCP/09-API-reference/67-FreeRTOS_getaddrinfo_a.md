---
title: "FreeRTOS_getaddrinfo_a()"
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
BaseType_t FreeRTOS_getaddrinfo_a( const char * pcName,
                                   const char * pcService,
                                   const struct freertos_addrinfo * pxHints,
                                   struct freertos_addrinfo ** ppxResult,
                                   FOnDNSEvent pCallback,
                                   void * pvSearchID,
                                   TickType_t uxTimeout );
```

后缀 "_a " 代表异步，表示该函数是非阻塞函数。API 
功能 
与 [FreeRTOS_getaddrinfo](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/66-FreeRTOS_getaddrinfo) 相同， 
但可以异步执行多个 IP 查找。这意味着调用会立即返回， 
而查找则在后台进行。一旦查找完成或发生超时， 
将调用用户定义的函数 pCallback 以发送更新后的结果。


**参数：**

+ *pcName*

    节点或设备的名称。

+ *pcService*

    暂时忽略。

+ *pxHints*

    如果不为 NULL，则可用于指示首选的 IP 类型（v4 或 v6）。

+ *ppxResult*

    分配的结构体，包含结果。 

+ *pCallback*

    当找到地址或超时时调用的回调函数。 

+ *pvSearchID*

    回调函数的搜索 ID。 

+ *uxTimeout*

    回调函数超时。 

回调函数应为以下类型：

```c
void (* FOnDNSEvent ) ( const char *               /* pcName */,
                        void *                     /* pvSearchID */,
                        struct freertos_addrinfo * /* pxAddressInfo */ );
```

其中，`pcName` 是查找的节点或设备的名称，`pvSearchID` 是 
调用 `FreeRTOS_getaddrinfo_a` 进行查询时传递的 ID，`pxAddressInfo` 包含 
结果。


**用法示例：**

```c
/* FreeRTOS-Plus-TCP DNS include. */
#include "FreeRTOS_DNS.h"

static BaseType_t xDNSResult = -2;

static void vDNSEvent( const char * pcName,
                       void * pvSearchID,
                       struct freertos_addrinfo * pxAddrInfo )
{
    ( void ) pcName;
    ( void ) pvSearchID;

    FreeRTOS_printf( ( "vDNSEvent: called with %p\n", pxAddrInfo ) );
    showAddressInfo( pxAddrInfo ); 

    if( pxAddrInfo != NULL )
    {
        xDNSResult = 0;
    }
}

static void dnsTest( const char * pcHostName )
{
    uint32_t ulID;
    BaseType_t rc;

    if( xApplicationGetRandomNumber( &( ulID ) ) != pdFALSE )
    {
        FreeRTOS_dnsclear();

        xDNSResult = -2;
        rc = FreeRTOS_getaddrinfo_a( pcHostName,
                                     NULL,
                                     &xHints,
                                     &pxResult, /* An allocated struct, containing the results. */
                                     vDNSEvent,
                                     ( void * ) ulID,
                                     pdMS_TO_TICKS( 1000U ) );
        vTaskDelay( pdMS_TO_TICKS( 1000U ) );
        rc = xDNSResult;
        FreeRTOS_printf( ( "Lookup '%s': %d\n", pcHostName, rc ) );
    }
    else
    {
        FreeRTOS_printf( ( "dns_test: Failed to generate a random SearchID\n" ) );
    }
}
```
*FreeRTOS_getaddrinfo_a() API 函数的用法示例*

