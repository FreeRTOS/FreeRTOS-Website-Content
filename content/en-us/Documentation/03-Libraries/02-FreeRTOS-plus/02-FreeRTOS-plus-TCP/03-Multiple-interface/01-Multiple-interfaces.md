---
title: FreeRTOS-Plus-TCP Multiple Interfaces
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction: Multiple interfaces, multiple end-points

We are introducing two new concepts in FreeRTOS-Plus-TCP: **interfaces** and **end-points**.

An interface corresponds to a Network Interface Card (NIC), and has the following properties: it has a set
of function addresses that perform the actual work i.e. initialise the NIC, send a
packet, get the Link Status, and as usual, each interface will start-up its own task
to do the reading of packets, and forward them to the IP-task. A message buffer will
contain pointers to both the Interface, and to the end-point on which it was received.

The concept of an end-point makes it possible to obtain multiple IP-addresses. Each
end-point has the following properties:

* IP-address ( either IPv4 or IPv6 )
* Default IP-address
* A prefix ( IPv6 ) or a net-mask ( IPv4 )
* Gateway address
* DNS addresses


### Single

Up until now, each FreeRTOS-Plus-TCP project had one physical interface, either a Local Area Network (LAN) or Wi-Fi.
The driver for this interface is linked into the code and offers the possibility to send and
receive packets. An application can only link with a single network interface, this is a
static (compile-time) choice.

The library expects a network interface that exchanges raw [IEEE 802.3](https://en.wikipedia.org/wiki/IEEE_802.3)
packets. Here is an example of an application with a single interface:   
![](/media/2020/Screen-Shot-2020-12-11-at-12.30.48-PM-1024x620.png)

An application can communicate with other nodes on the same LAN. The physical (MAC-) addresses are
looked up by using ARP. The bindings can be stored in a cache.

When an application wants to connect to the Internet, it must first find the remote IP-address. A DNS
client takes care of this. Once the IP-address is known, the application must know a gateway
address. This is normally a network router. If there is no gateway defined, a packet will be dropped.

The routing logic in the single driver is very simple. If the peer's IP-address is within the
network mask, packets will be sent directly. For instance, the laptop here above ( 192.168.2.5 )
can be reached directly.


### Multiple

More and more applications want to make use of more than one network interface. With multiple
interfaces this is possible.
Here below a configuration with 2 network interfaces:   
![](/media/2020/FreeRTOS_TCP_Single_Multi.5.png)

Now the FreeRTOS application is connected to a LAN (Interface 0) and also to a Wi-Fi station (Interface 1). 
It uses the addresses 192.168.2.100 (Interface 0, endpoint 0), fe80::7009 (Interface 0, endpoint 1), 
2406:7400:56:4914::100 (Interface 0, endpoint 2) and 10.2.0.45 (Interface 1, endpoint 3). These addresses 
can be configured either statically or automatically by the use of DHCP, or Router Advertisement ( “RA” ) 
in case of IPv6. The multiple end-points associated the LAN network interface allows us to have multiple 
IPv6 addresses (link local and global) that are required for IPv6 to work properly. 

IP-routing becomes a little more complex now. Suppose the application wants to send a UDP packet
to the IoT-thing. The library will try to find a matching network address:


| Endpoint | IP-address             | Network             | Mask          | Interface     | Gateway                  |
| -------- | ---------------------- | ------------------- | ------------- | ------------- | ------------------------ |
| 0        | 192.168.2.100          | 192.168.2.0         | 255.255.255.0 | LAN           | 192.168.2.1              |
| 1        | fe80::7009             | fe80::              | 64            | LAN (0)       |                          |
| 2        | 2406:7400:56:4914::100 | 2406:7400:56:4914:: | 10            | LAN (0)       | fe80::522b:73ff:feb4:a60 |
| 3        | 10.2.0.45              | 10.2.0.0            | 255.0.0.0     | Wi-Fi LTS (1) |                          |

The solution is easy: 10.2.0.45 matches with the network address 10.2.0.0, which is the Wi-Fi network.
No gateway is needed.

Now it wants to load a page from Google.com. DNS returns the address 64.233.167.113. This address does
not match with either the LAN or the Wi-Fi network address.
The library will iterate through the list of interfaces again and look for a Gateway. The first gateway
found will be used.


### Two networks, same network address

Some users on the FreeRTOS forum have asked if two networks may have the same network address.
The algorithm says that the first interface with a matching
network address shall be used. The same for an incoming TCP connection: the very first SYN
packet will set the MAC-address and the interface used. As for UDP packets: incoming packets
will be replied to through the interface that received the packet.


### Porting existing applications to FreeRTOS-Plus-TCP /multi:

Any existing application can easily be ported by defining `ipconfigCOMPATIBLE\_WITH\_SINGLE` in the
FreeRTOSIPConfig.h file. In that case, only one interface shall be linked to the project, and IPv6
shall be disabled.

When not using the compatible mode, each end-point must be initialised by the application: set the
default values, and indicate whether DHCP or Router Advertisement is desired.

In the earlier /single version, the device (as a whole) was said to be up or down. In the new
version, an end-point can become up or down. So earlier functions like FreeRTOS\_GetAddressConfiguration()
can not be used as is. A new parameter will be added: the end-point.

Lean and mean: while adding these new features, we have tried to keep both the code and the usage of
RAM as small as possible. It has no sophisticated indexed tables or complex routing rules.
For instance, it is assumed that there is only one gateway and one DNS address. If there is more than
one gateway or DNS address, the first one will be chosen.

The actual logic for TCP has not been changed. The windowing mechanism, the retransmissions, time-out,
all remain the same.


## Demo

The [how to setup and run a demo for multiple interfaces](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/03-IPv6-multi-functions) page
provides instructions on setting up multiple interfaces


## Multiple Interface functions

The [IPv6 and multiple interface functions](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/03-IPv6-multi-functions) page provides information on new functions
required to use both IPv6 and multiple interfaces.

