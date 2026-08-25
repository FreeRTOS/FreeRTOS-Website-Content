---
title: FreeRTOS_ioctl()
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
BaseType_t FreeRTOS_ioctl( Peripheral_Descriptor_t const xPeripheral,
                           uint32_t ulRequest,
                           void *pvValue );
```

ioctl() 是输入输出控制（Input Output Control）的缩写，
是用于输入输出设备控制（包括设备特定配置）的函数的标准名称。FreeRTOS_ioctl() 相当于 FreeRTOS-Plus-IO。
调用 FreeRTOS_ioctl() 所要执行的操作由作为第二个参数传递给
FreeRTOS_ioctl() 的请求代码确定。


**参数：**

- *pxPeripheral*

  与 FreeRTOS_ioctl() 调用将影响到的外围设备有关的描述符。此描述符
  将在调用 [FreeRTOS_open()](FreeRTOS_open) 以打开外围设备时返回。

- *ulRequest*

  请求代码。通用请求代码[如下文所列](#请求代码参考)。板级支持
  包特定的请求代码随[板级支持包](Board_Support_Packages)
  文档一起提供。

- *pvValue*

  所使用请求代码的特定参数。例如，如果请求代码用于设置
  超时值，则此参数用于定义超时。许多请求代码
  不需要参数。在这种情况下，为了将来的兼容性，
  建议将 pvValue 设为 NULL。pvValue 是一个 void 指针，因此可以用来传递任何数据类型，
  无论是简单的整数值（转为 void \*），还是指向更复杂数据类型的指针。


**返回：**

- 如果请求代码已成功处理，返回 pdPASS。
- 其他情况则返回 pdFAIL。


**用法示例：**

所有这些代码示例都假定 pxPort 描述符已经打开并且有效。

示例 1 代码片段展示了如何配置外围设备以使用零拷贝传输
模式。该请求不使用 pvValue 参数，因此参数设置为 NULL。

```c
FreeRTOS_ioctl( pxPort, ioctlUSE_ZERO_COPY_TX, NULL );
```
*示例 1：将与 pxPort 描述符相关联的外围设备配置为*

示例 2 代码片段展示了如何配置外围设备的写超时。在这种情况下，
pvValue 参数用于传递超时值（单位：滴答）。常量 portTICK_PERIOD_MS 用于
将 200 毫秒转换为滴答数。

```c
FreeRTOS_ioctl( pxPort, ioctlSET_TX_TIMEOUT, ( void * ) ( 200 / portTICK_PERIOD_MS ) );
```
*示例 1：为与 pxPort 描述符相关联的外围设备配置写超时。*

示例 3 代码段展示了如何设置与 I2C 移植相关的从机地址。在这种情况下，
pvValue 参数用于传递要使用的从机地址，即 0x20。

```c
FreeRTOS_ioctl( pxPort, ioctlSET_I2C_SLAVE_ADDRESS, ( void * ) 0x20 );
```
*示例 1：使用 FreeRTOS_ioctl() 设置与 I2C 移植相关的从机地址。*


## 请求代码参考

### 用于设置待使用传输模式的请求代码

以下请求代码用于设置[传输模式](FreeRTOS_IO_Transfer_Modes)。
[板级支持包](Board_Support_Packages)文档详细描述了
各种外围设备适用的传输模式。

#### ioctlUSE_POLLED_TX

  配置外围设备，使其在写入字节时使用[轮询传输模式](Polled_Transfer_Mode)。

  所有外围设备在首次打开时都默认使用轮询传输模式。目前，
  很少有外围设备能在手动选择其他模式后
  返回轮询传输模式。

  **参数：** 未使用。

#### ioctlUSE_POLLED_RX

  配置外围设备，使其在读取字节时使用[轮询传输模式](Polled_Transfer_Mode)。

  所有外围设备在首次打开时都默认使用轮询传输模式。目前，
  很少有外围设备能在手动选择其他模式后
  返回轮询传输模式。

  **参数：** 未使用。

#### ioctlUSE_ZERO_COPY_TX

  配置外围设备，使其在写入字节时使用中断驱动的[零拷贝传输模式](Zero_Copy_Transfer_Mode)
  。

  该请求代码将启用外围设备的中断，并将外围设备的中断优先级设置为
  尽可能低的值。如有必要，可以使用 ioctlSET_INTERRUPT_PRIORITY 请求代码
  在必要时提高中断优先级。

  外围设备中断服务程序由 FreeRTOS-Plus-IO 代码提供，
  因此无需由应用程序代码实现。

  **参数：** 未使用。

#### ioctlUSE_CHARACTER_QUEUE_TX

  配置外围设备，使其在写入字节时使用中断驱动的[字符队列传输模式](Character_Queue_Transfer_Mode)  
  。

  该请求代码将启用外围设备的中断，并将外围设备的中断优先级设置为
  尽可能低的值。如有必要，可以使用 ioctlSET_INTERRUPT_PRIORITY 请求代码
  在必要时提高中断优先级。

  外围设备中断服务程序由 FreeRTOS-Plus-IO 代码提供，
  因此无需由应用程序实现。

  **参数：**用于保存等待
  FreeRTOS-Plus-IO 中断服务程序写入外围设备的字节的队列的长度（单位：字节）。该队列由
  FreeRTOS-Plus-IO 代码创建，无需由应用程序代码创建。

#### ioctlUSE_CHARACTER_QUEUE_RX

  配置外围设备，使其在读取字节时使用中断驱动的[字符队列传输模式](Character_Queue_Transfer_Mode)  
  。

  该请求代码将启用外围设备的中断，并将外围设备的中断优先级设置为
  尽可能低的值。如有必要，可以使用 ioctlSET_INTERRUPT_PRIORITY 请求代码
  在必要时提高中断优先级。

  外围设备中断服务程序由 FreeRTOS-Plus-IO 代码提供，
  因此无需由应用程序实现。

  **参数**：用于保存已接收
  但尚未通过调用 FreeRTOS_read() 返回的字节的队列的长度（单位：字节）。队列由 FreeRTOS-Plus-IO 代码创建，
  无需由应用程序代码创建。

#### ioctlUSE_CIRCULAR_BUFFER_RX

  配置外围设备，使其在读取字节时使用中断驱动的[循环缓冲区传输模式](Circular_Buffer_Transfer_Mode)
  。

  该请求代码将启用外围设备的中断，并将外围设备的中断优先级设置为
  尽可能低的值。如有必要，可以使用 ioctlSET_INTERRUPT_PRIORITY 请求代码
  在必要时提高中断优先级。

  外围设备中断服务程序由 FreeRTOS-Plus-IO 代码提供，
  因此无需由应用程序实现。

  **参数：**用于保存
  FreeRTOS-Plus-IO 中断服务程序接收到的字符，但尚未通过调用 FreeRTOS_read() 返回的循环缓冲区的长度（单位：字节）。循环缓冲区由
  FreeRTOS-Plus-IO 代码创建，
  因此无需由应用程序代码分配。


### 影响传输模式行为的请求代码

以下请求代码适用于一种或多种传输模式：

#### ioctlOBTAIN_WRITE_MUTEX

  该请求代码仅适用于
  外围设备使用中断驱动[零拷贝传输模式](Zero_Copy_Transfer_Mode)时。

  在使用零拷贝传输模式时，
  必须在调用 FreeRTOS_write() 之前获取外围设备的写入互斥锁。ioctlOBTAIN_WRITE_MUTEX 是一个用于获取互斥锁的请求。

  如果成功获得互斥锁，FreeRTOS_ioctl() 返回 pdPASS，其他情况下返回 pdFAIL。

  当写入所有字节后，FreeRTOS-Plus-IO 中断服务程序会自动释放互斥锁
  。因此，成功获得写入互斥锁也表明当前没有写入操作，
  正在写入的缓冲区已空闲，可以重新使用。

  如果互斥锁由任务获得，
  但任务没有调用 FreeRTOS_write()，则必须使用 ioctlRELEASE_WRITE_MUTEX 请求代码手动释放互斥锁。请参阅
  [ioctlWAIT_PREVIOUS_WRITE_COMPLETE](#ioctlwait_previous_write_complete) 了解替代方案。

  请参阅中断驱动[零拷贝写入传输模式文档页面](Zero_Copy_Transfer_Mode)上的示例代码。

  **参数：**调用任务在
  [阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) 
  状态下等待互斥锁可用的最长时间（单位：滴答）。

  常量 portTICK_PERIOD_MS 可用于将毫秒数转换为滴答数。例如，要等待 50 毫秒，
  则指定值 ( 50UL / portTICK_PERIOD_MS ) 即可。

#### ioctlWAIT_PREVIOUS_WRITE_COMPLETE

  该请求代码仅适用于
  外围设备使用中断驱动[零拷贝传输模式](Zero_Copy_Transfer_Mode)或
  中断驱动[字符队列传输模式](Character_Queue_Transfer_Mode)时。

  ioctlWAIT_PREVIOUS_WRITE_COMPLETE 可使调用任务
  保持在[阻塞](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/)状态， 
  直到当前写入操作完成。

  需要注意的是，每次只能从将一个任务移出阻塞状态。因此，
  如果两个任务同时在同一外围设备上使用 ioctlWAIT_PREVIOUS_WRITE_COMPLETE 请求代码，
  那么只有优先级最高的任务才能在传输完成后退出阻塞状态。

  请参阅中断驱动[零拷贝写入传输模式文档页面](Zero_Copy_Transfer_Mode)上的示例代码。

  **参数：**调用任务在阻塞状态下
  等待当前写入操作完成的最长时间（单位：滴答）。

  常量 portTICK_PERIOD_MS 可用于将毫秒数转换为滴答数。例如，要等待 50 毫秒，
  则指定值 ( 50UL / portTICK_PERIOD_MS ) 即可。

#### ioctlRELEASE_WRITE_MUTEX

  该请求代码仅适用于
  外围设备使用中断驱动[零拷贝传输模式](Zero_Copy_Transfer_Mode)时。

  在使用零拷贝传输模式时，
  必须在调用 FreeRTOS_write() 之前获取外围设备的写入互斥锁。当写入完成后，FreeRTOS-Plus-IO 中断服务程序
  将自动释放互斥锁。

  如果互斥锁由任务获得，
  但任务没有调用 FreeRTOS_write()，则必须使用 ioctlRELEASE_WRITE_MUTEX 请求代码手动释放互斥锁。另请参阅
  [ioctlWAIT_PREVIOUS_WRITE_COMPLETE](#ioctlwait_previous_write_complete) 和
  ioctlOBTAIN_WRITE_MUTEX 请求代码。

  **参数：** 未使用。

#### ioctlSET_TX_TIMEOUT

  该请求代码仅适用于
  外围设备使用中断驱动[字符队列传输模式](Character_Queue_Transfer_Mode)时。

  当使用字符队列传输模式时，FreeRTOS_write() 会将待写入的字节数据放置在
  一个队列中。如果队列中没有足够空间容纳所有字节，
  调用任务就会进入“阻塞”状态，等待更多可用空间。ioctlSET_TX_TIMEOUT
  设置任务处于阻塞状态的最长时间。FreeRTOS_write() 返回
  成功写入队列的字节数，如果写入超时到期，
  则返回的字节数将少于请求的字节数。

  **参数：**调用 FreeRTOS_write() 的任务
  在等待写入队列中有足够空间完成
  FreeRTOS_write() 操作时保持阻塞状态的最长时间（单位：滴答）。

  常量 portTICK_PERIOD_MS 可用于将毫秒数转换为滴答数。例如，
  要设置 50 毫秒的最长阻塞时间，则使用值 ( 50UL / portTICK_PERIOD_MS ) 即可。

#### ioctlSET_RX_TIMEOUT

  该请求代码仅适用于
  外围设备使用中断驱动[字符队列传输模式](Character_Queue_Transfer_Mode)
  或中断驱动[循环缓冲区传输模式](Circular_Buffer_Transfer_Mode)时。

  使用这些模式时，FreeRTOS_read() 会返回
  已被 FreeRTOS-Plus-IO 中断服务程序缓冲的字节（在队列或循环缓冲区中缓冲）。如果缓冲区尚未包含所请求的字节数，
  则调用 FreeRTOS_read() 的任务将处于“阻塞”状态，
  等待更多可用字节。ioctlSET_RX_TIMEOUT
  用于设置任务保持阻塞状态的最长时间。FreeRTOS_read() 返回的是成功读取的字节数，
  如果读取超时到期，
  此数目将少于请求的字节数。

  **参数：**调用 FreeRTOS_read() 的任务
  在等待完成 FreeRTOS_read() 操作时保持阻塞状态的最长时间（单位：滴答）。

  常量 portTICK_PERIOD_MS 可用于将毫秒数转换为滴答数。例如，
  要设置 50 毫秒的最长阻塞时间，则使用值 ( 50UL / portTICK_PERIOD_MS ) 即可。

#### ioctlCLEAR_RX_BUFFER

  该请求代码仅适用于
  外围设备使用中断驱动[字符队列传输模式](Character_Queue_Transfer_Mode)
  或中断驱动[循环缓冲区传输模式](Circular_Buffer_Transfer_Mode)时。使用这些模式时，
  FreeRTOS_read() 会返回已被
  FreeRTOS-Plus-IO 中断服务程序缓冲的字节（在队列或循环缓冲区中缓冲）。ioctlCLEAR_RX_BUFFER 请求代码将删除
  （并释放）缓冲区中已包含的字节，使缓冲区为空。

  **参数：** 未使用。


### 可影响多种外围设备行为的请求代码

此处列出的请求代码适用于多种外围设备类型。
[板级支持包](Board_Support_Packages)文档详细描述了
各种外围设备适用的请求代码。

#### ioctlSET_SPEED

  配置串行总线的速度。例如，如果外围设备是 UART，
  则该请求代码将设置 UART 波特率。该请求代码适用于大多数（如非全部）串行外围设备。

  **参数：**绝对总线速度。例如，使用 9600 将 UART 的波特率设为 9600，
  使用 200000 将 SPI 总线速度设置为 200000。

#### ioctlSET_INTERRUPT_PRIORITY

  设置由外围设备生成中断的优先级。

  请注意，对于所有 FreeRTOS 移植，如果其使用
  [configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel_priority)
  设置，则分配给中断的优先级必须等于或低于
  configMAX_SYSCALL_INTERRUPT_PRIORITY 定义的优先级。

  **参数：**中断优先级的绝对值。

  在 Cortex-M 设备上，
  必须使用 CMSIS NVIC_SetPriority() 函数预期的格式指定中断优先级。请记住，Cortex-M 设备使用数值较低的优先级值
  来表示高中断优先级。


### SPI 特定请求代码

#### ioctlSET_SPI_DATA_BITS

  设置 SPI 传输中使用的数据位数。

  **参数：**数据位的数量。例如，使用 8 来表示数据使用 8 位。

#### ioctlSET_SPI_CLOCK_PHASE

  设置 SPI 时钟的相位 (CPHA)。

  **参数：**有两个有效值。

  - boardSPI_SAMPLE_ON_LEADING_EDGE_CPHA_0：

    使用 boardSPI_SAMPLE_ON_LEADING_EDGE_CPHA_0 在时钟前沿捕获数据
    （无论其极性如何）。

    boardSPI_SAMPLE_ON_LEADING_EDGE_CPHA_0 等效于值为 0 的 CPHA。

  - boardSPI_SAMPLE_ON_TRAILING_EDGE_CPHA_1：

    使用 boardSPI_SAMPLE_ON_TRAILING_EDGE_CPHA_1 在时钟后沿捕获数据
    （无论其极性如何）。

    boardSPI_SAMPLE_ON_TRAILING_EDGE_CPHA_1 等效于值为 1 的 CPHA。

#### ioctlSET_SPI_CLOCK_POLARITY

  设置 SPI 时钟的极性 (CPOL)。

  **参数：**有两个有效值。

  - boardSPI_CLOCK_BASE_VALUE_CPOL_1：

    使用 boardSPI_CLOCK_BASE_VALUE_CPOL_1 将帧间时钟的基准值设为高值，
    将活动时钟设为低值。

    boardSPI_CLOCK_BASE_VALUE_CPOL_1 等效于值为 1 的 CPOL。

  - boardSPI_CLOCK_BASE_VALUE_CPOL_0：

    使用 boardSPI_CLOCK_BASE_VALUE_CPOL_0 将帧间时钟的基准值设为低值，
    将活动时钟设为高值。

    boardSPI_CLOCK_BASE_VALUE_CPOL_0 等效于值为 0 的 CPOL。

#### ioctlSET_SPI_MODE

  将总线设置为主模式或从模式。

  **参数：**有两个有效值。

  - boardSPI_MASTER_MODE：

    boardSPI_MASTER_MODE 将 SPI 外围设备设置为主模式。

  - boardSPI_SLAVE_MODE：

    boardSPI_SLAVE_MODE 将 SPI 外围设备设置为从模式。请注意，暂且不支持从模式。


### I2C 特定请求代码

#### ioctlSET_I2C_SLAVE_ADDRESS

  设置 I2C 外围设备处于主模式时的写入地址。所有的 I2C 传输
  均将使用此地址，直到其因另一个 ioctlSET_I2C_SLAVE_ADDRESS 请求而发生变更。

  **参数：**待设置的从地址。例如，要写入地址 0x20，使用 0x20 即可。

