---
title: "FreeRTOS_gethostbyname_a()"
created: 2024-09-18
categories:
  - kernel
description: TBD
relatedLinks: 
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 参考](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_DNS.h
 
```c
uint32_t FreeRTOS_gethostbyname_a( const char * pcHostName,
                                   FOnDNSEvent pCallback,
                                   void * pvSearchID,
                                   TickType_t uxTimeout );
```
The suffix "_a" stands for asynchronous, and the function is a non-blocking function. The API 
functionality is the same 
as [FreeRTOS_gethostbyname](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname),
along with the capability to perform Domain Name System (DNS) lookup on a host name asynchronously. Which means the call returns 
immediately whereas the lookup happens in the background. Once the lookup is completed or a timeout 
occurs, a user defined function pCallback will be called to send the updated results back.

Performs a Domain Name System (DNS) lookup on a host name, returning the hosts IP address. For example, 
assuming a DNS server replies to the lookup request, a call to FreeRTOS\_gethostbyname_a( "www.freertos.org", NULL, NULL, 0U ) 
will return freertos.org's IP address.

ipconfigUSE\_DNS and ipconfigDNS\_USE\_CALLBACKS must be set to 1 in FreeRTOSIPConfig.h for FreeRTOS\_gethostbyname\_a() to be available.
 
A DNS lookup can only be performed when FreeRTOS-Plus-TCP knows the IP address of a DNS server. If 
ipconfigUSE\_DHCP is 0 in FreeRTOSIPConfig.h then the DNS server address is passed into FreeRTOS-Plus-TCP 
as a parameter of the FreeRTOS\_IPInit() function. If ipconfigUSE\_DHCP is 1 in FreeRTOSIPConfig.h then 
the DNS server address can be obtained from a DHCP server.
 
FreeRTOS\_gethostbyname() will wait (in the Blocked state so other tasks can execute) for a reply for 200ms 
after each DNS request - with a maximum of 5 DNS requests being sent.
 

**Parameters:** 

+ *pcHostName*

  A standard NULL terminated string containing the name of the host being looked up.

+ *pCallback*

  The callback function which will be called upon DNS response. It will be called with `pcHostName`, `pvSearchID` and 
  `pxAddressInfo` which points to address info. The pxAddressInfo should be freed by the application once the callback 
  has been called by the FreeRTOS_freeaddrinfo(). In case of timeouts pxAddressInfo can be NULL.

+ *pvSearchID*

  Search ID for the callback function.

+ *uxTimeout*

  Timeout for the callback function.

**Returns:** 

+ If the lookup is successful then the IP address of the host is returned in network byte order.
 
+ If the lookup fails then 0 is returned.
 

**Example usage:** 

```c
/* FreeRTOS-Plus-TCP DNS include. */  
#include "FreeRTOS_DNS.h"

BastType_t xHasIPv4Address = pdFALSE;

static void vDNS_callback( const char * pcName,
                           void * pvSearchID,
                           uint32_t ulIPAddress )
{
    if( pxAddress && pxAddress->ai_family == FREERTOS_AF_INET4 )
    {
         char pcBuf[ 16 ];
         uint32_t ulIPAddress;

         /* The DNS lookup has a result, or it has reached the time-out. */
         ulIPAddress = pxAddress->ai_addr->sin_address.ulIP_IPv4;
         FreeRTOS_inet_ntoa( ulIPAddress, pcBuf );
         FreeRTOS_printf( ( "vDNS_callback: IP address of %s found: %s\n", pcName, pcBuf ) );

         xHasIPv4Address = pdTRUE;
    }
}

void aFunction( void )  
{
    xHasIPv4Address = pdFALSE;
    FreeRTOS_gethostbyname_a( "www.freertos.org", /* The target DNS name. */
                              vDNS_callback, /* The DNS callback function. */
                              NULL, /* Search ID for the callback function. */
                              1000 ); /* Timeout in ms. */
}
```
*Example use of the FreeRTOS_gethostbyname_a() API function*
