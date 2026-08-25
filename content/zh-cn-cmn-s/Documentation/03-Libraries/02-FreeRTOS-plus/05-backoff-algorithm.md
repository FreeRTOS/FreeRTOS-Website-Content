---
title: 退避算法
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


## 简介


[backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm) 库是一个实用程序库， 
用于隔开同一数据块的重复传输，以避免网络堵塞。该库 
使用 
[带抖动的指数退避算法](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)计算重试网络操作（如与服务器的网络连接失败） 
的退避周期。 


带抖动的指数退避通常用于重试失败的服务器连接或网络请求 
。通过将重试请求分散到多个尝试网络连接的设备上， 
带抖动的指数退避有助于缓解因网络堵塞 
或服务器负载过高而导致的服务器网络操作失败。此外，在连接不佳的环境中， 
客户端随时可能断开连接。当重新连接不太可能成功时， 
退避策略可以帮助客户端避免重复尝试重新连接，从而节省电量。 


此库以 C 语言编写，其设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90)  
和 [MISRA C:2012](https://www.misra.org.uk/MISRAHome/MISRAC2012/tabid/196/Default.aspx)。除了 
标准 C 库以外，此库不依赖任何其他库，也没有堆分配， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

请参阅 backoffAlgorithm 库 [API 引用](https://freertos.github.io/backoffAlgorithm/v1.3.0/)。

此库可免费使用，且根据 [MIT 开源许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)发布。


**backoffAlgorithm 的代码大小（使用 GCC 为 ARM Cortex-M 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| backoff_algorithm.c | 0.1K | 0.1K |
| 总估计值 | 0.1K | 0.1K |

