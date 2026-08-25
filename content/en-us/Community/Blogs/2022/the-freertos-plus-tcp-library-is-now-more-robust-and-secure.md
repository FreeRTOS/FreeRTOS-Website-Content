---
title: The FreeRTOS-Plus-TCP library is now more robust and secure
date: 9 Aug 2022
feature: blog
categories:
  - Long term support
authors: 
  - wallit
---
While we work on the [FreeRTOS Labs IPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/02-IPv6-functionality) project, 
we are continuing to improve the robustness, security, and modularity of 
the [FreeRTOS-Plus-TCP](https://github.com/freertos/freertos-plus-tcp) library. To that end, today, we 
are excited to release the FreeRTOS-Plus-TCP V3.0.0 library.

FreeRTOS-Plus-TCP V3.0.0 adds comprehensive unit test coverage for all lines and branches of code, and 
has undergone penetration testing and protocol testing by AWS Security to reduce the exposure to security 
vulnerabilities. For context, protocol testing involves compliance and impairment checks for IPv4, TCP, 
UDP, DHCP, ARP and ICMP, which helps ensure the FreeRTOS-Plus-TCP TCP/IP stack is more robust.
The source code has also been restructured to make it more modular, extensible, and easier to add unit tests.

The new source code organization requires existing projects to be updated. However, if you want to continue 
using your existing source code organization, you can use a script to generate the older file and directory 
structure. To learn more and download the latest library, visit 
the [FreeRTOS-Plus-TCP GitHub repository](https://github.com/freertos/freertos-plus-tcp).

  
## About the author

![](https://secure.gravatar.com/avatar/fb75dac2926bf515a691ef90995a1554?s=200&d=mm&r=g)   
Toshiyanger Walling is a Software Development Manager on the FreeRTOS team at Amazon Web Services where 
he manages a team responsible for building and sustaining FreeRTOS software.   
[View articles by this author](../author/wallit) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
