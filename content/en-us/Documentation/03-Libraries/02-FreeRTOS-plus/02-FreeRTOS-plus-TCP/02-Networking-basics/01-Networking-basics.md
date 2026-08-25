---
title: Embedded TCP/IP Networking Basics
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Introduction

The page links below aim to provide a brief introduction to the concepts and terminology of
TCP/IP and UDP/IP networks, and how they relate to the FreeRTOS-Plus-TCP implementation.
The pages do nothing more than
provide a top level overview of subjects that could be comprehensive
topics in their own right, so links to external references are also
provided where appropriate.

Do not be put off by the apparent complexity of the subject. FreeRTOS-Plus-TCP
takes care of implementing the protocols. FreeRTOS-Plus-TCP users only need
to know enough to understand the [FreeRTOS-Plus-TCP configuration](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) options, and
how to use the standard [Berkeley sockets](http://en.wikipedia.org/wiki/Berkeley_sockets)
interface to send and receive data.
A [FreeRTOS-Plus-TCP networking tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
with simple worked examples and an API
reference are provided on this website.

The following links provide a glossary of networking terminology, and
are best read in order:

* [Ethernet Networking and Addressing](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
* [MTU - Maximum Transmission Unit](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/03-MTU)
* [IP Networking](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/04-Internet-protocol)
* [IP Network Addressing](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
* [ARP - Address Resolution Protocol](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/06-ARP)
* [Subnets / Netmasks](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
* [Gateways and Routers](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
* [UDP Networking](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP)
* [TCP Networking](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
* [MSS - Maximum Segment Size](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/11-MSS)
* [Port Numbers](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number)
* [Sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
* [Binding](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)
* [Clients and Servers](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_client_server)
* [Static IP Addresses](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
* [DHCP - Dynamic Host Control Protocol](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4)
* [Name Resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution)
* [DNS - Domain Name Service](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS)
* [LLMNR - Link-local Multicast Name Resolution](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR)
* [NBNS - NetBIOS Name Service](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/23-NetBIOS)
* [Bytes Order and Endian](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/25-Endian)
