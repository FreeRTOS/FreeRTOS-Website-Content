---
title: "RTOS 基础知识"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: RTOS 概念页面链接
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 实现教程
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS 参考手册
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/

next:
  title: 构建您的首个 FreeRTOS 项目
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project
---


**实时操作系统概述**

## 引言

实时操作系统 (RTOS) 是一种体积小巧、确定性强的计算机操作系统。
RTOS 通常用于需要在严格时间限制内对外部事件做出反应的嵌入式系统，如医疗设备和汽车电子控制单元 (ECU)。  通常，此类嵌入式系统中只有一两项功能需要确定性时序，即使嵌入式系统不需要严格的实时反应，使用 RTOS 仍能提供诸多优势。  请参阅常见问题：“[为什么使用 RTOS？](/Why-FreeRTOS/FAQs/What-is-this-all-about/#why-use-an-rtos)”。

RTOS 通常比通用操作系统体积更小、重量更轻，因此 RTOS 非常适用于
内存、计算和功率受限的设备。



## 多任务处理

**内核**是操作系统的核心组件。Linux 等通用操作系统采用的内核
允许多个用户看似同时访问计算机的处理器。这些用户可以各自执行多个程序，看起来像是并发运行。

每个执行的程序由操作系统控制下的一个或多个**线程**实现。如果操作系统能够以这种方式执行多个线程，则称为**多任务处理**。  像 FreeRTOS 这样的小型 RTOS 通常将线程称为**任务**，因为它们不支持虚拟内存，因此进程和线程之间没有区别。

使用多任务操作系统可以简化原本复杂的软件应用程序的设计：

- 操作系统的多任务处理和任务间通信功能允许将复杂的应用程序
  划分为一组更小且更易于管理的任务。
- 这种划分可以简化软件测试，确保团队分工明确，并促进代码复用。
- 复杂的时序和排序细节将由 RTOS 内核负责，从而减轻了应用程序代码的负担。

有关更全面的列表，请参阅常见问题：“[为什么使用 RTOS？](/Why-FreeRTOS/FAQs/What-is-this-all-about/#why-use-an-rtos)”。

## 多任务处理与并发

常规单核处理器一次只能执行一个任务，但多任务操作系统可以快速切换任务，
使所有任务**看起来**像是同时在执行。下图展示了
三个任务相对于时间的执行模式。任务名称用不同颜色标示，并写在左侧。时间从左向右移动，
彩色线条显示在特定时间执行的任务。上方展示了所感知的并发执行模式，
下方展示了实际的多任务执行模式。

![TaskExecution.gif](/media/2018/TaskExecution.gif)

## 调度

**调度器**是内核中负责决定在特定时间应执行什么任务的部分。内核
可以在任务的生命周期内多次暂停并恢复该任务。  如果任务 B 取代任务 A 成为当前执行的任务
（即任务 A 暂停，任务 B 恢复），我们就可以称任务 A “换出”，任务 B “换入”。

**调度策略**是调度器用来决定何时执行哪个任务的算法。在（非实时）多用户系统中，
调度策略通常会确保每个任务获得“公平”的处理器时间。实时嵌入式系统中使用的策略详见下文。

只有当调度算法决定执行不同的任务时，任务才会换出。这种切换可能在当前
执行的任务不知情的情况下发生，例如调度算法响应外部事件或定时器到期时；  还可能
发生在执行任务显式调用某个导致其**让出**、**休眠**（也称为**延迟**）或**阻塞**的 API 函数时。

如果某任务让出，调度算法可能会再次选择同一任务执行。如果某任务休眠，
则在指定的延迟时间到期前不可被选择。  同样，如果某任务阻塞，
则在特定事件发生（例如，数据到达 UART）或超时期满之前将不可被选择。

操作系统内核负责管理这些任务状态和转换，
确保根据调度算法和每个任务的当前状态在给定时间选择适当的任务执行。

![suspending.gif](/media/2018/suspending.gif)

参考上图中的数字标记：

- 在标记 (1) 处，任务 1 正在执行。
- 在标记 (2) 处，内核将任务 1 换出……
- ……并在标记 (3) 处将任务 2 换入。
- 在任务 2 执行期间，在标记 (4) 处，任务 2 锁定了处理器外设以进行独占访问（图中不可见）。
- 在标记 (5) 处，内核将任务 2 换出……
- ……并在标记 (6) 处将任务 3 换入。
- 任务 3 试图访问之前被任务 2 锁定的处理器外设，发现其被锁定，在标记 (7) 处阻塞以等待外设解锁。
- 在标记 (8) 处，内核将任务 1 换入。
- 如此往复。
- 在标记 (9) 处，任务 2 再次执行，完成对外设的操作并解锁。
- 在标记 (10) 处，任务 3 再次执行，发现外设可用，继续执行直到再次被换出。

## 实时调度

实时操作系统 (**RTOS**) 利用与通用（非实时）系统相同的原理来实现多任务处理，
但两者的目标截然不同。这一差异主要体现在调度策略上。实时嵌入式系统
旨在对现实世界的事件作出及时响应。这些事件通常有截止时间，
实时嵌入式系统必须在此之前响应，RTOS 调度策略必须确保遵守这些截止时间要求。

为在小型 RTOS（如 FreeRTOS）中实现这一目标，软件工程师必须为每个任务分配优先级。RTOS 的调度策略
就是确保能够执行的最高优先级任务获得处理时间。如果存在多个能够运行的同等最高优先级任务（既没有延迟也没有阻塞），则调度策略可以选择在这些任务之间“公平”地分配处理时间。

这种基本形式的实时调度并非万能，无法改变时间的快慢，应用程序编写者必须确保设定的时序约束在所选任务优先级安排下是可行的。

### 示例

以下为最基本的示例，涉及一个带有键盘、LCD 和控制算法的实时系统。

用户每次按键后，
必须在合理的时间内获得视觉反馈，如果用户在此期间无法看到按键已被接受，
则该软件产品的使用感会很差（软实时）。如果最长可接受的响应时间是 100 毫秒，则任何介于 0 和 100 毫秒之间的响应都是
可接受的。此功能可作为自主任务实现，结构如下：

```c
void vKeyHandlerTask( void *pvParameters )
{
    // Key handling is a continuous process and as such the task
    // is implemented using an infinite loop (as most real-time
    // tasks are).
    for( ;; )
    {
        [Block to wait for a key press event]
        [Process the key press]
    }
}
```

现在假设实时系统还在执行依赖于数字滤波输入的控制功能。输入必须
每 2 毫秒采样一次、滤波一次并执行控制周期。为了正确操作滤波器，采样时间
必须精确到 0.5 毫秒。此功能可作为自主任务实现，结构如下：

```c
void vControlTask( void *pvParameters )
{
    for( ;; )
    {
        [Delay waiting for 2ms since the start of the previous cycle]
        [Sample the input]
        [Filter the sampled input]
        [Perform control algorithm]
        [Output result]
    }
}
```

软件工程师必须为控制任务分配最高优先级，因为：

1. 控制任务的截止时间比按键处理任务更严格。
2. 错过截止时间对控制任务的后果比对按键处理任务更严重。


下图演示了实时操作系统如何调度这些任务。RTOS 会自行创建一个任务，即**空闲**任务，
仅当没有其他任务能够执行时，该任务才会执行。RTOS 空闲任务总是处于
可以执行的状态。

![RTExample.gif](/media/2018/RTExample.gif)

请参阅上图：

- 起初，两个任务都不能运行：vControlTask 等待合适的时间来开始新的控制周期，
  而 vKeyHandlerTask 则在等待按键操作。处理器时间分配给了 RTOS 空闲任务。
- 在时间 t1 处，发生按键事件。vKeyHandlerTask 可以执行，其优先级高于 RTOS 空闲任务，
  因此获得了处理器时间。
- 在时间 t2 处，vKeyHandlerTask 已完成按键处理并更新 LCD。在按下另一个键之前该任务无法继续执行，
  因此将自己挂起，RTOS 空闲任务恢复执行。
- 在时间 t3 处，定时器事件指示执行下一个控制循环的时间到了。vControlTask 现在可以执行，
  因为优先级最高的任务被立刻分配了处理器时间。
- 在时间 t3 和 t4 之间，vControlTask 仍在执行时，发生了按键事件。vKeyHandlerTask 可以执行，
  但由于其优先级低于 vControlTask，因此未获得任何处理器时间。
- 在 t4 处， vControlTask 完成了控制周期的处理，并且直到下一次定时事件的发生前不能重新开始运行，
  进入阻塞态。vKeyHandlerTask 现在成为可以运行的最高优先级的任务，
  因此获得处理器时间以处理先前的按键事件。
- 在 t5 处，按键事件处理完成，并且 vKeyHandlerTask 进入阻塞态等待下一次按键事件。再一次，
  两个任务都未进入就绪态，RTOS 空闲任务获得处理器时间。
- 在 t5 与 t6 之间，定时事件发生并处理，没有进一步的按键事件发生。
- 在 t6 处发生按键事件，但在 vKeyHandlerTask 完成按键处理之前，发生了定时事件。
  此时两个任务都可以执行。由于 vControlTask 具有更高的优先级，
  因此 vKeyHandlerTask 在完成按键操作之前被挂起，vControlTask 获得处理器时间。
- 在 t8 处，vControlTask 完成控制周期的处理，然后进入阻塞态等待下一次事件。vKeyHandlerTask 再次
  成为运行的最高优先级任务，因此获得处理器时间，以便完成按键处理
  。

