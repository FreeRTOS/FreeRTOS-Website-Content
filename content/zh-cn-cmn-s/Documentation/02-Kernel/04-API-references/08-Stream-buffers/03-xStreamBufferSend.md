---
title: xStreamBufferSend()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 流缓冲区 API](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream_buffer.h

```c
size_t xStreamBufferSend( StreamBufferHandle_t xStreamBuffer,
                          const void *pvTxData,
                          size_t xDataLengthBytes,
                          TickType_t xTicksToWait );
```

将字节发送到[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)。
字节复制到流缓冲区中。

**注意**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（消息缓冲区的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一个任务或中断将写入
缓冲区（写入器），而且只有一个任务或中断会从
缓冲区读取（读取器）。写入器和读取器为不同的任务或中断是安全的，
或中断，但与其他 FreeRTOS 对象不同，
拥有多个不同的编写器或多个不同的读取器是不安全的。如果有
多个不同的写入器，那么应用程序写入器必须把对写入 API 函数（如 xStreamBufferSend()）的每个调用放在一个临界区内，
并使用发送阻塞时间 0。
同样，如果有多个不同的读取器，
那么应用程序必须把对读取 API 函数（如 xStreamBufferReceive()）的每个调用放在一个临界区内，
并使用接收阻塞时间 0。

使用 xStreamBufferSend() 从任务写入流缓冲区。使用
xStreamBufferSendFromSISR () 从
中断服务程序 (ISR) 写入流缓冲区。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  作为流发送目标缓冲区的流缓冲区的句柄。

+ *pvTxData* 

  一个指向缓冲区的指针，该缓冲区存放要复制到流缓冲区的字节。

+ *xDataLengthBytes* 

  从 pvTxData 复制到流缓冲区的最大字节数。

+ *xTicksToWait* 

  如果流缓冲区空间太小， 
  无法容纳 
  另一个 xDataLengthBytes 的字节时，任务应保持在阻塞状态，以等待流缓冲区中出现足够空间的最长时间。阻塞时间的单位为滴答周期， 
  因此，它代表的绝对时间取决于滴答频率。pdMS_TO_TICKS() 可用于将以毫秒为单位指定的时间转换为以 
  滴答为单位的时间。将 xTicksToWait 设置为 portMAX_DELAY 将 
  导致任务无限期等待（不超时），前提是 INCLUDE_vTaskSuspend 
  在 FreeRTOSConfig.h 中设置为 1。如果任务在将所有 xDataLengthBytes 写入缓冲区之前超时， 
  它仍然会写入尽可能多的字节数。处于阻塞状态的任务不会使用任何 CPU 时间 
  。


**返回：** 

写入流缓冲区的字节数。如果一个任务
在向缓冲区写入所有 xDataLengthBytes 之前就超时，
它仍然会写入尽可能多的字节数。


**用法示例：**

```c
void vAFunction( StreamBufferHandle_t xStreamBuffer )
{
size_t xBytesSent;
uint8_t ucArrayToSend[] = { 0, 1, 2, 3 };
char *pcStringToSend = "String to send";
const TickType_t x100ms = pdMS_TO_TICKS( 100 );

    /* Send an array to the stream buffer, blocking for a maximum of 100ms to
       wait for enough space to be available in the stream buffer. */
    xBytesSent = xStreamBufferSend( xStreamBuffer,
                                   ( void * ) ucArrayToSend,
                                   sizeof( ucArrayToSend ),
                                   x100ms );

    if( xBytesSent != sizeof( ucArrayToSend ) )
    {
        /* The call to xStreamBufferSend() times out before there was enough
           space in the buffer for the data to be written, but it did
           successfully write xBytesSent bytes. */
    }

    /* Send the string to the stream buffer. Return immediately if there is not
       enough space in the buffer. */
    xBytesSent = xStreamBufferSend( xStreamBuffer,
                                    ( void * ) pcStringToSend,
                                    strlen( pcStringToSend ), 0 );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The entire string could not be added to the stream buffer because
           there was not enough free space in the buffer, but xBytesSent bytes
           were sent. Could try again to send the remaining bytes. */
    }
}
```
