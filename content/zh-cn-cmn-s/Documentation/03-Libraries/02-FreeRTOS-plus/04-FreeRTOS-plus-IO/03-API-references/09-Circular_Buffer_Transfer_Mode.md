---
title: 中断驱动的循环缓冲区传输模式
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO 传输模式](FreeRTOS_IO_Transfer_Modes)]


### 数据方向

中断驱动的循环缓冲区传输模式可与 FreeRTOS_read() 同时使用。


### 描述

必须在 [FreeRTOSIOConfig.h](FreeRTOS_Plus_IO_Configuration) 中将 ioconfigUSE_CIRCULAR_BUFFER_RX 设置为 1，
才可使用循环缓冲区传输模式。此外，还必须在同一配置文件中
为正在使用的外设外围设备明确启用该参数。

选择循环缓冲区传输模式时，FreeRTOS_read() 不会直接从外围设备读取字节，
而是从由 FreeRTOS-Plus-IO 中断服务程序在收到数据时填充的循环缓冲区
读取字节。

中断服务程序和 FreeRTOS 循环缓冲区由 FreeRTOS-Plus-IO 代码实现，
无需由应用程序编写者提供。

**中断驱动的循环缓冲区传输模式**

- **优点**

  - 用法简单的模型

  - 如果无法立即完成调用任务，可自动将其置于 
    [阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) 状态，
    以等待读取操作完成。这可确保
    调用 FreeRTOS_read() 的任务仅在循环缓冲区中有字节时才占用 CPU 时间。

  - 可以设置读取超时时间，以确保 FreeRTOS_read() 调用不会无限期阻塞。

  - 可以使用简单的 RAM 缓冲区，实现效率适中的接收方法，
    但是这种方法需要在缓冲区内外来回复制。

  - 外围设备收到的字节会自动缓冲，即使在收到字节时没有进行 FreeRTOS_read()  
     操作，这些字节也不会丢失。

- **缺点**

  - FreeRTOS-Plus-IO 驱动程序需要 RAM 来存储循环缓冲区。缓冲区长度
    由 FreeRTOS_ioctl() 调用（可用于选择传输模式）的第三个参数配置。

ioctlUSE_CIRCULAR_BUFFER_RX 请求代码可用于在调用 FreeRTOS_ioctl() 时配置外围设备，
使其在执行读取操作时使用中断驱动的循环缓冲区传输模式。请注意，此请求代码
会导致外围设备启用中断，并将外围设备的中断优先级设置为
最低。如有必要，可以使用 ioctlSET_INTERRUPT_PRIORITY 请求代码
提高外围设备的优先级。


### 用法示例

```c
/* FreeRTO+IO includes. */
#include "FreeRTOS_IO.h"

void vAFunction( void )
{
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */
Peripheral_Descriptor_t xOpenedPort;
BaseType_t xReturned;
const uint32_t ulMaxBlock100ms = ( 100UL / portTICK_PERIOD_MS );

    /* Open the SPI port identified in the board support package as using the
       path string "/SPI2/". The second parameter is not currently used and can
       be set to anything, although, for future compatibility, it is recommneded
       that it is set to NULL. */
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );

    if( xOpenedPort != NULL )
    {
        /***************** Configure the port *********************************/

        /* xOpenedPort now contains a valid descriptor that can be used with
           other FreeRTOS-Plus-IO API functions.

           Peripherals default to using Polled mode for both reads and writes.
           Change from the default to use the interrupt driven circular buffer
           transfer mode for reading. The third FreeRTOS_ioctl() parameter sets the
           buffer length. In this example, the length is set to 20. A successful
           FreeRTOS_ioctl() call will return pdPASS, for simplicity, this example
           does not show the return value being checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CIRCULAR_BUFFER_RX, ( void * ) 20 );

        /* By default, a peripheral configured to use an interrupt driven circual
           buffer transfer will have an infinite block time. Lower the block time
           to ensure FreeRTOS_read() calls will return, even in the presense of an
           error. In this example the read block time is set to 100ms. Again, for
           simplicity, this example does not show the return value being checked. */
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_RX_TIMEOUT, ( void * ) ulMaxBlock100ms );


        /***************** Use the port ***************************************/

        for( ;; )
        {
            /* Read 10 bytes from the port into ucBuffer. Note, this will
               not read the bytes from the peripheral directly, but from the circular
               buffer that is populated by the FreeRTOS-Plus-IO peripheral interrupt service
               routine. The calling task is held in the Blocked state to wait
               for 10 bytes to become available if they are not available immediately,
               but the task will not be held in the Blocked state for more than 100ms.
               ucBuffer is assumed to be defined outside of this function. */
            xBytesTransferred = FreeRTOS_read( xOpenedPort, ucBuffer, 10 );

            if( xBytesTransferred == 10 )
            {
                /* Ten bytes were read from the peripheral before the 100ms block
                   time expired. */
            }
            else
            {
                /* The block time must have expired before ten bytes could be
                   read from the peripheral. xBytesTransferred could be any value
                   from 0 to 9. */
            }
        }
    }
    else
    {
        /* The port was not opened successfully. */
    }
}
```

