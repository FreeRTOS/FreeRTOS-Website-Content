---
title: FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Using the FreeRTOS Windows Port


[[Buildable TCP/IP and FAT FS Examples](TCP_FAT_demo_projects)]


## Introduction

Two projects are provided that allow both FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT
to be built and executed using free tools and in a Windows environment, so without
the need to purchase any special hardware:

1. **FreeRTOS-Plus-TCP Starter Project**

   The FreeRTOS-Plus-TCP starter project only
   includes two of the [examples](#selecting-the-examples-to-run) listed at
   the bottom of this page. It does not include FreeRTOS-Plus-FAT,
   FreeRTOS-Plus-CLI, or any tracing capability.

2. **Comprehensive Project**

   The comprehensive project includes all the [examples](#selecting-the-examples-to-run)
   listed at the bottom of this page.  [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)
   provides the file storage for the FTP and HTTP
   examples, and [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
   provides the command line interface.

Both projects are preconfigured to build with the free version
of [Visual Studio C/C++](https://visualstudio.microsoft.com/vs/community/),
and use the [FreeRTOS Win32 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).


## Instructions

### Prerequisites

The following are required to build and run the Win32 RTOS port
examples:

* A windows host computer with a connected Ethernet network port (see the [hardware setup](#hardware-setup)
  section below). The projects have been tested with Windows XP, Windows 7 and Windows 10.

  If you do not have a wired Ethernet port then:

  + It may be possible to install a virtual network card, and then bridge the virtual network
    card to a Wi-Fi interface - if that works for you then please describe
    your configuration in [a support forum post](https://forums.freertos.org/)!

  + We have successfully used
    an [Ethernet to Wi-Fi bridge](https://www.amazon.com/Vonets-VAP11G-300-Wireless-Multi-Functional-Amplifier/dp/B014SK2H6W/ref=sr_1_1?keywords=VAP11G),
    although I'm afraid we cannot provide technical support for the use of such a device.

* An installed version of Visual Studio C/C++. The [free community edition](https://visualstudio.microsoft.com/vs/community/)
  is adequate. See the note at the top of the
  [page that described the FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
  regarding Visual Studio for C/C++ versions.

* An installed version of [WinPCap](https://www.winpcap.org/) (NPCap may also work). If
  you have Wireshark installed then this step might not be necessary.

* The [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) if you want to run the starter project, or the
  FreeRTOS Labs [source code download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)
  if you want to run the comprehensive project. **Note** the source code in the Labs download is much older
  and not recommended for production use.

* Finally, Although not strictly a prerequisite, it is also highly recommended to install a tool such
  as [Wireshark](https://www.wireshark.org/) so you can view network traffic.


### Hardware Setup

The Win32 example uses WinPCap to read and write raw Ethernet packets in
order to create a virtual node on the Ethernet network. The virtual node has its
own [MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing)
and [IP address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address). In the examples the host computer uses
its real MAC and IP addresses to communicate with the virtual MAC and
IP address as if they were two separate computers on the same network - whereas
in reality both nodes are running on the same host PC.

For this setup to work the host PC **must** be physically connected to a network,
even though no other nodes on the network are used, otherwise, as far as
Windows is concerned, the Ethernet port is disconnected and no communication can
take place. The network need not be a real network though - simply connecting the
host Windows machine to an MCU development board that has an Ethernet port is enough
provided Windows see the Ethernet as connected.

![TCP/IP in the RTOS simulator](/media/2018/Win32_network_environment.png)
*The real and virtual nodes are connected to the same network so can talk to each other*


### Opening a Project

It is necessary to open the project before completing the software setup.

1. **FreeRTOS-Plus-TCP Only Starter Project**

   The Visual Studio workspace for the FreeRTOS-Plus-TCP starter example is called FreeRTOS\_Plus\_TCP\_Minimal.sln,
   and is located in the FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_Minimal\_Windows\_Simulator
   directory of the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).

2. **Comprehensive Project**

   The Visual Studio workspace for the comprehensive example is called FreeRTOS\_Plus\_TCP\_and\_FAT.sln,
   and is located in the FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_and\_FAT\_Windows\_Simulator
   directory of the [FreeRTOS labs](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) download.


### Software Setup #1: Setting a Static or Dynamic IP Address

![Allocating an IP address to the RTOS node](/media/2018/Network_Address_Setup_In_FreeRTOSConfig.png)
*Network address settings in FreeRTOSConfig.h*

The [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
and [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) header files are the
FreeRTOS-Plus-TCP and FreeRTOS configuration files respectively. Both can be opened
from within Visual Studio.

If a [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) server
is present on the network to which the host computer is connected then
set [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) to 1 in FreeRTOSIPConfig.h, and no further IP address
configuration is necessary. It is not necessary to know the IP address
allocated to the demo by the DHCP server if a [hostname is configured](#software-setup-3-setting-the-hostname), because the demo can be
located by its name directly. The IP address can however be
viewed, as it is output using the [logging facility](#software-setup-4-print-and-logging-messages).

If there is no DHCP server connected to the network then set ipconfigUSE\_DHCP to
0 in FreeRTOSIPConfig.h, then configure the IP address and [netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
manually. The IP address and netmask are set using
the configIP\_ADDR0/3 and configNET\_MASK0/3 constants respectively in FreeRTOSConfig.h.
Note the IP address setting is in FreeRTOSConfig.h rather than
FreeRTOS**IP**Config.h because it is related to the application,
rather than being a TCP/IP stack configuration option.

When manually setting the IP address it is necessary to ensure the chosen
IP address is compatible with the netmask. In most cases
a compatible IP address will be one that uses the same first three octets
as the host computer. For example, if the IP address of the
host computer is 192.168.0.100 then
any 192.168.0.nnn address (other than when nnn is 0 or 255, and any other address
already present on the network) will be compatible.

It is also necessary to set a [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
address that is also compatible with
the netmask. This step is necessary even if the gateway does not actually
exist on the network (otherwise an internal sanity check will trigger a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
failure). The gateway address is set using the
configGATEWAY\_ADDR0/3 constants in FreeRTOSConfig.h.


### Software Setup #2: Selecting the (virtual) MAC Address

If only one computer that is running the example is connected to the network
then it will not be necessary to modify the [virtual] [MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing).

If multiple computers that are running the example are connected to the
same network then it will be necessary to ensure each computer has a
unique [virtual] MAC address.

The MAC address is set using the configMAC\_ADDR0/5 constants in
FreeRTOSConfig.h.


### Software Setup #3: Setting the Hostname

It is often more convenient to identify a node on the network using a
name, rather than an IP address. This is especially the case when the
IP address is not known. For example, rather than sending a ping
request to an IP address, such as "ping 192.168.0.200", a ping request
can instead be sent to a hostname, such as "ping MyHostName" (where
MyHostName is the name assigned to the network node).

If only one computer that is running the example is connected to the
network then it will not be necessary to modify the default hostname,
which is "RTOSDemo". If multiple computers that are running the example
are connected to the same network then it will be necessary to assign a
different hostname to each computer.

The hostname is set by the mainHOST\_NAME constant at the top of the
main.c source file.
Depending on the network topology, it may also be possible to use a second
hostname set by the mainDEVICE\_NICK\_NAME constant, which is also
defined at the top of main.c.


### Software Setup #4: Print and Logging Messages

![Directing RTOS debug output](/media/2018/Logging_Setup.png)
*Logging configuration in FreeRTOSIPConfig.h*

FreeRTOSIPConfig.h is provided with FreeRTOS\_debug\_printf() disabled,
and FreeRTOS\_printf() set to call a Windows simulator specific utility
file called vLoggingPrintf().

Log output can be sent to:

1. A UDP port:

   If mainLOG\_TO\_UDP is set to pdTRUE in main.c then log output will
   be sent using [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP).
   The UDP data will be sent to the IP address set by the configECHO\_SERVER\_ADDR0
   to configECHO\_SERVER\_ADDR3 constants defined in FreeRTOSConfig.h
   (which is the address of the echo server when the [echo server demo](TCP_Echo_Clients)
   example is used) and the [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number)
   set by the configPRINT\_PORT constant, also in FreeRTOSConfig.h.

2. A disk file:

   If mainLOG\_TO\_DISK\_FILE is set to pdTRUE in main.c then log output will be
   written to a file called RTOSDemo.log. When the file reaches
   40M bytes in size it is renamed RTOSDemo.ful, and a new log file
   is started.

3. Standard out:

   If mainLOG\_TO\_STDOUT is set to pdTRUE in main.c then log output will
   be sent to stdout.

**Note:** Output related Windows system calls should not be made from RTOS tasks.
Therefore standard out and disk file log data is passed to a standard
Windows thread for output. UDP logging is sent directly from the RTOS
task as it uses FreeRTOS-Plus-TCP, not the Windows TCP/IP stack.


### Software Setup #5: Selecting the Network Interface

Most computers have multiple network interfaces, and it is necessary to
tell the application which interface to use.

Compile (press F7 in Visual Studio) then run (press F5 in Visual Studio)
the application. A console screen will display the available network
interfaces. Set the configNETWORK\_INTERFACE\_TO\_USE constant in
FreeRTOSConfig.h to the number that appears next to the interface
being used. It will then be necessary to re-compile the program.

**Trouble shooting:**

* If the network interfaces are not displayed then it is
  likely Windows is not running the **NPF** service. To correct this
  type "sc start npf" into a command console (administrator privileges are
  required), then re-start the application.

* If you cannot establish communication, or if you cannot see
  any network traffic in [Wireshark](https://www.wireshark.org/), then try using a wired network
  rather than a wireless network. If that is not possible try
  connecting to (or pinging) the project from a different computer
  on the same network.

* Ensure your firewall or Windows settings are not blocking the
  network traffic.

![RTOS network interfaces](/media/2018/network_interface_in_command_console.png)
*The available network interfaces displayed when the example starts running*


## Running Examples

Now the hardware and software are configured the examples can be executed.


### Basic Connectivity Test

Before experimenting with the examples below it is advised to test basic
connectivity by starting the application running, then pinging the target.
If ping replies are received then the application is both running and
connected to the network correctly.

To ping the device, open a command prompt and type "ping aaa.bbb.ccc.ddd", where aaa.bbb.ccc.ddd is the IP address
displayed on the console when the network connected. Alternatively, if enabled in the configuration file,
type "ping RTOSDemo", assuming
the hostname has not be changed from the default of "RTOSDemo".

If a ping reply is not received then turn DHCP off, assign the target a
static IP address, and try again using the assigned IP address in place of the host
name.

Instructions describing how to set a static IP address, and how to set
a hostname, are provided in the setup instructions on this page.

![pinging the TCP target](/media/2018/pinging_the_target.png)
*Pinging the target, and receiving ping responses*


### Selecting the Examples to Run

The comprehensive projects contain multiple examples that can be selectively included
in the build using the #define constants at the top of
main.c. A description of each example, along with instructions
for including the example in the build, are provided on the links below.

All the examples are available for use in the comprehensive project. Only
the "Basic UDP clients communicating with basic UDP servers" and the
"TCP echo clients (Rx and Tx performed in the same RTOS task)" examples
are available for use in the simpler FreeRTOS-Plus-TCP starter project.

Available examples

* FreeRTOS-Plus-TCP UDP sockets examples

  1. [Command line interface using a UDP socket for input and output](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
  2. [Basic UDP clients communicating with basic UDP servers (standard and zero copy)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_client_server)
  3. [Using FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/using_select)
  4. [UDP echo clients](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Echo_Clients)

* FreeRTOS-Plus-TCP TCP sockets examples

  1. [Command line interface using a TCP socket for input and output](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/05-File-system-CLI)
  2. [TCP echo clients (Rx and Tx performed in the same RTOS task)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients)
  3. [TCP echo clients (Rx and Tx performed in separate RTOS tasks)](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients_Separate)
  4. [TCP echo server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Server)

* FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT web (HTTP) and FTP examples

  1. [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
  2. [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
