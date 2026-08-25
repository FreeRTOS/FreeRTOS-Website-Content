---
title: vTaskStartScheduler
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task. h 

```c
void vTaskStartScheduler( void );
```

启动 RTOS 调度器。调用后，RTOS 内核可以控制在何时执行哪些任务。

[空闲任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)和[定时器守护进程任务](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)（可选）会在 RTOS 调度器启动时自动创建。

`vTaskStartScheduler()` 仅在以下情况下返回：没有足够的 [RTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
可用来创建空闲或定时器守护进程任务。

所有 RTOS 演示应用程序项目都包含使用 `vTaskStartScheduler()`的示例，通常在 main.c 中的 `main()` 函数中使用。

**用法示例：** 

```c
void vAFunction( void )
{
    // Tasks can be created before or after starting the RTOS scheduler
    xTaskCreate( vTaskCode,
                 "NAME",
                 STACK_SIZE,
                 NULL,
                 tskIDLE_PRIORITY,
                 NULL );

    // Start the real time scheduler.
    vTaskStartScheduler();

    // Will not get here unless there is insufficient RAM.
}
```

