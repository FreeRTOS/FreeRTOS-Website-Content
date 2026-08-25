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


### 局限和限制

与同等任务相比，协程的优势是使用的 RAM 较少，但代价是 
使用协程时存在一些限制条件。与任务相比，协程的限制性更强，使用起来也更复杂 
。

* **共享堆栈**   

  当协程阻塞时，协程的堆栈无法维持。这意味着在堆栈上分配的变量 
  很可能丢失其值。要克服这一问题， 
  需将在阻塞调用中维持其值的变量声明为静态。例如：

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle,
                            UBaseType_t uxIndex )
  {
      static char c = 'a';

      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // If we set c to equal 'b' here ...
          c = 'b';

          // ... then make a blocking call ...
          crDELAY( xHandle, 10 );

          // ... c will only be guaranteed to still 
          // equal 'b' here if it is declared static
          // (as it is here).
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }
  ```

  共享堆栈的另一个结果是，能从协程函数本身调用可能导致协程阻塞的 API 函数， 
  而*不能*从协程调用的函数中调用 
  。例如：

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
  {
      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // It is fine to make a blocking call here,
          crDELAY( xHandle, 10 );

          // but a blocking call cannot be made from within
          // vACalledFunction().
          vACalledFunction();
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }

  void vACalledFunction( void )
  {
      // Cannot make a blocking call here!
  }
  ```

* **switch 语句的使用**   

  FreeRTOS 下载中的默认协程实现不允许 
  在 switch 语句中进行阻塞调用。例如：

  ```c
  void vACoRoutineFunction( CoRoutineHandle_t xHandle, UBaseType_t uxIndex )
  {
      // Co-routines must start with a call to crSTART().
      crSTART( xHandle );

      for( ;; )
      {
          // It is fine to make a blocking call here,
          crDELAY( xHandle, 10 );

          switch( aVariable )
          {
              case 1 : // Cannot make a blocking call here!
                       break;
              default: // Or here!
          }
      }

      // Co-routines must end with a call to crEND().
      crEND();
  }
  ```
  
