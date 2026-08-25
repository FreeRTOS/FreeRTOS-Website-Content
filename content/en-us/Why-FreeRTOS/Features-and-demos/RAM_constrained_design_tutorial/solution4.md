---
title: "Solution #4"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: Hypothetical system and requirements
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: Solution 3
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution3
---

**Reducing the Processor Overhead**

> **NOTE:** These pages have not been updated since the introduction of FreeRTOS V4.0.0. V4.0.0 introduces 
> the concept of co-routines which would provide a different and novel solution to those presented here. 
> The [Tasks and Co-routines](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines) documentation provides further information.


## Synopsis

Solution #2 showed how a clean application can be produced by fully utilising the RTOS functionality.
Solution #3 showed how this can be adapted for embedded computers with limited RAM resource. Solution #4 
makes further modifications with the objective of a reduction in the RTOS processing overhead.

A hybrid scheduling algorithm (neither fully preemptive or fully cooperative) is created by configuring 
the kernel for cooperative scheduling, then performing context switching from within event interrupt 
service routines.


## Implementation

![](/media/2018/tasks3.gif)   
**Solution #4 functions tasks and priorities**

The critical plant control functionality is once again implemented by a high priority task but the 
use of the cooperative scheduler necessitates a change to its implementation. Previously the timing 
was maintained using the vTaskDelayUntil() API function. When the preemptive scheduler was used, assigning 
the control task the highest priority ensured it started executing at exactly the specified time. Now the 
cooperative scheduler is being used - therefore a task switch will only occur when explicitly requested 
from the application source code so the guaranteed timing is lost.

Solution #4 uses an interrupt from a peripheral timer to ensure a context switch is requested at the exact
frequency required by the control task. The scheduler ensures that each requested context switch results in 
a switch to the highest priority task that is able to run. 

The keypad scanning function also requires regular processor time so it too is executed within the task 
triggered by the timer interrupt. The timing of this task can be easily evaluated;

The worst case processing time of the control function is given by the error case - when no data is forthcoming 
from the networked sensors causing the control function to time out. The execution time of the keypad scanning 
function is basically fixed. We can therefore be certain that chaining their functionality in this manner will 
never result in jitter in the control cycle frequency - or worse still a missed control cycle.

The RS232 task will be scheduled by the RS232 interrupt service routine.

The flexible timing requirements of the LED functionality means it can probably join the embedded web server 
task within the idle task hook.  If this is not adequate then it too can be moved up to the high priority task.


### Concept of Operation

The cooperative scheduler will only perform a context switch when one is explicitly requested. This greatly 
reduces the processor overhead imposed by the RTOS (except for the fact that the idle task can no longer put 
the processor into a power saving mode?)].  The idle task, including the embedded web server functionality, 
will execute without any unnecessary interruptions from the kernel.

An interrupt originating from either the RS232 or timer peripheral will result in a context switch exactly 
and only when one is necessary. This way the RS232 task will still pre-empt the idle task, and can still 
itself be pre-empted by the plant control task - maintaining the prioritised system functionality.


### Scheduler Configuration

The scheduler is configured for cooperative operation. The kernel tick is used to maintain the real time 
tick value only.


### Evaluation

![](/media/2018/good.gif) Creates only two application tasks so therefore uses much 
less RAM than solution #2. 

![](/media/2018/indif.gif) The RTOS context switching overhead is reduced to a 
minimum - although more CPU cycles might be utilised by the idle  task which can no longer make use 
of power saving modes.

![](/media/2018/indif.gif) Only a subset of the RTOS features are used. This 
necessitates a greater consideration of the timing and  execution environment at the application source 
code level, but still allows for a greatly simplified design  (when compared to solution #1).

![](/media/2018/bad.gif) Reliance on processor peripherals. Non portable.

![](/media/2018/bad.gif) The problems of analysis and interdependencies between 
modules as were identified with solution #1 are starting  to become a consideration again - although to 
a much lesser extent.

![](/media/2018/bad.gif) The design might not scale if the application grows too large.


### Conclusion

Features of the RTOS kernel can be used with very little overhead, enabling a simplified design even 
on systems where processor and memory constraints prevent a fully preemptive solution.

---


## Example

This example is a partial implementation of the hypothetical application introduced previously. The
FreeRTOS API is used.
  

### High Priority Task

The high priority task is triggered by a semaphore 'given' by a periodic interrupt service routine:

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

Note that the syntax used to force a context switch from within an ISR is different for different ports. 
Do not copy this example directly but instead check the documentation for the port you are using.

The high priority task contains both the plant control and keypad functionality. PlantControlCycle() 
is called first to ensure consistency in its timing. 

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

### RS232 Task

The RS232 task simply blocks on a queue waiting for data to arrive. The RS232 interrupt service routine 
must post the data onto the queue - making the task ready to run - then force a context switch. This 
mechanism is as per the timer interrupt pseudo code given above.

The RS232 task can therefore be represented by the following pseudo code:

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

### The Embedded Web Server and LED Functionality

The remaining system functionality is placed within the idle task hook. This is simply a function that is called
by each cycle of the idle task.

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
