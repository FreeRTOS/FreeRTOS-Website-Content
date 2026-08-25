---
title: FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Running on an ST STM32F407 ARM Cortex-M4 microcontroller

[[Buildable TCP/IP and FAT FS Examples](TCP_FAT_demo_projects)]


## Introduction

![RTOS and TCP/IP running on STM3240G-EVAL](/media/2018/stm3240g-eval.jpg)
*Don't have any hardware? You can still try the RTOS TCP and FAT examples
now by using the [Win32 demo](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator), which uses free tools, and runs in a Windows environment.*

**Note 1:** In order to demonstrate FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT being
used in a RAM constrained system the project described on this page
only uses the STM32's 192K bytes of internal RAM. The external RAM on
the STM3240G-EVAL development board is not used.

**Note 2:** The demo presented on this page can be built using the
free Lite version
of [Atollic's TrueStudio IDE](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html),
as even the free version does not have a code size limit.

The ST STM32F407 ARM Cortex-M4 TCP/IP and FAT demo includes the following standard examples:

* [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [TCP echo server](TCP_Echo_Server)
* [TCP echo clients](TCP_Echo_Clients)
* [Command line interface using a UDP socket](UDP_CLI)
* [UDP logging; sending FreeRTOS-Plus-TCP log output to a UDP port](UDP_Logging)

FreeRTOS-Plus-FAT is used to mount a FAT formatted SD card. The mounted file
system then serves the files for both the HTTP and FTP server examples.

The project builds using the free edition of the

[Atollic TrueStudio](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html)
GCC based development tools (which don't have a code size limit), and targets the
ST [STM3240G-EVAL](http://www.st.com/web/en/catalog/tools/FM116/SC959/SS1532/PF252216?sc=stm3240g-eval)
evaluation board.


## Instructions

### Hardware Setup

No specific hardware setup is required.


### Locating the Project

The Atollic TrueStudio project that builds the demo described on this page
is located in the /FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_and\_FAT\_STM32F4xxx
directory of the [FreeRTOS Labs download](/Documentation/03-Libraries/05-FreeRTOS-labs/RTOS_labs_download).

**NOTE**: The ST STM32F407 ARM Cortex-M4 TCP/IP and FAT demo project is provided in the download is
for community interest and to serve as a reference. It is fully functional, but may not comply with
our production code standards.


### Software Setup #1: Setting a Static or Dynamic IP Address

![Allocating an IP address to the free RTOS TCP/IP target](/media/2018/STM3240G-EVAL_Network_Address_Setup_In_FreeRTOSConfig.png)
*Network address settings in FreeRTOSConfig.h*


The [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
and [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) header files are the
FreeRTOS-Plus-TCP and FreeRTOS configuration files respectively. Both can be opened
from within the TrueStudio Eclipse based IDE.

If a [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) server
is in use, then
set [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp)
to 1 in FreeRTOSIPConfig.h, and no further IP related network address
configuration is necessary. If a [hostname](#software-setup-3-setting-the-hostname) is
provided for the STM32 target then it is not necessary to know the IP
address assigned to the STM32 by the DHCP server, because the STM32 can
be located using the assigned name. The IP address can however be
viewed, as it is printed out using the [UDP logging facility](#software-setup-5-print-and-logging-messages).

If a DHCP server is not in use then set ipconfigUSE\_DHCP to
0 in FreeRTOSIPConfig.h, and configure a static IP address and [netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/07-Subnet)
using the configIP\_ADDR0/3 and configNET\_MASK0/3 constants located in
FreeRTOSConfig.h.
Note the IP address constants are in FreeRTOSConfig.h, rather than
FreeRTOS**IP**Config.h, because they are related to the
application, and not the TCP/IP stack directly.

It is necessary to ensure any manually configured IP address is compatible with
the netmask used by the network to which the STM32 is being connected.
In most cases a compatible IP address will be one that uses
the same first three octets as the host computer. For example, if the
IP address of the host computer is 172.25.218.100, then
any 172.25.218.nnn address, other than where nnn is 0, 255, or
already present on the network, is valid.

It is also necessary to set a [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router)
address that is correct for the network to which the STM32 is being
connected, or at least compatible with the configured netmask if no gateway
exists. This step is necessary to prevent an internal sanity check triggering
a [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
failure due to a mismatched gateway address and netmask. The gateway
address is set using the configGATEWAY\_ADDR0/3 constants in FreeRTOSConfig.h.


### Software Setup #2: Setting the MAC Address

If only one embedded target that is running a FreeRTOS-Plus-TCP example is connected to the network
then it will not be necessary to modify the [MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing).

If multiple embedded targets that are running FreeRTOS-Plus-TCP examples are connected to the
same network then it will be necessary to ensure the MAC address assigned
to each embedded target is unique.

The MAC address is set using the configMAC\_ADDR0/5 constants in
FreeRTOSConfig.h.


### Software Setup #3: Setting the Hostname

It is more convenient to identify a network node using a
human readable text name than an IP address. This is especially the case when the
IP address is assigned by a DHCP server, and it therefore not necessarily
known, and liable to be changed. For example,
rather than sending a ping request to an IP address, such as
"ping 172.25.218.200", a ping request can instead be sent to a hostname,
such as "ping MyHostName" (where "MyHostName" is the name assigned to
the network node).

If only one embedded target that is running a FreeRTOS-Plus-TCP example is connected to the
network then it will not be necessary to modify the default hostname,
which is "RTOSDemo". If multiple embedded targets that are running
FreeRTOS-Plus-TCP examples are connected to the same network then it will be
necessary to ensure the hostname assigned to each embedded target is unique.

The hostname is set by the mainHOST\_NAME constant, which is located near
the top of the main.c source file.
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

![Directing RTOS TCP/IP stack debug output](/media/2018/TrueStudio_Logging_Setup.png)
*Logging configuration in FreeRTOSConfig.h*

As delivered, [FreeRTOS\_debug\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
is not used, and [FreeRTOS\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
is set to [send TCP/IP stack and application logging messages to a UDP port](UDP_Logging).
The IP address and port number
to which the UDP logging messages are sent, along with a few other
logging related parameters, are set using constants within FreeRTOSConfig.h,
as shown in the image on the right.

Log messages are buffered for transmission by a low priority background
RTOS task.

Log output can be viewed in many different terminal programs, including
UDPTerm, from Cinetix.


### Software Setup #6: Hardware Specific Settings

The project is delivered pre-configured to execute on an STM32F40G-EVAL
evaluation board. To execute the demo on different hardware:

* Update HAL\_ETH\_MspInit(), which is the ST HAL driver callback
  function, to ensure it correctly configures the IO for your
  hardware. HAL\_ETH\_MspInit() is implemented near the bottom of
  main.c.

* Set the configSD\_DETECT\_GPIO\_PORT and configSD\_DETECT\_PIN settings
  in FreeRTOSConfig.h to the GPIO port and pin used to detect if
  an SD card is present.

* It may be necessary to update the network driver if a different
  PHY is used.


## Running Examples

The instructions below describe how to build, download, then execute the
application on a STM3240G-EVAL evaluation board:

1. Follow the software configuration steps detailed above.

2. If available, insert a clean FAT formatted SD card into the
   STM32F407G-EVAL SD card socket.

3. Inspect the comments at the top of main.c, and set the constants
   that build individual examples into and out of the demo as
   required.

   Note: If an SD card is not being used then do not include the
   HTTP or FTP server examples.

4. Ensure the STM3240G-EVAL hardware is connected to the host
   computer (the computer running Atollic TrueStudio) using a suitable
   debug connection (such as ST Link, or J-Link) and connected to
   a network using an Ethernet cable.

5. Select "Import" from the TrueStudio IDE's "File" menu. The dialogue box shown below
   will appear. Select "Existing Projects into Workspace".

   ![Importing the STM32 TrueStudio project into the Eclipse workspace](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)
   *The dialogue box that appears when "Import" is first clicked*

6. In the next dialogue box, select /FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_and\_FAT\_STM32F4xxx
   as the root directory. Then, make sure the RTOSDemo
   project is checked in the "Projects" area, and that the Copy Projects Into
   Workspace box is not checked, before clicking
   the Finish button (see the image below for the correct check box states,
   the finish button is not visible in the image).

   ![Selecting the RTOS STM32 project to import into Eclipse](/media/2018/Import_RTOS_Atollic.png)
   *Make sure that RTOSDemo is checked, and "Copy projects into workspace" is not checked*

7. Select "Build All" from the TrueStudio IDE's "Project" menu to create
   the executable image.

8. Select "Debug" from the TrueStudio IDE's "Run" menu to create
   a debug configuration, which can then be used to program the
   STM32 flash memory and start a debug session.

**Green LED 1 will toggle when the application is executing.** The LED is
toggled from the Idle task, so the toggle rate will not necessarily
be constant.


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
