---
title: Percepio View for FreeRTOS
created: 2025-01-20
categories:
  - kernel
relatedLinks:
  - title: Tracealyzer™
    link: /Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Free tracing tool for FreeRTOS applications, based on Percepio Tracealyzer.
<br />

[![](/media/2025/percepio-view-freertos-2.png)](/media/2025/percepio-view-freertos-2.png)

```jsx
<TraceButton link="https://traceviewer.io/get-view/?target=freertos" text="Download Percepio View"/>
```

## Introduction

The FreeRTOS kernel provides real-time multithreading, which brings many advantages, but also another
dimension for developers to consider – the concept of tasks and their runtime interactions.

Percepio View is a free tracing tool based on Percepio Tracealyzer. This works as a surveillance
camera for your FreeRTOS application, facilitating debugging and verification.

Percepio View can be used side-by-side with a traditional debugger and complements your debugger
by visualising the real-time execution of tasks and ISRs, including FreeRTOS API calls and your own “User Events”.
It does not require any special tracing hardware.
<br />

[![](/media/2025/FreeRTOS-View-User-Events.png)](/media/2025/FreeRTOS-View-User-Events.png)


To learn more about Percepio View, how to get started and upgrade options, check out [Percepio's product page](https://traceviewer.io/get-view/?target=freertos).

## How it works

The FreeRTOS kernel contains around 100 “[trace hooks](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature)” at strategic locations in the code.
Percepio View includes the TraceRecorder library that uses these trace hooks to record important
kernel events. No modifications of the FreeRTOS source code are needed, only a configuration change and rebuild
to enable the trace hooks. The tracing overhead is typically not noticeable, although
this depends on the application and processor speed.

Percepio View is limited to snapshot tracing, meaning the data is stored to a ring-buffer
in target RAM. Percepio View runs on Windows and Linux hosts.

## Demo

The [CORTEX\_MPS2\_QEMU\_IAR\_GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model) demo has been extended with Percepio TraceRecorder to demonstrate Percepio View.
This runs in the QEMU simulator, so no development board is needed. See [readme.md in the CORTEX\_MPS2\_QEMU\_IAR\_GCC demo folder](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC) for instructions.

