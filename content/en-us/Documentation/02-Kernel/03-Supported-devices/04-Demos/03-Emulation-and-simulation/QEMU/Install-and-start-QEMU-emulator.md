---
title: "Installing and starting the QEMU emulator "
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### for use with FreeRTOS demos applications

This page describes how to install QEMU for use with [FreeRTOS demo applications](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) that target the QEMU emulator, rather than physical chips.

**Note:** At the time of writing all demo projects that target QEMU were developed and tested on Windows hosts.

1. [Download and install QEMU](https://www.qemu.org/download/) - there is [a separate download page](https://qemu.weilnetz.de/w64/)
   for pre-built QEMU Windows executables.

2. Build the demo application by following the instructions on the relevant [demo specific documentation page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos), and note the name of the
   resultant executable. The rest of this page assumes the executable is called RTOSDemo.elf.

3. Start QEMU using the following command:

   ```c
   qemu-system-<TARGET_ARCHITECTURE> -kernel <PATH_TO>/RTOSDemo.elf -S -s -machine <TARGET_MACHINE>
   ```

   - replacing _\<TARGET_ARCHITECTURE\>_ with your target's architecture, such as:

     **qemu-system-arm** ----> for [ARM CPUs](https://www.qemu.org/docs/master/system/target-arm.html).

     **qemu-system-riscv32** ----> for RISC-V CPUs.

   - replacing _\<PATH_TO\>_ with the real path to the FreeRTOS image, assumed to be RTOSDemo.elf in the above example.

   - replacing _\<TARGET_MACHINE\>_ with your target chip name as defined by QEMU. Use the "_-machine help_" command to list the chips supported by QEMU. For example:

     ```c
     qemu-system-riscv32 -machine help
     ```

     results in the following output:

     ![](/media/2020/Screen-Shot-2020-08-19-at-3.17.55-PM.png)

     Checking CPU name defined by QEMU

4. Once running, QEMU will display a window as shown below. Leave the window open. At this point QEMU is waiting for a GDB connection - return
   to the demo specific documentation page for information on starting a debug session. **Note:** It is necessary to restart QEMU each time the
   RTOS executable is rebuilt.

   ![](/media/2020/Screen-Shot-2020-08-19-at-3.43.19-PM.png)
   QEMU Emulator
