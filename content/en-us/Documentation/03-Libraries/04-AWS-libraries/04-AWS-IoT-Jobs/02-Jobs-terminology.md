---
title: Jobs Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Job*   
A job is a set of operations defined for the device to perform. For example, you can define a job that 
instructs a set of devices to download and install application or firmware updates, reboot, rotate certificates, 
or perform remote troubleshooting operations.

*Job Document*   
The job document details the operations that will be performed by each device. It is a UTF-8 encoded 
JSON document that contains all of the information the device needs to perform the job. For example, 
a job document can contain multiple URLs from which the device can download a firmware update or receive 
other data. The job document can be stored in an Amazon S3 bucket, or be included inline with the command 
that creates the job.

*Target*   
A target is a device, or a group of devices, that are required to execute the job. After a list of targets 
has been defined in the AWS IoT Console, each device is notified that there is a pending job.

*Job Execution*   
A job execution is the performance of the operations defined by the job on a particular device. The 
device starts its job execution after it has downloaded the job document. It then performs the operations 
specified in the document, and reports its progress to AWS IoT. Each job execution on each individual 
device is given a unique identifier, so you can track and manage the progress of a job on all targets.

*Snapshot Job*   
A snapshot job is sent only to the targets you defined when you created the job. If new devices are 
required to perform the same operation, a new snapshot job must be created for these additional devices. 
Once all targets have completed the snapshot job (or reported they are unable to do so), it is considered 
completed.

*Continuous job*   
A continuous job is sent to the targets you defined when you created the job, and also to any devices 
that are added to a target group later. Continuous Jobs are often used to onboard or upgrade new devices 
as they are added to the group. You can make a job continuous by setting an optional parameter when 
you create the job.

*Rollouts*   
You can specify how quickly targets are notified of a pending job execution. This allows you to create 
a staged rollout to better manage updates, reboots, and other operations across an entire fleet of devices.

The following field can be added to the `CreateJob` request to specify the maximum number of job targets 
to inform per minute. This example sets a static rollout rate.

```c
"jobExecutionRolloutConfig": {
        "maximumPerMinute": "integer"
    }
```

You can also set a variable rollout rate with the `exponentialRate` field. The following example creates 
a rollout that has an exponential rate.

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

For more information about configuring job rollouts, 
see [Job Rollout and Abort Configuration](https://docs.aws.amazon.com/iot/latest/developerguide/job-rollout-abort.html) 
in the *AWS IoT Developer Guide*.


*Abort*   
An Abort is the cancellation of a job rollout based on a set of predefined criteria. For example, you 
can set a job rollout to be aborted if there are 10 Jobs that fail to execute. The job rollouts can 
also be aborted if the number of failed jobs matches a set of criteria. The job's abort criteria are 
set at job creation by using the [`AbortConfig`](https://docs.aws.amazon.com/iot/latest/apireference/API_AbortConfig.html) 
object. For more information, 
see [Job Rollout and Abort Configuration](https://docs.aws.amazon.com/iot/latest/developerguide/job-rollout-abort.html) 
in the *AWS IoT Developer Guide*.


*Placeholder Links and Presigned URLs*   
A device may require additional data beyond what is contained in the job document. This data can be 
placed in an Amazon S3 bucket and a placeholder link provided within the job document. When AWS Jobs 
begins notifying the target devices, the placeholder link is replaced with a presigned Amazon S3 URL. 
The presigned URL provides a secure and time-limited location for the device to retrieve additional 
data (such as a firmware image for a software update).

The placeholder link has the following form: `${aws:iot:s3-presigned-url:https://s3.amazonaws.com/*bucket*/*key*}`
where *bucket* is your bucket name and *key* is the object in the bucket that contains the data.


*Timeouts*   
Job timeouts make it possible to be notified whenever a job execution gets stuck in the `IN_PROGRESS` 
state for an unexpectedly long period of time. There are two types of timers: in-progress timers and 
step timers.

When you create a job, you can set a value for the `inProgressTimeoutInMinutes` property in the 
optional [TimeoutConfig](https://docs.aws.amazon.com/iot/latest/apireference/API_TimeoutConfig.html) 
object. The in-progress timer can't be updated and applies to all job executions for the job. Whenever 
a job execution remains in the `IN_PROGRESS` state for longer than this interval, the job execution 
fails and switches to the terminal `TIMED_OUT` state. AWS IoT also publishes an MQTT notification.

You can also set a step timer for a device's job execution by setting a value for `stepTimeoutInMinutes` 
when you call [UpdateJobExecution](https://docs.aws.amazon.com/iot/latest/apireference/API_iot-jobs-data_UpdateJobExecution.html). 
The step timer applies only to the specific job execution that you update. You can set a new value for 
this timer each time you update the job execution. You can also create a step timer when you 
call [StartNextPendingJobExecution](https://docs.aws.amazon.com/iot/latest/apireference/API_iot-jobs-data_StartNextPendingJobExecution.html). 
If the job execution remains in the `IN_PROGRESS` state for longer than the step timer interval, it 
fails and switches to the terminal `TIMED_OUT` state. The step timer has no effect on the in-progress 
timer that you set when you create a job. See 
the [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) for 
more information.
