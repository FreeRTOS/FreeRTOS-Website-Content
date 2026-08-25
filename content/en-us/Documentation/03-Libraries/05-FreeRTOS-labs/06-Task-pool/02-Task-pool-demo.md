---
title: "Task pool demo"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**NOTE**: _The Task Pool library has been redesigned to become an internal utility for FreeRTOS libraries.
The pages below are only to be used as reference with older versions of the FreeRTOS-Labs_
**(FreeRTOS V10.2.1_191129, 190725_FreeRTOS_IoT_Libs_Task_Pool_and_MQTT_Preview, and 191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview)**

- On this Page
  - [Source Code Organization](#source-code-organization) (includes [download](/media/2019/191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview.zip) link)
  - [Build Instructions](#building-the-demo-project)
  - [Functionality](#functionality)
    - [Creating a Job that Immediately Executes](#creating-a-job-that-immediately-executes)
    - [Creating a Deferred Job](#creating-a-deferred-job)

### Introduction

The task pool demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
enabling it to be built and evaluated with
the [free Community version of Visual Studios](https://visualstudio.microsoft.com/vs/community/) on Windows,
so without the need for any particular MCU hardware.


### Source Code Organization

[![](/media/2019/task_pool_source_and_header_files.jpg)](/media/2019/task_pool_source_and_header_files.jpg)
*Click to enlarge*

The project that builds the task pool demo is called task_pool_demo.sln and is located in
the `\FreeRTOS-Labs\Demo\FreeRTOS\_IoT\_Libraries\utilities\task\_pool` of the main FreeRTOS
download. **NOTE:**The project is not in the main FreeRTOS download yet so for now
is [provided as a separate zip file download](/media/2019/191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview.zip).

**Notes:** The demo project is an extension to
the [TCP/IP Starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) that has
been provided with FreeRTOS for several years. While the IoT Task Pool library is not directly related to
connectivity, the MQTT demo project builds on the task pool project and depends on both the task pool
and TCP/IP stack. The figure on the right (click to enlarge) shows the files added into the TCP/IP starter
project to integrate the task pool library.

### Building the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).

To build the demo:

1. Open the `\FreeRTOS-Labs\Demo\FreeRTOS_IoT_Libraries\utilities\task_pool\task_pool_demo.sln` Visual
   Studio solution file from within the Visual Studio IDE

2. Select ‘build solution’ from the IDE’s ‘build’ menu (or press F7).

### Functionality

The demo creates a single application task that loops through a set of examples. The examples introduce
task pool concepts progressing from the simplest use cases to more advanced scenarios.

All of the jobs created in the demo use the same callback function. The callback sends a direct to task
notification to the demo task to let the task know the job callback has been executed.

**The Callback Function used by the Jobs in this Demo**

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

The screenshot below shows the expected output when the demo is executing correctly.

[![](/media/2019/task_pool.png)](/media/2019/task_pool.png)
*Click to enlarge*

The following sub-sections describe the individual examples.

#### Creating a Job that Immediately Executes

The function `prvExample_BasicSingleJob()` demonstrates the simplest use case 
where [IotTaskPool_CreateJob](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_createjob.html) is
used to create a non-persistent job that is then scheduled for immediate execution by a call
to [IotTaskPool_Schedule()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_schedule.html).
The Job's data structure is allocated on the stack, so the job does not need to be dynamically allocated
or freed.

A worker task will have a higher priority than the task that calls `prvExample_BasicSingleJob()`, so
the worker task will preempt the calling task, resulting in the job's callback executing immediately.

A simplified version of the function is shown below with some error checking removed. See the source code
for the full version.

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

#### Creating a Deferred Job

The function `prvExample_DeferredJobAndCancellingJobs()` is similar to `prvExample_BasicSingleJob()`, but
uses [IotTaskPool_ScheduleDeferred()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_scheduledeferred.html)
in place of [IotTaskPool_Schedule()](https://aws.github.io/amazon-freertos/202107.00/c-sdk/taskpool/taskpool_function_schedule.html).
This will create a job that does not execute immediately, but at a time deferred to the future.

`prvExample_DeferredJobAndCancellingJobs()` also demonstrates how a scheduled job can be cancelled before
it has been executed.

A simplified version of the function is shown below with some error checking removed. See the source code
for the full version.

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

    /* Schedule the job to run its callback in xShortDelay\_ms
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
