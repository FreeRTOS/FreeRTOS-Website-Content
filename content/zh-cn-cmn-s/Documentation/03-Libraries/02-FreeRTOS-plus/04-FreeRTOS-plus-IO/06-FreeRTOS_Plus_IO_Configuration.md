---
title:
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS-Plus-IO 配置


### 简介

FreeRTOS-Plus-IO 和 FreeRTOS 内核一样，使用头文件进行配置。
FreeRTOS 配置头文件名为 FreeRTOSConfig.h，
而 FreeRTOS-Plus-IO 配置头文件名为 FreeRTOS**IO**Config.h。

内核配置文件 (FreeRTOSConfig.h) 中的设置
对代码编译后生成的可执行二进制文件的大小影响不大
。这是因为，
其中所含的设置在大多数情况下是用来包含或排除整体函数。
大多数链接器默认*从可执行二进制文件中移除任何未引用的
函数。
而 FreeRTOS-Plus-IO 配置文件 (FreeRTOS**IO**Config.h) 中的设置
却**会**对代码大小产生很大影响。因为它们是用于
选择性地包含或排除函数内的代码，而不是选择性地包含或排除整体函数本身。
如果 flash/ROM 空间紧缺，应务必以最优方式对 FreeRTOSIOConfig.h 进行配置
。

* GCC 是个例外，它需要特定编译时间选项来请求
  删除未引用的代码。


### FreeRTOSIO Config.h 头文件示例

FreeRTOSIOConfig.h 头文件中所含参数的详情
取决于使用的[板级支持包](Board_Support_Packages)。
以下为相关示例，随后为解释说明。

```c
/* Globally include or exclude transfer modes. -------------------------------*/
#define ioconfigUSE_ZERO_COPY_TX                     1
#define ioconfigUSE_TX_CHAR_QUEUE                    1
#define ioconfigUSE_CIRCULAR_BUFFER_RX               1
#define ioconfigUSE_RX_CHAR_QUEUE                    1


/* Peripheral options --------------------------------------------------------*/

/* There is one group of definitions for each peripheral defined by the
board support package. More details are provided below this example. */

/* Globally include or exclude the UART driver. */
#define ioconfigINCLUDE_UART                         1
    /* Include or exclude transfer modes for this particular peripheral. These
 are dependent on the global transfer mode settings at the top, and the
 global setting for the UART peripheral directly above. */
    #define ioconfigUSE_UART_POLLED_TX               0
    #define ioconfgiUSE_UART_POLLED_RX               0
    #define ioconfigUSE_UART_ZERO_COPY_TX            0
    #define ioconfigUSE_UART_TX_CHAR_QUEUE           1
    #define ioconfigUSE_UART_CIRCULAR_BUFFER_RX      0
    #define ioconfigUSE_UART_RX_CHAR_QUEUE           1

/* As above, but for the SPI peripheral. */
#define ioconfigINCLUDE_SPI                          1
    #define ioconfigUSE_SPI_POLLED_TX                0
    #define ioconfigUSE_SPI_POLLED_RX                0
    #define ioconfigUSE_SPI_ZERO_COPY_TX             1
    #define ioconfigUSE_SPI_CIRCULAR_BUFFER_RX       1
    #define ioconfigUSE_SPI_RX_CHAR_QUEUE            0
    #define ioconfigUSE_SPI_TX_CHAR_QUEUE            0

/* Etc. for any other peripherals defined by the board support package. */

```

### 全局传输模式选项

在上面的示例中，顶部的选项组用于包含或排除
FreeRTOS-Plus-IO 中的特定[传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)。轮询模式始终可用，
所以并没有特定于其的选项。

| **FreeRTOSIOConfig.h 参数** | **用法** |
| --- | --- |
|  ioconfigUSE_ZERO_COPY_TX  |  此情况下必须置 1：如果要使用  [中断驱动的零拷贝传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)。否则设置为零，以确保最佳运行时和代码大小的效率。   |
|  ioconfigUSE_CIRCULAR_BUFFER_RX  |  此情况下必须置 1：如果要使用  [中断驱动的循环缓冲区传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode)。否则设置为零，以确保最佳运行时和代码大小的效率。   |
|  ioconfigUSE_TX_CHAR_QUEUE  |  此情况下必须置 1：如果要使用  [中断驱动的字符队列传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)以写入数据。否则设置为零，以确保最佳运行时和代码大小的效率。   |
|  ioconfigUSE_RX_CHAR_QUEUE  |  此情况下必须置 1：如果要使用  [中断驱动的字符队列传输模式](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)以读取数据。否则设置为零，以确保最佳运行时和代码大小的效率。   |


### 外围设备特定选项

板级支持包定义了可用的外围设备。
每个外围设备都有一个全局的包含或排除选项。例如，
若要包含 SPI 外设，可将 configINCLUDE_SPI 设置为 1。
若要排除 SPI 外设，则将 configINCLUDE_SPI 设置为 0。

另外，每个外围设备对其支持的每种传输模式都具有一个子选项
。例如，若要以中断驱动的零拷贝模式使用 SPI 端口，
可将 ioconfigUSE_SPI_ZERO_COPY_TX 设置为 1；
否则，将 ioconfigUSE_SPI_ZERO_COPY_TX 设置为 0。

因此，继续讨论上面的例子，若要以中断驱动的零拷贝模式使用 SPI 端口，
需要三个设置：

1. 必须将 ioconfigUSE_ZERO_COPY_TX 设置为 1，以启用 FreeRTOS-Plus-IO 的传输模式。
2. 必须将 ioconfigINCLUDE_SPI 设置为 1，以启用 SPI 支持。
3. 必须将 ioconfigUSE_SPI_ZERO_COPY_TX 设置为 1，以在 SPI 移植中明确启用零拷贝传输模式
   。
