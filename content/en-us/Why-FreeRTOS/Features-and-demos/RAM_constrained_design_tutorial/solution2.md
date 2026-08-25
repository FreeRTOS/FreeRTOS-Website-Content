---
title: "Solution #2"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: Hypothetical system and requirements
    link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design
previous:
  title: Solution 1
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution1
next:
  title: Solution 3
  link: /Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/solution3
---

**A Fully Preemptive System**


## Synopsis

This is a traditional preemptive multitasking solution. 

It makes full use of the RTOS services with no regard to the resultant memory and processor overhead.

There is a simplistic partitioning of the required functionality
to a number of autonomous tasks.

---


## Implementation

A separate task is created for each part of the system that can be identified as being able to exist 
in isolation, or as having a particular timing requirement.


![](/media/2018/tasks1.gif)   
**Solution #2 functions tasks and priorities**


Tasks will block until an event indicates that processing is required. Events can either be external 
(such as a key being pressed), or internal (such as a timer expiring). This event driven approach means 
that no CPU time is wasted polling for events that have not occurred.


Priorities are allocated to tasks in accordance to their timing requirements. The stricter the timing 
requirement the higher the priority (not all priority assignment assessments are that simplistic).


### Concept of Operation

The highest priority task that is able to execute (is not blocked) is the task guaranteed by the RTOS 
to get processor time. The kernel will immediately suspend an executing task should a higher priority 
task become available.

This scheduling occurs automatically, with no explicit knowledge, structuring or commands within the 
application source code. It is however the responsibility of the application designers to ensure that 
tasks are allocated an appropriate priority.

When no task is able to execute the idle task will execute. The idle task has the option of placing the 
processor into power save mode.


### Scheduler Configuration

The scheduler is configured for preemptive operation. The kernel tick frequency should be set at the 
slowest value that provides the required time granularity.


### Evaluation

![](/media/2018/good.gif)  Simple, segmented, flexible, maintainable design with few interdependencies.

![](/media/2018/good.gif)  Processor utilisation is automatically switched from task to task on a most urgent need basis with no<br/> explicit action required within the application source code.

![](/media/2018/good.gif)  The event driven structure ensures that no CPU time is wasted polling for events that have not occurred. Processing<br/> is only performed when there is work needing to be done.

![](/media/2018/indif.gif)  Power consumption can be reduced if the idle task places the processor into power save (sleep) mode, but may<br/> also be wasted as the tick interrupt will sometimes wake the processor unnecessarily.

![](/media/2018/indif.gif)  The kernel functionality will use processing resources. The extent of this will depend on the chosen kernel<br/> tick frequency.

![](/media/2018/bad.gif)  This solution requires a lot of tasks, each of which require their own stack, and many of which require<br/> a queue on which events can be received. This solution therefore uses a lot of RAM.

![](/media/2018/bad.gif)  Frequent context switching between tasks of the same priority will waste processor cycles.


### Conclusion

This can be a good solution provided the RAM and processing capacity is available. The partitioning of 
the application into tasks and the priority assigned to each task requires careful consideration.


---

## Example

This example is a partial implementation of the hypothetical application introduced previously. The
FreeRTOS API is used.
  

### Plant Control Task

This task implements all the control functionality. It has critical timing requirements and is therefore 
given the highest priority within the system:

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

Referring to the labels within the code fragment above:

1. xLastWakeTime is initialised. This variable is used with the vTaskDelayUntil() API function to control the
   frequency at which the control function executes.

2. This function executes as an autonomous task so must never exit.

3. vTaskDelayUntil() tells the kernel that this task should start executing exactly 10ms after the time stored 
   in xLastWakeTime. Until this time is reached the control task will block. As this is the highest priority
   task within the system it is guaranteed to start executing again at exactly the correct time. It will pre-empt
   any lower priority task that happens to be running.

4. There is a finite time between data being requested from the networked sensors and that data being received.
   Data arriving on the field bus is placed in the xFieldBusQueue by an interrupt service routine, the control task
   can therefore make a blocking call on the queue to wait for data to be available. As before, because it is
   the highest priority task in the system it is guaranteed to continue executing immediately data is available.

5. As 'D', waiting for data from the second sensor.

A return value of 0 from xQueueReceive() indicates that no data arrived within the specified block period. 
This is an error condition the task must handle. This and other error handling functionality has been 
omitted for simplicity.

  
### Embedded Web Server Task

The embedded web server task can be represented by the following pseudo code. This only utilises processor 
time when data is available but will take a variable and relatively long time to complete. It is therefore 
given a low priority to prevent it adversely effecting the timing of the plant control, RS232 or keypad 
scanning tasks.

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


### RS232 Interface

This is very similar in structure to the embedded web server task. It is given a medium priority to 
ensure it does not adversely effect the timing of the plant control task.

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


### Keypad Scanning Task

This is a simple cyclical task. It is given a medium priority as its timing requirements are similar 
to the RS232 task.

The cycle time is set much faster than the specified limit. This is to account for the fact that it 
may not get processor time immediately upon request - and once executing may get pre-empted by the 
plant control task.


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

If the overall system timing were such that this could be made the lowest priority task then the call to 
vTaskDelayUntil() could be removed altogether. The key scan function would then execute continuously 
whenever all the higher priority tasks were blocked - effectively taking the place of the idle task.


### LED Task

This is the simplest of all the tasks.

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
