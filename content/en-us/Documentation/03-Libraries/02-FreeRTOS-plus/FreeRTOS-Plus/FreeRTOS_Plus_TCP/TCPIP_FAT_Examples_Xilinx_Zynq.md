---
title: FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Running on a Xilinx Zynq dual core ARM Cortex-A9 SoC

[[Buildable TCP/IP and FAT FS Examples](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_FAT_demo_projects)]


## Introduction

![](/media/2018/MicroZed.jpg)
*Don't have any hardware? You can still try the RTOS TCP and FAT examples
 now by using the [Win32 demo](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator), which uses free tools, and runs in a
Windows environment.*

The Zynq FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT demo includes the following standard examples:

* [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [TCP echo clients](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients)
* [TCP echo server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Server)
* [Command line interface using a UDP socket](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
* [UDP logging; sending FreeRTOS-Plus-TCP log output to a UDP port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Logging)

FreeRTOS-Plus-FAT is used to create and format a RAM disk, then mount both
the RAM disk and a FAT formatted SD card in the same virtual
file system. The mounted file systems then provide the storage for both
the FreeRTOS-Plus-TCP FTP and HTTP server examples.

The RAM disk is accessible
even if an SD card is not inserted.


The project builds using the free [Xilinx SDK](https://www.xilinx.com/products/design-tools/legacy-tools/sdk.html)
GCC based development tools, and hardware projects are
provided that allow the demo to run on either the [ZC702](http://www.xilinx.com/zc702) or lower
cost [MicroZed](https://www.avnet.com/wps/portal/us/products/avnet-boards/avnet-board-families/microzed/)
evaluation boards.

**Important Note:** Due to the combination of memory caching and DMA requiring 32-byte multiples, it is necessary
to use [BufferAllocation\_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)
with this demo.


## Instructions

### Prerequisites

The following are required to build and run the FreeRTOS-Plus-TCP and
FreeRTOS-Plus-FAT examples on a Xilinx Zynq SoC:

* Either a ZC702 or MicroZed evaluation board.

  [The FreeRTOS TCP/IP and FAT middleware components can also
  be evaluated using the
  the [FreeRTOS Windows port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
  without the need to purchase any special hardware]

* An installation of the Eclipse based Xilinx SDK development tools. The demo
  is always released with a project that is compatible with whatever
  is the latest SDK version at the time of release.

* The FreeRTOS Labs [source code download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).


### Hardware Setup

No specific hardware setup is required.


### Opening the Project

**Note: Previous FreeRTOS Labs releases required the end user to
create the BSP project - which can be done automatically by the
SDK. Now the BSP project is distributed along with the hardware
and application projects, so there is no need to create the BSP
as a separate step.**

The Eclipse project builds files from various directories within
the FreeRTOS-Labs source tree, so ensure the directory structure
has not been modified.

1. Start the SDK Eclipse IDE, selecting an existing Eclipse
   workspace or create a new workspace when prompted.

2. Select "Import" from the IDE's "File" menu. The Import dialogue
   will appear.

3. In the Import dialogue, select "General-\>Existing Projects Into Workspace",
   then navigate to and select the /FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_and\_FAT\_Zynq\_SDK
   directory within the FreeRTOS Labs source code directory tree.

4. Four projects will
   appear in the projects window of the Import dialogue, as shown
   below. Ensure the RTOSDemo and RTOSDemo\_bsp projects are selected,
   then also select either the MicroZed\_hw\_platform or the ZC702\_hw\_platform
   depending on the development board in use.

   Click the "Finish" button to close the Import dialogue.

   ![importing the RTOS TCP/IP and FAT projects](/media/2018/importing_the_zynq_tcpip_projects.png)
   *Importing the projects*

5. Right click the "RTOSDemo" project in the Project Explorer
   and select "Refresh" from the pop up menu.

   ![Creating the board support package for the Zynq TCP/IP example](/media/2018/projects_in_the_sdk_project_explorer_window.png)
   *The three projects in the Eclipse Project Explorer*

6. It should now be possible to build the project.

   Right click the "RTOSDemo" project in the Eclipse Project Explorer window
   once more. This time select "Build Project" from the pop-up
   menu.


### Software Setup #1: Setting a Static or Dynamic IP Address

![Allocating an IP address to the RTOS TCP/IP target](/media/2018/SDK_Network_Address_Setup_In_FreeRTOSConfig.png)
*Network address settings in FreeRTOSConfig.h*

The [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
and [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) header files are the
FreeRTOS-Plus-TCP and FreeRTOS configuration files respectively. Both can be opened
from within the SDK's Eclipse IDE.

If a [DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) server
is present on the network to which the Zynq is connected then
set [ipconfigUSE\_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) to 1 in FreeRTOSIPConfig.h, and no further IP address
configuration is necessary. It is not necessary to know the IP address
allocated to the Zynq by the DHCP server if a [hostname is configured](#software-setup-3-setting-the-hostname), because the Zynq can be
located by its name directly. The IP address can however be
viewed, as it is output using the [UDP logging facility](#software-setup-5-print-and-logging-messages).

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


### Software Setup #2: Setting the MAC Address

The MAC address is set using the configMAC\_ADDR0/5 constants in
FreeRTOSConfig.h.

If only one embedded target that is running the example is connected to the network
then it will not be necessary to modify the [MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/02-Ethernet-addressing).

If multiple embedded targets that are running FreeRTOS-Plus-TCP examples are connected to the
same network then it will be necessary to ensure each computer has a
unique MAC address.


### Software Setup #3: Setting the Hostname

It is often more convenient to identify a node on the network using a
name, rather than an IP address. This is especially the case when the
IP address is not known. For example, rather than sending a ping
request to an IP address, such as "ping 192.168.0.200", a ping request
can instead be sent to a hostname, such as "ping MyHostName" (where
MyHostName is the name assigned to the network node).

If only one embedded device that is running a FreeRTOS-Plus-TCP example is connected to the
network then it will not be necessary to modify the default hostname,
which is "RTOSDemo". If multiple embedded devices that are running the example
are connected to the same network then it will be necessary to assign a
different hostname to each embedded device.

The hostname is set by the mainHOST\_NAME constant at the top of the
main.c source file.
Depending on the network topology, it may also be possible to use a second
hostname set by the mainDEVICE\_NICK\_NAME constant, which is also
defined at the top of main.c.


### Software Setup #4: Setting the Echo Server Address

If the TCP echo client example is used then set the constants
configECHO\_SERVER\_ADDR0 to configECHO\_SERVER\_ADDR3
in FreeRTOSConfig.h to the IP address of a [suitable echo server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients).


### Software Setup #5: Print and Logging Messages

![Directing RTOS debug output](/media/2018/SDK_Logging_Setup.png)
*Logging configuration in FreeRTOSConfig.h*

FreeRTOSIPConfig.h is provided with [FreeRTOS\_debug\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
disabled, and [FreeRTOS\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
set to [send TCP/IP stack and application logging messages over UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Logging).
The IP address and port number
to which the UDP logging messages are sent, along with a few other
logging related parameters, are set using constants within FreeRTOSConfig.h,
which are shown in the image on the right.

Log messages are buffered for transmission by a low priority background
RTOS task.

Log output can be viewed in many different terminal programs.  [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm),
from Cinetix, it a convenient free standing utility that can be
used for this purpose.


## Running Examples

Now the hardware and software are configured the examples can be executed.
The instructions below describe how to download then execute the application
from RAM:

1. First it is necessary to create a debug configuration.

   Select "Debug Configurations..." from the IDE's "Run" menu. The
   Debug Configurations dialogue will appear.

2. Double click the "Xilinx C/C++ application (System Debugger)"
   option to create a new debug configuration.

3. Complete the new debug configuration's tabs as shown in the
   images below. The images assume the MicroZed hardware platform
   is being used.

   ![RTOS TCP/IP debug configuration 1](/media/2018/zynq_debug_configuration_1.png)

   ![RTOS TCP/IP debug configuration 1](/media/2018/zynq_debug_configuration_2.png)

4. Ensure the Zynq evaluation platform is connected to the host
   computer using an appropriate debug connection, then press
   the "Debug" button to close the Debug Configurations dialogue,
   download the application to RAM, and start a debug session.


### Basic Connectivity Test

Before experimenting with the examples below it is advised to test basic
connectivity by starting the application running, then pinging the target.
If ping replies are received then the application is both running and
connected to the network correctly.

To ping the device, open a command prompt and type "ping RTOSDemo", assuming
the hostname has not be changed from the default of RTOSDemo.

If a ping reply is not received then turn DHCP off, assign the target a
static IP address, and try again using the assigned IP address in place of the host
name.

Instructions describing how to set a static IP address, and how to set
a hostname, are provided in the setup instructions on this page.

![pinging the TCP target](/media/2018/pinging_the_target.png)
*Pinging the target, and receiving ping responses*


### Included Examples

The project includes the following examples:

* [Command line interface using a UDP socket](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_CLI)
* [FTP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/06-FTP-server)
* [HTTP web server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/11-Demos/07-HTTP-web-server)
* [TCP echo clients](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Clients)
* [TCP echo server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/TCP_Echo_Server)
* [UDP logging; sending FreeRTOS-Plus-TCP log output to a UDP port](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Logging)
