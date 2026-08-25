---
title: "xStreamBufferCreate, xStreamBufferCreateWithCallback"
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
StreamBufferHandle_t xStreamBufferCreate( size_t xBufferSizeBytes,
                                           size_t xTriggerLevelBytes );

StreamBufferHandle_t xStreamBufferCreateWithCallback( 
                         size_t xBufferSizeBytes,
                         size_t xTriggerLevelBytes
                         StreamBufferCallbackFunction_t pxSendCompletedCallback,
                         StreamBufferCallbackFunction_t pxReceiveCompletedCallback );
```

创建一个使用动态分配内存的新[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)。 
流缓冲区会在每次发送和接收操作完成后执行回调。使用 
xStreamBufferCreate() API 创建的流缓冲区共享相同的发送和接收完成回调函数， 
这些函数使用 sbSEND_COMPLETED() 和 sbRECEIVE_COMPLETED() 宏定义。使用 
xStreamBufferCreateWithCallback() API 创建的流缓冲区可以拥有各自独特的发送和接收完成 
回调函数。请参阅 [xStreamBufferCreateStatic() and xStreamBufferCreateStaticWithCallback()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/02-xStreamBufferCreateStatic) 
获取使用静态分配内存（在编译时分配的内存）的相应版本。

[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 必须在 
FreeRTOSConfig.h 中设置为 1 或未定义，xStreamBufferCreate () 才可用。 
此外，[configUSE_SB_COMPLETED_CALLBACK](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_sb_completed_callback) 必须在 
FreeRTOSConfig.h 中设置为 1，xStreamBufferCreateWithCallback() 才可用。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中即可启用流缓冲区功能。


**参数：**

+ *xBufferSizeBytes*

  流缓冲区在任何时候能够容纳的总字节数。

+ *xTriggerLevelBytes*

  在流缓冲区中被阻塞以等待数据的任务离开阻塞状态之前， 
  流缓冲区中必须包含的字节数。例如，如果一个任务 
  在读取触发等级为 1 的空流缓冲区时被阻塞，那么当单个字节写入缓冲区或该任务的阻塞时间到期时， 
  该任务将被解除阻塞。另一个示例是，如果一个任务 
  在读取触发等级为 10 的空流缓冲区时被阻塞， 
  那么直到流缓冲区至少包含 10 个字节或该任务的阻塞时间结束，该任务才会被解除阻塞。如果读任务的阻塞时间 
  在达到触发等级之前过期，那么该任务仍将接收实际可用的字节数。 
  将触发等级设置为 0 将导致使用触发等级 1。指定 
   一个大于缓冲区大小的触发等级是无效的。

+ *pxSendCompletedCallback*

  当对流缓冲区的数据写入导致缓冲区的字节数超过触发等级时调用的回调函数 
  。如果参数为 NULL，则使用 sbSEND_COMPLETED 宏所提供的默认实现 
  。发送完成的回调函数必须具有 
  StreamBufferCallbackFunction_t 定义的原型，即：

  ```c
  void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                              BaseType_t xIsInsideISR,  
                              BaseType_t * const pxHigherPriorityTaskWoken );  
  ```

+ *pxReceiveCompletedCallback*

  当从流缓冲区读取数据（多于 0 字节）时调用的回调函数。如果 
  参数为 NULL，则使用 sbRECEIVE_COMPLETED 宏所提供的默认实现。接收 
  完成的回调函数必须具有 StreamBufferCallbackFunction_t 定义的原型， 
  即：

  ```c
  void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                                 BaseType_t xIsInsideISR,  
                                 BaseType_t * const pxHigherPriorityTaskWoken );  
  ```


**返回：**

如果返回 NULL，则说明因为没有足够的堆内存可供 
FreeRTOS 分配流缓冲区的数据结构体和存储区域，所以流缓冲区无法被创建。如果返回非 NULL 值， 
则表示流缓冲区已成功创建， 
返回值应该作为所创建流缓冲区的句柄来存储。


**用法示例：**

```c
void vSendCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                            BaseType_t xIsInsideISR,  
                            BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when a data write operation  
     * to the stream buffer causes the number of bytes in the buffer  
     * to be more then the trigger level.  

     * This is useful when a stream buffer is used to pass data between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xStreamBufferSendCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting for the data. */  
}  

void vReceiveCallbackFunction( StreamBufferHandle_t xStreamBuffer,  
                               BaseType_t xIsInsideISR,  
                               BaseType_t * const pxHigherPriorityTaskWoken )  
{  
    /* Insert code here which is invoked when data is read from a stream  
     * buffer.  

     * This is useful when a stream buffer is used to pass data between  
     * cores on a multicore processor. In that scenario, this callback  
     * can be implemented to generate an interrupt in the other CPU core,  
     * and the interrupt's service routine can then use the  
     * xStreamBufferReceiveCompletedFromISR() API function to check, and if  
     * necessary unblock, a task that was waiting to send the data. */  
}  

void vAFunction( void )  
{  
StreamBufferHandle_t xStreamBuffer, xStreamBufferWithCallback;  
const size_t xStreamBufferSizeBytes = 100, xTriggerLevel = 10;  
  
    /* Create a stream buffer that can hold 100 bytes and uses the  
     * functions defined using the sbSEND_COMPLETED() and  
     * sbRECEIVE_COMPLETED() macros as send and receive completed  
     * callback functions. The memory used to hold both the stream  
     * buffer structure and the data in the stream buffer is  
     * allocated dynamically. */  
    xStreamBuffer = xStreamBufferCreate( xStreamBufferSizeBytes,  
                                         xTriggerLevel );  

    if( xStreamBuffer == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
           stream buffer. */  
    }  
    else  
    {  
        /* The stream buffer was created successfully and can now be used. */  
    }  
      
    /* Create a stream buffer that can hold 100 bytes and uses the  
     * functions vSendCallbackFunction and vReceiveCallbackFunction  
     * as send and receive completed callback functions. The memory  
     * used to hold both the stream buffer structure and the data  
     * in the stream buffer is allocated dynamically. */  
    xStreamBufferWithCallback = xStreamBufferCreateWithCallback(   
                                    xStreamBufferSizeBytes,  
                                    xTriggerLevel,  
                                    vSendCallbackFunction,  
                                    vReceiveCallbackFunction );  

    if( xStreamBufferWithCallback == NULL )  
    {  
        /* There was not enough heap memory space available to create the  
         * stream buffer. */  
    }  
    else  
    {  
        /* The stream buffer was created successfully and can now be used. */  
    }  
}  
```
