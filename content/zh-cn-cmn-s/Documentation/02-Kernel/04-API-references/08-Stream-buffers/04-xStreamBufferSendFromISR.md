---
title: xStreamBufferSendFromISR()
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
size_t xStreamBufferSendFromISR( StreamBufferHandle_t xStreamBuffer,
                                 const void *pvTxData,
                                 size_t xDataLengthBytes,
                                 BaseType_t *pxHigherPriorityTaskWoken );
```

向
[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)发送字节流的中断安全版本 API 函数。

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

+ *pxHigherPriorityTaskWoken* 

  （这是一个可选参数，可以设置为 NULL。）流缓冲区上可能会有一个任务被阻塞， 
  以等待数据。xStreamBufferSendFromISR() 可以使数据可用， 
  进而导致正在等待数据的任务离开阻塞状态。如果调用 xStreamBufferSendFromISR() 
  会导致任务离开阻塞状态， 
  且未阻塞任务的优先级高于当前执行的任务（被中断的任务），则 xStreamBufferSendFromISR() 
  将在内部把 \*pxHigherPriorityTaskWoken 设置为 pdTRUE。xStreamBufferSendFromSISR() 将此值设置为 pdTRUE，那么通常应在 
  退出中断之前执行上下文切换。这将确保 
  中断直接返回最高优先级的就绪状态任务。在将 \*pxHigherPriorityTaskWoken 传递给函数之前， 
  应将其设置为 pdFALSE。有关示例，请参阅下面的示例代码。


**返回：** 

写入流缓冲区的字节数。


**用法示例：**

```c
/* A stream buffer that has already been created. */
StreamBufferHandle_t xStreamBuffer;

void vAnInterruptServiceRoutine( void )
{
size_t xBytesSent;
char *pcStringToSend = "String to send";
BaseType_t xHigherPriorityTaskWoken = pdFALSE; /* Initialised to pdFALSE. */

    /* Attempt to send the string to the stream buffer. */
    xBytesSent = xStreamBufferSendFromISR( xStreamBuffer,
                                           ( void * ) pcStringToSend,
                                           strlen( pcStringToSend ),
                                           &xHigherPriorityTaskWoken );

    if( xBytesSent != strlen( pcStringToSend ) )
    {
        /* There was not enough free space in the stream buffer for the entire
           string to be written, ut xBytesSent bytes were written. */
    }

    /* If xHigherPriorityTaskWoken was set to pdTRUE inside
       xStreamBufferSendFromISR() then a task that has a priority above the
       priority of the currently executing task was unblocked and a context
       switch should be performed to ensure the ISR returns to the unblocked
       task. In most FreeRTOS ports this is done by simply passing
       xHigherPriorityTaskWoken into taskYIELD_FROM_ISR(), which will test the
       variables value, and perform the context switch if necessary. Check the
       documentation for the port in use for port specific instructions. */
    taskYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
