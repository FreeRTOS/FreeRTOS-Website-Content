---
title: "解决方案 #4"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: 实时应用程序设计教程
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: 解决方案 3
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution3
---

**减少处理器开销**

> **注意：**自 FreeRTOS V4.0.0 推出以来，相关页面尚未更新。V4.0.0 引入了 
> 协程的概念，可为本文介绍的设计提供另一种新颖解决方案。 
> 有关更多信息，请参阅[任务和协程](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines)文档。


## 概要

解决方案 #2 演示了如何通过充分利用 RTOS 功能来构建结构清晰的应用程序。
解决方案 #3 演示了如何针对 RAM 资源有限的嵌入式计算机进行适配。解决方案 #4 
进一步修改，旨在减少 RTOS 的处理开销。

本解决方案创建了一种混合调度算法（既不完全抢占，也不完全协作）， 
具体方法为将内核配置为协作式调度，然后在事件中断服务程序中 
执行上下文切换。


## 实现

![](/media/2018/tasks3.gif)   
**解决方案 #4 函数任务和优先级**

关键的工厂控制功能依然通过高优先级任务实现， 
但使用协作式调度器需要对其实现进行修改。以前，时序 
可通过 vTaskDelayUntil() API 函数来维护。使用抢占式调度器时，为控制任务分配最高优先级 
可确保该任务在指定的时间准时开始执行。现在 
正在使用协作式调度器，因此只有在应用程序源代码中明确请求时才会切换任务， 
因此失去了时序保证。

解决方案 #4 使用外围设备定时器的中断，确保以控制任务所需的确切频率
请求上下文切换。调度器确保每次请求的上下文切换 
都会切换到可运行的最高优先级任务。 

键盘扫描函数同样需要定期的处理器时间， 
因此也在由定时器中断触发的任务中执行。可以轻松评估此任务的时序；

控制函数的最长处理时间通常发生在出错时， 
即联网传感器没有提供数据，导致控制函数超时。键盘扫描函数的 
执行时间基本固定。因此可以确定，以这种方式链接其功能 
绝不会导致控制周期频率的抖动，更不会导致错过控制周期。

RS232 任务将由 RS232 中断服务程序调度。

LED 功能的时序要求较为灵活，因此可以加入嵌入式 Web 服务器任务， 
在空闲任务钩子中执行。  如果不足以满足需求，也可以将其提升到高优先级任务中。


### 操作理念

协作式调度器仅在收到显式请求时才会执行上下文切换。这可大幅 
降低 RTOS 产生的处理器开销 
（但空闲任务无法再将处理器置于节能模式）。  空闲任务（包括嵌入式 Web 服务器功能） 
将在没有任何不必要的内核中断的情况下执行。

RS232 或定时器外围设备中断 
仅在必要时才触发上下文切换。如此一来，RS232 任务仍可以抢占空闲任务， 
也可以被工厂控制任务抢占，从而确保整个系统能够根据任务的优先级进行有效调度。


### 调度器配置

调度器配置为协作式操作。内核滴答仅用于维持实时 
滴答值。


### 评估

![](/media/2018/good.gif)本解决方案仅创建两种应用程序任务，因此使用的 
RAM 比解决方案 #2 少得多。 

![](/media/2018/indif.gif)RTOS 上下文切换开销降至最低， 
但是空闲任务  可能无法再使用节能模式， 
因此会消耗更多 CPU 周期。

![](/media/2018/indif.gif)本解决方案仅使用 RTOS 的部分功能。这需要 
在应用程序源代码层面  更多地考虑时序和执行环境， 
但仍可大大简化设计  （与解决方案 #1 相比）。

![](/media/2018/bad.gif)本解决方案依赖处理器外围设备，不可移植。

![](/media/2018/bad.gif)虽然程度较轻， 
但模块间分析和相互依赖的问题  （见解决方案 #1） 
再次出现。

![](/media/2018/bad.gif)如果应用程序规模过大，设计可能无法扩展。


### 结语

RTOS 内核功能只需很少的开销，即使在因处理器和内存限制而无法使用完全抢占式解决方案的系统上， 
也能实现简化的设计。

---


## 示例

本示例是先前介绍的假设应用程序的部分实现，使用了
FreeRTOS API。
  

### 高优先级任务

高优先级任务由周期性中断服务程序“给定”的信号量触发：

```c
void vTimerInterrupt( void )
{
    // 'Give' the semaphore. This will wake the high priority task.
    xSemaphoreGiveFromISR( xTimingSemaphore );
    
    // The high priority task will now be able to execute but as
    // the cooperative scheduler is being used it will not start
    // to execute until we explicitly cause a context switch.
    taskYIELD();    
}
```

请注意，用于在 ISR 中强制执行上下文切换的语法可能因移植而异。 
请勿直接复制本示例，而应查看所用移植的相关文档。

高优先级任务包含工厂控制和键盘功能。为确保时序一致性，请先调用 PlantControlCycle() 
。 

```c
void HighPriorityTaskTask( void *pvParameters )
{
    // Start by obtaining the semaphore.
    xSemaphoreTake( xSemaphore, DONT_BLOCK );  

    for( ;; )
    {
        // Another call to take the semaphore will now fail until
        // the timer interrupt has called xSemaphoreGiveFromISR().
        // We use a very long block time as the timing is controlled
        // by the frequency of the timer.
        if( xSemaphoreTake( xSemaphore, VERY_LONG_TIME ) == pdTRUE )
        {
            // We unblocked because the semaphore became available.
            // It must be time to execute the control algorithm.
            PlantControlCycle();
            
            // Followed by the keyscan.
            if( KeyPressed( &Key ) )
            {
                UpdateDisplay( Key );
            }
        }
        
        // Now we go back and block again until the next timer interrupt.
    }
}
```

### RS232 任务

RS232 任务仅在等待数据到达的队列上才会进入阻塞状态。RS232 中断服务程序 
必须将数据发布到队列中（使任务处于就绪态），然后强制执行上下文切换。此 
机制类似于之前提到的定时器中断伪代码。

因此，RS232 任务可以用以下伪代码表示：

```c
void vRS232Task( void *pvParameters )
{
DataType Data;

    for( ;; )
    {
       if( cQueueReceive( xRS232Queue, &Data, MAX_DELAY ) )
        {
            ProcessRS232Data( Data );
        }        
    }
}
```

### 嵌入式 Web 服务器和 LED 功能

其他系统功能放置在空闲任务钩子中。空闲任务钩子是
在每个空闲任务周期中被调用的函数。

```c
void IdleTaskHook( void )
{
static TickType_t LastFlashTime = 0;

    ProcessHTTPRequests();
    
    // Check the tick count value to see if it is time to flash the LED
    // again.
    if( ( xTaskGetTickCount() - LastFlashTime ) > FLASH_RATE )
    {
        UpdateLED();
        
        // Remember the time now so we know when the next flash is due.
        LastFlashTime = xTaskGetTickCount();
    } 
}
```

---
