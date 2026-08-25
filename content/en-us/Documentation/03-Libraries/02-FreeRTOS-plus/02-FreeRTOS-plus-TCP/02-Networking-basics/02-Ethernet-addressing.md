---
title: Ethernet Address and Network
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Ethernet Network

Data is carried across a local Ethernet network in [Ethernet frames](http://en.wikipedia.org/wiki/Ethernet_frame).


### Ethernet Address

Ethernet frames are used to move data from node to node across
the network. The data in the Ethernet frame may just be
raw data, but is normally associated with another protocol
such as the [Internet Protocol](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol) (IP),
which in turn may carry further protocols such as [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) 
or [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP).

Different nodes on the same Ethernet network are identified by
their [MAC address](http://en.wikipedia.org/wiki/MAC_address) (hardware address).
MAC addresses are normally written as 6 octets (8-bit values) separated
by a colon. For example 00:12:34:56:78:90.
Each node on a local Ethernet network must have a unique MAC address.
