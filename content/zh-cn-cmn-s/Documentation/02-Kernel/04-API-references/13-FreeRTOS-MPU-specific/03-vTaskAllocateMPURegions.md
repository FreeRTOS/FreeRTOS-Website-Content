---
title: vTaskAllocateMPURegions
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-MPU 特定](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task. h

```c
void vTaskAllocateMPURegions(
               TaskHandle_t xTaskToModify,
               const MemoryRegion_t * const xRegions );
```

在使用
`xTaskCreateRestricted()` 调用创建任务时，内存区域会分配给受限任务。然后，可以
在运行时使用 `vTaskAllocateMPURegions()` 对这些区域进行修改或重新定义。

`vTaskAllocateMPURegions()` 适用于 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，
其[演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)包含
被使用的 `vTaskAllocateMPURegions()` 的示例。


**参数：**

- *xTask*

  正在更新的任务的句柄。

- *xRegions*

  指向 `MemoryRegion_t` 结构体数组的指针，每个结构体都包含一个新的内存区域定义。
  应使用常量 `portNUM_CONFIGURABLE_REGIONS` 确定数组的大小，该常量在 ARM Cortex-M3 上设置为 3。

`MemoryRegion_t` 在 task.h 中定义为：

```c
typedef struct xMEMORY_REGION
{
    void *pvBaseAddress;
    unsigned long ulLengthInBytes;
    unsigned long ulParameters;
} MemoryRegion_t;
```

`pvBaseAddress` 和 `ulLengthInBytes` 成员分别自行解释为
内存区域的开始和内存区域的长度。
必须指出，MPU 必须满足一些约束条件，
每个区域的尺寸和对齐，必须均等于两个值的相同幂函数。

`ulParameters` 定义了访问内存区域的方法，
并且可以采用以下值中的按位 OR：

```c
    portMPU_REGION_READ_WRITE
    portMPU_REGION_PRIVILEGED_READ_ONLY
    portMPU_REGION_READ_ONLY
    portMPU_REGION_PRIVILEGED_READ_WRITE
    portMPU_REGION_CACHEABLE_BUFFERABLE
    portMPU_REGION_EXECUTE_NEVER
```

使用示例（请参阅 FreeRTOS-MPU [ 演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)
了解更完整、更全面的示例）：

```c
/* Define an array that the task will both read from and write to. Make sure
   the size and alignment are appropriate for an MPU region (note this uses GCC
   syntax). */
static unsigned char ucOneKByte[ 1024 ] __attribute__((align( 1024 )));

/* Define an array of MemoryRegion_t structures that configures an MPU region
   allowing read/write access for 1024 bytes starting at the beginning of the
   ucOneKByte array. The other two of the maximum 3 definable regions are
   unused so set to zero. */
static const MemoryRegion_t xAltRegions[ portNUM_CONFIGURABLE_REGIONS ] =
{
    /* Base address Length Parameters */
    { ucOneKByte, 1024, portMPU_REGION_READ_WRITE },
    { 0, 0, 0 },
    { 0, 0, 0 }
};

void vATask( void *pvParameters )
{
    /* This task was created such that it has access to certain regions of
       memory as defined by the MPU configuration. At some point it is
       desired that these MPU regions are replaced with that defined in the
       xAltRegions const struct above. Use a call to vTaskAllocateMPURegions()
       for this purpose. NULL is used as the task handle to indicate that this
       function should modify the MPU regions of the calling task. */
    vTaskAllocateMPURegions( NULL, xAltRegions );

    /* Now the task can continue its function, but from this point on can only
       access its stack and the ucOneKByte array (unless any other statically
       defined or shared regions have been declared elsewhere). */
}
```
