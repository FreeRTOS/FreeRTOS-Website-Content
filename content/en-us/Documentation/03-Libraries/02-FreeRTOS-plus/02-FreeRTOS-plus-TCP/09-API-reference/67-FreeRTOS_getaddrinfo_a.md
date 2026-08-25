---
title: "FreeRTOS_getaddrinfo_a()"
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
BaseType_t FreeRTOS_getaddrinfo_a( const char * pcName,
                                   const char * pcService,
                                   const struct freertos_addrinfo * pxHints,
                                   struct freertos_addrinfo ** ppxResult,
                                   FOnDNSEvent pCallback,
                                   void * pvSearchID,
                                   TickType_t uxTimeout );
```

The suffix "_a" stands for asynchronous, and the function is a non-blocking function. The API 
functionality is the same 
as [FreeRTOS_getaddrinfo](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/66-FreeRTOS_getaddrinfo), 
along with the capability to perform multiple IP lookups asynchronously. Which means the call returns 
immediately whereas the lookup happens in the background. Once the lookup is completed or a timeout 
occurs, a user defined function pCallback will be called to send the updated results back.


**Parameters:**

+ *pcName*

    The name of the node or device.

+ *pcService*

    Ignored for now.

+ *pxHints*

    If not NULL then can be used to indicate the preferred type of IP ( v4 or v6 ).

+ *ppxResult*

    An allocated struct, containing the results. 

+ *pCallback*

    The callback function to be called when the address has been found or when a timeout has been reached. 

+ *pvSearchID*

    Search ID for the callback function. 

+ *uxTimeout*

    Timeout for the callback function. 

The callback function should be of the following type:

```c
void (* FOnDNSEvent ) ( const char *               /* pcName */,
                        void *                     /* pvSearchID */,
                        struct freertos_addrinfo * /* pxAddressInfo */ );
```

where the `pcName` is the name of the node or device that's looked up, `pvSearchID` is the ID that was 
passed when the call to `FreeRTOS_getaddrinfo_a` was made for that query, and `pxAddressInfo` contains 
the result.


**Example usage:**

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
*Example use of the FreeRTOS_getaddrinfo_a() API function*

