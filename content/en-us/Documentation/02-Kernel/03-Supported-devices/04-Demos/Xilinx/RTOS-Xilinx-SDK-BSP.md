---
title: "A FreeRTOS BSP for the Xilinx SDK"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

## Introduction

The Xilinx Software Development Kit [(SDK)](https://www.xilinx.com/products/design-tools/embedded-software/sdk.html)
can automatically generate a board support package from a hardware definition file. The board support 
package provides comprehensive run time, processor and peripheral support. It is also possible for the 
BSP to include the FreeRTOS real time operating system.

Including FreeRTOS in the BSP presents the application writer with a pre-configured FreeRTOS environment 
that does not require any source files to be added manually, any callback functions to be provided by
the application code, and allows FreeRTOSConfig.h to be edited within the IDE.

Instructions for creating a FreeRTOS BSP are provided below. The FreeRTOS download also includes separate 
and comprehensive demo applications for 
the [Xilinx Zynq](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq) dual 
core ARM Cortex-A9 processor, 
an [ARM Cortex-A53 core on the UltraScale+ MPSoC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-UltraScale_MPSoC_64-bit) (AArch64, 64-bit), 
an [ARM Cortex-R5 core on the UltraScale+ MPSoC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-ARM-Cortex-R5-Xilinx-UltraScale_MPSoC) (32-bit), 
and [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Microblaze-KC705)
soft-core processors. Those comprehensive demo applications, as provided in the FreeRTOS download, 
use a standalone BSP. A standalone BSP does not itself include FreeRTOS, so FreeRTOS is instead built 
as part of the application. It is still important to read the documentation pages for those standalone 
demos, even when a FreeRTOS BSP is being used, as the pages provide information on how to use FreeRTOS 
on those ARM and Xilinx architectures.

---

## Instructions

### Creating a Hello World Project That Uses the FreeRTOS BSP

The board support package (BSP) repositories that ship as part of the Xilinx SDK come with a simple 
FreeRTOS hello world application. The hello world project is created as follows:

1. Select "New: Application Project" from the SDK's "File" menu to bring up
   the new project Window, then give the project a name.

   ![New RTOS BSP project](/media/2018/new_sdk_rtos_bsp_project.png)   
   *The "New: Application Project" menu option*

2. In the new project window - first select the hardware platform in use. Pre-defined hardware platforms 
   are provided for all the processors supported by FreeRTOS (Zynq ARM Cortex-A9, UltraScale+ ARM Cortex-A53 
   and ARM Cortex-A9 cores, and Microblaze). The image below shows the pre-configured ZC702 platform 
   being used.

3. After the hardware platform has been selected, select the processor. The image below shows the 
   ps7\_cortexa9\_0 processor selected.

4. After the processor has been selected, select the OS Platform. The image below shows freertos822 
   selected.

   ![creating the RTOS application](/media/2018/creating_the_rtos_bsp_project.png)   
   *Defining the project settings*

5. Click the "Next" button to move onto the next stage. The Templates Window will appear - select 
   the "FreeRTOS Hello World" template, then click the "Finish" button to generate both the FreeRTOS 
   BSP and the Hello World project.

   ![Selecting the RTOS hello world template](/media/2018/RTOS_BSP_Hello_World.png)   
   *Selecting the FreeRTOS Hello World template*

### Editing the FreeRTOS Configuration

A FreeRTOSConfig.h file was automatically created when the FreeRTOS BSP was generated. The values contained 
in the file can be viewed, and edited, using the following procedure:

1. Select "Board Support Package Settings" from the "Xilinx Tools" menu in the SDK. The Board Support 
   Package Settings window will appear.

2. Select FreeRTOS in the left pane of the Board Support Package Settings window. The table in the right 
   pane will populate with the FreeRTOSConfig.h settings.

3. Edit the settings as necessary, then click the "Ok" button to update FreeRTOSConfig.h with the edited 
   values, and re-build the BSP.

   [![Editing the RTOS settings](/media/2018/editing_the_rtos_settings.png)](/media/2018/editing_the_rtos_settings.png)   
   *The Board Support Package Settings window*

### Starting a Debug Session

It is therefore necessary to ensure the SDK launch configurations used to start a debug session resets 
the entire CPU, and runs the necessary initialisation scripts. A debug configuration suitable for running 
the Zynq demo is shown in the image below.

![](/media/2018/Zynq_target_setup_tab.jpg)

