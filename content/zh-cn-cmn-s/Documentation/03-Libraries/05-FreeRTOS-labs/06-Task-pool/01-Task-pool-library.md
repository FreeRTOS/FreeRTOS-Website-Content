---
title: 任务池
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意**：任务池库经过重新设计，成为 FreeRTOS 库的内部实用程序。 
以下页面仅作为旧版本 
FreeRTOS-Labs **(FreeRTOS V10.2.1_191129, 190725_FreeRTOS_IoT_Libs_Task_Pool_and_MQTT_Preview、
和 191125_FreeRTOS_Libs_Task_Pool_MQTT_HTTPS_Preview)**的参考


## 引言

任务池库是一个实用程序库， 
提供可由 MCU 应用程序和 FreeRTOS-Plus 库共享的任务“池”。将任务汇集在一起， 
每个库不再需要自行创建和管理任务。

FreeRTOS-Plus 库可单独或共同用于创建本地连接或 
互联网连接的 MCU 应用程序。可免费使用每个库， 
且根据 [MIT 开源许可](https://opensource.org/licenses/MIT)进行发布。


## 任务池实现

任务池库有许多用例，包括大型 Linux 应用程序开发。典型的  
FreeRTOS 用例不需要其全部功能，因此在这些页面上描述的演示中提供了专门针对 FreeRTOS 
的优化版本。在此优化版本中，任务池：

* 一次仅支持单个任务池（系统任务池）。

* 如果池中的任务数耗尽，则不会通过动态添加更多任务来自动扩展。 
  相反，池中的任务数在编译时由 iot_config.h 中的 IOT_TASKPOOL_NUMBER_OF_WORKS 常量固定 
  。

* 无法关闭，在应用程序的整个生命周期内存在。

如果需要完整的功能，用户可以[切换到完整的任务池实现](https://github.com/aws/amazon-freertos/tree/master/libraries/c_sdk/standard/common/taskpool) 
。
