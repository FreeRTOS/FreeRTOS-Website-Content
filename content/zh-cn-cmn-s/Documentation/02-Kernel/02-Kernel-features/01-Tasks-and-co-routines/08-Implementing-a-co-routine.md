---
title: "FreeRTOS 协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——协程
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
  - title: 协程示例
    link: /Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Co-routine-example/
---

[[更多关于协程的信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### 协程实现

协程应具有以下结构体： 

```c
void vACoRoutineFunction( CoRoutineHandle_t xHandle,
                          UBaseType_t uxIndex )
{
    crSTART( xHandle );

    for( ;; )
    {
        -- Co-routine application code here. --
    }

    crEND();
}
```

类型 crCOROUTINE_CODE 定义为返回 void 并以 CoRoutineHandle_t 和索引作为其参数的函数 
。实现协程的函数都应属于这种类型（如上所示） 
。

调用 xCoRoutineCreate() 即可创建协程。

注意事项：

* 所有协程函数都**必须**以调用 crSTART() 开始。
  
* 所有协程函数都**必须**以调用 crEND() 结束。
  
* 协程函数不应返回任何值，因此通常实现为连续循环。
  
* 可通过单个协程函数创建多个协程。提供的 uxIndex 参数 
  作为区分此类协程的方法。
