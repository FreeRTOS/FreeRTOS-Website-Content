---
title: "FreeRTOS_IPInit_Multi()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-TCP API 引用](../FreeRTOS_TCP_API_Functions")]

FreeRTOS_sockets.h

`FreeRTOS_IPInit_Multi()` 取代了之前的 [FreeRTOS_IPInit()](../30-FreeRTOS_IPInit)。 `FreeRTOS_IPInit_Multi()` 
必须在除网络接口特定 API 之外的任何其他 FreeRTOS-Plus-TCP 函数之前调用， 
为所需接口或初始化端点的 API 填写接口描述符 (`pxInterface_FillInterfaceDescriptor`)。 
这些 API 包括  `FreeRTOS_FillEndPoint()` 或 `FreeRTOS_FillEndPoint_IPv6()`。


**参数：**

无参数


**返回：**

+ 如果 TCP/IP 堆栈初始化成功，则返回 pdPASS。 
+ 如果 TCP/IP 堆栈因为以下原因未初始化，则返回 pdFAIL：因为 FreeRTOS_IPInit() 
  之前已调用，或者是无法创建网络缓冲区或 IP RTOS 任务 
  。


**用法示例：**

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

