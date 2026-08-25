---
title: Intertask Communications
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**Design concepts and performance optimisation**


## Introduction

This page discusses the relationship between the different intertask communication API functions available 
under FreeRTOS - where a [fully featured](#the-full-featured-api), an [alternative](#the-alternative-api), and a [light weight](#the-light-weight-api) API 
are provided. The information below is intended to enable users to better select the API function to 
use under various usage scenarios, especially with respect to:

> **NOTE:** The alternative API is no longer under development, and its use
> is deprecated and not recommended for new designs.


* Function execution time.
* Interrupt responsiveness.
* Ease of use.

Outside of interrupt service routines, **the fully featured API would be the normal choice** for all 
but advanced users. It is simplest to use and makes efficient use of critical sections.


### Brief summary

The [fully featured](#the-full-featured-api) and [alternative](#the-alternative-api) API provide the same functionality - but implemented 
in different ways.  The source code that implements the alternative (Alt) API is much simpler because it 
executes everything from within a critical section.  This is the approach taken by many other RTOSes but 
is less sophisticated than the preferred fully featured API. The fully featured API has more complex code 
that takes longer to execute, but makes much less use of critical sections. Therefore the alternative API 
sacrifices interrupt responsiveness to gain API function execution speed, whereas the fully featured API 
sacrifices API function execution speed to ensure better interrupt responsiveness.

The [light weight](#the-light-weight-api) API alternative offers even faster execution times, again at the expense of 
interrupt responsiveness and also a little more complexity from the application writer's point of view. Use 
of the light weight API is therefore considered to be within the 'advanced topics' category, and is intended 
for the more experienced users only.

The API reference should be consulted for information of a more functional nature, for example, details 
of the function parameters.


### Design goals and concepts

FreeRTOS was designed to have a small ROM footprint. To this end, all intertask communications are built 
around a single queue primitive - greatly limiting the amount of source code required. Further to this,
all event management functionality is built into the queue data structures. This second point is contrary 
to other RTOS designs where an event control block is often a separate entity in its own right.

The queue mechanism is used to implement:

1. The queues themselves
2. Semaphores - which are implemented as macros that uses queues and therefore introduce no new code
3. Mutexes - which are also implemented as macros that use queues, introducing only a small amount of new code

FreeRTOS can easily be extended to include other intertask communication mechanisms in the same manner.

As all communication mechanisms are based on the same underlying queue concept, the API functions provided 
for each mechanism are in fact relatively interoperable.
  

---

## The full featured API

This relates to the following functions:

* xQueueSend()
* xQueueSendToBack()
* xQueueSendToFront()
* xQueueReceive()
* xQueuePeek()
* xSemaphoreTake()
* xSemaphoreGive()


### Function characteristics

These functions are classed as fully featured for the following reasons:

1. They utilise the queue and RTOS scheduler locking mechanisms. This allows the use of critical sections 
   (within the API function itself) to be minimised - ensuring minimum impact on interrupt responsiveness 
   no matter how big the data being queued.

2. They automatically cause a context switch should reading from or writing to the queue cause a task of 
   higher priority to unblock.

3. They are (naturally) thread safe.

4. They are interrupt safe - in the sense that both a task and an interrupt can access the queue simultaneously. 
   Please note that they are **not** interrupt safe in the sense that they can be called from within an 
   ISR, where only the light weight API must be used.

Being fully featured, these functions are internally complex, but this complexity is hidden from the user 
so they are simple to use.

The fully featured API functions take longer to execute than their alternative and light weight counterparts. 
This is because more code is required for their implementation. We see therefore a trade off between function 
execution time and efficient use of critical sections.


### Full featured API conclusions

When compared to the [alternative](#the-alternative-api) and [light weight](#the-light-weight-api) API, the full featured API functions:


* ![](/media/2018/good.gif) Have a lower impact on interrupt response times.
* ![](/media/2018/good.gif) Are simpler to use. The RTOS kernel takes care of thread/interrupt 
  safety, and task prioritisation.
* ![](/media/2018/bad.gif)  Are larger, and therefore take longer to execute.


---

## The alternative API

This relates to the following functions:

* xQueueAltSend()
* xQueueAltSendToBack()
* xQueueAltSendToFront()
* xQueueAltReceive()
* xQueueAltPeek()
* xSemaphoreAltTake()
* xSemaphoreAltGive()


Usage of these functions is demonstrated by the standard demo source files that have a filename 
starting "Alt", located in the FreeRTOS/Demo/Common/Minimal directory.

  
### Function characteristics

These API functions are functionally identical to their fully featured counterparts, but are implemented 
in a less sophisticated way.

They use crude critical sections in place of the queue and RTOS scheduler locking mechanisms utilised 
by their fully featured counterparts. This simplifies the code and improves execution speed, but increases 
the amount of time spent inside critical sections and therefore has a comparatively negative impact on 
interrupt response times. Also, unlike the fully featured versions, interrupts being disabled while
the queue is accessed means that interrupts and tasks cannot access the queue simultaneously.

The alternative API functions take less time to execute than the fully featured API functions, but more 
time to execute than their light weight counterparts.


### Alternative API conclusions

When compared to the [fully featured](#the-full-featured-api) API, the alternative API functions:

* ![](/media/2018/bad.gif)  Have a higher impact on interrupt response times.
* ![](/media/2018/indif.gif)  Have equivalent function call prototypes so are therefore 
  neither simpler nor more complex to use.   |
* ![](/media/2018/good.gif)  Are smaller, and therefore take less time to execute 
  (although more time than the light weight alternatives).   |

---

## The light weight API

This relates to the following functions:

* xQueueSendFromISR()
* xQueueSendToBackFromISR()
* xQueueSendToFrontFromISR()
* xQueueReceiveFromISR()
* xSemaphoreGiveFromISR()

These are the functions that can be used from within an ISR, and are named accordingly for ease of 
recognition. Please note however that their use need not be restricted purely to within interrupts. 
They can be used within tasks in order to boost run time efficiency. More information is provided below.
  

### Function characteristics

1. These functions are much simpler than their full featured or alternative versions. Their implementation 
   uses less code and they therefore execute more quickly.

2. They are designed to be safe for use within an interrupt so in themselves make no attempt to be interrupt 
   safe. This means their use within an interrupt is simple, but their use outside of an interrupt requires 
   special consideration.

3. They also do not automatically perform a context switch should reading or writing to the queue cause 
   a task of higher priority to unblock. Instead they return a value indicating whether or not a context 
   switch is required.

The light weight functions provide more flexibility by leaving more decisions to the application writer. 
This provides the application designer greater choice in trading off function execution time against 
interrupt responsiveness - but care needs to be taken in how this flexibility is used. More information is
provided on this in the following sections of this page.
  

### Light weight API conclusions

When compared to the [fully featured](#the-full-featured-api) API, the light weight API functions:

* ![](/media/2018/good.gif)  Are simple to use when called from within an interrupt.
* ![](/media/2018/good.gif)  Are smaller, and more flexible. They therefore offer 
  an opportunity to improve run time performance by allowing the application  designer to tailor the 
  trade off between execution timing and interrupt responsiveness. 
* ![](/media/2018/bad.gif)  Require special consideration when called from a task, 
  rather than an interrupt.   


---

## FreeRTOS performance tips and tricks: Using the light weight API outside of an interrupt

*This information is intended for more experienced users only.*

The following subsections detail how and where the light weight API functions can be used in place 
of their full featured and alternative versions. A series of examples demonstrate different usage 
scenarios, starting from very basic fast use, then adding in more functionality.

Please **note** that these examples relate only to the use of the light weight API functions outside 
of an ISR. The API functions are named to include the text "FromISR" to indicate that they are safe 
to use from within an ISR, not that they are exclusively for use inside an ISR.


### Light weight example 1 - basic fast usage

The following code shows the fastest way of sending and receiving a message from one task to another:

---
```c
    void vAFunction( void )
    {
        /* Fast send to queue. Passing pdTRUE prevents the function
           attempting to unblock a task. */
        xQueueSendToFrontFromISR( xQueue, pvItemToQueue, pdTRUE );
    }

    void vAnotherFunction( void )
    {
        /* Setting this to true will prevent the function attempting to
           unblock a task. */
        signed BaseType_t x = pdTRUE;

        /* Fast receive from queue. */
        xQueueReceiveFromISR( xQueue, pvBuffer, &x );
    }
```
**Listing 1: The fastest way to send or receive a message**
---

The description of the light weight API above notes that, unlike the full featured variants, these API 
functions do not do anything to ensure thread or interrupt safety.

Notes:

* The parameters passed to the functions in listing 1 prevent the functions from attempting to unblock 
  any tasks that may be blocked waiting for queue events. This means thread safety is not an issue when 
  used with the cooperative RTOS scheduler - it does mean though that in this form the light weight API 
  should only be used when the task accessing the other end of the queue does so without blocking.

* In this form the API functions are not interrupt or preemption safe, meaning this is **not** an 
  appropriate usage if an interrupt makes use of the same queue, or the task accessing the queue could be 
  preempted by a task that accesses the same queue.


### Light weight example 2 - allowing tasks to be unblocked

The following code shows how Listing 1 can be extended to allow the light weight API functions to unblock a task.

---
```c
    void vAFunction( void )
    {
        /* Fast send to queue. Passing pdFALSE makes the function look
           to see if a task requires unblocking. */
        if( xQueueSendToFrontFromISR( xQueue, pvItemToQueue, pdFALSE ) )
        {
            /* Writing to the queue unblocked a task of higher priority,
               force a context switch. This would be done within the API
               function if using the fully featured variant. */
            taskYIELD();
        }
    }

    void vAnotherFunction( void )
    {
        /* Setting this to false will make the function look to see
           if a task requires unblocking. */
        signed BaseType_t x = pdFALSE;

        /* Fast receive from queue. */
        xQueueReceiveFromISR( xQueue, pvBuffer, &x );

        if( x == pdTRUE )
        {
            /* Reading from the queue unblocked a task of higher priority,
               force a context switch. This would be done within the API
               function if using the fully featured variant. */
            taskYIELD();
        }
    }
```
**Listing 2: Unblocking tasks using the light weight API**
---

Notes:

* We have done nothing between Listing 1 and Listing 2 to ensure interrupt safety. This is therefore 
  still **not** appropriate usage if the queue is also accessed from an ISR.

* The parameters passed to the functions in listing 2 allow the functions to unblock any tasks that 
  might be blocked waiting for queue events. This is therefore **not** appropriate usage if using the 
  preemptive RTOS scheduler. It provides a nice mechanism when using the co-operative RTOS scheduler only.


### Light weight example 3 - introducing preemption and interrupt safety

The following code updates that presented in Listing 2 to make the light weight API usage both preemption 
and interrupt safe. The entire call to the API function is placed within a critical section, adversely 
effecting interrupt response timing. This method therefore trades off interrupt response times for improved 
execution time, whereas the full featured versions of these API functions do the opposite - they instead 
trade off execution time for improved interrupt response times.

---
```c
    void vAFunction( void )
    {
    BaseType_t xYieldRequired;

        /* Fast send to queue. Passing pdFALSE makes the function look
           to see if a task requires unblocking. Note the fully featured
           version of this API function uses critical sections in a much
           more efficient manner than this! */
        taskENTER_CRITICAL();
            xYieldRequired = xQueueSendToFrontFromISR( xQueue, pvItemToQueue, pdFALSE );
        taskEXIT_CRITICAL();

        if( xYieldRequired )
        {
            /* Writing to the queue unblocked a task of higher priority,
               force a context switch. This would be done within the API
               function if using the fully featured variant. */
            taskYIELD();
        }
    }

    void vAnotherFunction( void )
    {
        /* Setting this to false will make the function look to see
           if a task requires unblocking. */
        signed BaseType_t x = pdFALSE;

        /* Fast receive from queue. The full featured version
           of this API function uses critical sections in a much more
           efficient manner than this! */
        taskENTER_CRITICAL();
            xQueueReceiveFromISR( xQueue, pvBuffer, &x );
        taskEXIT_CRITICAL();

        if( x == pdTRUE )
        {
            /* Reading from the queue unblocked a task of higher priority,
               force a context switch. This would be done within the API
               function if using the fully featured variant. */
            taskYIELD();
        }
    }
```
**Listing 3: Full preemption and interrupt safety - the full featured API versions do not execute the 
entire queue function in a critical section in the manner shown here!** 
---

Notes:

* Macros can be provided to facilitate the use of the light weight API in this manner.

* Used in this way the light weight API provides similar functionality to the fully featured API versions, 
  but with less efficient use of critical sections.


### What about using semaphores and mutexes?

The principles demonstrated here for accessing queues also apply when accessing semaphores and mutexes.
