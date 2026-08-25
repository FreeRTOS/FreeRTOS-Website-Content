---
title: "DHCPv6"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

DHCPv6 代表[动态主机配置协议第 6 版](https://en.wikipedia.org/wiki/DHCPv6)。

DHCPv6 提供了静态 IPv6 地址分配和通过 RA 分配 IPv6 地址的替代方案。

如果在 [FreeRTOSIPConfig.h](TCP_IP_Configuration) 中将 ipconfigUSE_DHCPv6 设置为 1，并且如果**** 
在端点初始化过程中设置了端点结构体 **bits** 字段中的 bWantRA 位， 
那么 FreeRTOS-Plus-TCP 将尝试从 DHCPv6 服务器获取端点的 IP 地址， 
并且只有在无法联系到 DHCPv6 服务器的情况下才恢复使用静态 IP 地址。

专家用户可以使用 
[应用程序 DHCP 钩子](TCP_IP_Configuration#ipconfiguse_dhcp_HOOK)（或“回调”）函数来影响 DHCP 进程。

下面是一个启用 DHCPv6 的端点初始化示例：

```c
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


#if ( ipconfigUSE_DHCPv6 != 0 )
    {
        /* End-point wants to use DHCPv6. */
        xEndPoints[ xEndPointCount ].bits.bWantDHCP = pdTRUE;
    }
#endif /* ( ipconfigUSE_DHCPv6 != 0 ) */
```

