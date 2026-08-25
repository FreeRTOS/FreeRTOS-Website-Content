---
title: IPv6 Demo Project
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


For the FreeRTOS Windows Simulator

This [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project is adding [IPv6](https://en.wikipedia.org/wiki/IPv6)
functionality to the currently IPv4 only FreeRTOS-Plus-TCP TCP/IP stack. While the resultant dual IPv4 / IPv6 version
is fully functional, it is still undergoing optimisation, test coverage and documentation improvements, and memory
safety checks. Until that work is complete the code is available as a branch of
the [FreeRTOS-Plus-TCP GitHub repo](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi).


## Source Code and Project Files

This demo application is available in
the [labs/ipv6\_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi) branch of
the [FreeRTOS-Plus-TCP](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) repository. It can be found in
the `demos/IPv6_Multi_WinSim_demo` directory of the above repository.

This demo demonstrates several protocols ( UDP, TCP, ICMP/ping, NTP ) of the FreeRTOS-Plus-TCP IPv6 and multiple interface library. It will use both IPv6 and IPv4 for each of the protocols mentioned.

The FreeRTOS-Plus-TCP Multiple Interface Visual Studio project file is in the following
directory: demos/IPv6\_Multi\_WinSim\_demo.
In the .props file, you will find several macros that indicate the location of source files:

- $(FREERTOS\_SOURCE\_DIR) The kernel sources

- $(FREERTOS\_INCLUDE\_DIR) The kernel header files

- $(DEMO\_COMMON\_SOURCE\_DIR) The location of the common directory of the demos

- $(PLUS\_TCP\_SOURCE\_DIR) The FreeRTOS-Plus-TCP source files

- $(PLUS\_TCP\_INCLUDE\_DIR) The FreeRTOS-Plus-TCP header files

- $(UTILITIES\_SOURCE\_DIR) The location of the tcp\_utilities directory

You can changes these macros to let the project work with a different
source tree.


## Target Hardware

The project uses
the [FreeRTOS-Plus-TCP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
FreeRTOS Windows simulator. The Windows simulator provides a convenient evaluation platform, but it
does not exhibit real time behavior. Simulated time is much slower than real time.


## Compiler / Tool Chain

The project is pre-configured to build with
the [free Express edition of Microsoft Visual C++](https://visualstudio.microsoft.com/) (MSVC). MSVC Express
Edition 2010 was used.


## Functionality

The IPv6\_Multi\_WinSim\_demo demo performs some basic network activities:

- ARP address resolution for IPv4 addresses on the LAN

- Neighbour Discovery for IPv6 addresses on the LAN

- Looking up a IPv4 or IPv6 address using DNS, either asynchronous or synchronous.

- Looking up a local host ( IPv4/6 ) using LLMNR ( not considered safe anymore )

- Talk with an NTP server and fetch the time using UDP, with IPv4/6

- Download a file from any public server using TCP/HTTP

- Ping any server on the web or on the LAN, , with IPv4 or IPv6

The demo can be easily adapted to your own needs. It works like a command line interface ( CLI ) that performs the above tasks.

Here are some examples:

```
	http4 google.co.uk /index.html
	http6 amazon.com /index.html
	ping4 10.0.1.10
	ping6 2001:470:ec54::
	dnsq4 yahoo.com
	ntp6a 2.europe.pool.ntp.org
```

The last line will first lookup the mentioned NTP server, send a request, and wait for a reply. The
time will be printed in the logging.

Although it is called a CLI, the demo does not have a STDIN. The commands are hard-coded in main.c

The keywords can have some single-letter suffices: 4 or 6 ( for IPv4/6 ), “a” to do an asynchronous
DNS lookup, and “c” to clear all caches before starting the task.


## Build Instructions

1. Download the source code via cloning
   the [labs/ipv6\_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi) branch of
   the FreeRTOS-Plus-TCP repository.

2. Open the Visual Studio solution file `FreeRTOS_Plus_TCP_IPv6_Multi.sln` from within the Visual Studio
   IDE. The solution file is located in the “demos/IPv6\_Multi\_WinSim\_demo” directory.

3. The demo uses WinPCap to create a virtual network connection by accessing raw Ethernet data on a real
   network connection – and thus can only work with wired network interfaces. Many computers have more
   than one real network interface. Set configNETWORK\_INTERFACE\_TO\_USE in FreeRTOSConfig.h. to tell
   the demo which real interface should be used to create the virtual interface. Available interface numbers
   are displayed on the console when the application is executed.

4. The virtual interface has its own MAC address. Set the constants configMAC\_ADDR0 to configMAC\_ADDR5
   to ensure the MAC address used by the virtual network connection is unique on the network. The constants
   are located at the bottom of FreeRTOSConfig.h.

5. IP address assignment is done statically in this case. It is not managed by a [DHCP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4).
   The IP address configured will be valid if the first three octets of the IP address match the first three
   octets of other IP addresses on the same network – each IP address must be unique on the network.

6. Select “Build Solution” from the IDE’s Build menu (or press F7) to build the application.


## Debug Instructions

The standard Visual Studio key used to start a debug session, and break on entry to main() is F10.
The same host computer is used to build the application, debug the application, and (because the Win32
simulator is used) run the application. There are no special debugging instructions.
