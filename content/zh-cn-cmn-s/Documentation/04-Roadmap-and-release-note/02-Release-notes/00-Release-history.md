---
title: FreeRTOS 版本历史
created: 2018-09-20 00:00:00.0 UTC
categories:
- 路线图和版本说明
description: 关于 FreeRTOS 版本历史的信息
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
- title: FreeRTOS 初学者指南
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
- title: 下载 FreeRTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: 常见问题
  link: /Why-FreeRTOS/FAQs
---


文档和下载地址：https://www.FreeRTOS.org/


### 从 FreeRTOS V10.6.0 到 2023 年 8 月 17 日发布的 FreeRTOS 10.6.1 的变更

+ 为 mpu_wrappers_v2.c 文件中的函数增加了运行时参数检查。
  在使用断言的 API 实现中
  已经执行了相同的检查。

  我们感谢以下人士为这些更改提供的贡献：

  - 中国安徽工业大学计算机科学与技术学院的
    Lan Luo、Zixia Liu。
  - 美国马萨诸塞大学洛厄尔分校计算机科学系的
    Xinwen Fu。
  - 中国东南大学计算机科学与工程学院的
    Xinhui Shao、Yumeng Wei、Huaiyu Yan、Zhen Ling。


### 从 FreeRTOS V10.5.1 到 2023 年 7 月 13 日发布的 FreeRTOS 10.6.0 的变更

+ 增加了一个全新的 MPU包装函数，
  对非特权任务施加了额外限制。以下是随新的 MPU
  包装函数引入的变更列表：

  1. 内核对象句柄的不透明和间接可验证整数：
     所有内核对象句柄（例如队列句柄）现在都是
     不透明整数。以前，对象句柄是原始指针。

  2. 将任务上下文保存在任务控制块（TCB）中： 
     当任务被调度器交换出去时，任务的上下文会保存在其
     TCB 中。以前，任务的上下文保存在其堆栈中。

  3. 仅在单独的、仅限特权的堆栈上执行系统调用：FreeRTOS
     系统调用以更高的权限执行，现在使用单独的
     仅限特权的堆栈。以前，
     系统调用使用调用任务的堆栈。应用程序写入器
     可以使用新的 configSYSTEM_CALL_STACK_SIZE 配置宏
     来控制系统调用堆栈的大小。

  4. 内存边界检查：接受指针并取消引用的 FreeRTOS 系统调用，
     现在要验证调用任务是否拥有所需的权限，
     以访问指针引用的内存位置。

  5. 系统调用限制：以下系统调用不再
     可用于非特权任务：

     - vQueueDelete
     - xQueueCreateMutex
     - xQueueCreateMutexStatic
     - xQueueCreateCountingSemaphore
     - xQueueCreateCountingSemaphoreStatic
     - xQueueGenericCreate
     - xQueueGenericCreateStatic
     - xQueueCreateSet
     - xQueueRemoveFromSet
     - xQueueGenericReset
     - xTaskCreate
     - xTaskCreateStatic
     - vTaskDelete
     - vTaskPrioritySet
     - vTaskSuspendAll
     - xTaskResumeAll
     - xTaskGetHandle
     - xTaskCallApplicationTaskHook
     - vTaskList
     - vTaskGetRunTimeStats
     - xTaskCatchUpTicks
     - xEventGroupCreate
     - xEventGroupCreateStatic
     - vEventGroupDelete
     - xStreamBufferGenericCreate
     - xStreamBufferGenericCreateStatic
     - vStreamBufferDelete
     - xStreamBufferReset

     此外，非特权任务不能再使用 vTaskSuspend 挂起
     除自身以外的任何任务。

  我们感谢以下人员对这些增强功能的贡献：

  - Meta Platforms, Inc. 的 David Reiss。
  - 中国东南大学计算机科学与工程学院的
    Lan Luo、Xinhui Shao、Yumeng Wei、Zixia Liu、Huaiyu Yan 和 Zhen Ling
    。
  - 美国马萨诸塞大学洛厄尔分校计算机科学系的
    Xinwen Fu。
  - 美国科罗拉多大学博尔德分校的
    Yuequi Chen、Zicheng Wang 和 Minghao Lin。

+ 增加了 Cortex-M35P 移植。由 @urutva 贡献。

+ 为 IAR RISC-V 移植增加了嵌入式扩展 (RV32E) 支持。

+ 增加了 ulTaskGetRunTimeCounter and ulTaskGetRunTimePercent API。由 @chrisnc 贡献。

+ 增加了 API，以便从静态创建的内核对象中获取应用程序提供的缓冲区。 
  增加了以下新 API：

  - xTaskGetStaticBuffers
  - xQueueGetStaticBuffers
  - xQueueGenericGetStaticBuffers
  - xSemaphoreGetStaticBuffer
  - xEventGroupGetStaticBuffer
  - xStreamBufferGetStaticBuffers
  - xMessageBufferGetStaticBuffers

  通过这些 API，
  应用程序写入器可以从内核对象中获取静态缓冲区，并在删除时释放/重复使用这些缓冲区。以前，
  应用程序写入器必须在应用程序中
  保持静态缓冲区和内核对象的关联。由 @Dazza0 贡献。

+ 使用 picolibc 函数增加了线程本地存储 (TLS) 支持。由
  @keith-packard 贡献。

+ 增加了 configTICK_TYPE_WIDTH_IN_BITS to configure TickType_t 数据类型。因此，
  事件组中的比特数也会随着大数据类型的增加而增加。由
  @Hadatko 贡献。

+ 更新了 eTaskGetState 和 uxTaskGetSystemState，
  使待处理的就绪任务返回 eReady。由 @Dazza0 贡献。

+ 更新了 heap_4 和 heap_5，
  使其仅在生成的数据块尚未对齐时添加填充。

+ 修正了几个地方的调度器逻辑，
  以便在同等优先级的任务就绪时不抢占任务。

+ 增加了在 FreeRTOS-Plus 库中使用的宏。由 @Holden 贡献。

+ 修复了 clang 编译器警告。由 @phelter 贡献。

+ 为 ARMv8-M port 增加了断言，以检测何时从优先级高于 configMAX_SYSCALL_INTERRUPT_PRIORITY 的中断调用 FreeRTOS API
  。
  由 @urutva 贡献。

+ 为 ARM_CM0 移植增加了 xPortIsInsideInterrupt API。

+ 修复了当使用大型数据模型时，MSP430X 移植中的构建警告。

+ 在不带 FPU 的部件上增加了使用 Cortex-R5 移植的功能。

+ 修复了 PIC24/dsPIC 堆实现中的构建警告。

+ 更新了 Cortex-M 移植的中断优先级断言，
  使其不会在未实现 PRIO 位的 QEMU 上触发。

+ 更新了 ARMv7-M 移植，确保内核中断以最低优先级运行。
  configKERNEL_INTERRUPT_PRIORITY 现在已不适用于 ARMv7-M 移植，
  并使这些移植与较新的 ARMv8-M 移植保持一致。由 @chrisnc 贡献。

+ 修复了 Linux Windows 子系统 (WSL) 上 POSIX GCC 移植的编译问题。由
  @jacky309 贡献。

+ 为 Microblaze 移植增加了 portMEMORY_BARRIER。由 @bbain 贡献。

+ 为 ATmega 移植增加了 portPOINTER_SIZE_TYPE 定义。由 @jputcu 贡献。

+ 对 CMake 支持进行了多项改进。由 @phelte 和 @cookpate 贡献。


### 从 FreeRTOS V10.5.0 到 2022 年 11 月 16 日发布的 FreeRTOS V10.5.1 的变更

+ 更新清单和 SBOM 中的内核版本


### 从 FreeRTOS V10.4.6 到 2022 年 9 月 16 日发布的 FreeRTOS V10.5.0 的变更

+ ARMv7-M 和 ARMv8-M MPU 移植：通过分别向 pvTaskGetThreadLocalStoragePointer()
  或 vTaskSetThreadLocalStoragePointer
  传递一个负实参作为 xIndex 参数，
  已经独立获得执行注入代码能力的第三方
  就可以读取或写入任意地址。增加了一项检查，
  以确保传递负实参作为 xIndex 参数
  不会导致任意读取或写入。
  感谢 Certibit Consulting, LLC 报告此问题。

+ ARMv7-M 和 ARMv8-M MPU 移植：非特权任务
  可以通过将任何具有权限的函数作为参数传递给
  MPU_xTaskCreate、MPU_xTaskCreateStatic、MPU_xTimerCreate、
  MPU_xTimerCreateStatic 或 MPU_xTimerPendFunctionCall，来调用该函数。MPU_xTaskCreate
  和 MPU_xTaskCreateStatic 已更新为只允许创建非特权任务。
  删除了 MPU_xTimerCreate、MPU_xTimerCreateStatic 和
  MPU_xTimerPendFunctionCall API。
  感谢华中科技大学报告
  此问题。

+ ARMv7-M 和 ARMv8-M MPU 移植：
  对于已经独立获得执行注入代码能力的第三方来说，
  通过在
  FreeRTOS MPU API 包装函数内部直接分支，并使用手动制作的堆栈帧，就有可能实现进一步的权限升级。
  已移除本地堆栈变量 `xRunningPrivileged`，
  这样就无法通过直接在
  FreeRTOS MPU API 封装函数内部直接分支来利用手动制作的堆栈帧进行权限升级。
  感谢 Certibit Consulting, LLC、华中科技大学和
  东北大学 SecLab 团队报告
  此问题。

+ ARMv7-M MPU 移植：有可能配置重叠的内存
  保护单元（MPU）区域，
  这样非特权任务就可以访问特权数据。内核现在使用编号最高的 MPU 区域进行内核保护，
  以防止出现 MPU 配置。
  感谢东北大学 SecLab 团队报告
  此问题。

+ 增加了对 ARM Cortex-M55 的支持。

+ 增加了对 ARM Cortex-M85 的支持。由 @gbrtth 贡献。

+ 为 RISC-V 移植增加了向量模式中断支持。

+ 在 RISC-V GCC 移植中增加了对 RV32E 扩展（嵌入式配置文件）的支持。  
  由 @Limoto 贡献。

+ 堆改进：

  - 在 heap_2 中增加了一项检查，
    以跟踪内存块是否已分配给应用程序。大小字段的 MSB 用于此
    目的。同样的检查在 heap_4 和 heap_5 中已经存在。该
    检查可防止双重空闲错误。

  - 为 heap_2、heap_4 和 heap_5
    增加了新的 configHEAP_CLEAR_MEMORY_ON_FREE 标志。如果在 FreeRTOSConfig.h 中设置了该标志，
    那么使用 vPortFree() 释放的内存将自动清零。

  - 为 heap_2、heap_4 和 heap_5 增加了新的 API pvPortCalloc，
    其签名与标准库 calloc 函数相同。

  - 将指针类型更新为 portPOINTER_SIZE_TYPE。由
    @Octaviarius 贡献。

+ 为流缓冲区或消息缓冲区
  的每个实例增加了覆盖发送和接收完成回调的功能。之前，
  流缓冲区和消息缓冲区的所有实例
  都只有一个发送回调和一个接收回调。每个实例都有单独的回调，
  这样就能以不同的方式使用不同的消息缓冲区和流缓冲区，
  例如，有些用于核心间通信，有些用于同一核心通信。
  可通过  在
  FreeRTOSConfig.h 中设置配置选项 configUSE_SB_COMPLETED_CALLBACK 来控制该功能。当该选项设置为 1 时，
  可使用 API xStreamBufferCreateWithCallback() 或 xStreamBufferCreateStaticWithCallback()
  （同样也可使用消息缓冲区的 API）
  来创建具有应用程序提供的回调覆盖的流缓冲区或消息缓冲区实例。当
  该选项设置为 0 时，
  将调用由 sbSEND_COMPLETED() 和 sbRECEIVE_COMPLETED() 宏定义的默认回调。为保持
  向后兼容性，configUSE_SB_COMPLETED_CALLBACK 默认为 0。
  启用 MPU 的移植目前不支持该功能。

+ 将 FreeRTOS 的线程本地存储（TLS）支持通用化，
  使其不再与 newlib 绑定，也可与其他 c 运行时库一起使用。
  为确保向后兼容，
  newlib 支持的默认行为保持不变。

+ 增加了使用 CMake 编译系统构建和链接 FreeRTOS 的支持。由
  @yhsb2k 贡献。

+ 增加了为每个版本生成软件物料清单 (SBOM) 的支持。

+ 在 GCC Cortex-M33 移植中增加了对 16 个 MPU区域的支持。

+ 为 ARM CM4 MPU 移植增加了 ARM Cortex-M7 r0p0/r0p1 Errata 837070 解决方法。
  在 Cortex-M7 r0p0/r0p1 内核上
  使用 CM4 MPU 移植时，应用程序写入器需要定义 configENABLE_ERRATA_837070_WORKAROUND。

+ 为 Cortex-M0 移植增加了 configSYSTICK_CLOCK_HZ。当 SysTick 定时器的时钟源与 CPU 的时钟源不同时，
  需要使用此功能。

+ 为 MicroBlazeV9 移植增加了硬件堆栈保护支持。这可确保
  一旦有任务违反堆栈限制，
  CPU 就会立即引发堆栈保护违规异常。由 @uecasm 贡献。

+ 引入了 configUSE_MINI_LIST_ITEM 配置选项。当该选项设置为 1 时，
  ListItem_t 和 MiniLitItem_t 仍然是不同的类型。
  但是，当 configUSE_MINI_LIST_ITEM == 0 时，MiniLitItem_t 和 ListItem_t
  都是同一结构体 xLIST_ITEM 的定义类型。这解决了
  在启用严格别名和链接时间优化时观察到的一些问题。
  为保持向后兼容性，configUSE_MINI_LIST_ITEM 默认为 1。

+ 简化了 prvInitialiseNewTask，
  以将新分配的 TCB 结构体设置为零，并移除将单个结构体成员设置为零的代码。

+ 为 POSIX port 增加了 prvPortYieldFromISR 原型，
  以便在使用 -Wmissing-prototypes 编译器选项时不会出现任何警告。

+ 在使用 vTaskGetInfo() 获得的任务信息报告中
  增加了栈顶和栈底。由 @shreyasbharath 贡献。

+ 为队列数据结构体的 cRxLock 和 cTxLock 成员增加了上限。
  这些锁会计算队列被锁定时
  收到和发送到队列的项目数。随后，当队列解锁时，
  这些任务就会被用来解除队列中等待任务的阻塞。此 PR
  将 cRxLock 和 cTxLock 的值限定为系统中的任务数，
  因为我们无法解锁比系统中任务数更多的任务。请注意，
  如果应用程序创建的任务超过 127 个，仍会触发相同的断言。

+ 将定时器函数中的 uxAutoReload 参数更改为 xAutoReload。  现在，
  该类型是 BaseType_t。  这与 pdTRUE 和 pdFALSE 的类型相匹配。
  新函数 xTimerGetAutoReload()
  以 BaseType_t 的形式提供自动重载状态。  原有函数 uxTimerGetAutoReload 保留了
  原来的 UBaseType_t 返回值。

+ 修复了对调用 vTaskStepTick() 时带有 xExpectedIdleTime ticks 的用户
  无滴答空闲实现的支持。新代码
  确保 xTickCount 在 xTaskIncrementTick() 而不是 vTaskStepTick() 内
  达到 xNextTaskUnblockTime。这修复了一个典型情况，
  即任务在一个滴答周期后激活，以及在 xTickCount\
   溢出时的一种罕见的断言失败情况。由 @jefftenney 贡献。

+ 修复了当 pvPortMalloc 和 vPortFree 函数使用互斥锁保护时，
  事件组中的死锁。由 @clemenskresser 贡献。

+ 修复了当使用 -Wduplicated-branches GCC 选项编译时，
  tasks.c 中的警告。由 @pierrenoel-bouteville-act 贡献。

+ 修复了当 configSUPPORT_DYNAMIC_ALLOCATION 设置为零时，
  tasks.c 中的编译错误。由 @rdpoor 贡献。

+ 修复了 stream_buffer.c 中的 prvWriteMessageToBuffer() 函数，
  使其在 big endian 平台上也能正确复制长度。

+ 启用 configUSE_TICKLESS_IDLE 时，  不再需要
  将 INCLUDE_vTaskSuspend 设为 1。由 @pramithkv 贡献。

+ 将 RL78 IAR 移植更新为最新版的 IAR，
  该版本使用行业标准 ELF 格式，而不是之前的 UBROF 对象格式。
  由 @felipe-iar 贡献。

+ 当 PIC24 移植的滴答计数为 16 位时，增加了滴答类型为原子标志。这样，
  当滴答计数也是 16 位时，
  PIC24 系列的 16 位处理器就可以读取滴答计数，而无需临界区。

+ 修正了启用链接时间优化时，
  GCC CM3/CM4 mpu 移植偏移超出范围的错误。由 @niniemann 贡献。

+ 删除在 64 位 RISC-V 平台上编译 RISC-V 移植时的 #error。
  由 @cmdrf 贡献。

+ 修复了 Cortex-A53 移植中的 ullPortInterruptNesting 对齐方式，
  使其采用 8 字节对齐方式。这修复了未对齐访问异常。由
  @Atomar25 贡献。

+ 修复了  NiosII 移植的
  中断处理寄存器功能和异常处理过程。由 @ghost 贡献。

+ 更改了 Cortex-A53 SRE 移植的 FreeRTOS IRQ 处理程序，
  以存储和恢复中断确认寄存器。这可确保 SRE 移植行为
  与内存映射 IO 移植相匹配。由 @sviaunxp 贡献。

+ 更新了 uncrustify 配置文件，
  以匹配 CI 操作中使用的 uncrustify 版本。此外，在 CI 中锁定了 uncrustify 版本。由
  @swaldhoer 贡献。


### 从 FreeRTOS V10.4.5 到 2021 年 11 月 12 日发布的 FreeRTOS V10.4.6 的变更

+ ARMv7-M 和 ARMv8-M MPU 移植——
  通过将 xPortRaisePrivilege 和 vPortResetPrivilege 改为宏，
  防止非内核代码调用内部函数。

+ 引入新配置 configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS，
  使开发人员能够阻止非特权任务访问临界区。
  为了向后兼容，默认值为 1。应用程序应将其设置为 0，
  以禁止非特权任务访问临界区。


### 从 FreeRTOS V10.4.4 到 2021 年 9 月 10 日发布的 FreeRTOS V10.4.5 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.4.5.html

+ 引入了 configRUN_TIME_COUNTER_TYPE，
  使开发人员能够定义用于保存运行时间统计计数器的类型。默认为 uint32_t，
  以便向后兼容。
  #在 FreeRTOSConfig.h 中将 configRUN_TIME_COUNTER_TYPE 定义为一种类型（例如 uint64_t），以覆盖默认值。

+ 引入了 ulTaskGetIdleRunTimePercent() 以补充已有的
   ulTaskGetIdleRunTimeCounter()。原有函数返回的是
  运行时间计数器的原始值，而新函数返回的是
  空闲任务消耗的时间占整个运行时间的百分比。请注意，
  只有在没有其他任务以空闲优先级执行、未使用无滴答空闲且
  configIDLE_SHOULD_YIELD 设置为 0 的情况下，
  空闲时间才能很好地反映系统中的闲置时间。

+ ARMv8-M 安全端移植：  从
  ARMv8-M MCU（ARM Cortex-M23 和 Cortex-M33）的非安全端调用安全函数的任务
  有两种上下文，一种位于非安全端，另一种位于安全端。以前版本的
  FreeRTOS ARMv8-M 安全端移植会在运行时
  分配参考安全端运行时上下文的结构体。  现在，结构体
  在编译时被静态分配。  这一变更要求
  引入 secureconfigMAX_SECURE_CONTEXTS 配置常量，
  用于设置静态分配的安全上下文数量。
  secureconfigMAX_SECURE_CONTEXTS 如果未定义，则默认为 8。
  仅在非安全端使用 FreeRTOS 代码的应用程序，
  如在安全端运行第三方代码的应用程序，
  不受此更改的影响。


### 从 FreeRTOS V10.4.3 到 2021 年 5 月 28 日发布的 FreeRTOS V10.4.4 的变更

+ 通过提供 uxListRemove() 和 vListInsertEnd() 的宏版本的，
  对 xTaskIncrementTick() 的性能进行了小幅改进。

+ 对 timers.c 进行了小幅重构，
  不再需要使用 tmrCOMMAND_START_DONT_TRACE 宏，
  也不再需要 timers.c 向自己的事件队列发布信息。  这一更改的结果是，
  错过预定下一次执行时间的自动重载定时器将立即重新执行，
  而不是在下一次处理命令队列时再次执行
  。  (感谢 Jeff Tenney）。

+ 修复了消息缓冲实现中的争用条件。  根本原因是
  长度和数据字节的写入和读取是两个不同的操作，
  它们都会修改缓冲区的大小。如果
  上下文切换发生在添加或删除长度字节之后，
  但在添加或删除数据字节之前，
  那么其他任务可能会发现消息缓冲区处于无效状态。

+ xTaskCreate() 和 xTaskCreateStatic() 函数
  接受任务优先级作为输入参数。  如果优先级被设置为高于该值，
  优先级将始终被悄悄地设置为不高于（configMAX_PRIORITIES - 1）。
  现在，高于该优先级的值也会触发 configASSERT() 失效。

+ 将 vQueueAddToRegistry 中的 configASSERT( pcQueueName )
  替换为 NULL 指针检查。

+ 引入了 configSTACK_ALLOCATION_FROM_SEPARATE_HEAP
  配置常量，
  使得分配给任务的堆栈可以是来自其他内存分配所用堆之外的堆。  这样，
  堆栈就能被放置在特殊区域内，如快速紧密耦合内存。

+ 如果试图在队列注册表中多次添加同一个队列或信号量句柄，
  那么以前的版本会创建两个不同的条目
  。  如果这样做，第一个条目就会被覆盖，
  而不是被复制。

+ 将 ESP32 移植和 TF-M（可信固件 M）代码
  更新为各自软件库中的最新版本。

+ 修复了 POSIX 移植中的一个构建错误。
+ 其他小的格式更新，
  包括在更多文件中用空格替换制表符。

+ 其他小更新，
  包括增加额外的 configASSERT() 检查以及更正和改进代码注释。

+ 请访问 smp 分支，查看 Symetric 多处理内核的进展情况。
  https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp


### 从 FreeRTOS V10.4.2 到 2020 年 12 月 14 日发布的 FreeRTOS V10.4.3 的变更

V10.4.3 包含在 202012.00 LTS 版本中。  了解更多信息，请访问 https:/freertos.org/lts-libraries.html

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.4.x.html

+ 改进了堆、队列和流缓冲区中
  缓冲区分配的稳健性和一致性。

+ 以下函数无法再被非特权代码调用。

  - xTaskCreateRestricted
  - xTaskCreateRestrictedStatic
  - vTaskAllocateMPURegions


### 从 FreeRTOS V10.4.1 到 2020 年 11 月 10 日发布的 FreeRTOS V10.4.2 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.4.x.html

+ 修复了 ARMv8-M 移植中的一个问题，
  该问题会导致 BASEPRI 在第一个任务开始执行
  和该任务调用 FreeRTOS API 之间被屏蔽。

+ 引入了 xTaskDelayUntil()，
  其功能等同于 vTaskDelayUntil()，
  但增加了一个返回值，
  用于指示函数是否将调用任务置于阻塞状态。

+ 将 WolfSSL 更新至 4.5.0 并增加了 FIPS ready 演示。

+ 在第三方 Xtensa 移植中增加了对 ESP IDF 4.2 的支持。

+ 重新引入了 uxTopUsedPriority 以支持 OpenOCD 调试。

+ 将 FreeRTOS/FreeRTOS 中的大多数依赖库转换为子模块。

+ 进行可各种一般性维护和改进，以确保 MISRA 合规性。


### 从 FreeRTOS V10.4.0 到 2020 年 9 月 17 日发布的 FreeRTOS V10.4.1 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.4.x.html

+ 修复了一个错误命名的参数，
  该参数导致 ulTaskNotifyTakeIndexed 宏无法编译，
  以及测试代码中的名称空间冲突，该冲突导致此错误未能引起测试失败。


### 从 FreeRTOS V10.3.1 到 2020 年 9 月 10 日发布的 FreeRTOS V10.4.0 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.4.x.html

主要改进：

+  任务通知：  在 FreeRTOS V10.4.0 之前，
  每个创建的任务只有单条直达任务通知。  从 FreeRTOS V10.4.0 开始，
  每个任务都有一个通知数组。  直达任务通知 API 已通过
  后缀为 "Indexed" 的 API 函数进行了扩展，
  使 API 可以在任意数组索引下对任务通知进行操作。  请参阅
  https://www.freertos.org/RTOS-task-notifications.html 了解更多信息。
+ 支持内存保护单元 (MPU) 的内核移植：ARMv7-M 和
  ARMv8-M MPU 移植现在支持仅有权限访问的堆。ARMv7-M
  MPU 移植现在支持具有 16 个 MPU 区域的设备，
  能够覆盖特权代码
  和数据区域的默认内存属性，并能将 FreeRTOS 内核代码置于
  闪存之外。ARMv8-M MPU 移植现在支持无滴答空闲模式。
  请参阅 https://www.freertos.org/FreeRTOS-MPU-memory-protection-unit.html
  了解更多信息。

其他值得注意的更新：

+ 代码格式化现已自动化，以增加
  Git 中的协作开发。  自动格式化代码与
  原来的格式化惯例不尽相同。  值得注意的是，现已使用空格
  代替制表符。

+ 回调函数（以 “Application ”开头的函数，
  如 vApplicationStackOverflowHook()）的原型现在位于 FreeRTOS
  头文件中，应用程序写入器无需
  在定义函数的 C 文件中添加原型。

+ 新的 Renesas RXv3 移植层。

+ 更新了 Synopsys ARC 代码，包括对 EM 和 HS 内核的支持，
  以及对更新 BSP 的支持。

+ 增加了 POSIX 移植层，允许 FreeRTOS 在 Linux 主机上运行，
  就像 Windows 移植层允许 FreeRTOS 在 Windows 主机上运行一样
  。

+ 还有许多其他小的优化和改进。详情
  请参阅 https://github.com/FreeRTOS/FreeRTOS-Kernel/commits/main


### 从 FreeRTOS V10.3.0 到 2020 年 2 月 18 日发布的 FreeRTOS V10.3.1 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.3.x.html

+ 从该文件中删除了 ./FreeRTOS-Labs 目录。其中包含的库
  现在可以单独下载。


### 从 FreeRTOS V10.2.1 到 2020 年 2 月 7 日发布的 FreeRTOS V10.3.0 的变更

请参阅 https://www.FreeRTOS.org/FreeRTOS-V10.3.x.html

新的和更新的内核移植：

+ 为 IAR 编译器增加了 RISC-V 移植。

+ 更新了 Windows 模拟器移植以使用同步对象，
  防止出现用户报告的错误，
  即任务在转入阻塞状态后继续运行很短的时间。  请注意，
  我们无法复制报告的问题，这可能取决于您的 CPU 型号。

+ 当 configISR_STACK_SIZE_WORDS 定义为非零值时，正确对齐 RISC-V
  移植中的堆栈顶部，
  这将导致中断堆栈被静态分配。

+ RISC-V 机器定时器比较寄存器现在可用于任何 HART，
  而以前总是假定 FreeRTOS 在 HART 0 上运行。

+ 更新了
  用于在 32 位内核上更新 64 位机器定时器比较寄存器的顺序，使其与 RISC-V
  文档中建议的顺序一致。

+ 在 ARM、IAR 和 GCC Cortex-M0 编译器移植中增加了无滴答低功耗模式
  。

+ 更新了 ARMv7-M MPU（内存保护单元）移植的行为，
  使其与 ARMv8-M 移植的行为一致，
  即特权升级只能来自内核自己的内存段。  增加了
  configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY 配置产量。

+ 更新现有 MPU 移植，以便在更新前正确禁用 MPU
  。

+ 增加了 T-Head（正式名称为 C-SKY）
  微控制器的贡献移植和演示应用程序。

新的 API 函数：

+ 增加了 vPortGetHeapStats() API 函数，
  该函数可返回有关 heap_4 和 heap_5 状态的信息。

+ 增加了 xTaskCatchUpTicks()，
  它可在应用程序代码长时间禁用中断后修正滴答计数值。

+ 增加了 xTaskNotifyValueClear() API 函数。

+ 增加了 uxTimerGetReloadMode() API 函数。

其他杂项更改：

+ 将 uxPendedTicks 的类型从 UBaseType_t 改为 TickType_t，
  以确保与之比较的变量具有相同的类型，
  因此也重新命名了变量 xPendingTicks。

+ 更新了使用 MPU 的 Keil 项目，
  使内存区域来自链接器脚本（分散文件）变量，而不是硬编码。

+ 为 GCC (MCUXpresso)、Keil 和 IAR
  编译器增加了 LPC51U68 Cortex-M0+ 演示。

+ 增加了 CORTEX_MPU_STM32L4_Discovery_Keil_STM32Cube 演示。

+ 增加了 LPC54018 MPU 演示。

+ 将 xTaskGetIdleRunTimeCounter() 重命名为 ulTaskGetIdleRunTimeCounter()。


### 从 FreeRTOS V10.2.0 到 2019 年 5 月 13 日发布的 FreeRTOS V10.2.1 的变更：

+ 增加了 ARM Cortex-M23 移植层，
  作为原有的 ARM Cortex-M33 移植层的补充。

+ RISC-V 移植现在可在 32 位和 64 位内核之间自动切换
  。

+ 引入了 portMEMORY_BARRIER 宏，
  以防止在使用 GCC 链接时间优化时出现指令重排。

+ 为 ARMv8-M 移植引入了 portDONT_DISCARD 宏，
  以防止安全端构建删除
  非安全端构建所需的符号。

+ 引入了 portARCH_NAME，
  为选择半自动构建环境提供额外数据。

+ Cortex-M33 和 Cortex-M23 移植现在可以正确禁用 MPU
  （在更新 MPU 寄存器之前）。

  + 增加了 Nuvoton NuMaker-PFM-M2351 ARM Cortex-M23 演示。
  + 增加了 LPC55S69 ARM Cortex-M33 演示。
  + 增加了一个 STM32 双核 AMP 压力测试演示。


### 从 FreeRTOS V10.1.1 到 2019 年 2 月 25 日发布的 FreeRTOS V10.2.0 的变更：

+ 增加了 GCC RISC-V MCU 移植和三个独立的演示应用程序。
+ 包含了已有的 ARM Cortex-M33 (ARMv8-M) GCC/ARMclang 和 IAR 移植
  以及 Keil 模拟器演示。

+ 更新了用于检测定时器是否处于活动状态的方法。  此前，
  如果定时器没有被列表引用，就会被认为处于非活动状态。
  但是，当更新定时器时，
  它会暂时从列表中删除，然后再重新添加到列表中，因此现在定时器的活动状态是单独存储的。

+ 增加了 vTimerSetReloadMode()、xTaskGetIdleRunTimeCounter() 和
  xTaskGetApplicationTaskTagFromISR() API 函数。

+ 更新了第三方 Xtensa 移植，使其获得 MIT 许可。

+ 为 Renesas
  编译器 RX600v2 移植增加了 configINCLUDE_PLATFORM_H_INSTEAD_OF_IODEFINE_H，
  以便在该移植的 port.c 文件中切换 platform.h 和 iodefine.h 的包含。

+ 删除了 MPU 移植中的 “FromISR” 函数，
  因为 ISR 是以特权方式运行的。

+ 增加了 uxTaskGetStackHighWaterMark2() 函数，
  以便在不破坏向后兼容性的情况下更改返回类型。
  uxTaskGetStackHighWaterMark() 一如既往地返回 UBaseType_t，
  而 uxTaskGetStackHighWaterMark2() 则返回 configSTACK_DEPTH_TYPE，
  以便用户确定返回类型。

+ 修复了内存保护移植中
  与仅静态内存和仅动态内存构建的不同组合有关的问题。  因此，
  tskSTATIC_AND_DYNAMIC_ALLOCATION_POSSIBLE 的定义变得更加复杂，
  被移至 FreeRTOS.h，并用表格解释其定义。

+ 增加了 “从 ISR 获取任务标记”函数。

+ 将用于确定定时器是否处于活动状态的方法
  从查看是否从活动定时器列表中引用
  改为明确存储其活动状态。  这一更改
  可防止定时器在从一个列表移动到另一个列表时报告其处于非活动状态。

+ 传入任务创建函数的 pcName 参数可以是 NULL，
  而此前必须提供一个名称。

+ 使用无滴答空闲时，如果调度程序未暂停，
  现在只在 xTaskRemoveFromEventList() 中调用 prvResetNextTaskUnblockTime()。

+ 引入了 portHAS_STACK_OVERFLOW_CHECKING，
  对于在具有堆栈限制寄存器的架构上运行的 FreeRTOS 移植，应将其设置为 1。


### 从 FreeRTOS V10.1.0 到 2018 年 9 月 7 日发布的 FreeRTOS V10.1.1 的变更

+ 撤销了几个结构体名称更改，
  这些更改破坏了几个内核感知调试器插件。

+ 更新至最新的跟踪记录器代码。

+ 修复了 FreeRTOS+TCP TCP/IP 堆栈代码中的一些格式。

+ 撤销了将某些变量从文件移到函数作用域的做法，
  因为这样做会破坏需要移除静态修饰符的调试场景。


### 从 FreeRTOS V10.0.1 到 2018 年 8 月 22 日发布的 FreeRTOS V10.1.0 的变更

FreeRTOS 内核更改：

+ 更新了对 MISRA 合规性的 Lint 检查，
  采用了最新的 MISRA 标准，之前使用的是原始的 MISRA 标准。

+ 更新了所有对象句柄（TaskHandle_t、QueueHandle_t 等），
  使其成为唯一类型而非空指针，从而提高了类型安全性。  (几年前曾尝试过，
  但由于一些调试器中的错误而不得不放弃）
  。  请注意，
  这需要重命名 ListItem_t 结构体的 pvContainer 成员——如果这导致问题，
  请将 configENABLE_BACKWARD_COMPATIBILITY 设置为 1。

+ 增加了 configUSE_POSIX_ERRNO，
  以更友好的方式启用每个任务的 POSIX 式 errno 功能——
  之前通用线程本地存储功能用于此目的。

+ 为 XCC 编译器增加了 Xtensa 移植和演示应用程序。

+ 更改了 Win32 移植的 vPortEndScheduler() 实现，
  使其只需调用 exit( 0 )。

+ 修复了 GCC Microblaze 移植 vPortEnableInterrupt() 中的错误，
  以保护对 Microblaze 内部寄存器的读修改写访问。

+ 修复了使用 MPU 时出现的原型差异、
  静态结构体大小差异等小问题。

+ TaskStatus_t 结构体中的 usStackHighWaterMark 成员
  现在使用 configSTACK_DEPTH_TYPE 类型，而不是 uint16_t——
  这一更改本应在引入 configSTACK_DEPTH_TYPE 类型
  （可规避堆栈大小规格的 16 位限制）时作出。

+ 增加了 xMessageBufferNextLengthBytes() API 函数
  和相应的流缓冲区。

+ 引入了 configMESSAGE_BUFFER_LENGTH_TYPE，
  允许减少消息缓冲区中用于保存消息长度的字节数。
  configMESSAGE_BUFFER_LENGTH_TYPE 的默认值为 size_t，
  但如果信息永远不能超过 255 字节，则可以将其设置为 uint8_t，
  这样每次向信息缓冲区写入信息时就可以节省 3 个字节
  （假设 sizeof( size_t ) 为 4）。

+ 更新了 StaticTimer_t 结构体，
  以确保当 TaskFunction_t 的大小不等于 void * 的大小时，
  它与 Timer_t 结构体的大小相匹配。

+ 更新了各种 Xilinx 演示，以使用 2018.1 版 SDK 工具。

+ 对演示任务进行了各种更新，以保持测试覆盖率。

+ 在 FreeRTOS V10.1.0 中删除了 FreeRTOS+UDP，
  因为它被 FreeRTOS+TCP 取代，而后者在 FreeRTOS
  V10.0.0 中被引入主下载。  FreeRTOS+TCP 可配置为仅 UDP 堆栈，
  而 FreeRTOS+UDP 不包含应用于 FreeRTOS+TCP 的补丁。

FreeRTOS+TCP 更改：

+ 在数据包解析例程、DNS
  缓存以及 TCP 序列号和 ID 生成方面进行了多项安全改进和修复。

+ 默认情况下禁用 NBNS 和 LLMNR。

+ 默认情况下添加 TCP 挂起保护。

感谢 Zimperium zLabs 团队的 Ori Karliner 报告这些问题。


### 从 FreeRTOS V10.0.0 到 2017 年 12 月 20 日发布的 FreeRTOS V10.0.1 的变更

+ 修复了 stream_buffer.h 中 “#if defined( __cplusplus )” 的位置。

+ 更正了 mpu_prototypes.h 中 MPU_xQueuePeek() and MPU_xQueueSemaphoreTake() 的声明
  。

+ 更正了 vTaskList() 辅助函数
  在打印当前执行任务的状态时的格式。

+ 如果编译 stream_buffer.c 时
  未设置 configUSE_TASK_NOTIFICATIONS 为 1，则引入 #error。

+ 更新 FreeRTOS+TCP 到 V2.0.0

  - 改进了在使用 WinPCap 的 Windows 系统中
    使用 FreeRTOS+TCP 时显示可用网文接口的文本格式。

  - 引入了 ipconfigSOCKET_HAS_USER_WAKE_CALLBACK 选项，
    以便在数据到达套接字时执行用户定义的回调。


### 从 FreeRTOS V9.0.1 到 FreeRTOS V10.0.0 的变更：

FreeRTOS 内核现已获得 MIT 许可：https://www.FreeRTOS.org/license

新功能和组件：

+ 流缓冲区——请参阅 https://www.FreeRTOS.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example
+ 消息缓冲区——请参阅 https://www.FreeRTOS.org//RTOS-message-buffer-example.html

+ 将 FreeRTOS+TCP 与基本 Win32
  TCP 演示 FreeRTOS_Plus_TCP_Minimal_Windows_Simulator 一起移入主存储库。

新移植或演示：

+ 增加了 TI SimpleLink CC3220 MCU 演示。

+ 为 Microchip CEC and MEC 17xx and 51xx MCU 增加了 MPU 和非 MPU 项目
  。

+ 增加了 CORTEX_MPU_Static_Simulator_Keil_GCC 演示，
  以测试 MPU 移植中的静态分配。

修复或改进：

+ Cortex-M 移植在调用 vTaskSwitchContext 之前会推送额外的寄存器，
  以确保保持 8 字节对齐。  只有
  在用户定义的滴答钩子函数执行需要 8 字节对齐的操作时
  才重要。

+ 优化了 Cortex-M 设备上
  标准无滴答空闲模式的实现。

+ 改进了 Win32 移植‘’，包括使用优先级更高的线程。

+ 确保 PIC32 移植的中断堆栈对齐。

+ 更新了 GCC TriCore 移植，以便与更高版本的编译器一起构建。

+ 更新了 mpu_wrappers.c 以支持静态分配。

+ List_t 的 uxNumberOfItems 成员现在是易失型—— 

  解决了在使用 IAR 编译器进行最大优化时出现的问题。

+ 引入了 configRECORD_STACK_HIGH_ADDRESS。  设置为 1 时，
  堆栈起始地址将保存到每个任务的 TCB 中（假设堆栈向下增长）。

+ 引入了 configINCLUDE_FREERTOS_TASK_C_ADDITIONS_H，
  允许在 FreeRTOS 的 tasks.c 源文件中
  添加用户定义的功能和用户定义的初始化。  当 configINCLUDE_FREERTOS_TASK_C_ADDITIONS_H 设置为 1 时，
  用户提供的名为 freertos_task_c_additions.h 的头文件
  将包含在 tasks.c 的底部。  在该头文件中定义的函数
  可以调用 freertos_tasks_c_additions_init()，
  后者又会调用一个名为 FREERTOS_TASKS_C_ADDITIONS_INIT() 的宏（如果它被定义的话）。
  可在 FreeRTOSConfig.h 中定义 FREERTOS_TASKS_C_ADDITIONS_INIT()。

+ 引入了可由用户
  在 FreeRTOSConfig.h 中定义的 configPRE_SUPPRESS_TICKS_AND_SLEEP_PROCESSING( x )。  该宏
  在评估是否进入无滴答空闲模式之前被调用。  如果该宏将 x 设为零，
  则不会进入无滴答空闲模式。  这样，
  用户就可以在调用无滴答空闲函数之前，
  中止进入无滴答空闲模式——
  以前只能在无滴答空闲函数内部中止。

+ 添加了 configPRINTF()，
  用户可通过它定义所有库使用相同的打印格式。

+ 引入了 configMAX() 和 configMIN() 宏，
  默认为标准的 max( x, y ) 和 min( x, y ) 宏行为，
  但如果应用程序写入器在 FreeRTOSConfig.h 中定义了相同的宏，则可以重写。

+ 更正了在 INCLUDE_xTaskAbortDelay 设置为 1 时的
  StaticTask_t 定义。

+ 引入了 configTIMER_SERVICE_TASK_NAME 和 configIDLE_TASK_NAME，
  两者都可以在 FreeRTOSConfig.h 中定义为字符串，
  以分别更改定时器服务和空闲任务的默认名称。

+ 只有在使用堆栈检查
  或高水位线检查/查看时，才用已知值填充新创建任务的堆栈，
  从而消除其他情况下对 memset() 的依赖。

+ 引入了 xTaskCreateRestrictedStatic()，
  以便在 MPU 中使用静态分配。

+ 确保被挂起的任务
  无法通过收到的任务通知取消挂起。

+ 修复了 vTaskSetTimeOutState() 中的争用条件。

+ 将跟踪记录器文件更新为最新版本。


### 自 FreeRTOSV9.0.0 以来的变更：

+ 当一个任务试图获取一个由较低优先级任务持有的互斥任务时，
  如果该任务在获取互斥任务之前超时
  （导致持有互斥任务的优先级提高，
  然后根据优先级继承协议再次降低），
  则优先级不继承行为得到了增强。

+ 将重载的 xQueueGenericReceive() 函数拆分为三个独立的
  专用函数。

+ 通过
  在
  FreeRTOSConfig.h 中分别定义 configIDLE_TASK_NAME 和 configTIMER_SERVICE_TASK_NAME 定义，允许覆盖赋予空闲和定时器任务的默认人可读文本名称。

+ 引入了 configINITIAL_TICK_COUNT，
  允许系统启动时，滴答计数的值大于 0。  虽然将 configUSE_16_BIT_TICKS 设置为 1
  也可用于测试频繁的滴答溢出，
  但该更改对测试而言非常有用。

+ 确保在启动第一个任务之前，
  将 Cortex-M SysTick 计数清零。

+ 在 ARM Cortex-M 移植中增加了 configASSERT()
  以检查优先级位设置的数量。

+ 在启动 ARM Cortex-M4F 移植前清空“控制”寄存器，
  以防在调度器启动前使用 FPU。  这样只是在主堆栈上节省了几个字节，
  因为这样可以避免
  为稍后保存 FPU 寄存器留下空间。

+ 增加了 xSemaphoreGetMutexHolderFromISR()。

+ 将 MPU 移植中的 portNVIC_PENDSVSET 更正为 portNVIC_PENDSVSET_BIT。

+ 引入了 configSTACK_DEPTH_TYPE，
  允许用户在使用 xTaskCreate() 时更改用于指定堆栈大小的类型。  由于历史原因，
  当 FreeRTOS 仅用于小型 MCU 时，其类型被设置为 uint16_t，
  但当 FreeRTOS 用于大型处理器时，
  其限制性就太大了。  configSTACK_DEPTH_TYPE 默认为 uint16_t。
  xTaskCreateStatic() 是一个较新的函数，使用 uint32_t。

+ 提高了 Win32 移植使用的 Windows 线程的优先级。  由于所有线程都在同一个内核上运行，
  而且线程运行的优先级非常高，
  因此主机有可能会出现反应迟钝的情况，
  所以也要防止 Windows 移植在单核主机上执行。


### 从 FreeRTOS V9.0.0 到 2016 年 5 月 25 日发布的 FreeRTOS V9.0.0rc2 的变更：

请参阅 https://www.FreeRTOS.org/FreeRTOS-V9.html

RTOS 内核更新：

+ 修改了新 xTaskCreateStatic() API 函数的原型，
  删除了一个参数，
  并提高了与其他新 “CreateStatic()” API 函数的兼容性。  xTaskCreateStatic() 中的
  堆栈大小参数现在是 uint32_t，
  这改变了回调函数的原型。  请参阅以下链接：
  https://www.FreeRTOS.org/xTaskCreateStatic.html

+ GCC ARM Cortex-A 移植：  引入了 configUSE_TASK_FPU_SUPPORT
   常量。  当 configUSE_TASK_FPU_SUPPORT 设置为 2 时，
  每个任务都会自动获得浮点（FPU）上下文。

+ GCC ARM Cortex-A 移植：  现在可以通过定义
  vApplicationFPUSafeIRQHandler() 而不是 vApplicationIRQHandler()，
  可以在进入每个潜在嵌套中断时
  自动保存和恢复所有浮点（FPU）寄存器。

+ 所有 ARM Cortex-M3/4F/7 移植：  为严格遵守 ARM Cortex-M3/4/7 架构文档的规定，
  在创建任务时
  清除任务入口地址堆栈中的最小有效位
  （除非使用 QMEU 模拟器，否则无明显影响）。

+ 增加了 GCC 和 Keil ARM Cortex-M4F MPU移植——此前仅 ARM Cortex-M3 支持 MPU
  。

+ ARM Cortex-M3/4F MPU 移植：  对其进行更新以全面支持 FreeRTOS V9.0.0
  API（创建静态对象除外），同时增加了
  FreeRTOS/Demo/CORTEX_MPU_Simulator_Keil_GCC 演示应用程序以
  展示如何使用更新的 MPU 移植。

+ 所有 ARM Cortex-M3/4F/7 移植：  在默认的低功耗无滴答实现中
  增加了额外的隔离指令。

+ 所有 ARM Cortex-M0 移植：  防止项目
  留在第一个执行任务的堆栈中。

+ Win32 移植：  减少了堆栈使用量，改变了 Windows 线程的删除方式，
  以延长最长执行时间。

+ 为 MikroC 编译器增加了一个 ARM Cortex-M4F 移植。  使用前
  请务必阅读该移植的文档页面。

+ MPS430X IAR 移植：  更新以兼容最新发布的 EW430 工具
  。

+ IAR32 GCC 移植：  更正了
   configMAX_API_CALL_INTERRUPT_PRIORITY == portMAX_PRIORITY 时的 vPortExitCritical()。

+ 为了保持一致，vTaskGetTaskInfo() 现在有了别名 vTaskGetInfo()，
  xTaskGetTaskHandle() 现在有了别名 xTaskGetHandle()，
  pcQueueGetQueueName() 现在有了别名 pcQueueGetName()。

+ 修复了注释和编译器警告中的各种错误。

 演示应用程序更新：

+ 更新了 Atmel Studio 项目以使用 Atmel Studio 7。

+ 更新了 Xilinx SDK 项目，以使用 2016.1 版本的 SDK。

+ 消除了 PIC32 演示对传统 IO 库的依赖。

+ 将 Xilinx UltraScale Cortex-R5 演示移到主发行版中。

+ 将 MSP432 库更新到最新版本。

+ 为 GCC、Keil 和 MikroC 编译器增加了 Microchip CEC1302（ARM Cortex-M4F）演示
  。

+ 将 Atmel SAMA5D2 演示移到主发行版中。


### 从 FreeRTOS V9.0.0rc1 到 2016 年 3 月 30 日发布的 FreeRTOS V9.0.0rc2（候选发布版 2）
的变更：

注——详细信息请参阅 https://www.FreeRTOS.org/FreeRTOS-V9.html

+ 简化了使用静态内存分配创建 RTOS 对象的函数，
  并且如果将缓冲区传递给函数为 NULL，
  则不会恢复为使用动态分配。

+ 引入了 configSUPPORT_DYNAMIC_ALLOCATION 配置常量，
  允许在未定义堆的情况下构建 FreeRTOS 应用程序
  。位于
  /FreeRTOS/demo/WIN32-MSVC-Static-Allocation-Only 目录中的 Win32 示例
  可作为不包含 FreeRTOS 堆的项目的参考。

+ 小幅运行时优化。

+ 增加了两个针对 Silicon Labs EFM32 微控制器的
  新型低功耗无滴答实现。

+ 添加了 xTimerGetPeriod() 和 xTimerGetExpireTime() API 函数。


### 从 FreeRTOS V8.2.3 到 2016 年 2 月 19 日发布的 FreeRTOS V9.0.0rc1（候选发布版 1）
的变更：

RTOS 内核更新：

+ 主要新功能——现在可以使用静态分配内存创建任务、信号量、队列、定时器和事件组，
  因此无需调用
   pvPortMalloc()。

+ 主要新功能——增加了 xTaskAbortDelay() API 函数，
  该函数允许一个任务强制另一个任务立即解除阻塞状态，
  即使阻塞任务正在等待的事件尚未发生，
  或阻塞任务的超时尚未结束。

+ 允许 FreeRTOS 在 64 位架构上运行所需的更新。

+ 增加了 vApplicationDaemonTaskStartupHook()，当 RTOS
  守护进程任务（以前称为定时器服务任务）开始运行时执行
  。  如果应用程序包含会从调度器启动后执行中受益的初始化代码，
  这将非常有用。

+ 增加了 xTaskGetTaskHandle() API 函数，
  该函数可从任务名称中获取任务句柄。  xTaskGetTaskHandle() 使用多字符串比较运算，
  所以建议每个任务只调用一次。
  xTaskGetTaskHandle() 返回的句柄可存储在本地，
  以备日后重用。

+ 增加了 pcQueueGetName() API 函数，
  该函数从队列的句柄中获取队列名称。

+ 当 configUSE_PREEMPTION 为 0 时，也可以使用无滴答闲置（适用于低功耗应用）
  。

+ 如果一个任务删除了另一个任务，
  那么被删除任务的堆栈和 TCB 就会立即被释放。  如果一个任务删除了自己，
  那么被删除任务的堆栈和 TCB 会像之前一样被空闲任务释放。

+ 如果一个任务通知被用来从 ISR 中解锁一个任务，
  但没有使用 xHigherPriorityTaskWoken 参数，那么就挂起一个上下文切换，
  然后在下一个滴答中断期间发生。

+ Heap_1.c 和 Heap_2.c 现在使用之前仅由 heap_4.c 使用的 configAPPLICATION_ALLOCATED_HEAP 设置
  。
  configAPPLICATION_ALLOCATED_HEAP 允许应用程序写入器声明
  将被用作 FreeRTOS 堆的数组，
  并在这样做时将堆放在一个特定的内存位置。

+ TaskStatus_t 结构体用于获取任务的详细信息。
  TaskStatus_t 现在包含了任务堆栈的 bae 地址。

+ 增加了 vTaskGetTaskInfo() API 函数，
  该函数会返回一个包含单个任务信息的 TaskStatus_t 结构体。  此前，
  只能一次性获得所有任务的此类信息，
  作为 TaskStatus_t 结构体的数组。

+ 新增了 uxSemaphoreGetCount() API 函数。

+ 在一些 Cortex-M3 移植层中复制以前的 Cortex-M4F 和 Cortex-M7 优化
  。

 演示应用程序更新：

在 FreeRTOS V9 最终版发布之前，
还将增加更多的演示应用程序。

+ 更新了 SAM4L Atmel Studio 项目以使用 Atmel Studio 7。
+ 增加了 ARM Cortex-A53 64 位移植。

+ 增加了用于 Xilinx Ultrascale MPSoC 上 ARM Cortex-A53 64 位内核的
  移植和演示。
+ 增加了 Cortex-M7 SAME70 GCC 演示。

+ 增加了 EFM32 Giant and Wonder Gecko 演示。


### 从 V8.2.2 到 2015 年 10 月 16 日发布的 V8.2.3 的变更

RTOS 内核更新：

+ 修复了在 V8.2.2 中对软件定时器代码所作修改中发现的错误，
  该错误允许无滴答低功耗应用程序
  在使用软件定时器时无限期休眠。

+ 简化了堆栈溢出检查并提高了其效率。

+ 增加了 xTaskNotifyStateClear() API 函数。

+ 新的 IAR 和 GCC Cortex-R 移植，
  适用于不使用 ARM 通用中断控制器 (GIC) 的微处理器。

+ 新的 PIC32MEC14xx 移植。

+ 在 PIC32MZ 移植中增加了对 PIC32MZ EF 部件（带浮点）的支持
  。

+ Zynq7000 移植层现在将设置和清除滴答中断的函数声明为弱符号，
  以便应用程序可以重写，
  并使用全局 XScuGic 对象，
  以便应用程序代码可以使用相同的对象。

+ 引入了 configUSE_TASK_FPU_SUPPORT，
  尽管 PIC32MZ EF 移植是目前唯一使用它的移植。

+ 更新了 RL78 和 78K0 IAR 移植层，
  以改进对内存模型组合的支持。

+ 对 heap_5.c 进行了小幅更新，
  以删除某些编译器生成的编译器警告。

+ 许可简化。  请参阅官方发行版中的 /FreeRTOS/License/license.txt
  。

FreeRTOS+ 更新：

+ 更新了目录名称，以使用 WolfSSL 代替 CyaSSL，
  与 WolfSSL 的品牌重塑保持一致。

+ 更新至最新的 WolfSSL 代码。

+ 更新至最新的 FreeRTOS+Trace 记录器代码。

+ 增加了流式跟踪所需的 FreeRTOS+Trace 记录器库。

 演示应用程序更改：

+ 为 Renesas RZ/T (Cortex-R)、PIC32MZ EF（带浮点硬件的 PIC32）、
  PIC32MEC14xx、RX71M、RX113 和 RX231 增加了演示应用程序。

+ 对拼写和编译器警告进行了全面整理。


### 从 V8.2.1 到 2015 年 8 月 12 日发布的 V8.2.2 的变更

RTOS 内核更新：

+ 增加了 Intel IA32/x86 32 位移植。

+ 一般维护。

+ 在较新的事件组和软件定时器函数中增加了
   PRIVILEGED_FUNCTION 和 PRIVILEGED_DATA 宏，
  这些宏用于内存保护系统。

+ 在 projdefs.h 中增加了 FreeRTOS+ 组件使用的 errno 定义。

+ 在同一应用程序中使用软件定时器时，
  删除了防止无滴答空闲实现无限期等待的限制
  。

+ 引入了 xTaskNotifyAndQueryFromISR() 作为
  xTaskNotifyAndQuery() 的中断安全版本。

+ 为 MSP430X 移植层增加了额外的 NOP，
  以确保严格遵守硬件文档。

+ Microblaze 移植：增加了移植优化任务选择选项。

+ Microblaze 移植：此前，
  任务会继承任务创建时的异常启用状态。  现在，如果 Microblaze 设计支持异常，
  创建的所有任务都会启用异常。

+ Windows 移植：增加了额外的安全保护，
  确保正确的启动顺序和线程切换时机。

+ Windows 移植：改进了
  移植优化任务选择汇编代码的实现。

+ 更新了 heap_4 和 heap_5，以便在 64 位处理器上使用。

+ 简化了创建队列的代码。

+ 全面改进了无滴答空闲行为。

+ 确保通用内核文件中的所有变量
  均未初始化为 0 以外的值。

+ 纠正了在 heap_4 和 heap_5 中的 xHeapStructSize 的计算。

 演示应用程序更新：

+ 增加了针对 Galileo 硬件的新 IA32/x86
  移植演示项目。

+ 增加了 MSP430FR5969 演示（之前作为单独下载提供）。

+ 增加了 FreeRTOS BSP 存储库，以便自动创建 FreeRTOS 应用程序
  （在 Xilinx SDK 中自动创建）。

+ 为 SAMV71（ARM Cortex-M7）增加了 Atmel Studio / GCC 项目

+ 更新了 Xilinx SDK 项目，以使用 2015.2 版本的 SDK。

+ 删除了使用过时工具的 Microblaze 演示。

+ 增加了 MSP43FR5969 IAR 和 CCS 演示。

FreeRTOS+ 更新：

+ 更新了 FreeRTOS+Trace 记录器库，
  这需要更新 FreeRTOS+Trace 应用程序。

+ 增加了 Reliance Edge 源代码和演示应用程序。  Reliance edge
  是一种故障安全事务性文件系统，非常适合需要文件存储的应用，
  尤其适合对高可靠性要求极高的应用。

+ 引入了 configAPPLICATION_PROVIDES_cOutputBuffer，允许 FreeRTOS+CLI
  用户将输出缓冲区置于固定的内存地址。

+ 改进了为
  FreeRTOS+UDP 的 Windows 移植提供的 NetworkInterface.c 文件。


### 从 V8.2.0 到 2015 年 3 月 24 日发布的 V8.2.1 的变更。

RTOS 内核更新：

+ 增加了用户可定义的灵活线程本地存储设备。

+ 增加了 vTimerSetTimerID() API 函数，
  作为 pvTimerGetTimerID() 函数的补充，允许将定时器的 ID 用作定时器本地存储。

+ 修复了一个与使用 ISR 的队列集有关的潜在问题。

+ 对 Xilinx Microblaze GCC 移植进行了一些更新。

+ 为 Texas Instruments Code Composer Studio 增加了 ARM Cortex-M4F 移植。

+ 为 IAR、GCC 和 Keil 增加了 ARM Cortex-M7 r0p1 移植层，
  其中包含一个小的勘误表修正。  所有其他 ARM Cortex-M7 内核版本都应
  使用 ARM Cortex-M4F 移植。

+ 如果 configUSE_CO_ROUTINES 设置为 0，则排除整个 croutine.c。

+ 将部分数据类型从 uint32_t 改为 size_t，
  为 64 位 Windows 移植做准备。

+ 更新了 PIC32 移植，删除了最新 XC32 编译器
  输出的弃用警告。

+ 修复了 ISR 中的 xQueueOverwrite() 和 xQueueOverwrite()
  用于覆盖属于同一集合的两个队列中的项目时出现的错误。

 演示应用程序更新：

+ 使用
  IAR、Keil 和 CCS 编译器为TI 的基于 ARM Cortex-M4F 的 MSP432 微控制器增加了演示应用程序。

+ 增加了针对
  基于 STM32F ARM Cortex-M7，使用 IAR 和 Keil 的微控制器的演示应用程序。

+ 增加了针对基于 Atmel SAMV71 ARM Cortex-M7，
  使用 IAR 和 Keil 的微控制器的演示应用程序。

+ 增加了使用 2014.4 版 Xilinx SDK
  并在 KC705 评估板（Kintex FPGA）上运行的 Microblaze 演示。


### 从 V8.1.2 到 2015 年 1 月 16 日发布的 V8.2.0 的变更

候选版本 1 和正式版本的变更
仅限于维护。

重大 RTOS 内核更新：

+ 主要新功能！  任务通知。  详细信息请参阅以下链接：
  https://www.FreeRTOS.org/RTOS-task-notifications.html

+ 需要新的头文件！  已将过时的定义分离到名为
  FreeRTOS/Source/include/deprecated_definitions.h 的新头文件中。
  必须有该头文件才能进行构建。  请注意，
  一些过时的定义仍被非常老的演示应用项目所使用。

其他 RTOS 内核更新：

+ 使 xSemaphoreGiveFromISR() 成为一个函数，
  而不是一个调用 xQueueGenericSendFromISR() 的宏。  如果在同一个应用程序中同时使用这两个函数，
  则可以大大提高性能，
  但需要增加一些代码量。  注意：  在大多数情况下，
  现在可以用更小更快的任务通知
  来替代信号量。

+ 现在 TCB 的分配总是使任务的堆栈远离
  TCB（改善了堆栈溢出的调试，
  因为溢出不会覆盖任务名称）。

+ GCC、IAR 和 Keil Cortex-M4F 移植现在使用更多内联
  （以增加代码空间为代价提高性能）。

+ 现在队列将通过一次调用 pvPortMalloc() 进行分配，
  该函数一次性分配队列结构体和队列存储区域。

+ 为读取滴答计数引入了一个新的临界区宏，
  在滴答宽度允许以原子方式读取滴答计数的情况下，
  该宏定义为空值（性能优势——
  尤其是在开启优化时）。

+ 在 heap_4.c 中引入了 configAPPLICATION_ALLOCATED_HEAP，
  允许应用程序写入器提供自己的堆数组，
  从而控制堆的位置。

+ 引入了 configUSE_LIST_DATA_INTEGRITY_CHECK_BYTES，
  设置后将在列表和列表项结构体中包含已知值。  这些值
  旨在协助调试。  如果数值被覆盖，
  那么很可能是应用程序代码写入了内核使用的 RAM。

+ 所有 Cortex-M 移植中的 configASSERT()s 用于测试中断控制寄存器的最低 5 位，
  以检测 taskENTER_CRITICAL()
  是否被中断调用。  已改为测试所有 8 位。

+ 引入了 uxTaskPriorityGetFromISR()。

+ Microblze V8 移植现在测试 XPAR_MICROBLAZE_0_USE_FPU 是否不等于 0，
  而不是等于 1、2 和 3 也是有效值。

+ Cortex-A5 无 GIC 移植不再向中断处理程序
  传递中断外设的地址。

+ 修复了 FreeRTOS-MPU 中的一个问题，
  即在删除任务时，即使堆栈是静态分配的，
  也会尝试释放属于该任务的堆栈。

+ 将任务统计信息格式化为人类可读表格的实用（辅助）函数，
  现在会在任务名称前加上空格，
  以确保即使在任务名称长度差异很大的情况下，列也能正确排列。

+ 将 FreeRTOS+Trace 记录器库更新至 2.7.0 版。

 演示应用程序更新：

+ 增加了两个标准演示任务集：  IntSemTest 和 TaskNotify。

+ 为 Atmel SAMA5D4 Cortex-A5 MPU 增加了移植和演示应用程序。

+ 为 Altera Cyclone V Cortex-A9 MPU 增加了演示应用程序。

+ 更新了 Zynq 演示，以使用 Xilinx 的 SDK 2014.4 版，
  并增加了 RTOS 新功能的演示任务。

+ 更新了 Atmel SAM4E 和 SAM4S 演示，
  增加了大量测试和演示任务。

+ 修复了 Atmel SAM4L 低功耗无滴答实现中的一个拐角问题，
  并增加了按钮中断处理功能。

+ 提高了中断队列测试对 CPU 负载的耐受性。

+ 更新了 MSVC FreeRTOS 模拟器演示，
  以包含最新的标准测试和演示任务。

+ 更新了 MingW/Eclipse FreeRTOS 模拟器演示，以与 FreeRTOS MSVC
  模拟器演示相匹配。

+ 更新了所有使用 FreeRTOS+Trace 的演示，
  使其能使用最新的跟踪记录器代码。


### 从 V8.1.1 到 2014 年 9 月 2 日发布的 V8.1.2 的变更

必要时将 configUSE_PORT_OPTIMISED_TASK_SELECTION 的默认设置
移到各个移植层，
这样就不会影响不支持该定义的移植。


### 从 V8.1.0 到 2014 年 8 月 29 日发布的 V8.1.1 的变更

应广大用户的要求——为 V8.1.0 增加了一个小补丁，
以重新启用从中断处理程序提供互斥型信号量（具有优先级继承）
的功能。


### 从 V8.0.1 到 2014 年 8 月 26 日发布的 V8.1.0 的变更

FreeRTOS 调度器、内核、演示和测试更新：

+ 改进了优先权继承算法，
  以协助与可能同时持有多个互斥锁的现成中间件集成。

+ 引入了 heap_5.c，它与 heap_4.c 类似，
  但允许堆跨越多个非连续内存区域。

+ 更新了所有 Cortex-A9 移植，以帮助捕获几个常见的使用错误——
  第一个出现在当任务错误地尝试退出其执行函数时，
  第二个出现在当从中断调用非中断安全 API 函数时
  。

+ 更新了所有 Cortex-A9 移植，
  以在恢复任务上下文之前移除过时的模式开关。

+ configUSE_PORT_OPTIMISED_TASK_SELECTION 现在默认为 1，而不是 0。

+ 更新了所有 Cortex-M3/4F 移植，
  以捕获从中断处理程序调用的非中断安全 API 函数。

+ 简化了 heap_4.c 中的对齐检查。

+ 更新了 MSVC Windows 模拟器演示，
  使用 heap_5.c 代替 heap_4.c，以确保终端用户有一个可参考的示例。

+ 更新了标准演示测试代码，
  以测试新的优先级继承算法。

+ 更新了标准演示任务，以使用 stdint 和 FreeRTOS
  专用 typedef（在 FreeRTOS V8.0.0 中引入）。

+ 引入了 pdMS_TO_TICKS()宏，
  作为 pdTICKS_PER_MS 的更友好、更直观的替代——
  两者都可用于将以毫秒为单位的时间转换为以 RTOS 滴答为单位的时间。

+ 修复了任务编译器的 Cortex-M 移植中的一个错误，
  该错误会导致向 basepri 寄存器写入不正确的值。  这只会对
  Tasking 编译器的用户产生影响。

+ 更新了 Zynq 演示以使用 2014.2 版 SDK，
  并增加了一个 lwIP 示例，
  演示如何使用 lwIP 的原始接口和套接字接口。

+ 更新了 CCS Cortex-R4 移植，
  使其能够使用最新的 CCS 编译器构建。

新移植和演示应用程序：

+ 引入了两个 Renesas RX64M 移植（RXv2 内核）和演示，
  一个用于 GCC 编译器，另一个用于 Renesas 编译器。  两个演示都使用 e2 studio。

+ 引入了通用 IAR Cortex-A5 移植（无需依赖 GIC）。
  在一块 Atmel SAMA5D3 XPlained 电路板上对新移植进行了演示。

FreeRTOS+ 组件更新：

+ 将 CyaSSL 更新至最新版本。

+ 更新了由 Real Time Engineers Ltd. 直接提供的 FreeRTOS+ 组件，
  以使用 stdint 和 FreeRTOS 专用 typedef
  （在 FreeRTOS V8.0.0 中引入）。

+ 重新设计并简化了 FreeRTOS+FAT SL RAM 磁盘驱动程序。

其他更新和维护：

+ 更新了 IAR 和 DS-5/ARM RZ 演示以针对官方 RZ RSK 硬件，
  替换之前针对 Renesas 内部
  （非公开）硬件的演示。

+ 其他各种维护任务。


### 从 V8.0.0 到 2014 年 5 月 2 日发布的 V8.0.1 的变更

+ 对 V8.0.0 中发布的事件组功能进行了小修小补。
  现在，“从 ISR 清除位”功能
  是通过延迟中断回调而不是通过函数来实现的，而且“等待位”和
  “任务同步”函数在通过各自函数的每种可能路径返回值之前，
  都会正确清除内部控制位。

+ 确保任务删除或挂起后，
  内部控制数据的更新受到临界区的保护。

+ 对 FreeRTOS+FAT SL 进行了一些小修小补——
  即当偏移量不是扇区大小的倍数时，在文件末尾之外进行搜寻。

+ 确保 Cortex-A9 系统寄存器只能作为 32 位值访问，
  即使只实现了寄存器的最末有效字节。

其他更新：

+ 更新了 XMC4200 IAR 项目，以便与 7.x 版 IAR
  工具链接。

+ 增加了 RL78L1C 演示。

+ 增加了 pcTimerGetName() API 函数。

+ 如果定义了 configUSE_NEWLIB_REENTRANT，
  则在删除任务时调用 _reclaim_reent()。


### 从 V7.6.0 到 2014 年 2 月 19 日发布的 V8.0.0 的变更

https://www.FreeRTOS.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/02-Upgrade-guidance/01-upgrading-to-FreeRTOS-V8

FreeRTOS V8.x.x 是 FreeRTOS V7.x.x 的直接兼容替代品，
尽管如果更改用于引用字符串的类型，可能会在升级后导致应用程序
代码生成一些易于清除的编译器警告，
而且更新后的 typedef 命名规范
表明目前不推荐使用旧的 typedef。
请参阅 https://www.FreeRTOS.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/02-Upgrade-guidance/01-upgrading-to-FreeRTOS-V8/ 了解完整
信息。

新功能和新特性：

+ 事件组——请参阅 https://www.FreeRTOS.org/FreeRTOS-Event-Groups.html

+ 集中延迟中断处理——请参阅
  https://www.FreeRTOS.org/xTimerPendFunctionCallFromISR.html

其他更新：

+ 以前，当任务离开“阻塞”状态时，
  如果未受阻任务的优先级大于或等于“运行”任务的优先级，
  就会执行上下文切换。  现在，
  只有当未受阻任务的优先级大于“运行”任务的优先级时，
  才会执行上下文切换。

+ 针对 ST STM32L 微控制器的
  新型低功耗无滴答演示项目——请参阅
  https://www.FreeRTOS.org/STM32L-discovery-low-power-tickless-RTOS-demo.html

+ 在 heap_4.c 中增加了 xPortGetMinimumEverFreeHeapSize()。

+ 对 SAM4L 上的无滴答低功耗实现进行了小改动，
  以确保
  在无滴答期间
  因 RTOS 滴答以外的源中断而退出时，警报值（比较匹配值）不会被设置为零。

+ 更新了 GCC/Eclipse Win32 模拟器演示，
  以便更好地利用 Eclipse 资源过滤器，并与 MSVC 的相应功能相匹配。

+ xTaskIsTaskSuspended() 不再是公共函数。  使用
  eTaskGetState() 代替它。

+ 改进了跟踪宏，包括跟踪堆的使用情况。

+ 在 PIC32MZ 上接受中断时取消一级间接。

+ 增加了 Cortex-A9 GCC 移植层。

+ 增加了 Xilinx Zynq 演示应用程序。


### 从 V7.5.3 到 2013 年 11 月 18 日发布的 V7.6.0 的变更

V7.6.0 更改了使用合作式调度器时的某些行为
（当 configUSE_PREEMPTION 设置为 0 时）。  需要注意的是，
抢占式调度器的行为不会改变，
以下描述仅适用于 configUSE_PREEMPTION 设置为 0 的情况：

当 configUSE_PREEMPTION 设置为 0 时（在少数情况下），
上下文切换现在只会在任务进入阻塞状态
或显式调用 taskYIELD() 时发生。  这与以前的版本不同，
以前的版本在将优先级较高的任务隐式移出阻塞状态时
也会发生上下文切换。  例如，
以前，当抢占被关闭时，
如果任务 A 通过向队列中写入内容来解除任务 B 的阻塞，
那么调度器就会切换到优先级更高的任务。  现在，当抢占关闭时，
如果任务 A 通过向队列写入内容来解除对任务 B 的阻塞，
那么任务 B 将不会开始运行，直到任务 A 进入阻塞状态或任务 A 调用 taskYIELD() 为止。  [如果 configUSE\\_PREEMPTION 未设置为 0，
因此使用的是正常的抢占式调度器，
那么任务 B 将在脱离阻塞状态后立即开始运行]。

其他变更：

+ 为新的 PIC32MZ 架构增加了一个移植层和一个演示项目。

+ 更新了 PIC32MX 移植层，重新引入以前删除的一些 ehb 指令，
  增加了捕获中断堆栈溢出的功能
  （以前只能捕获任务堆栈溢出），
  还增加了捕获错误地试图从实现函数
  返回的应用任务的功能。

+ 大幅提高了 Win32 模拟器移植层的性能
  。

+ 确保被无限期阻止的任务将其状态报告为“阻塞”
  而不是“挂起”。

+ 对 Cortex-M4F 移植层进行了细微改进，
  以前一个寄存器会无意中被保存两次。

+ 引入了 xSemaphoreCreateBinary() API 函数，
  确保创建的每种信号量类型的语义一致。  不再
  建议使用 vSemaphoreCreateBinary()（前缀为“v”的版本），
  但为了向后兼容，代码中仍将保留该版本。

+ 更新了 Cortex-M0 移植层，
  允许在不使用 SVC 处理程序的情况下启动调度器。

+ 为针对 PIC32 USB II 入门套件的 PIC32MX MPLAB X 演示项目
  增加了构建配置。  以前，所有的构建配置
  都需要 Explorer 16 硬件。

+ 对一些标准演示任务进行了更新，
  以确保它们在更新的合作调度行为下正确执行。

+ 增加了 Atmel SAM4E 的综合演示，
  包括 FreeRTOS+UDP、FreeRTOS+FAT SL 和 FreeRTOS+CLI 的使用。

FreeRTOS+ 更改：

+ 对 FreeRTOS+UDP 进行小规模维护。


### 从 V7.5.2 到 2013 年 10 月 14 日发布的 V7.5.3 的变更

内核更改：

+ 在 V7.5.x 之前，从滴答钩子请求的让位
  会在同一个滴答中断中发生——恢复到原来的行为。

+ 新的 API 函数 uxQueueSpacesAvailable()。

+ 引入了 prvTaskExitError() function to Cortex-M0、Cortex-M3/4 
  和 Cortex-M4F 移植。  prvTaskExitError() 用于捕获
  试图从其实现函数返回的任务（任务如果要退出，
  应调用 vTaskDelete( NULL )）。

+ Cortex-M0 版本的 portSET_INTERRUPT_MASK_FROM_ISR 和
  portCLEAR_INTERRUPT_MASK_FROM_ISR 现在可以完全嵌套。

+ 改进了默认 Cortex-M 无滴答空闲行为的性能和稳健性
  。

+ 为所有 Cortex-M4F 移植增加了 Infineon XMC4000 设备中硅勘误表 PMU_CM001
  的解决方法。

+ 为 Keil 增加了 Keil 移植。

+ 更新了 Cortus 移植。

+ 确保 _impure_ptr 在调度器启动前初始化。
  以前，只有在第一次上下文切换时才会设置。

FreeRTOS+ 更改：

+ 将 FreeRTOS+UDP 更新至 V1.0.1——
  包括 FreeRTOS+Nabto 任务的直接集成、DHCP 行为的改进以及对测试的修正
  （该测试可防止在第一次网络瘫痪事件中
  调用网络事件钩子）。  FreeRTOS+UDP 变更历史
  单独保存。

+ 更正了 NXP CMSIS 库中提供的 LPC18xx.h 头文件中的 __NVIC_PRIO_BITS 设置，
  然后相应更新
  LPC18xx 演示使用的中断。

+ 将 FreeRTOS+CLI 帮助字符串中的双引号（"）替换为单引号（'），
  以确保字符串可与
  FreeRTOS+Nabto 演示中使用的 JSON 描述一起使用。

演示和杂项更改：

+ 为 Atmel SAMD20 Cortex-M0+ 增加了演示。  该演示包含
  FreeRTOS+CLI

+ 为可用 IAR
  Keil 和 GCC 工具构建的 Infineon Cortex-M0 增加了演示。

+ 更新了针对 IAR、Keil、GCC 和 Tasking 工具的 Infineon XMC4000 演示，
  除了之前支持的 XMC4500 外，还增加了构建配置，
  以直接支持 XMC4200 和 XMC4400 设备。

+ 更新了演示应用程序。

+ 增加了跟踪宏 traceMALLOC 和 traceFREE，
  以跟踪堆的使用情况。


### 从 V7.5.0 到 2013 年 7 月 24 日发布的 V7.5.2 的变更

V7.5.2 使新的 Cortex-M vPortCheckInterruptPriority() 函数
与 STM32 标准外设驱动程序库兼容，
并在默认低功耗无滴答模式实现中
增加了一个额外的临界区。  只有使用 STM32 外设库
或默认无滴答实现的用户才需要从 7.5.0 版本升级。


### 从 V7.4.2 到 2013 年 7 月 19 日发布的 V7.5.0 的变更

V7.5.0 是一次重大升级，包括多项调度和效率改进，
以及一些新的 API 函数。

FreeRTOS 用户的兼容性信息：
FreeRTOS V7.5.0 可向后兼容 FreeRTOS V7.4.0 ，
但有一个例外；vTaskList() 和 vTaskGetRunTimeStats() 函数现在被视为传统函数，
已被单一的 uxTaskGetSystemState() 函数取代
。  configUSE_STATS_FORMATTING_FUNCTIONS 必须
在 FreeRTOSConfig.h 中设为 1，才能使用 vTaskList() 和 vTaskGetRunTimeStats()
。

FreeRTOS 移植写入器的兼容性信息：
vTaskIncrementTick() 现在称为 xTaskIncrementTick()
（因为它现在返回一个值）。

主要更改：

+ 多种调度和效率改进。

+ 核心内核文件现在可以通过 PC-Lint V8 静态检查，
  不会输出任何警告（有关测试条件的信息将在后面提供）。

新的 API 函数：

+ uxTaskGetSystemState() https://www.FreeRTOS.org/uxTaskGetSystemState.html

+ xQueueOverwrite() https://www.FreeRTOS.org/xQueueOverwrite.html

+ xQueueOverwriteFromISR()

+ xQueuePeekFromISR()

以下是以前单独提供的移植和演示，
现在已并入主 FreeRTOS 压缩文件下载包中：

+ ARM Cortex-A9 IAR

+ ARM Cortex-A9 ARM 编译器

+ Renesas RZ

+ Microsemi SmartFusion2

新的 FreeRTOSConfig.h 设置
[link](/Documentation/02-Kernel/03-Supported-devices/02-Customization/)

+ configUSE_TIME_SLICING

+ configUSE_NEWLIB_REENTRANT

+ configUSE_STATS_FORMATTING_FUNCTIONS

+ configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS

其他变更：

+ (仅 MPU 移植）configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS
  选项提供了一种机制，允许应用程序写入器
  在特权模式下执行某些函数，
  即使任务是在用户模式下运行的。

+ 支持中断嵌套的移植现在包含一个 configASSERT()，
  如果从优先级高于最大系统/API 调用中断优先级的中断调用中断安全 FreeRTOS 函数，
  该函数就会触发
  。

+ 随附的 FreeRTOS+Trace 记录器代码已更新至最新版本，
  使用跟踪记录器代码的演示应用程序
  也已相应更新。

+ FreeRTOS Windows 模拟器（仅限 MSVC 版本）已更新，
  除原有的综合构建选项外，
  还增加了新的基本 “blinky” 构建选项。

+ 改进了 heap_4.c 和 heap_2.c 的 RAM 使用效率。

+ 防止 heap_4.c 试图释放未被 heap_4.c 分配
  或已被释放的内存块。

+ 由于 FreeRTOS 现在带有 FreeRTOS+FAT SL（由 HCC 捐赠），
  FreeRTOS/Demo/Common 中的 Chan FATfs 文件已被删除。

+ 修复在合作模式下构建 R4 移植时的错误。

+ 多种移植和演示应用程序维护活动。


### 从 V7.4.1 到 2013 年 5 月 1 日发布的 V7.4.2 的变更

注意：V7.4.1 和 V7.4.2 之间的 FreeRTOS 内核没有变化

+ 增加了 FreeRTOS+FAT SL 源代码和演示项目。  演示项目
  可在 FreeRTOS Windows 模拟器中运行，
  便于进行独立于硬件的实验和评估。  请参阅 https://www.FreeRTOS.org/fat_sl


### 从 V7.4.0 到 2013 年 4 月 18 日发布的 V7.4.1 的变更

+ 为确保严格遵守规范并与未来芯片兼容，
  在 Cortex-M 和 Cortex-R 移植层的 yield 宏中增加了
  数据和指令隔离指令。  为了提高效率，
  Cortex-M 移植层的 “yield” 和 ISR 的 “yield” 现在分开实现，
  因为在 ISR 情况下无需隔离指令。

+ 在主下载包中增加了 FreeRTOS+UDP。

+ 重新整理了 FreeRTOS+ 目录，使其与 FreeRTOS
  目录的源代码和演示子目录相匹配。

+ 在 FreeRTOS+UDP 中实现了 Berkeley 套接字 select() 函数。

+ 在调用标准库函数时，
  更改了（无符号）强制转换，改为使用（size_t）强制转换。

+ 增加了 Atmel SAM4L 和 Renesas RX100 演示，
  以演示无滴答（滴答抑制）低功耗 FreeRTOS 功能。

+ 增加了一个针对众多新 RL78 芯片和评估板的新 IAR RL78 演示
  。

+ 调整了 RX200 移植的堆栈对齐方式，
  以确保在定义 configASSERT() 时不会错误触发断言。

+ 更新了 Cortex_M4F_Infineon_XMC4500_IAR 演示，
  以便使用最新版本的 EWARM 构建。

+ 更正了 het.c 和 het.h 文件中的标头注释（RM48/TMS570 演示）。


### 从 V7.3.0 到 2013 年 2 月 20 日发布的 V7.4.0 的变更

+ 新功能：  队列集。  请参阅：
  https://www.FreeRTOS.org/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets

+ 全面修改了 ARM Cortex-M3 移植层
  提供的默认无滴答空闲模式实现。

+ 通过引入
   configEXPECTED_IDLE_TIME_BEFORE_SLEEP 宏
  和 eTaskConfirmSleepModeStatus() 函数，增强了核心内核代码中的无滴答支持。

+ 增加了 QueueSet.c 通用演示/测试文件。  更新了多个演示应用程序，
  以使用新的演示/测试任务。

+ 消除了 MPLAB PIC32 移植层和
  演示应用程序对 PLIB 库的依赖。

+ 为 MSVC Win32 演示 增加了 FreeRTOS+Trace 记录器代码。

+ 为保持一致，将 eTaskStateGet() 更名为 eTaskGetState()，
  并添加了一个预处理器宏，以便向后兼容之前的名称。

+ 更新了核心 queue.c 源文件中的函数，
  使 queue.h 可以直接包含在 .c 文件中
  （这避免了某些编译器产生的编译器警告）。

+ 更新了 CCS Cortex-R4 移植层，
  用最新版本的 CCS ARM 编译器提供的 CLZ 编译器固有函数
  替换 CLZ 汇编器函数。

+ 更新了所有 heap_x.c 实现，
  以更可移植的直接 C 代码实现
  取代用于确保堆的起点对齐的结构体。

+ 增加了对包含 EDS 的 PIC24 设备的支持。

+ 对 PIC32 移植层进行了小幅优化。

+ 对 tasks.c 稍作修改，
  使状态查看器插件能够显示更多信息。

+ 错误修复：  更新了 timers.c 中的 prvProcessReceivedCommands()，
  以消除在定时器守护进程任务的优先级设置
  低于使用定时器服务的任务的优先级时可能出现的问题。

+ 将 FreeRTOS+Trace 记录器代码更新为最新版本。


### 从 V7.2.0 到 2012 年 10 月 31 日发布的 V7.3.0 的变更

+ 增加了覆盖默认调度器任务选择机制的功能，
  可使用特定架构指令实现。

+ 增加了在空闲时间抑制滴答中断的功能，
  从而提供了
  利用特定架构低功耗功能的能力。

+ 增加了 portSUPPRESS_TICKS_AND_SLEEP() 宏和 vTaskStepTick() 辅助
  函数。

+ 增加了 configSYSTICK_CLOCK_HZ 配置常量。

+ 为 GCC、Keil 和 IAR 重构了 Cortex-M3 和 Cortex-M4F 移植层，
  以直接支持基本的省电功能。

+ 增加了钩子，
  允许在应用程序中利用芯片特定功能增强基本的省电功能。

+ 进行了一些小改动，
  允许在中断中使用互斥型信号量（互斥锁的正常使用模式并非如此）。

+ 更改 Cortex-M 移植中
  安全中断屏蔽保存和恢复宏的行为。  现在，
  保存宏会返回之前的掩码值。  现在，还原宏使用之前的掩码值。  这些
  改动对于内核本身的实现并无必要，
  纯粹是因为应用程序写入器正在使用这些宏。

+ 增加了 eTaskStateGet() API 函数。

+ 为 PIC32 移植层增加了特定于移植的优化功能，
  并更新了 PIC32 演示应用程序以使用这一新功能。

+ 为 Win32 模拟器移植增加了移植特定优化。

+ 为 TI Hercules RM48 和 TMS570 安全微控制器
  增加了新移植和演示应用程序。

+ 增加了针对 ATSAM3S-EK2 和 ATSAM3X-EK 评估板的 SAM3 演示
  。

+ 更新了 PIC32 MPLAB X 项目，
  以手动设置编译器包含路径，而不是使用 IDE 输入框，
  因为有报告称包含路径以某种方式被删除。

+ 改进了 FreeRTOS+CLI 中的字符处理。


### 从 V7.1.1 到 2012 年 8 月 14 日发布的 V7.2.0 的变更

FreeRTOS V7.2.0 向后兼容 FreeRTOS V7.1.2。

+ 增加了一个 FreeRTOS+ 子目录。  该目录包含一些 FreeRTOS+
  源代码和使用 FreeRTOS Win32 模拟器的示例项目。

+ 增加了一个新的堆分配实现示例 (heap_4.c)，
  其中包括内存块合并。

+ 增加了针对基于 Atmel SAM4S Cortex-M4 微控制器的演示。
  该演示经过预配置，可使用免费的 Atmel Studio 6 IDE 和
  GCC 编译器构建。

+ 增加了 xSemaphoreTakeFromISR() 实现。

+ ISR 安全 FreeRTOS 队列和信号量函数中的最后一个参数
  （xHigherPriorityTaskWoken）现在是可选参数，
  如果不需要，可设置为 NULL。

+ 更新了 IAR 和 MSP430X 移植，
  在退出滴答中断前清除所有低功耗模式位 [错误修正]。

+ 即使队列事件列表不为空，
  也允许使用 xQueueReset()。

+ 为 FreeRTOS MPU 移植增加了 vQueueDelete() 处理程序
  （之前缺少）。

+ 更新了 FreeRTOS MPU 移植层中的 vPortSVCHandler() 函数，
  以确保能与 Linaro 提供的最新 ARM GCC 编译器进行编译。

+ 更新了 NIOS II 移植中的 prvReadGP() 函数，
  以确保编译器可为函数参数选择任何寄存器
  （编译器优化级别较高时需要）。

+ 在 Keil 和 IAR Cortex-M 移植中增加了 #error 宏，
  以确保在用户将 configMAX_SYSCALL_INTERRUPT_PRIORITY
  设置为 0 时无法编译。

+ 在与 Cortex-M3 和 Cortex-M4 演示相关的 FreeRTOSConfig.h 文件中添加了注释，
  说明 configMAX_SYSCALL_INTERRUPT_PRIORITY 参数
  不得设置为 0。

+ 引入了新的 INCLUDE_xQueueGetMutexHolder 配置常量
  （默认为 0）。

+ 增加了两个新的列表处理宏——
  仅供即将推出的新产品内部使用。

+ 删除了所有提及传统 vTaskStartTrace 和 ulTaskEndTrace 宏的内容
  。  FreeRTOS+Trace 取代了传统跟踪。

+ 在 heap_1.c 中的 vPortFree() 函数中增加了 configASSERT()，
  因为调用该函数是无效的。

+ 使队列结构体中的 xRxLock 和 xTxLock 成员具有易失性。
  这可能没有必要，
  只是作为一项预防措施。

+ 修改用于检查传入 xTaskCreate() 函数的优先级
  是否在有效范围内的 assert()，
  以便在 FreeRTOS MPU 移植中使用断言。

+ 软件定时器服务（守护进程）任务的创建方式
  可确保与 FreeRTOS MPU 兼容。


### 从 V7.1.0 到 2012 年 5 月 1 日发布的 V7.1.1 的变更

新移植：

以下是全新移植：
+ Cortex-M3 Tasking

以下移植已作为单独下载包提供了几个月，
但现在已包含在主 FreeRTOS 下载包中。

+ Cortex-M0 IAR

+ Cortex-M0 GCC

+ Cortex-M4F GCC（支持全浮点运算）


新演示：

以下是全新演示：

+ Renesas RX63N RDK（Renesas 编译器）

以下演示已作为单独下载包提供了几个月，
但现在已包含在主 FreeRTOS 下载包中。

+ NXP LPC1114 GCC/LPCXpresso

+ ST STM32F0518 IAR

+ Infineon XMC4500 GCC/Atollic

+ Infineon XMC4500 IAR

+ Infineon XMC4500 Keil

+ Infineon XMC4500 Tasking

内核杂项/维护：

+ 引入了 portSETUP_TCB() 宏，
  以消除 Windows 模拟器使用 traceTASK_CREATE() 宏的要求，
  使 FreeRTOS+Trace (https://www.FreeRTOS.org/trace) 可以使用跟踪宏。

+ 增加了一个新的跟踪宏 traceMOVE_TASK_TO_READY_STATE()，
  允许未来的 FreeRTOS+Trace 版本为用户提供更多信息。

+ 更新了 FreeRTOS MPU 移植，
  以适应 FreeRTOS V7.1.0 中引入的变更。

+ 引入了 xQueueReset() API 函数。

+ 引入了 xSemaphoreGetMutexHolder() API 函数。

+ 整理了各种移植实现，
  在适当的地方添加了静态关键词，并删除了过时的代码。

+ 对 RX600 移植的初始堆栈框架稍作修改，
  以便在基于 Eclipse 的 E2Studio IDE 中使用这些移植时不会混淆 GDB。

+ 修正了 Cortex-M4F 任务初始堆栈的对齐方式。

+ 在 MSP430 设备的每条 DINT 指令后添加了一个 NOP，
  以严格遵守 DINT 的使用说明。

+ 更改了 Win32 移植中线程删除的实现，
  以防止移植使用 traceTASK_DELETE() 跟踪宏——
  将此宏留给 FreeRTOS+Trace 使用。

+ 对 RX600 Renesas 编译器移植层做了一些良性改动，
  以确保代码可以编译为库，
  而不会被链接器删除重要代码。

+ 撤销了 V7.1.0 中对 uxTaskNumber 变量名的更改，
  因为它破坏了 IAR 插件。


演示杂项/维护：

+ 命令解释器现已正式发布为 FreeRTOS+CLI，
  并从 FreeRTOS 主下载包中移出，
  可从 FreeRTOS+ 生态系统网站 https://www.FreeRTOS.org/plus 获取。

+ 在标准演示任务列表中增加了 flash_timer.c/h。  它
  执行的功能与 flash.c 任务相同，
  但使用软件定时器代替任务。

+ 对 PIC32 演示进行了如下升级：  修改了新编译器版本所需的库函数调用方式，
  添加了 PIC32MX360、PIC32MX460 和 PIC32MX795
  配置的 MPLAB X 项目，
  添加了简单的 blinky 演示，更新了 FreeRTOSConfig.h 以包含更多参数，
  添加了钩子函数存根。

+ 更新了 MSP430X IAR 和 CCS 演示，
  以确保功率设置正确，适用于配置的 CPU 频率。

+ 更新了 Rowley CrossWorks 项目，
  以纠正更新工具链时引入的“……的多重定义”警告。

+ 更新了与使用 Eclipse 构建的项目相关的各种 FreeRTOSConfig.h 头文件，
  使其包含一个 #error 语句，
  通知用户在打开项目前
  需要执行 CreateProjectDirectoryStructure.bat 批处理文件。

+ 重命名了名称中包含 “CCS4” 的目录，去掉 “4”，
  改为 “CCS”。  这是因为该演示经过更新和测试后，
  也可在 Code Composer Studio 的后续版本中使用。

+ 将大量 uIP 演示中的 TCP/IP 周期性定时器频率
  从 500ms 更新为 50ms。


### 从 V7.0.2 到 2011 年 12 月 13 日发布的 V7.1.0 的变更

新移植：

+ Cortex-M4F IAR 移植。

+ Cortex-M4F Keil/RVDS 移植。

+ TriCore GCC 移植。

新演示：

+ 使用 Keil MDK 的 NXP LPC4350，并在 Hitex 开发板上进行了演示
  。

+ 使用 IAR Embedded Workbench for ARM 的 STM32F407，
  并在 IAR STM32F407ZG-SK 入门套件上进行了演示。

+ 使用 GCC 编译器的 Infineon TriCore TC1782，
  在 TriBoard TC1782 评估板上进行了演示。

+ 使用 Renesas 编译器和 HEW 的 Renesas RX630，
  并在 RX630 RSK（Renesas 入门套件）上进行了演示。

演示杂项/维护：

+ 删除了 K60/IAR Kinetis 演示中对 printf() 的所有调用，
  因此该项目可以独立运行，无需连接调试器。

+ 完成了命令解释器框架。  命令处理程序现在可以接收
  整个命令字符串，从而可以直接访问参数。
  提供了用于检查参数数量
  和返回参数子字符串的实用程序函数。

+ xTaskResumeFromISR() 中的错误
  （仅影响支持中断嵌套的移植）
  已在主版本中进行了修复。

+ 增加了 portALIGNMENT_ASSERT_pxCurrentTCB() 定义，
  允许特定移植
  在创建任务时跳过第二次堆栈对齐检查。  这是因为第二种检查不适合某些移植，
  包括新的 TriCore 移植，因为在这些移植中，
  被检查的指针实际上并不指向堆栈。

+ 增加了 portCLEAN_UP_TCB()宏，
  以便在删除任务时进行特定的移植清理——这也是 TriCore 移植的要求。

+ 其他各种小改动，
  以确保在越来越多的微控制器和工具链平台上进行无警告构建。  这包括
  对最近大量演示中发现的 vApplicationStackOverflowHook()
  定义原型的（良性）修正。

跟踪系统：

+ 传统的跟踪机制已被完全删除——
  自跟踪宏引入以来，该机制已过时多年。  配置常量
  configUSE_TRACE_FACILITY 现在可用于
  选择性地包含额外的队列和任务信息。  附加信息
  旨在使跟踪机制更加通用，
  并允许跟踪输出提供更多信息。  当 configUSE_TRACE_FACILITY 设置为
  1 时：

  - 队列结构体包括一个用于保存队列类型的成员，
    队列类型可以是基本队列、互斥锁、计数信号量、二进制信号量
    或递归互斥锁。

  - 队列结构体包括一个用于保存队列编号的附加成员
    。  跟踪工具可以为自己的目的
    设置和查询队列编号。  内核本身不使用队列编号。

  - TCB 结构体包括一个用于保存任务编号的附加附加成员
    。  跟踪工具可以为自己的目的
    设置和查询任务编号。  内核本身不使用任务编号。

+ 队列和所有类型的信号量
  现在会在创建时自动分配其类型。

+ 增加了两个跟踪宏——traceTASK_PRIORITY_INHERIT() 和
  traskTASK_PRIORITY_DISINHERIT()。

+ 更新了 traceQUEUE_CREATE_FAILED()宏，
  使其可接受一个参数，指示创建失败的队列、互斥锁或信号量的类型
  。

+ 调用 traceCREATE_MUTEX() 的位置
  已从调用 xQueueGenericSend() [同一函数内] 之后
  移至调用之前。  这可确保跟踪事件以正确的顺序发生。

+ 针对调用 vTaskPrioritySet() 时参数为空的情况，
  修正了传入 tracePRIORITY_SET() 的值。


### 从 V7.0.1 到 2011 年 9 月 20 日发布的 V7.0.2 的变更

新移植：

+ 官方 FreeRTOS Renesas RX200 移植和演示应用程序
  已并入主 FreeRTOS 压缩文件下载包中。

+ 官方 FreeRTOS Renesas RL78 移植和演示应用程序
  已并入主 FreeRTOS 压缩文件下载包中。

+ 官方 FreeRTOS Freescale Kinetis K60 塔演示应用程序
  已并入主 FreeRTOS 压缩文件下载包中。  其中包括
  一个嵌入式网络服务器示例。

+ 创建了一个新的 Microblaze V8 移植层，
  以取代旧的、现已废弃的移植层。  V8 移植支持 Microblaze IP 的 V8.x，
  包括异常、缓存和浮点运算单元。  还增加了一个新的
  Microblaze 演示，以展示新的 Microblaze V8
  移植层。  演示应用程序是使用 Xilinx EDK V13.1 创建的，
  其中包括一个使用 lwIP V1.4.0 的基本嵌入式网络服务器。

+ 官方 FreeRTOS Fujitsu FM3 MB9A310 演示应用程序
  已并入主 FreeRTOS 压缩文件下载包中。  为
  IAR 和 Keil 工具链提供了项目。


增加 API：

+ 增加了 xTaskGetIdleTaskHandle()。

+ 增加了 xTaskGetTimerDaemonTaskHandle()。

+ 增加了 pcTaskGetTaskName()。

+ 增加了 vSemaphoreDelete() 宏，
  使删除信号量时的操作一目了然。  在以前的版本中，必须使用 vQueueDelete()。

+ 已删除 vTaskCleanUpResources()。  它已经过时
  有一段时间了。

+ 引入了 portPOINTER_SIZE_TYPE，
  以防止在指针大小与堆栈类型大小不匹配时
  产生编译器警告。  这将用于（已经用于）新的移植，
  但在现有移植本身更新之前
  不会加装到现有移植上。

其他更新和新特性：

+ 核心文件已全部修改，
  以进一步加强编码标准。  这些都是风格上的变化，而不是功能上的变化。

+ 对所有 ARM7 移植层稍作修改，
  以防止在创建任务和定义 configASSERT() 时出现错误的 assert() 故障。

+ 所有 ARM IAR 项目均已更新，
  以便使用最新 V6.2.x 版本的 IAR Embedded Workbench for ARM 工具 (EWARM) 构建。  这有必要，
  因为 EWARM 使用 CMSIS 库的方式发生了变化。

+ PIC32 移植层已更新，为 C32 编译器 V2 做准备
  。

+ 旧的 Virtex-4 Microblaze 演示已被标记为过时。  请
  使用全新的 Spartan-6 移植和演示代替它。

+ 新的通用命令解释器骨架位于
  FreeRTOS/Demo/Common/Utils/CommandInterpreter.c 中。  这项工作仍在进行中，
  没有记录在案。  不过，它已经投入使用。  在已经使用该系统的项目完成后，
  将对其进行全面记录
  。

+ 其中包括几个新的标准演示。  首先，
  是名为 sp_flop.c 的 flop.c 版本。  它与 flop.c 类似，
  但是使用单精度浮点数代替双精度浮点数。  这样
  就可以在只有单精度浮点运算单元的处理器上测试移植，
  并在使用双倍运算时恢复使用模拟运算
  。  其次，还加入了 comtest_strings.c，
  以便在一次性传输整个字符串时测试 UART 驱动程序。  之前的
  comtest.c 只使用单字符传输和接收。

+ lwIP V1.4.0 现已包含在 FreeRTOS/Demo/Common 目录中，
  并被几个新的演示所使用。


### 从 V7.0.0 到 2011 年 5 月 13 日发布的 V7.0.1 的变更

+ 为 IAR 和 Keil 工具链增加了 Fujitsu FM3 演示应用程序
  。

+ 为所有 IAR、Keil 和 SoftConsole (GCC/Eclipse) 工具链
  增加了 SmartFusion 演示应用程序。

+ 更新了 RX600 移植和演示应用程序，
  以考虑到使用最新（V1.0.2.0）版本
  Renesas 编译器时所需的不同语义。

+ 对 RX600 以太网驱动程序稍作修改，
  使其在大负荷下更加稳定，并更新了 uIP 处理任务，以便使用 FreeRTOS
  软件定时器。

+ 对 PIC32 移植层稍作修改，
  使 ehb 指令与 MIPS 内核手册的建议保持一致，
  并确保真正始终实现 8 字节堆栈对齐。

+ 更改了任务在调度器启动前
  挂起时的行为。  以前，至少需要有一个任务
  不处于挂起状态。  现在情况已不再如此。


### 从 V6.1.1 到 2011 年 4 月 8 日发布的 V7.0.0 的变更

FreeRTOS V7.0.0 向后兼容 FreeRTOS V6.x.x

主要变更：

+ 引入了一个新的软件定时器实现。

+ 引入了一个新的通用演示应用程序文件，
  用于练习新的定时器实现。

+ 更新了 Win32/MSVC 模拟器项目，
  加入了新的软件定时器演示任务和软件定时器滴答钩子测试。  两个新移植
  （使用 CCS4 的 MSP430X 和使用 TrueStudio 的 STM32）
  的演示项目中都包含了简单得多的软件定时器演示。

+ 对 tasks.c 中的内核实现进行了各种改进。  这些对用户是透明的，
  不会影响原有的 API。

+ 在内核代码中添加了对 configASSERT() 的调用。  configASSERT()
  在功能上等同于标准的 C assert() 宏，
  但不依赖于编译器提供的 assert.h。

其他变更：

+ 更新了 MSP430X IAR 移植和演示项目，
  使其支持中等内存模型。

+ 增加了针对 MSP430X Discovery 板并
  使用 Code Composer Studio 4 工具的 MSP430X 演示项目。  该演示包括
  新软件定时器的使用。

+ 增加了一个针对 STM32 Discovery Board 的 STM32F100RB 演示项目，
  使用 Atollic 的基于 TrueStudio Eclipse 的 IDE。

+ 删除了 PSoC 演示应用程序中的一些编译器警告。

+ 更新了 PIC32 移植层，
  以确保 configMAX_SYSCALL_INTERRUPT_PRIORITY 常量无论取值多少
  （在微控制器内核设定的有效范围内）
  都能按预期工作。

+ 更新了 PIC24、dsPIC 和 PIC32 项目，
  使它们能与 Microchip. 的最新 MPLAB 编译器版本兼容。

+ 进行各种外观修改，
  为软件发布后的标准符合性声明做准备。


### 从 V6.1.0 到 2011 年 1 月 14 日发布的 V6.1.1 的变更

+ 增加了两个新的 Windows 模拟器移植。  一个使用免费的 Microsoft Visual Studio 2010 快速版，
  另一个使用免费的 MingW/Eclipse
  环境。  为两者提供了演示项目。

+ 为 PSoC 5 (CYAC5588) 增加了三个演示项目。  这些演示适用于
  GCC、Keil 和 RVDS 构建工具，均使用 PSoC Creator IDE。

+ 增加了针对使用 IAR
  Embedded Workbench 的低功耗 STM32L152 微控制器的演示。

+ 增加了针对使用 IAR Embedded Workbench 的 MSP430X 核心的新移植。

+ 更新了所有针对 Renesas 演示的 RX62N 演示项目
  该工具包（RDK）考虑到了以后硬件版本上受推崇的 LED 接线，
  以及新的 J-Link 调试接口 DLL。

+ 更新了所有 RX62N 演示项目，
  使嵌入式网络服务器示例提供的 IO 页面能在所有网络浏览器上运行。

+ 更新了 Red Suite 项目，
  以便与即将发布的 Red Suite 版本配合使用，并使用最新版本的 CMSIS 库。

+ 增加了 traceTAKE_MUTEX_RECURSIVE_FAILED() 跟踪宏。

+ 删除了 traceTASK_CREATE_FAILED()
  跟踪宏中的参数（毫无意义）。

+ 引入了 portALT_GET_RUN_TIME_COUNTER_VALUE() 宏，
  以补充已有的 portGET_RUN_TIME_COUNTER_VALUE()。  这使得
  运行时间统计功能的时间基准
  可以更灵活地实现。

+ 在用于启动每个 Cortex M3 移植调度器的 “svc 0 ”
  指令之前添加了 “cpsie i” 指令。  这是为了确保
  在 C 启动代码禁用中断的情况下，
  在执行 “svc 0” 指令之前
  全局启用中断。

+ 运行时间统计计算略有优化。


### 从 V6.0.5 到 2010 年 10 月 6 日发布的 V6.1.0 的变更

+ 增加了 xTaskGetTickCountFromISR() 函数。

+ 修改了 vTaskSuspend()，
  即使内核尚未启动，也能立即挂起刚刚创建的任务。  这样，
  它们就能有效地在挂起状态下启动，
  而这一功能曾多次被要求用于协助初始化
  程序。

+ 增加了针对使用 IAR、GCC 和 Renesas 工具套件的 Renesas RX62N 的移植。

+ 增加了一个使用 Rowley 工具的 STM32F103 演示应用程序。

+ 在特定条件下，heap_2.c 中的 xFreeBytesRemaining
  可能会出现错误值。  已修复该错误。

+ xTaskCreateGeneric() 有一个参数，
  可用于将刚刚创建的任务句柄传递给调用任务。  该参数的赋值已被移动，
  以确保在新创建的程序有可能执行之前
  对其进行赋值。  这考虑到了为全局变量赋值的情况，
  新创建的任务会访问该全局变量
  。

+ 修复了各种 FreeTCPIP（基于 uIP）
  文件中的一些构建时编译器警告。

+ 修复了 Demo/Common/Minimal/IntQueue.c 中的一些构建时编译器警告。


### 从 V6.0.4 到 2010 年 5 月 17 日发布的 V6.0.5 的变更

+ 为 Cortus APS3 处理器增加了移植和演示应用程序。


### 从 V6.0.3 到 2010 年 3 月 14 日发布的 V6.0.4 的变更

+ 已删除 Demo/Unsupported_Demos
  目录中的所有贡献文件。  这些文件
  现在可在  FreeRTOS 网站新的“社区贡献”部分查阅。  请参阅
  https://www.FreeRTOS.org/RTOS-contributed-ports.html

+ Demo/CORTEX_STM32F107_GCC_Rowley 目录
  中的项目文件已升级至使用 Rowley Crossworks STM32 支持包的 V2.x
  。

+ 其中包括一个初始 Energy Micro EFM32 演示。  未来几个月内将对其进行更新，
  以便更好地利用 EFM32 提供的低功耗模式
  。


### 从 V6.0.2 到 2010 年 2 月 26 日发布的 V6.0.3 的变更

+ 增加了 SuperH SH7216 (SH2A-FPU) 移植和演示应用程序。

+ 对 pvPortMallocAligned()
  和 vPortFreeAligned() 宏的默认实现稍作修改，
  默认情况下它们只调用 pvPortMalloc() 和 vPortFree()。  只有在
  使用内存保护单元 (MPU) 时，
  才需要定义宏，而且只能根据其他配置设置来定义。


### 从 V6.0.1 到 2010 年 1 月 9 日发布的 V6.0.2 的变更

+ 更改了所有 GCC ARM 7 移植以将 0 用作 SWI 指令参数。
  以前该参数是空白的，因此只能隐含 0，
  但较新的 GCC 版本不允许这样做。

+ 更新了 IAR SAM7S 和 SAM7X 移植，以便与 IAR V5.40 兼容。

+ 将 PIC32 的堆栈对齐要求从 4 字节改为 8 字节。

+ 更新了 prvListTaskWithinSingleList()，
  使其能在堆栈从低内存增长的处理器上运行。

+ 修改了一些注释。

+ 更新了 RVDS LPC21xx 演示的启动文件。


### 从 V6.0.0 到 2009 年 11 月 15 日发布的 V6.0.1 的变更

+ 修改了所有 Cortex-M3 移植的 pxPortInitialiseStack()，
  以确保在任务首次开始执行时，
  堆栈指针位于编译器预期的位置。

以下小改动只对 Cortex-M3 MPU 移植产生影响：

+ portRESET_PRIVILEGE() 汇编宏已更新，以包含一个受影响列表。

+ 为所有特权函数包装器添加了原型，
  以确保无论警告级别设置如何，
  都不会产生编译时警告。

+ 将 portSVC_prvRaisePrivilege 的名称
  更正为 portSVC_RAISE_PRIVILEGE。

+ 在 xTaskGenericCreate() 中添加了条件编译，
  以防止某些编译器在 portPRIVILEGE_BIT 定义为零时发出警告。


### 从 V5.4.2 到 2009 年 10 月 16 日发布的 V6.0.0 的变更

FreeRTOS V6 向后兼容 FreeRTOS V5.x。

主要变更：

+ FreeRTOS V6 是第一个支持内存保护单元（MPU）的版本
  。  Cortex M3 目前有两种移植，一种是标准 FreeRTOS
  移植，不支持 MPU；另一种是 FreeRTOS-MPU 移植，提供相关支持 。

+ 增加了 xTaskCreateRestricted() and vTaskAllocateMPURegions() API 函数
  以支持 FreeRTOS-MPU。

+ 澄清了 GPL 例外的措辞（希望如此）。  此外，
  下载包中的 license.txt 文件也已修复
  （之前的版本包含一些损坏）。

其他变更：

+ 在 heap_1.c 和 heap_2.c 中新增了 API 函数 xPortGetFreeHeapSize()。

+ 修改了 ARM7 GCC 演示中断服务程序包装函数，
  以便使用 __asm 语句调用 C 部分。  这样可以防止函数
  调用在更高的优化级别下被内联。

+ ARM7 移植现在可以在设置任务的初始堆栈时
  根据需要自动设置 THUMB 位，
  而无需定义 THUMB_INTERWORK。  这也使得 THUMB 模式和 ARM 模式
  任务更容易混合使用。

+ 现在，所有 ARM7/9 移植的 portBYTE_ALIGNMENT 默认设置为 8。

+ 更新了各种演示应用程序项目文件，
  以便与最新的 IDE 版本保持一致。

+ 命令行 GCC 演示中使用的链接器脚本
  已更新为包含 eh_frame 区，
  以便与最新发布的 Yagarto 一起使用。  同样，演示的 makefile 也已更新，
  加入了命令行选项，
  以减少或完全取消 eh_frame 区。

+ portBYTE_ALIGNMENT_MASK 的定义
  已从各种内存分配文件中移出，
  转入普通的 portable.h 头文件中。

+ 删除了对 portLONG、portSHORT 和 portCHAR 的不必要使用。

+ 为 Rowley CrossWorks 增加了 LM3Sxxxx 演示。

+ Posix 模拟器已升级，请参阅
  FreeRTOS.org 网站上的相应 WEB 页面。


### 从 V5.4.1 到 2009 年 8 月 9 日发布的 V5.4.2 的变更

+ 为 Altera Nios2 软核增加了新的移植和演示应用程序。

+ 为 IAR 增加了 LPC1768 演示。

+ 在所有 LPC1768 演示（Code Red、CrossWorks 和 IAR）中增加了 USB CDC 演示。

+ 将 LPC1768 演示的时钟频率改为 99 MHz。


### 从 V5.4.0 到 2009 年 7 月 25 日发布的 V5.4.1 的变更

+ 增加了新的钩子函数。  如果 pvPortMalloc() 返回 NULL，
  则调用 vApplicationMallocFailedHook()（可选）。

+ 为 xTaskCheckForTimeOut() 增加了额外的转换功能。  这样可以避免
  在 32 位架构上将 configUSE_16_BIT_TICKS 设置为 1 时
  可能出现的问题（无论如何，这可能是个错误）。

+ 纠正了在两个 LPC1768 演示中
  为设置 MAC 中断优先级而传递给 NVIC_SetPriority() 的参数。

+ 降低了 PIC32 演示应用程序中
  configMINIMAL_STACK_SIZE 的默认设置，
  以确保在调度器启动之前堆空间不会被完全占用。


### 从 V5.3.1 到 2009 年 7 月 13 日发布的 V5.4.0 的变更

+ 增加了 Virtex5 / PPC440 移植和演示。

+ 用 LPC1768 Red Suite 演示取代了 LPC1766 Red Suite 演示。  最初的
  演示配置为使用 CPU 的工程样品。  新的
  演示改进了以太网驱动程序。

+ 增加了带有零拷贝以太网驱动程序的 LPC1768 Rowley 演示。

+ 重写了字节对齐代码，以确保 8 字节对齐正常工作。

+ 在 PPC405 演示项目中将 configUSE_16_BIT_TICKS 设置为 0。

+ 更改了 PPC405 的初始堆栈设置，
  以确保正确设置小数据区指针。


### 从 V5.3.0 到 2009 年 6 月 21 日发布的 V5.3.1 的变更

+ 增加了 ColdFire V1 MCF51CN128 移植和 WEB 服务器演示。

+ 增加了 STM32 Connectivity Line STM32107 Cortex M3 WEB 服务器演示。

+ 将 Cortex M3 port.c asm 语句改为 __asm，
  以便在默认配置下使用 Rowley CrossWorks V2 进行编译。

+ 更新了 Posix/Linux 模拟器贡献移植。


### 从 V5.2.0 到 2009 年 6 月 1 日发布的 V5.3.0 的变更

主要变更：

+ 增加了新功能（可选），
  可收集每个任务所用 CPU 时间的统计数据。

+ 为基于 Atmel AT91SAM3U Cortex-M3 的微控制器
  增加了一个新的演示应用程序。

+ 为基于 NXP LPC1766 Cortex-M3 的微控制器
  增加了一个新的演示应用程序。

+ 增加了一个贡献移植/演示，允许“模拟” FreeRTOS
  （在 Linux 环境中模拟）。

细微变更：
+ 更新了 Stellaris uIP WEB 服务器演示，
  以包括新的运行时间统计收集功能，
  并包括一个以表格形式显示信息的 WEB 服务器页面。

+ 为 Coldfire MCF52259 增加了 lwIP 移植层。

+ 更新了 CrossWorks LPC2368 WEB 服务器，
  以便在提供的内容中包含图片。

+ 更改了 LPC2368 MAC 初始化的部分时序，
  以便在所有部分修订版上使用。

+ 对 uIP 核心代码稍作修改，删除了一些编译器警告。

+ 增加了 xTaskGetApplicationTaskTag() 函数，
  并更新了 OpenWatcom 演示以使用新函数。

+ 增加了针对使用 Rowley Crossworks 的 AVR32 AP7000、STM32 Primer 2 和 STM32
  的贡献演示。

+ Heap_1.c 和 Heap_2.c 用于定义数据对齐结构体
  。  这些数据已转换为共用体，
  以节省几个字节的 RAM，否则会造成浪费。

+ 当最大任务名称长度配置为 1 字节时，
  移除用于将任务名称复制到 TCB 的 strncpy() 调用。


### 从 V5.1.2 到 2009 年 3 月 14 日发布的 V5.2.0 的变更

+ 优化了队列发送和接收函数（也用于信号量）。

+ 替换了用于保护 PC 移植 BIOS 调用的标准临界区，
  转而使用调度器锁。  这是因为 BIOS 调用
  总是在中断启用的情况下返回。

+ 更正了 boot.s 中未关闭的注释。


### 从 V5.1.1 到 2009 年 2 月 9 日发布的 V5.1.2 的变更

+ 增加了 NEC V850ES 移植和演示。

+ 增加了 NEC 78K0R 移植和演示。

+ 增加了 MCF52259 移植和演示。

+ 增加了 AT91SAM9XE 移植和演示。

+ 更新了 MCF52233 FEC 驱动程序，以解决一个硅错误，
  该错误导致部件无法自动协商某些网络参数。

+ 对 MCF52233 makefile 稍作修改，
  使其可用于 Linux 主机。

+ 更新了 STM32 入门文件，
  使其能够使用最新版本的 RIDE 工具构建。

+ 更新了用于在 Rowley CrossWorks IDE 中
  进行内核感知调试的 threads.js Java 脚本。


### 从 V5.1.0 到 2008 年 11 月 20 日发布的 V5.1.1 的变更

+ 增加了 Coldfire MCF52233 Web 服务器演示（使用 GCC 和 Eclipse）。

+ 增加了 IAR MSP430 移植和演示。

+ 修正了几个编译器时间问题，这些问题是随着工具版本的变化而出现的
  。

+ 包括 FreeRTOS-uIP——一个更快的 uIP。  目前尚未完成。


### 从 V5.0.4 到 2008 年 10 月 24 日发布的 V5.1.0 的变更

+ 增加了针对使用
  CodeWarrior 开发工具的 ColdFire V2 核心的移植和演示应用程序。

+ 使用新的 Keil/RVDS 组合替换了使用旧版（现已不再支持）
  Keil 编译器的 ARM7 演示。

+ 堆栈溢出检查现在适用于
  从低内存增长的堆栈（PIC24 和 dsPIC）。

+ 错误修正——将 portSTACK_GROWTH 的 PIC32 定义设置为正确的
   -1 值。

+ 对 MSP430 移植层进行了更新，
  允许任务将微控制器置于断电模式 1 至 3。  演示应用程序也已更新，
  以演示新功能。

+ 用更灵活的单一版本取代了两个独立的 MSP430/Rowley 移植层
  。

+ 增加了更多贡献移植，
  包括用于 NEC 和 SAM9 微控制器的移植。

+ 更改了 LPC2368 Eclipse 演示中使用的链接器脚本。


### 从 V5.0.3 到 2008 年 9 月 22 日发布的 V5.0.4 的变更

+ 完全为 ColdFire GCC 重新编写了移植。

+ 错误修复：  所有 Cortex M3 移植都
  对设置待处理中断的代码进行了细微修改。

+ 某些头文件要求在包含之前先包含 FreeRTOS.h
  。  在所有此类头文件中都添加了 #error 信息，
  如果头文件未按正确顺序包含，
  则会告知用户编译错误的原因。


### 从 V5.0.2 到 2008 年 7 月 31 日发布的 V5.0.3 的变更

与 Cortex M3 相关的变更：

+ 在所有 Cortex M3 移植和演示中
  增加了 configMAX_SYSCALL_INTERRUPT_PRIORITY 的用法。  请参阅 FreeRTOS.org
  WEB 网站上的移植文档页面了解完整使用信息。

+ 进一步提高了 Cortex M3 移植的效率。

+ 确保无论向量表位于何处，
  Cortex M3 移植都能正常工作。

+ 为每个 CM3 移植
  （Keil、GCC 和 IAR）的演示项目添加了 IntQTimer 演示/测试任务，
  以测试新的 configMAX_SYSCALL_INTERRUPT_PRIORITY 功能。

+ 在 LM3SXXXX IAR 和 Keil 项目中添加了 mainINCLUDE_WEB_SERVER 定义，
  允许在构建时有条件地排除 WEB 服务器，
  从而允许使用 KickStart（代码大小受限）
  编译器版本。

其他变更：

+ 将 vPortYield() 的 PIC24 和 dsPIC 版本从 C 文件移到汇编文件，
  以便与所有 MPLAB 编译器版本一起使用。  这样还可以
  关闭省略帧指针优化。


### 从 V5.0.0 到 2008 年 5 月 30 日发布的 V5.0.2 的变更

+ 更新了 PIC32 移植，
  允许从高于内核中断优先级的中断中使用队列 API 调用，
  并允许完全中断嵌套。  任务堆栈的使用量也有所减少。

+ 增加了一个新的 PowerPC 移植，
  演示如何使用跟踪宏来允许使用浮点协处理器。  traceTASK_SWITCHED_OUT()
  和 traceTASK_SWITCHED_INT() 宏分别用于
  保存和恢复实际使用浮点运算
  的任务的浮点上下文。

+ 错误修复：  第一个 PPC405 移植包含一个错误，
  即当任务首次开始执行时，
  堆栈上方没有留出足够的空间来保存后链。

+ 更新了 queue.c，添加了允许中断嵌套的方法，
  以及从优先级高于内核优先级的中断
  调用队列 API 函数的方法。  到目前为止，
  只有 PIC32 移植支持该功能。

+ 修复了使用最新版 WinAVR 时
  产生的编译器警告。

+ 删除了核心内核代码中所有“内联”的内联用法。

+ 增加了队列注册表功能。  队列注册表
  是内核感知调试器查找队列定义的一种手段。  除非使用内核感知调试器，
  否则它没有任何作用。  只有当 configQUEUE_REGISTRY_SIZE 大于零时，
  才会使用队列注册表。

+ 将 ST Cortex-M3 驱动程序添加到 Demo/Common/Drivers 目录中，
  以避免在多个演示中包含这些驱动程序。

+ 增加了一个 Keil STM32 演示应用程序。

+ 修改了 blocktim.c 测试文件，
  因为所有移植在临界区内调用队列 API 函数已不再合法。

+ 增加了 IntQueue.c 测试文件，
  以测试从不同中断优先级调用队列 API 函数，并测试中断嵌套。


### 从 V5.0.0 到 V5.0.1 的变更

+ V5.0.1 是客户定制版。


### 从 V4.8.0 到 2008 年 4 月 15 日发布的 V5.0.0 的变更

*** 关于升级到 FREERTOS.ORG V5.0.0 的重要信息 ***

函数 xQueueSendFromISR()、xQueueSendToFrontFromISR()、
xQueueSendToBackFromISR() 和 xSemaphoreGiveFromISR() 的参数已更改。  必须
更新对这些函数的所有调用，以使用新的调用约定！  编译器
可能不会发出任何类型不匹配警告！

其他变更：

+ 增加了对新型 Luminary Micro LM3S3768 和 LM3S3748 Cortex-M3
  微控制器的支持。

+ 增加了新的任务钩子功能。

+ PowerPC 演示已更新为使用 10.1 版 Xilinx EDK。

+ 提高了 PIC32 移植层的效率。


### 从 V4.7.2 到 2008 年 3 月 26 日发布的 V4.8.0 的变更

+ 增加了 Virtex4 PowerPC 405 移植和演示应用程序。

+ 增加了可选的堆栈溢出检查和新的
  uxTaskGetStackHighWaterMark() 函数。

+ 增加了 xQueueIsQueueEmptyFromISR()、xQueueIsQueueFullFromISR() 和
  uxQueueMessagesWaitingFromISR() API 函数。

+ 提高了 Cortex-M3 移植层的效率。  注意：
  这要求在应用程序中安装 SVC 处理程序。

+ 提高了队列发送和接收函数的效率。

+ 增加了新的跟踪宏。  这些宏可由应用程序定义，
  以提供灵活的跟踪功能。

+ 在 Keil Cortex M3 移植层中实现
  configKERNEL_INTERRUPT_PRIORITY（使其达到与 IAR 和 GCC
  版本相同的标准）。

+ 使用 arm-stellaris-eabi-gcc 工具的移植已转换为
  使用 arm-non-eabi-gcc 工具。


### 从 V4.7.1 到 2008 年 2 月 21 日发布的 V4.7.2 的变更

+ 增加了 Fujitsu MB91460 移植和演示。

+ 增加了 Fujitsu MB96340 移植和演示。

+ 整理了 include 文件的大写格式，
  以方便在 Linux 主机上构建。

+ 删除了一些会产生警告的多余转换，
  但加入这些转换是为了删除其他编译器上的警告。


### 从 V4.7.0 到 2008 年 2 月 3 日发布的 V4.7.1 的变更

+ 更新了所有 IAR ARM 项目，以使用 ARM IAR Embedded Workbench V5.11
  。

+ 引入递归信号量功能。

+ 更新了 LPC2368 演示，以考虑到旧版芯片中的硅缺陷
  。

+ 更新了 STR9 uIP 移植，以手动设置网络掩码和网关地址。

+ 更新了演示，使更多演示能与合作式调度器一起运行。

+ 修复了在调度器挂起时
  发生滴答中断时的合作式调度器行为。

+ 更新了 semphr.h 中的文档。

+ ARM7 GCC 移植不再使用 IRQ 属性。


### 从 V4.6.1 到 2007 年 12 月 6 日发布的 V4.7.0 的变更

+ 引入了计数信号量宏和演示源文件。  Open Watcom PC 项目已更新，
      以包含新的演示。  请参阅
      在线文档了解更多信息。

+ 引入了“替代”队列处理 API 和演示源文件。
  Open Watcom PC 项目已更新，以包含新的演示
  源文件。  请参阅在线文档了解更多信息。

+ 增加了 AT91SAM7X Eclipse 演示项目。

+ 为 GCC 编译器和 Ride IDE 增加了 STM32 入门演示项目。

+ 删除了 V4.6.1
  版 eclipse 工作区中错误包含的 .lock 文件。


### 从 V4.6.0 到 2007 年 11 月 5 日发布的 V4.6.1 的变更

+ 增加了对基于 MIPS M4K 的 PIC32 的支持。

+ 在所有头文件中增加了 “extern ”C"，以便与 C++ 一起使用。


### 从 V4.5.0 到 2007 年 10 月 28 日发布的 V4.6.0 的变更

+ 更改了仅用于 ARM7/9 GCC 移植的 ISR 中
  强制上下文切换的方法。  不再支持 portENTER_SWITCHING_ISR() 和
  portEXIT_SWITCHING_ISR() 宏。  这样做
  是为了确保无论使用哪个 GCC 版本，
  无论是否使用 -fomit-frame-pointer 选项，以及在所有优化级别下都能正确运行。

+ 更正了 queue.h 中 xQueueGenericSend() 的原型。


### 从 V4.4.0 到 2007 年 9 月 17 日发布的 V4.5.0 的变更

+ 增加了 xQueueSendToFront()、xQueueSendToBack() 和 xQueuePeek()
  函数。  现在应优先使用这些函数，
  而不是旧的 xQueueSend() 函数，后者是为了向后兼容而保留的。

+ 增加了互斥锁功能。  由于互斥锁自动包含优先级继承机制，
  因此其行为与现有的二进制信号量
  有着微妙的不同。

+ 增加了 GenQTest.c 和 QPeek.c，
  以测试和演示新函数的行为。

+ 更新了 LM3Sxxxx 和 PC 移植，
  以包含新的 GenQTest.c 和 QPeek.c 文件。

+ 更新了 Cortex M3 的 GCC 移植，
  加入了 configKERNEL_INTERRUPT_PRIORITY 函数。  这在以前
  只包括在 IAR 移植中。

+ 优化了 GCC 和 IAR 移植层代码，
  特别是上下文切换代码。

+ 将所有开发工具的 LM3Sxxxx EK 演示
  合并到一个项目中，
  该项目可自动检测应用程序在哪个版本的 EK 上执行。

+ 增加了对 LM3Sxxxx 评估套件的 Eclipse 支持。

+ 增加了对 Keil LPC2368 评估套件的 Eclipse 支持。

+ 增加了 Demo/Drivers 目录，
  用于保存多个演示应用程序项目通用的代码。

+ 修正了 uIP 1.0 代码中的一些小错误。

+ 增加了 STR9 的 lwIP 演示——感谢 ST 的协助。

+ 更新了 AVR32 移植，
  以确保在编译器完全优化的情况下行为正确。

+ 包含 OpenOCD FTDI 和并行移植接口的二进制文件。


### 从 V4.3.1 到 2007 年 7 月 31 日发布的 V4.4.0 的变更

+ 增加了 AVR32 UC3B 演示应用程序。

+ 更新了 AVR32 UC3A 移植和演示应用程序。

+ 增加了适用于 AVR32 UC3A 的 IAR lwIP 演示。

+ 更新了 listGET_OWNER_OF_NEXT_ENTRY()，以协助编译器优化
  （感谢 Niu Yong 的建议）。

+ 增加了 xTaskGetSchedulerState() API 函数。

+ 错误修复：  纠正了被无限期阻塞的任务的阻塞时间被调整时的行为
  （在 xQueueSend() 和 xQueueReceive() 中），
  并纠正了调用 vTaskResume() 时
  任务实际上并未处于挂起状态的行为
  （感谢 Dan Searles 报告了这些问题）。


### 从 V4.3.0 到 2007 年 6 月 11 日发布的 V4.3.1 的变更

+ 增加了 STMicroelectronics STM32 Cortex-M3 演示应用程序。

+ 更新了适用于 GCC LM3S6965 演示的 ustdlib.c。


### 从 V4.2.1 到 2007 年 6 月 5 日发布的 V4.3.0 的变更

+ 为 IAR Cortex-M3、PIC24 和 dsPIC 移植引入了 configKERNEL_INTERRUPT_PRIORITY
  。  请参阅 LM3S6965 和 PIC24 演示应用程序
  文档页面了解更多信息。

+ 更新了 PIC24 和 dsPIC 演示，以便使用 PIC30 GCC 工具的 V3.0 版构建，
  并更改了演示应用程序。

+ 增加了启用以太网和 CAN 的新型 Luminary Micro Stellaris 微控制器的演示
  。

+ 修正了 uIP 演示中的错误，该错误导致无法传输约 1480
  字节及以上的帧。

+ 将 LPC2368/uIP/Rowley 演示纳入 FreeRTOS.org
  主下载包中。

+ 更新到了 WizC PIC18 移植，使其可与第 14 版编译器一起使用
  。  感谢 Marcel！


### 从 V4.2.0 到 2007 年 4 月 2 日发布的 V4.2.1 的变更

+ 增加了适用于 GCC 和 IAR 的 AVR32 AT32UC3A 移植。

+ 为 lwIP SAM7X 演示生成文件增加了 -fomit-frame-pointer 选项。

+ 移动了 STR9 演示中调用 LCD_Init() 的位置，
  以确保仅在调度器启动后才调用。


### 从 V4.1.3 到 2007 年 2 月 8 日发布的 V4.2.0 的变更

+ 根据
  SafeRTOS 代码库的测试结果，对 task.c 和 queue.c 进行了修改。

+ 增加了适用于 GCC 和 IAR 工具的 Cortex-M3 LM3S811 演示。


### 从 V4.1.2 到 2006 年 11 月 19 日发布的 V4.1.3 的变更

+ 增加了 STR750 ARM7 移植（使用 Raisonance RIDE/GCC 工具）。

+ 为 Rowley ARM7 演示增加了 -fomit-frame-pointer 选项，
  以解决 GCC 在某些优化级别上的错误。

+ 修改了 LM3S811 Keil 演示中定义堆的方式，
  以防止 RAM 使用量计入代码大小限制计算。

+ 协程错误修复：  删除了 xQueueCRReceive 中对 prvIsQueueEmpty 的调用，
  因为它是在启用中断的情况下退出的。  感谢 Paul Katz。

+ 如果定义了 configINCLUDE_vTaskSuspend，
  在超时为 portMAX_DELAY 的事件上阻塞的任务现在会被无限期阻塞。
  以前，portMAX_DELAY 只是可能的最长阻塞时间。如果未定义 configINCLUDE_vTaskSuspend，
  情况仍然如此。

+ 对一些演示应用程序文件进行了小改动。


### 从 V4.1.1 到 2006 年 10 月 21 日发布的 V4.1.2 的变更

+ 增加了 16 位 PIC 移植和演示。

+ 增加了 STR750 移植和演示。


### 从 V4.1.0 到 2006 年 9 月 24 日发布的 V4.1.1 的变更

+ 增加了 Luminary Micro Stellaris LM3S811 演示应用程序。


### 从 V4.0.5 到 2006 年 8 月 28 日发布的 V4.1.0 的变更

+ 在 V4.1.0 之前，在某些有记录的情况下，
  xQueueSend() 和 xQueueReceive() 有可能
  在未完成且阻塞时间未结束的情况下返回。  阻塞时间有效
  规定了最长阻塞时间，而且需要检查函数的返回值，
  以确定返回的原因。  现在情况不再如此，
  因为只有在阻塞时间结束或函数能够完成运算后，
  函数才会返回。  因此，
  不再需要将调用包裹在循环中。

+ 修改了 IAR AVR 移植中的临界区处理，
  以纠正与较晚版本编译器一起使用时的行为。

+ 在压缩文件中增加了 LPC2138 CrossWorks 演示。  在此之前，
  这只能通过单独下载获得。

+ 修改了 AVR 演示应用程序，以展示协程的使用。


### 从 V4.0.4 到 2006 年 8 月 13 日发布的 V4.0.5 的变更

+ 引入了 API 函数 xTaskResumeFromISR()。  功能与 xTaskResume() 相同，
  但可在中断服务程序中调用。

+ 优化了 vListInsert()，
  以适应唤醒时间为最大滴答计数值的情况。

+ 错误修复：  当任务的优先级发生变化时，
  事件列表项的“值”也会随之更新。  在此之前，只有 TCB 本身的优先级会发生变化
  。

+ vTaskPrioritySet() 和 vTaskResume() 不再使用事件列表项。
  自 V4.0.1 版添加了 xMissedYield 处理后，
  就不再需要这样做了。

+ 将 ARM9 STR9 演示的 PCLK 设置从 96MHz 降至 48MHz。

+ 结束调度程序时——
  删除当前任务时不要尝试上下文切换。

+ SAM7X EMAC 驱动程序：  更正了从 rx 描述符
  获取长度时的 Rx 帧长度掩码。


### 从 V4.0.3 到 2006 年 6 月 22 日发布的 V4.0.4 的变更

+ 为 ST 的基于 ARM9 的 STR9 处理器增加了移植和演示应用程序
  。

+ 对 vTaskPrioritySet() 函数进行了小幅优化。

+ 在 demo/common/ethernet 目录中
  加入了最新的 uIP 版本（1.0）。


### 从 V4.0.2 到 2006 年 6 月 7 日发布的 V4.0.3 的变更

+ 增加了针对使用 IAR
  开发工具的 Cortex-M3 目标的移植和演示应用程序。

+ ARM Cortex-m3 Rowley 项目已更新为使用 V1.6 版本
  的 CrossStudio 工具。

+ 减少了为 lwIP Rowley 演示定义的堆大小，
  以便在使用命令行 GCC 工具时
  也能正确链接该项目。  此外，还修改了生成文件，以便进行调试。

+ lwIP Rowley 演示不包括“内核感知”调试窗口。

+ uIP Rowley 项目已更新为使用 CrossWorks V1.6 版构建。

+ blockQ 演示中的第二组任务的创建方式是错误的
  （与文件中的描述不一致）。  这一问题
  已得到纠正。


### 从 V4.0.1 到 2006 年 5 月 28 日发布的 V4.0.2 的变更

+ 增加了针对 Tern Ethernet Engine 控制器的移植和演示应用程序。

+ 增加了针对使用 GCC 的 MC9S12 的移植和演示应用程序，感谢
  Jefferson "imajeff" Smith。

+ 函数 vTaskList() 现在可以在创建任务列表时挂起调度器，
  而不是禁用中断。

+ 允许任务通过传递自己的句柄来删除自己。  在此之前，
  只能通过输入 NULL 来实现该效果。

+ 更正了 STR71x 演示中
  传递给 WDG_PeriodValueConfig() 库函数的值。

+ 滴答钩子函数现在只在滴答 isr 内调用。  在此之前，
  在调度器解锁过程中调用滴答函数时也会调用它
  。

+ SAM7X lwIP 演示中的 EMAC 驱动程序已变得更加稳健，
  详情请参阅以下帖子：https://sourceforge.net/forum/message.php?msg_id=3714405。

+ 在 PC 移植中：  增加了函数 prvSetTickFrequencyDefault()，
  以便在调度器退出时将 DOS 滴答设回正确值。  感谢
  Raynald！

+ 在 Borland x86 移植中，portFIRST_CONTEXT 宏中有一个错误，
  没有正确地从堆栈中弹出 BP 寄存器。  BP 值
  永远不会被使用，所以这并没有造成问题，
  但还是对其进行了纠正。


### 从 V4.0.0 到 2006 年 4 月 7 日发布的 V4.0.1 的变更

+ 改进了 ARM CORTEX M3 移植，
  现在只需为 pendSV 中断提供服务。

+ 增加了与 Rowley CrossWorks 一起使用的 Luminary Micro 移植和演示。

+ 在 tasks.c 中增加了 xMissedYield 处理功能。


### 从 V3.2.4 到 V4.0.0 的变更

主要变更：

+ 增加了适用于 Luminary Micro 的 ARM CORTEX M3 微控制器的新 RTOS 移植。

+ 增加了新的协程功能。

其他内核变更：

+ 现在，滴答函数中包含了可选的滴答钩子调用。

+ 引入了 xMiniListItem 结构体，并删除了列表 pxHead 成员，
  以减少 RAM 的使用。

+ 在每个移植随附的 FreeRTOSConfig.h 文件中
  添加了以下定义：
    configUSE_TICK_HOOK
    configUSE_CO_ROUTINES
    configMAX_CO_ROUTINE_PRIORITIES

+ 更改了列表成员的易失性限定，
  以便稍微整理 task.c 代码。

+ 现在，即使没有创建任务，也可以启动调度器！
  这样做是为了在没有任务时允许协程运行。

+ 现在，被事件唤醒的任务将抢先执行当前正在运行的任务，
  即使其优先级仅与当前正在运行的任务相同。

移植和演示应用程序变更：

+ 更新了 WinAVR 演示，以便使用最新版本的 WinAVR 进行编译，
  且不会产生警告。

+ 修改了 WinAVR 生成文件，使字符有符号——
  如果 BaseType_t 设置为 char，则协程代码需要字符有符号。

+ 增加了新的演示应用程序文件 crflash.c。  这演示了协程的功能，
  包括在协程之间传递数据。

+ 增加了新的演示应用程序文件 crhook.c。  这演示了协程
  和滴答钩子功能，
  包括在 ISR 和协程之间传递数据。

+ 在各种 ARM7 移植中，
  stmdb{}^ 指令后缺少一些 NOP。  已添加这些内容。

+ 更新了 Open Watcom PC 演示项目，
  加入了 crflash 和 crhook 演示协程，作为使用示例。

+ 更新了 H8S 演示，以便使用最新版本的 GCC 进行编译。

+ 更新了 SAM7X EMAC 驱动程序，
  以考虑到有关数据包丢失的硬件勘误表。

+ 更改了某些 WEB 服务器演示使用的默认 MAC 地址，
  因为某些路由器不喜欢原来使用的地址。

+ 对 SAM7X/IAR 启动代码稍作修改，
  以防止使用 j-link 调试器执行代码时在某些系统上挂起。  j-link 宏文件
  会在代码执行前配置 PLL，
  因此尝试在启动代码中再次配置
  会给某些用户带来问题。  现在，
  首先要检查 PLL 是否已经设置好。

+ GCC 移植现在将所有汇编程序代码包含在一个 asm 块中，
  而不是像以前那样包含在单个块中。

+ GCC LPC2000 代码现在明确使用 R0，
  而不是让汇编程序选择在上下文切换期间用作临时寄存器的寄存器
  。

+ 增加了 portNOP() 宏。

+ LPC2000 移植上的比较匹配负载值现在增加了 1，
  以纠正所使用的值。

+ WIZC PIC18 移植的最小堆栈深度略有增加
  。


### 从 V3.2.3 到 V3.2.4 的变更

+ 修改了 GCC ARM7 移植层，以便与 GCC V4.0.0 及以上版本一起使用。
  非常感谢 Glen Biagioni 提供的最新信息。

+ 增加了新的 Microblaze 移植和演示应用程序。

+ 修改了 SAM7X EMAC 演示，默认使用 MII 接口而不是
  RMII 接口。

+ 对 SAM7X 演示的启动顺序稍作修改，
  使 EMAC 不再自动协商。


### 从 V3.2.2 到 V3.2.3 的变更

+ 为 SAM7X EMAC 外围设备驱动程序增加了 MII 接口支持。
  以前的版本只能使用 RMII 接口。

+ 为 SAM7X lwIP 演示增加了命令行 GCC 支持。  此前，
  只能使用 CrossWorks IDE 构建项目。  为此所做的修改
  包括在下载包中添加标准生成文件和链接器脚本，
  以及对分配给每个任务的堆栈进行一些调整。

+ 更改了 lwIP WEB 服务器演示返回的页面，
  以显示任务状态表而非 TCP/IP 统计数据。

+ 更正了某些头文件包含项和生成文件依赖项的大写，
  以方便在 Linux 主机上使用。

+ 各种 LPC2000 移植的定时器设置存在错误，
  预刻度值被写入 T0_PC，而不是 T0_PR。  除非实际需要预刻度值，
  否则这不会产生任何影响。  这一问题
  已得到纠正。


### 从 V3.2.1 到 2005 年 9 月 23 日发布的 V3.2.2 的变更

+ 增加了适用于 Philips LPC2129 的 IAR 移植

+ Atmel ARM7 IAR 演示项目文件现在以 IAR Embedded
  Workbench V4.30a 格式保存。

+ 更新了 SAM7X uIP 演示项目随附的 J-Link 宏文件，
  允许通过 J-Link 复位演示板。


### 从 V3.2.0 到 2005 年 9 月 1 日发布的 V3.2.1 的变更

+ 增加了针对使用 Rowley 工具的 AT91SAM7X 的 lwIP 演示。

+ 增加了针对使用 IAR 工具的 AT91SAM7X 的 uIP 演示。

+ 增加了函数 xTaskGetCurrentTaskHandle()。

+ 将 events.h 重命名为 mevents.h，
  以防止与 HCS12 处理器专家实用程序自动生成的 events.h 冲突。  events.h
  仅用于 PC 演示应用程序。

+ 现在，两个 PIC18 移植都将 TBLPTRU 初始化为 0，
  因为这是编译器所期望的值，而且编译器不会写入该
  寄存器。

+ HCS12 银行模型演示现在
  会在启动调度器之前立即创建“自杀”任务。  这些任务应该是最后启动的任务，
  以便测试正常运行。


### 从 V3.1.1 到 2005 年 6 月 29 日发布的 V3.2.0 的变更

V3.2.0 引入了两个新的 MSP430 移植，并修正了一个内核
小问题。  感谢 Ares.qi 提供的信息。

+ 增加了两个使用 Rowley CrossWorks 开发工具的 MSP430 移植。
  其中一个移植只是镜像了现有的 GCC 移植。  另一个移植
  由 Milos Prokic 提供。  感谢！

+ V3.2.0 修正了当调度器被锁定
  （通过调用 vTaskSuspendAll()）时调用 vTaskPrioritySet()
  或 vTaskResume() 的行为。  这样做后，
  如果主题任务的优先级最高，并已准备好运行，
  那么当调度器解锁时，主题任务就会立即开始执行。  以前，
  任务可能要到下一次 RTOS 滴答或调用 portYIELD() 时才能运行。

+ 另一个类似的小修正可确保
  在一个以上的任务被阻塞在一个信号量或队列中时，
  可保证优先级最高的任务首先解除阻塞。

+ 在 PC 演示中又添加了几个测试任务，
  涵盖了上述几点。


### 从 V3.1.0 到 2005 年 6 月 21 日发布的 V3.1.1 的变更

该版本更新了 HCS12 移植。  通用内核代码
保持不变。

+ 更新了 HCS12 移植以支持银行业务，
  并引入了一个适用于 MC9S12DP256 的演示应用程序。  该演示应用程序
  可在 Demo/HCS12_CodeWarrior_banked 目录中找到。

+ 包含 MC9S12F32 演示应用程序的目录名称
  已更改为 Demo/HCS12_CodeWarrior_small（“小”
  内存模型）。

+ MC9S12F32 演示稍作更新，以使用 PLL。  现在，
  演示应用程序的 CPU 速度为 24 MHz。  之前，该数字为 8 MHz。

+ 演示应用程序文件 Demo/Common/Minimal/death.c 略有改动，
  以防止使用浮点变量。


### 从 V3.0.0 到 2005 年 6 月 11 日发布的 V3.1.0 的变更

+ 增加了适用于 ST Microsystems STR71x 和 Freescale HCS12 微控制器的新移植
  。  目前，HCS12 移植仅限于小
  内存模型。  下一个版本将支持
  大内存模型。

+ 更新了 PIC18 wizC 移植。  感谢 Marcel van Lieshout
  一直以来的贡献。

+ AVR 移植定时器设置的准确性得到提高。  感谢
  Thomas Krutmann 的贡献。

+ 增加了新的条件编译宏 configIDLE_SHOULD_YIELD。
  请参阅 WEB 文档了解详细信息。

+ 更新了 CrossWorks uIP 演示，以便使用 CrossWorks V1.4 版构建。

+ 对 SAM7 版本的构建配置稍作修改，
  以纠正包含路径定义。

+ 更新了 MPLAB PIC18 文档，
  以提供有关链接器文件配置的更多详细信息。


### 从 V2.6.1 到 2005 年 4 月 23 日发布的 V3.0.0 的变更

V3.0.0 包含许多增强功能，因此本历史列表
分为以下几个小节：

+ API 变更

+ 新移植

+ 目录名称变更

+ 内核和杂项变更


#### API 变更

+ 现在，每个移植都将 BaseType_t 定义为
  该架构最有效的数据类型。  BaseType_t 类型
  在 API 调用中被广泛使用，
  因此有必要对 FreeRTOS API 函数原型进行如下修改。

  请参阅 FreeRTOS 在线文档中的 “New for V3.0.0” 章节
  了解 API 变更的完整信息。


#### 新移植

+ John Feller 提供的 AT91FR40008 ARM7 移植
  现已包含在下载包中（感谢 John！）。

+ 由 Marcel van Lieshout 提供的 wizC/fedC 编译器的 PIC18 移植
  现在已包含在下载包中（感谢 Marcel！）。

+ AVR 微控制器的 IAR 移植已升级到 V3.0.0，
  现在是受支持的移植。


#### 目录名称变更

为了保持一致，并允许整合新的移植，
更改了以下目录名称。

+ source/portable/GCC/ARM7 目录已更名为
  source/portable/GCC/ARM7_LPC2000，
  以便与其他 GCC ARM7 移植的命名一致。

+ Demo/PIC 目录已更名为 Demo/PIC18_MPLAB，
  以适应 wizC/fedC PIC 移植。

+ 两个 AVR 移植的演示应用程序不再共享同一
  目录。  WinAVR 演示位于 Demo/AVR_ATMega323_WinAVR 目录下，
  IAR 移植位于 Demo/AVR_ATMega323_IAR 目录下。


#### 内核和杂项变更

请参阅 FreeRTOS 在线文档中的 “New for V3.0.0” 章节
了解更多信息。

+ 以前，“portmacro.h ”包含
  一些与用户应用程序相关的用户可编辑定义，
  以及一些与所使用移植相关的固定定义。  portmacro.h' 中的应用程序特定定义已被删除，
  并被放入一个
  名为 “FreeRTOSConfig.h” 的新头文件中。  现在，“portmacro.h”
  绝不能被用户修改。  现在，“FreeRTOSConfig.h” 包含在
  每个 FreeRTOS/Demo 子目录中，
  因为它的设置与演示应用程序有关，而不是特定于移植。

+ 在空闲任务中引入了 configUSE_IDLE_HOOK。

+ 当另一个空闲优先级任务准备就绪时，空闲任务将让位
  。此前，空闲任务无论如何都会运行到其时间切片的末尾
  。

+ 现在，空闲任务会在调度器启动时创建。  与
  之前在创建第一个应用程序任务时创建堆栈的方案相比，
  这种方案所需的堆栈更少。

+ 函数 usPortCheckFreeStackSpace() 已更名为
  usTaskCheckFreeStackSpace() 并从可移植层移至
  tasks.c。

+ 将 portMINMAL_STACK_SIZE 的拼写更正为 portMINIMAL_STACK_SIZE。

+ AVR 移植随附的 portheap.c 文件已被删除。  AVR 演示
  现在使用标准 heap1 样本内存分配器。

+ GCC AVR 移植现在使用标准 make 实用程序构建。  之前使用的
  批处理文件已被删除。  这意味着
  需要最新版本的 WinAVR 才能创建适合源代码级调试
  的二进制文件。

+ vTaskStartScheduler() 不再将 configUSE_PREEMPTION 常量
  作为参数。  取而代之的是
  在 tasks.c 中直接使用该常量，  不需要任何参数。

+ 已创建头文件 “FreeRTOS.h”，
  并用于按必要顺序包含 “projdefs.h”、“FreeRTOSConfig.h ”和 “portable.h”
  。  现在可以用 FreeRTOS.h 代替这些其他
  标头。

+ 头文件 'errors.h' 已被删除。  其中包含的定义
  现在位于 “projdefs.h ”中。

+ pvPortMalloc() 现在与 ANSI malloc() 一样使用 size_t 参数。
  以前使用的是无符号短字符。

+ 恢复调度器时，如果错过了一个滴答，
  或者任务从待定就绪列表移到了就绪列表，
  则会执行一次让位。  在此之前，
  并没有对这第二个条件进行让位。

+ 在 heap1.c 中添加了溢出检查，
  以确保下一个空闲字节变量不会缠绕。

+ 引入了 portTASK_FUNCTION() and portTASK_FUNCTION_PROTO() 
  宏。

+ MPLAB PIC 移植现在可以在中断服务例程中保存 TABLAT 寄存器
  。


### 从 V2.6.0 到 2005 年 2 月 22 日发布的 V2.6.1 的变更

该版本增加了对 H8 处理器的支持。

其他变更：

+ 删除了 task.h 头文件中的 tskMAX_TASK_NAME_LEN， 
  并将其作为 portMAX_TASK_NAME_LEN 添加到各 portmacro.h 文件中。  这样，受 RAM 限制的
  移植就可以为任务名称分配较少的字符。

+ AVR 移植——以直接内存访问取代 inb() 和 outb() 函数
  。  这样就可以使用 WinAVR 的 20050414 版本
  来构建移植。

+ GCC LPC2106 移植——删除了 vNonPreemptiveTick() 定义中的 “static”，
  以便在使用合作式调度器时链接演示
  。

+ GCC LPC2106 移植——更正了批处理文件
  ROM_THUMB.bat、RAM_THUMB.bat、ROM_ARM.bat 和 RAM_ARM.bat 中的优化选项。  小写
  -o 被大写 -O 代替。

+ Tasks.c——在将任务名称复制到 TCB 时
  删除了 strcpy 调用。

+ 更新了跟踪可视化，使其始终采用 4 字节对齐方式，
  以便在 ARM 架构上使用。

+ 现在有两个 tracecon 可执行程序
  （将二进制跟踪文件转换为 ASCII 文件）。  一个用于大 endian 目标，一个用于小 endian
  目标。

+ 增加了 ucTasksDeleted 变量，
  以防止在空闲任务中频繁调用 vTaskSuspendAll()。

+ SAM7 USB 驱动程序——将中断屏蔽中重复的 RX_DATA_BK0
  替换为 RX_DATA_BK1。


### 从 V2.5.5 到 2005 年 1 月 16 日发布的 V2.6.0 的变更

+ 增加了 API 函数 vTaskDelayUntil()。  演示应用程序文件
  Demo/Common/Minimal/flash.c 已更新，以演示其用法。

+ 增加了 INCLUDE_vTaskDelay 条件编译。

+ 将 Demo/ARM7_AtmelSAM7S64_IAR 目录更名为
  Demo/ARM7_AT91SAM7S64_IAR，以保持一致。

+ 修改了 AT91SAM7S USB 驱动程序，
  允许传输长度为 FIFO 整数倍的描述符。


### 从 V2.5.4 到 2005 年 1 月 3 日发布的 V2.5.5 的变更

该版本增加了对 Atmel SAM7 ARM7 微控制器
和 IAR 开发工具的支持。

其他变更：

+ 将 Demo/ARM7 目录重命名为 Demo/ARM7_LPC2106_GCC。

+ 将 Demo/ARM7_Keil 目录重命名为 Demo/ARM7_LPC2129_Keil。

+ 修改了 Philips ARM7 串行中断服务程序，
  使每次调用只处理一个中断。  这似乎使 ISR
  能够更快地运行。

+ 删除了 Open Watcom 可移植图层源文件中的 “far ”关键字
  。  这样，它们就可以与 V1.3 Open Watcom 一起使用。

+ 对 SDCC 生成文件稍作修改，
  以便在 Linux 下使用。  感谢 Frieder Ferlemann 的贡献。

+ 对 sTaskCreate() 稍作修改，
  以便在 pxCreatedTask 为 NULL 时也能进行上下文切换。  感谢 Kamil 的贡献。

+ 删除了 vTaskSwitchContext() 和 VTaskIncrementTick()
  定义中的 inline 关键字。


### 从 V2.5.3 到 2004 年 12 月 1 日发布的 V2.5.4 的变更

这是一个重要的维护版本。

修改了函数 cTaskResumeAll()，
使其可以在内核初始化之前安全使用。  这是一个问题，
因为 cTaskResumeAll() 是通过 pvPortMalloc() 调用的。  感谢 Daniel Braun
强调这一问题。


### 从 V2.5.2 到 2004 年 11 月 2 日发布的 V2.5.3 的变更

为 GCC ARM7 移植修改了临界区处理功能
。   某些优化级别使用堆栈的方式与其他优化级别不同。  这意味着
中断标志不能总是存储在堆栈中，
而是存储在一个变量中，
然后作为任务上下文的一部分保存。  这使得 GCC ARM7 移植可以
在包括 -Os 在内的所有优化级别下使用。

其他细微变更：

+ MSP430 的 usCriticalNesting 定义现在使用易失限定符。
  这可能不是必需的，但为了以防万一还是加上了。


### 从 V2.5.1 到 2004 年 10 月 26 日发布的 V2.5.2 的变更

+ 增加了 Keil ARM7 移植。

+ 对 comtest.c 稍作修改，使延迟时间更加随机。
  这样就能创造更好的测试条件。


### 从 V2.5.0 到 2004 年 10 月 9 日发布的 V2.5.1 的变更

+ 增加了 MSP430 移植。

+ 在 GCC ARM7 port.c 和 portISR.c 文件中添加了额外注释。

+ 在 heap_1.c 中分配的内存池被置于一个结构体中，
  以确保在 32 位系统上正确对齐内存。

+ 在 GCC ARM7 串行驱动程序中，
  如果尝试立即检索已发布的字符，则会进行额外检查，
  以确保向队列发布成功。

+ 将 portTICKS_PER_MS 常量的名称改为 portTICK_PERIOD_MS，
  因为旧名称容易引起误解。


### 从 V2.4.2 到 2004 年 8 月 12 日发布的 V2.5.0 的变更

RTOS 源代码下载包现在包括三种独立的内存分配方案，
因此您可以选择最适合您应用程序的方案。
这些内容可在 Source/Portable/MemMang 目录中找到。  演示
应用程序项目也已更新，以展示新方案。
请参阅 API 文档中的“内存管理”页面了解详细信息。

+ 在 Source/Portable/MemMang 目录中添加了 heap_1.c、heap_2.c 和 heap_3.c
  。

+ 用新的内存分配文件
  替换了每个演示程序的 portheap.c 文件。

+ 更新了每个演示应用程序的 portmacro.h 文件，
  以包含新内存分配器所需的常量：portTOTAL_HEAP_SIZE 和
  portBYTE_ALIGNMENT。

+ 为 ARM7 演示应用程序添加了一个新测试，
  以测试 heap_2 内存分配器的运行情况。


### 从 V2.4.1 到 2004 年 7 月 14 日发布的 V2.4.2 的变更

+ ARM7 移植现在支持 THUMB 模式。

+ 修改了 ARM7 演示应用程序串行端口驱动程序。


### 从 V2.4.0 到 2004 年 7 月 2 日发布的 V2.4.1 的变更

+ 合理化了 ARM7 移植版本的 portEXIT_CRITICAL()
  ——改进由 Bill Knight 提供。

+ 使演示串行驱动程序更完整、更强大。


### 从 V2.3.1 到 2004 年 6 月 30 日发布的 V2.4.0 的变更

+ 增加了第一个 ARM7 移植——感谢 Bill Knight 提供的帮助
  。

+ 在 Demo/Common/Minimal 目录中添加了额外文件。  它们
  与 Demo/Common/Full 中的对应程序等价，
  但删除了对 print.c 中定义的函数的调用。

+ 在作为 PIC18 上下文的一部分保存的寄存器列表中添加了 TABLAT。


### 从 V2.3.0 到 2004 年 6 月 25 日发布的 V2.3.1 的变更

+ 更改了矢量表的定义方式，使其更具可移植性。

+ 修正了 portmacro.s90 中 SPH 和 SPL 的定义。
  如果 portmacro.s90 中包含 iom323.h 头文件，
  以前的定义会阻止 V2.3.0 运行。


### 从 V2.2.0 到 2004 年 6 月 19 日发布的 V2.3.0 的变更

+ 增加了一个使用 IAR 编译器的 AVR 移植。

+ 在普通字符类型中明确使用 “signed” 限定符。

+ 修改了 Open Watcom 项目文件，
  将 “signed” 作为默认字符类型。

+ 更改了 portSTACK_GROWTH < 0 时 pxTopOfStack 初始值
  的奇异计算。

+ 为 task.c 中的上下文切换函数添加了内联限定符。
  不支持（非 ANSI）内联关键字的移植
  会在各自的 portmacro.h 文件中  取消内联 #define。


### 从 V2.1.1 到 2004 年 5 月 18 日发布的 V2.2.0 的变更

+ 增加了 Cygnal 8051 移植。

+ PCLATU 和 PCLATH 现在保存为 PIC18 上下文的一部分。  这样
  就可以在任务中使用函数指针。  感谢 Javier
  特别是在增强功能方面。

+ 对演示应用程序文件稍作修改，以减少堆栈使用。

+ 进行了一些小改动，以防止编译新移植时出现编译器警告。


### 从 V2.1.0 到 2004 年 3 月 12 日发布的 V2.1.1 的变更

+ 错误修复——现在会在调用 prvInitialiseTaskLists() 之前
  初始化 pxCurrentTCB。  以前，
  在初始化序列中，pxCurrentTCB 可以在空值状态下被访问。  感谢 Giuseppe
  Franco 的纠正。


### 从 V2.0.0 到 2004 年 2 月 29 日发布的 V2.1.0 的变更

V2.1.0 版进行了重大修改，
大大减少了内核禁用中断的时间。  用户必须注意此处列出的
第一节修改。  第二节
与内核实现有关，因此是透明的。

第 1 节：

+ 引入了 typedef TickType_t。  现在，所有延迟时间
  都应使用 TickType_t 类型的变量，
  以取代之前使用的无符号 long 变量。  API 函数原型已做
  适当更新。

+ 引入了配置宏 USE_16_BIT_TICKS。  如果
  设置为 1，TickType_t 将被定义为无符号短型。  如果
  设置为 0，TickType_t 将被定义为无符号长型。  请参阅
  API 文档的配置章节了解更多信息。

+ 配置宏 INCLUDE_vTaskSuspendAll 现已弃用。

+ vTaskResumeAll() 已更名为 cTaskResumeAll()，
  因为它现在返回一个值（请参阅 API 文档）。

+ ulTaskGetTickCount() 已更名为 xTaskGetTickCount()，
  因为其返回的类型现在取决于 USE_16_BIT_TICKS 定义。

+ 现在必须 >绝不< 在 ISR 中使用 cQueueReceive()。  请使用新的
  cQueueReceiveFromISR() 函数。

第 2 节：

+ 引入了一种机制，
  允许任务和 ISR 同时访问队列。

+ 引入了“等待就绪”队列，
  使调度器挂起时也能处理中断。

+ 改进了列表实现，
  以提供更快的项目移除速度。

+ 调度器现在可以
  在以前禁用中断的地方使用调度器挂起机制。


### 从 V1.2.6 到 2004 年 1 月 31 日发布的 V2.0.0 的变更

+ 引入了新的 API 函数：

  + vTaskPriorityGet ()
  + vTaskPrioritySet ()
  + vTaskSuspend ()
  + vTaskResume ()
  + vTaskSuspendAll ()
  + vTaskResumeAll ()

+ 增加了条件编译选项，
  允许在构建过程中排除应用程序未使用的内核组件。
  请参阅 WEB 网站上的配置章节了解更多信息
  （在 API 页面上）。  宏已添加到每份 portmacro.h 文件
  （有时称为 prtmacro.h）中。

+ 重新排列了 tasks.c。

+ 增加了演示应用程序文件 dynamic.c。

+ 更新了 PC 演示应用程序以使用 dynamic.c。

+ 更新了内核头文件中包含的文档。

+ 现在，如果创建的任务比调用任务的优先级更高
  （假设内核正在运行），
  则创建任务会导致上下文切换。

+ 现在，vTaskDelete() 只有在调用任务是被删除的任务时
  才会导致上下文切换。


### 从 V1.2.5 到 2003 年 12 月 31 日发布的 V1.2.6 的变更

除了中断向量（PIC 移植）的变化外，
这些都是小改进。

+ 用于 PIC 主 ISR 的中断向量
  已从 0x18 更改为 0x08——它本应始终为 0x08。  不正确的地址
  仍然可以工作，但在进入 ISR 之前可能会执行许多 NOP
  。

+ 将 AVR 演示应用程序使用的波特率改为 38400。  在
  时钟频率为 8 MHz 的情况下，误差率小于 1%。

+ 提高了 demo\full\comtest.c 中 Rx 任务的优先级。  这只影响
  Flashlite 和 PC 移植。  这样做是为了防止 Rx
  缓冲区满载。

+ 恢复了 Flashlite COM 移植驱动程序，使其不使用 DMA。
  在压力下，DMA 似乎会丢失字符。  Borland Flashlite
  移植还错误地计算了寄存器值，
  导致使用了错误的 DMA 源地址。  同样的代码
  在使用 Open Watcom 编译时也能正常运行。  还对中断处理进行了
  其他小的改进。

+ 修改了 PIC 串行 Rx ISR，以检查并清除超限错误。
  超限错误似乎阻止了接收更多字符。

+ 现在，PIC 演示项目已经开启了一些优化功能。


### 从 V1.2.4 到 V1.2.5 的变更

对 PIC 专用的 port.c 文件进行了小修，如下所述。

+ 引入了 portGLOBAL_INTERRUPT_FLAG 定义，
  用于测试全局中断标志设置。  使用
  portINITAL_INTERRUPT_STATE 中定义的两个位
  会导致 w 寄存器在执行测试前被重写。


### 从 V1.2.3 到 V1.2.4 的变更

V1.2.4 包含 PIC18 移植的发布版本。
GPL 中包含一个可选的例外。  请参阅
www.FreeRTOS.org 许可章节了解详细信息。

+ 函数 xPortInitMinimal() 已更名为
  xSerialPortInitMinimal()，函数 xPortInit() 已更名为
  xSerialPortInit()。

+ 函数 sSerialPutChar() 已更名为 cSerialPutChar()，
  函数返回类型已改为 portCHAR。

+ 整数任务和 flop 任务现在包含了对 tskYIELD() 的调用，
  允许它们与合作式调度器一起使用。

+ 在使用合作式调度器时，
  所有演示应用程序现在都使用整数任务和 comtest 任务。  以前，
  它们只使用抢占式调度器。

+ 对 comtest.c 和 integer.c 最小版本的运算
  进行了细微修改。

+ ATMega 移植的 portCPU_CLOCK_HZ 定义改为
  以 10 为基数的 8 MHz 频率，以前是以 16 为基数。


### 从 V1.2.2a 到 V1.2.3 的变更

唯一重要的变化是许可证，
从开放软件许可证改为 GNU GPL。

该压缩文件还包含 PIC18 移植的预发布版本。  该版本
尚未完成测试，
因此不构成 V1.2.3 版本的一部分。  不过，它仍受 GNU GPL 的保护。

为适应 PIC C 编译器，源代码略有改动。
这主要涉及更明确的转换。

+ 对 sTaskCreate() 稍作修改，
  以便使用 portSTACK_GROWTH 宏。  这对 PIC 移植而言是必要的，
  因为其堆栈的增长方向与其他现有移植相反。

+ 对 prvCheckTasksWaitingTermination() 稍作修改，
  以便将 usCurrentNumberOfTasks 的递减功能置于临界区内，
  自创建八位移植以来，该功能本应置于临界区内。


### 从 V1.2.2 到 V1.2.2a 的变更

AVR 演示应用程序中包含的生成文件和 buildcoff.bat 文件已作修改，
以便与 WinAVR 2003 年 9 月版一起使用。  没有
更改源文件。


### 从 V1.2.1 到 V1.2.2 的变更

这里只做了很小的改动，以便 PC 和 Flashlite 186 移植
使用随 Flashlite 186 开发套件提供的 Borland V4.52
编译器。

+ 在 source\portable 下引入了 BCC 目录。  其中包含
  Borland 编译器移植的所有特定文件。

+ 将 portMS_PER_TICK 的宏命名更正为 portTICKS_PER_MS。

+ 修改了 comtest.c，
  以提高串行端口收发字符串的速率。  Flashlite 186 演示
  程序的波特率也已提高。

+ 增加了两个 integer.c 文件中使用的常量值，
  以强制 Borland 编译器使用 32 位值。  Borland
  优化器将之前的值放入了 16 位寄存器，
  从而使测试失效。


### 从 V1.2.0 到 V1.2.1 的变更

该版本包括对列表实现的一些小改动，
旨在改进上下文切换时间——现在大约快了 10%。
改动包括删除了一些空指针赋值检查。  在
调度器使用列表函数的情况下，这些函数是多余的，
但这意味着任何选择使用相同列表函数的用户应用程序
现在都必须检查是否有 NULL 指针作为参数传递。

Flashlite 186 串行端口驱动程序也进行了修改，
以使用 DMA 通道进行传输。  串行驱动程序功能齐全，
但仍在开发中。  Flashlite 用户可能更愿意暂时使用 V1.2.0。

详细信息：

+ 将 ATMega323 串行测试的波特率从 19200 改为 57600。

+ 在 Demo\Full\Comtest.c 中
  使用 vSerialPutString() 代替单字符输入。  这样就可以使用 flashlite DMA 串行
  驱动程序。  此外，只有在连续两次失败后，
  校验变量才会停止递增。

+ semtest.c 创建了四个任务，其中两个以空闲优先级运行。
  现在，以空闲优先级运行的任务
  比以较高优先级运行的任务使用更少的预期计数。  这样可以防止
  低优先级任务发出错误信号，
  因为它们没有安排足够的时间
  让每个任务都将共享变量计入较高的原始值。

+ flashlite 186 串行驱动程序现在使用 DMA 通道进行传输。

+ 删除了列表函数参数中的易失性修饰符。  这样做
  只是为了防止编译器发出警告。  现在，
  在调用时通过转换参数来消除警告。

+ 删除了 list.c 中的 prvListGetOwnerOfNextEntry()
  和 prvListGetOwnerOfHeadEntry() 宏，并将其添加到 list.h 中。

+ usNumberOfItems 已添加到列表结构体中。  这样，
  在检查列表是否为空时，就不需要进行指针比较，
  因此速度稍快。

+ 删除了 vListRemove() 中的 NULL 检查。  这样可以加快调用速度，
  但使用列表实现的应用代码
  必须确保不传递 NULL 指针。

+ 将 portTICKS_PER_MS 定义更名为 portMS_PER_TICK
  （每滴答毫秒）。  这本来就应该是这样。


### 从 V1.01 到 V1.2.0 的变更

这些改动大部分是为了适应 8 位 AVR 移植。
调度器的工作原理没有改变，
但所使用的一些数据类型对 8 位环境更加友好。

详细信息：

+ 更改了版本编号格式。

+ 增加了 AVR 移植。

+ 将 demo\common 目录分为 demo\common\minimal 和
  demo\common\full 两部分。  完整目录中的文件适用于带显示屏的系统
  （目前为 PC 和 Flashlite 186 演示的系统）。  最小目录中的文件
  适用于 RAM 有限且无显示屏的系统
  （目前为 MegaAVR）。

+ 对演示应用程序函数原型稍作修改，
  以便更多地使用 8 位数据类型。

+ 在调度器中，对以下函数的声明稍作修改，
  以便尽可能地使用 8 位数据类型：

  + xQueueCreate(),
  + sQueueReceive(),
  + sQUeueReceive(),
  + usQueueMessageWaiting(),
  + sQueueSendFromISR(),
  + sSemaphoreTake(),
  + sSemaphoreGive(),
  + sSemaphoreGiveFromISR(),
  + sTaskCreate(),
  + sTaskMoveFromEventList()。

  当返回类型发生变化时，
  函数名称也会根据命名规则发生变化。  例如，
  usQueueMessageWaiting() 变成了 ucQueueMessageWaiting()。

+ tskMAX_PRIORITIES 定义已从 task.h 移至 portmacro.h，
  并更名为 portMAX_PRIORITIES。  这样，
  不同的移植就可以分配不同的最大优先级数量。

+ 默认情况下，跟踪工具是关闭的，
  之前定义了 USE_TRACE_FACILITY。

+ comtest.c 现在在发送之间使用了假随机延迟。  这样可以
  更好地进行测试，因为中断不会以固定的时间间隔出现。

+ 对 Flashlite 串行端口驱动程序稍作修改。  编写该驱动程序
  是为了演示调度器，而不是为了提高效率。


### 从 V1.00 到 V1.01 的变更

这些改动对移植进行了改善。  调度器本身没有变化。

改进了从 ISR
（演示应用程序中的滴答 ISR 和串行通信 ISR）
执行上下文切换时使用的上下文切换机制。  新机制速度更快，使用的堆栈更少。

用头文件 portasm.h 取代了汇编文件
 portasm.asm。  其中包括一些汇编程序宏定义。

现在，所有将寄存器存入/存出堆栈的操作
都由编译器处理。  这意味着任务的初始堆栈设置
必须模仿编译器使用的堆栈，
而调试版本和发布版本使用的是不同的堆栈。

对演示程序的操作略有改动，详情如下。

详细信息：

+ 用 vPortFirstContext() 代替 portSWITCH_CONTEXT()。

+ 修改 pxPortInitialiseStack()
  以复制编译器使用的堆栈。

+ 删除了 portasm.asm 文件。

+ 引入了 portasm.h。  其中包含
  portSWITCH_CONTEXT() 和 portFIRST_CONTEXT() 的宏定义。

+ 从 ISR 的上下文切换现在使用编译器生成的中断机制
  。  只需调用 portSWITCH_CONTEXT
  并将保存/恢复操作留给编译器生成的代码即可。

+ ISR 期间对 taskYIELD() 的调用已被更简单、更快速的
  portSWITCH_CONTEXT() 所取代。

+ Flashlite 186 移植现在使用 186 指令集
  （过去仅使用 80x86 指令）。

+ 演示应用程序中的阻塞队列任务
  没有完全按照描述的那样运行。  这一点已修正。

+ 降低了演示应用程序中 comtest Rx 任务的优先级
  。  现在，接收到的字符将以空闲优先级处理（从队列中读取），
  从而使低优先级任务在通信开销较高时
  也能均衡运行。

+ 在调试构建时，防止调用 main.c 中的 kbhit()，
  因为调试器似乎无法跳过该调用。  这仅适用于 PC 移植
  。
      
