---
title: NBNS
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


NBNS (sometimes called WINS) stands for [NetBIO Name Service](http://wiki.wireshark.org/NetBIOS/NBNS),
which is a protocol for [name resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution).

NBNS performs the same function as [LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR),
but using [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) broadcast packets
instead of multi cast packets. Browsers normally only attempt to use
NBNS after attempts to use LLMNR have failed.

[ipconfigUSE\_NBNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_LLMNR)
must be set to 1 in FreeRTOSIPConfig.h for NBNS to be
enabled. As with LLMNR, the application writer must provide the
xApplicationDNSQueryHook() callback function which takes a
character pointer as a parameter and returns pdTRUE if the
name passed into the function matches a name used to identify the node.
