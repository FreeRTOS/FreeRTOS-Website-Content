---
title: FreeRTOS-Plus-TCP IPv6 Functionality
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

IPv6 functionality is enabled by default from FreeRTOS V4.0.0 onwards. IPv6 functionality can be disabled 
as a compile time option using the flag `ipconfigUSE_IPv6`. The IPv6 IP-addresses can be configured either 
statically, or automatically using either Router Advertisement (RA) (along with SLAAC) or DHCP 
version 6 (DHCPv6).

When using Stateless address auto-configuration (SLAAC), the device will first receive the address of a
network prefix. Then it will take a random IP-address that is valid, and it will test if the address is
already in use in the LAN. These addresses can be public Internet addresses, which means that NAT is not
needed, only a IPv6 gateway.

The IPv6 functionality adds 3 new modules:

**FreeRTOS\_Routing**   
Introduces the concept of end-points and address resolution. See the page about “multiple interfaces“.
These are necessary to get both IPv4 and IPv6 addresses.

**FreeRTOS\_ND**   
[Neighbourhood Discovery](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/24-ND) (ND): this handles all ICMPv6 messages. It does 
the (MAC-) address resolution, along with a cache, ping and router solicitation.

**FreeRTOS\_DHCPv6**   
This is the [DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/18-DHCPv6) client. Note that it will create a session for each of the 
end-point that has DHCP enabled.

**FreeRTOS\_RA**   
[Router Advertisement](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/28-RA): This implements Router Solicitation and SLAAC. 
An IPv6 router advertises a network prefix, and the end-point
will select its own IP-address. By issuing Neighbour Solicitation messages, it will find out 
if the chosen address is unique.


## Demo

The [how to setup and run a demo for IPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/IPv6/ipv6-demo) page provides instructions on setting up an IPv6 demo


## IPv6 functions

The [IPv6 and multiple interface functions](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/03-IPv6-multi-functions) 
page provides information on new functions required to use both IPv6 and multiple interfaces.

