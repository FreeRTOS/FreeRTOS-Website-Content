---
title: xStreamBufferReceiveFromISR()
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
size_t xStreamBufferReceiveFromISR( StreamBufferHandle_t xStreamBuffer,
                                    void *pvRxData,
                                    size_t xBufferLengthBytes,
                                    BaseType_t *pxHigherPriorityTaskWoken );
```

一个从
[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)中接收字节的 API 函数的中断安全版本。

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
那么应用程序写入器必须把对读取 API 函数（如 xStreamBufferReceive()）的每个调用放在一个临界区内，
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

  由 pvRxData 参数指向的缓冲区的长度。这会设置一次调用中 
  可接收的最大字节数。xStreamBufferReceive 将返回尽可能多的字节数， 
  最大值由 xBufferLengthBytes 设置。

+ *pxHigherPriorityTaskWoken* 

  （这是一个可选参数，可以设置为 NULL。）流缓冲区上可能会有一个任务被阻塞， 
  等待空间变为可用。调用 xStreamBufferReceiveFromISR() 可以 
  腾出空间，从而使正在等待空间的任务脱离阻塞状态。如果调用 
  xStreamBufferReceiveFromISR() 导致任务离开阻塞状态，并且 
  被解除阻塞的任务的优先级高于当前正在执行的任务（被中断的任务），那么 
  xStreamBufferReceiveFromISR() 将从内部把 \*pxHigherPriorityTaskWoken 设置为 pdTRUE。

  如果 xStreamBufferSendFromSISR() 将此值设置为 pdTRUE，那么通常应在 
  退出中断之前执行上下文切换。这将确保中断直接返回优先级最高的就绪状态任务。  
  在将 \*pxHigherPriorityTaskWoken 传递给函数之前， 
  应将其设置为 pdFALSE。有关示例，请参阅下面的代码示例。


**返回：** 

从流缓冲区读取的字节数（如有）。


**用法示例：**

```c
/* A stream buffer that has already been created. */
StreamBuffer_t xStreamBuffer;

void vAnInterruptServiceRoutine( void )
{
uint8_t ucRxData[ 20 ];
size_t xReceivedBytes;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;  /* Initialised to pdFALSE. */

    /* Receive the next stream from the stream buffer. */
    xReceivedBytes = xStreamBufferReceiveFromISR( xStreamBuffer,
                                                  ( void * ) ucRxData,
                                                  sizeof( ucRxData ),
                                                  &xHigherPriorityTaskWoken );

    if( xReceivedBytes > 0 )
    {
        /* ucRxData contains xReceivedBytes read from the stream buffer.
           Process the stream here.... */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xStreamBufferReceiveFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD_FROM_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```
