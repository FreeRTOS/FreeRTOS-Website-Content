---
title: "FreeRTOS_IPInit_Multi()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

`FreeRTOS_IPInit_Multi()` replaces the earlier [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit). `FreeRTOS_IPInit_Multi()` 
must be called before any other FreeRTOS-Plus-TCP function, other than the network interface specific APIs, 
to fill the interface descriptors (`pxInterface_FillInterfaceDescriptor`) for the required interfaces or 
APIs that initialise the endpoints -  `FreeRTOS_FillEndPoint()` or `FreeRTOS_FillEndPoint_IPv6()`.


**Parameters:**

No params


**Returns:**

+ pdPASS is returned if the TCP/IP stack was initialised successfully. 
+ pdFAIL is returned if the TCP/IP stack was not initialised - either because FreeRTOS\_IPInit() 
  has already been called previously or because the network buffers or the IP RTOS task could 
  not be created.


**Example usage:**

```c
BaseType_t xRet;
BaseType_t xEndPointCount = 0;
const uint8_t ucIPAddress[ 4 ] = { 192, 168, 0, 200 };
const uint8_t ucNetMask[ 4 ] =  { 255, 255, 255, 0 };
const uint8_t ucGatewayAddress[ 4 ] = { 192, 168, 0, 1 };
const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };
const uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };

static NetworkInterface_t xInterfaces[1];
static NetworkEndPoint_t xEndPoints[4];

extern NetworkInterface_t * px<Interface>_FillInterfaceDescriptor( BaseType_t xEMACIndex,
                                                    NetworkInterface_t * pxInterface );

/* Initialize the interface descriptor. */
pxInterface_FillInterfaceDescriptor(0, &(xInterfaces[0]));

/* === End-point 0 === */
#if ( ipconfigUSE_IPv4 != 0 )
    {
        FreeRTOS_FillEndPoint( &(xInterfaces[0]), 
                               &(xEndPoints[xEndPointCount]), 
                               ucIPAddress, 
                               ucNetMask, 
                               ucGatewayAddress, 
                               ucDNSServerAddress, 
                               ucMACAddress );
        #if ( ipconfigUSE_DHCP != 0 )
        {
            /* End-point 0 wants to use DHCPv4. */
            xEndPoints[xEndPointCount].bits.bWantDHCP = pdTRUE; 
                
        #endif /* ( ipconfigUSE_DHCP != 0 ) */

        xEndPointCount += 1;

    }
#endif /* ( ipconfigUSE_IPv4 != 0 */


#if ( ipconfigUSE_IPv6 != 0 )
    /*
     *     End-point-1 : public
     *     Network: 2001:470:ed44::/64
     *     IPv6   : 2001:470:ed44::4514:89d5:4589:8b79/128
     *     Gateway: fe80::ba27:ebff:fe5a:d751  // obtained from Router Advertisement
     */
    {
        IPv6_Address_t xIPAddress;
        IPv6_Address_t xPrefix;
        IPv6_Address_t xGateWay;
        IPv6_Address_t xDNSServer1, xDNSServer2;

        FreeRTOS_inet_pton6( "2001:470:ed44::", xPrefix.ucBytes );

        FreeRTOS_CreateIPv6Address( &xIPAddress, &xPrefix, 64, pdTRUE );
        FreeRTOS_inet_pton6( "fe80::ba27:ebff:fe5a:d751", xGateWay.ucBytes );

        FreeRTOS_FillEndPoint_IPv6( &( xInterfaces[ 0 ] ),
                                    &( xEndPoints[ xEndPointCount ] ),
                                    &( xIPAddress ),
                                    &( xPrefix ),
                                    64uL, /* Prefix length. */
                                    &( xGateWay ),
                                    NULL, /* pxDNSServerAddress: Not used yet. */
                                    ucMACAddress );
        FreeRTOS_inet_pton6( "2001:4860:4860::8888", xEndPoints[ xEndPointCount ].ipv6_settings.xDNSServerAddresses[ 0 ].ucBytes );
        FreeRTOS_inet_pton6( "fe80::1", xEndPoints[ xEndPointCount ].ipv6_settings.xDNSServerAddresses[ 1 ].ucBytes );
        FreeRTOS_inet_pton6( "2001:4860:4860::8888", xEndPoints[ xEndPointCount ].ipv6_defaults.xDNSServerAddresses[ 0 ].ucBytes );
        FreeRTOS_inet_pton6( "fe80::1", xEndPoints[ xEndPointCount ].ipv6_defaults.xDNSServerAddresses[ 1 ].ucBytes );

        #if ( ipconfigUSE_RA != 0 )
            {
                /* End-point 1 wants to use Router Advertisement */
                xEndPoints[ xEndPointCount ].bits.bWantRA = pdTRUE;
            }
        #endif /* #if( ipconfigUSE_RA != 0 ) */
            
        #if ( ipconfigUSE_DHCPv6 != 0 )
            {
                /* End-point 1 wants to use DHCPv6. */
                xEndPoints[ xEndPointCount ].bits.bWantDHCP = pdTRUE;
            }
        #endif /* ( ipconfigUSE_DHCPv6 != 0 ) */

        xEndPointCount += 1;

    }

    /*
    *     End-point-3 : private
    *     Network: fe80::/10 (link-local)
    *     IPv6   : fe80::7009
    *     Gateway: -
    */
    {
        IPv6_Address_t xIPAddress;
        IPv6_Address_t xPrefix;

        FreeRTOS_inet_pton6( "fe80::", xPrefix.ucBytes );
        FreeRTOS_inet_pton6( "fe80::7009", xIPAddress.ucBytes );

        FreeRTOS_FillEndPoint_IPv6(
            &( xInterfaces[ 0 ] ),
            &( xEndPoints[ xEndPointCount ] ),
            &( xIPAddress ),
            &( xPrefix ),
            10U,  /* Prefix length. */
            NULL, /* No gateway */
            NULL, /* pxDNSServerAddress: Not used yet. */
            ucMACAddress );

        xEndPointCount += 1;
    }

#endif /* ( ipconfigUSE_IPv6 != 0 ) */
    
/* Initialise the TCP/IP stack. */
FreeRTOS_IPInit_Multi();
```

