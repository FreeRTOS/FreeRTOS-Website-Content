---
title: "保存 RTOS 任务上下文"
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

各实时任务都有自己的堆栈内存区域，因此只需将处理器寄存器推送到任务堆栈上，
即可保存上下文。汇编代码无法避免地需要保存 AVR 上下文。

portSAVE_CONTEXT() 作为宏实现，其源代码如下所示：

```c
#define portSAVE_CONTEXT()
asm volatile (
  "push r0 nt" (1)
  "in r0, __SREG__ nt" (2)
  "cli nt" (3)
  "push r0 nt" (4)
  "push r1 nt" (5)
  "clr r1 nt" (6)
  "push r2 nt" (7)
  "push r3 nt"
  "push r4 nt"
  "push r5 nt"

 :
 :
 :

  "push r30 nt"
  "push r31 nt"
  "lds r26, pxCurrentTCB nt" (8)
  "lds r27, pxCurrentTCB + 1 nt" (9)
  "in r0, __SP_L__ nt" (10)
  "st x+, r0 nt" (11)
  "in r0, __SP_H__ nt" (12)
  "st x+, r0 nt" (13)
);
```

参考上方源代码：

- 处理器寄存器 R0 在保存状态寄存器时使用，因此首先保存，
  而且必须保存其原始值。
- 状态寄存器被移入 R0 (2)，因此可以保存到堆栈 (4) 中。
- 处理器中断已禁用 (3)。如果仅从 ISR 中调用 portSAVE_CONTEXT()，则无需显式禁用中断，
  因为 AVR 已经执行了此操作。由于 portSAVE_CONTEXT() 宏也用于
  中断服务程序之外（任务自行挂起时），
  因此必须尽早显式禁用中断。
- 编译器从 ISR C 源代码生成的代码假设 R1 设置为零。在禁用 R1 之前 (6)，
  R1 的原始值已保存为 (5)。
- (7) 和 (8) 之间的所有剩余处理器寄存器均按数字顺序保存。
- 挂起的任务堆栈现在包含任务执行上下文的副本。内核存储
  任务堆栈指针，以便在恢复任务时可以检索和还原上下文。X 处理器寄存器
  加载要保存堆栈指针的地址（8 和 9）。
- 保存堆栈指针，首先是低字节（10 和 11），然后是高四位字节（12 和 13）。

下一节：[RTOS 实现 — 恢复上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/10-Restoring-the-context)
