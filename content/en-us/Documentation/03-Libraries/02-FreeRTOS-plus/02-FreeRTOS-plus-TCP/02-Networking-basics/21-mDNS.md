---
title: mDNS
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

mDNS stands for [Multicast Domain Name System](https://en.wikipedia.org/wiki/Multicast_DNS), which is a 
form of [domain name resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution).

mDNS is a variation of [DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS) service, which is a form 
of [domain name resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution). When an mDNS client 
needs to resolve a hostname, it sends an [IP multicast](https://en.wikipedia.org/wiki/IP_multicast) query message 
that asks the host that has that name to identify itself.

An mDNS message is a multicast UDP packet sent using the following addressing:

+ [IPv4 address](https://en.wikipedia.org/wiki/IPv4_address) 224.0.0.251 
  or [IPv6 address](https://en.wikipedia.org/wiki/IPv6_address) ff02::fb
+ [UDP port](https://en.wikipedia.org/wiki/UDP_port) 5353
+ When using [Ethernet frames](https://en.wikipedia.org/wiki/Ethernet_frame), 
  the [standard IP multicast MAC address](https://en.wikipedia.org/wiki/Multicast_address#Ethernet) 
  01:00:5E:00:00:FB (for [IPv4](https://en.wikipedia.org/wiki/IPv4) or 33:33:00:00:00:FB 
  (for [IPv6](https://en.wikipedia.org/wiki/IPv6)

If [ipconfigUSE\_DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dns) 
and [ipconfigUSE\_MDNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_mdns) 
are set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) then the FreeRTOS-Plus-TCP API 
function [FreeRTOS\_gethostbyname()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname) 
can be used to resolve a text name to an IP address when the hostname has a postfix ".local".

