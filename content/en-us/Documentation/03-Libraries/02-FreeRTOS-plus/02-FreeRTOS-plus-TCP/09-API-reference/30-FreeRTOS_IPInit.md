---
title: "FreeRTOS_IPInit()"
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
BaseType_t FreeRTOS_IPInit( const uint8_t ucIPAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucNetMask[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucGatewayAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucDNSServerAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );
```

Initialises the FreeRTOS-Plus-TCP stack. FreeRTOS\_IPInit() must be called before any other FreeRTOS-Plus-TCP function.
 
ipIP\_ADDRESS\_LENGTH\_BYTES is defined as 4. ipMAC\_ADDRESS\_LENGTH\_BYTES is defined as 6.
 

**Parameters:** 
 
+ *ucIPAddress* 
  
  If ipconfigUSE\_DHCP is set to 0 (in FreeRTOSIPConfig.h) then the IP address of the network node 
  is static and configured by the value of ucIPAddress.
 
  If ipconfigUSE\_DHCP is set to 1 then FreeRTOS-Plus-TCP will attempt to obtain an IP address from 
  a DHCP sever. If an IP address cannot be obtained then the network node will revert to using the 
  static IP address configured by the value of ucIPAddress.
 
  The IP address is specified as a four byte array, where index 0 holds the first octet of the IP address 
  and index 3 holds the last octet of the IP address. See the example below.
 
+ *ucNetmask* 
  
  If ipconfigUSE\_DHCP is set to 0 (in FreeRTOSIPConfig.h) then the net mask of the network node is static 
  and configured by the value of ucNetmask.
 
  If ipconfigUSE\_DHCP is set to 1 then FreeRTOS-Plus-TCP will attempt to obtain a net mask from a DHCP 
  sever. If a net mask cannot be obtained then the network node will revert to using the static net mask 
  configured by the value of ucNetMask.
 
  The net mask is specified as a four byte array, where index 0 holds the first octet of the mask and 
  index 3 holds the last octet of the mask. See the example below.
 
+ *ucGatewayAddress* 
  
  If ipconfigUSE\_DHCP is set to 0 (in FreeRTOSIPConfig.h) then the IP address of the network gateway 
  is static and configured by the value of ucGatewayAddress.
 
  If ipconfigUSE\_DHCP is set to 1 then FreeRTOS-Plus-TCP will attempt to obtain the IP address of the 
  network gateway from a DHCP sever. If a gateway IP address cannot be obtained then the network node 
  will revert to using the static IP address configured by the value of ucGatewayAddress as the gateway 
  address.
 
  The IP address is specified as a four byte array, where index 0 holds the first octet of the IP address 
  and index 3 holds the last octet of the IP address. See the example below.
 
+ *ucDNSServerAddress* 
  
  If ipconfigUSE\_DHCP is set to 0 (in FreeRTOSIPConfig.h) then the IP address of the DNS server is static 
  and configured by the value of ucDNSServerAddress.
 
  If ipconfigUSE\_DHCP is set to 1 then FreeRTOS-Plus-TCP will attempt to obtain the IP address of the DNS
  server from a DHCP sever. If a DNS server IP address cannot be obtained then the network node will 
  revert to using the static IP address configured by the value of ucDNSServerAddress as the DNS server 
  address.
 
  The IP address is specified as a four byte array, where index 0 holds the first octet of the IP address 
  and index 3 holds the last octet of the IP address. See the example below.
 
+ *ucMACAddress* 
 
  The MAC address of the network node.
 
  The MAC IP address is specified as a six byte array, where index 0 holds the first octet of the MAC 
  address and index 5 holds the last octet of the MAC address. See the example below.
 
 
**Returns:** 

+ pdPASS is returned if the TCP/IP stack was initialised successfully.

+ pdFAIL is returned if the TCP/IP stack was not initialised - either because FreeRTOS\_IPInit() has 
  already been called previously or because either the network buffers or the IP RTOS task could not 
  be created.
 

**Example usage:** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
/* Define the network addressing. These parameters will be used if either  
   ipconfigUDE_DHCP is 0 or if ipconfigUSE_DHCP is 1 but DHCP auto configuration  
   failed. */  
static const uint8_t ucIPAddress[ 4 ] = { 192, 168, 0, 200 };  
static const uint8_t ucNetMask[ 4 ] = { 255, 255, 255, 255 };  
static const uint8_t ucGatewayAddress[ 4 ] = { 192, 168, 0, 1 };  
  
/* The following is the address of an OpenDNS server. */  
static const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };  
  
/* The MAC address array is not declared const as the MAC address will normally  
   be read from an EEPROM and not hard coded (in real deployed applications).*/  
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };  
  
void aFunction( void )  
{  
    /* Initialise the TCP/IP stack. */  
    FreeRTOS_IPInit( ucIPAddress,  
                     ucNetMask,  
                     ucGatewayAddress,  
                     ucDNSServerAddress,  
                     ucMACAddress );  
}  
```
*Example use of the FreeRTOS\_IPInit() API function*
