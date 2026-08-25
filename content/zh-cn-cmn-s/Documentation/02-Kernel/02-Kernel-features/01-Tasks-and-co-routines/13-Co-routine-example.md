---
title: "FreeRTOS 协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——协程
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
---

[[更多关于协程的信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### 快速协程示例

此快速示例展示了协程的使用方法。

1. **创建一个简单的协程来闪烁 LED**

   以下代码定义了一个非常简单的协程，它只会定期闪烁 LED。

   ```c
   void vFlashCoRoutine( CoRoutineHandle_t xHandle,
                         UBaseType_t uxIndex )
   {
       // Co-routines must start with a call to crSTART().
       crSTART( xHandle );

       for( ;; )
       {
           // Delay for a fixed period.
           crDELAY( xHandle, 10 );

           // Flash an LED.
           vParTestToggleLED( 0 );
       }

       // Co-routines must end with a call to crEND().
       crEND();
   }
   ```

   就是这样！

2. **调度协程**

   通过重复调用 vCoRoutineSchedule() 来调度协程。执行这一操作的最佳位置是 
   空闲任务内部，通过编写空闲任务钩子函数来完成。首先，请确保 configUSE_IDLE_HOOK 
   在 FreeRTOSConfig.h中设置为 1。然后编写空闲任务钩子函数，如下所示：

   ```c
   void vApplicationIdleHook( void )
   {
       vCoRoutineSchedule( void );
   }
   ```

   如果空闲任务没有执行任何其他函数，那按以下方式在循环中调用 
   vCoRoutineSchedule() 效率会更高：

   ```c
   void vApplicationIdleHook( void )
   {
       for( ;; )
       {
           vCoRoutineSchedule( void );
       }
   }
   ```

3. **创建协程并启动 RTOS 调度器**

   协程可在 main() 中创建。

   ```c
   #include "task.h"
   #include "croutine.h"

   #define PRIORITY_0 0

   void main( void )
   {
       // In this case the index is not used and is passed 
       // in as 0.
       xCoRoutineCreate( vFlashCoRoutine, PRIORITY_0, 0 );

       // NOTE: Tasks can also be created here!

       // Start the RTOS scheduler.
       vTaskStartScheduler();
   }
   ```
   
4. **示例扩展：使用索引参数**

   现在假设我们要从同一函数中创建 8 个这样的协程。每个协程将 
   以不同速度闪烁不同的 LED。索引参数可用于在协程函数中 
   区分协程。

   这一次，我们将创建 8 个协程，并向每个协程传递不同的索引。

   ```c
   #include "task.h"
   #include "croutine.h"

   #define PRIORITY_0        0
   #define NUM_COROUTINES    8

   void main( void )
   {
       int i;

       for( i = 0; i < NUM_COROUTINES; i++ )
       {
           // This time i is passed in as the index.
           xCoRoutineCreate( vFlashCoRoutine, PRIORITY_0, i );
       }

       // NOTE: Tasks can also be created here!

       // Start the RTOS scheduler.
       vTaskStartScheduler();
   }
   ```

   协程函数也被扩展，因此每个协程使用的 LED 和闪烁速度都不同。

   ```c
   const int iFlashRates[ NUM_COROUTINES ] = { 10, 20, 30, 40, 50, 60, 70, 80 };
   const int iLEDToFlash[ NUM_COROUTINES ] = { 0, 1, 2, 3, 4, 5, 6, 7 }

   void vFlashCoRoutine( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
   {
       // Co-routines must start with a call to crSTART().
       crSTART( xHandle );

       for( ;; )
       {
           // Delay for a fixed period. uxIndex is used to index into
           // the iFlashRates. As each co-routine was created with
           // a different index value each will delay for a different
           // period.
           crDELAY( xHandle, iFlashRate[ uxIndex ] );

           // Flash an LED. Again uxIndex is used as an array index,
           // this time to locate the LED that should be toggled.
           vParTestToggleLED( iLEDToFlash[ uxIndex ] );
       }

       // Co-routines must end with a call to crEND().
       crEND();
   }
   ```
