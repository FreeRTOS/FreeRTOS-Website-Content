---
title: 任务间通信
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**设计理念和性能优化**


## 引言

本页介绍了 
FreeRTOS 提供的不同任务间通信 API 函数之间的关系，其中提供了[全功能](#全功能-api)、可替代和轻量化的 API 
。以下信息旨在帮助用户在不同使用场景下， 
尤其是针对以下场景选择最合适的 API 函数：

> **注意：**可替代 API 已停止开发并且已弃用，
> 不推荐用于新设计。


* 函数执行时间。
* 中断响应性。
* 易于使用。

除中断服务程序之外，**全功能 API 将是高级用户以外的其他所有用户的首要选择** 
。它最简单易用，能有效利用临界区。


### 简要总结

[全功能](#全功能-api)和可替代 API 提供相同的功能—— 
但其实现方式不同。  实现可替代 (Alt) API 的源代码要简单的多， 
因为它可以在临界区执行所有内容。  这是很多其他 RTOS 采用的方法， 
但没有首选的全功能 API 那么复杂。全功能 API 的代码更为复杂， 
执行时间更长，而且不能充分利用临界区。因此，可替代 API 牺牲了中断响应速度， 
以确保 API 函数的执行速度，而全功能 API 则牺牲了 API 函数的执行速度， 
以确保更好的中断响应性。

[轻量化](#轻量化-api) API 替代方案提供了更快的执行时间，同样是牺牲了中断响应性， 
而且从应用程序编写者的角度来看更复杂一些。因此， 
轻量化 API 的使用属于“高级主题”范畴， 
仅供经验丰富的用户使用。

需查阅 API 引用以获取更多功能属性，例如， 
函数参数的详细信息。


### 设计目标和概念

FreeRTOS 设计为占据较小的 ROM 空间。为此，所有任务间通信 
都是围绕一个队列基元构建的，这大大限制了所需源代码的数量。此外，
所有事件管理功能都内置于队列数据结构体中。第二点 
与其他 RTOS 设计相反，在此类设计中，事件控制块往往是一个独立的实体。

队列机制用于实现：

1. 队列本身
2. 信号量：作为使用队列的宏实现，因此不引入新代码
3. 互斥锁：也作为使用队列的宏实现，仅引入少量新代码

可以轻松对 FreeRTOS 进行扩展，以便以相同的方式包含其他任务间通信机制。

由于所有通信机制都基于相同的基础队列概念，因此为每个机制提供的 API 函数 
实际上具有相对互操作性。
  

---

## 全功能 API 

包括以下函数：

* xQueueSend()
* xQueueSendToBack()
* xQueueSendToFront()
* xQueueReceive()
* xQueuePeek()
* xSemaphoreTake()
* xSemaphoreGive()


### 函数特点

这些函数可归类为全功能函数，原因如下：

1. 它们利用队列和 RTOS 调度器锁定机制。这样就能最大限度地减少临界区 
   （API 函数本身内部）的使用，确保无论队列中的数据量有多大， 
   都能将对中断响应速度的影响降至最低。

2. 如果对队列的读取或写入操作会导致更高优先级的任务解除阻塞， 
   则它们会自动导致上下文切换。

3. 它们（自然）具有线程安全性。

4. 任务和中断都可以同时访问队列，就这一点而言，它们具有中断安全性。 
   请注意，在 ISR 中调用这些程序并**不**保证中断安全， 
   在 ISR 中只能使用轻量化 API。

由于功能齐全，这些函数内部较为复杂，而这种复杂性对用户是隐藏的， 
因此它们用起来十分简单。

与对应的可替代和轻量化 API 函数相比，全功能的 API 函数执行起来时间更长。 
这是因为实现这些功能需要更多的代码。因此， 
我们需要在函数执行时间和临界区的有效利用之间进行权衡。


### 关于全功能 API 的总结

与[可替代](#可替代-api)和[轻量化](#轻量化-api) API 相比，全功能 API 函数具有以下优缺点：


* ![](/media/2018/good.gif)对中断响应时间的影响较小。
* ![](/media/2018/good.gif)更简单易用。RTOS 内核负责线程/中断 
  安全和任务优先级。
* ![](/media/2018/bad.gif)  此类函数更大，因此执行时间更长。


---

## 可替代 API

包括以下函数：

* xQueueAltSend()
* xQueueAltSendToBack()
* xQueueAltSendToFront()
* xQueueAltReceive()
* xQueueAltPeek()
* xSemaphoreAltTake()
* xSemaphoreAltGive()


有关此类函数的使用说明请参考标准演示源文件， 
此类文件的文件名以 “ALT” 开头，可在 FreeRTOS/Demo/Common/Minimal 目录中找到。

  
### 函数特点

此类 API 函数在功能上与对应的全功能函数相同， 
但实现起来更简单一些。

它们使用粗略的临界区来代替对应的全功能函数所使用的队列和 RTOS 调度器锁定机制 
。这虽然简化了代码并提高了执行速度， 
但却增加了在临界区中的耗时， 
因此对中断响应时间产生了相对不利的影响。此外，与全功能版本不同的是，
在访问队列时需要禁用中断，这意味着中断和任务不能同时访问队列。

可替代 API 函数与全功能 API 函数相比，执行时间更短， 
但与轻量化 API 函数相比，执行时间更长。


### 关于可替代 API 的总结

与[全功能](#全功能-api) API 相比，可替代 API 函数具有以下优缺点：

* ![](/media/2018/bad.gif)  对中断响应时间的影响更大。
* ![](/media/2018/indif.gif)  具有等效的函数调用原型， 
  因此使用起来难度适中，既不简单也不复杂。   |
* ![](/media/2018/good.gif)  体积更小，因此执行时间更短 
  （尽管比轻量化 API 耗时更长）。   |

---

## 轻量化 API

包括以下函数：

* xQueueSendFromISR()
* xQueueSendToBackFromISR()
* xQueueSendToFrontFromISR()
* xQueueReceiveFromISR()
* xSemaphoreGiveFromISR()

这些函数可在 ISR 内使用，并使用相应名称命名， 
以便于识别。请注意它们并非只能在中断内使用。 
此类函数还可以在任务内使用，以提高运行时效率。更多信息请参阅下文。
  

### 函数特点

1. 此类函数比它们的全功能或可替代版本简单得多。它们的实现 
   使用的代码更少，因此执行速度更快。

2. 它们设计成可以在中断内安全使用，因此本身不会尝试做到中断 
   安全。这意味着在中断内使用它们很简单， 
   但在中断外使用它们则需要特别考虑。

3. 如果对队列的读取或写入操作会导致更高优先级的任务解除阻塞， 
   它们也不会自动执行上下文切换。相反，它们会返回一个值， 
   表明是否需要进行上下文切换。

轻量化函数将更多决策留给应用程序编写者，因此灵活性更高。 
这为应用程序设计人员提供了更多选择，可以在函数执行时间与中断响应速度之间进行权衡， 
但在如何灵活运用时需要注意。有关这方面的更多信息，
请参阅本页面以下部分。
  

### 关于轻量化 API 的总结

与[全功能](#全功能-api) API 相比，轻量化 API 函数具有以下优缺点：

* ![](/media/2018/good.gif)  从中断中调用时，使用起来很简单。
* ![](/media/2018/good.gif)  更小、更灵活。因此， 
  此类函数允许应用程序设计者  在执行时间和中断响应速度之间进行权衡， 
  进而提高运行时性能。 
* ![](/media/2018/bad.gif)  从任务调用时需要特别留意， 
  而从中断调用时不需要。   


---

## FreeRTOS 性能提示和技巧：在中断之外使用轻量化 API

*此信息仅适用于经验丰富的用户。*

以下子节详细介绍了如何及何时使用轻量化 API 函数 
代替它们的全功能版本和可替代版本。以下示例演示了从最基本的快速使用， 
到添加更多功能的不同的使用场景。

请**注意**，这些示例仅涉及在 ISR 外部使用轻量化 API 函数 
。API 函数的名称中包含文本 "FromISR"， 
表示它们可在 ISR 内安全使用，而不是专门在 ISR 内使用。


### 轻量化示例 1——基本快速使用

以下代码显示在两个任务间发送和接收消息最快的方式：

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
**列表 1：发送或接收消息的最快方式**
---

上述轻量化 API 的描述指出，与全功能版本不同的是，此类 API 
函数不会执行任何操作来确保线程或中断安全。

注意：

* 传递给列表 1 所列函数的参数可用于 
  防止此类函数尝试解除对等待队列事件的任何任务的阻塞。这意味着 
  在与协作 RTOS 调度器一起使用时，线程安全不是问题， 
  但这也意味着在这种形式下，只有在访问队列另一端的任务不阻塞的情况下，才能使用轻量化 API。

* 在这种形式下，API 函数不是中断或抢占安全的，也就是说，这种使用方式在以下情况下**不**合适： 
  如果中断使用了同一队列， 
  或者访问队列的任务可能被访问同一队列的任务抢占。


### 轻量化示例 2：允许解除任务阻塞

以下代码显示了如何扩展列表 1 以允许轻量化 API 函数解除任务阻塞。

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
**列表 2：使用轻量化 API 解除任务阻塞**
---

注意：

* 为确保中断安全性，我们在列表 1 和列表 2 之间没有采取任何措施。因此， 
  如果队列也从 ISR 访问，这仍**不是**适当的使用方法。

* 传递给列表 2 所列函数的参数允许此类函数 
  解除对等待队列事件的任何任务的潜在阻塞。因此，**** 
  如果使用抢占式 RTOS 调度器，则不适合使用这种方法。仅使用协同RTOS调度器时，它提供了一个良好的机制。


### 轻量化示例 3：引入抢占和中断安全性

以下代码更新了列表 2 中所列函数，以确保轻量化 API 使用时能保证抢占安全性 
和中断安全性。对 API 函数的整个调用都被置于临界区内， 
从而对中断响应时间造成不利影响。因此，这种方法以牺牲中断响应时间来换取执行时间的改善， 
而这些 API 函数的全功能版本则恰恰相反， 
它们以牺牲执行时间来换取中断响应时间的改善。

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
**列表 3：完全抢占和中断安全——全功能 API 版本不会以此处所示方式在临界区执行
整个队列函数！** 
---

注意：

* 可以提供宏以便于以这种方式使用轻量化 API。

* 以这种方式使用的轻量化 API 提供与全功能 API 版本相似的功能， 
  但临界区的使用效率较低。


### 使用信号量和互斥锁会产生什么效果呢？

此处演示的队列访问原则也适用于访问信号量和互斥锁。

