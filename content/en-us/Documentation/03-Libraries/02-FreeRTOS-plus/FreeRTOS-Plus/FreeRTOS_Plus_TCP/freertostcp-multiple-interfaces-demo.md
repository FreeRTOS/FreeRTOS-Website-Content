---
title: FreeRTOS-Plus-TCP Multiple Interface Demo Project
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


For the FreeRTOS Windows Simulator

This [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project is adding multiple interfaces and multiple
endpoint support to the currently single interface only FreeRTOS-Plus-TCP TCP/IP stack. While the resultant
multiple interface version is fully functional, it is still undergoing optimisation, test coverage and
documentation improvements, and memory safety checks. Until that work is complete the code is available
as a branch of the [FreeRTOS-Plus-TCP GitHub repo](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi).

---

## Source Code and Project Files

This demo application is available in the `labs/ipv6_multi` branch of
the [FreeRTOS-Plus-TCP](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) repository. It can be found in
the `demos/Multi\_interface\_demo` directory of the above repository.

This demo demonstrates the multiple interface (or rather the multiple endpoint) functionality of the
FreeRTOS-Plus-TCP IPv6 and multiple interface library.

When a device has multiple interfaces, a generated IP packet can be sent to any of those interfaces. But
choosing the correct one is important since the packet might not get through to the desired destination
in case of separated subnets. Additionally, sending the packet to all interfaces will only create unnecessary
network traffic.


The demo uses two different [classes](https://en.wikipedia.org/wiki/Classful_network) of IP addresses.
Since the Windows Simulator environment does not have multiple interfaces which can be used by FreeRTOS,
the demo is configured to use just one interface: Ethernet. The IP addresses can be changed according
to your needs by modifying the below macros:

In `FreeRTOSConfig.h`

```c
/* Default IP address configuration. Used in ipconfigUSE_DNS is set to 0, or
 * ipconfigUSE_DNS is set to 1 but a DNS server cannot be contacted. */
#define configIP1_ADDR0                      192
#define configIP1_ADDR1                      168
#define configIP1_ADDR2                      0
#define configIP1_ADDR3                      200
```

and in `main.c`

```c
/* Second set of IP address to be used by this demo. */
#define configIP2_ADDR0                 10
#define configIP2_ADDR1                 0
#define configIP2_ADDR2                 1
#define configIP2_ADDR3                 6
```

The demo shall attempt to ping the two different IP address present on different subnet masks which
are configured in `main.c` as shown below. Using a network analyser such as [Wireshark](https://www.wireshark.org/)
you should be able to see that the IP addresses used to ping the below IP address belong to the same
subnet. That is, `10.0.1.6` will be used to ping `10.0.1.10` and `192.168.0.200` will be used to ping `192.168.0.1`.

```c
#define democonfigCLASS_A_IP_ADDRESS  "10.0.1.10"    /* IP address of another
                                                        device on the network
                                                        with configured static
                                                        IP that can be pinged. */

#define democonfigCLASS_C_IP_ADDRESS  "192.168.0.1"  /* IP address of the router. */
```


## Target Hardware

The project uses the [FreeRTOS Windows simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).
The Windows simulator provides a convenient evaluation platform, but it
does not exhibit real time behavior. Simulated time is much slower than
real time.


## Compiler / Tool Chain

The project is pre-configured to build with
the [free Express edition of Microsoft Visual C++](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
(MSVC). MSVC Express Edition 2010 was used.


## Functionality

The demo includes the following standard demo configurations:

* Two sets of tasks which try to ping the class A and class C IP addresses as
  configured using the macros `democonfigCLASS_A_IP_ADDRESS`
  and `democonfigCLASS_C_IP_ADDRESS` as shown above.


## Build Instructions

1. Download the source code via cloning
   the "[labs/ipv6\_multi](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)"
   branch of the FreeRTOS-Plus-TCP repository.

2. Open the Visual Studio solution file Multi\_interface\_demo.sln
   from within the Visual Studio IDE. The solution file is located
   in the "demos/Multi\_interface\_demo" directory.

3. The demo uses WinPCap to create a virtual network connection by
   accessing raw Ethernet data on a real network connection - so can only work with wired network interfaces. Many
   computers have more than one real network interface. Set
   configNETWORK\_INTERFACE\_TO\_USE in FreeRTOSConfig.h. to tell the demo which real interface
   should be used to create the virtual interface.

   Available interface numbers are displayed on the console when the
   application is executed (See the image below).

   ![](/media/2020/Interfaces_displayed-lanczos3-1024x593.png)

4. You will need to configure another device to use a different class of IP address than
   the one your router uses. That is, if the router uses 192.x.x.x (Class C), then the
   other device should use 10.x.x.x (`democonfigCLASS_A_IP_ADDRESS`) and vice versa.

   **Using a PC**

   If you are using a PC as a second device, you need to go to "`Control Panel > Network and
   Sharing Center > Change adapter settings`". There you can see all the adapters your PC has.
   Choose the one which you want to use for this demo. Right click on it and choose "`Properties`".
   You will be shown a window as shown below.

   ![](/media/2020/Adapter_Properties.png)

   Select the "Internet Protocol Version 4 (TCP/IPv4)" and click on Properties. A new
   window should open. Make the changes so that it looks like the below image.

   ![](/media/2020/Static_IP_settings.jpg)

   **Note that the IP address shown in the image (and the one you put in the settings)
   should be same as democonfigCLASS\_A\_IP\_ADDRESS.**

5. The virtual interface has its own MAC address.
   Set the constants configMAC\_ADDR0 to configMAC\_ADDR5 to ensure
   the MAC address used by the virtual network connection is unique on the network. The constants
   are located at the bottom of FreeRTOSConfig.h.

6. IP address assignment is done statically in this case. It is not managed by a [DHCP server](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4).

   The IP address configured will be valid if the first three
   octets of the IP address match the first three octets of other
   IP addresses on the same network - each IP address must be unique
   on the network.

7. Select "Build Solution" from the IDE's Build menu (or press F7)
   to build the application.


## Debug Instructions

The standard Visual Studio
key used to start a debug session and break on entry to main() is F10.

The same host computer is used to build the application, debug the application,
and (because the Win32 simulator is used) run the application.
There are no special debugging instructions.
