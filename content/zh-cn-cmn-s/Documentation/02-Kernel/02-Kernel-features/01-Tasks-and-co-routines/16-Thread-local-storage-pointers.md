---
title: "线程本地存储指针"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 通过使用线程本地存储指针为应用程序编写者提供灵活的线程本地存储机制。
relatedLinks:
  - title: API 引用 - vTaskSetThreadLocalStoragePointer
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/07-vTaskSetThreadLocalStoragePointer/
  - title: API 引用 - pvTaskGetThreadLocalStoragePointer
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/08-pvTaskGetThreadLocalStoragePointer/
---

### 引言

线程本地存储 (TLS) 允许应用程序编写者将值存储在任务的控制块中，
控制块内，使值特定于（本地）任务本身，
并允许每个任务具有自己的唯一值。

线程本地存储最常用于
存储单线程程序会存储在全局变量中的值。例如，许多库包含一个
名为 errno 的全局变量。如果库函数向调用函数返回错误条件，
则调用函数可以检查 errno 值
以确定是什么错误。在单线程应用程序中，只需
将 errno 声明为全局变量，但在多线程应用程序中，
每个线程（任务）必须有其唯一的 errno 值，
否则一个任务可能会读取另一个任务的 errno 值。


### 线程本地存储指针

通过使用线程本地存储指针，FreeRTOS 为应用程序编写者提供了灵活的线程本地存储
机制。

[configNUM_THREAD_LOCAL_STORAGE_POINTERS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#confignum_thread_local_storage_pointers)
编译时配置常量为每个任务的 void 指针数组 (void*) 确定维度。 
[vTaskSetThreadLocalStoragePointer()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/07-vTaskSetThreadLocalStoragePointer) API 函数用于
在 void 指针数组中设置值， [pvTaskGetThreadLocalStoragePointer()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/08-pvTaskGetThreadLocalStoragePointer)
API 函数用于从 void 指针数组读取值。


### 线程本地整数

小于或等于 void 指针大小的值
可以直接存储在线程本地存储指针数组中。例如，
如果 sizeof( void * ) 为 4，则可以使用简单的强制转换将 32 位值存储在 void 指针变量中，
以避免编译器发出警告。但是，
如果 sizeof( void * ) 为 2，则只能直接存储 16 位值。


```c
uint32_t ulVariable;  

/* Write the 32-bit 0x12345678 value directly into index 1 of the thread   
   local storage array. Passing NULL as the task handle has the effect of writing   
   to the calling task's thread local storage array. */  
vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   1,     /* Index into the array. */  
                                   ( void * ) 0x12345678 );  

/* Store the value of the 32-bit variable ulVariable to index 0 of the calling  
   task's thread local storage array. */  
ulVariable = ERROR_CODE;  

vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   0,     /* Index into the array. */  
                                   ( void * ) ulVariable );  

/* Read the value stored in index 5 of the calling task's thread local storage  
   array into ulVariable. */  
ulVariable = ( uint32_t ) pvTaskGetThreadLocalStoragePointer( NULL, 5 );  
```
*直接从线程本地存储数组中的索引存储和检索 32 位值*


### 线程本地结构体

上述示例直接将值存储在线程本地存储数组中。下一示例演示了 
如何使用数组中的值作为指向内存中其他位置的结构体的指针。

```c
typedef struct  
{  
    uint32_t ulValue1;  
    uint32_t ulValue2;  
} xExampleStruct;  

xExampleStruct *pxStruct;  

/* Create a structure for use by this task. */  
pxStruct = pvPortMalloc( sizeof( xExampleStruct ) );  

/* Set the structure members. */  
pxStruct->ulValue1 = 0;  
pxStruct->ulValue2 = 1;  

/* Store a pointer to the structure in index 0 of the calling task's thread   
   local storage array. */  
vTaskSetThreadLocalStoragePointer( NULL,  /* Task handle. */  
                                   0,     /* Index into the array. */  
                                   ( void * ) pxStruct );  

/* Locate the structure used by the calling task by reading its location from  
   index 0 of the calling task's thread local storage array. */  
pxStruct = ( xExampleStruct * ) pvTaskGetThreadLocalStoragePointer( NULL, 0 );  
```
*存储指向调用任务线程本地存储数组中结构体的指针*
