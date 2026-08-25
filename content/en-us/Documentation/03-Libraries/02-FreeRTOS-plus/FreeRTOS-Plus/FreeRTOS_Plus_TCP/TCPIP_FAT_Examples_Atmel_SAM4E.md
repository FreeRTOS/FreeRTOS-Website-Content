---
title: FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Running on an Atmel SAM4E ARM Cortex-M4 microcontroller

[[Buildable TCP/IP and FAT FS Examples](TCP_FAT_demo_projects)]


## Introduction

![RTOS and TCP/IP running on SAM4E Xplained Pro](/media/2018/sam4e_xplained_pro.jpg)
*Don't have any hardware? You can still try the RTOS TCP and FAT examples
now by using the [Win32 demo](examples_FreeRTOS_simulator), which builds with free tools, and runs in a Windows environment.*

The Atmel SAM4E ARM Cortex-M4 TCP/IP and FAT demo includes the following standard examples:

* [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [TCP echo server](TCP_Echo_Server)
* [TCP echo clients](TCP_Echo_Clients)
* [Command line interface using a UDP socket](UDP_CLI)
* [UDP logging; sending FreeRTOS-Plus-TCP log output to a UDP port](UDP_Logging)

FreeRTOS-Plus-FAT is used to mount a FAT formatted SD card. The mounted file
system then provide the storage for both the HTTP and FTP server examples.

The project builds using the free [Atmel Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio)
GCC based development tools, and targets the
Atmel [SAM4E Xplained Pro](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=atsam4e-xpro)
evaluation kit.


## Instructions

### Hardware Setup

No specific hardware setup is required.


### Locating the Project

The Atmel Studio project that builds the demo described on this page
is located in the /FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_and\_FAT\_ATSAM4E
directory of the [FreeRTOS Labs download](/Documentation/03-Libraries/05-FreeRTOS-labs/RTOS_labs_download).


### Software Setup #1: Setting a Static or Dynamic IP Address

![Allocating an IP address to the RTOS TCP/IP target](/media/2018/Atmel_Studio_Network_Address_Setup_In_FreeRTOSConfig.png)
*Network address settings in FreeRTOSConfig.h*


The [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
and [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) header files are the
FreeRTOS-Plus-TCP and FreeRTOS configuration files respectively. Both can be opened
from within the Atmel Studio IDE.

If a [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) server
is used on the network to which the SAM4E is connected, then
set [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp)
to 1 in FreeRTOSIPConfig.h, and no further IP related network address
configuration is necessary. If a [hostname is configured](#software-setup-3-setting-the-hostname)
then it is not necessary to know the IP address assigned to the SAM4E by
the DHCP server because the SAM4E can be addressed directly by its hostname.
The IP address can however be
viewed, as it is printed out using the [UDP logging facility](#software-setup-5-print-and-logging-messages).

If there is no DHCP server connected to the network then set ipconfigUSE\_DHCP to
0 in FreeRTOSIPConfig.h, and instead configure the IP address and [netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
manually using the configIP\_ADDR0/3 and configNET\_MASK0/3 constants in FreeRTOSConfig.h.
Note the IP address constants are in FreeRTOSConfig.h, rather than
FreeRTOS**IP**Config.h, because they are related to the
application, and not the TCP/IP stack directly.

It is necessary to ensure a manually configured IP address is compatible with
the netmask. In most cases a compatible IP address will be one that uses
the same first three octets as the host computer. For example, if the
IP address of the host computer is 172.25.218.100, then
any 172.25.218.nnn address, other than when nnn is 0, 255, or
already present on the network, is compatible.

It is also necessary to set a [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
address that is correct for the network to which the SAM4E is being
connected, or at least compatible with the netmask if no gateway
exists. This step is necessary to prevent an internal sanity check triggering
a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
failure. The gateway address is set using the
configGATEWAY\_ADDR0/3 constants in FreeRTOSConfig.h.


### Software Setup #2: Setting the MAC Address

The MAC address is set using the configMAC\_ADDR0/5 constants in
FreeRTOSConfig.h.

If only one target that is running a FreeRTOS-Plus-TCP example is connected to the network
then it will not be necessary to modify the [MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing).

If multiple targets that are running FreeRTOS-Plus-TCP examples are connected to the
same network then it will be necessary to ensure each target has a
unique MAC address.


### Software Setup #3: Setting the Hostname

It is often more convenient to identify a node on the network using a
text name, rather than an IP address. This is especially the case when the
IP address is assigned by DHCP, and it therefore not known. For example,
rather than sending a ping request to an IP address, such as
"ping 172.25.218.200", a ping request can instead be sent to a hostname,
such as "ping MyHostName" (where "MyHostName" is the name assigned to
the network node).

If only one target that is running a FreeRTOS-Plus-TCP example is connected to the
network then it will not be necessary to modify the default hostname,
which is set to "RTOSDemo". If multiple targets that are running
FreeRTOS-Plus-TCP examples are connected to the same network then it will be
necessary to assign a different hostname to each target.

The hostname is set by the mainHOST\_NAME constant at the top of the
main.c source file.
Depending on the network topology, it may also be possible to use a second
hostname set by the mainDEVICE\_NICK\_NAME constant, which is also
defined at the top of main.c.


### Software Setup #4: Setting the Echo Server Address

If the TCP echo client example is used then set the constants
configECHO\_SERVER\_ADDR0 to configECHO\_SERVER\_ADDR3
in FreeRTOSConfig.h to the IP address of a [suitable echo server](TCP_Echo_Clients). FreeRTOS-Plus-TCP
will then send echo requests to,
and receive echo replies from, the configured echo server.


### Software Setup #5: Print and Logging Messages

![Directing RTOS TCP/IP stack debug output](/media/2018/Atmel_Studio_Logging_Setup.png)
*Logging configuration in FreeRTOSConfig.h*

In FreeRTOSIPConfig.h, [FreeRTOS\_debug\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
is disabled, and [FreeRTOS\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
is set to [send TCP/IP stack and application logging messages over UDP](UDP_Logging).
The IP address and port number
to which the UDP logging messages are sent, along with a few other
logging related parameters, are set using constants within FreeRTOSConfig.h,
which are shown in the image on the right.

Log messages are buffered for transmission by a low priority background
RTOS task.

Log output can be viewed in many different terminal programs,
including [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm),
from Cinetix.


### Software Setup #6: Hardware Specific Settings

The project is delivered pre-configured to execute on a SAM4E Xplained Pro
evaluation board. It may be necessary to update the IO configure to use
the demo on different hardware, or update the network driver if a different
PHY is used.


## Running Examples

The instructions below describe how to build, download then execute the
application on a SAM4E Xplained Pro evaluation board:

1. Follow the software configuration steps detailed above.

2. If available, insert a clean FAT formatted SD card into the
   SAM4E Xplained Pro's SD card socket.

3. Inspect the comments at the top of main.c, and set the constants
   that build individual examples into and out of the demo.

   Note: If an SD card is not being used then do not include the
   HTTP or FTP server examples.

4. Ensure the SAM4E Xpalained Pro hardware is connected to the host
   computer (the computer running Atmel Studio) using the target's
   debug USB port, and a suitable network using an Ethernet cable.

5. First press F7 to build the project, and then press F5 to
   program the target flash memory, and start the application
   executing

**LED0 will toggle every half second when the application is executing.**


### Basic Connectivity Test

It is advised to test basic connectivity before experimenting with the
examples linked below. This can be done by pinging the target.
If ping replies are received, then the application is both running and
connected to the network correctly.

To ping the device, open a command prompt and type "ping ",
where  is the name assigned to the target - which by default
will be "RTOSDemo".

If a ping reply is not received then turn DHCP off, assign the target a
static IP address, and try again using the assigned IP address in place of the host
name.

Instructions describing how to set a static IP address, and how to set
a hostname, are provided in the setup instructions on this page.


![pinging the TCP target](/media/2018/pinging_the_target.png)
*Pinging the target, and receiving ping responses*


### Included Examples

The project includes the following examples:

* [Command line interface using a UDP socket](UDP_CLI)
* [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [TCP echo clients](TCP_Echo_Clients)
* [TCP echo server](TCP_Echo_Server)
* [UDP logging; sending FreeRTOS-Plus-TCP log output to a UDP port](UDP_Logging)
