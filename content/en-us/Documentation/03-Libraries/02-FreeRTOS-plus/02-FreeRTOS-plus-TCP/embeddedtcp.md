---
title: FreeRTOS-Plus-TCP Demo Project
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

For Windows Simulator

---

## Source Code and Project Files

This demo application is available in the `FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator`
directory of the official [FreeRTOS zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) and on
the [FreeRTOS\_Plus\_TCP\_Minimal\_Windows\_Simulator](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_Minimal_Windows_Simulator)
repository on GitHub.


## Target Hardware

The project uses the [FreeRTOS Windows simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).
The Windows simulator provides a convenient evaluation platform, but it does not exhibit real time behavior.
Simulated time is much slower than real time.


## Compiler / Tool Chain

The project is pre-configured to build with
the [free Express edition of Microsoft Visual C++](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
(MSVC). MSVC Express Edition 2010 was used.


## Functionality

The demo includes the following standard demo configurations:

* Two sets of UDP client and server tasks, where the client task sends
  data to the server task. One set of tasks uses the standard sockets
  interface. The other set of tasks uses the zero copy sockets interface.

The project can optionally be built to also include:


* A simple TCP echo client task, where the task sends data to a server
  (address configured using configECHO\_SERVER\_ADDR[0-3] and echoECHO\_PORT)
  and waits for the echo reply. The reply is checked for correctness.

* A simple TCP echo server task, where the task waits for incoming connections
  using [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen).
  When a connection is made and data is received, the task responds backs with
  the same data.


## Build Instructions

1. Download the source code via the [FreeRTOS downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) that contains the source code and project
   files. Extract the zip file into a convenient location, ensuring
   the directory structure is maintained.

2. Open the Visual Studio solution file FreeRTOS\_Plus\_TCP\_Minimal.sln
   from within the Visual Studio IDE. The solution file is located
   in the "FreeRTOS-Plus/Demo/FreeRTOS\_Plus\_TCP\_Minimal\_Windows\_Simulator"
   directory.

3. The demo uses WinPCap to create a virtual network connection by
   accessing raw Ethernet data on a real network connection. Many
   computers have more than one real network port. Set
   configNETWORK\_INTERFACE\_TO\_USE in FreeRTOSConfig.h. to tell the demo which real port
   should be used to create the virtual port.

   Available port numbers are displayed on the console when the
   application is executed (see the image in the Usage Instructions
   section below).

4. Follow the instructions provided on the
   [Echo Client example documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_Echo_Clients)
   to set up an echo server and set the address of the echo server
   in FreeRTOSConfig.h. Alternatively, a TCP echo server and/or
   client can be set up by setting the macros mainCREATE\_TCP\_ECHO\_TASKS\_SINGLE
   and mainCREATE\_TCP\_ECHO\_SERVER\_TASK to 1.

5. The virtual port has its own MAC address.
   Set the constants configMAC\_ADDR0 to configMAC\_ADDR5 to ensure
   the MAC address used by the virtual network connection is unique on the network. The constants
   are located at the bottom of FreeRTOSConfig.h.

6. If the IP address assignment is managed by a
   [DHCP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4)
   then no further configuration is required.

   If IP address assignment is not managed by a DHCP server then set
   ipconfigUSE\_DHCP to 0 in [FreeRTOS**IP**Config.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration),
   then edit the constants at the bottom of FreeRTOSConfig.h that
   set the default values for a static IP address, DNS server address,
   gateway address and netmask to ensure they are valid for the
   Ethernet network. The IP address will be valid if the first three
   octets of the IP address match the first three octets of other
   IP addresses on the same network - each IP address must be unique
   on the network.

7. Select "Build Solution" from the IDE's Build menu (or press F7)
   to build the application.


## Debug Instructions

The standard Visual Studio key used to start a debug session and break on entry to main() is F10.

The same host computer is used to build the application, debug the application,
and (because the Win32 simulator is used) run the application.
There are no special debugging instructions.


## Usage Instructions

* The following constants are defined in main.c to allow tasks to be included or excluded from the build:


```c
/* Set the following constants to 1 or 0 to define which tasks to include and
exclude. */
#define mainCREATE_SIMPLE_UDP_CLIENT_SERVER_TASKS     1
#define mainCREATE_TCP_ECHO_TASKS_SINGLE              0
#define mainCREATE_TCP_ECHO_SERVER_TASK               0
```


## Old Demos with Other Open Source TCP/IP Stacks


Read further for additional information on  [legacy TCP/IP demos.](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/legacy-demo-projects)
