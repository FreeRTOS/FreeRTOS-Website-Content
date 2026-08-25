---
title: FreeRTOS-Plus-TCP API
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 主套接字函数

* [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
* [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)
* [FreeRTOS\_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect)
* [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen)
* [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept)
* [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send)
* [FreeRTOS\_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto)
* [FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv)
* [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom)
* [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt)
* [FreeRTOS\_shutdown()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/12-shutdown)
* [FreeRTOS\_closesocket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/13-close)
* [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select)


### 其他套接字函数

套接字函数使用小写格式，以符合 Berkeley 惯例。

* [FreeRTOS\_CreateSocketSet()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/15-createsocketset)
* [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET)
* [FreeRTOS\_FD\_CLR()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/17-FD_CLR)
* [FreeRTOS\_ISSET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/18-FD_ISSET)
* [FreeRTOS\_gethostbyname()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname)
* [FreeRTOS\_inet\_ntoa()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/20-inet_ntoa)
* [FreeRTOS\_inet\_addr\_quick()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/21-inet_addr_quick)
* [FreeRTOS\_inet\_addr()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/22-inet_addr)
* [FreeRTOS\_htons()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl)
* [FreeRTOS\_ntohs()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl)
* [FreeRTOS\_htonl()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl)
* [FreeRTOS\_ntohl()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl)
* [FreeRTOS\_outstanding()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/24-outstanding)
* [FreeRTOS\_recvcount()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/25-recvcount)
* [FreeRTOS\_issocketconnected()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/26-issocketconnected)
* [FreeRTOS\_GetLocalAddress()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/27-getlocaladdress)
* [FreeRTOS\_GetRemoteAddress()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/28-getremoteaddress)
* [FreeRTOS\_maywrite()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/29-maywrite)


### IP 函数

IP 函数使用大小写混合格式，以符合 FreeRTOS 惯例。

* [FreeRTOS\_IPInit() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit)
* [FreeRTOS\_IPInit\_Multi()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/31-FreeRTOS_IPInit_Multi)
* [FreeRTOS\_GetAddressConfiguration() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/32-FreeRTOS_GetAddressConfiguration)
* [FreeRTOS\_GetEndPointConfiguration()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/32-FreeRTOS_GetEndPointConfiguration)
* [FreeRTOS\_GetUDPPayloadBuffer() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/34-FreeRTOS_GetUDPPayloadBuffer)
* [FreeRTOS\_GetUDPPayloadBuffer\_Multi()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/34-FreeRTOS_GetUDPPayloadBuffer)
* [FreeRTOS\_ReleaseUDPPayloadBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/35-FreeRTOS_ReleaseUDPPayloadBuffer)
* [FreeRTOS\_SendPingRequest()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/36-FreeRTOS_SendPingRequest)
* [FreeRTOS\_GetMACAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/37-FreeRTOS_GetMACAddress)
* [FreeRTOS\_GetIPAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/38-FreeRTOS_GetIPAddress)
* [FreeRTOS\_GetIPType()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/39-FreeRTOS_GetIPType)
* [FreeRTOS\_GetGatewayAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/49-FreeRTOS_GetGatewayAddress)
* [FreeRTOS\_GetDNSServerAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/41-FreeRTOS_GetDNSServerAddress)
* [FreeRTOS\_GetNetmask() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/42-FreeRTOS_GetNetmask)
* [FreeRTOS\_OutputARPRequest()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/43-FreeRTOS_OutputARPRequest)
* [FreeRTOS\_IsNetworkUp()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/44-FreeRTOS_IsNetworkUp)
* [FreeRTOS\_AllEndPointUp()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/45-FreeRTOS_AllEndPointsUp)
* [FreeRTOS\_IsEndPointUp()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/46-FreeRTOS_IsEndPointUp)
* [FreeRTOS\_SetAddressConfiguration() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/47-FreeRTOS_SetAddressConfiguration)
* [FreeRTOS\_SetEndPointConfiguration() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/48-FreeRTOS_SetEndPointConfiguration)
* [FreeRTOS\_SetGatewayAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/40-FreeRTOS_SetGatewayAddress)
* [FreeRTOS\_SetIPAddress() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/50-FreeRTOS_SetIPAddress)
* [FreeRTOS\_SetNetmask() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/51-FreeRTOS_SetNetmask)
* [FreeRTOS\_SignalSocket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
* [FreeRTOS\_FillEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/53-FreeRTOS_FillEndPoint)
* [FreeRTOS\_FillEndPoint_IPv6()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/54-FreeRTOS_FillEndPoint_IPv6)



### 事件钩子函数

* [eApplicationProcessCustomFrameHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/55-eApplicationProcessCustomFrameHook)
* [pcApplicationHostnameHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/56-pcApplicationHostnameHook)
* [vApplicationIPNetworkEventHook_Multi()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/58-vApplicationIPNetworkEventHook_Multi)
* [vApplicationIPNetworkEventHook() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook)
* [vApplicationPingReplyHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/59-vApplicationPingReplyHook)
* [xApplicationDHCPHook() \[Deprecated\]](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/60-xApplicationDHCPHook)
* [xApplicationDHCPHook\_Multi()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/64-xApplicationDHCPHook_Multi)
* [xApplicationDNSQueryHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/61-xApplicationDNSQueryHook)
* [xApplicationDNSQueryHook()\_Multi](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/65-xApplicationDNSQueryHook_Multi)


### 应用程序提供的函数

* [ulApplicationGetNextSequenceNumber()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/62-ulApplicationGetNextSequenceNumber)
* [xApplicationGetRandomNumber()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/63-xApplicationGetRandomNumber)


### DNS 函数

* [FreeRTOS\_getaddrinfo](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/66-FreeRTOS_getaddrinfo)
* [FreeRTOS\_getaddrinfo_a](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/67-FreeRTOS_getaddrinfo_a)
