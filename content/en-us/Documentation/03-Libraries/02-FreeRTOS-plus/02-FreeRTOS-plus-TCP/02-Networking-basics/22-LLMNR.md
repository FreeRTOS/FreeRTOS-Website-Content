---
title: LLMNR
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

LLMNR stands for [Link Local Multicast Name Resolution](http://en.wikipedia.org/wiki/Link-local_Multicast_Name_Resolution),
which is a protocol for [name resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution).

LLMNR is a multicast protocol used on local area networks. It is the method used by all major web browsers 
to resolve names that do not include a dot ('.'). For example, if you attempt to open the web page:
http://my\_freertos\_device/index.html, then the web browser would send an LLMNR request to try to resolve 
the name 'my\_freertos\_device'.

All LLMNR packets are sent to IP address 224.0.0.252 on MAC address
01:00:5E:00:00:FC, so the network interface (MAC) must be programmed to
accept packets on that address for LLMNR to function. In 
addition [ipconfigUSE\_LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_LLMNR)
must be defined as 1 in FreeRTOSIPConfig.h, and the
user must provide the implementation of a callback function xApplicationDNSQueryHook()
that takes a char pointer as a parameter and returns pdTRUE if the name
passed into the function matches a name used to identify the node.

