---
title: xStreamBufferReceive()
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
size_t xStreamBufferReceive( StreamBufferHandle_t xStreamBuffer,
                             void *pvRxData,
                             size_t xBufferLengthBytes,
                             TickType_t xTicksToWait );
```


从[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)接收字节。

**注意**：与其他 FreeRTOS 对象都不同的是，流缓冲区的实现
（消息缓冲区的实现也是如此，因为消息缓冲区是建立在流缓冲区之上的）
假定只有一个任务或中断将写入
缓冲区（写入器），只有一个任务或中断会从
缓冲区读取（读取器）。写入和读取
不同的任务或中断是安全的，但与其他FreeRTOS对象不同，
有多个不同的写入或多个不同的读取是不安全的。如果
有多个不同的写入器，
那么应用程序写入器必须把对写入 API 函数（如 xStreamBufferSend()）的每个调用放在一个临界区内，
并使用发送阻塞时间 0。同样，如果有多个不同的读取器，
那么应用程序必须把对读取 API 函数（如 xStreamBufferReceive()）的每个调用放在一个临界区内，
并使用接收阻塞时间 0。

使用 xStreamBufferReceive() 从任务的流缓冲区读取数据。使用
xStreamBufferReceiveFromISR() 从
中断服务程序 (ISR) 的流缓冲区读取数据。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  要接收字节来自的流缓冲区的句柄。  

+ *pvRxData* 

  指向缓冲区的指针，接收的字节将被复制到该缓冲区。

+ *xBufferLengthBytes* 

  pvRxData 参数<br /> 所指向的缓冲区的长度。这会设置一次调用中 
  可接收的最大字节数。xStreamBufferReceive 将返回尽可能多的字节数， 
  最大值由 xBufferLengthBytes 设置。

+ *xTicksToWait* 

  如果流缓冲区为空， 
  任务应保持阻塞状态等待数据可用的最长时间。如果 xTicksToWait 为零， 
  xStreamBufferReceive() 将立即返回。阻塞时间的单位为滴答周期，因此，它代表的绝对时间取决于 
  滴答频率。pdMS_TO_TICKS() 可用于将以毫秒为单位的时间 
  转换为以滴答为单位的时间。将 xTicksToWait 设置为 portMAX_DELAY 将 
  导致任务无限期等待（不超时），前提是 INCLUDE_vTaskSuspend 在 FreeRTOSConfig.h 中设置为 1。任务 
  处于“阻塞”状态时不会占用任何 CPU 时间。


**返回：** 

从流缓冲区读取的字节数。这将为最多等于 
xBufferLengthBytes 的可用字节数。例如：

* 如果触发等级为 1（触发等级是[在创建流缓冲区时设置的](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate)）-

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 5 个字节， 
      则 xStreamBufferReceive() 不会阻塞，从缓冲区中读取 5 个字节，并返回 5。

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 50 个字节， 
      则 xStreamBufferReceive() 不会阻塞，从缓冲区中读取 10 个字节，并返回 10。

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 0 个字节， 
      xTicksToWait 为 100，且在 50 个滴答后缓冲区接收到 5 个字节，那么 xStreamBufferReceive() 
      将进入阻塞状态 50 个滴答（即直到数据到达缓冲区）， 
      之后将从缓冲区读取 5 个字节，并返回 5。

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 0 个字节， 
      xTicksToWait 为 100，且在 100 个滴答后缓冲区没有接收到任何字节，那么 xStreamBufferReceive() 
      将在 100 个滴答的整个阻塞时间内进入阻塞状态，之后返回 0。

* 如果触发等级为 6 -

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 0 个字节， 
      xTicksToWait 为 100，且在 50 个滴答后缓冲区接收到 10 个字节，那么 xStreamBufferReceive() 
      将进入阻塞状态，持续 50 个滴答（即直到缓冲区中至少到达触发等级的字节数）， 
      之后将从缓冲区中读取 10 个字节，并返回 10。

	+如果 xBufferLengthBytes 为 10，且在调用 xStreamBufferReceive() 时，流缓冲区中包含 0 个字节， 
      xTicksToWait 为 100，且在 50 个滴答后缓冲区接收到 5 个字节，那么 xStreamBufferReceive() 
      将在整个 100 个滴答块期间保持阻塞（因为缓冲区中的数据量从未达到触发等级）， 
      之后将从缓冲区读取 5 个字节，并返回 5。


**用法示例：**

```c
void vAFunction( StreamBuffer_t xStreamBuffer )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
const TickType_t xBlockTime = pdMS_TO_TICKS( 20 );

    /* Receive up to another sizeof( ucRxData ) bytes from the stream buffer.
       Wait in the Blocked state (so not using any CPU processing time) for a
       maximum of 100ms for the full sizeof( ucRxData ) number of bytes to be
       available. */
    xReceivedBytes = xStreamBufferReceive( xStreamBuffer,
                                           ( void * ) ucRxData,
                                           sizeof( ucRxData ),
                                           xBlockTime );

    if( xReceivedBytes > 0 )
    {
        /* A ucRxData contains another xRecievedBytes bytes of data, which can
           be processed here.... */
    }
}
```
