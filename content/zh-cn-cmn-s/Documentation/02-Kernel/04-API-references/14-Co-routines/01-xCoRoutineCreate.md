---
title: xCoRoutineCreate
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[协程专用](/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
BaseType_t xCoRoutineCreate
    (
      crCOROUTINE_CODE pxCoRoutineCode,
      UBaseType_t uxPriority,
      UBaseType_t uxIndex
    );
```

创建新协程，并将其添加到做好运行准备的协程的列表中。


**参数：**

- *pxCoRoutineCode*

  指向协程函数的指针。协程函数需要特殊的语法，请参阅在线文档中的
  协程部分以获取更多信息。

- *uxPriority*

  协程运行时相对于其他协程的优先级。

- *uxIndex*

  用于区分执行相同函数的不同协程。有关更多信息，请参阅下方示例
  和在线文档中的协程部分。


**返回：**

- 如果协程成功创建并添加到做好运行准备的协程的列表中，则返回 *pdPASS*，
  否则返回 ProjDefs.h 定义的错误代码。


**用法示例：**

```c
// Co-routine to be created.
void vFlashCoRoutine( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must
    // maintain value across a blocking call. This may not be necessary
    // for const variables.
    static const char cLedToFlash[ 2 ] = { 5, 6 };
    static const TickType_t uxFlashRates[ 2 ] = { 200, 400 };

    // Must start every co-routine with a call to crSTART();
    crSTART( xHandle );

    for( ;; )
    {
        // This co-routine just delays for a fixed period, then toggles
        // an LED.  Two co-routines are created using this function, so
        // the uxIndex parameter is used to tell the co-routine which
        // LED to flash and how long to delay.  This assumes xQueue has
        // already been created.
        vParTestToggleLED( cLedToFlash[ uxIndex ] );
        crDELAY( xHandle, uxFlashRates[ uxIndex ] );
    }

    // Must end every co-routine with a call to crEND();
    crEND();
}

// Function that creates two co-routines.
void vOtherFunction( void )
{
    unsigned char ucParameterToPass;
    TaskHandle_t xHandle;

    // Create two co-routines at priority 0.  The first is given index 0
    // so (from the code above) toggles LED 5 every 200 ticks.  The second
    // is given index 1 so toggles LED 6 every 400 ticks.
    for( uxIndex = 0; uxIndex < 2; uxIndex++ )
    {
        xCoRoutineCreate( vFlashCoRoutine, 0, uxIndex );
    }
}
```


### CoRoutineHandle_t

引用协程的类型。协程句柄会自动传递给所有协程
函数。
