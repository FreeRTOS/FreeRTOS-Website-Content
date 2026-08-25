---
title: IP Address
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Different nodes on the same [IP network](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol)
are identified by their IP
address. For example, each network interface on the computer on which
you are reading this text will have a different IP address, as will
every remote interface on the network to which your computer is connected.

There are two IP address formats in common use. Currently the huge majority
of remote addresses use the IPv4 format, which is a 32-bit
number, but is most often written as four separate octets (8-bit numbers)
separated by a dot. For example "192.168.0.32".


The other version of IP addressing which is also widely used is the [IPv6](https://en.wikipedia.org/wiki/IPv6) 
format. An IPv6 address is a 128-bit number, represented in 8 groups of 16 bits each. Each group is written 
as four hexadecimal digits and the groups are separated by colons (:). An example of this representation is 
2001:0db8:0000:0000:0000:ff00:0042:8329. For convenience and clarity, the representation of an IPv6 address 
may be shortened to 2001:db8::ff00:42:8329. 
See [Address representation](https://en.wikipedia.org/wiki/IPv6#Address_representation) for more detail.

See also [Static IP Address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address),
[DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4),
and [DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/18-DHCPv6).

