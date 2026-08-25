---
title: 软件定时器
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## FreeRTOS 软件定时器 API 函数

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

**返回：** 

返回与软件定时器守护进程（或服务）任务
关联的任务句柄。如果在
FreeRTOSConfig.h 中将 configUSE_TIMERS 设置为 1，
则在启动 RTOS 调度器时会自动创建定时器守护进程任务。

---


### pcTimerGetName

timers.h

```c
const char * pcTimerGetName( TimerHandle_t xTimer )
```

返回创建定时器时分配给定时器的人类可读名称
。


**参数：** 

+ *xTimer*  

  正在查询的定时器的句柄。


**返回：** 

指向定时器名称的指针，该指针为以 NULL 结尾的标准 C 字符串。

---

### vTimerResetState

timers.h

```c
void vTimerResetState( void );
```

该函数可重置定时器模块的内部状态。 
在重新启动调度器之前，应用程序必须调用它。

---
