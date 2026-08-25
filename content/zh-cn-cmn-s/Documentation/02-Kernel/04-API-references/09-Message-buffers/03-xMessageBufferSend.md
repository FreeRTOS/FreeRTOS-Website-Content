---
title: xMessageBufferSend()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 消息缓冲区 API](/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]

message_buffer.h

```c
size_t xMessageBufferSend( MessageBufferHandle_t xMessageBuffer,
                           const void *pvTxData,
                           size_t xDataLengthBytes,
                           TickType_t xTicksToWait );
```

将离散消息发送到[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)。消息可以是
适合缓冲区可用空间的任意长度，并复制到缓冲区中。

**注意**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（消息缓冲区的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一个任务或中断将写入
缓冲区（写入器），而且只有一个任务或中断会从
缓冲区读取（读取器）。写入器和读取器为不同的任务或中断是安全的，
或中断，但与其他 FreeRTOS 对象不同，
拥有多个不同的编写器或多个不同的读取器是不安全的。如果有
多个不同的编写器，则应用程序编写者必须将每次调用
在临界区内写入 API 函数（如 xMessageBufferSend()），并使用发送阻塞时间 0。
同样，如果有多个不同的读取器，则应用程序
编写者必须将每次调用读取 API 函数（如 xMessageBufferRead()）
放在临界区中，并使用接收阻塞时间 0。

使用 xMessageBufferSend() 从任务写入消息缓冲区。 
使用 [xMessageBufferSendFromISR()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/04-xMessageBufferSendFromISR) 从中断服务程序 (ISR) 向消息缓冲区写入消息
。

通过将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  要将消息发送到的消息缓冲区的句柄。

- *pvTxData*

  指向要复制到信息缓冲区的消息的指针。

- *xDataLengthBytes*

  消息长度。也就是从 pvTxData 复制到消息缓冲区的字节数。当
  消息写入消息缓冲区时，同时也会写入额外的 sizeof( size_t ) 字节
  以存储消息的长度。sizeof( size_t ) 在 32 位架构上通常为 4 字节，
  因此在大部分 32 位架构上将 xDataLengthBytes 设置为 20 时，会将消息缓冲区中的可用空间减少 24 字节
  （20 字节的消息数据和 4 字节用来保存消息长度）。

- *xTicksToWait*

  xTicksToWait 在调用 xMessageBufferSend() 时，
  如果消息缓冲区空间不足，
  调用任务应在阻塞状态下等待消息缓冲区有足够可用空间的最长时间。如果 xTicksToWait 为零，则调用任务将永远不会阻塞。阻塞时间
  的单位为滴答周期，因此，它代表的绝对时间取决于滴答频率。宏
  pdMS_TO_TICKS() 可用于将以毫秒为单位的时间转换为以滴答为单位的时间。
  将 xTicksToWait 设置为 portMAX_DELAY 将导致任务无限期等待（无超时），前提是
  INCLUDE_vTaskSuspend 在 FreeRTOSConfig.h 中设置为 1。任务处于“阻塞”状态时不会占用任何 CPU 时间
  。


**返回：** 

写入消息缓冲区的字节数。如果调用
xMessageBufferSend() 在有足够的空间将消息写入消息缓冲区之前超时，
则返回零。如果调用未
超时，则返回 xDataLength 字节。


**用法示例：**

```c
void vAFunction( MessageBufferHandle_t xMessageBuffer )
{
size_t xBytesSent;
uint8_t ucArrayToSend[] = { 0, 1, 2, 3 };
char *pcStringToSend = "String to send";
const TickType_t x100ms = pdMS_TO_TICKS( 100 );

    /* Send an array to the message buffer, blocking for a maximum of 100ms to
       wait for enough space to be available in the message buffer. */
    xBytesSent = xMessageBufferSend( xMessageBuffer,
                                     ( void * ) ucArrayToSend,
                                     sizeof( ucArrayToSend ),
                                     x100ms );

    if( xBytesSent != sizeof( ucArrayToSend ) )
    {
        /* The call to xMessageBufferSend() times out before there was enough
           space in the buffer for the data to be written. */
    }

    /* Send the string to the message buffer. Return immediately if there is
       not enough space in the buffer. */
    xBytesSent = xMessageBufferSend( xMessageBuffer,
                                    ( void * ) pcStringToSend,
                                    strlen( pcStringToSend ), 0 );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* The string could not be added to the message buffer because there was
           not enough free space in the buffer. */
    }
}
```
