---
title: FreeRTOS-Plus-TCP 配置示例
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

配置 RTOS 的 TCP/IP 堆栈，以最小化 RAM 消耗或最大化吞吐量


[FreeRTOS-Plus-TCP 配置文件](TCP_IP_Configuration.md)
页面记录了每个 TCP/IP 堆栈的
配置选项。本页提供了关于如何设置
关键 TCP 参数的建议，以调整 TCP/IP 堆栈，从而最大限度地减少其 RAM 消耗，
最大限度地提高其吞吐量。请注意，最小化 RAM 消耗
和最大化吞吐量在某种程度上是两个相互排斥的目标——
一定程度上，分配给 TCP/IP 堆栈的 RAM 越多，
吞吐量就越大。

在所有情况下，可以使用网络驱动将 RAM 消耗和 CPU 负载降到最低，
因为网络驱动充分利用了所有[可用的硬件功能](TCP_IP_Configuration.md#hardware_specific_settings)，
例如校验和卸载以及 MAC 地址筛选。如果硬件
不具备这些功能，网络驱动程序仍可改善
RAM 消耗和 CPU 负载，方法是先执行任何可能的筛选，
之后再将数据包传递至 TCP/IP 堆栈。


### 最小化 RAM 消耗的 TCP/IP 堆栈配置

 如果您的 CPU 很小，RAM 小于 64KB，请勿使用滑动窗口：

```c
#define ipconfigUSE_TCP_WIN       0

```

窗口大小将固定为 1 [MSS](MSS.md)。
缓冲区大小可宣布为 1 或 2 MSS：

```c
#define ipconfigTCP_TX_BUFFER_LENGTH   ( 2 * ipconfigTCP_MSS )
#define ipconfigTCP_RX_BUFFER_LENGTH   ( 2 * ipconfigTCP_MSS )

```

如果 RAM 真受到限制，就使用较小的段：

```c

#define ipconfigNETWORK_MTU   576
#define ipconfigTCP_MSS       522

```

所有对等体都知道这一点，只会发送小数据包。

只分配您能接受的最小数量的网络缓冲区
描述符。这也有防止高网络流量
导致内存耗尽的作用，因为如果没有可用的描述符，
就不会分配网络缓冲区：

```c
#define ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS  [a small number]

```

最后，确保任何时候都只分配实际需要的 RAM 数量，
方法是使用 [BufferAllocation_2.c](Embedded_Ethernet_Buffer_Management.md)。
 
  
### 最大化吞吐量的 TCP/IP 堆栈配置

首先，请注意，网络驱动程序实现对于
可以获得的吞吐量至关重要。网络驱动程序应尽可能少地复制数据（不复制！），
使用 DMA，计算硬件中的校验和，充分利用硬件过滤，
在无法进行硬件过滤时使用软件过滤
（确保只将实际需要处理的数据包传递给
TCP/IP 堆栈）。

其次，TCP/IP 堆栈的高级功能，包括
[ipconfigUSE_LINKED_RX_MESSAGES](TCP_IP_Configuration.md#ipconfiguse_linked_rx_messages) 参数描述中提及的功能
和回调 API，其目的都是为了最大化吞吐量，
不过，这些功能被认为只适用于高级用户
。

如果您有足够的 RAM，则以下声明将有助于提高性能：

```c
#define ipconfigNETWORK_MTU           1526
#define ipconfigTCP_MSS               1460
#define ipconfigTCP_TX_BUFFER_LENGTH  ( 16 * ipconfigTCP_MSS )
#define ipconfigTCP_RX_BUFFER_LENGTH  ( 16 * ipconfigTCP_MSS )

```
在局域网中，滑动窗口的大小为 (8 * ipconfigTCP_MSS)，意味着
8 个数据包中只有一个会收到 ACK。

为了获得更大灵活性，FreeRTOS_setsockopt() 可以用于设置
正在创建的套接字和正在使用的相同套接字之间的大小。

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
  
Using FreeRTOS_setsockopt() to set TCP/IP options  

```

通常，将窗口设置为大于 (8 * MSS) 不会有什么好处，
除非 CPU 和 MAC 速度非常快，且连接到 1 Gbit 的局域网。
在终端速度较慢的情况下，使用较大的缓冲区进行接收是有意义的，
例如所有接收的数据都必须写入 SD 卡的情况。

最后，确保快速和确定的缓冲区分配，也可以
直接从 MAC 中断中使用，方法是使用 [BufferAllocation_1.c](Embedded_Ethernet_Buffer_Management.md)。

