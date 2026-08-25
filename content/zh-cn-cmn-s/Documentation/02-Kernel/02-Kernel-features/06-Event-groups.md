---
title: "FreeRTOS 事件组"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 事件组
relatedLinks:
  - title: API 引用 - 事件组
    link: /Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups/
---

## 事件位（或*标志*）和事件组

[**提示：在许多情况下，“任务通知”可以提供事件组的轻量级替代方案**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)

### 事件位（事件标志）

事件位用于指示事件
是否发生。事件位通常称为事件*标志*。例如，
应用程序可以：

* 定义一个位（或标志），
  设置为 1 时表示“已收到消息并准备好处理”，
  设置为 0 时表示“没有消息等待处理”。

* 定义一个位（或标志），
  设置为 1 时表示“应用程序已将准备发送到网络的消息排队”，
  设置为 0 时表示
  “没有消息需要排队准备发送到网络”。

* 定义一个位（或标志），
  设置为 1 时表示“需要向网络发送心跳消息”，
  设置为 0 时表示“不需要向网络发送心跳消息”。


### 事件组

事件组就是一组事件位。事件组中的事件位
通过位编号来引用。同样，以上面列出的三个例子为例：

* 事件标志组位编号
  为 0 表示“已收到消息并准备好处理”。

* 事件标志组位编号
  为 1 表示“应用程序已将准备发送到网络的消息排队”。

* 事件标志组位编号
  为 2 表示“需要向网络发送心跳消息”。


### 事件组和事件位数据类型

事件组由 EventGroupHandle_t 类型的变量引用。

如果 
[configUSE_16_BIT_TICKS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_16_bit_ticks) 设为 1，则事件组中存储的位（或标志）数为 8；
如果 configUSE_16_BIT_TICKS 设为 0，则为 24。
configUSE_16_BIT_TICKS 的值取决于
任务内部实现中用于线程本地存储的数据类型。

事件组中的所有事件位都
存储在 EventBits_t 类型的单个无符号整数变量中。事件位 0 存储在位 0 中，
事件位 1 存储在位1 中，依此类推。

下图表示一个 24 位事件组，
使用 3 个位来保存前面描述的 3 个示例事件。在图片中，仅设置了
事件位 2。

![包含 24 个事件标志的事件组](/media/2018/24-bit-event-group.gif)   
*包含 24 个事件位的事件组，其中只有三个在使用中* 


### 事件组 RTOS API 函数

提供的事件组 [API 函数](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups) 
允许任务在事件组中[设置](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/05-xEventGroupSetBits)一个或多个事件位， 
[清除](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/07-xEventGroupClearBits)事件组中的一个或多个事件位，
并[挂起](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/04-xEventGroupWaitBits)（进入阻塞状态，
因此任务不会消耗任何处理时间）以等待
事件组中一个或多个事件位固定下来。

事件组也可用于[同步 ](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/11-xEventGroupSync) 任务，
创建通常称为“集合”的任务。任务同步点是
应用程序代码中的一个位置，在该位置任务将在
阻塞状态（不消耗任何 CPU 时间）下等待，直到参与同步的所有其他任务
也到达其同步点。


### 实现事件组时 RTOS 必须克服的挑战

在实现事件组时，RTOS 必须克服以下两项主要挑战：

1. 避免在用户的应用程序中创建争用条件：  
   如果出现以下情况，
   事件组实现将在应用程序中创建争用条件：
   
   * 不清楚各个位（或标志）由谁清除。

   * 不清楚何时清除位。

   * 不清楚在任务退出测试位值的 API 函数时
     是否设置或清除了位（可能是
     另一个任务或中断已更改该位的状态）。
     
   FreeRTOS 事件组的实现通过内置智能来确保位的设置、测试和清除具有原子性，
   从而消除了争用条件的可能性。线程本地存储和
   谨慎使用 API 函数返回值使之成为可能。

2. 避免不确定性：

   事件组概念意味着非确定性行为，因为
   不知道在一个事件组上有多少任务被阻塞，因此
   不清楚在设置事件位时
   需要测试多少条件或解除多少阻塞任务。

   根据 FreeRTOS 质量标准，**无法**在禁用中断时
   或在中断服务程序中
   执行非确定性操作。为确保在设置事件位时
   不违反这些严格的质量标准，需要以下两点：

   * RTOS 调度器的锁定机制用于确保
     在 RTOS 任务中设置事件位时中断仍处于启用状态。
     
   * 尝试在中断服务程序中设置事件位时，
     集中延迟中断机制用于
     将设置位的动作延迟到任务。


### 示例代码

[API](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups) 文档中提供了
如需查看完整示例，请参阅 EventGroupsDemo.c
标准演示任务集（源文件位于 FreeRTOS/Demo/Common/Minimal 目录中，
该目录位于 [FreeRTOS 主下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)中）。
