---
title: 作业术语
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*作业*   
作业是为设备定义的一组要执行的操作。例如，您可以定义一个作业， 
指示一组设备下载和安装应用程序或固件更新、重新启动、轮换证书 
或执行远程故障排除操作。

*作业文档*   
作业文档详细说明了每台设备将执行的操作。它是一份 UTF-8 编码的 
JSON 文档，其中包含设备执行作业所需的所有信息。例如， 
例如，一份作业文档可以包含多个 URL，设备可以从中下载固件更新或接收 
其他数据。作业文档可以存储在 Amazon S3 存储桶中，或包含在 
创建作业的命令中。

*目标*   
目标是执行作业所需的一台设备或一组设备。在 
AWS IoT 控制台中定义目标列表后，将通知每台设备有待处理的作业。

*作业执行*   
作业执行是指在特定设备上执行由作业定义的操作。设备 
下载作业文档后就开始作业执行。然后设备会 
执行文档中指定的操作，并向 AWS IoT 报告进度。每台独立设备上的每个作业执行都有一个唯一的标识符， 
因此您可以跟踪和管理所有目标上的作业进度。

*快照作业*   
快照作业仅发送到您在创建作业时定义的目标。如果需要新设备执行相同的操作， 
则必须为这些附加设备创建新的快照作业。 
一旦所有目标完成快照作业（或报告无法完成），即视为该作业已完成 
。

*连续作业*   
连续作业将发送到您在创建作业时定义的目标， 
以及此后添加到目标组的任何设备。连续作业通常用于在新设备添加到组中时， 
对其进行上机或升级。您可以通过在创建作业时设置可选参数 
来使作业连续。

*推出*   
你可以指定目标在挂起作业中被通知的速度。这允许您 
创建一个分阶段的推出，以更好地管理整个设备群的更新、重启和其他操作。

可以将以下字段添加到 `CreateJob` 请求，以指定每分钟要通知的作业目标的最大数量 
。此示例设置静态推出率。

```c
"jobExecutionRolloutConfig": {
        "maximumPerMinute": "integer"
    }
```

您还可以使用 `exponentialRate` 字段来设置可变的推出率。以下示例创建了 
一个具有指数率的推出。

```c
"jobExecutionsRolloutConfig": { 
    "exponentialRate": { 
        "baseRatePerMinute": integer,
        "incrementFactor": integer,
        "rateIncreaseCriteria": { 
            "numberOfNotifiedThings": integer, // Set one or the other
            "numberOfSucceededThings": integer // of these two values.
        },
        "maximumPerMinute": integer
    }
}
```

有关配置作业推出的更多信息， 
请参阅[作业推出和中止配置章节](https://docs.aws.amazon.com/iot/latest/developerguide/job-rollout-abort.html) 
（位于 *AWS IoT 开发者指南*中）。


*中止*   
中止是指根据一组预定义标准取消作业推出。例如， 
如果有 10 个作业无法执行，您可以将作业推出设置为中止。如果失败作业的数量符合一组标准， 
也可以中止作业推出。作业的中止标准 
在创建作业时使用 [`AbortConfig`](https://docs.aws.amazon.com/iot/latest/apireference/API_AbortConfig.html) 
对象设置。更多信息， 
请参阅[作业推出和中止配置章节](https://docs.aws.amazon.com/iot/latest/developerguide/job-rollout-abort.html) 
（位于 *AWS IoT 开发者指南*中）。


*占位符链接和预签名 URL*   
除了作业文档中所包含的数据，设备可能还需要其他数据。可将这些数据放在 
Amazon S3 存储桶中，并在作业文档中提供一条占位符链接。当 AWS 作业 
开始通知目标设备时，占位符链接将被替换为预签名的 Amazon S3 URL。 
预签名的 URL 为设备检索额外数据 
（如软件更新的固件映像）提供了一个安全和有时间限制的位置。

占位符链接的形式如下：`${aws:iot:s3-presigned-url:https://s3.amazonaws.com/*bucket*/*key*}`
其中，*bucket* 表示存储桶名称，*key* 表示存储桶中包含数据的对象。


*超时*   
作业超时使得每当作业执行被卡在 `IN_PROGRESS` 
状态中的时间格外长时都可以收到通知。定时器有两种类型：进行中定时器和 
步进计时器。

创建作业时，您可在可选的 TimeoutConfig 对象中为 `inProgressTimeoutInMinutes` 
[属性设置一个值](https://docs.aws.amazon.com/iot/latest/apireference/API_TimeoutConfig.html) 
。进行中定时器无法更新，并且适用于该作业的所有作业执行。每当 
作业执行在 `IN_PROGRESS` 状态下停留的时间超过这个时间间隔，作业执行就会失败， 
并切换到终端 `TIMED_OUT` 状态。AWS IoT 也会发布 MQTT 通知。

你也可以在调用 UpdateJobExecution 时，通过设置 `stepTimeoutInMinutes` 的值， 
[为设备的作业执行设置一个步进定时器](https://docs.aws.amazon.com/iot/latest/apireference/API_iot-jobs-data_UpdateJobExecution.html)。 
步进定时器仅适用于您更新的特定作业执行。您可以在每次更新作业执行时 
为此定时器设置一个新值。您也可以在调用 
[StartNextPendingJobExecution](https://docs.aws.amazon.com/iot/latest/apireference/API_iot-jobs-data_StartNextPendingJobExecution.html) 时创建步进定时器。 
每当作业执行在 `IN_PROGRESS` 状态下停留的时间超过步进定时器时间间隔， 
作业执行就会失败，并切换到终端 `TIMED_OUT` 状态。步进定时器 
对您在创建作业时设置的进行中定时器没有影响。请参阅 
[AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) 
了解更多信息。
