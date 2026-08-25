---
title: Task Pool
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**NOTE**:The Task Pool library has been redesigned to become an internal utility for FreeRTOS libraries. 
The pages below are only to be used as reference with older versions of the 
FreeRTOS-Labs **(FreeRTOS V10.2.1\_191129, 190725\_FreeRTOS\_IoT\_Libs\_Task\_Pool\_and\_MQTT\_Preview, 
and 191125\_FreeRTOS\_Libs\_Task\_Pool\_MQTT\_HTTPS\_Preview)**


## Introduction

The Task Pool library is a utility library that provides a “pool” of tasks that can be shared by the 
MCU application and FreeRTOS-Plus libraries. This pooling of tasks alleviates the need for each library 
to create and manage its own tasks.

The FreeRTOS-Plus libraries can be used individually or collectively to create locally connected or 
internet connected MCU applications.  Each library can be freely used and is distributed under 
the [MIT Open Source License](https://opensource.org/licenses/MIT).


## Task Pool Implementations

The Task Pool library has many use cases, including for large Linux application development. Typical 
FreeRTOS use cases do not require its full functionality, so an optimized version specifically for FreeRTOS 
is provided in the demo described on these pages. In this optimized version, the task pool:

* Only supports a single task pool (system task pool) at a time.

* Does not auto-scale by dynamically adding more tasks if the number of tasks in the pool becomes exhausted. 
  Instead, the number of tasks in the pool is fixed at compile time by the IOT\_TASKPOOL\_NUMBER\_OF\_WORKERS 
  constant in iot\_config.h.

* Cannot be shut down - it exists for the lifetime of the application.

Users can [switch to the full task pool implementation](https://github.com/aws/amazon-freertos/tree/master/libraries/c_sdk/standard/common/taskpool) 
if the full capability is needed.
