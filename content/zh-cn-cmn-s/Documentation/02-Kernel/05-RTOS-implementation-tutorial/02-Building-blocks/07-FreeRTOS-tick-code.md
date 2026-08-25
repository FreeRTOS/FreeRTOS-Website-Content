---
title: FreeRTOS 滴答代码
created: 2018-09-20
categories:
- 内核
description: FreeRTOS 内核构建块
relatedLinks:
- title: 免费下载RTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: FreeRTOS 参考手册
  link: /Documentation/02-Kernel/06-Books-and-mannual/01-RTOS_book/
---

[[RTOS 实现构建块](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

FreeRTOS AVR 移植使用的实际源代码与前文的示例略有不同。
vPortYieldFromTick() 本身是作为一个“裸”函数实现的，
且上下文在 vPortYieldFromTick() 中存储和恢复。之所以这么做是为了实现非抢占式上下文切换（在这种情况下，任务阻塞了自己）
——这里不做描述。

因此，RTOS 滴答的 FreeRTOS 实现如下所示（请参阅源代码段注释以了解更多详情）：__

```c
void SIG_OUTPUT_COMPARE1A( void ) \_\_attribute\_\_ ( ( signal, naked ) );
void vPortYieldFromTick( void ) \_\_attribute\_\_ ( ( naked ) );

/\*--------------------------------------------------\*/

/* Interrupt service routine for the RTOS tick. \*/
void SIG_OUTPUT_COMPARE1A( void )
{
    /\* Call the tick function. */
    vPortYieldFromTick();

    /* Return from the interrupt. If a context
       switch has occurred this will return to a
       different task. */
    asm volatile ( "reti" );
}

/\*--------------------------------------------------\*/

void vPortYieldFromTick( void )
{
    /* This is a naked function so the context
       is saved. */
    portSAVE_CONTEXT();

    /* Increment the tick count and check to see
       if the new tick value has caused a delay
       period to expire. This function call can
       cause a task to become ready to run. */
    vTaskIncrementTick();

    /* See if a context switch is required.
       Switch to the context of a task made ready
       to run by vTaskIncrementTick() if it has a
       priority higher than the interrupted task. */
   vTaskSwitchContext();

    /* Restore the context. If a context switch
       has occurred this will restore the context of
       the task being resumed. */
    portRESTORE_CONTEXT();

    /* Return from this naked function. */
    asm volatile ( "ret" );
}

/\*--------------------------------------------------\*/
```

下一节：[RTOS 实现 - AVR 上下文](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/08-The-AVR-context)
