---
title: coreSNTP 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

此演示展示了一个应用程序如何使用 coreSNTP 库，
通过设置 SNTP 客户端定期将系统时间与时间服务器同步，
以此来维持协调世界时 (UTC) 区的实时时钟（或挂钟时间）。演示还展示了如何通过双向身份验证使用 coreSNTP 库与 SNTP/NTP 服务器
进行安全通信。该示例使用基于对称密钥的 AES-128-CMAC 作为身份验证算法。要在启用认证的情况下运行该演示，
使用的服务器必须支持 AES-128-CMAC 算法验证，
在运行演示之前，必须在客户端（演示）和服务器之间生成并预先共享对称密钥。


## 设置 NTP 服务器

为了使用基于 AES-128-CMAC 的身份验证运行 coreSNTP 演示，您需要一个支持该算法进行身份验证的 NTP 服务器。

可以使用支持 AES-128-CMAC 身份验证的 **chronyd** 包来设置 NTP 服务器。**chronyd 服务器** 可以配置为使用一组上游服务器定期同步其时间，
以便能够准确响应 coreSNTP 演示客户端发出的时间请求。请按照 [设置带有身份验证的 NTP 服务器的说明](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/03-Setting-up-an-NTP-server)，
在 AWS EC2 Linux 实例中使用 **chronyd** 并将 Amazon Time Sync 服务作为上游服务器。

## 初始化演示中的配置参数

演示程序通过配置 **democonfigSYSTEM_START_YEAR** 宏来初始化系统时间的第一秒。例如，如果该宏配置为 2021 年，演示程序将系统时间初始化为 2021 年 1 月 1 日 00:00:00。
这么做的目的是避免将系统时间初始化为零，而是将其初始化为一个 *足够接近* 真实世界时间的时间，以便满足应用程序的需求，
如在系统能够与时间服务器同步时间之前，进行诸如服务器证书验证等操作以建立 TLS 连接。

这种做法对于那些没有电池支持的实时时钟（RTC）硬件模块的设备平台尤其有用，因为这些设备没有硬件机制在系统启动时获取真实世界的时间。

1. 打开本地的 `/FreeRTOS-Plus/Demo/coreSNTP_Windows_Simulator/demo_config.h`

2. 定义以下参数(每个参数对应一个 **chronyd** NTP 服务器实现示例):
   ```c
   #define democonfigSNTP_CLIENT_POLLING_INTERVAL_SECONDS ( 16 )
   #define democonfigLIST_OF_TIME_SERVERS "pool.ntp.org"
   #define democonfigLIST_OF_AUTHENTICATION_SYMMETRIC_KEYS {"D5580F199AB94736D4C532842F2C1951"}
   #define democonfigLIST_OF_AUTHENTICATION_KEY_IDS 0x01
   #define democonfigSYSTEM_START_YEAR ( 2021 )
   ```


## 多线程架构 - SNTP 客户端任务和示例应用程序任务

演示架构包含两个任务：

* **SNTP 客户端任务** - 此任务是一个专用的 SNTP 客户端，定期
  使用 coreSNTP 库与时间服务器同步时间。它根据收到的服务器时间校正系统时钟，
  经计算的系统时钟相对于服务器时间漂移以将墙上时钟/实时时钟维持在 UTC 时区中。
  SNTP 客户端任务的逻辑可以在
  GitHub 上的演示文件 [SNTPClientTask.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreSNTP_Windows_Simulator/SNTPClientTask.c) 中找到
  。

* **示例应用程序任务** - 此任务是依赖于从系统中查询的实时信息的
  示例应用程序任务。此基本应用程序任务定期打印从系统中查询的
  实时/墙上时间 (UTC) 。用于定期查询系统时间的此实例应用程序任务的代码
  可在 GitHub 上的
  文件 [SampleAppTask.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreSNTP_Windows_Simulator/SampleAppTask.c) 中找到
  。

coreSNTP 库的所有用途都包含在 SNTP 客户端任务中，以展示如何可以
在FreeRTOS系统中设置 SNTP 客户端任务代理/实用程序，以服务来自多个应用程序任务的时间请求。


## 用于墙上时钟的系统时钟模型

演示显示没有实时时钟硬件模块的设备如何能够将实时时钟（或墙上时钟）
在 RAM中维持在 UTC 时区内。演示使用以下数学模型，可以灵活进行更新，
定期与 SNTP 时间同步：

```c
 **System Time** = **Base Time** +
               **Time Elapsed since last** **SNTP time synchronization** +
               **Slew Adjustment**

 where

 **BaseTime** = Time set at boot or the last synchronized time
 **Slew Rate** = Number of milliseconds of clock correction per system time second
 **No. of ticks since last** **SNTP sync** = Current FreeRTOS Tick Count -
                                     Tick count at last SNTP synchronization

 **Time Elapsed since last** **SNTP time synchronization** =
                            No. of ticks since last SNTP synchronization
                                                   x
                            Number of milliseconds per FreeRTOS tick

 **Slew Adjustment** = Slew Rate x Time Elapsed since last SNTP sync

```

在上述数学模型中，系统时钟振荡器中的任何频率差异都会导致时钟漂移，
使与实际/互联网时间相关的 FreeRTOS tick 的执行时间产生偏差。因此，
在计算系统时钟时要加上一个 **Slew Adjustment 偏移量**，以校正总的
时钟漂移。这样，系统时间就与现实世界的时间一致了。**Slew Adjustment** 取决于
**Slew Rate**，即应定期应用于系统时间，
以抵消系统时钟漂移的调整。当 coreSNTP 库从时间服务器接收时间时，
会根据其提供的时钟偏移值计算一次该速率。


## 时钟校正/约束模型

演示结合 “step” 和 “slew” 两种方法来校正系统时钟，这会分别影响
上一节所述系统时钟的数学模型的 “**Base Time**” 和 “**Slew Adjustment**”
参数。

1. **“Step” 校正**从服务器收到时间时更新系统时钟的 **Base Time**
   参数。此校正用于每个成功与时间服务器同步时间的周期，
   以立即校正系统时钟，使其与服务器时间相匹配。

2. **“Slew” 校正方法**用于补偿系统时钟漂移，该漂移会出现在
   每次与时间服务器的成功时间同步之间的间隔。时钟漂移发生在该间隔中，因为
   系统时间构建于 HW 系统时钟振荡器之上，其频率偏差导致了上述漂移。用于 slew 校正的
   "**Slew Rate**" 仅在第二次与时间服务器
   成功同步时间时计算一次。这是因为演示将系统时间初始化为
   `democonfigSYSTEM_START_YEAR`（的第一秒），因此漂移了一段时间的实际系统时钟
   只有在演示系统时间与从时间服务器获取的真实世界时间同步一次后，
   才能正确进行计算。鉴于第一次和第二次与时间服务器进行时间同步之间的间隔，
   可以计算实际系统时钟漂移，并且可以正确建立用于时钟调整的 **Slew Rate**
   。

以下是演示时钟约束方法如何影响系统的摘要：

```c
On every time response recevied from time server,

  **Base Time = Time from Server**

On the 2nd successful time synchronization with time server,

  **Slew Rate = Clock-Offset (calculated by coreSNTP library) / Poll Period**

```


## 演示中的初始化时间

该演示用
`democonfigSYSTEM_START_YEAR` 宏配置的年份的第一秒初始化系统时间。例如，如果宏被配置为 2021 年，
演示会将系统时间初始化为 2021 年 1 月 1 日 0 时 0 分 0 秒。完成此操作后，系统时间不会
初始化为零，但用*足够接近*真实世界时间的时间来满足
应用程序执行操作的需要，例如验证服务器证书，在它能够与时间服务器同步时间，
获得准确的真实世界时间之前建立 TLS 连接。这对于那些
没有电池支持的实时时钟 (RTC) 硬件模块，且没有硬件机制
在系统启动时获取真实世界时间的设备平台很有用。
