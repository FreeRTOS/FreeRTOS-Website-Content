---
title: "解决方案 #3"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: 实时应用程序设计教程
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: 解决方案 2
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution2
next:
  title: 解决方案 4
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution4
---

\*\*减少 RAM 的使用\*\*

> **注意：**自 FreeRTOS V4.0.0 推出以来，相关页面尚未更新。V4.0.0 引入了 
> 协程的概念，可为本文介绍的设计提供另一种新颖解决方案。 
> 有关更多信息，请参阅[任务和协程](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines)文档。

## 概要

解决方案 #2 充分利用 RTOS 的特性，得到的设计结构清晰， 
但只能在具有充足 RAM 和处理资源的嵌入式计算机上使用。解决方案# 3 尝试调整功能划分，将其更改为任务的形式，以此减少 RAM 的使用 
。

---

## 实现

![](/media/2018/tasks2.gif)   
**解决方案 #3 函数任务和优先级** 

我们[之前已介绍过](/Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design#the-hypothetical-application)假设应用程序的时序要求 
可以分为三类：

1. **严格时序** - 工厂控制

   与之前一样，创建高优先级任务来处理关键控制功能。

2. **仅限截止日期时序** - 人机接口

   解决方案 #3 将 RS232、键盘扫描和 LED 功能合并到优先级中等的任务中。 

   鉴于之前提到的原因，嵌入式 Web 服务器任务最好以较低的 
   优先级运行。与其为 Web 服务器专门创建任务，不如实现空闲任务钩子， 
   将 Web 服务器功能添加到空闲任务中。Web 服务器必须编写成 
   永不阻塞的方式。

3. **灵活时序** - LED

   LED 功能过于简单，不值得为其单独分配任务，尤其是在 RAM 资源有限的情况下。出于演示目的， 
   本示例在单个中等优先级任务中添加了 LED 功能。当然，这可以 
   通过多种方式实现（例如使用外围设备定时器）。

在事件指示需要处理之前，空闲任务之外的其他任务将处于阻塞状态。事件 
可以是外部事件（如按下按键），也可以是内部事件（如定时器到期）。 

### 操作理念

与解决方案 #1 中介绍的无限循环实现相比， 
将功能合并到中等优先级任务中具有以下三大优势：

1. 通过使用队列，中等优先级任务将处于阻塞状态，直到事件触发数据可用， 
   然后立即跳转到相关函数来处理事件，从而避免 
   处理器周期的浪费，这与无限循环实现不同，在无限循环实现中， 
   只有循环到相应的处理程序时才会处理事件。

2. 通过使用实时内核，无需在应用程序源代码中 
   显式考虑时间关键型任务的调度。

3. 从循环中删除嵌入式 Web 服务器函数，可提高执行时间的 
   可预测性。

此外，合并到一个任务中的功能原本属于具有相同优先级的不同任务 
（LED 功能除外）。代码在这个优先级下的执行频率 
不会因为是单个任务还是多个任务而改变。

工厂控制任务是优先级最高的任务， 
应确保其在需要时能够获得处理时间。必要时，该任务将抢占低优先级和中等优先级的任务。当高优先级和中等优先级任务都被阻塞时， 
空闲任务就会执行。空闲任务可以选择 
将处理器置于节能模式。 

### 调度器配置

调度器配置为抢占式操作。内核滴答频率应设置为 
提供所需时间粒度的最慢值。 

### 评估

![](/media/2018/good.gif)  本解决方案仅创建两种应用程序任务，因此使用的 
RAM 比解决方案 #2 少得多。

![](/media/2018/good.gif)  处理器利用率会根据最紧急的需求 
自动在任务之间切换。  

![](/media/2018/good.gif)  有效利用空闲任务，相当于创建了三个应用程序任务优先级， 
但只需两个任务的管理开销。

![](/media/2018/indif.gif)  设计依然简单，但中等优先级任务中 
函数的执行时间   可能会带来时序问题。嵌入式 Web 服务器任务的分离 
降低了这种风险，而且即使存在时序问题，  也不会影响 
工厂控制任务。

![](/media/2018/indif.gif)  如果空闲任务将 CPU 置于节能（休眠）模式， 
则可以降低功耗，  但也可能浪费功耗，因为滴答中断有时 
会不必要地唤醒 CPU。

![](/media/2018/indif.gif)  RTOS 功能会消耗处理资源， 
消耗的程度取决于所选的内核  滴答频率。

![](/media/2018/bad.gif)  如果应用程序规模过大， 
设计可能无法扩展。

### 结语

本解决方案适用于 RAM 有限的系统，但对处理器资源的要求较高。
需要检查系统的剩余容量，以便为未来扩展留出空间。 

---

## 示例

本示例是先前介绍的假设应用程序的部分实现，使用了
FreeRTOS API。

### 工厂控制任务

工厂控制任务与[解决方案# 2](solution2#pcf) 中的介绍完全相同。

### 嵌入式 Web 服务器

该函数从空闲任务调用，一直运行直到完成。

### 中等优先级任务

中优先级任务可以用以下伪代码表示。

```c
#define DELAY_PERIOD 4
#define FLASH_RATE 1000

void MediumPriorityTask( void *pvParameters )
{
xQueueItem Data;
TickType_t FlashTime;

    InitialiseQueue();
    FlashTime = xTaskGetTickCount();
    
    for( ;; )
    {
        do
        {
            // A
            if( xQueueReceive( xCommsQueue, &Data, DELAY_PERIOD ) )
            {
                ProcessRS232Characters( Data.Value );
            }
            
            // B
        } while ( uxQueueMessagesWaiting( xCommsQueue ) );
        
        // C
        if( ScanKeypad() )
        {
            UpdateLCD();
        }
        
        // D
        if( ( xTaskGetTickCount() - FlashTime ) >= FLASH_RATE )
        {
            FlashTime = xTaskGetTickCount();
            UpdateLED();
        }
    }

    // Should never get here.
    return 0;
}
```

根据上述代码片段中的标注：

1. 任务首先进入阻塞状态以等待通信事件。阻塞时间相对较短。

2. do-while 循环一直执行，直到队列中没有数据。如果数据到达速度过快，导致队列永远无法完全清空， 
   则必须修改此实现。

3. 队列中的所有数据已清空，或者在指定的阻塞时间内没有数据到达 
   。等待数据的最大阻塞时间足够短， 
   以确保键盘扫描频率足以满足指定的时序要求。

4. 检查是否是时候闪烁 LED。这行代码执行的频率会有一些抖动， 
   但 LED 时序要求足够灵活，可以通过此实现满足 
   。

---
