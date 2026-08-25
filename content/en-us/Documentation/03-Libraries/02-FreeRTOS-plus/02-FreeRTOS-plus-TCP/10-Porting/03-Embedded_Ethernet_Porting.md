---
title: Porting FreeRTOS-Plus-UDP to a Different Microcontroller
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

![](/media/2019/warning_icon.png)
FreeRTOS+UDP was removed from the FreeRTOS kernel download from FreeRTOS V10.1.0. See
the [FreeRTOS+TCP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), which can be configured for UDP only use, as an
alternative.

### Introduction

 The implementation of the network interface, and in particular the Ethernet
 MAC driver, are crucial to the data throughput that can be achieved when
 using the embedded TCP/IP stack. For high throughput the
 MAC driver must make efficient use of the DMA and avoid copying
 data where possible. End to end zero copy is possible with
 FreeRTOS-Plus-TCP for UDP packets, and an advanced interface exists that also
 allows zero copy for TCP packets. There are also advanced options available
 that allow packets to be filtered before they are even sent to the embedded
 TCP/IP stack, and packets that are received in quick successions can be
 sent to the embedded TCP/IP stack in one go rather than individually.
 
 However, few applications actually require throughput to be maximised,
 especially on small MCUs, and the implementer may instead
 opt to sacrifice throughput in favour or simplicity.

 This page describes how to interface FreeRTOS-Plus-TCP with a network driver,
 and provides an outline example of both a [simple](#functions-that-must-be-implemented-by-the-port-layer)
 and a [faster](#example-implementation-of-pfinitialise-for-a-zero-copy-port-layer) (but more complex)
 interface. **It is very important to refer to these examples as
 they demonstrate how network buffers are freed after data has been
 transmitted.**

 The network driver port layers that ship with FreeRTOS-Plus-TCP are located in the
 FreeRTOS-Plus-TCP/source/portable/NetworkInterface directory of the
 FreeRTOS-Plus-TCP download. Note however that these drivers have been created
 in order to allow testing of the embedded TCP/IP stack, and are not
 intended to represent optimised examples.

### Summary Bullet Points

![porting the free TCP IP stack to a different MCU](/media/2018/network_interface.png)

**The network interface port layer sits between the IP stack and the embedded Ethernet hardware drivers** 

* Each MCU to which FreeRTOS-Plus-TCP is ported requires an Ethernet
 MAC driver. It is assumed this already exists and is known to
 work.
* FreeRTOS-Plus-TCP is ported to new hardware by providing a 'network
 interface port layer' that provides the interface between the embedded
 TCP/IP stack and the Ethernet MAC driver. See the image on the
 right.
* The network interface port layer must provide a function called 
 [`px[port_name]_FillInterfaceDescriptor()`](#pxport_name_fillinterfacedescriptor) 
 that initialises the instance of the 'network interface port layer'.

	+ When the FreeRTOS+TCP library is built with 
	 [ipconfigIPv4\_BACKWARD\_COMPATIBLE](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigIPv4_BACKWARD_COMPATIBLE) enabled, 
	 the network interface port layer must also provide a function `pxFillInterfaceDescriptor`.
* The network interface port layer must provide a callback function called 
 [pfInitialise()](#pfinitialise) 
 that initialises the MAC driver in the instance of the 'network interface port layer'.
* The network interface port layer must provide a callback function called 
 [pfOutput()](#pfoutput) 
 that sends data received from the embedded TCP/IP stack to the Ethernet MAC driver 
 for transmission in the instance of the 'network interface port layer'.
* The network interface port layer must send packets received
 from the Ethernet MAC driver to the TCP/IP stack by calling
 [xSendEventStructToIPTask()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/08-xSendEventStructToIPTask).
* Only if [BufferAllocation\_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management) is used for buffer allocation, the network
 interface port layer must statically allocate [network buffers](#network-buffers-and-network-buffer-descriptors) and
 provide a function called
 [vNetworkInterfaceAllocateRAMToBuffers()](#vnetworkinterfaceallocateramtobuffers-only-when-bufferallocation_1c-is-used)
 to assign the statically allocated network buffers to network
 buffer descriptors.
* Network buffers (the buffer in which the actual data is stored)
 are referenced using
 [NetworkBufferDescriptor\_t](#network-buffers-and-network-buffer-descriptors)
 structures.
* The embedded TCP/IP stack provides a set of
 [porting utility functions](#functions-provided-by-the-tcpip-stack-for-use-by-the-port-layer)
 to allow the port layer to perform actions such as obtaining and
 freeing network buffers.

 This page provides more information on each of these steps, and provides two
 examples. The [first example demonstrates](#functions-that-must-be-implemented-by-the-port-layer)
 how to implement a simple (but slower) driver. The
 [second example](#example-implementation-of-pfinitialise-for-a-zero-copy-port-layer)
 demonstrates how to implement a more sophisticated (and faster) driver.
 **It is very important to refer to these examples as
 they demonstrate how network buffers are freed after data has been
 transmitted.**

---

### Network Buffers and Network Buffer Descriptors

 Ethernet (or other network) frames are stored in network buffers. A network buffer descriptor
 (a variable of type NetworkBufferDescriptor\_t) is used to describe a network
 buffer, and pass network buffers between the TCP/IP stack and the network
 drivers.

![Embedded network buffers](/media/2018/Ethernet_buffer.png)

**pucEthernetBuffer points to the start of the network buffer.

 xDataLength holds the size of the buffer in bytes, excluding the Ethernet CRC bytes.** 

 Only the following two members of the NetworkBufferDescriptor\_t structure should
 be accessed:

1. uint8\_t *pucEthernetBuffer;

 pucEthernetBuffer points to the start of the network buffer.
2. size\_t xDataLength

 xDataLength holds the size of the network buffer pointed to by pucEthernetBuffer.
 The size is specified in bytes but the length excludes the bytes that
 hold the Ethernet frame's CRC byte.

[pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer)
 is used to obtain just the network buffer itself, and is normally only
 used in zero copy drivers.

[pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor)
 is used to obtain both a network buffer **and** a network buffer
 descriptor at the same time.

### Functions That Must be Implemented by the Port Layer

#### px[port_name]_FillInterfaceDescriptor()

##### (For example: pxSAM\_FillInterfaceDescriptor)

px[port_name]_FillInterfaceDescriptor()
 must initialise the instance of 'network interface port layer'. Below is the data structure of the instance.

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

* pcName is used for debugging purposes, and it's usually a unique name for the network interface.
* pvArgument is the arguments passed to the access functions.
* pfInitialise is the callback function that initialises the MAC driver.
* pfOutput is the callback function that sends data received from the embedded TCP/IP stack to the Ethernet MAC driver for transmission.
* pfGetPhyLinkStatus provides the query function for users to get the interface's status.
* bits contains bInterfaceUp and bCallDownEvent which represent whether the interface is up and the down 
 event is pending respectively.
* pxEndPoint is the list of endpoints that are bound to this interface.
* pxNext is the next interface instance in a linked list structure.

#### pxFillInterfaceDescriptor()

 When [ipconfigIPv4\_BACKWARD\_COMPATIBLE](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigIPv4_BACKWARD_COMPATIBLE)
 is enabled, the function FreeRTOS\_IPInit() will call pxFillInterfaceDescriptor to initialise the interface descriptor. The 
 implementation of this function can just call the 
 [`px[port_name]_FillInterfaceDescriptor()`](#pxport_name_fillinterfacedescriptor) as the functionality is the same.

#### pfInitialise()

pfInitialise() is the callback function in the instance of the 'network interface port layer', 
 it must prepare the Ethernet MAC to send and receive data. In most cases this will just involve calling 
 whichever initialise function is provided with the Ethernet MAC peripheral drivers - which will in turn 
 ensure the MAC hardware is enabled and clocked, as well as configure the MAC peripheral's DMA descriptors.
 
pfInitialise() takes the network interface as a parameter. It returns pdPASS if the initialisation was successful, 
 and returns pdFAIL if the initialisation fails.

```c

typedef BaseType_t ( * NetworkInterfaceInitialiseFunction_t ) ( struct xNetworkInterface * pxDescriptor );  
```

The pfInitialise() function prototype

#### pfOutput()

**The TCP/IP stack calls pfOutput() whenever a network buffer is ready to be transmitted.**  

A description of the buffer to transmit is passed into the function using the function's pxDescriptor parameter. 
If xReleaseAfterSend does not equal pdFALSE then both the buffer and the buffer's descriptor must be 
released (returned) back to the embedded TCP/IP stack by the driver code when they are no longer required. If 
xReleaseAfterSend is pdFALSE then both the network buffer and the buffer's descriptor will be released 
by the TCP/IP stack itself (in which case the driver does not need to release them).

Note that, at this time, the value returned from pfOutput() is ignored. The embedded TCP/IP stack will NOT call 
pfOutput() for the same network buffer twice, even if the first call to pfOutput() could not send the 
network buffer on to the network.  

Basic and more advanced examples are provided below, and the FreeRTOS-Plus-TCP/source/portable/NetworkInterface 
directory of the FreeRTOS-Plus-TCP download contains examples that can be referenced. Note, however, that the examples 
in the download may not be optimised.

```c

typedef BaseType_t ( * NetworkInterfaceOutputFunction_t ) ( struct xNetworkInterface * pxDescriptor,  
                                                            NetworkBufferDescriptor_t * const pxNetworkBuffer,  
                                                            BaseType_t xReleaseAfterSend );         
```

The pfOutput() function prototype

#### vNetworkInterfaceAllocateRAMToBuffers() only when BufferAllocation\_1.c is used

[BufferAllocation\_1.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)
 uses pre-allocated network buffers that are normally
 statically allocated at compile time.
 
 The number of network buffers that must be allocated is set by the
 [ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfignum_network_buffer_descriptors)
 definition in FreeRTOSIPConfig.h, and the size of each buffer must be
 ( ipTOTAL\_ETHERNET\_FRAME\_SIZE + ipBUFFER\_PADDING ). ipTOTAL\_ETHERNET\_FRAME\_SIZE is
 calculated automatically from the value of
 [ipconfigNETWORK\_MTU](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigNETWORK_MTU),
 and ipBUFFER\_PADDING is calculated automatically from
 [ipconfigBUFFER\_PADDING](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigBUFFER_PADDING).

 Networking hardware can impose strict alignment requirements on the
 allocated buffers, so it is recommended that the buffers are allocated
 in the embedded Ethernet driver itself - that way the buffer's alignment
 can always be made to match the hardware's requirements.

 The embedded TCP/IP stack allocates the network buffer descriptors, but
 does not know anything about the alignment of the network buffers themselves.
 Therefore the embedded Ethernet driver must also provide a function called
 vNetworkInterfaceAllocateRAMToBuffers() that allocates a statically
 declared buffer to each descriptor. Note that ipBUFFER\_PADDING bytes
 at the beginning of the buffer are left for use by the embedded TCP/IP
 stack itself. See the example below.

```c

void vNetworkInterfaceAllocateRAMToBuffers(  
       NetworkBufferDescriptor_t xDescriptors[ ipconfigNUM_NETWORK_BUFFERS ] );  
```

The vNetworkInterfaceAllocateRAMToBuffers() function prototype
<br/>
<br/>

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

An example implementation of vNetworkBufferInterfaceAllocateRAMToBuffers().

### Functions Provided by the TCP/IP Stack For Use By The Port Layer

 The port layer can use the following functions:
 * [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor) -

 Obtains both a network buffer and a descriptor that describes the
 network buffer. This function can also be used to obtain just a
 network buffer descriptor - which can be useful when implementing
 zero copy drivers.
* [vReleaseNetworkBufferAndDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/04-vReleaseNetworkBufferAndDescriptor) -

 Releases (returns to the embedded TCP/IP stack) a network buffer descriptor, and
 the network buffer referenced by the descriptor (if any).
* pxNetworkBufferGetFromISR() - not available when [BufferAllocation\_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management) is used

* vNetworkBufferReleaseFromISR() - not available when [BufferAllocation\_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management) is used

* [eConsiderFrameForProcessing()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/07-eConsiderFrameForProcessing) -
 Used to determine if data received from the network needs to be
 passed to the embedded TCP/IP stack. Ideally this function would
 be called from the network interrupt to allow received packets to
 be discarded at the earliest possible opportunity.

* [xSendEventStructToIPTask()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/08-xSendEventStructToIPTask) -
 xSendEventStructToIPTask() is a function used by the embedded TCP/IP
 stack itself to send various events to the RTOS task that is running
 the embedded TCP/IP stack. The port layer uses the function with
 eNetworkRxEvent events to pass received data into the stack for processing.

* [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer) -
 Obtains just a network buffer, without a network buffer descriptor.
 This function is normally only used in zero copy interfaces to
 allocate buffers to DMA descriptors.

* [vReleaseNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/06-vReleaseNetworkBuffer) -
 Releases (returns to the embedded TCP/IP stack) a network buffer
 by itself - without a network buffer descriptor. This function
 is normally only used in zero copy interfaces where network buffers
 were allocated to DMA descriptors.

* [FreeRTOS\_AddNetworkInterface()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/02-FreeRTOS_AddNetworkInterface) -
 Appends the current instance of the network interface to the linked list in the TCP/IP Stack.

* [FreeRTOS\_FirstEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/09-FreeRTOS_FirstEndPoint) -
 Used to get the first end-point stored in the TCP/IP Stack. The port layer normally uses this 
 function to get all MAC addresses stored in the TCP/IP stack, then sets the hardware to allow 
 packets for these addresses.

* [FreeRTOS\_NextEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/11-FreeRTOS_NextEndPoint) -
 Used to get the next end-point stored in the TCP/IP Stack. The port layer normally uses this 
 function to get all MAC addresses stored in the TCP/IP stack, then sets the hardware to allow 
 packets for these addresses.

* [FreeRTOS\_MatchingEndpoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/10-FreeRTOS_MatchingEndpoint) -
 Finds the best end-point for an incoming ethernet packet. The port layer must set the end-point 
 in the network buffer descriptor correctly before sending it to the TCP/IP stack.

### Receiving Data

 The Ethernet MAC driver will place received Ethernet frames into a buffer.
 The port layer has to:

1. Determine if the received data needs to be sent to the embedded
 TCP/IP stack. Ideally this would be done in the receive interrupt
 itself to allow unnecessary packets to be dropped at the earliest
 possible time.
2. Allocate a network buffer descriptor.
3. Set the xDataLength and pucEthernetBuffer members of the allocated
 descriptor accordingly (see both the basic and zero copy examples
 later on this page).
4. Call xSendEventStructToIPTask() to send the network buffer
 descriptor into the embedded TCP/IP stack for processing
 (see both the basic and zero copy examples later on this
 page).

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
The IPStackEvent\_t type

<br/>
<br/>

```c
/* The timeout is specified in RTOS ticks.  Returns pdTRUE if the message was  
sent successfully, otherwise return pdFALSE. */  
BaseType_t xSendEventStructToIPTask( const IPStackEvent_t *pxEvent, TickType_t xTimeout )  
```

The xSendEventStructToIPTask() function prototype

<br/>
<br/>

Basic and more advanced examples are provided below. The network driver 
port layers that ship with FreeRTOS-Plus-TCP (which are not necessarily 
optimised) can be found in the FreeRTOS-Plus-TCP/source/portable/NetworkInterface 
directory.

### Network Interface Port Layer Examples

#### 1. Example of px[port_name]_FillInterfaceDescriptor() as common part for the interface port layer.

 Each network interface must provide a function to initialise an instance of it, and which is called 
 [`px[port_name]_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#pxport_name_FillInterfaceDescriptor). 
 This function initialises the callback functions in the instance structure and appends the instance 
 to the linked list by calling 
 [FreeRTOS\_AddNetworkInterface()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/02-FreeRTOS_AddNetworkInterface).

 **Example implementation of px[port_name]_FillInterfaceDescriptor()** (taking a SAM driver as an example)

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

**Example implementation of pxFillInterfaceDescriptor()** (taking a SAM driver as an example)

```c
#if ( ipconfigIPv4_BACKWARD_COMPATIBLE == 1 )  
    NetworkInterface_t * pxFillInterfaceDescriptor( BaseType_t xEMACIndex,  
                                                    NetworkInterface_t * pxInterface )  
    {  
        return pxSAM_FillInterfaceDescriptor( xEMACIndex, pxInterface );  
    }  
#endif
```

#### 2. Example of a Basic Network Interface Port Layer

 Simple network interfaces can be created by copying Ethernet frames
 between buffers allocated by the Ethernet MAC driver libraries and buffers
 allocated by the port layer. [A more efficient zero copy
 alternative is provided
 [after the simple example](#example-implementation-of-pfinitialise-for-a-zero-copy-port-layer).] 


##### Example implementation of pfInitialise() for a basic port layer

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

pfInitialise() is hardware specific, therefore this example describes what needs to be done without showing any detail

##### Example implementation of pfOutput() for a basic port layer

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

Example implementation of pfOutput() suitable for a simple (rather than zero copy) network interface implementation

##### Example of passing received data to the TCP/IP in a basic port layer

 When a packet is received from the Ethernet (or other network) driver
 the port layer must use a [NetworkBufferDescriptor\_t](#network-buffers-and-network-buffer-descriptors)
 structure to describe the packet, then call
 [xSendEventStructToIPTask()](#receiving-data)
 to send the NetworkBufferDescriptor\_t structure to the embedded TCP/IP stack.
 
**NOTE 1:** If [BufferAllocation\_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)
 is used then network buffer
 descriptors and Ethernet buffers cannot be allocated from inside an
 interrupt service routine (ISR). In this case the Ethernet MAC receive
 interrupt can [defer the receive
 processing to a task](../../deferred_interrupt_processing). This is demonstrated
 below.

**NOTE 2:** There are numerous advanced techniques that can be employed
 to minimise the amount of data sent from the port layer into the embedded
 TCP/IP stack. For example, [eConsiderFrameForProcessing()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/07-eConsiderFrameForProcessing)
 can be called to determine if the received Ethernet frame needs to be
 sent to the embedded TCP/IP stack at all, and Ethernet frames that are
 received in quick succession can be sent to the embedded TCP/IP stack in
 one go. See the
 [Hardware and Driver Specific Settings](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#hardware_specific_settings)
 section of the FreeRTOS-Plus-TCP configuration page for more information.

**NOTE 3:**Remember to set pxEndPoint correctly by calling 
 [FreeRTOS\_MatchingEndPoint()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/10-FreeRTOS_MatchingEndpoint) 
 before sending packets and a descriptor to the TCP/IP stack.

```c

/* The deferred interrupt handler is a standard RTOS task.  FreeRTOS's   
   [centralised deferred interrupt handling](/Documentation/02-Kernel/02-Kernel-features/11-Deferred-interrupt-handling) capabilities can also be used. */  
static void prvEMACDeferredInterruptHandlerTask( void *pvParameters )  
{  
    NetworkBufferDescriptor_t *pxBufferDescriptor;  
    size_t xBytesReceived;  

    /* Used to indicate that xSendEventStructToIPTask() is being called because  
       of an Ethernet receive event. */  
    [IPStackEvent_t](#receiving-data) xRxEvent;  

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
                   parameter.  **Remember!** While it is a simple robust technique -  
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

An example of a simple (rather than more efficient zero copy) receive handler

#### 3. Example of a More Efficient Network Interface Port Layer

 It is intended that this section is read after the section that describes
 how to create a simple network interface port layer.
 
 Simple network interfaces copy Ethernet frames between buffers used and
 managed by the TCP/IP stack and buffers used and managed by the Ethernet
 (or other network) MAC drivers. Copying data between
 buffers makes the driver's implementation simple, but is inefficient.

 Zero copy network interfaces do not copy data between buffers, but instead
 pass references to buffers between the TCP/IP stack and the Ethernet MAC
 drivers.

 Zero copy interfaces are more complex, and can rarely be created without
 editing the Ethernet MAC drivers themselves.

 If transmission is performed using zero copy then it is necessary to
 set [ipconfigZERO\_COPY\_TX\_DRIVER](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigZERO_COPY_TX_DRIVER) to 1.

 Most Ethernet hardware will use DMA (Direct Memory Access) to move frames
 between the Ethernet hardware and pre-allocated RAM buffers. Normally
 the pre-allocated memory buffers are referenced using a set of DMA
 descriptors. DMA descriptors are normally chained - each descriptor
 points to the next in the chain, with the last in the chain pointing
 back to the first.

![Chained embedded Ethernet buffers](/media/2018/Network_DMA_Descriptors.png)

 Chained DMA descriptors

##### Example implementation of pfInitialise() for a zero copy port layer

pfInitialise() must use
 [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer)
 to obtain the pointers to which the receive DMA descriptors point. It is
 not necessary to allocate any buffers for the transmit DMA descriptors -
 the buffers will be passed in (by reference) as data becomes available
 to send.

![Zero copy Ethernet driver initialisation](/media/2018/Zero_copy_DMA_initialisation.png)

 The DMA Rx descriptors are initialised to point to buffers
 that were allocated by pucGetNetworkBuffer().

 The DMA Tx descriptors do not point to any buffers after
 they have been initialised.

##### Example implementation of pfOutput() for a zero copy layer

pfOutput() does not copy the frame being transmitted
 to a buffer that is being managed by the MAC driver (it can't because
 the DMA's Tx descriptors are not pointing to any buffers) but instead
 updates the next DMA Tx descriptor so the descriptor points to the buffer
 that already contains the data.
 
**NOTE:** The Ethernet buffer must be released after the data it
 contains has been transmitted. If [BufferAllocation\_2.c](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/05-Buffer-management)
 is used the
 Ethernet buffer cannot be released from the Ethernet Transmit End interrupt,
 so must be released by the pfOutput() function the next
 time the same DMA descriptor is used. Often only one or two descriptors
 are used for transmitting data anyway, so this does not waste too much
 RAM.

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

An example zero copy implementation of xNetworkInterfaceOutput()

##### Receiving Data Using Zero-Copy

 If reception is performed using zero copy then it is necessary to
 set [ipconfigZERO\_COPY\_RX\_DRIVER](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigZERO_COPY_RX_DRIVER) to 1.
 
 The receive DMA will place received frames into the buffer pointed to
 by the receive DMA descriptor. The buffer was allocated using a call
 to [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer),
 which allows it to be referenced from a network buffer descriptor, and
 therefore passed by reference directly into the TCP/IP stack. A new empty
 network buffer is then allocated, and the receive DMA descriptor is updated
 to point to the empty buffer ready to receive the next packet.

 All the notes regarding the implementation of the simple receive handler
 (including advanced features to improve efficiency) apply to the zero
 copy receive handler and are not repeated here.

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
    [IPStackEvent_t](#receiving-data) xRxEvent;  

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

An example of a zero copy receive handler function
