---
title: "AVR 上下文"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核构建块
relatedLinks:
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS 参考手册
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
---

[[RTOS 实现构建块](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

如需切换上下文，需要保存整个执行上下文。AVR 微控制器中的上下文
包括：

- 32 个通用处理器寄存器。GCC 开发工具会假定寄存器 R1 设置为 0。
- 状态寄存器。状态寄存器的值会影响指令的执行，
  必须在上下文切换时保持不变。
- 程序计数器。恢复后，任务必须从暂停前即将执行的指令
  继续执行。
- 两个堆栈指针寄存器。

![AVRContext.gif](/media/2018/AVRContext.gif)

下一节：[RTOS 实现 - 保存上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/09-Saving-the-RTOS-task-context)
