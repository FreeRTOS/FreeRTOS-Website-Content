---
title: "FreeRTOS 调度（单核、AMP 和 SMP）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——任务创建
    link: /Documentation/02-Kernel/04-API-references/01-Task-creation/00-TaskHandle/
  - title: API 引用——任务控制
    link: /Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control/
  - title: API 引用——任务实用程序
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/
---

本页简要概述的 FreeRTOS 调度算法适用于单核、非对称多核 (AMP) 
和对称多核 (SMP) RTOS 配置。调度算法是决定 
哪个 RTOS 任务应处于[运行状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)的软件程序。在任何给定时间， 
每个处理器核心只能有一个任务处于运行状态。在 AMP 中， 
每个[处理器核心运行自身的 FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32H7_Dual_Core_AMP_RTOS_demo/) 实例。在 SMP 中， 
存在[一个实例 FreeRTOS，可以跨多核调度 RTOS 任务](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/)。

可免费下载的 [FreeRTOS 书籍](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
更全面地介绍了基础 FreeRTOS 调度算法，还提供了图表和示例。


## 默认 RTOS 调度策略（单核）

FreeRTOS 默认使用固定优先级的抢占式
调度策略，对[同等优先级的任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)执行时间切片轮询调度：


* “固定优先级”是指调度器不会永久更改任务的优先级，
  但可能会因 
  [优先级继承](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)而暂时提高任务的优先级。
  
* “抢占式”是指调度器始终运行优先级最高且可运行的 RTOS 任务，
  无论任务何时能够运行。例如，
  如果中断服务程序 (ISR) 更改了优先级最高且可运行的任务，
  调度器会停止当前正在运行的低优先级任务
  并启动高优先级任务——即使这发生在同一个时间片内
  。这种情况下可以说高优先级任务
  “抢占”了低优先级任务。
  
* “轮询调度”是指具有相同优先级的任务轮流进入运行状态。
  
* “时间切片”是指调度器会在每个 tick 中断上在同等优先级任务之间进行切换，
  tick 中断之间的时间构成一个时间切片。（tick
  中断是 RTOS 用来衡量时间的周期性中断。）


#### 使用优先排序的抢占式调度器，避免任务饥饿

始终运行优先级最高且可运行的任务的一个后果是 
从未进入[阻塞或挂起](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)状态的高优先级任务将永久性剥夺 
所有更低优先级任务的任何执行时间。这就是通常最好创建事件驱动型任务的原因之一
。例如，如果一个高优先级任务正在等待一个事件，那么它就不应 
处于该事件的循环（轮询）中，因为如果处于轮询中，它会一直运行，永远不进入“阻塞”或 
“挂起”状态。相反，该任务应进入“阻塞”状态等待这一事件。该事件可以 
通过某个[FreeRTOS任务间通信和同步原语](/Why-FreeRTOS/highlighted-features)发送至任务。  
收到事件后，优先级更高的任务会自动解除“阻塞”状态。这样低优先级 
任务会运行，而高优先级任务会处于“阻塞”状态。


#### 配置 RTOS 调度策略

以下 FreeRTOSConfig.h 设置更改了默认调度行为：

* `configUSE_PREEMPTION`

  如果 [configUSE_PREEMPTION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_preemption) 为 0，则表示抢占已关闭，
  而且只有当运行状态的任务进入“阻塞”或“挂起”状态，
  或运行状态任务调用 `taskYIELD()`，
  或中断服务程序 (ISR) 手动请求上下文切换时，才会发生上下文切换。
  
* `configUSE_TIME_SLICING`

  如果 [configUSE_TIME_SLICING](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_time_slicing) 为 0，则表示时间切片已关闭，
  因此调度器不会在每个 tick 中断上在同等优先级的任务之间切换。


## FreeRTOS AMP 调度策略

使用 FreeRTOS 的非对称多处理 (AMP)
是指多核设备的每个核心都单独运行自己的 FreeRTOS 实例。这些
核心并不都需要具有相同架构，
但如果 FreeRTOS 实例之间需要进行通信，则需要共享一些内存。 

每个核心都会运行自己的 FreeRTOS 实例，
因此任何给定核心上的调度算法与上文的单核系统调度算法完全相同
。您可以使用[流缓冲区或消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)作为核间通信原语，
这样一来，一个核心上的任务可以进入“阻塞”状态，
以等待另一个核心发来的数据或事件。


## FreeRTOS SMP 调度策略

使用 FreeRTOS 的对称多处理 (SMP) 指的是 
[一个 FreeRTOS 实例可以跨多个处理器核心调度 RTOS 任务](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/)。
由于只有一个 FreeRTOS 实例在运行，一次只能使用 FreeRTOS 的一个移植， 
因此每个核心必须具有相同的处理器架构并共用相同的内存空间。

FreeRTOS SMP 调度策略使用与单核调度策略相同的算法，
但与单核和 AMP 场景不同的是，
SMP 在任何给定时间都会导致多个任务处于运行状态
（每个核心上都有一个运行状态的任务）。这意味着， 
只有缺乏可运行的高优先级任务时，才会运行低优先级任务的假设不再成立
。要想了解其中的原因，请考虑一下，
若起初只有一个高优先级任务
和两个中等优先级任务处于 
[“就绪”状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)，SMP 调度器会如何选择在双核微控制器上运行的任务。调度器需要选择两个任务，每个核心对应一个任务。 
首先，高优先级任务是指可运行的最高优先级任务，
因此会选择将它用于第一个核心。这样就剩下了两个中等优先级的任务
作为可运行的最高优先级任务，因此会将它们用于第二个核心
。结果是高优先级和中等优先级的任务同时运行。


#### 配置 SMP RTOS 调度策略

将为单核或 AMP RTOS 配置编写的代码移动到 
SMP RTOS 配置，而且该代码依据的假设是：如果存在能够运行的较高优先级任务， 
则较低优先级任务将不会运行时，可以使用以下配置选项。

* `configRUN_MULTIPLE_PRIORITIES`

  如果 `configRUN_MULTIPLE_PRIORITIES` 在 `FreeRTOSConfig.h` 中设置为 0，则只有在多个任务具有相同优先级的情况下， 
  调度器才会同时运行多个任务。这可以修复基于下列假设编写的代码： 
  一次将只运行一个任务，但同时必须牺牲
  SMP 配置带来的一些好处。
  
* `configUSE_CORE_AFFINITY`

  如果 `configUSE_CORE_AFFINITY` 在 `FreeRTOSConfig.h` 中设置为 1，
  则 `vTaskCoreAffinitySet()` API 函数可用于定义某个任务可以在哪些核心上运行
  以及不可以在哪些核心上运行。使用该方法，应用程序编写者可以防止
  同时执行假设了自身执行顺序的两个任务
  。
