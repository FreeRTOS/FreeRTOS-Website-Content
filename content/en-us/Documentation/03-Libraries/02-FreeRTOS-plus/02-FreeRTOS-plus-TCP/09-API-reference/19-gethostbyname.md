---
title: "FreeRTOS_gethostbyname()"
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
uint32_t FreeRTOS_gethostbyname( const uint8_t *pcHostName );
```

Performs a Domain Name System (DNS) lookup on a host name, returning the hosts IP address. For example, 
assuming a DNS server replies to the lookup request, a call to FreeRTOS\_gethostbyname( "www.freertos.org" ) 
will return freertos.org's IP address.

ipconfigUSE\_DNS must be set to 1 in FreeRTOSIPConfig.h for FreeRTOS\_gethostbyname() to be available.
 
A DNS lookup can only be performed when FreeRTOS-Plus-TCP knows the IP address of a DNS server. If 
ipconfigUSE\_DHCP is 0 in FreeRTOSIPConfig.h then the DNS server address is passed into FreeRTOS-Plus-TCP 
as a parameter of the FreeRTOS\_IPInit() function. If ipconfigUSE\_DHCP is 1 in FreeRTOSIPConfig.h then 
the DNS server address can be obtained from a DHCP server.
 
FreeRTOS\_gethostbyname() will wait (in the Blocked state so other tasks can execute) for a reply for 200ms 
after each DNS request - with a maximum of 5 DNS requests being sent.

Note that if DNS cache is enabled (`ipconfigUSE_DNS_CACHE`), then the maximum length of hostnames that can be
resolved is capped by `ipconfigDNS_CACHE_NAME_LENGTH` since all DNS queries are cached.

**Parameters:** 

+ *pcHostName*

  A standard NULL terminated string containing the name of the host being looked up.


**Returns:** 

+ If the lookup is successful then the IP address of the host is returned in network byte order.
 
+ If the lookup fails then 0 is returned.
 

**Example usage:** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
uint32_t ulIPAddress;  
int8_t cBuffer[ 16 ];  
  
    /* Lookup the IP address of the FreeRTOS.org website. */  
    ulIPAddress = FreeRTOS_gethostbyname( "www.freertos.org" );  
  
    if( ulIPAddress != 0 )  
    {  
        /* Convert the IP address to a string. */  
        FreeRTOS_inet_ntoa( ulIPAddress, ( char * ) cBuffer );  
  
        /* Print out the IP address. */  
        printf( "www.FreeRTOS.org is at IP address %srn", cBuffer );  
    }  
    else  
    {  
        printf( "DNS lookup failed. " );  
    }  
}  
```
*Example use of the FreeRTOS_gethostbyname() API function*
