---
title: "FreeRTOS_write()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO API](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions)]

FreeRTOS_IO.h


```c
size_t FreeRTOS_write( Peripheral_Descriptor_t const pxPeripheral,
                       const void *pvBuffer,
                       const size_t xBytes );

```

将一个或多个字节写入打开的外围设备。

[板级支持包](Board_Support_Packages)
明确规定了可以打开的外围设备。 [FreeRTOS_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl)
用于在中断驱动模式和轮询写入模式之间进行选择。


**参数：**

+ *pxPeripheral*

  与要写入字节的外围设备相关联的描述符。该描述符将
  将在调用 [FreeRTOS_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open) 以打开外围设备时返回。

+ *pvBuffer*

  指向待写入数据的第一个字节的指针。

+ *xBytes*

  待写入的字节总数。

  使用中断驱动的[传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)时，
  如果在外围设备的写入超时过期之前无法写入所有字节，
  则实际写入外围设备的字节数可能少于请求的字节数。可以使用 [FreeRTOS_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl)
  设置写入超时值。


**返回：**

使用[轮询传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)时，
返回值为
实际写入外围设备的总字节数。假定未发生错误，
这就是所请求的总字节数。

当使用中断驱动的[字符队列传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)时，
返回值为实际写入写队列的
总字节数。如果队列中
没有足够空间用于立即写入所有待写字节，
并且外围设备的写入超时
在获取到足够空间之前已过期，则这将小于请求的字节数。实际数据传输
由
FreeRTOS-Plus-IO 中断服务程序控制，
返回对 FreeRTOS_write() 的调用后即可完成。

使用中断驱动的[零拷贝传输模式时](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)，
则：

* 如果调用 FreeRTOS_write() 的任务保存了写互斥锁
  则返回值为待传输的总字节数，
  此时假定未发生错误。实际数据传输
  由FreeRTOS-Plus-IO 中断服务程序控制，
  返回对 FreeRTOS_write() 的调用后即可完成。

* 如果调用 FreeRTOS_write() 的任务未保存写
  互斥锁，或者如果 [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) 未配置为包含
  外围设备的零拷贝写入传输模式，
  同时返回零。

[FreeRTOS_ioctl()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) 用于设置写入超时值。


**用法示例：**

示例 1 的代码片段展示了当外围设备
被配置为[轮询传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)时如何执行写入。外围设备
在打开时默认采用轮询模式。

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

示例 2 的代码片段展示了当外围设备
被配置为中断驱动的[字符队列传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)时如何执行写入。
在此模式下，调用 FreeRTOS_write() 的任务将处于[阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)状态
（不占用任何 CPU 时间），直到请求的
字节数全部发送到队列，或者写入超时过期。FreeRTOS_ioctl()
与 [ioctlSET_TX_TIMEOUT](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/05-FreeRTOS_ioctl) 请求代码一起使用，以配置
写入超时，与 ioctlWAIT_PREVIOUS_WRITE_COMPLETE 请求代码一起使用，
以等待写入队列完全清空。

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
*示例 2：向配置为使用中断驱动字符队列传输模式的外围设备写入字节。*


示例 3 的代码片段展示了当外围设备
被配置为中断驱动的[零拷贝传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)时如何执行写入。
在此模式下，调用 FreeRTOS_write() 的任务始终会
立即返回。如果返回值等于待写入字节数，
则表示 FreeRTOS_write() 调用成功启动了
中断驱动的传输。如果返回值为零，则表示
FreeRTOS_write() 调用无法启动传输，
可能是因为没有保存写入互斥锁，也可能是因为 [FreeRTOSIOConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/06-FreeRTOS_Plus_IO_Configuration) 未配置为支持此模式。

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
*示例 3：向配置为使用中断驱动零拷贝传输模式的外围设备写入字节。*

