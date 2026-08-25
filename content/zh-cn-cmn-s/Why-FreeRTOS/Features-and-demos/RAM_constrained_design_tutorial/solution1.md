---
title: "解决方案 #1"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
previous:
  title: 实时应用程序设计教程
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
next:
  title: 解决方案 2
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution2
---

\*\*为什么使用 RTOS 内核？\*\*

另请参阅常见问题“[为什么使用 RTOS？](/Why-FreeRTOS/FAQs/What-is-this-all-about#why-use-an-rtos)”。


## 概要

许多应用程序可以在不使用 RTOS 内核的情况下生成，本页介绍了可能采取的方法 
。

尽管在这种情况下，应用程序可能过于复杂，导致无法采用这种方法，但本页 
不仅着重介绍潜在的问题，而且为以下基于 RTOS 的软件设计提供对比。


## 实现

此解决方案使用传统的无限循环方法，即应用程序的每个组件 
都由一个执行到完成的函数表示。 

理想情况下，将使用硬件定时器调度时间关键型设备控制函数。但是， 
必须等待数据到来以及所执行的复杂计算使得控制函数 
不适合在中断服务程序中执行。


### 运行理念

在无限循环内调用组件的频率和顺序可以加以修改， 
以引入一些优先级。下面的示例中提供了几种此类排序替代方案。

  
### 调度器配置

未使用 RTOS 调度器。


### 评估

![](/media/2018/good.gif) 代码较小。

![](/media/2018/good.gif) 不依赖第三方源代码。

![](/media/2018/good.gif) 无 RTOS RAM、ROM 或处理开销。

![](/media/2018/bad.gif) 难以满足复杂的定时要求。

![](/media/2018/bad.gif) 如果不大幅增加复杂性，就不能很好地扩展。

![](/media/2018/bad.gif) 由于不同函数之间的相互依存关系， 
很难评估或维持定时。


### 结论

简单的循环方法非常适合小型应用程序和具有灵活定时要求的应用程序， 
但如果扩展到更大的系统，可能会变得复杂、难以分析和维护 
。


---


## 示例

此示例是先前介绍的假设应用程序的部分实现。


### 设备控制函数

控制函数可由以下伪代码表示：


```c
void PlantControlCycle( void )
{
    TransmitRequest();
    WaitForFirstSensorResponse();

    if( Got data from first sensor )
    { 
        WaitForSecondSensorResponse();
        
        if( Got data from second sensor )
        {
            PerformControlAlgorithm();
            TransmitResults();
        }
    }
}

```


### 人机界面函数

这包括键盘、液晶屏、RS232 通信和嵌入式 Web 服务器。以下伪代码 
表示用于控制这些接口的简单无限循环结构体。 

```c
int main( void )
{
    Initialise();
    
    for( ;; )
    {
        ScanKeypad();
        UpdateLCD();
        ProcessRS232Characters();
        ProcessHTTPRequests();   
    }

    // Should never get here.
    return 0;
}

```

这假设了两件事：首先，通信 IO 由中断服务程序缓冲， 
因此外围设备不需要轮询。其次，循环中的单个函数调用执行快速， 
足以满足所有最大定时要求。


---

## 调度设备控制函数

控制函数的长度意味着不能简单地从 10 毫秒定时器中断调用它。

将它添加到无限循环中需要引入一些时间控制。例如……：

```c
// Flag used to mark the time at which a
// control cycle should start (mutual exclusion
// issues being ignored for this example).
int TimerExpired;

// Service routine for a timer interrupt. This
// is configured to execute every 10ms.
void TimerInterrupt( void )
{    
    TimerExpired = true;
}


// Main() still contains the infinite loop - 
// within which a call to the plant control
// function has been added.
int main( void )
{
    Initialise();
    
    for( ;; )
    {
        // Spin until it is time for the next
        // cycle.
        if( TimerExpired )
        {
            PlantControlCycle();
            TimerExpired = false;

            ScanKeypad();
            UpdateLCD();

            // The LEDs could use a count of
            // the number of interrupts, or a
            // different timer.
            ProcessLEDs();

            // Comms buffers must be large
            // enough to hold 10ms worth of
            // data.
            ProcessRS232Characters();
            ProcessHTTPRequests();   
        }

        // The processor can be put to sleep
        // here provided it is woken by any
        // interrupt.
    }

    // Should never get here.
    return 0;
}

```

…但这不是一个可接受的解决方案：


* 现场总线延迟或故障会导致设备控制函数的执行时间增加。 
  极可能违反接口函数的定时要求。

* 每个周期执行所有函数也可能导致违反控制周期定时。

* 执行时间的抖动可能导致错过周期。例如，
  没有收到 HTTP 请求时，ProcessHTTPRequests() 可能可以忽略不计，
  但当提供页面时，此函数执行时间相当长。

* 它不是很容易维护 - 它依赖于在最大时间内执行的每个函数。

* 通信缓冲区每个周期仅维护一次，因此其长度必须大于
  其他必要长度。

---


## 替代结构

两个可确定因素限制了迄今为止描述的简单循环结构的适用性。


1. 每个函数调用的长度

   允许每个函数完全执行需要很长时间。这可以通过将每个函数拆分为 
   多个状态来防止。每次调用仅执行一个状态。将控制函数 
   作为示例：

   ```c
   // Define the states for the control cycle function.
   typdef enum eCONTROL_STATES
   {
       eStart, // Start new cycle.
       eWait1, // Wait for the first sensor response.
       eWait2  // Wait for the second sensor response.
   } eControlStates;
   
   void PlantControlCycle( void )
   {
   static eControlState eState = eStart;
   
       switch( eState )
       {
           case eStart :
               TransmitRequest();
               eState = eWait1;
               break;
               
           case eWait1;
               if( Got data from first sensor )
               {
                   eState = eWait2;
               }
               // How are time outs to be handled?
               break;
               
           case eWait2;
               if( Got data from first sensor )
               {
                   PerformControlAlgorithm();
                   TransmitResults();
                   
                   eState = eStart;
               }
               // How are time outs to be handled?
               break;           
       }
   }
   
   ```

   此函数现在在结构上更加复杂，并引入了进一步的调度问题。随着额外状态的添加，代码本身将 
   变得难以理解，例如在处理超时和错误条件时。

2. 定时器的粒度

   缩短定时器间隔将提高灵活性。 

   将控制函数实现为状态机（从而缩短每次调用的时间）可 
   允许从定时器中断调用此函数。定时器间隔必须足够短， 
   才能确保以满足定时要求的频率调用该函数。此选项 
   充满了定时和维护问题。

   或者，可以修改无限循环解决方案以在每个循环上调用不同函数， 
   更频繁地调用高优先级控制函数：

   ```c
   int main( void )
   {
   int Counter = -1;
   
       Initialise();
       
       // Each function is implemented as a state 
       // machine so is guaranteed to execute 
       // quickly - but must be called often.
    
       // Note the timer frequency has been raised.
       
       for( ;; )
       {
           if( TimerExpired )
           {
               Counter++;
               
               switch( Counter )
               {
                   case 0  : ControlCycle();
                             ScanKeypad();
                             break;
                             
                   case 1  : UpdateLCD();
                             break;
   
                   case 2  : ControlCycle();
                             ProcessRS232Characters();
                             break;
   
                   case 3  : ProcessHTTPRequests();
                             
                             // Go back to start
                             Counter = -1;                          
                             break;
                             
               }
               
               TimerExpired = false;
           }
       }
   
       // Should never get here.
       return 0;
   }
   ```

   可通过事件计数器引入更高智能，其中 
   只有在发生需要服务的事件时才调用更低优先级的函数：

   ```c
   for( ;; )
   {
       if( TimerExpired )
       {
           Counter++;
            
           // Process the control cycle every other loop.
           switch( Counter )
           {
               case 0  : ControlCycle();
                         break;
                         
               case 1  : Counter = -1;
                         break;
           }

           // Process just one of the other functions. Only process
           // a function if there is something to do. EventStatus()
           // checks for events since the last iteration.
           switch( EventStatus() )
           {
               case EVENT_KEY  :   ScanKeypad();
                                   UpdateLCD();
                                   break;
                           
               case EVENT_232  :   ProcessRS232Characters();
                                   break;
                            
               case EVENT_TCP  :   ProcessHTTPRequests();
                                   break;
           }
           
           TimerExpired = false;
       }
   }
   ```
   以这种方式处理事件将减少 CPU 周期浪费，但此设计仍将 
   带来控制周期执行频率上的抖动。
