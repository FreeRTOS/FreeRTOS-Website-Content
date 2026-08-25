---
title: "SMP Demo for the XMOS XCORE.AI Explorer Board"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

## Introduction

This demo uses the
[Symmetric Multiprocessing (SMP) version](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/) of the FreeRTOS kernel.
It targets the [XCORE.AI](https://www.xmos.ai/xcore-ai/),
which has 16 cores. The demo project uses [XMOS XTC Tools](https://www.xmos.ai/software-tools/) to build the FreeRTOS XCORE.AI port (note the tools require a Linux host or a Linux like environment).
It demonstrates support for [FreeRTOS symmetric multiprocessing (SMP)](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp) in the kernel.

## Source Code Organization

The project files for this demo are located in the `FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo`
directory of the [FreeRTOS SMP Demo Git repository](https://github.com/FreeRTOS/FreeRTOS-SMP-Demos).
FreeRTOS Port files compiled in the project are in the
`FreeRTOS/Source/portable/ThirdParty/xClang/XCORE.AI` directory.

## The SMP Demo Application

The constant `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY`, which is defined at the top
of `testing_main.h`, is used to switch between a simple "blinky" style getting
started project and a more comprehensive test and demo application.

### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY` is set to 1, the demo application
creates two tasks, each of which periodically toggles an on-board LED (LED 0 is toggled by
one task and LED 1 by the other).

### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY` is set to 0, the demo application
implements a comprehensive test and demo that, among other things, demonstrates
and/or tests:

* [Message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications. They
have no specific functionality, and were created simply to demonstrate how to use
the FreeRTOS API, and to test the RTOS port.

Two "check" tasks are created to periodically inspect the standard demo tasks
(which contain self monitoring code) to ensure all the tasks are functioning as
expected. One check task monitors the demo tasks running on tile 0 and toggles
LED 0 each time it executes. The other check task monitors the demo tasks
running on tile 1 and toggles LED 1 each time it executes. This gives visual
feedback of the system health. **If both the LEDs toggle every 3 seconds, then the
check tasks have not discovered any problems. If any LED toggles every 200ms,
then the check task has discovered a problem in one or more tasks.**

### Building and Running the RTOS Demo Application

### Hardware setup

Plug the xTAG programmer into the evaluation board. Ensure both the xTAG and
evaluation board are connected to the computer via USB.

### Toolchain installation

The development tools require a Linux host or a Linux style environment.

1. Download the [XMOS XTC Tools](https://www.xmos.ai/software-tools/).
2. Uncompress the archive to your chosen installation directory. The example
 below will install to your home directory:

```c
$ tar -xf archive.tgz -C ~
```
3. Configure the default set of environment variables:

```c
$ cd ~/XMOS/XTC/15.1.0
$ source SetEnv
```
4. Check that your tools environment has been setup correctly:

```c
$ xcc --help
```
5. Make the XTAG drivers accessible to all users. This step is only required
 to be done once on a given development machine.

```c
$ cd ~/XMOS/XTC/15.1.0/scripts
$ sudo ./setup_xmos_devices.sh
```
6. Check that the XTAG devices are available and accessible:

```c
$ cd ~/XMOS/XTC/15.1.0/scripts
$ ./check_xmos_devices.sh
Searching for xtag3 devices...
0 found
Searching for xtag4 devices...
1 found
Success: User <username> is able to access all xtag4 devices
```
7. Check that the device is available for debugging:

```c
$ xrun -l
### Available XMOS Devices

  ID  Name            Adapter ID    Devices
  --  ----            ----------    -------
  0   XMOS XTAG-4     2W3T8RAG      P[0]
```

### Build and Run the demo application

1. Go to the RTOSDemo directory:

```c
$ cd FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo
```
2. Build the demo:

```c
$ make
```
3. Run the demo:

```c
$ make run
```

## RTOS Configuration and Usage Details

* Configuration items specific to this demo are in the file
`FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo/src/FreeRTOSConfig.h`. The
[constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization) can be
edited to suit your application. The following configuration options are
specific to the SMP support in the FreeRTOS Kernel:
	+ `configNUM_CORES` - Set the number of cores.
	+ `configRUN_MULTIPLE_PRIORITIES` - Enable/Disable simultaneously running tasks with multiple priorities.
	+ `configUSE_CORE_AFFINITY` - Enable/Disable setting a task's affinity to certain cores.
* `Source/Portable/MemMang/heap_4.c` is included in the project to provide the
memory allocation required by the RTOS kernel. Please refer to the
[Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API
documentation for complete information.
* vPortEndScheduler() has not been implemented.
