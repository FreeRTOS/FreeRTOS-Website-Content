---
title: FreeRTOS 二进制信号量
created: 2018-09-20
categories:
- 内核
说明: FreeRTOS 二进制信号量
relatedLinks:
- title: API 引用——信号量
  link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
---

[[任务间通信和同步](Inter-Task-Communication)]

[另请参阅[阻塞多个 RTOS 对象](Pend-on-multiple-rtos-objects)]

[FreeRTOS 教程书](Documentation/RTOS_book)
提供更多信息，包括队列、二进制信号量、互斥锁、计数信号量、
递归信号量，以及包含在配套的示例项目中的简单示例
。

### FreeRTOS二进制信号量

[**提示：在许多情况下， “任务通知”可以提供二进制信号量的轻量级替代方案 **](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)

二进制信号量用于互斥和同步目的。

二进制信号量和互斥锁极为相似，但存在一些细微差别：互斥锁包括优先继承机制，
而二进制信号量则不然。因此，二进制信号量是
实现同步的更好选择（任务之间或任务与中断之间），
而互斥锁是实现简单互斥的更好选择。[](Real-time-embedded-RTOS-mutexes)
对如何将互斥锁用作互斥机制的描述同样适用于二进制信号量。本小节
将仅对使用二进制信号量实现同步进行描述。

信号量 API 函数允许指定阻塞时间。阻塞时间表示在尝试“获取”信号量时，
如果信号量不是立即可用，
任务应进入阻塞状态的最大“滴答”数。如果多个任务在同一信号量上阻塞，
则具有最高优先级的任务将成为下次信号量可用时解除阻塞的任务。

可将二进制信号量视为仅能容纳一个项目的队列。因此，队列只能为空或满
（因此称为二进制）。使用队列完成任务和发生中断无关紧要，
因为队列是空还是满才至关重要。可以利用这项机制同步任务和中断（例如）
。

考虑使用任务为外围设备提供服务的情形。轮询外围设备将会耗费 CPU 资源，
阻止执行其他任务。因此，
最好让任务大部分时间处于阻塞状态（允许其他任务执行），
只有在确实有事情需要执行时才执行自身。可以通过使用二进制信号量来实现，
方法是“获取”信号量时使任务阻塞。然后为外围设备编写中断例程，
当外围设备需要服务时，只是“提供”信号量。任务
始终“接收”信号量（从队列中读取信号以使队列变空），但从不“提供”信号量。中断
始终“提供”信号量（将写入队列使其为满），但从不获取信号量。
xSemaphoreGiveFromISR()[/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR] 文档页面提供的源代码应更对此予以清楚说明。()另请参阅
 [RTOS 任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)，在某些情况下，
它可以作为二进制信号量的更快、更轻的替代品。

任务优先级可确保外围设备及时获得服务，进而有效生成“延迟中断”方案。
（注意 FreeRTOS
还具有[内置的延迟中断机制](/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR)）。一种替代方法
是使用队列代替信号量。完成此操作后，
中断例程可以捕获与外设事件关联的数据并将其发送到任务的队列中。队列数据可用时，
任务将取消阻塞，从队列中检索数据，
然后执行必要的数据处理。此第二种方案要求中断尽可能短，
在一个任务中进行所有后置处理。

信号量相关 API 函数的列表，请参阅用户文档的[信号量/互斥锁](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)章节
。请搜索 FreeRTOS/Demo/Common/Minimal 目录下的文件，您将会看到它们的多个用法示例
。请注意，中断只能使用以 "FromISR" 结尾的 API 函数。

![](/media/2018/binary-semaphore.gif)  
_使用信号量同步任务与中断。中断仅“提供” 
 信号量，而任务仅“获取”信号量。_
