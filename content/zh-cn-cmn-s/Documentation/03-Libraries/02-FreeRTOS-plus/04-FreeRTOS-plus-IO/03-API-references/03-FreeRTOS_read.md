---
title: FreeRTOS_read()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO API](FreeRTOS_IO_API_Functions)]

FreeRTOS_IO.h

```c
size_t FreeRTOS_read( Peripheral_Descriptor_t const pxPeripheral,
                      void * const pvBuffer,
                      const size_t xBytes );
```

从打开的外围设备读取一个或多个字节。

[板级支持包](Board_Support_Packages)
定义了可以打开的外围设备。 [FreeRTOS_ioctl()](FreeRTOS_ioctl)
用于在中断驱动读取模式和轮询读取模式之间进行选择。

**参数：**

- *pxPeripheral*

  与从中读取字节的外围设备相关联的描述符。此描述符
  将在调用 [FreeRTOS_open()](FreeRTOS_open) 以打开外围设备时返回。

- *pvBuffer*

  放置读取数据的缓冲区。

- *xBytes*

  请求的字节总数。使用中断驱动的[传输模式](FreeRTOS_IO_Transfer_Modes)  
   时，如果在外围设备的读取超时时间结束之前
  无法获得请求的字节总数，则实际读取的字节总数将小于请求的字节总数。
  [FreeRTOS_ioctl()](FreeRTOS_ioctl) 用于设置读取超时值。


**返回：**

读取的字节总数。如果在外围设备的读取超时时间结束之前无法读取请求的字节数，
则此值将小于 xBytes 参数请求的字节数。
[FreeRTOS_ioctl()](FreeRTOS_ioctl) 用于设置读取超时值。


**用法示例：**

示例 1 代码片段演示了当外围设备
配置为使用[轮询传输模式](FreeRTOS_IO_Transfer_Modes)时如何执行读取操作。外围设备
在打开时默认采用轮询模式。

```c
/* By default the port is opened in polled mode. Read sizeof( ucBuffer ) bytes into
   ucBuffer using polled mode. */
xBytesRead = FreeRTOS_read( xPort, ucBuffer, sizeof( ucBuffer ) );

/* The port is currently in polled mode, so FreeRTOS_read() will only have
   returned once all the requested bytes had been read (barring any errors on
   the peripheral). Note that, because polling mode is being used, the task
   making the FreeRTOS_read() call will not have entered the Blocked
   state if it had to wait for the requested number of bytes. */
configASSERT( xBytes == sizeof( ucBuffer ) );
```
*示例 1：从配置为使用轮询传输模式的外围设备读取字节。*


示例 2 代码片段演示了当外围设备配置为使用
中断驱动的字符队列[传输模式](FreeRTOS_IO_Transfer_Modes)
或中断驱动的循环缓冲区传输模式时如何执行读取操作。使用这些模式时，在读取到请求的字节数或者读取超时时间结束之前，执行 FreeRTOS_read() 调用的任务
将处于[阻塞状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)（不占用 CPU 时间）。
FreeRTOS_ioctl()
与 [iocltSET_RX_TIMEOUT](FreeRTOS_ioctl) 请求代码一起用于配置读取超时时间。

```c
/* Read some bytes in one of the interrupt driven transfer modes. If the
   character queue transfer mode is being used, this will remove bytes from the
   queue that had previously been placed into the queue by the FreeRTOS-Plus-IO interrupt
   service routine. If the circular buffer transfer mode is being used, this will
   remove bytes from the circular buffer that had previously been placed into the
   buffer by the FreeRTOS-Plus-IO interrupt service routine. In both cases, read bytes
   are placed in ucBuffer. */
xBytesRead = FreeRTOS_read( xPort, ucBuffer, sizeof( ucBuffer ) );

if( xBytesRead < sizeof( ucBuffer ) )
{
    /* The Rx timeout must have expired before sizeof( ucBuffer ) bytes could
       be read. xBytesRead number of bytes will have been placed into ucBuffer. */
}
else
{
    /* The requested number of bytes were read before the read timeout expired.
       All the requested bytes have been placed in ucBuffer. */
}
```
*示例 2：从配置为使用  
中断驱动的字符队列传输模式或中断驱动的循环  
缓冲区传输模式的外围设备读取字节。*

