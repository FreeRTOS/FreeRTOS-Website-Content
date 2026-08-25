---
title: QEMU-emulated ARM Cortex-M3 on MPS2 (AN385) Quick Connect Demo
---
by FreeRTOS

The FreeRTOS team has created a Quick Connect demo using a QEMU-emulated ARM Cortex-M3 on MPS2 (AN385). This demo uses AWS services to take care of the AWS account creation and AWS IoT configuration required to connect your emulated device to [AWS IoT](https://aws.amazon.com/iot/). Once connected, messages containing alternating 1's and 0's are sent, allowing you to simulate AWS IoT applications.


### To begin the Quick Connect demo:

**Step 1:** [Download QEMU](https://www.qemu.org/download) and include the `qemu-system-arm` emulator in your shell's path. To check your path, run: "`which qemu-system-arm`" which should produce a valid path.  

 **Linux**: depending on your Linux distro, you maybe able to get QEMU through your system's package manager. If you are on Ubuntu, run "`sudo apt install qemu-system`".  

 **Mac**: You can get QEMU through Homebrew. If it's not already installed, install [Homebrew](https://brew.sh/), then run "`brew install qemu`".  

 **Windows**:In a powershell, run the command "`winget install qemu`". (If you do not already have winget on your machine, follow [these instructions.](https://learn.microsoft.com/en-us/windows/package-manager/winget/#install-winget)) Next, ensure that you have added QEMU to your PATH. You can add the directory to your PATH by going to settings and searching for "Edit the system environment variables". Then, click on the "Environment variables" button in the bottom right corner and double click on the variable named "Path". Finally, click "New" and add the qemu directory (it should be located in program files) to your PATH.  

**Step 2:** To set up the QEMU emulated board, download the Quick Connect setup package for the computer you will use.  

 For Windows: Download [Quick\_Connect\_QEMU-windows.x64.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-windows.x64.zip)  

 For Apple Silicon Macs: Download [Quick\_Connect\_QEMU-macos(Arm).x64.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-macos(Arm).x64.zip)  

 For Intel Macs: Download [Quick\_Connect\_QEMU-macos(Intel).x64.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-macos(Intel).x64.zip)  

 For Linux: Download [Quick\_Connect\_QEMU-linux.x64.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-linux.x64.zip)  

**Step 3:** Unzip the Quick Connect archive. Then, in a terminal, go to the folder which was created (where the archive was decompressed), then directly invoke the file "Start\_Quick\_Connect" (run: "`./Start_Quick_Connect`").  

 **Note**: If you receive warnings while trying to run the application, see the troubleshooting section below.   

**Step 4:** Follow and complete all of the prompts in the command line interface.

**Step 5:** When "Start\_Quick\_Connect" is complete, a file called "CLICK-ME.html" will be created in the same directory. Double-click "CLICK-ME.html" to open a custom URL where you can visualize data from the sensors on your emulated ARM CM3 board.
  **Note:** Please ignore the "Add a sensor graph" section in the URL that you open, and use the instructions below.   

### To update the Quick Connect demo:


**Step 1:** Download [QEMU](https://www.qemu.org/download) and include the `qemu-system-arm` emulator in your shell's path. Then run "`which qemu-system-arm`" to make sure that produces a valid path.  

 **Note**: follow the instructions in Step 1 of the previous section to get QEMU on your system.  

**Step 2:** Download the [ARM GNU embedded toolchain](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads) and include the ARM compiler `arm-none-eabi-gcc` in your shell's path. Run "`which arm-none-eabi-gcc`" to make sure that produces a valid path.
  **Note**: This step is the most difficult as the most up-to-date version of the ARM GNU embedded toolchain is currently not in any package management system. What you will need to do in your system is download the embedded toolchain (arm-none-eabi), extract the archive to a directory of your choice, and add that directory to your system's path. To do this on MacOS/Linux, add "`export PATH=$PATH:<ARM toolchain directory>`" to the profile of your shell (usually this is `~/.bashrc` or `~/.zshrc` but it depends on your own system customization), and then run "`source <profile path>`".  

 To do this on Windows, see the instructions in Step 1 of the previous section for adding QEMU to your path, and follow the same steps to add this directory to your system's path.  

**Step 3:** Download [the demo source code](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-source.zip). The source archive contains the binary source (device code). 


**Step 4:** Download [the FreeRTOS repository](https://github.com/FreeRTOS/FreeRTOS/releases), and extract the archive. Move the downloaded source archive (from the previous step) into the FreeRTOS-Plus/Demo folder, and extract the archive. 


**Step 5:** Go into the extracted demo folder and follow the instructions in the "README.md" file there to customize the demo. After you are done customizing, rebuild the demo using the instructions in the "README.md" for the demo 


**Step 6:** Copy the generated executable (QuickConnect-Demo) from "Quick\_Connect\_QEMU-source/build" into "Quick\_Connect\_QEMU-platformName.x64/Demo", replacing the binary that is currently in the demo folder. 


**Step 7:** Rerun the file "Start\_Quick\_Connect" by directly invoking it through a terminal to see your changes. 

Specifications


QEMU is a generic and open source machine emulator and virtualizer. This demo uses QEMU to emulate an ARM Cortex-M3 MPU on a MPS2 using AN385.


**Hardware Architecture**
ARM (Cortex-M3)

**Network Connectivity**
Ethernet only

**Mounting / Form Factor**
Emulated

**Operating System**
FreeRTOS

**Programming Language**
C/C++

### Troubleshooting:

**Permission issues while running the application:**  

**Mac:** After double-clicking the Quick Connect executable, depending on your security settings, you may see a pop up window that says "Start\_Quick\_Connect cannot be opened because it is from an unidentified developer". Right click on the Start\_Quick\_Connect file in the Finder app and select the "Open" option. Then click on the "Open" button in the popup that shows up.  

**Windows:** After double-clicking the Quick Connect executable, depending on your security settings, you may see a pop-up page that says "Windows protected your PC". Click on the "More Info" link to see a "Run Anyway" button. Click on the "Run Anyway" button.

**Antivirus issues:**  
You might run into issues where your antivirus software thinks the `Start_Quick_Connect` executable is malware. This may be because the demo writes to a configuration file in the `Demo` folder; if your demo is quarantined because of your antivirus software, please mark the demo as trusted or disable antivirus for the duration of the demo.  
