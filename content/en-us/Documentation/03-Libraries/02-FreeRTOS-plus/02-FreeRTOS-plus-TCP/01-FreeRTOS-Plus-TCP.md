---
title: FreeRTOS-Plus-TCP
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Open source and thread safe TCP/IP stack for FreeRTOS**


FreeRTOS-Plus-TCP is a scalable, open source and thread safe TCP/IP stack for FreeRTOS.
 
FreeRTOS-Plus-TCP provides a familiar and standards based Berkeley sockets interface, making it as simple to
use and as quick to learn as possible. An alternative callback interface is also available for advanced users.
 
FreeRTOS-Plus-TCP's features and RAM footprint are fully scalable, making FreeRTOS-Plus-TCP equally applicable 
to smaller lower throughput microcontrollers as larger higher throughput microprocessors.
 
See the FreeRTOS-Plus-TCP section in the tree menu (on the left) for 
a [FreeRTOS-Plus-TCP networking tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial/), [porting guide](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/01-FreeRTOS_TCP_Porting/), [API documentation](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs), 
and a link to the [free TCP/IP source code download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).
 
[![RTOS, TCP, FAT](/media/2018/0.png)](https://www.youtube.com/v/gZt5G5pWUv4?autoplay=1&rel=0&enablejsapi=1&playerapiid=ytplayer "RTOS, TCP")  
*Filezilla FTP'ing large and small files to a 66MHz MCU running FreeRTOS-Plus-TCP and [**FreeRTOS-Plus-FAT**](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT/)*

 
**Features**
+ Berkeley sockets API
+ Optionally supports TCP sliding windows
+ Fully re-entrant and thread safe API
+ Includes [ARP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/06-ARP/), [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4/), [DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS), [LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR), [NBNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/23-NetBIOS), [RA](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/28-RA), [ND](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/24-ND), [ICMP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/26-ICMP), 
and [ICMPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/27-ICMPv6)
+ Gratuitous ARPs
+ Static, DHCP and Auto-IP address assignment
+ Can also be used as a UDP only stack
+ Optionally callback interface
+ Optionally fragment outgoing packets

**Berkeley Sockets API**
+ [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/02-socket/)
+ [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt/)
+ [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind/)
+ [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen/)
+ [FreeRTOS\_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect/)
+ [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept/)
+ [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send/) / [FreeRTOS\_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto/)
+ [FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv/) / [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom/)
+ etc.


FreeRTOS-Plus-TCP Supports the following build combinations, (by default IPv4, IPv6 and TCP are enabled):

| Build combination       | ipconfigUSE\_IPv4 | ipconfigUSE\_IPv6 | ipconfigUSE\_TCP |
| ----------------------- | ----------------- | ----------------- |----------------- |
| IPv4 + UDP              | 1                 | 0                 | 0                |
| IPv4 + UDP + TCP        | 1                 | 0                 | 1                |
| IPv6 + UDP              | 0                 | 1                 | 0                |
| IPv6 + UDP + TCP        | 0                 | 1                 | 1                |
| IPv4 + IPv6 + UDP       | 1                 | 1                 | 0                |
| IPv4 + IPv6 + UDP + TCP | 1                 | 1                 | 1                |


**Code Size (example generated with GCC for ARM Cortex-M) with IPv4 & IPv6 Enabled**
| GCC ARM `-01 [-mcpu=cortex-m4 -std=gnu11]` |  | GCC ARM `-0s [-mcpu=cortex-m4 -std=gnu11]` |  |
| ---- | ---- | ---- | ---- | 
| **File** | **Size** | **File** | **Size** |
| FreeRTOS\_ARP.c | 2400 | FreeRTOS\_ARP.c | 2094 |
| FreeRTOS\_BitConfig.c | 452 | FreeRTOS\_BitConfig.c | 400 |
| FreeRTOS\_DHCP.c | 2689 | FreeRTOS\_DHCP.c | 2359 |
| FreeRTOS\_DHCPv6.c | 2934 | FreeRTOS\_DHCPv6.c | 2676 |
| FreeRTOS\_DNS.c | 1463 | FreeRTOS\_DNS.c | 1309 |
| FreeRTOS\_DNS\_Cache.c | 980 | FreeRTOS\_DNS\_Cache.c | 860 |
| FreeRTOS\_DNS\_Callback.c | 408 | FreeRTOS\_DNS\_Callback.c | 396 |
| FreeRTOS\_DNS\_Networking.c | 188 | FreeRTOS\_DNS\_Networking.c | 178 |
| FreeRTOS\_DNS\_Parser.c | 910 | FreeRTOS\_DNS\_Parser.c | 782 |
| FreeRTOS\_ICMP.c | 80 | FreeRTOS\_ICMP.c | 78 |
| FreeRTOS\_IP.c | 2584 | FreeRTOS\_IP.c | 2366 |
| FreeRTOS\_IP\_Timers.c | 756 | FreeRTOS\_IP\_Timers.c | 682 |
| FreeRTOS\_IP\_Utils.c | 2495 | FreeRTOS\_IP\_Utils.c | 2177 |
| FreeRTOS\_IPv4.c | 296 | FreeRTOS\_IPv4.c | 208 |
| FreeRTOS\_IPv4\_Sockets.c | 292 | FreeRTOS\_IPv4\_Sockets.c | 190 |
| FreeRTOS\_IPv4\_Utils.c | 180 | FreeRTOS\_IPv4\_Utils.c | 134 |
| FreeRTOS\_IPv6.c | 790 | FreeRTOS\_IPv6.c | 644 |
| FreeRTOS\_IPv6\_Sockets.c | 885 | FreeRTOS\_IPv6\_Sockets.c | 769 |
| FreeRTOS\_IPv6\_Utils.c | 290 | FreeRTOS\_IPv6\_Utils.c | 292 |
| FreeRTOS\_ND.c | 1850 | FreeRTOS\_ND.c | 1704 |
| FreeRTOS\_RA.c | 1228 | FreeRTOS\_RA.c | 1022 |
| FreeRTOS\_Routing.c | 1739 | FreeRTOS\_Routing.c | 1559 |
| FreeRTOS\_Sockets.c | 7272 | FreeRTOS\_Sockets.c | 6206 |
| FreeRTOS\_Stream\_Buffer.c | 498 | FreeRTOS\_Stream\_Buffer.c | 424 |
| FreeRTOS\_TCP\_IP.c | 1186 | FreeRTOS\_TCP\_IP.c | 942 |
| FreeRTOS\_TCP\_IP\_IPV4.c | 608 | FreeRTOS\_TCP\_IP\_IPV4.c | 430 |
| FreeRTOS\_TCP\_IP\_IPV6.c | 614 | FreeRTOS\_TCP\_IP\_IPV6.c | 482 |
| FreeRTOS\_TCP\_Reception.c | 832 | FreeRTOS\_TCP\_Reception.c | 678 |
| FreeRTOS\_TCP\_State\_Handling.c | 1690 | FreeRTOS\_TCP\_State\_Handling.c | 1464 |
| FreeRTOS\_TCP\_State\_Handling\_IPV4.c | 276 | FreeRTOS\_TCP\_State\_Handling\_IPV4.c | 224 |
| FreeRTOS\_TCP\_State\_Handling\_IPV6.c | 304 | FreeRTOS\_TCP\_State\_Handling\_IPV6.c | 256 |
| FreeRTOS\_TCP\_Transmission.c | 1866 | FreeRTOS\_TCP\_Transmission.c | 1636 |
| FreeRTOS\_TCP\_Transmission\_IPV4.c | 788 | FreeRTOS\_TCP\_Transmission\_IPV4.c | 658 |
| FreeRTOS\_TCP\_Transmission\_IPV6.c | 996 | FreeRTOS\_TCP\_Transmission\_IPV6.c | 918 |
| FreeRTOS\_TCP\_Utils.c | 22 | FreeRTOS\_TCP\_Utils.c | 14 |
| FreeRTOS\_TCP\_Utils\_IPV4.c | 72 | FreeRTOS\_TCP\_Utils\_IPV4.c | 46 |
| FreeRTOS\_TCP\_Utils\_IPV6.c | 50 | FreeRTOS\_TCP\_Utils\_IPV6.c | 48 |
| FreeRTOS\_TCP\_WIN.c | 2086 | FreeRTOS\_TCP\_WIN.c | 1768 |
| FreeRTOS\_Tiny\_TCP.c | 302 | FreeRTOS\_Tiny\_TCP.c | 290 |
| FreeRTOS\_UDP\_IP.c | 116 | FreeRTOS\_UDP\_IP.c | 112 |
| FreeRTOS\_UDP\_IPv4.c | 620 | FreeRTOS\_UDP\_IPv4.c | 548 |
| FreeRTOS\_UDP\_IPv6.c | 756 | FreeRTOS\_UDP\_IPv6.c | 656 |
| Total | 46843 | Total | 40679 |


**Code Size (example generated with GCC for ARM Cortex-M) with only IPv4 Enabled**
| GCC ARM `-01 [-mcpu=cortex-m4 -std=gnu11]` |  | GCC ARM `-0s [-mcpu=cortex-m4 -std=gnu11]` |  |
| ---- | ---- | ---- | ---- | 
| **File** | **Size** | **File** | **Size** |
| FreeRTOS\_ARP.c | 2282 | FreeRTOS\_ARP.c | 1990 |
| FreeRTOS\_BitConfig.c | 452 | FreeRTOS\_BitConfig.c | 400 |
| FreeRTOS\_DHCP.c | 2613 | FreeRTOS\_DHCP.c | 2293 |
| FreeRTOS\_DNS.c | 1225 | FreeRTOS\_DNS.c | 1005 |
| FreeRTOS\_DNS\_Cache.c | 856 | FreeRTOS\_DNS\_Cache.c | 734 |
| FreeRTOS\_DNS\_Callback.c | 408 | FreeRTOS\_DNS\_Callback.c | 396 |
| FreeRTOS\_DNS\_Networking.c | 188 | FreeRTOS\_DNS\_Networking.c | 178 |
| FreeRTOS\_DNS\_Parser.c | 910 | FreeRTOS\_DNS\_Parser.c | 782 |
| FreeRTOS\_ICMP.c | 80 | FreeRTOS\_ICMP.c | 78 |
| FreeRTOS\_IP.c | 2316 | FreeRTOS\_IP.c | 2108 |
| FreeRTOS\_IP\_Timers.c | 734 | FreeRTOS\_IP\_Timers.c | 656 |
| FreeRTOS\_IP\_Utils.c | 2243 | FreeRTOS\_IP\_Utils.c | 1981 |
| FreeRTOS\_IPv4.c | 296 | FreeRTOS\_IPv4.c | 208 |
| FreeRTOS\_IPv4\_Sockets.c | 292 | FreeRTOS\_IPv4\_Sockets.c | 190 |
| FreeRTOS\_IPv4\_Utils.c | 180 | FreeRTOS\_IPv4\_Utils.c | 134 |
| FreeRTOS\_Routing.c | 1183 | FreeRTOS\_Routing.c | 1019 |
| FreeRTOS\_Sockets.c | 6914 | FreeRTOS\_Sockets.c | 5856 |
| FreeRTOS\_Stream\_Buffer.c | 498 | FreeRTOS\_Stream\_Buffer.c | 424 |
| FreeRTOS\_TCP\_IP.c | 1172 | FreeRTOS\_TCP\_IP.c | 930 |
| FreeRTOS\_TCP\_IP\_IPV4.c | 608 | FreeRTOS\_TCP\_IP\_IPV4.c | 430 |
| FreeRTOS\_TCP\_Reception.c | 808 | FreeRTOS\_TCP\_Reception.c | 658 |
| FreeRTOS\_TCP\_State\_Handling.c | 1676 | FreeRTOS\_TCP\_State\_Handling.c | 1448 |
| FreeRTOS\_TCP\_State\_Handling\_IPV4.c | 276 | FreeRTOS\_TCP\_State\_Handling\_IPV4.c | 224 |
| FreeRTOS\_TCP\_Transmission.c | 1788 | FreeRTOS\_TCP\_Transmission.c | 1548 |
| FreeRTOS\_TCP\_Transmission\_IPV4.c | 784 | FreeRTOS\_TCP\_Transmission\_IPV4.c | 650 |
| FreeRTOS\_TCP\_Utils.c | 18 | FreeRTOS\_TCP\_Utils.c | 12 |
| FreeRTOS\_TCP\_Utils\_IPV4.c | 72 | FreeRTOS\_TCP\_Utils\_IPV4.c | 46 |
| FreeRTOS\_TCP\_WIN.c | 2086 | FreeRTOS\_TCP\_WIN.c | 1768 |
| FreeRTOS\_Tiny\_TCP.c | 302 | FreeRTOS\_Tiny\_TCP.c | 290 |
| FreeRTOS\_UDP\_IP.c | 82 | FreeRTOS\_UDP\_IP.c | 72 |
| FreeRTOS\_UDP\_IPv4.c | 616 | FreeRTOS\_UDP\_IPv4.c | 544 |
| Total | 33958 | Total | 29052 |

**Code Size (example generated with GCC for ARM Cortex-M) with only IPv6 Enabled**
| GCC ARM `-01 [-mcpu=cortex-m4 -std=gnu11]` |  | GCC ARM `-0s [-mcpu=cortex-m4 -std=gnu11]` |  |
| ---- | ---- | ---- | ---- | 
| **File** | **Size** | **File** | **Size** |
| FreeRTOS\_ARP.c | 1294 | FreeRTOS\_ARP.c | 1090 |
| FreeRTOS\_BitConfig.c | 452 | FreeRTOS\_BitConfig.c | 400 |
| FreeRTOS\_DHCPv6.c | 2934 | FreeRTOS\_DHCPv6.c | 2676 |
| FreeRTOS\_ICMP.c | 80 | FreeRTOS\_ICMP.c | 78 |
| FreeRTOS\_IP.c | 2274 | FreeRTOS\_IP.c | 2082 |
| FreeRTOS\_IP\_Timers.c | 648 | FreeRTOS\_IP\_Timers.c | 590 |
| FreeRTOS\_IP\_Utils.c | 2411 | FreeRTOS\_IP\_Utils.c | 2095 |
| FreeRTOS\_IPv6.c | 790 | FreeRTOS\_IPv6.c | 644 |
| FreeRTOS\_IPv6\_Sockets.c | 885 | FreeRTOS\_IPv6\_Sockets.c | 769 |
| FreeRTOS\_IPv6\_Utils.c | 290 | FreeRTOS\_IPv6\_Utils.c | 292 |
| FreeRTOS\_ND.c | 1850 | FreeRTOS\_ND.c | 1704 |
| FreeRTOS\_RA.c | 1228 | FreeRTOS\_RA.c | 1022 |
| FreeRTOS\_Routing.c | 1357 | FreeRTOS\_Routing.c | 1269 |
| FreeRTOS\_Sockets.c | 6910 | FreeRTOS\_Sockets.c | 5982 |
| FreeRTOS\_Stream\_Buffer.c | 498 | FreeRTOS\_Stream\_Buffer.c | 424 |
| FreeRTOS\_TCP\_IP.c | 1176 | FreeRTOS\_TCP\_IP.c | 934 |
| FreeRTOS\_TCP\_IP\_IPV6.c | 614 | FreeRTOS\_TCP\_IP\_IPV6.c | 482 |
| FreeRTOS\_TCP\_Reception.c | 818 | FreeRTOS\_TCP\_Reception.c | 666 |
| FreeRTOS\_TCP\_State\_Handling.c | 1676 | FreeRTOS\_TCP\_State\_Handling.c | 1448 |
| FreeRTOS\_TCP\_State\_Handling\_IPV6.c | 304 | FreeRTOS\_TCP\_State\_Handling\_IPV6.c | 256 |
| FreeRTOS\_TCP\_Transmission.c | 1814 | FreeRTOS\_TCP\_Transmission.c | 1588 |
| FreeRTOS\_TCP\_Transmission\_IPV6.c | 996 | FreeRTOS\_TCP\_Transmission\_IPV6.c | 918 |
| FreeRTOS\_TCP\_Utils.c | 18 | FreeRTOS\_TCP\_Utils.c | 12 |
| FreeRTOS\_TCP\_Utils\_IPV6.c | 50 | FreeRTOS\_TCP\_Utils\_IPV6.c | 48 |
| FreeRTOS\_TCP\_WIN.c | 2086 | FreeRTOS\_TCP\_WIN.c | 1768 |
| FreeRTOS\_Tiny\_TCP.c | 302 | FreeRTOS\_Tiny\_TCP.c | 290 |
| FreeRTOS\_UDP\_IP.c | 94 | FreeRTOS\_UDP\_IP.c | 90 |
| FreeRTOS\_UDP\_IPv6.c | 720 | FreeRTOS\_UDP\_IPv6.c | 616 |
| Total | 34569 | Total | 30233 |


Compiler: arm-none-eabi-gcc (GNU Tools for STM32) 10.3.1
Version used for object size calculation: [bb654636](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/commit/bb654636d2cccd1121aeef681f005dfe8e38ca1a)

