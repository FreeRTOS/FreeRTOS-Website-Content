---
title: "解决方案 #2"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: 实时应用程序设计教程
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: 解决方案 1
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution1
next:
  title: 解决方案 3
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution3
---

**完全抢占式系统**


## 概要

本文将介绍一种传统的抢占式多任务处理解决方案。 

该方案充分利用 RTOS 服务，不考虑由此产生的内存和处理器开销，

而是将所需功能简单地
划分为多个自主任务。

---


## 实现

为系统中每一个可以独立存在或具有特定时序要求的部分 
创建单独的任务。


![](/media/2018/tasks1.gif)   
**解决方案 #2 函数任务和优先级**


在事件指示需要处理之前，任务将处于阻塞状态。事件可以是外部事件 
（如按下按键），也可以是内部事件（如定时器到期）。这种基于事件的方法可确保 
不会浪费 CPU 时间来轮询尚未发生的事件。


根据任务的时序要求为其分配优先级。时序要求越严格， 
优先级越高（并非所有优先级分配评估都如此简单）。


### 操作理念

最高优先级的任务（即未阻塞的任务）由 RTOS 保证 
获得处理器时间。一旦有更高优先级的任务可执行， 
内核会立即挂起正在执行的任务。

这种调度自动执行， 
无需对调度算法有深入的了解，也无需在应用程序源代码中添加特定的调度结构或命令。但是，应用程序设计者有责任确保 
为任务分配适当的优先级。

没有任务可执行时，空闲任务将执行。空闲任务可以选择 
将处理器置于节能模式。


### 调度器配置

调度器配置为抢占式操作。内核滴答频率应设置为 
提供所需时间粒度的最慢值。


### 评估

![](/media/2018/good.gif)  设计简单、模块化、灵活且易于维护，任务之间的相互依赖较少。

![](/media/2018/good.gif)  处理器利用率会根据最紧急的需求自动在任务之间切换，<br/> 无需在应用程序源代码中进行显式操作。

![](/media/2018/good.gif)  基于事件的结构可确保不会浪费 CPU 时间来轮询尚未发生的事件。仅在<br/> 有实际工作需要完成时才进行处理。

![](/media/2018/indif.gif)  如果空闲任务将处理器置于节能（休眠）模式，则可以降低功耗，<br/> 但也可能浪费功耗，因为滴答中断有时会不必要地唤醒处理器。

![](/media/2018/indif.gif)  内核功能会消耗处理资源，消耗的程度取决于所选的内核<br/> 滴答频率。

![](/media/2018/bad.gif)  本解决方案需要大量任务，每个任务都需要自己的堆栈，其中许多任务需要<br/> 可以接收事件的队列，因此会占用大量 RAM。

![](/media/2018/bad.gif)  在具有相同优先级的任务之间频繁切换上下文会浪费处理器周期。


### 结语

本解决方案适用于具有足够 RAM 和处理能力的系统。需要仔细考虑如何将应用程序划分为 
不同任务并为每个任务分配适当的优先级。


---

## 示例

本示例是先前介绍的假设应用程序的部分实现，使用了
FreeRTOS API。
  

### 工厂控制任务

此任务可实现所有控制功能，具有严格的时序要求， 
因此在系统中具有最高优先级：

```c
#define CYCLE_RATE_MS       10
#define MAX_COMMS_DELAY     2

void PlantControlTask( void *pvParameters )
{
TickType_t xLastWakeTime;
DataType Data1, Data2;

    InitialiseTheQueue();

    // A
    xLastWakeTime = xTaskGetTickCount();

    // B
    for( ;; )
    {
        // C
        vTaskDelayUntil( &xLastWakeTime, CYCLE_RATE_MS );
        
        // Request data from the sensors.
        TransmitRequest();
        
        // D
        if( xQueueReceive( xFieldBusQueue, &Data1, MAX_COMMS_DELAY ) )
        {
            // E
            if( xQueueReceive( xFieldBusQueue, &Data2, MAX_COMMS_DELAY ) )
            {
                PerformControlAlgorithm();
                TransmitResults();                
            }
        } 
    }
    
    // Will never get here!
}

```

根据上述代码片段中的标注：

1. xLastWakeTime 已初始化。此变量与 vTaskDelayUntil() API 函数一起使用，
   以控制控制函数的执行频率。

2. 此函数作为自主任务执行，因此绝不能退出。

3. vTaskDelayUntil() 会指示内核此任务 
   应在 xLastWakeTime 存储的时间之后正好 10 毫秒开始执行。在达到该时间之前，控制任务处于阻塞状态。由于这是系统中优先级最高的任务，
   因此一定会在正确的时间再次开始执行，并且会抢占
   任何正在运行的低优先级任务。

4. 从联网传感器请求数据到接收数据之间存在一定的时间差。
   中断服务程序会将到达现场总线的数据放置在 xFieldBusQueue 中，
   因此控制任务可以在队列中进行阻塞调用，以等待有可用数据。该任务在系统中优先级最高，
   因此数据一旦可用，便会立即继续执行。

5. 类似于第 4 点，等待来自第二个传感器的数据。

xQueueReceive() 的返回值为 0，表示在指定的阻塞期间内没有数据到达。 
这是任务必须处理的错误情况。为简单起见，已省略 
此错误情况和其他错误处理功能。

  
### 嵌入式 Web 服务器任务

嵌入式 Web 服务器任务可以用以下伪代码表示。该任务仅在有数据时才会使用处理器时间， 
但完成时间相对较长且不确定。因此， 
此任务被赋予低优先级，以防止对工厂控制、RS232 或键盘扫描任务的时序产生不利影响 
。

```c
void WebServerTask( void *pvParameters )
{
DataTypeA Data;

    for( ;; )
    {
        // Block until data arrives. xEthernetQueue is filled by the
        // Ethernet interrupt service routine.
        if( xQueueReceive( xEthernetQueue, &Data, MAX_DELAY ) )
        {
            ProcessHTTPData( Data );
        }        
    }
}
```


### RS232 接口

此任务在结构上与嵌入式 Web 服务器任务非常相似，被赋予中等优先级， 
以确保不会对工厂控制任务的时序产生不利影响。

```c
void RS232Task( void *pvParameters )
{
DataTypeB Data;

    for( ;; )
    {
        // Block until data arrives. xRS232Queue is filled by the
        // RS232 interrupt service routine.
        if( xQueueReceive( xRS232Queue, &Data, MAX_DELAY ) )
        {
            ProcessSerialCharacters( Data );
        }        
    }
}
```


### 键盘扫描任务

这是一项简单的循环任务，被赋予中等优先级 
时序要求与 RS232 任务类似。

循环时间设置得比指定的限制快得多，这是考虑到 
该任务在请求数据后可能无法立即获得处理器时间， 
并且一旦执行，可能会被工厂控制任务抢占。


```c
#define DELAY_PERIOD 4

void KeyScanTask( void *pvParmeters )
{
char Key;
TickType_t xLastWakeTime;

    xLastWakeTime = xTaskGetTickCount();

    for( ;; )
    {
        // Wait for the next cycle.
        vTaskDelayUntil( &xLastWakeTime, DELAY_PERIOD );
        
        // Scan the keyboard.
        if( KeyPressed( &Key ) )
        {
            UpdateDisplay( Key );
        }
    }
}
```

如果系统总体时序允许此任务成为最低优先级任务，则可以完全删除 
对 vTaskDelayUntil() 的调用。键盘扫描函数将在所有高优先级任务阻塞时连续执行， 
有效地取代空闲任务。


### LED 任务

这是所有任务中最简单的任务。

```c
#define DELAY_PERIOD 1000

void LEDTask( void *pvParmeters )
{
TickType_t xLastWakeTime;

    xLastWakeTime = xTaskGetTickCount();

    for( ;; )
    {
        // Wait for the next cycle.
        vTaskDelayUntil( &xLastWakeTime, DELAY_PERIOD );

        // Flash the appropriate LED.
        if( SystemIsHealthy() )
        {
            FlashLED( GREEN );
        }
        else
        {
            FlashLED( RED );
        }        
    }
}
```

---
