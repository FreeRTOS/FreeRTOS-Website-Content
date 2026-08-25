---
title: FreeRTOS FAQ - Ports
created: 2018-09-20
description: Information about FreeRTOS ports
---

## Will FreeRTOS run under Windows?

Yes, but not with true real time behaviour.

[Two FreeRTOS Windows simulator projects are provided in the main FreeRTOS download](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW).
The first uses the free express edition of Visual Studio, and the second uses the Free GCC/MingW and Eclipse tools.

The x86 port will run in a DOS emulation box and the ARM7 Keil port can be completely simulated under
windows (as can various other ports).

## Will FreeRTOS run on any Cortex -M port?

Everything required to run FreeRTOS on an Arm Cortex-M device is included in the
kernel port layer - so FreeRTOS runs on any Cortex-M3/4/4F/7/23/33/55/85 device.
There cannot be a demo for every device, so you may have to
[create a project yourself](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos).
Many MCU vendors provide FreeRTOS projects with their toolchains too.


## Are the NNN development tools supported?

Lots of different development tools are
supported. [Check the list of ports](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices).


## Is the NNN microcontroller supported?

Lots of different microcontrollers are
supported. [Check the list of ports](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices).


## How do I create a new port?

See the [FreeRTOS porting guide](/Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-porting-guide).


## What is the difference between an official port, and an unsupported port?

See the ['Officially Supported' and 'Contributed' FreeRTOS Code](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)
description.
