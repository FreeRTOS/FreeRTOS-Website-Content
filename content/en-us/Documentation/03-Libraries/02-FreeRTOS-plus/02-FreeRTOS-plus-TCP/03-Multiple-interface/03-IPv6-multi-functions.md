---
title: IPv6 and Multiple Interface Functions
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**This page summarises the new API calls for IPv6 and multiple interfaces.**

```c
/*  
 * FreeRTOS_IPInit_Multi() replaces the earlier FreeRTOS_IPInit(). It assumes that  
 * network interfaces and IP-addresses have been configured using the functions  
 * from FreeRTOS_Routing.h. As a minimum, one interface and one end-point must be  
 * defined.  
 */  
BaseType_t FreeRTOS_IPInit_Multi( void );  
```

```c
/*  
 * *Do not call this function directly*.  
 *  
 * Add a new physical Network Interface. The object pointed to by 'pxInterface'  
 * must continue to exist as long as TCP is being used.  
 * Only the Network Interface function xx\_FillInterfaceDescriptor() shall  
 * call this function.  
 */  
NetworkInterface_t * FreeRTOS_AddNetworkInterface( NetworkInterface_t * pxInterface );  
```

```c
/*  
 * Fill-in an IPv4 end-point structure.  
 *  
 * The end-point will be added to the list of end-points, and it will  
 * be connected to the mentioned interface.  
 *  
 * All parameters are mandatory, they must be valid pointers, although they may  
 * point to an array of zeros when not in use.  
 */  
void FreeRTOS_FillEndPoint( NetworkInterface_t * pxNetworkInterface,  
                            NetworkEndPoint_t * pxEndPoint,  
                            const uint8_t ucIPAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucNetMask[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucGatewayAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucDNSServerAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );  
```

```c
/*  
 * Fill-in an IPv6 end-point structure ( IPv6 only ).  
 *  
 * The end-point will be added to the list of end-points, and it will be  
 * connected to the mentioned interface.  
 *  
 * All parameters are mandatory, they must be valid pointers, although they may  
 * point to an array of zeros when not in use.  
 */  
void FreeRTOS_FillEndPoint_IPv6( NetworkInterface_t * pxNetworkInterface,  
                                 NetworkEndPoint_t * pxEndPoint,  
                                 IPv6_Address_t * pxIPAddress,  
                                 IPv6_Address_t * pxNetPrefix,  
                                 size_t uxPrefixLength,  
                                 IPv6_Address_t * pxGatewayAddress,  
                                 IPv6_Address_t * pxDNSServerAddress, /* Not used yet. */  
                                 const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );  
```

```c
/*  
 * ipconfigIPv4_BACKWARD_COMPATIBLE mode only:  
 * *Do not call the following function directly*. It is there for downward  
 * compatibility.  
 *  
 * The function FreeRTOS\_IPInit() will call it to initialise the interface  
 * and end-point objects.  
 */  
struct xNetworkInterface * pxFillInterfaceDescriptor( BaseType_t xEMACIndex,  
                                                struct xNetworkInterface * pxInterface );  
```

```c
/*  
 * ipconfigIPv4_BACKWARD_COMPATIBLE mode only:  
 * The following function is only provided to allow backward compatibility  
 * with the earlier version of FreeRTOS-Plus-TCP which had a single interface only.  
 */  
BaseType_t FreeRTOS_IPInit( const uint8_t ucIPAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucNetMask[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucGatewayAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucDNSServerAddress[ ipIP_ADDRESS_LENGTH_BYTES ],  
                            const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );  
```

```c
/*  
 * Returns the addresses stored in an end-point structure.  
 *  
 * Parameters with a value of NULL are ignored.  
 */  
void FreeRTOS_GetEndPointConfiguration( uint32_t * pulIPAddress,  
                                        uint32_t * pulNetMask,  
                                        uint32_t * pulGatewayAddress,  
                                        uint32_t * pulDNSServerAddress,  
                                        struct xNetworkEndPoint * pxEndPoint );  
```

```c

/*  
 * Change the configuration of a given end-point. Under normal circumstances,  
 * this function is not used.  
 *  
 * Parameters with a value of NULL are ignored.  
 */  
void FreeRTOS_SetEndPointConfiguration( const uint32_t * pulIPAddress,  
                                        const uint32_t * pulNetMask,  
                                        const uint32_t * pulGatewayAddress,  
                                        const uint32_t * pulDNSServerAddress,  
                                        struct xNetworkEndPoint * pxEndPoint );  
```

```c
/*  
 * Send a ping using ICMPv6. When a ping is replied, the hook  
 * vApplicationPingReplyHook() will be called by the IP-task.  
 */  
BaseType_t FreeRTOS_SendPingRequestIPv6( const IPv6_Address_t * pxIPAddress,  
                                         size_t uxNumberOfBytesToSend,  
                                         TickType_t uxBlockTimeTicks );  
```

```c
/*  
 * Create an IPv6 address. This IPv6 address is based upon a prefix and a  
 * prefix length.  
 */  
BaseType_t FreeRTOS_CreateIPv6Address( IPv6_Address_t * pxIPAddress,  
                                       const IPv6_Address_t * pxPrefix,  
                                       size_t uxPrefixLength,  
                                       BaseType_t xDoRandom );  
```

```c
/*  
 * Send out an ND request for the IPv6 address contained in pxNetworkBuffer,  
 * and add an entry into the ND table that indicates that an ND reply is  
 * outstanding so re-transmissions can be generated.  
 */  
void vNDSendNeighbourSolicitation( NetworkBufferDescriptor_t * const pxNetworkBuffer,  
                                   const IPv6_Address_t * pxIPAddress );  
```

```c
/*  
 * FreeRTOS_ClearND() clears the cache that holds MAC- and IPv6 couples.  
 */  
void FreeRTOS_ClearND( void );  
```

```c
/*  
 * The last parameter is either ipTYPE_IPv4 or ipTYPE_IPv6.  
 */  
void * FreeRTOS_GetUDPPayloadBuffer_Multi( size_t uxRequestedSizeBytes,  
                                           TickType_t uxBlockTimeTicks,  
                                           uint8_t ucIPType );  
```

```c
/*  
 * Set the MAC-address that belongs to a given IPv6 multi-cast address.  
 */  
void vSetMultiCastIPv6MacAddress( IPv6_Address_t * pxAddress,  
                                  MACAddress_t * pxMACAddress );  
```


### Functions to find end-points

```c
/*  
 * Get the first Network Interface. The function is used to iterate through all  
 * end-points.  
 */  
NetworkInterface_t * FreeRTOS_FirstNetworkInterface( void );  
```

```c
/*  
 * Get the next Network Interface, used after calling FirstNetworkInterface().  
 */  
NetworkInterface_t * FreeRTOS_NextNetworkInterface( NetworkInterface_t * pxInterface );  
```

```c
/*  
 * Get the first end-point belonging to a given interface. When pxInterface  
 * is NULL, the very first end-point will be returned.  
 */  
NetworkEndPoint_t * FreeRTOS_FirstEndPoint( NetworkInterface_t * pxInterface );  
```

```c
/*  
 * Get the next end-point. When pxInterface is null, all end-points can be  
 * iterated. Used in combination with FreeRTOS_FirstEndPoint().  
 */  
NetworkEndPoint_t * FreeRTOS_NextEndPoint( NetworkInterface_t * pxInterface,  
                                           NetworkEndPoint_t * pxEndPoint );  
```

```c
/*  
 * Find the end-point with given IP-address.  
 */  
NetworkEndPoint_t * FreeRTOS_FindEndPointOnIP_IPv4( uint32_t ulIPAddress 
                                                    uint32_t ulWhere );  
```

```c
/* Find the end-point with given IP-address ( IPv6 only ). */  
NetworkEndPoint_t * FreeRTOS_FindEndPointOnIP_IPv6( const IPv6_Address_t * pxIPAddress );  
```

```c
/*  
 * Find the end-point with given MAC-address.The search can be limited by  
 * supplying a particular interface.  
 */  
NetworkEndPoint_t * FreeRTOS_FindEndPointOnMAC( const MACAddress_t * pxMACAddress,  
                                                const NetworkInterface_t * pxInterface );  
```

```c
/*  
 * Find the best fitting end-point to reach a given IP-address. Find an end-point  
 * whose IP-address is in the same network as the IP-address provided.  
 */  
NetworkEndPoint_t * FreeRTOS_FindEndPointOnNetMask( uint32_t ulIPAddress 
                                                    uint32_t ulWhere );  
```

```c
/* IPv6 only */
NetworkEndPoint_t * FreeRTOS_FindEndPointOnNetMask_IPv6( const IPv6_Address_t * pxIPv6Address );
```

```c
/* Get the first end-point belonging to a given interface.  
 *  
 * When pxInterface is NULL, the very first end-point will be returned ( IPv6  
 * only ).  
 */  
NetworkEndPoint_t * FreeRTOS_FirstEndPoint_IPv6( const NetworkInterface_t * pxInterface );  
```

```c
/*  
 * An Ethernet packet has come in on a certain network interface. Find the best  
 * matching end-point.  
 */  
NetworkEndPoint_t * FreeRTOS_MatchingEndpoint( const NetworkInterface_t * pxNetworkInterface,  
                                               const uint8_t * pucEthernetBuffer );  
```

```c
/*  
 * Find an end-point that has a defined gateway.  
 *  
 * xIPType should equal ipTYPE_IPv4 or ipTYPE_IPv6.  
 */  
NetworkEndPoint_t * FreeRTOS_FindGateWay( BaseType_t xIPType );  
```
