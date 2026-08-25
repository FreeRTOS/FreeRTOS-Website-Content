---
title: "FreeRTOS_getaddrinfo()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_DNS.h

```c
BaseType_t FreeRTOS_getaddrinfo( const char * pcName,
                                 const char * pcService,
                                 const struct freertos_addrinfo * pxHints,
                                 struct freertos_addrinfo ** ppxResult );
```        

The API is used to lookup the IP-address of a host. It is an alternative to `FreeRTOS_gethostbyname()` 
with support for IPv6. When 'ipconfigUSE\_IPv6' is defined, it can also retrieve IPv6 addresses, in 
case `pxHints→ai_family` equals `FREERTOS_AF_INET6`. When `pxHints` is NULL, only IPv4 addresses will 
be returned.


**Parameters:**

+ *pcName*

  The name of the node or device.

+ *pcService*

  Ignored for now.

+ *pxHints*

  If not NULL, then can be used to indicate the preferred type of IP (v4 or v6 ).

+ *ppxResult*

  An allocated struct, containing the results.


**Example usage:**

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
*Example use of the FreeRTOS_getaddrinfo() API function*

