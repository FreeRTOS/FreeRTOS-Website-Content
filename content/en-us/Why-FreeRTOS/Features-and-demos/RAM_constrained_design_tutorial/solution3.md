---
title: "Solution #3"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: Hypothetical system and requirements
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: Solution 2
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution2
next:
  title: Solution 4
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution4
---

** Reducing RAM Utilisation**

> **NOTE:** These pages have not been updated since the introduction of FreeRTOS V4.0.0. V4.0.0 introduces 
> the concept of co-routines which would provide a different and novel solution to those presented here. 
> The [Tasks and Co-routines](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines) documentation provides further information.

## Synopsis

Solution #2 makes full use of the RTOS. This results in a clean design, but one that can only be used 
on embedded computers with ample RAM and processing resource. Solution #3 attempts to reduce the RAM 
usage by changing the partitioning of functionality into tasks.

---

## Implementation

![](/media/2018/tasks2.gif)   
**Solution #3 functions tasks and priorities** 

We have [previously seen](/Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design#the-hypothetical-application) how the timing requirements of our hypothetical application 
can be split into three categories:

1. **Strict timing** - the plant control

   As before, a high priority task is created to service the critical control functionality.

2. **Deadline only timing** - the human interfaces

   Solution #3 groups the RS232, keyscan and LED functionality into a single medium priority task. 
 
   For reasons previously stated it is desirable for the embedded web server task to operate at a lower 
   priority. Rather than creating a task specifically for the web server an idle task hook is implemented 
   to add the web server functionality to the idle task. The web server must be written to ensure it never 
   blocks!

3. **Flexible timing** - the LED

   The LED functionality is too simple to warrant its own task if RAM is at a premium. For reasons of 
   demonstration this example includes the LED functionality in the single medium priority task. It could 
   of course be implemented in a number of ways (from a peripheral timer for example).

Tasks other than the idle task will block until an event indicates that processing is required. Events 
can either be external (such as a key being pressed), or internal (such as a timer expiring). 

### Concept of Operation

The grouping of functionality into the medium priority task has three important advantages over the 
infinite loop implementation presented in solution #1:

1. The use of a queue allows the medium priority task to block until an event causes data to be 
   available - and then immediately jump to the relevant function to handle the event. This prevents 
   wasted processor cycles - in contrast to the infinite loop implementation whereby an event will 
   only be processed once the loop cycles to the appropriate handler.

2. The use of the real time kernel removes the requirement to explicitly consider the scheduling of 
   the time critical task within the application source code.

3. The removal of the embedded web server function from the loop has made the execution time more 
   predictable.

In addition, the functionality that has been grouped into a single task is taken from several tasks 
that previously shared the same priority anyway (barr the LED function). The frequency at which code 
at this priority executes will not alter whether in a single or multiple tasks.

The plant control task, as the highest priority task, is guaranteed to be allocated processing time 
whenever it requires. It will pre-empt the low and medium priority tasks if necessary. The idle task 
will execute whenever both application tasks are blocked. The idle task has the option of placing the 
processor into power save mode. 

### Scheduler Configuration

The scheduler is configured for preemptive operation. The kernel tick frequency should be set at the 
slowest value that provides the required time granularity. 

### Evaluation

![](/media/2018/good.gif)  Creates only two application tasks so therefore uses 
much less RAM than solution #2.

![](/media/2018/good.gif)  Processor utilisation is automatically switched from 
task to task on a most urgent need basis.  

![](/media/2018/good.gif)  Utilising the idle task effectively creates three 
application task priorities with the overhead of only two.

![](/media/2018/indif.gif)  The design is still simple but the execution time 
of the functions within the medium priority task   could introduce timing issues. The separation of 
the embedded web server task reduces this risk and in any case  any such issues would not affect the 
plant control task.

![](/media/2018/indif.gif)  Power consumption can be reduced if the idle task 
places the CPU into power save (sleep) mode, but may  also be wasted as the tick interrupt will sometimes 
wake the CPU unnecessarily.

![](/media/2018/indif.gif)  The RTOS functionality will use processing resources. 
The extent of this will depend on the chosen kernel  tick frequency.

![](/media/2018/bad.gif)  The design might not scale if the application grows too 
large.

### Conclusion

This can be a good solution for systems with limited RAM but it is still processor intensive.
Spare capacity within the system should be checked to allow for future expansion. 

---

## Example

This example is a partial implementation of the hypothetical application introduced previously. The
FreeRTOS API is used.

### Plant Control Task

The plant control task is identical to that [described in solution #2](solution2#pcf).

### The Embedded web Server

This is simply a function that is called from the idle task and runs to completion.

### The medium Priority Task

The medium priority task can be represented by the following pseudo code.

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

Referring to the labels within the code fragment above:

1. The task first blocks waiting for a communications event. The block time is relatively short.

2. The do-while loop executes until no data remains in the queue. This implementation would have 
   to be modified if data arrives too quickly for the queue to ever be completely empty.

3. Either the queue has been emptied of all data, or no data arrived within the specified blocking 
   period. The maximum time that can be spent blocked waiting for data is short enough to ensure the 
   keypad is scanned frequently enough to meet the specified timing constraints.

4. Check to see if it is time to flash the LED. There will be some jitter in the frequency at which 
   this line executes, but the LED timing requirements are flexible enough to be met by this 
   implementation.

---
