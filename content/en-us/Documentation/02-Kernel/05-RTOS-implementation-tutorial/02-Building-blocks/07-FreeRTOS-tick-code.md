---
title: "FreeRTOS Tick Code"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS kernel building blocks
relatedLinks:
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS reference manual
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
---

[[RTOS Implementation Building Blocks](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/01-Building-blocks)]

The actual source code used by the FreeRTOS AVR port is slightly different to the examples shown on the previous
pages. vPortYieldFromTick() is itself implemented as a 'naked' function, and the context is saved and restored within
vPortYieldFromTick(). It is done this way due to the implementation of non-preemptive context switches (where a task blocks
itself) - which are not described here.

The FreeRTOS implementation of the RTOS tick is therefore _(see the comments in the source code snippets for further details)_:

```c
void SIG_OUTPUT_COMPARE1A( void ) __attribute__ ( ( signal, naked ) );
void vPortYieldFromTick( void ) __attribute__ ( ( naked ) );

/*--------------------------------------------------*/

/* Interrupt service routine for the RTOS tick. */
void SIG_OUTPUT_COMPARE1A( void )
{
    /* Call the tick function. */
    vPortYieldFromTick();

    /* Return from the interrupt. If a context
       switch has occurred this will return to a
       different task. */
    asm volatile ( "reti" );
}

/*--------------------------------------------------*/

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

/*--------------------------------------------------*/
```

Next: [RTOS Implementation - The AVR Context](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/08-The-AVR-context)
