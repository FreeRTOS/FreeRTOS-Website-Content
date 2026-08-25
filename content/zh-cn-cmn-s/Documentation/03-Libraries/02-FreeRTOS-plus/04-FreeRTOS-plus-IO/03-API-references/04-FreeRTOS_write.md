---
title: FreeRTOS_write()
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
size_t FreeRTOS_write( Peripheral_Descriptor_t const pxPeripheral,
                       const void *pvBuffer,
                       const size_t xBytes );
```

将一个或多个字节写入打开的外围设备。

[板级支持包](Board_Support_Packages)定义了可打开的外围设备。
[FreeRTOS_ioctl()](FreeRTOS_ioctl) 用于在中断驱动写入模式和轮询写入模式之间进行选择
。

**参数：**

- *pxPeripheral*

  与要写入字节的外围设备相关联的描述符。此描述符
  将在调用 [FreeRTOS_open()](FreeRTOS_open) 以打开外围设备时返回。

- *pvBuffer*

  指向待写入数据的第一个字节的指针。

- *xBytes*

  待写入的字节总数。使用中断驱动的[传输模式](FreeRTOS_IO_Transfer_Modes)时，
  如果在外围设备写入超时前无法写入所有字节，
  则写入外围设备的实际字节数可能少于请求的字节数。
  [FreeRTOS_ioctl()](FreeRTOS_ioctl) 用于设置写入超时值。

**返回：**

- 当使用[轮询传输模式](Polled_Transfer_Mode)时，返回值为
  实际写入外围设备的总字节数。假定未发生错误，
  这将是申请的总数。

- 当使用中断驱动的[字符队列传输模式](Character_Queue_Transfer_Mode)时，
  返回值为实际写入写入队列的字节总数。如果队列中没有足够的空间立即写入所有字节，
  并且外围设备的写超时在足够的空间出现之前就已结束，
  则写入的字节数将少于请求的字节数。
  字节的实际传输由 FreeRTOS-Plus-IO 中断服务程序控制，
  能在 FreeRTOS_write() 调用返回后才完成。

- 当使用中断驱动的[零拷贝传输模式](Zero_Copy_Transfer_Mode)时，

  - 如果调用 FreeRTOS_write() 的任务含有写入互斥锁，假定未发生错误，
    则返回值将是要传输的总字节数。实际数据传输由
    FreeRTOS-Plus-IO 中断服务程序控制，可能在调用 FreeRTOS_write() 返回后才完成
    。

  - 如果调用 FreeRTOS_write() 的任务不含写入互斥锁，
    或者 [FreeRTOSIOConfig.h](FreeRTOS_Plus_IO_Configuration) 未配置为包含针对
    外围设备的零拷贝写入传输模式，则返回零。

[FreeRTOS_ioctl()](FreeRTOS_ioctl) 用于设置写入超时值。


**用法示例：**

示例 1 的代码片段展示了当外围设备配置为
使用[轮询传输模式时](FreeRTOS_IO_Transfer_Modes)，如何执行写入操作。外围设备打开时
默认为轮询模式。

```c
/* By default the port is opened in polled mode. Write some bytes in polled
   mode. */
xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );


/* The port is currently in polled mode, so FreeRTOS_write() will only have
   returned once all the requested bytes had been written (barring any errors on
   the peripheral). Note that because polling mode is being used, the task
   making the FreeRTOS_write() call will not have entered the Blocked
   state during the write process. The bytes written to the peripheral come from
   the ucBuffer buffer. */
configASSERT( xBytes == sizeof( ucBuffer ) );
```
*示例 1：向配置为使用轮询传输模式的外围设备写入字节。*

示例 2 的代码片段展示了当外围设备配置为
中断驱动的[字符队列传输模式](FreeRTOS_IO_Transfer_Modes)时，如何执行写入操作。在此模式下，
执行 FreeRTOS_write() 调用的任务会保持在 
[阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)
状态（不占用任何 CPU 时间） ，直到请求的所有字节数
全部发送到队列，或者写入超时结束。FreeRTOS_ioctl() 与
[ioctlSET_TX_TIMEOUT](FreeRTOS_ioctl) 请求代码配合使用，可配置写入超时，
而 ioctlWAIT_PREVIOUS_WRITE_COMPLETE 请求代码则用于等待写入队列为空。

```c
/* Write some bytes in interrupt driven character queue Tx mode. */
xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );

if( xBytesWritten < sizeof( ucBuffer ) )
{
    /* The Tx timeout must have expired before sizeof( ucBuffer ) bytes could
       be written to the write queue. */
}
else
{
    /* The requested number of bytes were sent to the write queue before
       the write timeout expired. */
}
```
*例 2：向配置为使用中断驱动字符队列
传输模式的外围设备写入字节。*

示例 3 的代码片段展示了当外围设备配置为
使用中断驱动的[零拷贝传输模式](FreeRTOS_IO_Transfer_Modes)时，如何执行写入操作。在此模式下，
调用 FreeRTOS_write() 的任务总是立即返回。如果返回值等于待写入字节数，
则 FreeRTOS_write() 调用成功启动了
中断驱动传输。如果返回值等于零，则 FreeRTOS_write() 调用无法启动传输，
原因可能是它不含写入互斥锁，或者是
[FreeRTOSIOConfig.h](FreeRTOS_Plus_IO_Configuration) 未配置为对其提供支持。

```c
/* As zero copy Tx is being used, a mutex must be obtained before a write can
   be requested. This call requests the mutex, and will wait a maximum of 50
   milliseconds for the mutex to be obtained. FreeRTOS_ioctl() will return pdPASS
   or pdFAIL. */
xMutexObtained = FreeRTOS_ioctl( xPort,
                                 ioctlOBTAIN_WRITE_MUTEX,
                                 ( void * ) ( 50 / portTICK_PERIOD_MS ) );

if( xMutexObtained != pdFAIL )
{
    /* The mutex was obtained, so a write can be performed. This
       time bytes are written directly from ucBuffer. */
    xBytesWritten = FreeRTOS_write( xPort, ucBuffer, sizeof( ucBuffer ) );

    /* Interrupt driven zero copy Tx is being used, so FreeRTOS_write() should
       return the number of requested bytes, even though the FreeRTOS-Plus-IO interrupt
       service routine might still be sending the data. */
    configASSERT( xBytesWritten == sizeof( ucBuffer ) );

    /* The mutex will only be available again after all the data has been
       transmitted by the peripheral. Attempting to obtain the mutex again is therefore
       a good way of knowing when all the data has been sent, and when the buffer being
       written can be updated without corrupting the data transmission. The FreeRTOS_ioctl()
       ioctlWAIT_PREVIOUS_WRITE_COMPLETE and ioctlOBTAIN_WRITE_MUTEX can both
       be used for this purpose - the difference between the two being that
       ioctlWAIT_PREVIOUS_WRITE_COMPLETE will not result in the calling task holding
       the mutex if the FreeRTOS_ioctl() call is successful. */
    xMutexObtained = FreeRTOS_ioctl( xPort,
                                     ioctlOBTAIN_WRITE_MUTEX,
                                     ( void * ) ( 50 / portTICK_PERIOD_MS ) );
    /* Or xMutexObtained = FreeRTOS_ioctl( xPort,
                                           ioctlWAIT_PREVIOUS_WRITE_COMPLETE,
                                           ( void * ) ( 50 / portTICK_PERIOD_MS ) ); */

    if( xMutexObtained != pdFAIL )
    {
        /* If another write is going to be performed, it can be performed now,
           as the write mutex is already held. If a write is not going to be
           performed, and another task uses the same peripheral, then the mutex
           should be returned, and ioctlWAIT_PREVIOUS_WRITE_COMPLETE would have been
           a better request code to use. The second parameter is not used in the
           following call. */
        FreeRTOS_ioctl( xPort, ioctlRELEASE_WRITE_MUTEX, NULL );
    }
}
```
*例 3：向配置为使用中断  
驱动零拷贝传输模式的外围设备写入字节。*

