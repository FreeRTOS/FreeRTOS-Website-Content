---
title: DNS
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

DNS stands for [Domain Name System](http://en.wikipedia.org/wiki/Domain_Name_System),
which is a form of [domain name resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution).

DNS maps static and easily human readable textual (rather than numerical) names 
to [IP addresses](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address).
A domain name server resolves the text domain name to the appropriate IP address. For example, 
entering "ping www.freertos.org" in the command console of a desktop computer will show a ping request 
being sent to the IP address 195.8.66.1 (at the time of writing - the IP address may change) because a 
DNS server resolved the string "www.freertos.org" to the IP address 195.8.66.1.

If [ipconfigUSE\_DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DNS)
is set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
then the FreeRTOS-Plus-TCP API function [FreeRTOS\_gethostbyname()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname)
can be used to resolve a text name to an IP address.

Like the IP address of the node running FreeRTOS-Plus-TCP, the IP address of a domain name server can 
be configured either statically as a parameter 
to [FreeRTOS\_FillEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/53-FreeRTOS_FillEndPoint),
or  [FreeRTOS\_FillEndPoint\_IPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/54-FreeRTOS_FillEndPoint_IPv6),
or dynamically from a [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) server.

