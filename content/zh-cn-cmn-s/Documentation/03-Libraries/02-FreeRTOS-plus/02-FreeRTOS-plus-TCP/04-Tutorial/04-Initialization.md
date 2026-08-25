---
title: 初始化 TCP/IP 堆栈
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 网络教程](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)节选

本页介绍了 [FreeRTOS_IPInit_Multi()](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/31-FreeRTOS_IPInit_Multi) 
以及发生“网络开启”和“网络关闭”事件时调用的回调函数。

在调用 `FreeRTOS_IPInit_Multi()` 函数之前，应用程序必须添加网络接口和 
至少一个与网络接口对应的端点。网络接口是 
`EMAC + PHY`（或 WiFi 适配器）的驱动程序。端点是一组网络参数，包括 IP 地址、MAC 地址、 
网关、DNS 等。可以有多个接口，每个接口可以拥有一个或多个端点。

用于初始化接口的函数是 `px${port_name}_FillInterfaceDescriptor`（例如 
`pxSAM_FillInterfaceDescriptor`）。用于添加端点的函数是 `FreeRTOS_FillEndPoint` 
或 `FreeRTOS_FillEndPoint_IPv6`。

`FreeRTOS_IPInit_Multi()` 可创建 FreeRTOS-Plus-TCP RTOS 任务。FreeRTOS-Plus-TCP 任务可配置 
并初始化网络接口。如果 `ipconfigUSE_NETWORK_EVENT_HOOK` 在 FreeRTOSIPConfig.h 中设置为 1， 
则当网络可用时，TCP/IP 堆栈将调用 `vApplicationIPNetworkEventHook_Multi()` 
回调函数。

下文提供了两个示例。第一个示例演示了 `FreeRTOS_IPInit_Multi()`。第二个示例 
演示了 `vApplicationIPNetworkEventHook_Multi()`。


**IPv4 示例：**

```c
/* The MAC address array is not declared const as the MAC address will
   normally be read from an EEPROM and not hard coded (in real deployed
   applications).*/
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };

/* Define the network addressing.  These parameters will be used if either
   ipconfigUDE_DHCP is 0 or if ipconfigUSE_DHCP is 1 but DHCP auto configuration
   failed. */
static const uint8_t ucIPAddress[ 4 ] = { 10, 10, 10, 200 };
static const uint8_t ucNetMask[ 4 ] = { 255, 0, 0, 0 };
static const uint8_t ucGatewayAddress[ 4 ] = { 10, 10, 10, 1 };

/* The following is the address of an OpenDNS server. */
static const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };

int main( void )
{

    /* Initialise the interface descriptor for WinPCap for example. */
    pxWinPcap_FillInterfaceDescriptor( 0, &( xInterfaces[ 0 ] ) );
    
    FreeRTOS_FillEndPoint( &( xInterfaces[ 0 ] ), &( xEndPoints[ 0 ] ), ucIPAddress,
            ucNetMask, ucGatewayAddress, ucDNSServerAddress, ucMACAddress );
    #if ( ipconfigUSE_DHCP != 0 )
    {
        /* End-point 0 wants to use DHCPv4. */
        xEndPoints[ 0 ].bits.bWantDHCP = pdTRUE;
    }
    #endif /* ( ipconfigUSE_DHCP != 0 ) */
    
    /* Initialise the RTOS's TCP/IP stack.  The tasks that use the network
       are created in the vApplicationIPNetworkEventHook() hook function
       below.  The hook function is called when the network connects. */                    
     FreeRTOS_IPInit_Multi();

    /*
     * Other RTOS tasks can be created here.
     */

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* If all is well, the scheduler will now be running, and the following
       line will never be reached.  If the following line does execute, then
       there was insufficient FreeRTOS heap memory available for the idle and/or
       timer tasks to be created. */
    for( ;; );
}
```   
*FreeRTOS_IPInit_Multi() API 函数的示例用法*

```c
void vApplicationIPNetworkEventHook_Multi( eIPCallbackEvent_t eNetworkEvent,
                                           struct xNetworkEndPoint * pxEndPoint )
{
static BaseType_t xTasksAlreadyCreated = pdFALSE;

    /* Both eNetworkUp and eNetworkDown events can be processed here. */
    if( eNetworkEvent == eNetworkUp )
    {
        /* Create the tasks that use the TCP/IP stack if they have not already
        been created. */
        if( xTasksAlreadyCreated == pdFALSE )
        {
            /*
             * For convenience, tasks that use FreeRTOS-Plus-TCP can be created here
             * to ensure they are not created before the network is usable.
             */

            xTasksAlreadyCreated = pdTRUE;
        }
    }
    /* Print out the network configuration, which may have come from a DHCP
     * server. */
    showEndPoint( pxEndPoint );
}
```   
*vApplicationIPNetworkEventHook_Multi() 定义的示例用法*


**IPv6 示例：**

```c
/* The MAC address array is not declared const as the MAC address will
   normally be read from an EEPROM and not hard coded (in real deployed
   applications).*/
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };

int main( void )
{
    IPv6_Address_t xIPAddress;
    IPv6_Address_t xPrefix;
    IPv6_Address_t xGateWay;

    /* Initialise the interface descriptor for WinPCap for example. */
    pxWinPcap_FillInterfaceDescriptor( 0, &( xInterfaces[ 0 ] ) );
    
    /* Add Endpoint - IPv6 needs minimum 2 EndPoints on the same network interface */
    
    /*
     *     End-point-1 : public
     *     Network: 2001:470:ed44::/64
     *     IPv6   : 2001:470:ed44::4514:89d5:4589:8b79/128
     *     Gateway: fe80::ba27:ebff:fe5a:d751  // obtained from Router Advertisement
     */
    FreeRTOS_inet_pton6( "2001:470:ed44::", xPrefix.ucBytes );
    FreeRTOS_CreateIPv6Address( &xIPAddress, &xPrefix, 64, pdTRUE );
    
    FreeRTOS_inet_pton6( "fe80::ba27:ebff:fe5a:d751", xGateWay.ucBytes );
    #if ( ipconfigUSE_RA != 0 )
    {
         /* End-point 1 wants to use Router Advertisement */
         xEndPoints[ 0 ].bits.bWantRA = pdTRUE;
    }
    #endif /* #if( ipconfigUSE_RA != 0 ) */
    #if ( ipconfigUSE_DHCPv6 != 0 )
    {
          /* End-point 1 wants to use DHCPv6. */
          xEndPoints[ 0 ].bits.bWantDHCP = pdTRUE;
    }
    
    FreeRTOS_FillEndPoint_IPv6( &( xInterfaces[ 0 ] ),
                                   &( xEndPoints[ 0] ),
                                   &( xIPAddress ),
                                   &( xPrefix ),
                                   64uL, /* Prefix length. */
                                   &( xGateWay ),
                                   NULL, /* pxDNSServerAddress: Not used yet. */
                                   ucMACAddress );
    FreeRTOS_inet_pton6( "2001:4860:4860::8888", xEndPoints[ 0 ].ipv6_settings.xDNSServerAddresses[ 0 ].ucBytes );
    FreeRTOS_inet_pton6( "fe80::1", xEndPoints[ 0 ].ipv6_settings.xDNSServerAddresses[ 1 ].ucBytes );
    FreeRTOS_inet_pton6( "2001:4860:4860::8888", xEndPoints[ 0 ].ipv6_defaults.xDNSServerAddresses[ 0 ].ucBytes );
    FreeRTOS_inet_pton6( "fe80::1", xEndPoints[ 0 ].ipv6_defaults.xDNSServerAddresses[ 1 ].ucBytes );
    
    /*
     *     End-point-2: private
     *     Network: fe80::/10 (link-local)
     *     IPv6   : fe80::d80e:95cc:3154:b76a/128
     *     Gateway: -
     */
    
     FreeRTOS_inet_pton6( "fe80::", xPrefix.ucBytes );
     FreeRTOS_inet_pton6( "fe80::7009", xIPAddress.ucBytes );

     #if ( ipconfigUSE_DHCPv6 != 0 )
    {
          /* End-point 2 wants to use DHCPv6. */
          xEndPoints[ 1 ].bits.bWantDHCP = pdTRUE;
    }
     
     FreeRTOS_FillEndPoint_IPv6(
                    &( xInterfaces[ 0 ] ),
                    &( xEndPoints[ 1 ] ),
                    &( xIPAddress ),
                    &( xPrefix ),
                    10U,  /* Prefix length. */
                    NULL, /* No gateway */
                    NULL, /* pxDNSServerAddress: Not used yet. */
                    ucMACAddress );
    
    /* Initialise the RTOS's TCP/IP stack.  The tasks that use the network
       are created in the vApplicationIPNetworkEventHook() hook function
       below.  The hook function is called when the network connects. */                 
    FreeRTOS_IPInit_Multi();

    /*
     * Other RTOS tasks can be created here.
     */

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* If all is well, the scheduler will now be running, and the following
    line will never be reached.  If the following line does execute, then
    there was insufficient FreeRTOS heap memory available for the idle and/or
    timer tasks to be created. */
    for( ;; );
}
```   
*FreeRTOS_IPInit_Multi() API 函数的示例用法*

```c
void vApplicationIPNetworkEventHook_Multi( eIPCallbackEvent_t eNetworkEvent,
                                           struct xNetworkEndPoint * pxEndPoint )
{
static BaseType_t xTasksAlreadyCreated = pdFALSE;

    /* Both eNetworkUp and eNetworkDown events can be processed here. */
    if( eNetworkEvent == eNetworkUp )
    {
        /* Create the tasks that use the TCP/IP stack if they have not already
           been created. */
        if( xTasksAlreadyCreated == pdFALSE )
        {
            /*
             * For convenience, tasks that use FreeRTOS-Plus-TCP can be created here
             * to ensure they are not created before the network is usable.
             */

            xTasksAlreadyCreated = pdTRUE;
        }
    }
    
    /* Print out the network configuration, which may have come from a DHCP
     * server. */
    showEndPoint( pxEndPoint );
}
```   
*vApplicationIPNetworkEventHook_Multi() 定义的示例用法*


[返回 RTOS TCP 网络教程索引](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
