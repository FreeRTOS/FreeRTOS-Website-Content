---
title: Subnet and Netmask
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Subnet

Subnets allow the most significant bits of 
an [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address) 
to be interpreted as routing information, and the least significant bits of an IP address to be interpreted 
as a unique node address on the local [IP network](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol). The local IP network (subnet) is the 
network that can be addressed without using 
a [gateway or router](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router). 
Traffic between subnets must pass through a router. Subnetting is supported by 
both [IPv4](https://en.wikipedia.org/wiki/Subnet#Internet_Protocol_version_4) 
and [IPv6](https://en.wikipedia.org/wiki/Subnet#Internet_Protocol_version_6) networks. 


### Netmask

The number of bits that are interpreted as containing routing information are determined by the net mask. 
A bit being set in the netmask means that bit is interpreted as routing information. For example, if the 
IPv4 address is 10.134.134.10 and the netmask is 255.255.0.0 then the 10.134 provides the routing information 
and 134.10 provides the local address information. IP addresses that start with 10.134 can be sent directly 
to their destination on the local network. IP addresses that start with any other numbers are not on the
local network so must instead be sent to the router.

The netmask used in IPv6 is called the prefix length or CIDR notation which stands for Classless Inter-Domain 
Routing. In IPv6 the prefix length is represented by the number of bits that are used to identify the network 
portion of the address. The remaining bits are used to identify the hosts. For example, if the IPv6 address 
is 2001:0db8:2345:: and a prefix length is 64, the corresponding netmask is /64. This means the first 64 bits 
of IPv6 address are used to identify the network and the remaining 64 bits are used to identify hosts within 
the network.

