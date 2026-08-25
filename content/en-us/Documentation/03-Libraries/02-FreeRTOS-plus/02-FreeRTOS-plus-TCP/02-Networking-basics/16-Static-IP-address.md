---
title: Static IP Address
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

It has already been noted that each network node has an [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/05-IP-address). If the IP address is 'static' 
then it is pre-assigned and never changed.

In the FreeRTOS-Plus-TCP API, before 
calling [FreeRTOS\_IPInit\_Multi](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/31-FreeRTOS_IPInit_Multi), 
you need to add an IPv4 address as an endpoint 
using [FreeRTOS\_FillEndPoint](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/53-FreeRTOS_FillEndPoint) or an IPv6 address 
using [FreeRTOS\_FillEndPoint\_IPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/54-FreeRTOS_FillEndPoint_IPv6) 
as one of its parameters. The Endpoints/IP address will be used as a static IP address 
if [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 
or [ipconfigUSE\_DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcpv6) 
is set to 0 or if [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 
or [ipconfigUSE\_DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcpv6) is 
set to 1 but a [DHCP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) cannot be contacted.

