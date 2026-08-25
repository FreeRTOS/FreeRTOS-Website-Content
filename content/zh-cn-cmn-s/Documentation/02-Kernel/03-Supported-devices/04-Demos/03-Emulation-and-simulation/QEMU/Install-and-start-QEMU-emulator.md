---
title: "安装并启动 QEMU 仿真器 "
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 用于 FreeRTOS 演示应用程序

本页将介绍如何安装 QEMU，以便用于面向 QEMU 仿真器而非实体芯片的 [FreeRTOS 演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)。

**注意：**在撰写本文时，所有针对 QEMU 的演示项目都是在 Windows 主机上开发和测试的。

1. [下载并安装 QEMU](https://www.qemu.org/download/) - 请参阅[单独的下载页面](https://qemu.weilnetz.de/w64/)，
   获取预构建的 QEMU Windows 可执行文件。

2. 按照相关[演示特定文档页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)上的说明构建演示应用程序，
   并记下生成的可执行文件的名称。本页其余部分假设可执行文件名为 RTOSDemo.elf。

3. 使用以下命令启动 QEMU：

   ```c
   qemu-system-<TARGET_ARCHITECTURE> -kernel <PATH_TO>/RTOSDemo.elf -S -s -machine <TARGET_MACHINE>
   ```

   - 将 _\<TARGET_ARCHITECTURE\>_ 替换为目标架构，例如：

     **qemu-system-arm** ----> 适用于 [ARM CPU](https://www.qemu.org/docs/master/system/target-arm.html)。

     **qemu-system-riscv32** ----> 适用于 RISC-V CPU。

   - 将 _\<PATH_TO\>_ 替换为 FreeRTOS 映像的实际路径，上述示例中假定为 RTOSDemo.elf。

   - 将 _\<TARGET_MACHINE\>_ 替换为 QEMU 定义的目标芯片名称。使用 "_-machine help_" 命令列出 QEMU 支持的芯片。例如：

     ```c
     qemu-system-riscv32 -machine help
     ```

     输出结果如下：

     ![](/media/2020/Screen-Shot-2020-08-19-at-3.17.55-PM.png)

     检查由 QEMU 定义的 CPU 名称

4. 运行后，QEMU 将显示如下所示的窗口。让该窗口处于开启状态。此时 QEMU 正在等待 GDB 连接。
   有关启动调试会话的信息，请返回演示特定的文档页面。**注意：**每次重建
   RTOS 可执行文件时都需要重启 QEMU。

   ![](/media/2020/Screen-Shot-2020-08-19-at-3.43.19-PM.png)
   QEMU 仿真器
