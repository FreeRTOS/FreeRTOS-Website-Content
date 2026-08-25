---
title: ARP
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


ARP stands for [Address Resolution Protocol](http://en.wikipedia.org/wiki/Address_Resolution_Protocol).

[IP packets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol)
are sent between [IP addresses](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address), but the [Ethernet frames](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
in which they are packaged
are sent between MAC (hardware) addresses. Therefore the
MAC address of the destination IP address must be known before an IP
packet can be sent onto an Ethernet network.

The Address Resolution Protocol (ARP) is used to obtain MAC address information. FreeRTOS-Plus-TCP (like 
most if not all IP stacks) stores IP address to MAC address mappings in an ARP table (sometimes called 
the ARP cache). ARP is handled automatically by the TCP/IP stack.

