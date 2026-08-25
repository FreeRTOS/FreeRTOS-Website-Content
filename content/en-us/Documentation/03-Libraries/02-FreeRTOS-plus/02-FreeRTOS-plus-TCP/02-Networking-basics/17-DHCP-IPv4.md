---
title: "DHCP (IPv4)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


DHCP stands for [Dynamic Host Control Protocol](http://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol).

[Static IP addresses](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
are useful during application development, but they are impractical for product deployment because:

* They need to be hard coded either in the executable binary or external flash memory.

* IP addresses cannot be pre-assigned to products without prior knowledge of the network environment 
  in which the products will be deployed.

* There is no prior knowledge of how many nodes will exist on the network, or indeed how many of the 
  possible total number of nodes will be active at any one time.

DHCP provides an alternative to static IPv4 address assignment. DHCP servers exist on local networks to 
dynamically allocate IP addresses to nodes on the same network. When a network enabled product boots up 
it contacts the DHCP server to request its IP address, removing the need for each node to be statically 
configured.

If [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) and [ipconfigUSE_IPv4](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) 
are set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) then FreeRTOS-Plus-TCP will attempt to obtain 
its IP address from a DHCP server, and only revert to using a static IP address (AutoIP is also on the 
roadmap) if a DHCP server cannot be contacted.

The device running FreeRTOS-Plus-TCP can register its hostname with the DHCP server. See 
the [ipconfigDHCP\_REGISTER\_HOSTNAME](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigDHCP_REGISTER_HOSTNAME) configuration 
constant for more information.

Expert users can influence the DHCP process using an [application DHCP hook](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp_HOOK)
(or 'callback') function.

Also, see [DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/18-DHCPv6) for dynamic assignment of an IPv6 address.

