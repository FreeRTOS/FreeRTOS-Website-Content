---
title: 将 FreeRTOS-Plus-UDP 移植到不同的微控制器
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

![](/media/2019/warning_icon.png)
自 FreeRTOS V10.1.0 开始，FreeRTOS+UDP 已从 FreeRTOS 内核下载包中移除。请参阅
[FreeRTOS+TCP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，此堆栈只能配置用于 UDP 作为替代方案
。

### 引言

 网络接口的实现，特别是以太网
 MAC 驱动程序的实现，
 对使用嵌入式 TCP/IP 堆栈时可实现的数据吞吐量至关重要。为获得高吞吐量，
 MAC 驱动程序必须有效利用 DMA 并
 尽可能避免复制数据。可以通过
 FreeRTOS-Plus-TCP 对 UDP 数据包进行端到端零拷贝；另外，也可以通过高级接口
 对 TCP 数据包进行零拷贝。还有一些高级选项
 可以在数据包被发送到嵌入式
 TCP/IP 堆栈前对其进行过滤，而且还可以一次性地将接连收到的数据包
 发送到嵌入式 TCP/IP 堆栈， 无需一个个单独发送。

 但实际上，需要最大化吞吐量的应用程序并不多，
 尤其是在小型 MCU 上，实现者可能会
 选择牺牲吞吐量以提升简洁性。

 本页面介绍了如何连接 FreeRTOS-Plus-TCP 和网络驱动程序，
 并提供了一个简要示例，其中包含简单
 且[更快](#适用于零拷贝移植层的-pfinitialise-实现示例)（但更复杂）的
 接口。**参考这些示例非常重要，因为
 它们演示了数据
 传输后如何释放网络缓冲区。**

 随 FreeRTOS-Plus-TCP 一起提供的网络驱动程序移植层位于
 FreeRTOS-Plus-TCP/source/portable/NetworkInterface 目录下
 （此为 FreeRTOS-Plus-TCP 下载文件中的目录）。但请注意，这些驱动程序
 是为测试嵌入式 TCP/IP 堆栈而创建的，并非
 用于表示优化过的示例。

### 要点总结

![将免费的 TCP IP 堆栈移植到其他 MCU](/media/2018/network_interface.png)

**网络接口移植层位于 IP 堆栈和嵌入式以太网硬件驱动程序之间** 

* FreeRTOS-Plus-TCP 移植的目标 MCU 都要具备以太网
 MAC 驱动程序。这里假定该驱动程序已经存在并且
 可以运行。
* 通过提供“网络接口移植层” 将 FreeRTOS-Plus-TCP 移植到新的硬件上，
 该层提供
 TCP/IP 堆栈和以太网 MAC 驱动程序之间的接口。请参见
 右图。
* 网络接口移植层必须提供名为 
 [`px[port_name]_FillInterfaceDescriptor()`](#pxport_name_fillinterfacedescriptor) 的函数， 
 用于初始化“网络接口移植层”实例。

	+ 如果 FreeRTOS+TCP 库构建时 
	 启用了 [ipconfigIPv4_BACKWARD_COMPATIBLE](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigIPv4_BACKWARD_COMPATIBLE)， 
	 网络接口移植层还必须提供函数 `pxFillInterfaceDescriptor`。
* 网络接口移植层必须提供一个 
 [pfInitialise()](#pfinitialise) 
 名为 pfInitialise() 的回调函数，用于初始化“网络接口移植层”实例。
* 网络接口移植层必须提供一个 
 [pfOutput()](#pfoutput) 
 名为 pfOutput() 的回调函数，用于将从嵌入式 TCP/IP 堆栈中收到的数据发送到以太网 MAC 驱动程序， 
 以便在“网络接口移植层”实例中进行传输。
* 网络接口移植层必须将
 从以太网 MAC 驱动程序中收到的数据包发送至 TCP/IP 堆栈，发送方法是调用
 [xSendEventStructToIPTask()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/08-xSendEventStructToIPTask)。
* 只有将 [BufferAllocation_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management) 用于缓冲区分配时，网络
 接口移植层才必须静态分配[网络缓冲区](#网络缓冲区和网络缓冲区描述符)并
 提供一个函数。
 [vNetworkInterfaceAllocateRAMToBuffers()](#vnetworkinterfaceallocateramtobuffers仅当使用-bufferallocation_1c-时)
 调用此函数是用于将静态分配的网络缓冲区分配给网络
 缓冲区描述符。
* 网络缓冲区（存储实际数据的缓冲区）
 的引用通过使用
 [NetworkBufferDescriptor_t](#网络缓冲区和网络缓冲区描述符)
 结构体得以实现。
* 嵌入式 TCP/IP 堆栈提供了一组
 [移植实用程序函数](#由-tcpip-堆栈提供给移植层使用的函数)
 使得移植层可以执行获取、
 释放网络缓冲区等操作。

 本页面详细介绍了上述步骤的具体操作过程，并提供了两个
 示例。[第一个示例演示了](#2-基础网络接口移植层示例)
 如何实现简单（但更慢的）驱动程序。而
 [第二个示例](#适用于零拷贝移植层的-pfinitialise-实现示例)
 则演示了如何实现更复杂（也更快）的驱动程序。
 **参考这些示例非常重要，因为
 它们演示了数据
 传输后如何释放网络缓冲区。**

---

网络缓冲区和网络缓冲区描述符
----------------------------------------------

 以太网（或其他网络）帧存储在网络缓冲器中。网络缓冲区描述符
 （NetworkBufferDescriptor_t 类型的变量）用于描述网络
 缓冲区，并在 TCP/IP 堆栈和网络
 驱动程序之间传递网络缓冲区。

![嵌入式网络缓冲区](/media/2018/Ethernet_buffer.png)

**pucEthernetBuffer 指向网络缓冲区的起点。

 xDataLength 保存缓冲区的大小（以字节为单位），不包括以太网 CRC 字节。** 

 仅需访问以下两个 NetworkBufferDescriptor_t 结构体成员
 ：

1. uint8_t *pucEthernetBuffer;

 pucEthernetBuffer 指向网络缓冲区的起点。
2. size_t xDataLength

 xDataLength 保持 pucEthernetBuffer 所指向的网络缓冲区的大小。
 此缓冲区大小以字节为单位，但其长度不包括
 含有以太网帧 CRC 字段的字节。

[pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer)
 仅用于获取网络缓冲区本身，且通常仅
 在零拷贝驱动程序中使用。

[pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor)
 用于同时获取网络缓冲区**和**网络缓冲区
 描述符。

必须由移植层实现的函数
----------------------------------------------------

### px[port_name]_FillInterfaceDescriptor()

#### （例如：pxSAM_FillInterfaceDescriptor）

px[port_name]_FillInterfaceDescriptor()
 必须初始化“网络接口移植层”实例。下面是该实例的数据结构体。

```c

typedef struct xNetworkInterface  

{
   const char * pcName;  

   void * pvArgument;  

   NetworkInterfaceInitialiseFunction_t pfInitialise;  

   NetworkInterfaceOutputFunction_t pfOutput;  

   GetPhyLinkStatusFunction_t pfGetPhyLinkStatus;  

   struct  

   { 
      uint32_t  

         bInterfaceUp : 1,  

         bCallDownEvent : 1;  
   } bits;  

   struct xNetworkEndPoint * pxEndPoint;  

   struct xNetworkInterface * pxNext;  

} NetworkInterface_t;  

```

* pcName 用于调试目的，通常是网络接口的唯一名称。
* pvArgument 是传递给访问函数的实参。
* pfInitialize 是初始化 MAC 驱动程序的回调函数。
* pfOutput 是一个回调函数，用于将从嵌入式 TCP/IP 堆栈中收到的数据发送到以太网 MAC 驱动程序以进行传输。
* pfGetPhyLinkStatus 为用户提供了获取接口状态的查询函数。
* bits 包含 bInterfaceUp 和 bCallDownEvent ，分别表示接口是否处于上行和下行状态 
 。
* pxEndPoint 是绑定到此接口的端点列表。
* pxNext 是链表结构体中的下一个接口实例。

### pxFillInterfaceDescriptor()

 当 [ipconfigIPv4_BACKWARD_COMPATIBLE](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigIPv4_BACKWARD_COMPATIBLE)
 启用后，函数 FreeRTOS_IPInit() 将调用 pxFillInterfaceDescriptor 以初始化接口描述符。想要 
 实现此函数，只需调用 
 [`px[port_name]_FillInterfaceDescriptor()`](#pxport_name_fillinterfacedescriptor)，因为两者功能相同。

### pfInitialise()

pfInitialise() 是“网络接口移植层”实例中的回调函数， 
 它必须让以太网 MAC 做好发送和接收数据的准备。大多数情况下，这只需调用 
 以太网 MAC 外设驱动程序中提供的初始化函数——这将确保 
 MAC 硬件已启用，且时钟已设置，并配置 MAC 外设的 DMA 描述符。

pfInitialise() 将网络接口作为参数。如果初始化成功，则返回 pdPASS； 
 如果初始化失败，则返回 pdFAIL 。

```c

typedef BaseType_t ( * NetworkInterfaceInitialiseFunction_t ) ( struct xNetworkInterface * pxDescriptor );  

```

pfInitialise() 函数原型

### pfOutput()

**每当网络缓冲区做好传输准备时，TCP/IP 堆栈就会调用 pfOutput()。**  

使用函数的 pxDescriptor 参数，将传输缓冲区的描述信息传入函数。 
如果 xReleaseAfterSend 不等于 pdFALSE， 
则在不再需要缓冲区和缓冲区的描述符时，驱动程序代码必须将它们释放（返回）给嵌入式 TCP/IP 堆栈。如果 
xReleaseAfterSend 为 pdFALSE，则网络缓冲区和缓冲区的描述符 
将由 TCP/IP 堆栈本身释放（在这种情况下，驱动程序不需要释放它们）。

请注意，此时 pfOutput() 返回的值将被忽略。嵌入式 TCP/IP 堆栈 
不会为同一个网络缓冲区调用 pfOutput() 两次，即使第一次调用 pfOutput() 后 
无法将网络缓冲区发送到网络上。  

下文列出了基本示例和更高级的示例，而且 FreeRTOS-Plus-TCP/source/portable/NetworkInterface 
目录（位于 FreeRTOS-Plus-TCP 下载文件中）包含可以参考的示例。但请注意， 
下载文件中的示例可能未经过优化。

```c

typedef BaseType_t ( * NetworkInterfaceOutputFunction_t ) ( struct xNetworkInterface * pxDescriptor,  
                                                            NetworkBufferDescriptor_t * const pxNetworkBuffer,  
                                                            BaseType_t xReleaseAfterSend );         

```

pfOutput() 函数原型

vNetworkInterfaceAllocateRAMToBuffers() 
仅当使用 BufferAllocation_1.c 时
--------------------------------------------------------------------------------

[BufferAllocation_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)
 使用预分配网络缓冲区，这些缓冲区通常
 在编译时被静态分配。

 必须分配的网络缓冲区数目由
 [ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfignum_network_buffer_descriptors)
 定义（在 FreeRTOSIPConfig.h 中）设置，并且每个缓冲区的大小必须为
 ( ipTOTAL_ETHERNET_FRAME_SIZE + ipBUFFER_PADDING )。ipTOTAL_ETHERNET_FRAME_SIZE
 根据
 [ipconfigNETWORK_MTU](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigNETWORK_MTU) 的数值自动计算，
 而 ipBUFFER_PADDING 则是根据
 [ipconfigBUFFER_PADDING](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigBUFFER_PADDING) 自动计算。

 联网硬件会对
 分配的缓冲区提出严格的对齐要求，因此建议
 在嵌入式以太网驱动程序中分配缓冲区——这样，缓冲区的对齐方式
 总是能满足硬件的要求。

 虽然嵌入式 TCP/IP 堆栈会分配网络缓冲区描述符，
 但它对网络缓冲区本身的对齐方式一无所知。
 因此，嵌入式以太网驱动程序还必须提供
 名为 vNetworkInterfaceAllocateRAMToBuffers() 的函数，
 为每个描述符分配一个静态声明的缓冲区。请注意，缓冲区开头的 ipBUFFER_PADDING
 字节留给嵌入式 TCP/IP
 堆栈使用。请参见下文示例。

```c

void vNetworkInterfaceAllocateRAMToBuffers(  
       NetworkBufferDescriptor_t xDescriptors[ ipconfigNUM_NETWORK_BUFFERS ] );  

```

vNetworkInterfaceAllocateRAMToBuffers() 函数原型

```c

/* First statically allocate the buffers, ensuring an additional ipBUFFER_PADDING  
bytes are allocated to each buffer.  This example makes no effort to align  
the start of the buffers, but most hardware will have an alignment requirement.  
If an alignment is required then the size of each buffer must be adjusted to  
ensure it also ends on an alignment boundary.  Below shows an example assuming  
the buffers must also end on an 8-byte boundary. */  

#define BUFFER_SIZE ( ipTOTAL_ETHERNET_FRAME_SIZE + ipBUFFER_PADDING )  
#define BUFFER_SIZE_ROUNDED_UP ( ( BUFFER_SIZE + 7 ) & ~0x07UL )  

static uint8_t ucBuffers[ ipconfigNUM_NETWORK_BUFFERS ][ BUFFER_SIZE_ROUNDED_UP ];  

/* Next provide the vNetworkInterfaceAllocateRAMToBuffers() function, which  
simply fills in the pucEthernetBuffer member of each descriptor. */  

void vNetworkInterfaceAllocateRAMToBuffers(  
    NetworkBufferDescriptor_t pxNetworkBuffers[ ipconfigNUM_NETWORK_BUFFERS ] )  
{  
    BaseType_t x;  

    for( x = 0; x < ipconfigNUM_NETWORK_BUFFERS; x++ )  
    {
        /* pucEthernetBuffer is set to point ipBUFFER_PADDING bytes in from the  
        beginning of the allocated buffer. */  

        pxNetworkBuffers[ x ].pucEthernetBuffer = &( ucBuffers[ x ][ ipBUFFER_PADDING ] );  

        /* The following line is also required, but will not be required in  
        future versions. */  
        *( ( uint32_t * ) &ucBuffers[ x ][ 0 ] ) = ( uint32_t ) &( pxNetworkBuffers[ x ] );  
    }  

}  

```

VNetworkBufferInterfaceAllocateRAMToBuffers() 实现示例。

由 TCP/IP 堆栈提供给移植层使用的函数
----------------------------------------------------------------

 移植层可使用以下函数：
 * [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor) -

 获取网络缓冲区和用于描述此网络缓冲区的描述符
 。此函数还可用来获取
 网络缓冲区描述符——这在实现
 零拷贝驱动程序时很有用。
* [vReleaseNetworkBufferAndDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/04-vReleaseNetworkBufferAndDescriptor) -

 释放（返回至嵌入式 TCP/IP 堆栈）网络缓冲区描述符，
 和此描述符所引用的网络缓冲区（如果有的话）。
* 使用了 pxNetworkBufferGetFromISR() - not available when [BufferAllocation_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)

* 使用了 vNetworkBufferReleaseFromISR() - not available when [BufferAllocation_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)

* [eConsiderFrameForProcessing()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/07-eConsiderFrameForProcessing)：
 用于确定从网络上接收到的数据是否需要传递至嵌入式
 TCP/IP 堆栈。理想情况下，
 可在网络中断时调用此函数，
 以尽早丢弃接收到的数据包。

* [xSendEventStructToIPTask()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/08-xSendEventStructToIPTask) -
 xSendEventStructToIPTask() 是嵌入式 TCP/IP
 堆栈所使用的函数，以将各种事件发送至 RTOS
 任务（此任务正在运行嵌入式 TCP/IP 堆栈）。移植层使用此函数和
 eNetworkRxEvent 事件以将接收到的数据传递到堆栈进行处理。

* [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer) -
 只获取网络缓冲区，不获取网络缓冲区描述符。
 此函数通常仅在零拷贝接口中使用，
 以将缓冲区分配给 DMA 描述符。

* [vReleaseNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/06-vReleaseNetworkBuffer) -
 仅释放（返回至嵌入式 TCP/IP 堆栈）网络缓冲区
 ——不释放网络缓冲区描述符。此函数
 通常仅在零拷贝接口中使用（在这些接口，网络缓冲区会被分配给
 DMA 描述符）。

* [FreeRTOS_AddNetworkInterface()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/02-FreeRTOS_AddNetworkInterface) -
 将网络接口的当前实例添加到 TCP/IP 堆栈的链表中。

* [FreeRTOS_FirstEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/09-FreeRTOS_FirstEndPoint) -
 用于获取 TCP/IP 堆栈中存储的第一个端点。移植层通常使用 
 此函数来获取 TCP/IP 堆栈中存储的所有 MAC 地址， 
 然后设置硬件以允许针对这些地址的数据包。

* [FreeRTOS_NextEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/11-FreeRTOS_NextEndPoint) -
 用于获取 TCP/IP 堆栈中存储的下一个端点。移植层通常使用 
 此函数来获取 TCP/IP 堆栈中存储的所有 MAC 地址， 
 然后设置硬件以允许针对这些地址的数据包。

* [FreeRTOS_MatchingEndpoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/10-FreeRTOS_MatchingEndpoint) -
 为传入的以太网数据包查找最佳端点。移植层必须在 
 将网络缓冲区描述符发送到 TCP/IP 堆栈之前正确设置端点。

### 接收数据

 以太网 MAC 驱动程序会将接收到的以太网帧放入缓冲区。
 移植层必须：

1. 确定是否需要将接收到的数据发送至嵌入式
 TCP/IP 堆栈。理想情况下，这将在接收中断中完成，
 以尽早丢弃不必要的数据包
 。
2. 分配网络缓冲区描述符。
3. 设置所分配的描述符的 xDataLength 和 pucEthernetBuffer
 成员（请参见本页后文中的基础示例和零拷贝示例）
 。
4. 调用 xSendEventStructToIPTask() 以将网络缓冲区
 描述符发送到嵌入式 TCP/IP 堆栈进行处理
 （请参见本页后文的基础示例和零拷贝示例）
 。

```c
typedef struct IP_TASK_COMMANDS  
{
    /* Specifies the type of event being sent to the RTOS task and must be set to  
    eNetworkRxEvent to signify a receive event. */  

    eIPEvent_t eEventType;  

    /* Points to additional data about the event.  In this case set pvData to the  
    the address of the network buffer descriptor. */  
    void *pvData;  
} IPStackEvent_t;  

```

IPStackEvent_t 类型

```c
/* The timeout is specified in RTOS ticks.  Returns pdTRUE if the message was  
sent successfully, otherwise return pdFALSE. */  
BaseType_t xSendEventStructToIPTask( const IPStackEvent_t *pxEvent, TickType_t xTimeout )  
```

xSendEventStructToIPTask() 函数原型

 下文将提供基础示例和高级示例教程。由
 FreeRTOS-Plus-TCP 自带的网络驱动程序移植层（不一定经过
 优化）位于 FreeRTOS-Plus-TCP/source/portable/NetworkInterface
 目录中。

网络接口移植层示例
-------------------------------------

#### 1\. px[port_name]_FillInterfaceDescriptor() 作为接口移植层中公共部分的示例。

 每个网络接口都必须提供一个函数来初始化其实例，该函数称为 
 [`px[port_name]_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#pxport_name_FillInterfaceDescriptor)。 
 该函数将初始化实例结构体中的回调函数， 
 并通过调用 
 [FreeRTOS_AddNetworkInterface()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/02-FreeRTOS_AddNetworkInterface) 将实例附加到链接的列表中。

 **px[port_name]_FillInterfaceDescriptor() 的实现示例**（以 SAM 驱动程序为例）

```c
NetworkInterface_t * pxSAM_FillInterfaceDescriptor( BaseType_t xEMACIndex,  
                                                    NetworkInterface_t * pxInterface )
{  

    pxInterface->pcName = "InterfaceName";  

    pxInterface->pvArgument = ( void * ) xEMACIndex;  

    pxInterface->pfInitialise = prvSAM_NetworkInterfaceInitialise; /* The initialisation function of this driver. */  

    pxInterface->pfOutput = prvSAM_NetworkInterfaceOutput; /* The output function of this driver. */  

    pxInterface->pfGetPhyLinkStatus = prvSAM_GetPhyLinkStatus; /* The query status function of this driver. */  

    FreeRTOS_AddNetworkInterface( pxInterface );  

    return pxInterface;
}  

```

**pxFillInterfaceDescriptor() 的实现示例**（以 SAM 驱动程序为例）

```c

#if ( ipconfigIPv4_BACKWARD_COMPATIBLE == 1 )  
    NetworkInterface_t * pxFillInterfaceDescriptor( BaseType_t xEMACIndex,  
                                                    NetworkInterface_t * pxInterface )  
    {  
        return pxSAM_FillInterfaceDescriptor( xEMACIndex, pxInterface );  
    }  
#endif  

```

### 2\. 基础网络接口移植层示例

 简单的网络接口可通过复制以太网帧
 （位于由以太网 MAC 驱动程序库分配的缓冲区和由移植层分配的缓冲区之间）
 创建。[此外提供了更高效的零拷贝
 替代方案
 [在简单示例之后](#适用于零拷贝移植层的-pfinitialise-实现示例)。] 
#### 适用于基础移植层的 pfInitialise() 实现示例

```c

static BaseType_t prvSAM_NetworkInterfaceInitialise( NetworkInterface_t * pxInterface )  

{  
    BaseType_t xReturn;  

    /*  
     * Perform the hardware specific network initialisation here.  Typically  
     * that will involve using the Ethernet driver library to initialise the  
     * Ethernet (or other network) hardware, initialise DMA descriptors, and  
     * perform a PHY auto-negotiation to obtain a network link.  
     *  
     * This example assumes InitialiseNetwork() is an Ethernet peripheral driver  
     * library function that returns 0 if the initialisation fails.  
     */  

    if( InitialiseNetwork() == 0 )  
    {  
        xReturn = pdFAIL;  
    }  
    else  
    {  
        /* Set the MAC addresses by calling FreeRTOS_FirstEndPoint() and  
         * FreeRTOS_NextEndPoint(). Make sure that all MAC addresses in  
         * all end-points are set to the hardware (if necessary). */  
        if( SetMACAddress() == 0 )  
        {  
            xReturn = pdFAIL;  
        }  
        else  
        {  
            xReturn = pdPASS;  
        }  
    }  
    return xReturn;  
}  
```

pfInitialise() 是针对特定硬件的，因此本示例只描述需要完成的操作，而不显示任何细节

#### 适用于基础移植层的 pfOutput() 实现示例

```c
static BaseType_t prvSAM_NetworkInterfaceOutput( NetworkInterface_t * pxInterface,  
                                                 NetworkBufferDescriptor_t * const pxDescriptor,  
                                                 BaseType_t xReleaseAfterSend )  
{  
    /* Simple network interfaces (as opposed to more efficient zero copy network  
       interfaces) just use Ethernet peripheral driver library functions to copy  
       data from the FreeRTOS-Plus-TCP buffer into the peripheral driver's own buffer.  
       This example assumes SendData() is a peripheral driver library function that  
       takes a pointer to the start of the data to be sent and the length of the  
       data to be sent as two separate parameters.  The start of the data is located  
       by pxDescriptor->pucEthernetBuffer.  The length of the data is located  
       by pxDescriptor->xDataLength. */  
    SendData( pxDescriptor->pucBuffer, pxDescriptor->xDataLength );  

    /* Call the standard trace macro to log the send event. */  

    iptraceNETWORK_INTERFACE_TRANSMIT();  

    if( xReleaseAfterSend != pdFALSE )  
    {  
        /* It is assumed SendData() copies the data out of the FreeRTOS-Plus-TCP Ethernet  
           buffer.  The Ethernet buffer is therefore no longer needed, and must be  
           freed for re-use. */  
        vReleaseNetworkBufferAndDescriptor( pxDescriptor );  
    }  

    return pdTRUE;  
}  
```

适用于简单（而非零拷贝）网络接口实现的 pfOutput() 实现示例

#### 将接收到的数据传递到基础移植层中的 TCP/IP 示例

 接收到来自以太网（或其他网络）驱动程序的数据包后，
 移植层必须使用 [NetworkBufferDescriptor_t](#网络缓冲区和网络缓冲区描述符)
 结构体描述此数据包，然后调用
 [xSendEventStructToIPTask()](#接收数据)
 以发送 NetworkBufferDescriptor_t 结构体至嵌入式 TCP/IP 堆栈。

**注 1：** 如果使用了 [BufferAllocation_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)，
 那么网络缓冲区
 描述符和以太网缓冲区不能从
 中断服务程序 (ISR) 内部分配。在这种情况下，以太网 MAC
 接收中断可以[将接收
 处理延迟到任务](../../deferred_interrupt_processing)。下文将展示这一情况
 。

**注 2 ：**可以采用许多先进技术
 尽可能减少从移植层发送至嵌入式
 TCP/IP 堆栈的数据量。例如，可以调用 [eConsiderFrameForProcessing()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/07-eConsiderFrameForProcessing)
 来确定已接收的以太网帧是否需要
 发送至嵌入式 TCP/IP 堆栈，以及接连收到的以太网帧
 是否可以一次性发送至嵌入式 TCP/IP 堆栈
 。详情请参见
 [硬件和驱动程序特定设置](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#hardware_specific_settings)
 部分（位于 FreeRTOS-Plus-TCP 配置页面）。

**注 3：**切记通过调用 
 [FreeRTOS_MatchingEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/10-FreeRTOS_MatchingEndpoint) 
 在向 TCP/IP 堆栈发送数据包和描述符之前正确设置 pxEndPoint。

```c

/* The deferred interrupt handler is a standard RTOS task.  FreeRTOS's   
   [centralised deferred interrupt handling](/Documentation/02-Kernel/02-Kernel-features/11-Deferred-interrupt-handling) capabilities can also be used. */  

static void prvEMACDeferredInterruptHandlerTask( void *pvParameters )  
{  
    NetworkBufferDescriptor_t *pxBufferDescriptor;  
    size_t xBytesReceived;  

    /* Used to indicate that xSendEventStructToIPTask() is being called because  
       of an Ethernet receive event. */  

    [IPStackEvent_t](#接收数据) xRxEvent;  

    for( ;; )  
    {  
        /* Wait for the Ethernet MAC interrupt to indicate that another packet  
           has been received.  The task notification is used in a similar way to a  
           counting semaphore to count Rx events, but is a lot more efficient than  
           a semaphore. */  

        [ulTaskNotifyTake](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)( pdFALSE, portMAX_DELAY );  

        /* See how much data was received.  Here it is assumed ReceiveSize() is  
           a peripheral driver function that returns the number of bytes in the  
           received Ethernet frame. */  

        xBytesReceived = ReceiveSize();  

        if( xBytesReceived > 0 )  
        {  

            /* Allocate a network buffer descriptor that points to a buffer  
               large enough to hold the received frame.  As this is the simple  
               rather than efficient example the received data will just be copied  
               into this buffer. */  

            pxBufferDescriptor = [pxGetNetworkBufferWithDescriptor](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor)( xBytesReceived, 0 );  

            if( pxBufferDescriptor != NULL )  

            {  
                /* pxBufferDescriptor->pucEthernetBuffer now points to an Ethernet  
                   buffer large enough to hold the received data.  Copy the  
                   received data into pcNetworkBuffer->pucEthernetBuffer.  Here it  
                   is assumed ReceiveData() is a peripheral driver function that  
                   copies the received data into a buffer passed in as the function's  
                   parameter.  **Remember!** While is is a simple robust technique -  
                   it is not efficient.  An example that uses a zero copy technique  
                   is provided further down this page. */  

                ReceiveData( pxBufferDescriptor->pucEthernetBuffer );  

                pxBufferDescriptor->xDataLength = xBytesReceived;  

                /* See if the data contained in the received Ethernet frame needs  
                   to be processed.  **NOTE!** It is preferable to do this in  
                   the interrupt service routine itself, which would remove the need  
                   to unblock this task for packets that don't need processing. */  

                if( eConsiderFrameForProcessing( pxBufferDescriptor->pucEthernetBuffer )  
                                                                      == eProcessBuffer )  
                {  
                    pxBufferDescriptor->pxEndPoint = FreeRTOS_MatchingEndpoint( pxMyInterface, pxBufferDescriptor->pucEthernetBuffer );  

                    if( pxBufferDescriptor->pxEndPoint != NULL )  
                    {  
                        /* The event about to be sent to the TCP/IP is an Rx event. */  

                        xRxEvent.eEventType = eNetworkRxEvent;  

                        /* pvData is used to point to the network buffer descriptor that  
                           now references the received data. */  

                        xRxEvent.pvData = ( void * ) pxBufferDescriptor;  

                        /* Send the data to the TCP/IP stack. */  

                        if( xSendEventStructToIPTask( &xRxEvent, 0 ) == pdFALSE )  
                        {  

                            /* The buffer could not be sent to the IP task so the buffer  
                               must be released. */  

                            vReleaseNetworkBufferAndDescriptor( pxBufferDescriptor );  

                            /* Make a call to the standard trace macro to log the  
                               occurrence. */  

                            iptraceETHERNET_RX_EVENT_LOST();  
                        }  
                        else  
                        {  
                            /* The message was successfully sent to the TCP/IP stack.  
                               Call the standard trace macro to log the occurrence. */  

                            iptraceNETWORK_INTERFACE_RECEIVE();  
                        }  
                    }  
                    else  
                    {  
                        /* The Ethernet frame can be dropped, but the Ethernet buffer  
                           must be released. */  

                        vReleaseNetworkBufferAndDescriptor( pxBufferDescriptor );  
                    }  
                }  
                else  
                {  
                    /* The Ethernet frame can be dropped, but the Ethernet buffer  
                       must be released. */  

                    vReleaseNetworkBufferAndDescriptor( pxBufferDescriptor );  
                }  
            }  
            else  
            {  
                /* The event was lost because a network buffer was not available.  
                   Call the standard trace macro to log the occurrence. */  

                iptraceETHERNET_RX_EVENT_LOST();  
            }  
        }  
    }  
}  
```

简单的（并非高效的零拷贝）接收处理程序示例

### 3\. 更高效的网络接口移植层示例

 查看本节内容前，请先查阅
 上节有关如何创建简单的网络接口移植层的内容。

 简单的网络接口在
 TCP/IP 堆栈使用、管理的缓冲区和以太网（或其他网络）
 MAC 驱动程序使用、管理的缓冲区之间复制以太网帧。在上述
 缓冲区之间复制数据使得驱动程序实现变得简单，但效率低下。

 零拷贝网络接口不在上述缓冲区之间复制数据，而是在
 TCP/IP 堆栈和以太网 MAC 驱动程序之间将引用传递给缓冲区
 。

 零拷贝接口更复杂，并且很少能在不
 编辑以太网 MAC 驱动程序的情况下被创建。

 如要使用零拷贝进行传送，则必须
 将 [ipconfigZERO_COPY_TX_DRIVER](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigZERO_COPY_TX_DRIVER) 设置为 1。

 大多数以太网硬件都使用 DMA （直接内存访问）
 在以太网硬件和预分配 RAM 缓冲区之间移动帧。通常
 可使用一组 DMA
 描述符引用预分配内存缓冲区。DMA 描述符通常是链式的——每个描述符
 都指向链中的下一个描述符，链中最后一个描述符则指向
 第一个描述符。

![链式嵌入式以太网缓冲区](/media/2018/Network_DMA_Descriptors.png)

 链式 DMA 描述符

#### 适用于零拷贝移植层的 pfInitialise() 实现示例

pfInitialise() 必须使用
 [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer)
 来获取接收 DMA 描述符所指向的指针。不必为
 传输 DMA 描述符而分配任何缓冲区——
 当有数据可发送时，可（通过引用）将其传入缓冲区
 。

![零拷贝以太网驱动程序初始化](/media/2018/Zero_copy_DMA_initialisation.png)

 初始化 DMA Rx 描述符以指向由
 pucGetNetworkBuffer() 分配的缓冲区。

 初始化之后，DMA Tx 描述符不指向任何缓冲区
 。

#### 适用于零拷贝层的 pfOutput() 实现示例

pfOutput() 不会将传输中的帧复制到由
 MAC 驱动程序托管的缓冲区中（它做不到，因为
 DMA Tx 描述符不指向任何缓冲区），而是会
 更新下一个 DMA Tx 描述符，使此描述符指向已包含数据的缓冲区
 。

**注意：**以太网缓冲区内的数据被传输后，必须释放此缓冲区
 。如果使用了 [BufferAllocation_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)，
 那么
 以太网缓冲区则无法从以太网传输端中断中释放，
 因此必须在下一次使用相同 DMA 描述符时由 pfOutput() 函数释放
 。反正通常只使用一、两个描述符传输数据，
 所以不会浪费太多的
 RAM。

```c

static BaseType_t prvSAM_NetworkInterfaceOutput(   
                      NetworkInterface_t * pxInterface,  
                      NetworkBufferDescriptor_t * const pxDescriptor,  
                      BaseType_t xReleaseAfterSend )  
{  
DMADescriptor_t *pxDMATxDescriptor;  

    /* This example assumes GetNextTxDescriptor() is an Ethernet MAC driver library  
       function that returns a pointer to a DMA descriptor of type DMADescriptor_t. */  

    pxDMATxDescriptor = GetNextTxDescriptor();  

    /* Further, this example assumes the DMADescriptor_t type has a member  
       called pucEthernetBuffer that points to the buffer the DMA will transmit, and  
       a member called xDataLength that holds the length of the data the DMA will  
       transmit.  If [BufferAllocation_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management) is being used then the DMA descriptor may  
       still be pointing to the buffer it last transmitted.  If this is the case  
       then the old buffer must be released (returned to the TCP/IP stack) before  
       descriptor is updated to point to the new data waiting to be transmitted. */  

    if( pxDMATxDescriptor->pucEthernetBuffer != NULL )  
    {  
        /* Note this is releasing just an Ethernet buffer, not a network buffer  
           descriptor as the descriptor has already been released. */  

        [vReleaseNetworkBuffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/06-vReleaseNetworkBuffer)( pxDMATxDescriptor->pucEthernetBuffer );  
    }  

    /* Configure the DMA descriptor to send the data referenced by the network buffer  
       descriptor.  This example assumes SendData() is an Ethernet peripheral driver  
       function. */  

    pxDMATxDescriptor->pucEthernetBuffer = pxDescriptor->pucEthernetBuffer;  

    pxDMATxDescriptor->xDataLength = pxDescriptor->xDataLength;  

    SendData( pxDMATxDescriptor );  

    /* Call the standard trace macro to log the send event. */  

    iptraceNETWORK_INTERFACE_TRANSMIT();  

    /* The network buffer descriptor must now be returned to the TCP/IP stack, but  
       the Ethernet buffer referenced by the network buffer descriptor is still in  
       use by the DMA.  Remove the reference to the Ethernet buffer from the network  
       buffer descriptor so releasing the network buffer descriptor does not result  
       in the Ethernet buffer also being released.  xReleaseAfterSend() should never  
       equal pdFALSE when  [ipconfigZERO_COPY_TX_DRIVER](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigZERO_COPY_TX_DRIVER) is set to 1 (as it should be  
       if data is transmitted using a zero copy driver.*/  

    if( xReleaseAfterSend != pdFALSE )  
    {  
        pxDescriptor->pucEthernetBuffer = NULL;  

        vReleaseNetworkBufferAndDescriptor( pxDescriptor );  
    }  

    return pdTRUE;  
}  
```

零拷贝实现 xNetworkInterfaceOutput()示例

#### 使用零拷贝接收数据

 如果使用零拷贝执行接收，则必须
 将 [ipconfigZERO_COPY_RX_DRIVER](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigZERO_COPY_RX_DRIVER) 设置为 1。

 接收 DMA 会将接收到的帧放入
 接收 DMA 描述符指向的缓冲区。此缓冲区通过调用
 [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer) 来分配，
 以便可以从网络缓冲区描述符中引用它，
 从而通过引用直接将其传递至 TCP/IP 堆栈。然后
 分配一个新的空网络缓冲区，并更新接收 DMA 描述符
 以指向随时可接收下一个数据包的空缓冲区。

 所有关于简单接收处理程序实现的说明事项
 （包括旨在提高效率的高级功能）均适用于零
 拷贝接收处理程序，此处不再赘述。

```c

/* The deferred interrupt handler is a standard RTOS task.  FreeRTOS's   
   [centralised deferred interrupt handling](/Documentation/02-Kernel/02-Kernel-features/11-Deferred-interrupt-handling) capabilities can also be used -   
   **however** for additional speed use [BufferAllocation_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)to perform the entire operation in the interrupt  
   handler. */  

static void prvEMACDeferredInterruptHandlerTask( void *pvParameters )  
{  
    NetworkBufferDescriptor_t *pxDescriptor;  
    size_t xBytesReceived;  
    DMADescriptor_t *pxDMARxDescriptor;  
    uint8_t *pucTemp;  

    /* Used to indicate that xSendEventStructToIPTask() is being called because  
       of an Ethernet receive event. */  
    [IPStackEvent_t](#接收数据) xRxEvent;  

    for( ;; )  
    {  
        /* Wait for the Ethernet MAC interrupt to indicate that another packet  
           has been received.  The task notification is used in a similar way to a  
           counting semaphore to count Rx events, but is a lot more efficient than  
           a semaphore. */  
      [ulTaskNotifyTake](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)( pdFALSE, portMAX_DELAY );  

      /* This example assumes GetNextRxDescriptor() is an Ethernet MAC driver  
         library function that returns a pointer to the DMA descriptor (of type  
         DMADescriptor_t again) that references the Ethernet buffer containing the  
         received data. */  
      pxDMARxDescriptor = GetNextRxDescriptor();  

      /* Allocate a new network buffer descriptor that references an Ethernet  
          frame large enough to hold the maximum network packet size (as defined  
          in the FreeRTOSIPConfig.h header file). */  
      pxDescriptor = pxGetNetworkBufferWithDescriptor( ipTOTAL_ETHERNET_FRAME_SIZE, 0 );  

      /* Copy the pointer to the newly allocated Ethernet frame to a temporary  
         variable. */  
      pucTemp = pxDescriptor->pucEthernetBuffer;  

      /* This example assumes that the DMADescriptor_t type has a member  
         called pucEthernetBuffer that points to the Ethernet buffer containing  
         the received data, and a member called xDataLength that holds the length  
         of the received data.  Update the newly allocated network buffer descriptor  
         to point to the Ethernet buffer that contains the received data. */  
      pxDescriptor->pucEthernetBuffer = pxDMARxDescriptor->pucEthernetBuffer;  

      pxDescriptor->xDataLength = pxDMARxDescriptor->xDataLength;  

      /* Update the Ethernet Rx DMA descriptor to point to the newly allocated  

         Ethernet buffer. */  

      pxDMARxDescriptor->puxEthernetBuffer = pucTemp;  

      /* A pointer to the descriptor is stored at the front of the buffer, so  
         swap these too. */  

      *( ( NetworkBufferDescriptor_t ** )  

         ( pxDescriptor->pucEthernetBuffer - ipBUFFER_PADDING ) ) = pxDescriptor;  

      *( ( NetworkBufferDescriptor_t ** )  

         ( pxDMARxDescriptor->pucEthernetBuffer - ipBUFFER_PADDING ) ) = pxDMARxDescriptor;  

      /*  
       * The network buffer descriptor now points to the Ethernet buffer that  
       * contains the received data, and the Ethernet DMA descriptor now points  
       * to a newly allocated (and empty) Ethernet buffer ready to receive more  
       * data.  No data was copied.  Only pointers to data were swapped.  
       *  
       * THE REST OF THE RECEIVE HANDLER FUNCTION FOLLOWS THE EXAMPLE PROVIDED  
       * FOR THE SIMPLE ETHERNET INTERFACE IMPLEMENTATION, whereby the network  
       * buffer descriptor is sent to the TCP/IP on the network event queue.  
       */  

      /* See if the data contained in the received Ethernet frame needs  
         to be processed.  **NOTE!** It might be possible to do this in  
         the interrupt service routine itself, which would remove the need  
         to unblock this task for packets that don't need processing. */  

      if( eConsiderFrameForProcessing( pxDescriptor->pucEthernetBuffer )  
                                  == eProcessBuffer )  
      {  
          pxDescriptor->pxEndPoint = FreeRTOS_MatchingEndpoint( pxMyInterface, pxBufferDescriptor->pucEthernetBuffer );  

          if( pxDescriptor->pxEndPoint != NULL )  
          {  
              /* The event about to be sent to the TCP/IP is an Rx event. */  
              xRxEvent.eEventType = eNetworkRxEvent;  

              /* pvData is used to point to the network buffer descriptor that  
                 references the received data. */  
              xRxEvent.pvData = ( void * ) pxDescriptor;  

              /* Send the data to the TCP/IP stack. */  
              if( xSendEventStructToIPTask( &xRxEvent, 0 ) == pdFALSE )  
              {  
                  /* The buffer could not be sent to the IP task so the buffer  
                     must be released. */  
                  vReleaseNetworkBufferAndDescriptor( pxDescriptor );  
                  /* Make a call to the standard trace macro to log the  
                     occurrence. */  
                  iptraceETHERNET_RX_EVENT_LOST();  
              }  
              else  
              {  
                  /* The message was successfully sent to the TCP/IP stack.  
                     Call the standard trace macro to log the occurrence. */  
                  iptraceNETWORK_INTERFACE_RECEIVE();  
              }  
          }  
          else  
          {  
              /* The Ethernet frame can be dropped, but the Ethernet buffer  
                 must be released. */  
              vReleaseNetworkBufferAndDescriptor( pxDescriptor );  
          }  
      }  
      else  
      {  
          /* The Ethernet frame can be dropped, but the Ethernet buffer  
             must be released. */  
          vReleaseNetworkBufferAndDescriptor( pxDescriptor );  
      }  
  }  
}  
```

零拷贝接收处理程序函数示例
