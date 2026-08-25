---
title: Software Timers
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## FreeRTOS Software Timer API Functions

* [xTimerCreate](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
* [xTimerCreateStatic](/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic)
* [xTimerIsTimerActive](/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive)
* [pvTimerGetTimerID](/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)
* [pcTimerGetName](/Documentation/02-Kernel/04-API-references/11-Software-timers/19-pcTimerGetName)
* [vTimerSetReloadMode](/Documentation/02-Kernel/04-API-references/11-Software-timers/14-vTimerSetReloadMode)
* [xTimerStart](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)
* [xTimerStop](/Documentation/02-Kernel/04-API-references/11-Software-timers/05-xTimerStop)
* [xTimerChangePeriod](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
* [xTimerDelete](/Documentation/02-Kernel/04-API-references/11-Software-timers/07-xTimerDelete)
* [xTimerReset](/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset)
* [xTimerStartFromISR](/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR)
* [xTimerStopFromISR](/Documentation/02-Kernel/04-API-references/11-Software-timers/10-xTimerStopFromISR)
* [xTimerChangePeriodFromISR](/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR)
* [xTimerResetFromISR](/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR)
* [vTimerResetState](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/#vtimerresetstate)
* [pvTimerGetTimerID](/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)
* [vTimerSetTimerID](/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID)
* [xTimerGetTimerDaemonTaskHandle](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/#xtimergettimerdaemontaskhandle)
* [xTimerPendFunctionCall](/Documentation/02-Kernel/04-API-references/11-Software-timers/17-xTimerPendFunctionCall)
* [xTimerPendFunctionCallFromISR](/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR)
* [xTimerGetPeriod](/Documentation/02-Kernel/04-API-references/11-Software-timers/20-xTimerGetPeriod)
* [xTimerGetExpiryTime](/Documentation/02-Kernel/04-API-references/11-Software-timers/21-xTimerGetExpiryTime)
* [xTimerGetReloadMode](/Documentation/02-Kernel/04-API-references/11-Software-timers/23-xTimerGetReloadMode)

---


### xTimerGetTimerDaemonTaskHandle

timers.h
 
```c
TaskHandle_t xTimerGetTimerDaemonTaskHandle( void );
```

**Returns:** 

Returns the task handle associated with the software timer daemon
(or service) task. If configUSE\_TIMERS is set to 1 in
FreeRTOSConfig.h, then the timer daemon task is created
automatically when the RTOS scheduler is started.
 
---


### pcTimerGetName

timers.h
 
```c
const char * pcTimerGetName( TimerHandle_t xTimer )
```

Returns the human readable name assigned to a timer when the timer was
created.
 

**Parameters:** 

+ *xTimer*  

  The handle of the timer being queried.


**Returns:** 

A pointer to the timer's name, which is a standard NULL terminated C string.
 
---

### vTimerResetState

timers.h
 
```c
void vTimerResetState( void );
```

This function resets the internal state of the timer module. 
It must be called by the application before restarting the scheduler.
 
---
