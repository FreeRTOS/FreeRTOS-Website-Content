---
title: "实现质量管理"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: FreeRTOS 内核
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel/
---

**价值主张**
* 配置管理严格，C 源代码质量高 
* 安全关键版本确保可靠性 
* 跨平台支持保障时间投入 
* 提供教程书籍和培训，以指导工程师 
* 为所有支持的移植提供预配置示例项目 
* 免费支持，口碑优于部分商业竞品 
* 用户群和社区庞大，且仍在不断增长 
* *省心*：可随时获取低成本的商业方案 
* **= 总拥有成本低、无风险、令人信服的解决方案** 

<table>
  <thead>
    <tr>
      <th colSpan={2}>RTOS 技术亮点</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>抢占式调度选项</td>
      <td>消息传递易于使用</td>
    </tr>
    <tr>
      <td>协同式调度选项</td>
      <td>带时间切片的轮询</td>
    </tr>
    <tr>
      <td>快速任务通知</td>
      <td>互斥锁采用优先级继承机制</td>
    </tr>
    <tr>
      <td>6K 到 12K 的 ROM 占用空间</td>
      <td>递归互斥锁</td>
    </tr>
    <tr>
      <td>可配置/可扩展</td>
      <td>二进制和计数信号量</td>
    </tr>
    <tr>
      <td>芯片和编译器通用</td>
      <td>软件定时器极其高效</td>
    </tr>
    <tr>
      <td>部分移植从不完全禁用中断</td>
      <td>API 易于使用</td>
    </tr>
  </tbody>
</table>

FreeRTOS 采用非常严格的质量管理，无论是在 
[软件编码标准和外观风格](../FreeRTOS-Coding-Standard-and-Style-Guide)方面， 
还是在各项实现中，均是如此。例如：

* FreeRTOS **从不**在临界区或中断内部执行非确定性操作， 
  例如遍历链接列表。
* 高效的[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)实现尤其让我们引以为傲，
  **该定时器只在确实需要维护时才占用 CPU 时间**。软件定时器不包含
  需要倒计时到零的变量。
* 阻塞（挂起）任务列表同样也不需要耗时的定期维护。
* [直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)可用于快速向任务发送信号，几乎不占用 RAM，
  并且可用于大多数任务间以及中断到任务的信号发送情景。
* 通常情况下，简单性和灵活性不可兼得，但 [FreeRTOS 队列使用模型](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
  （通过很短的代码）却兼具两种特性。
* FreeRTOS 队列是基础原语，其他通信和同步原语都在其上构建。
  代码的重复使用可大幅减少代码的总长度，这反过来又**有助于进行测试和确保稳健性**。

此外，经 [TÜV SÜD](http://www.tuev-sued.com/) 认证的 SIL 
3 [SafeRTOS 实时内核](../FreeRTOS-Plus/Safety_Critical_Certified/SafeRTOS)最初源自 
FreeRTOS，并且经过了最严格的分析和测试过程，其结果 
反馈回 FreeRTOS 代码库中（两者具有共性时）。

