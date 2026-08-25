---
title: FreeRTOS-Plus-TCP Configuration Examples
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Configuring the RTOS's TCP/IP stack to either minimise RAM consumption or maximise throughput


The [FreeRTOS-Plus-TCP configuration file](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
page documents each TCP/IP stack
configuration option. This page provides suggestions on how to set key
TCP parameters to tailor the TCP/IP stack to minimise its RAM consumption,
and then to maximise its throughput. Note that minimising RAM consumption
and maximising throughput are somewhat mutually exclusive objectives -
up to a point the more RAM that is allocated to the TCP/IP stack the
higher the throughput will be.

In all cases RAM consumption and CPU load can be minimised by using
network drivers that make full use of any [hardware features available](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#hardware_specific_settings),
such as checksum offloading and MAC address filtering. If the hardware
does not offer these facilities then the network driver can still improve
RAM consumption and CPU load by performing any filtering it can before
passing packets to the TCP/IP stack.


### TCP/IP Stack Configuration To Minimise RAM Consumption

 If you have a tiny CPU with less than 64KB of RAM, do not use sliding Windows:

```c
#define ipconfigUSE_TCP_WIN       0
```

The window size will be fixed to 1 [MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/11-MSS).
The buffer size can be declared as 1 or 2 MSS:

```c
#define ipconfigTCP_TX_BUFFER_LENGTH   ( 2 * ipconfigTCP_MSS )
#define ipconfigTCP_RX_BUFFER_LENGTH   ( 2 * ipconfigTCP_MSS )
```

If RAM is really constrained then use smaller segments:

```c

#define ipconfigNETWORK_MTU   576
#define ipconfigTCP_MSS       522
```

All peers will understand this and only send small packets.

Only allocate the minimum number of network buffer descriptors you can get
away with. This also has the effect of preventing high network traffic
resulting in memory exhaustion as network buffers will not be allocated if
no descriptors are available:

```c
#define ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS  [a small number]
```

Finally, ensure only the amount of RAM that is actually required is allocated
at any given time by using the [BufferAllocation\_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management).


### TCP/IP Stack Configuration to Maximise Throughput

First - note that network driver implementation is crucial in the throughput
that can be obtained. Network drivers should copy as little data as possible (none!),
use DMAs, calculate checksums in hardware, make full use of hardware filtering,
and make use of software filtering where hardware filtering is not possible
(to ensure only packets that actually require processing are passed to the
TCP/IP stack).

Second the advanced features of the TCP/IP stack, including the functionality
mentioned in the description of the [ipconfigUSE\_LINKED\_RX\_MESSAGES](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_linked_rx_messages)
parameter and the callback API are provided with the aim of maximising
throughput - however these features are considered to be for advanced users
only.

If you have enough RAM then the following declarations will help performance:

```c
#define ipconfigNETWORK_MTU           1526
#define ipconfigTCP_MSS               1460
#define ipconfigTCP_TX_BUFFER_LENGTH  ( 16 * ipconfigTCP_MSS )
#define ipconfigTCP_RX_BUFFER_LENGTH  ( 16 * ipconfigTCP_MSS )
```
On a LAN, the sliding windows will get a size of ( 8 * ipconfigTCP\_MSS ), meaning
that only one out of 8 packets will receive an ACK.

For more flexibility FreeRTOS\_setsockopt() can be used to set sizes between
a socket being created and the same socket getting used.

```c
    /* Declare the variable used to set the configuration parameters. */
    WinProperties_t xWinProps;

    /* Start with everything set to 0. */
    memset( &xWinProps, '�', sizeof( xWinProps ) );

    /* Configure as required. */
    xWinProps.ulTxBufSize = 24 * ipconfigTCP_MSS;
    xWinProps.ulTxWinSize = 8;
    xWinProps.ulRxBufSize = 24 * ipconfigTCP_MSS;
    xWinProps.ulRxWinSize = 8;

    /* Set the socket options. */
    FreeRTOS_setsockopt( sock,
                         0,
                         FREERTOS_SO_WIN_PROPERTIES,
                         ( void * ) &xWinProps,
                         sizeof( xWinProps ) );
```
*Using FreeRTOS_setsockopt() to set TCP/IP options*

Usually nothing is to be gained by setting the windows larger than ( 8 * MSS ),
unless the CPU and MAC are very fast and connected to a 1 Gbit LAN.
Using larger buffers for reception does make sense in case the end-point is slow,
for instance if all the received data must be written to an SD-card.

Finally, ensure fast and deterministic buffer allocation that can also be
used directly from within the MAC interrupt by using [BufferAllocation\_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management).
