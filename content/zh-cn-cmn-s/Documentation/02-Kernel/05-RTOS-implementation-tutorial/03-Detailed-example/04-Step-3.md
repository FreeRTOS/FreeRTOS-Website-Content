---
title: RTOS 上下文切换 - 步骤 3
created: 2018-09-20
categories:
- 内核
description: FreeRTOS 内核详细描述
relatedLinks:
- title: 免费下载RTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: FreeRTOS 参考手册
  link: /Documentation/02-Kernel/06-Books-and-mannual/01-RTOS_book/
---

[[详细示例](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

## RTOS 滴答中断执行

ISR 源代码如下。为方便阅读，已删除注释（可在之前的页面查看）。

```c
/* Interrupt service routine for the RTOS tick. \*/
void SIG_OUTPUT_COMPARE1A( void )
{
    vPortYieldFromTick();
    asm volatile ( "reti" );
}
/\*--------------------------------------------------*/

void vPortYieldFromTick( void )
{
    portSAVE_CONTEXT();

    vTaskIncrementTick();
    vTaskSwitchContext();
    portRESTORE_CONTEXT();

    asm volatile ( "ret" );
}
/\*--------------------------------------------------\*/
```

SIG_OUTPUT_COMPARE1A() 是裸函数，因此第一条指令是调用 vPortYieldFromTick()。
vPortYieldFromTick() 也是裸函数，因此可调用
portSAVE_CONTEXT() 显式保存 AVR 执行上下文。

portSAVE_CONTEXT() 将整个 AVR 执行上下文推送到 TaskA 的堆栈上，从而产生下图所示的堆栈。
TaskA 的堆栈指针目前指向其自身上下文的顶部。在存储堆栈指针的副本后， portSAVE_CONTEXT() 执行
完成。实时内核已有 TaskB 堆栈指针的副本，该指针是在上次挂起 TaskB 时获取的。

![AtoB3.gif](/media/2018/AtoB3.gif)

下一节：[RTOS 实现 - 详细示例步骤 4](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/03-Detailed-example/05-Step-4)
