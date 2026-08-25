---
title: "恢复上下文"
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

RTOS 宏 portRESTORE_CONTEXT() 是 portSAVE_CONTEXT() 的逆向操作。正在恢复的任务的上下文
先前存储在任务堆栈中。实时内核检索任务的堆栈指针，
然后将上下文弹出回正确的处理器寄存器。

```c
#define portRESTORE_CONTEXT()
asm volatile (
  "lds r26, pxCurrentTCB nt" (1)
  "lds r27, pxCurrentTCB + 1 nt" (2)
  "ld r28, x+ nt"
  "out __SP_L__, r28 nt" (3)
  "ld r29, x+ nt"
  "out __SP_H__, r29 nt" (4)
  "pop r31 nt"
  "pop r30 nt"

 :
 :
 :

  "pop r1 nt"
  "pop r0 nt" (5)
  "out __SREG__, r0 nt" (6)
  "pop r0 nt" (7)
);
```

请参阅以上代码：

- FreeRTOS pxCurrentTCB 变量保存可从中检索任务堆栈指针的地址。
  这被加载到 X 寄存器（1 和 2）。
- 被恢复的任务的堆栈指针被加载到 AVR 堆栈指针中，首先是低字节 (3)，然后是高
  半字节 (4)。
- 之后，处理器寄存器以相反的数字顺序从堆栈中弹出 (pop)，直至 R1。
- 状态寄存器存储在寄存器 R1 和 R0 之间的堆栈上，因此在 R0 (7) 前被恢复 (6)。

下一节：[RTOS 实现 — 整合所有部分](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/01-Putting-it-all-together)
