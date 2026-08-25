---
title: "xStreamBatchingBufferCreate() / xStreamBatchingBufferCreateWithCallback()"
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
StreamBufferHandle_t xStreamBatchingBufferCreate( size_t xBufferSizeBytes,
                                                  size_t xTriggerLevelBytes );

StreamBufferHandle_t xStreamBatchingBufferCreateWithCallback( 
                         size_t xBufferSizeBytes,
                         size_t xTriggerLevelBytes
                         StreamBufferCallbackFunction_t pxSendCompletedCallback,
                         StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

使用动态分配的内存创建新的流批处理缓冲区。 
请参阅 [xStreamBatchingBufferCreateStatic()](19-xStreamBatchingBufferCreateStatic) 
获取使用静态分配内存（在编译时分配的内存）的相应版本。

`configSUPPORT_DYNAMIC_ALLOCATION` 必须在 FreeRTOSConfig.h 中设置为 1 或未定义， 
`xStreamBatchingBufferCreate()` 才可用。`configUSE_STREAM_BUFFERS` 必须 
在 FreeRTOSConfig.h 中设置为 1，`xStreamBatchingBufferCreate()` 才可用。 
此外，`configUSE_SB_COMPLETED_CALLBACK` 必须在 FreeRTOSConfig.h 中设置为 1， 
`xStreamBatchingBufferCreateWithCallback()` 才可用。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中即可启用流缓冲区功能。

流缓冲区和流批处理缓冲区的区别在于， 
当任务在非空缓冲区上执行读取时：

+ 从非空流缓冲区读取数据的任务会立即返回， 
  无论缓冲区中的数据量有多少。

+ 从非空流批处理缓冲区中读取的任务会阻塞， 
  直到缓冲区中的数据量超过触发水平或阻塞时间结束。


**参数：**

+ `xBufferSizeBytes`

  流批处理缓冲区在任何时候能够容纳的总字节数。

+ `xTriggerLevelBytes`

  为了在阻塞时间结束前解除对调用 
  `xStreamBufferReceive` 的任务的阻塞，流批处理缓冲区中必须含有的字节数。

+ `pxSendCompletedCallback`

  当至少等于触发水平的字节数被发送到流批处理缓冲区时调用的回调 
  。如果参数为 NULL，则使用 
  `sbSEND_COMPLETED` 宏所提供的默认实现。要启用回调，`configUSE_SB_COMPLETED_CALLBACK` 必须 
  在 FreeRTOSConfig.h 中设置为 1。发送完成的回调函数必须具有 
  由 `StreamBufferCallbackFunction_t` 定义的原型，即：

  ```c
  void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,
                              BaseType_t xIsInsideISR,
                              BaseType_t * const pxHigherPriorityTaskWoken );
  ```

+ `pxReceiveCompletedCallback`

  从流批处理缓冲区读取的数据超过零字节数时调用的回调。如果参数 
  为 NULL，则将使用由 `sbRECEIVE_COMPLETED` 宏提供的默认实现。要启用 
  回调，`configUSE_SB_COMPLETED_CALLBACK` 必须在 FreeRTOSConfig.h 中设置为 1。接收完成 
  回调函数必须具有由 `StreamBufferCallbackFunction_t` 定义的原型，即：

  ```c
  void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,
                                 BaseType_t xIsInsideISR,
                                 BaseType_t * const pxHigherPriorityTaskWoken );
  ```


**返回：**

+ 如果返回 NULL，则说明因为没有足够的堆内存可供 
  FreeRTOS 分配流批处理缓冲区的数据结构体和存储区域，所以流批处理缓冲区无法被创建 
  。 

+ 返回非 NULL 值表示已成功创建流批处理缓冲区—— 
  返回值应存储为所创建流批处理缓存区的句柄。


**用法示例：**

```c
void vAFunction( void )
{
StreamBufferHandle_t xStreamBatchingBuffer;
const size_t xStreamBufferSizeBytes = 100, xTriggerLevel = 10;

    // Create a stream batching buffer that can hold 100 bytes.  The memory used
    // to hold both the stream batching buffer structure and the data in the stream
    // batching buffer is allocated dynamically.
    xStreamBatchingBuffer = xStreamBatchingBufferCreate( xStreamBufferSizeBytes, xTriggerLevel );

    if( xStreamBatchingBuffer == NULL )
    {
        // There was not enough heap memory space available to create the
        // stream batching buffer.
    }
    else
    {
        // The stream batching buffer was created successfully and can now be used.
    }
}
```

