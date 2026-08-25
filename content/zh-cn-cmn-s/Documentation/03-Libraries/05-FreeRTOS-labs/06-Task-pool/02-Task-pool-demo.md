---
title: "任务池演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**注意**：_任务池已重新设计，成为 FreeRTOS 库的内部实用程序。
以下页面仅作为旧版本 FreeRTOS-Labs_
**（FreeRTOS V10.2.1_191129, 190725_FreeRTOS_IoT_Libs_Task_Pool_and_MQTT_Preview 和 191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview）**的参考

- 本页内容：
  - [源代码组织](#源代码组织)（包括[下载](/media/2019/191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview.zip)链接）
  - [构建说明](#构建演示项目)
  - [功能](#功能)
    - [创建立即执行的作业](#创建立即执行的作业)
    - [创建延迟作业](#创建延迟作业)

### 引言

任务池演示项目使用
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)，
因此可以在 Windows 上使用
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估，
无需任何特定 MCU 硬件。


### 源代码组织

[\![](/media/2019/task_pool_source_and_header_files.jpg)](/media/2019/task_pool_source_and_header_files.jpg)
*点击放大*

构建任务池演示的项目名为 task_pool_demo.sln，位于
 FreeRTOS 主下载文件的 `\FreeRTOS-Labs\Demo\FreeRTOS\_IoT\_Libraries\utilities\task\_pool`。
**注意：**此项目不包含在 FreeRTOS 主下载文件中，目前
[作为单独的 zip 文件下载](/media/2019/191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview.zip)提供。

**注意：**演示项目是
[TCP/IP 入门项目](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)的扩展，此项目
已提供 FreeRTOS 数年。而 IoT 任务池库与
连接性没有直接关系，但 MQTT 演示项目以任务池项目为基础构建，并且依赖于任务池
和 TCP/IP 堆栈。右图（点击放大）显示了添加到 TCP/IP 入门项目以集成任务池库的文件
。

### 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。

要构建演示，请执行如下操作：

1. 从 Visual Studio IDE 中打开 `\FreeRTOS-Labs\Demo\FreeRTOS_IoT_Libraries\utilities\task_pool\task_pool_demo.sln` Visual
   Studio 解决方案文件

2. 在 IDE 的 "Build" 菜单中选择 "Build Solution"（或按 F7 ）

### 功能

该演示会创建单项应用程序任务，循环遍历一组示例。这些示例介绍
了一些任务池概念，涵盖最简单用例到更高级的场景。

演示中创建的所有作业都使用相同的回调函数。回调发送直达任务
通知到演示任务，让任务了解已执行作业回调。

**演示中作业所使用的回调函数**

```c
static void prvSimpleTaskNotifyCallback( IotTaskPool_t pTaskPool,
                                         IotTaskPoolJob_t pJob,
                                         void *pUserContext )
{
    /* The jobs context is the handle of the task to which a
     * notification should be sent. */
    TaskHandle_t xTaskToNotify = ( TaskHandle_t ) pUserContext;

    /* Remove warnings about unused parameters. */
    ( void ) pTaskPool;
    ( void ) pJob;

    /* Notify the task that created this job. */
    xTaskNotifyGive( xTaskToNotify );
}
```

下方截图显示了演示执行无误时的预期输出结果。

[\![](/media/2019/task_pool.png)](/media/2019/task_pool.png)
*点击放大*

各示例详见以下小节。

#### 创建立即执行的作业

函数 `prvExample_BasicSingleJob()` 展示了最简单的用例
其中 [IotTaskPool_CreateJob](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_createjob.html)
用于创建非永久性作业，然后通过调用
[IotTaskPool_Schedule()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_schedule.html) 来调度以便立即执行。
作业的数据结构体在堆栈上分配，因此无需动态分配或释放作业。
。

工作线程任务的优先级将高于调用 `prvExample_BasicSingleJob()` 的任务，因此
工作线程任务会抢占调用任务，导致立即执行作业回调。

该函数的简化版如下所示，其中移除了一些错误检查。如需完整内容，
请参阅源代码。

```c
static void prvExample_BasicSingleJob( void )
{
    IotTaskPoolJobStorage_t xJobStorage;
    IotTaskPoolJob_t xJob;
    uint32_t ulReturn;
    const uint32_t ulNoFlags = 0UL;
    const TickType_t xNoDelay = ( TickType_t ) 0;

    /* Create and schedule a job using the handle of
     * this task as the job's context and the function
     * that sends a notification to the task handle as
     * the jobs callback function. This is not a recyclable
     * job so the storage required to hold information
     * about the job is provided by this task - in this
     * case the storage is on the stack of this task so no
     * memory is allocated dynamically but the stack frame
     * must remain in scope for the lifetime of the job.
     */
    IotTaskPool_CreateJob(
        /* Callback function. */
        prvSimpleTaskNotifyCallback,

        /* Job context, in this case the handle of the calling
         * task so the callback knows which task to send a
         * notification to.
         */
        ( void * ) xTaskGetCurrentTaskHandle(),

        &xJobStorage,
        &xJob );

    /* In the full task pool implementation the first parameter
     * is used to pass the handle of the task pool to schedule.
     * The lean task pool implementation used in this demo only
     * supports a single task pool, which is created internally
     * within the library, so the first parameter is NULL.
     */
    IotTaskPool_Schedule( NULL, xJob, ulNoFlags );

    /* Look for the notification coming from the job's callback
     * function. The priority of the task pool worker task that
     * executes the callback is higher than the priority of this
     * task so a block time is not needed - the task pool worker
     * task pre-empts this task and sends the notification (from
     * the job's callback) as soon as the job is scheduled.
     */
    ulReturn = [ulTaskNotifyTake](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)( pdTRUE, xNoDelay );
    configASSERT( ulReturn );
}
```

#### 创建延迟作业

函数 `prvExample_DeferredJobAndCancellingJobs()` 类似于 `prvExample_BasicSingleJob()`，但
使用 [IotTaskPool_ScheduleDeferred()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_scheduledeferred.html)
而非 [IotTaskPool_Schedule()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_schedule.html)。
结果是创建的作业不会立即执行，但可延迟到将来某个时间点。

`prvExample_DeferredJobAndCancellingJobs()` 还演示了如何在调度作业执行之前将其取消
。

该函数的简化版如下所示，其中移除了一些错误检查。如需完整内容，
请参阅源代码。

```c
static void prvExample_DeferredJobAndCancellingJobs( void )
{
    IotTaskPoolJobStorage_t xJobStorage;
    IotTaskPoolJob_t xJob;
    uint32_t ulReturn;
    const uint32_t ulShortDelay_ms = 100UL;
    const TickType_t xAllowableMargin = ( TickType_t ) 5;
    TickType_t xTimeBefore, xElapsedTime, xShortDelay_ticks;
    IotTaskPoolJobStatus_t xJobStatus;

    /* Create a job using the handle of this task as the job's
     * context and the function that sends a notification to
     * the task handle as the jobs callback function. The job
     * is created using storage allocated on the stack of this
     * function - so no memory is allocated.
     */
    IotTaskPool_CreateJob(
        /* Callback function. */
        prvSimpleTaskNotifyCallback,

        /* Job context, in this case the handle of the calling
         * task so the callback knows which task to send a
         * notification to.
         */
        ( void * ) xTaskGetCurrentTaskHandle(),

        &xJobStorage,
        &xJob );

    /* Schedule the job to run its callback in xShortDelay_ms
     * milliseconds time. In the full task pool implementation
     * the first parameter is used to pass the handle of the
     * task pool to schedule. The lean task pool implementation
     * used in this demo only supports a single task pool, which
     * is created internally within the library, so the first
     * parameter is NULL.
     */
    IotTaskPool_ScheduleDeferred( NULL, xJob, ulShortDelay_ms );

    /* The scheduled job should not have executed yet, so
     * expect the job's status to be 'deferred'.
     */
    IotTaskPool_GetStatus( NULL, xJob, &xJobStatus );
    configASSERT( xJobStatus == IOT_TASKPOOL_STATUS_DEFERRED );

    /* As the job has not yet been executed it can be stopped. */
    IotTaskPool_TryCancel( NULL, xJob, &xJobStatus );

    IotTaskPool_GetStatus( NULL, xJob, &xJobStatus );
    configASSERT( xJobStatus == IOT_TASKPOOL_STATUS_CANCELED );

    /* Schedule the job again, and this time wait until its
     * callback is executed (the callback function sends a
     * notification to this task) to see that it executes at
     * the right time. Remember the time now so the time between
     * scheduling and the callback executing can be measured.
     */
    xTimeBefore = xTaskGetTickCount();

    IotTaskPool_ScheduleDeferred( NULL, xJob, ulShortDelay_ms );

    /* Wait twice the deferred execution time to ensure the
     * callback is executed before the call below times out.
     */
    ulReturn = ulTaskNotifyTake(
        pdTRUE,
        pdMS_TO_TICKS( ulShortDelay_ms * 2UL ) );

    xElapsedTime = xTaskGetTickCount() - xTimeBefore;

    /* A single notification should not have been received... */
    configASSERT( ulReturn == 1 );

    /* ...and the time since scheduling the job should be
     * greater than or equal to the deferred execution time
     * - which is converted to ticks for comparison.
     */
    xShortDelay_ticks = pdMS_TO_TICKS( ulShortDelay_ms );

    configASSERT( ( xElapsedTime >= xShortDelay_ticks ) &&
                  ( xElapsedTime < ( xShortDelay_ticks + xAllowableMargin ) ) );
}
```
