---
title: "DHCPv6"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

DHCPv6 stands for [Dynamic Host Configuration Protocol version 6](https://en.wikipedia.org/wiki/DHCPv6).

DHCPv6 provides an alternative to static IPv6 address assignment as well as IPv6 address assignment via RA.

If ipconfigUSE\_DHCPv6 is set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) and if the **bWantDHCP** 
bit in the **bits** field of the endpoint structure is set during the endpoint initialisation, then 
FreeRTOS-Plus-TCP will attempt to obtain the endpoint's IP address from a DHCPv6 server, and only revert 
to using a static IP address if a DHCPv6 server cannot be contacted.

Expert users can influence the DHCP process using 
an [application DHCP hook](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp_hook) (or 'callback') function.

Below is an example endpoint initialisation that enables DHCPv6:

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

