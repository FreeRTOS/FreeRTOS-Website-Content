---
title: 中断驱动字符队列传输模式
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-IO 传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)]


### 数据方向

中断驱动的字符队列传输模式可以与 FreeRTOS_read() 和 FreeRTOS_write() 同时使用。
 
  
### 描述

ioconfigUSE_TX_CHAR_QUEUE and/or ioconfigUSE_RX_CHAR_QUEUE 必须 
在 [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) 中设置为 1，才能将字符队列传输模式 
分别用于写入和读取。此外，还必须在同一配置文件中 
为正在使用的外设外围设备明确启用该参数。

当字符队列传输模式选择为写入时，FreeRTOS_write() 不 
直接向外围设备写入，而是将字节发送到传输队列。外围设备的中断服务 
例程从队列中删除字节，并将其发送到外围设备。

当字符队列传输模式选择为读取时，FreeRTOS_read() 不直接从外围设备读取字节， 
而是从由 FreeRTOS-Plus-IO 中断服务程序在收到数据时填充的接收队列 
读取字节。

中断服务程序和 FreeRTOS 队列由 FreeRTOS-Plus-IO 代码实现， 
无需由应用程序写入器提供。


**中断驱动字符队列传输模式**

+ **优点** 

  * 用法简单的模型 

  * 如果读或写操作无法立即完成，则自动将调用任务置于阻塞状态， 
    等待读或写操作完成。这样  可以确保调用 FreeRTOS_read() 或 
    FreeRTOS_write() 的任务只在可以执行实际处理时才占用 CPU 时间。 

  * 可以设置读取和/或写入超时，以确保 FreeRTOS_read() 和 FreeRTOS_write() 调用不会
    无限期阻塞。 

  * 外围设备收到的字节会自动缓冲，即使在收到字节时没有进行 FreeRTOS_read() 操作， 
    这些字节也不会丢失。 

  * 可以随时调用 FreeRTOS_write()。无需等待前一次传输完成 
    或外围设备空闲。

+ **缺点**

  * FreeRTOS-Plus-IO 驱动程序需要为队列提供 RAM。队列长度由 
    FreeRTOS_ioctl() 调用（可用于选择传输模式）的第三个参数配置。 

  * 字符队列的效率很低， 
    因此应仅限于不需要读写大量数据的应用程序。例如，字符队列为命令行接口提供了一种非常方便的  
    传输模式，  其中字符的接收速度仅取决于输入者的打字速度
    。 

  * FreeRTOS 队列具有内置的互斥机制，但仅限于单字符级别。 
    因此，如果两个任务试图同时执行 
     FreeRTOS_write()（或 FreeRTOS_read()），可以保证队列数据结构体不会损坏， 
    但不能保证在这种情况下数据不会交错。如有必要，应用程序写入器 
    可以使用  任务优先级或外部互斥  （例如使用互斥锁） 
    来防止这种情况的发生。

在调用 
FreeRTOS_ioctl() 时，可使用 ioctlUSE_CHARACTER_QUEUE_TX 和 ioctlUSE_CHARACTER_QUEUE_RX 请求代码 
来配置外围设备分别使用中断驱动的字符队列写入和读取。请注意，这些请求代码将导致外围设备中断被启用， 
外围设备中断优先级被设置为可能的最低等级。必要时，可以使用 ioctlSET_INTERRUPT_PRIORITY 
请求代码来提高外围设备的优先级。
 

### 用法示例

```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  
  
void vAFunction( void )  
{  
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */  
Peripheral_Descriptor_t xOpenedPort;  
BaseType_t xReturned;  
const uint32_t ulMaxBlock100ms = ( 100UL / portTICK_PERIOD_MS );  
  
    /* Open the SPI port identified in the board support package as using the  
       path string "/SPI2/". The second parameter is not currently used and can  
       be set to anything, although, for future compatibility, it is recommended   
       that it is set to NULL. */  
    xOpenedPort = FreeRTOS_open( "/SPI2/", NULL );  
  
    if( xOpenedPort != NULL )  
    {  
        /***************** Configure the port *********************************/  
      
        /* xOpenedPort now contains a valid descriptor that can be used with  
           other FreeRTOS-Plus-IO API functions.   
   
           Peripherals default to using Polled mode for both reads and writes.  
           Change from the default to use interrupt driven character queues for both  
           reading and writing. The third FreeRTOS_ioctl() parameter sets the  
           queue length. In this example, the length is set to 20 in both cases.  
           A successful FreeRTOS_ioctl() call will return pdPASS, for simplicity,  
           this example does not show the return value being checked. */  
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CHARACTER_QUEUE_RX, ( void * ) 20 );  
        FreeRTOS_ioctl( xOpenedPort, ioctlUSE_CHARACTER_QUEUE_TX, ( void * ) 20 );  
                  
        /* By default, a peripheral configured to use an interrupt driven character  
           queue transfer will have an infinite block time. Lower the block time for  
           reading and writing to ensure FreeRTOS_read() and FreeRTOS_write() calls  
           will return, even in the presence of an error. In this example, both  
           the read and write block times are set to 100ms. Again, for simplicity,  
           this example does not show the return value being checked. */  
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_RX_TIMEOUT, ( void * ) ulMaxBlock100ms );  
        FreeRTOS_ioctl( xOpenedPort, ioctlSET_TX_TIMEOUT, ( void * ) ulMaxBlock100ms );  
          
  
        /***************** Use the port ***************************************/  
          
          
        for( ;; )  
        {  
            /* Write 10 bytes from ucBuffer to the opened port. Note the   
               definition of ucBuffer is assumed to be outside of this function. */  
            xBytesTransferred = FreeRTOS_write( xOpenedPort, ucBuffer, 10 );  
              
            /* At this point, 10 bytes will have been written to the Tx queue,  
               but not necessarily written to the peripheral yet. Check all 10 bytes  
               were written to the queue - they should have been as the queue is  
               20 bytes long. */  
            configASSERT( xBytesTransferred == 10 );  
              
            /* Read 10 bytes from the same port into ucBuffer. Note, this will  
               not read the bytes from the peripheral directly, but from the Rx   
               queue that is populated by the FreeRTOS-Plus-IO peripheral interrupt service  
               routine. The calling task is held in the Blocked state to wait  
               for 10 bytes to become available if they are not available immediately,  
               but the task will not be held in the Blocked state for more than 100ms. */  
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
