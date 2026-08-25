---
title: "xStreamBatchingBufferCreateStatic() / xStreamBatchingBufferCreateStaticWithCallback()"
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
StreamBufferHandle_t xStreamBatchingBufferCreateStatic( size_t xBufferSizeBytes,
                                                        size_t xTriggerLevelBytes,
                                                        uint8_t *pucStreamBufferStorageArea,
                                                        StaticStreamBuffer_t *pxStaticStreamBuffer );

StreamBufferHandle_t xStreamBatchingBufferCreateStaticWithCallback(
                                    size_t xBufferSizeBytes,
                                    size_t xTriggerLevelBytes,
                                    uint8_t *pucStreamBufferStorageArea,
                                    StaticStreamBuffer_t *pxStaticStreamBuffer,
                                    StreamBufferCallbackFunction_t pxSendCompletedCallback,
                                    StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

使用静态分配的内存创建一个新的流批处理缓冲区。 
请参阅 [xStreamBatchingBufferCreate()](18-xStreamBatchingBufferCreate) 了解使用动态分配内存的版本 
。

`configSUPPORT_STATIC_ALLOCATION` 必须在 FreeRTOSConfig.h 中设置为 1，`xStreamBatchingBufferCreateStatic()` 
才可用。`configUSE_STREAM_BUFFERS` 必须在 FreeRTOSConfig.h 中设置为 1， 
`xStreamBatchingBufferCreateStatic()` 才可用。此外，`configUSE_SB_COMPLETED_CALLBACK` 
必须在 FreeRTOSConfig.h 中设置为1，`xStreamBatchingBufferCreateStaticWithCallback()` 才可用。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中即可启用流缓冲区功能。

流缓冲区和流批处理缓冲区的区别在于， 
当任务在非空缓冲区上执行读取时：

+ 从非空流缓冲区读取数据的任务会立即返回， 
  无论缓冲区中的数据量有多少。

+ 从非空流批处理缓冲区中读取的任务会阻塞， 
  直到缓冲区中的数据量超过触发水平或阻塞时间结束。


**参数：**

+ `xBufferSizeBytes`

  pucStreamBufferStorageArea 参数所指向的缓冲区的大小（单位：字节）。

+ `xTriggerLevelBytes`

  为了在阻塞时间结束前解除对调用 
  `xStreamBufferReceive` 的任务的阻塞，流批处理缓冲区中必须含有的字节数。

+ `pucStreamBufferStorageArea`

  必须指向一个大小至少为 `xBufferSizeBytes` 的 `uint8_t` 数组。这是一个数组， 
  当将流写入流批处理缓冲区时，流会被复制到这个数组中。

+ `pxStaticStreamBuffer`

  必须指向一个 `StaticStreamBuffer_t` 类型的变量，它将用于保存流批处理缓冲区的 
  数据结构体。

+ `pxSendCompletedCallback`

  当至少等于触发水平的字节数被发送到流批处理缓冲区时调用的回调 
  。如果参数为 NULL，则使用 
  由 `sbSEND_COMPLETED` 宏提供的默认实现。要启用回调，`configUSE_SB_COMPLETED_CALLBACK` 必须 
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

+ 如果流批处理缓冲区创建成功，则返回已创建流批处理缓冲区的句柄 
  。 

+ 如果 `ppucStreamBufferStorageArea` 或 `ppxStaticStreamBuffer` 为 NULL，则返回 NULL。


**用法示例：**

```c
// Used to dimension the array used to hold the streams.  The available space
// will actually be one less than this, so 999.
#define STORAGE_SIZE_BYTES 1000

// Defines the memory that will actually hold the streams within the stream
// batching buffer.
static uint8_t ucStorageBuffer[ STORAGE_SIZE_BYTES ];

// The variable used to hold the stream batching buffer structure.
StaticStreamBuffer_t xStreamBufferStruct;

void MyFunction( void )
{
StreamBufferHandle_t xStreamBatchingBuffer;
const size_t xTriggerLevel = 1;

    xStreamBatchingBuffer = xStreamBatchingBufferCreateStatic( sizeof( ucStorageBuffer ),
                                                               xTriggerLevel,
                                                               ucStorageBuffer,
                                                               &xStreamBufferStruct );

    // As neither the pucStreamBufferStorageArea or pxStaticStreamBuffer
    // parameters were NULL, xStreamBatchingBuffer will not be NULL, and can be
    // used to reference the created stream batching buffer in other stream
    // buffer API calls.

    // Other code that uses the stream batching buffer can go here.
}
```

