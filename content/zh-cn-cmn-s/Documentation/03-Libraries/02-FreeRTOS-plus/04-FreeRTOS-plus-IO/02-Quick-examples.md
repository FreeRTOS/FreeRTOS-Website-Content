---
title: FreeRTOS-Plus-IO 快速示例
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

此页面包含基本的源代码示例，以演示 FreeRTOS-Plus-IO 概念。本网站的 
[API 引用](FreeRTOS_IO_API_Functions) 
和[传输模式部分](FreeRTOS_IO_Transfer_Modes)提供了更详细的示例。在板级支持软件包中提供了全面的应用示例， 
并在 
[精选演示](Demo_Applications/LPCXpresso_LPC1769/NXP_LPC1769_Demo_Description)页面上列出了一些知名项目。

示例 1 演示了如何从已打开并配置的外围设备中读取字节。 
该示例适用于所有数据传输模式。


```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  

/* The size of the buffer into which data will be read. */  
#define BUFFER_SIZE        200  

/* The buffer itself. */  
const int8_t cBuffer[ 200 ] = { 0 };  

/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a  
   descriptor. */  
void vReadExample( Peripheral_Descriptor_t xOpenPort )  
{  
size_t xBytesTransferred;  

    /* The peripheral has already been opened and configured. Read BUFFER_SIZE  
       bytes into cBuffer. The syntax is the same here no matter which  
       transfer mode is being used. */  
    xBytesTransferred = FreeRTOS_read( xOpenPort, cBuffer, BUFFER_SIZE );  

    /* xBytesTransferred will now hold the number of bytes read, which could be  
       less than BUFFER_SIZE bytes if the configured read timeout expired before  
       the requested amount of data was available. */  
}  
```
*示例 1： 从已打开并配置的描述符中读取字节。*


示例 2 演示了如何将字节写入已打开并配置为 
使用[中断驱动零拷贝写入](Zero_Copy_Transfer_Mode)传输模式的外围设备。


```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  

/* The size of the buffer to read and write. */  
#define BUFFER_SIZE        200  

/* The buffer itself. */  
const int8_t cBuffer[ 200 ] = { 0 };  

/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a  
   descriptor. */  
void vWriteExample( Peripheral_Descriptor_t xOpenPort )  
{  
size_t xBytesTransferred;  
BaseType_t xReturn;  
  
    /* This port is configured to use the zero copy Tx transfer mode, so the   
       write mutex must be obtained before starting a new write operation. Wait   
       a maximum of 200ms for the mutex - this task will not consume any CPU time   
       while it is waiting. */  
    xReturn = FreeRTOS_ioctl( xOpenPort, iocltOBTAIN_WRITE_MUTEX, ( void * ) ( 200 / portTICK_PERIOD_MS ) );  
  
    if( xReturn != pdFAIL )  
    {  
        /* The write mutex was obtained, so it is safe to perform a write. This  
           writes BUFFER_SIZE bytes from cBuffer to the peripheral. */  
        xBytesTransferred = FreeRTOS_write( xOpenPort, cBuffer, BUFFER_SIZE );  
  
        /* The actual peripheral transmission is performed by an interrupt, so,   
           in the particular case of using a zero copy transfer, xBytesTransferred   
           will be either 0, if the transfer could not be started, or equal to   
           BUFFER_SIZE. Note however, that the interrupt may still be in the process   
           of actually transmitting the data, even though the function has returned.   
           The actual transmission of data will have completed when the mutex is  
           available again. */  
    }  
}  
```
*示例 2： 向已打开并配置为使用零
拷贝写入传输模式的描述符写字节。*

示例 3 演示了如何打开和配置描述符。首先，打开一个 I2C 移植。然后， 
假设打开成功，移植将被配置为零拷贝写入传输和循环缓冲区读取 
传输。读取超时和写入超时均设置为 200ms。

```c
/* FreeRTOS-Plus-IO includes. */  
#include "FreeRTOS_IO.h"  
  
Peripheral_Descriptor_t xOpenAndConfigureI2CPort( void )  
{  
/* The Peripheral_Descriptor_t type is the FreeRTOS-Plus-IO equivalent of a descriptor. */  
Peripheral_Descriptor_t xI2CPort;  
  
    /* Open the I2C0 port, storing the returned value as the port's descriptor.  
       The peripherals that are actually available to be opened depends on the board  
       support package being used. The second parameter is not currently used and can  
       be set to anything, although, for future compatibility, it is recommended that  
       it is set to NULL. By default, the port is opened with its transfer mode set   
       to polling. */  
    xI2CPort = FreeRTOS_open( "/I2C0/", NULL );  
  
    /* FreeRTOS_open() returns NULL when the open operation cannot complete. Check   
       the return value is not NULL. */  
    configASSERT( xI2CPort );  
  
    /* Configure the port for zero copy Tx. The third parameter is not used in   
       this case. */  
    FreeRTOS_ioctl( xI2CPort, iocltUSE_ZERO_COPY_TX, NULL );  
  
    /* Configure the same port for circular buffer Rx. This time the third  
       parameter is used, and defines the buffer size.  
    FreeRTOS_ioctl( xI2CPort, iocltUSE_CIRCULAR_BUFFER_RX, ( void * ) 100 );  
  
    /* Set the read timeout to 200ms. This is the maximum time a FreeRTOS_read()   
       call will wait for the requested amount of data to be available. As the port   
       is configured to use interrupts, the task performing the read is in the   
       Blocked state while the operation is in progress, so not consuming any CPU time.   
       An interrupt driven zero copy write does not require a timeout to be set. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_RX_TIMEOUT, ( void * ) ( 200 / portTICK_PERIOD_MS ) );  
  
    /* Set the I2C clock frequency to 400000. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_SPEED, ( void * ) 400000 );  
  
    /* Set the I2C slave address to 50. */  
    FreeRTOS_ioctl( xI2CPort, iocltSET_I2C_SLAVE_ADDRESS, ( void * ) 50 );  
  
    /* Return a handle to the open port, which can now be used in FreeRTOS_read()  
       and FreeRTOS_write() calls. */  
    return xI2CPort;  
}  
```
*示例 3： 打开并配置描述符*

