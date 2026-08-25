---
title: Router and Gateway
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Router

The [netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet) 
is used to sub-divide an [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
into bytes that provide routing information and bytes that provide local address information. If a 
destination IP address bitwise ANDed with the subnet mask does **not** match the local IP address 
bitwise ANDed with the subnet mask then the two IP addresses do **not** exist on the same network.
In this case the packet being sent to the destination address cannot be sent directly, and must 
instead be sent to a router for intelligent inter-network routing.


### Gateway

The Gateway address is the IP address of the router - the router being the gateway to other (remote) 
networks.

FreeRTOS-Plus-TCP determines whether an [IP packet](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol) can be sent directly, or if it 
needs to be sent to a router. FreeRTOS-Plus-TCP users only need to provide a gateway address. Like the 
IP address, the IP address of a gateway can be configured either statically as a parameter 
to [FreeRTOS\_FillEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/53-FreeRTOS_FillEndPoint),
[FreeRTOS\_FillEndPoint_IPv6()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/54-FreeRTOS_FillEndPoint_IPv6),
or dynamically from a [DHCP/DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/18-DHCPv6) server.

