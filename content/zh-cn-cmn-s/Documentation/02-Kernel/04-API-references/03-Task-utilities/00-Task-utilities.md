---
title: 任务实用程序
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 模块

* [uxTaskGetSystemState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)
* [vTaskGetInfo](/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo)
* [xTaskGetCurrentTaskHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle)
* [xTaskGetIdleTaskHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetidletaskhandle)
* [uxTaskGetStackHighWaterMark](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
* [eTaskGetState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#etaskgetstate)
* [pcTaskGetName](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#pctaskgetname)
* [xTaskGetHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)
* [xTaskGetTickCount](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgettickcount)
* [xTaskGetTickCountFromISR](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgettickcountfromisr)
* [xTaskGetSchedulerState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetschedulerstate)
* [uxTaskGetNumberOfTasks](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ustaskgetnumberoftasks)
* [vTaskList](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtasklist)
* [vTaskListTasks](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtasklisttasks)
* [vTaskStartTrace](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskstarttrace)
* [ulTaskEndTrace](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ustaskendtrace)
* [vTaskGetRunTimeStats](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestats)
* [vTaskGetRunTimeStatistics](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestatistics)
* [vTaskGetIdleRunTimeCounter](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetidleruntimecounter)
* [ulTaskGetRunTimeCounter](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ultaskgetruntimecounter)
* [ulTaskGetRunTimePercent](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ultaskgetruntimepercent)
* [ulTaskGetIdleRunTimeCounter](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ultaskgetidleruntimecounter)
* [ulTaskGetIdleRunTimePercent](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ultaskgetidleruntimepercent)
* [vTaskSetApplicationTaskTag](/Documentation/02-Kernel/04-API-references/03-Task-utilities/06-vTaskSetApplicationTag)
* [xTaskGetApplicationTaskTag](/Documentation/02-Kernel/04-API-references/03-Task-utilities/03-xTaskGetApplicationTaskTag)
* [xTaskCallApplicationTaskHook](/Documentation/02-Kernel/04-API-references/03-Task-utilities/05-xTaskCallApplicationTaskHook)
* [pvTaskGetThreadLocalStoragePointer](/Documentation/02-Kernel/04-API-references/03-Task-utilities/08-pvTaskGetThreadLocalStoragePointer)
* [vTaskSetThreadLocalStoragePointer](/Documentation/02-Kernel/04-API-references/03-Task-utilities/07-vTaskSetThreadLocalStoragePointer)
* [vTaskSetTimeOutState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/09-vTaskSetTimeOutState)
* [xTaskCheckForTimeOut](/Documentation/02-Kernel/04-API-references/03-Task-utilities/10-xTaskCheckForTimeOut)
* [vTaskResetState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskresetstate)

### xTaskGetCurrentTaskHandle

task.h

```c
TaskHandle_t xTaskGetCurrentTaskHandle( void );
```

`INCLUDE_xTaskGetCurrentTaskHandle` 必须设置为 1，才可使用此函数。

**返回：**

- 当前正在运行（调用）的任务的句柄。

---

### xTaskGetIdleTaskHandle

task.h

```c
TaskHandle_t xTaskGetIdleTaskHandle( void );
```

`INCLUDE_xTaskGetIdleTaskHandle` 必须设置为 1，才可使用此函数。

**返回：**

- 与空闲任务关联的任务句柄。RTOS 调度器启动时，自动创建空闲任务。

---

### eTaskGetState

task.h

```c
eTaskState eTaskGetState( TaskHandle_t xTask );
```

返回在执行 `eTaskGetState()` 时任务所处状态作为枚举类型。

`INCLUDE_eTaskGetState` 必须在 FreeRTOSConfig.h 中设置为 1，才可使用 `eTaskGetState()`。

另请参阅 [vTaskGetInfo()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo)。

**参数：**

- *xTask*

主题任务（正在查询的任务）的句柄。

**返回：**

下表列出了 `eTaskGetState()`
针对 `xTask` 参数引用的任务可能所处的每种状态返回的值。

| **状态** | **返回值** |
| --- | --- |
|  准备就绪  | eReady  |
|  运行  | eRunning（调用任务正在查询自己的优先级）  |
|  已阻塞  | eBlocked  |
|  已挂起  | eSuspended  |
|  已删除  | eDeleted（任务 TCB 正在等待清理）  |

---

### pcTaskGetName

task.h

```c
char * pcTaskGetName( TaskHandle_t xTaskToQuery );
```

从任务的句柄中查找任务的名称。

**参数：**

- *xTaskToQuery*

  所查询任务的句柄。xTaskToQuery 可以设置为 NULL，以查询调用任务的名称。

**返回：**

- 指向主题任务名称的指针，它是一个标准的以 NULL 结尾的 C 字符串。

---

### xTaskGetHandle

task.h

```c
TaskHandle_t xTaskGetHandle( const char *pcNameToQuery );
```

从任务的名称中查找任务的句柄。

注意：此函数需要较长时间才能完成，
因此每个任务只能调用一次。获取任务句柄后，
该函数将储存在本地，以供再次使用。

`INCLUDE_xTaskGetHandle` 必须在 FreeRTOSConfig.h 中设置为 1，才可使用 `xTaskGetHandle()`。

**参数：**

- *pCNAMEToQuery*

  将返回句柄的任务的文本名称（以 NULL 结尾的标准 C 字符串）。

  请参阅 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 和 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) API 函数的 `pcName` 参数，
  了解如何设置任务的文本名称。

**返回：**

- 如果能够找到名称与 `pcNameToQuery` 传递的名称相匹配的任务，
  则返回任务句柄，否则返回 NULL。

---

### xTaskGetTickCount

task.h

```c
volatile TickType_t xTaskGetTickCount( void );
```

无法从 ISR 调用此函数。请使用 `xTaskGetTickCountFromISR()` 代替。

**返回：**

- 自调用 vTaskStartScheduler 以来的滴答数。

---

### xTaskGetTickCountFromISR

task.h

```c
volatile TickType_t xTaskGetTickCountFromISR( void );
```

可以从 ISR 中调用的 xTaskGetTickCount() 版本。

**返回：**

- 自调用 vTaskStartScheduler 以来的滴答数。

---

### xTaskGetSchedulerState

task.h

```c
BaseType_t xTaskGetSchedulerState( void );
```

**返回：**

- 以下任一常量（在 task.h 中定义）：`taskSCHEDULER_NOT_STARTED`、`taskSCHEDULER_RUNNING`、`taskSCHEDULER_SUSPENDED`。

`INCLUDE_xTaskGetSchedulerState` 或 `configUSE_TIMERS` 必须在 FreeRTOSConfig.h 中设置为 1，才可使用此函数。

---

### uxTaskGetNumberOfTasks

task.h

```c
UBaseType_t uxTaskGetNumberOfTasks( void );
```

**返回：**

- RTOS 内核当前正在管理的任务数。这包括所有准备就绪、阻塞和
  挂起的任务。已删除但尚未被空闲任务释放的任务也将包含
  在计数中。

---

### vTaskList

task.h

```c
void vTaskList( char *pcWriteBuffer );
```

`configUSE_TRACE_FACILITY` 和 `configUSE_STATS_FORMATTING_FUNCTIONS`
必须在 FreeRTOSConfig.h 中定义为 1，才可使用此函数。
有关详细信息，请参阅[配置部分](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

注意：此函数在执行期间会禁用中断。它不是作为
一种正常的应用程序运行时的工具，而是作为调试辅助工具。

`vTaskList()` 调用 [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)，然后
将 `uxTaskGetSystemState()` 生成的原始数据转换为易于阅读的 (ASCII) 表格形式，表格中会显示每个任务的状态，
其中包括任务的堆栈高水位线（堆栈高水位线数字越小，
表示任务越接近堆栈溢出）。

[点击此处，查看生成的输出结果示例](/media/2018/log.gif)。

在 ASCII 表中，以下字母用于表示任务的状态：

* 'B' - 已阻塞
* 'R' - 准备就绪
* 'D' - 已删除（等待清理）
* 'S' - 已挂起或已阻塞，没有超时

`vTaskList()` 是一个仅为方便起见而提供的实用程序函数，并不属于内核。
有关生成类似运行时任务利用率信息表的实用程序函数，请参阅 [vTaskGetRunTimeStats()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestats)
。

**参数：**

- *pcWriteBuffer*

  上述详细信息将以 ASCII 形式写入的缓冲区。假设此缓冲区
  的大小足以容纳生成的报告。大约为每个任务分配 40 字节的缓冲区就足够了。

---

### vTaskListTasks

task.h

```c
void vTaskListTasks( char *pcWriteBuffer, size_t uxBufferLength );
```

`configUSE_TRACE_FACILITY` 和 `configUSE_STATS_FORMATTING_FUNCTIONS`
必须在 FreeRTOSConfig.h 中定义为 1，才可使用此函数。
有关详细信息，请参阅[配置部分](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

注意：此函数在执行期间会禁用中断。它不是作为
一种正常的应用程序运行时的工具，而是作为调试辅助工具。

`vTaskListTasks()` 调用 [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)，然后
将 `uxTaskGetSystemState()` 生成的原始数据转换为易于阅读的 (ASCII) 表格形式，表格中会显示每个任务的状态，
其中包括任务的堆栈高水位线（堆栈高水位线数字越小，
表示任务越接近堆栈溢出）。

[点击此处，查看生成的输出结果示例](/media/2018/log.gif)。

在 ASCII 表中，以下字母用于表示任务的状态：

* 'B' - 已阻塞
* 'R' - 准备就绪
* 'D' - 已删除（等待清理）
* 'S' - 已挂起或已阻塞，没有超时

`vTaskListTasks()` 是一个仅为方便起见而提供的实用程序函数，并不属于内核。

**参数：**

- *pcWriteBuffer*

  上述详细信息将以 ASCII 形式写入的缓冲区。假设此缓冲区
  的大小足以容纳生成的报告。大约为每个任务分配 40 字节的缓冲区就足够了。

- *uxBufferLength*

  pcWriteBuffer 的长度。

---

### vTaskStartTrace

task.h

```c
void vTaskStartTrace( char * pcBuffer, unsigned long ulBufferSize );
```

[此函数与旧版跟踪实用程序相关，后者已从 FreeRTOS V7.1.0 中删除，用户可能会发现
新版[跟踪钩子宏](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature)更容易使用，功能也更强大。]

启动 RTOS 内核活动跟踪。跟踪记录何时运行任务的标识。

跟踪文件以二进制格式存储。可以使用名为 convtrce.exe 的单独 DOS 实用程序
将其转换为制表符分隔的文本文件，该文件可以在电子表格中查看和绘制。

**参数：**

- *pcBuffer*

  跟踪将写入的缓冲区。

- *ulBufferSize*

  pcBuffer 的大小（以字节为单位）。跟踪将持续到缓冲区已满或 `ulTaskEndTrace()`
  被调用。

---

### ulTaskEndTrace

task.h

```c
unsigned long ulTaskEndTrace( void );
```

[此函数与旧版跟踪实用程序相关，后者已从 FreeRTOS V7.1.0 中删除，用户可能会发现
新版[跟踪钩子宏](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature)更容易使用，功能也更强大。]

停止 RTOS 内核活动跟踪。请参阅 vTaskStartTrace()。


**返回：**

- 已写入跟踪缓冲区的字节数。

---

### vTaskGetRunTimeStats

task.h

```c
void vTaskGetRunTimeStats( char *pcWriteBuffer );
```

请参阅[运行时统计](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)页面，获取此功能的完整说明。

`configGENERATE_RUN_TIME_STATS`、`configUSE_STATS_FORMATTING_FUNCTIONS` 和 `configSUPPORT_DYNAMIC_ALLOCATION`
必须定义为 1，才可使用此函数。此外，应用程序还必须提供
`portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` 和 `portGET_RUN_TIME_COUNTER_VALUE` 的定义，分别用于配置外设
定时器/计数器和返回定时器的当前计数值。计数器的频率应该至少是
滴答计数的 10 倍

注意：此函数在执行期间会禁用中断。它
不是作为正常的应用程序运行时的工具，而是作为调试辅助工具。

`vTaskGetRunTimeStats()` 调用 [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)，
然后将 `uxTaskGetSystemState()` 生成的原始数据转换为
易于阅读的 (ASCII) 表格形式，表格中会显示
每个任务在运行状态下所花费的时间（即每个任务消耗的 CPU 时间量）。数据以
绝对值和百分比值的形式提供。绝对值的分辨率
取决于应用程序提供的运行时间统计时钟的频率。

`vTaskGetRunTimeStats()` 是一个仅为方便起见而提供的实用程序函数，它
不属于内核。请参阅 [vTaskList()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtasklist)，
了解生成各任务状态信息的实用程序函数。

**参数：**

- *pcWriteBuffer*

  执行时间将以 ASCII 形式写入的缓冲区。假设此缓冲区
  的大小足以容纳生成的报告。大约为每个任务分配 40 字节的缓冲区就足够了。

---

### vTaskGetRunTimeStatistics

task.h

```c
void vTaskGetRunTimeStatistics( char *pcWriteBuffer, size_t uxBufferLength );
```

请参阅[运行时统计](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)页面，获取此功能的完整说明。

`configGENERATE_RUN_TIME_STATS`、`configUSE_STATS_FORMATTING_FUNCTIONS` 和 `configSUPPORT_DYNAMIC_ALLOCATION`
必须定义为 1，才可使用此函数。此外，应用程序还必须提供
`portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` 和 `portGET_RUN_TIME_COUNTER_VALUE` 的定义，分别用于配置外设
定时器/计数器和返回定时器的当前计数值。计数器的频率应该至少是
滴答计数的 10 倍

注意：此函数在执行期间会禁用中断。它
不是作为正常的应用程序运行时的工具，而是作为调试辅助工具。

`vTaskGetRunTimeStats()` 调用 [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)，
然后将 `uxTaskGetSystemState()` 生成的原始数据转换为
易于阅读的 (ASCII) 表格形式，表格中会显示
每个任务在运行状态下所花费的时间（即每个任务消耗的 CPU 时间量）。数据以
绝对值和百分比值的形式提供。绝对值的分辨率
取决于应用程序提供的运行时间统计时钟的频率。

`vTaskGetRunTimeStatistics()` 是一个仅为方便起见而提供的实用程序函数，它
不属于内核。请参阅 [vTaskListTasks()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vTaskListTasks)，
了解生成各任务状态信息的实用程序函数。

**参数：**

- *pcWriteBuffer*

  执行时间将以 ASCII 形式写入的缓冲区。假设此缓冲区
  的大小足以容纳生成的报告。大约为每个任务分配 40 字节的缓冲区就足够了。

- *uxBufferLength*

  pcWriteBuffer 的长度。

---

### vTaskGetIdleRunTimeCounter

task.h

```c
TickType_t xTaskGetIdleRunTimeCounter( void );
```

返回空闲任务的运行时间计数器。该函数可用于确定空闲任务
获得的 CPU 时间。请参阅[运行时统计](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)页面，
获取运行时统计功能的完整说明。

`configGENERATE_RUN_TIME_STATS` 和 `INCLUDE_xTaskGetIdleTaskHandle` 必须定义为 1，
才可使用此函数。此外，应用程序还必须提供 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
和 `portGET_RUN_TIME_COUNTER_VALUE` 的定义，分别用于配置外设定时器/计数器和返回定时器的当前
计数值。建议确保定时器的频率至少是滴答计数的 10 倍。

**返回：**
  空闲任务的运行时间计数器。该函数可用于确定空闲任务获得的 CPU 时间。
  请参阅[运行时统计](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)页面，获取运行时统计功能的完整说明。

---

### ulTaskGetRunTimeCounter

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetRunTimeCounter( const TaskHandle_t xTask );
```

`configGENERATE_RUN_TIME_STATS` 必须定义为 1，才可使用此函数。
此外，应用程序还必须提供 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
和 `portGET_RUN_TIME_COUNTER_VALUE()` 的定义，分别用于配置外设定时器/计数器和返回定时器的当前
计数值。计数器的频率应该至少是滴答计数的 10 倍。

将 `configGENERATE_RUN_TIME_STATS` 设置为 1 会导致为每个任务存储累积的总执行时间。
`ulTaskGetRunTimeCounter()` 返回给定任务的总执行时间。

**返回：**
  给定任务的总运行时间。这是任务实际执行的时间。
  时间单位取决于使用
  `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()` 和 `portGET_RUN_TIME_COUNTER_VALUE()` 宏配置的频率。

---

### ulTaskGetRunTimePercent

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetRunTimePercent( const TaskHandle_t xTask );
```

`configGENERATE_RUN_TIME_STATS` 必须定义为 1，才可使用此函数。
此外，应用程序还必须提供 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
和 `portGET_RUN_TIME_COUNTER_VALUE()` 的定义，分别用于配置外设定时器/计数器和返回定时器的当前
计数值。计数器的频率应该至少是滴答计数的 10 倍。

将 `configGENERATE_RUN_TIME_STATS` 设置为 1 会导致为每个任务存储累积的总执行时间。
`ulTaskGetRunTimePercent())` 返回给定任务所用 CPU 时间的百分比。

**返回：**
  给定任务所用 CPU 时间的百分比。

---

### ulTaskGetIdleRunTimeCounter

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimeCounter( void );
```

`configGENERATE_RUN_TIME_STATS` 必须定义为 1，才可使用此函数。
此外，应用程序还必须提供 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
和 `portGET_RUN_TIME_COUNTER_VALUE()` 的定义，分别用于配置外设定时器/计数器和返回定时器的当前
计数值。计数器的频率应该至少是滴答计数的 10 倍。

将 `configGENERATE_RUN_TIME_STATS` 设置为 1 会导致为每个任务存储累积的总执行时间。
`ulTaskGetIdleRunTimeCounter()` 返回空闲任务的总执行时间。

请注意，只有在没有其他任务以空闲优先级执行、未使用无滴答空闲模式
且 configIDLE_SHOULD_YIELD 设置为 0 的情况下，空闲时间量才能有效衡量系统中的空闲时间。

**返回：**
  空闲任务的总运行时间。这是空闲任务实际执行的时间。
  时间单位取决于使用 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
  和 `portGET_RUN_TIME_COUNTER_VALUE()` 宏配置的频率。

---

### ulTaskGetIdleRunTimePercent

task.h

```c
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimePercent( void );
```

`configGENERATE_RUN_TIME_STATS` 必须定义为 1，才可使用此函数。
此外，应用程序还必须提供 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`
和 `portGET_RUN_TIME_COUNTER_VALUE()` 的定义，分别用于配置外设定时器/计数器和返回定时器的当前
计数值。计数器的频率应该至少是滴答计数的 10 倍。

将 `configGENERATE_RUN_TIME_STATS` 设置为 1 会导致为每个任务存储累积的总执行时间。
`ulTaskGetIdleRunTimePercent()` 返回空闲任务所用 CPU 时间的百分比。

请注意，只有在没有其他任务以空闲优先级执行、未使用无滴答空闲模式
且 `configIDLE_SHOULD_YIELD` 设置为 0 的情况下，空闲时间量才能有效衡量系统中的空闲时间。

**返回：**
  空闲任务所用 CPU 时间的百分比。

---

### vTaskResetState

task.h

```c
void vTaskResetState( void );
```

该函数可重置任务模块的内部状态。应用程序必须调用此函数，方可重新启动调度器。

---
