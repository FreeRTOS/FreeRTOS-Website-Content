---
title: "FreeRTOS on the Intel® Galileo (x86 Quark™ SoC X1000)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Intel Galileo Gen 2 Single Board Computer](/media/2018/intel_galileo_gen_2.jpg)

### Introduction

[![FreeRTOS kernel aware RTOS plug-in](/media/2018/Galileo_state_viewer.png)](/media/2018/Galileo_state_viewer.png)

**The FreeRTOS Eclipse plug-in showing

 the state of tasks running on the Galileo

 Quark X1000 SoC. Click to enlarge.**

This page documents an RTOS demo application that uses the FreeRTOS IA32 (x86)
flat memory model port, and is pre-configured to run on the [Galileo Gen 2 single board computer](https://software.intel.com/iot/hardware/galileo),
which uses an
[Intel Quark SoC X1000](http://www.intel.co.uk/content/www/uk/en/intelligent-systems/quark/quark-x1000-overview.html)
 (x86/IA32) CPU.

The FreeRTOS IA32 port implements a full interrupt nesting model, utilises a separate
system stack to save RAM, and never globally
disables interrupts (although the hardware itself disables interrupts on interrupt entry).

---

### *IMPORTANT! Notes on using the FreeRTOS Intel Quark SoC demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The RTOS Demo Application](#functionality)
3. [Build Instructions](#build-instructions)
4. [Running the RTOS Demo on the Galileo Gen 2 Board](#creating-the-initial-bootable-sd-card)
	* [Creating the initial bootable SD card](#creating-the-initial-bootable-sd-card)
	* [Using the SD card to boot FreeRTOS](#using-the-sd-card-to-boot-freertos)
	* [Updating the RTOS executable using SCP](#updating-the-rtos-executable-using-scp-across-the-network) (across the network)
5. Debugging the RTOS Demo on the Galileo Gen 2 Board
6. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)
	* [FreeRTOS Intel IA32 Port Specific Configuration](#freertos-intel-ia32-port-specific-configuration)
	* [Interrupt Service Routines](#interrupt-service-routines)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Source Code Organisation

Only a small subset of the files in the FreeRTOS .zip file download are
required by the Intel Quark SoC demo. The [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page describes
the structure of the FreeRTOS zip file download.

The Eclipse project used to build and debug the demo is located in the
FreeRTOS/Demo/IA32\_flat\_GCC\_Galileo\_Gen\_2
directory. Note the RTOS project includes files from elsewhere in the directory
structure, so the project may not build if the directory structure has been altered.

---

The Intel Quark SoC X1000### Demo Application

### Hardware and software set up

The RTOS demo uses the LED and UART built onto the Galileo hardware, so no
specific hardware setup is required.

The UART uses 115200 baud, no parity bits, and 8 data bits, and one stop bit.

### Functionality

The behaviour of the demo is dependent on the mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY
constant, which is declared at the top of main.c.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 1

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 then main() will
call main\_blinky().
main\_blinky() creates a very simple demo that creates two
[tasks](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview) and one [queue](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/),
as follows:
* **A 'queue send' task**

 The 'queue send' task sends the value 100 to the queue every 200 milliseconds.
* **A 'queue receive' task**

 The 'queue receive' task reads values from the queue, toggling an LED
 and writing the LED state to the UART, each time the value 100 is received.

If the simple blinky demo is functioning correctly then the LED will toggle every
200 milliseconds.

#### Functionality with mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY set to 0

If mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 then main() will
call main\_full(). main\_full() creates a comprehensive test and demo application
that demonstrates:
* Interrupt nesting
* Installing interrupts using both methods described in the
 [Interrupt Service Routines](#interrupt-service-routines)
 section below.
* [Direct to Task Notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications).
* [Software Timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers).
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/).
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/).
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/).
* [Event Groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups).
* [Queue Sets](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets).

Most of the RTOS tasks created by the demo are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. These are used by all FreeRTOS demo applications, and
have no specific functionality or purpose other than to demonstrate the FreeRTOS
API being used, and test the RTOS kernel port.

Included in the full demo is a 'check' task. The check task periodically
monitors all the other tasks in the demo before toggling an LED and printing a
status code to the UART. If the LED toggles every five seconds, and the printed
status code is 0, then the check task has not detected any unexpected behaviour.
If the LED toggles every second, then the check task has detected
unexpected behaviour, and the source of the potential error is latched in the
status code value - the meaning of the status code can be determined by inspecting
the implementation of prvCheckTask() within the main\_full.c source file.

---

### Build Instructions

The Eclipse project [uses both virtual folders and links](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse) that reference files from elsewhere within
the FreeRTOS directory structure. The [virtual] file structure viewed in the
Eclipse project explorer will not match the [actual] file structure
viewed on the disk.

Note the demo was developed and tested on a Windows host. Any issues building the
demo on a Linux host will most likely to be related to the case of letters used
in include file names, or include paths.
[Please report](/Why-FreeRTOS/Support-options) any
such errors so they can be corrected.

To build the RTOS demo application:

1. If not already installed, download and install the [Eclipse CDT](https://eclipse.org/cdt/)
 distribution.
2. If not already installed, download and install an x86 GCC elf compiler.
 The project was developed using, and is pre-configured to use, the
 [pre-built i686-elf-gcc GCC tool chain](http://wiki.osdev.org/GCC_Cross-Compiler#Prebuilt_Toolchains)
 referenced from the osdev.org website.

**NOTE:** It has been discovered that the above
 referenced compiler has dependencies on DLLs that are not part of the
 compiler package. The simplest way around this is to also
 [install the
 MingW](http://sourceforge.net/projects/mingw/files/latest/download) compiler, and ensure the MingW bin directory is also in your path,
 as that comes with the necessary dll files. If anybody is aware of an
 elf compiler that doesn't have this external dependency then please
 [let us know](/Why-FreeRTOS/Support-options).

 COFF compilers (such and MingW), can also be used to build the example,
 but will probably require
 adjustments to the project settings, and will not offer such a good
 debugging experience.
3. Ideally, ensure the path to the compiler's bin directory is included in the Windows
 PATH environment variable. It is also possible to set the path within the
 Eclipse project itself - this is described later.
4. If your host system does not provide an implementation of the 'rm' (remove files)
 command, then it may be necessary to provide or install one in order to perform a
 'build clean' operation. The [UnxUtils](http://sourceforge.net/projects/unxutils/)
 package provides a pre-built version suitable for use on Windows. Ensure
 the 'rm' executable is also located in a path that is included in the
 Windows PATH environment variable.
5. Open the Eclipse IDE and either create a new workspace or select an existing
 workspace when prompted.
6. Select "Import" from the IDE's "File" menu to bring up the import
 dialogue box.
7. In the Import dialogue box, select "General->Existing Projects Into Workspace"
 then browse to and select the FreeRTOS/Demo/IA32\_flat\_GCC\_Galileo\_Gen\_2
 directory. A project called "RTOSDemo" will be visible.
8. Ensure RTOSDemo is checked, and that Copy Projects Into Workspace is
 not checked, before clicking "Finish".

![Importing the Intel Quark IA32 RTOS demo project into an Eclipse workspace](/media/2018/importing_intel_galileo_free_rtos_project.png)

**Import RTOSDemo into the Eclipse workspace without
 copying it into the workspace.**
9. If you are using a GCC compiler other than the i686-elf-gcc distribution,
 or you need to set the path to the compiler,
 then you can update the Eclipse project's 'cross compiler' settings as
 follows:

 Select "Properties" from the IDE's "Project" menu to bring up the
 properties dialogue box. In the dialogue box select "C/C++Build->Settings->Cross Settings",
 then set the name, and if necessary the path, to the
 compiler that will be used.

![Setting the path to the compiler that builds the Intel Quark RTOS demo](/media/2018/setting_intel_quark_rtos_compiler.png)

**Setting the path to the compiler in the RTOS project's properties dialogue box**
10. Open main.c and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the simple blinky demo, or the full test and demo application, as
 required.
11. Select "Build All" from the IDE's "Project" menu. The project should build
 with no errors - see the build troubleshooting tips below if this is not the
 case.

Build trouble shooting tips:

* The GCC compiler should automatically locate the standard library header
 files, in which case the path to the header files will be displayed in
 the project options as shown in the images below. Click the images to
 enlarge:

|  |  |
| --- | --- |
| [![cross compiler options for Intel Quark project](/media/2018/Intel_cross_settings_0.png)](/media/2018/Intel_cross_settings_0.png) | [![GCC compiler options for Intel Quark project](/media/2018/Intel_cross_settings_1.png)](/media/2018/Intel_cross_settings_0.png) |
| <br/><br/>**Project options that should get set automatically** <br/><br/> |

 If you receive errors such as "Symbol NULL could not be resolved" or
 "Type size\_t could not be resolved" then it is likely you will have to
 set the path to the header files manually in the project options.
* It has been reported that build errors can occur if Eclipse is not running
 with administrator rights.

Running the RTOS Demo on the Galileo Gen 2### Board

The RTOS demo executable can be booted on the Galileo board from an SD card.
A multi-boot GRUB image is used for this purpose. The GRUB configuration enables the Galileo to
boot into either FreeRTOS, or Linux. Booting into Linux allows the RTOS demo
executable to be updated over the network.

Full instructions for creating the GRUB image are provided
[in the pdf file provided on this link](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Boot_Instructions.pdf/download). For
simplicity,
[a pre-built SD card image is also provided on this link](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Multiboot_GRUB_SD_Card_Image.7z/download).
Brief instructions on using the pre-built SD card image are provided below.
Refer to the pdf file for full instructions.

It may be necessary to update the Galileo firmware before proceeding -
instructions for updating the firmware are provided in the same pdf file.

The SD card must be formatted as FAT or FAT32, be 32G bytes or smaller, and SDHC
format. SDXC format is not supported.

### Creating the initial bootable SD card

To create the initial bootable SD card from a Windows host:
1. Open a command prompt (cmd.exe) as an administrator.
2. Run diskpart.exe in the command prompt to start the diskpart utility.
3. Enter the following diskpart commands:
	* select volume n       [where 'n' is the drive
	 letter assigned to the SD card by windows. For example, if the SD card
	 was drive z, then you would enter 'select volume z'.]
	* clean
	* create part primary
	* active
	* format quick label="BOOTME"
	* exit
4. Unzip the [pre-build SD image](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Multiboot_GRUB_SD_Card_Image.7z/download)
 into the root of the partitioned and
 formatted SD card, such that the root of the SD card contains the boot
 folder, and the bzImage (and other) file.
5. Copy the RTOSDemo.elf file created when the RTOS demo was built into the
 /kernel directory on the SD card.

### Using the SD card to boot FreeRTOS

To boot FreeRTOS from the SD card:
1. Connect the Galileo to a host computer running a dumb terminal program
 (such as Tera Term) using a suitable serial cable. The connection uses
 115200 baud, no parity, 8 data bits and no stop bits.
2. After following the instructions above to create the SD card, insert the
 SD card into the slot on Galileo Gen 2 hardware.
3. Reset the Galileo board.
4. The boot options menu will be displayed in the dumb terminal. Select "Multiboot
 GRUB", or simply let the menu time out as Multiboot GRUB is the default selection.

![RTOS on Intel x86 boot options](/media/2018/Intel_Galileo_RTOS_boot_options.jpg)

**The boot options menu**
5. The Multiboot GRUB menu will then be displayed in the terminal. Select "FreeRTOS Demonstration",
 or simply let the menu time out as FreeRTOS Demonstration is the default selection.
 The RTOS demo will start to execute.

![Using GRUB to boot the free RTOS on the Galileo hardware](/media/2018/galileo_multiboot_grub_menu.jpg)

**The multiboot GRUB menu**

### Updating the RTOS executable using SCP (across the network)

Subsequent updates to the RTOS demo elf file can be copied onto the SD card by booting
the Galileo into Linux, then using WinSCP. As supplied, the SD card used to boot FreeRTOS
on the Galileo board will use the 192.168.0.10
IP address, so the host computer will need to have a compatible IP address on the same local
network.

To update the RTOS demo elf file using SCP:

1. If not already installed, download and install [WinSCP](https://winscp.net/eng/index.php),
 or other compatible SCP client.
2. Reboot the Intel Galileo hardware, this time use the multiboot GRUB menu
 to select "Clanton SVP kernel", which will boot Linux instead of FreeRTOS.
3. Wait for Linux to boot, entering "root" as the username and "intel" as the
 password when prompted.
4. Ensure the Galileo board is connected to the same network as the host
 computer before starting WinSCP.
5. Create then connect a WinSCP session using the settings shown in the image below.
 The password is 'intel'.

![Using WinSCP to copy the Intel RTOS image](/media/2018/using_winscp_to_copy_intel_rtos_image.png)

**The necessary WinSCP session settings**
6. Once WinSCP has connected, copy the new RTOS demo elf file into the "/media/realroot/kernel"
 directory, as shown in the image below.

![Updating the Intel RTOS image using WinSCP](/media/2018/Updating_RTOS_image_for_quark.jpg)

**The directory into which updated FreeRTOS images must be copied**
7. Enter "reboot" in the Linux command console. That will ensure the updated
 elf file is committed to the SD card before rebooting the Galileo into FreeRTOS.

Debugging the RTOS Demo on the Galileo Gen 2### Board

Eclipse, OpenOCD and GDB can be used to download, run, and debug updated executables, without
needing to reboot the hardware. A JTAG debug interface is required. The demo was created and tested using an
[ARM-USB-OCD-H](https://www.olimex.com/Products/ARM/JTAG/ARM-USB-OCD-H/)
pod from Olimex, with an [ARM-JTAG-20-10](https://www.olimex.com/Products/ARM/JTAG/ARM-JTAG-20-10/)
adapter.

These instructions download an image to RAM only, so the updated image will
not be persistent, and will not be available after the Galileo has been reset.

To download a new RTOS demo executable to RAM, then start a debug session:

1. If not already installed, download and install [OpenOCD](http://openocd.org/).
2. Connect the Galileo Gen 2 evaluation board to the host computer using a
 suitable FTDI based JTAG adapter.
3. Open a command console, navigate to the directory in which openocd.exe
 was installed, and execute the following command to start OpenOCD with
 the required configuration. Note the command should be entered on a
 single line, and assumes the ARM-USB-OCD-H interface is being used.

```c

openocd.exe -f ..scriptsinterfaceftdiolimex-arm-usb-ocd-h.cfg
                                         -f ..scriptsboardquark_x10xx_board.cfg
```
4. Boot the Galileo into FreeRTOS, as described above.
5. In Eclipse, use the "Run->Debug Configurations..." menu item to create
 a new debug configuration, as shown in the images below.
 **Click the images to enlarge**

[![Debugging the free Intel RTOS step 1](/media/2018/galileo_rtos_debug_configuration_1.jpg)](/media/2018/galileo_rtos_debug_configuration_1.jpg)

**Creating a debug configuration - step 1**

[![Debugging the free Intel RTOS step 2](/media/2018/galileo_rtos_debug_configuration_2.jpg)](/media/2018/galileo_rtos_debug_configuration_2.jpg)

**Creating a debug configuration - step 2**

[![Debugging the free Intel RTOS step 3](/media/2018/galileo_rtos_debug_configuration_3.jpg)](/media/2018/galileo_rtos_debug_configuration_3.jpg)

**Creating a debug configuration - step 3.
Options that are
 not visible in the image are left empty**
6. Click "Debug" to connect to the Galileo using GDB. See the debug troubleshooting
 tips below.
7. Multiple consoles are available within the Eclipse IDE. Select the GDB console
 as shown below:

![Debugging the free Intel RTOS step 3](/media/2018/selecting_the_gdb_console.jpg)

**Selecting the GDB console in Eclipse**
8. In the GDB console, enter the following commands, replacing [enter path]
 with the correct path to the RTOS demo elf file for your installation.
 See the debug troubleshooting tips below. The following commands can be
 added to a script for simplicity.

```c

monitor reg eflags 0x0
flushregs
echo Downloading elf file.  Please wait.
monitor load_image C:[enter path]/RTOSDemo.elf 0
symbol-file C:[enter path]/RTOSDemo.elf
set $eip=_restart
c
```

 The RTOS demo elf file should download to RAM, which takes some time,
 and then start executing.

Debug trouble shooting tips:

* If the correct source line, or assembly code line, is not displayed when
 a debug session is first started, then try a single stepping operation in
 the debugger. Sometimes that will result in a refresh, and then the
 correct code will be shown.
* Keep an eye on the console window in which OpenOCD is running. If it
 starts to show "invalid memory" errors then it may be necessary to reset
 everything, and restart OpenOCD.
* If you are developing by downloading images to RAM, and you want to have
 the debugger stop on entry to main, then add "b main" (breakpoint at
 main) command before the "c" (continue) command in step 8 of the instructions
 above.
* If you are developing by copying new RTOS images to the SD card, then
 rebooting the Galileo, and you want the debugger to stop on entry to main,
 then set the #define mainWAIT\_FOR\_DEBUG\_CONNECTION to 1 at the top of the
 main.c source file. That will cause the application to sit in a loop
 at the top of main(), giving you the opportunity to connect the debugger
 before the application starts executing properly. Once the debugger is
 connected it can be used to change the value of ulExitResetSpinLoop to
 any non-zero value, and in so doing, exit the loop. The loop can also be
 exited by pressing a key in the console.

---

### RTOS Configuration and Usage Details

#### FreeRTOS Intel IA32 run-time model

The FreeRTOS IA32 (x86) port uses a flat 32-bit memory space, [currently] runs
all tasks with full privileges, and does not use the MMU.

#### FreeRTOS Intel IA32 port specific configuration

Configuration items specific to this demo are contained in FreeRTOS/Demo/IA32\_flat\_GCC\_Galileo\_Gen\_2/FreeRTOSConfig.h.
The constants defined in this file can be edited to suit your application.

The following Intel IA32 target specific constants are required in addition to the
standard [FreeRTOS configuration constants](/Documentation/02-Kernel/03-Supported-devices/02-Customization):

* **configISR\_STACK\_SIZE**

 FreeRTOS will switch the stack in use to a dedicated interrupt/system
 stack on interrupt entry. configISR\_STACK\_SIZE defines the number of
 32-bit values that can be stored on the system stack, and must be large
 enough to hold a potentially nested interrupt stack frame.

 Using a separate system stack means the stacks allocated to tasks can all
 be smaller, as they do not each need to include space for a nested interrupt
 stack frame.

Changing this parameter necessitates a complete clean and rebuild
 to ensure the assembly files are also re-built.
* **configSUPPORT\_FPU**

 If configSUPPORT\_FPU is set to 1 then tasks can opt to have a floating
 point context (the floating point registers will be saved as part of
 the task context).

 Tasks are not created with an FPU context and must not use any FPU instructions
 until after they have called vPortTaskUsesFPU().

```c

void vPortTaskUsesFPU( void );

vPortTaskUsesFPU() function prototype
```

 If configSUPPORT\_FPU is set to 0 then floating point instructions must
 never be used.

Changing this parameter necessitates a complete clean and rebuild
 to ensure the assembly files are also re-built.
* **configUSE\_COMMON\_INTERRUPT\_ENTRY\_POINT**

 If configUSE\_COMMON\_INTERRUPT\_ENTRY\_POINT is set to 0 then all
 interrupt service routines need a short assembly code entry point.
 The assembly code wraps the interrupt handler in the FreeRTOS
 portFREERTOS\_INTERRUPT\_ENTRY and portFREERTOS\_INTERRUPT\_EXIT macros, which handle interrupt
 entry and exit respectively. See
 the [Interrupt Service Routines](#interrupt-service-routines) section for an example.

 If configUSE\_COMMON\_INTERRUPT\_ENTRY\_POINT is set to 1, then interrupt
 service routines can also be written as standard C functions, in which
 case interrupt entry and exit is handled by common code within the
 FreeRTOS port layer. See the [Interrupt Service Routines](#interrupt-service-routines)
 section for an example.

 Writing an interrupt handler that provides its own assembly file
 wrapper is slightly more complex than using the common interrupt
 entry point, but interrupt entry will be faster and always deterministic.

* **configMAX\_API\_CALL\_INTERRUPT\_PRIORITY**

 The FreeRTOS Quark port implements a full interrupt nesting model.

 Interrupts that are assigned a priority at or below
 configMAX\_API\_CALL\_INTERRUPT\_PRIORITY can call interrupt safe API functions
 and will nest.

 Interrupts that are assigned a priority above
 configMAX\_API\_CALL\_INTERRUPT\_PRIORITY cannot call any FreeRTOS API functions,
 will nest, and will not be masked by FreeRTOS critical sections (although all
 interrupts are briefly masked by the hardware itself on interrupt entry).

 FreeRTOS functions that can be called from an interrupt are those that end in
 "FromISR". FreeRTOS maintains a separate interrupt safe API to enable
 interrupt entry to be shorter and faster, and to enable all API functions to be
 simpler and smaller.

 User definable interrupt priorities range from 2 (the lowest) to 15 (the
 highest).

#### Interrupt Service Routines

Interrupt service routines (ISRs) can be written in two different ways, as follows:
1. As standard C functions

 This method can only be used if configUSE\_COMMON\_INTERRUPT\_ENTRY\_POINT
 is set to 1. The interrupt handler must be installed using the
 xPortRegisterCInterruptHandler() function.

```c

/*

 * pxHandler: Pointer to the function that implements the ISR.

 * ulVectorNumber: The interrupt vector number to which the ISR will be

 * assigned. Vector numbers can be between 34 (in the

 * lowest priority group) and 255 (in the highest priority

 * group).

 */

BaseType_t xPortRegisterCInterruptHandler( ISR_Handler_t pxHandler,

                                           uint32_t ulVectorNumber );

The xPortRegisterCInterruptHandler() function prototype
```

 This is the simplest of the two methods, but incurs a slightly longer
 interrupt entry time. Interrupts are enabled before the ISR (the C function)
 is called.

 The example below is a cut-down version of an interrupt used in the
 RTOS demo project.

```c

/* The function that implements the ISR is a standard C function. */

static void vHPETIRQHandler0( void )

{

    /* Perform ISR processing here. */

    /* Clear the interrupt in the IP API. It is not necessary to

 clear the interrupt in the local API - that is done by FreeRTOS. */

    hpetIO_APIC_EOI = hpetHPET_TIMER0_ISR_VECTOR;

}

/*-----------------------------------------------------------*/

/* The C function is then installed as the handler for vector 100 using the

following code. */

xPortRegisterCInterruptHandler( vHPETIRQHandler0, 100 );

Implementing an ISR as a standard C function
```
2. As standard C functions that are called from an assembly code entry point

 The assembly code wraps the interrupt handler in the FreeRTOS
 provided portFREERTOS\_INTERRUPT\_ENTRY and portFREERTOS\_INTERRUPT\_EXIT macros. The
 interrupt handler must be installed using the xPortInstallInterruptHandler()
 function.

```c

/*

 * pxHandler: Pointer to the assembly code stub that wraps the ISR.

 * ulVectorNumber: The interrupt vector number to which the ISR will be

 * assigned. Vector numbers can be between 34 (in the

 * lowest priority group) and 255 (in the highest priority

 * group).

 */

BaseType_t xPortInstallInterruptHandler( ISR_Handler_t pxHandler,

                                         uint32_t ulVectorNumber );

The xPortInstallInterruptHandler() function prototype
```

 This method can always be used. It is slightly more complex than
 method 1, but benefits from a faster and deterministic interrupt entry time.
 The application writer can re-enable interrupt before calling the C portion
 of the ISR if desired.

 The example below is a cut-down version of an interrupt used in the RTOS
 demo project.

```c

/* The function that implements the C portion of the ISR. This is the

function called from the assembly code wrapper. */

void vHPETIRQHandler1( void )

{

    /* Perform ISR processing here. */

    /* Clear the interrupt in the IP API. It is not necessary to clear the

 interrupt in the local API - that is done by FreeRTOS. */

    hpetIO_APIC_EOI = hpetHPET_TIMER1_ISR_VECTOR;

}

/*-----------------------------------------------------------*/

/* The assembly code wrapper that calls the C function shown immediately

above. **The wrapper must be implemented in an assembly file, not a C file.**

The interrupt entry point assembly code makes use of the

portFREERTOS\_INTERRUPT\_ENTRY and portFREERTOS\_INTERRUPT\_EXIT macros,

so ISR\_Support.h must be included. ISR\_Support.h is located in the

FreeRTOS/source/portable/GCC/IA32\_flat directory. */

#include "ISR_Support.h"

.align 4

.func vApplicationHPETTimer1Wrapper

.extern vHPETIRQHandler1

vApplicationHPETTimer1Wrapper:

    /* FreeRTOS macro that handles interrupt entry. Must be called

 first. */

    portFREERTOS_INTERRUPT_ENTRY

    /* It is safe to enable interrupts here, if desired. */

    sti

    /* The rest of the ISR is implemented in C. Call the C function

 now. */

    call vHPETIRQHandler1

    /* FreeRTOS macro that handles interrupt exit. Must be called

 last. */

    portFREERTOS_INTERRUPT_EXIT

.endfunc

/*-----------------------------------------------------------*/

/* Finally, the assembly code wrapper is then installed as the handler

for vector 100 using the following code. This code must be in a C

file. */

extern void vApplicationHPETTimer1Wrapper( void );

xPortInstallInterruptHandler( vApplicationHPETTimer1Wrapper, 100 );

The C function called from the assembly code wrapper
```

If an ISR causes an RTOS task of equal or higher priority than the currently executing
task to leave the Blocked state (see the description of the pxHigherPriorityTaskWoken
parameter in the API documentation for functions such as
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR))
then the ISR must request a context switch before
the ISR exits if it wants the unblocked task to execute immediately. When this
is done, the interrupt will interrupt one RTOS task, but return to a different
RTOS task.

The macro portYIELD\_FROM\_ISR() (or portEND\_SWITCHING\_ISR()) is used to
request a context switch from within an ISR.
The following source code snippet is provided as an example. The ISR in the example
uses a task notification to synchronise with a task (not shown), and calls portYIELD\_FROM\_ISR()
to ensure the interrupt returns directly to the unblocked task.

The application writer may choose not to call portYIELD\_FROM\_ISR() if
it is known that the interrupt did not necessitate any immediate processing - for
example, if the interrupt was a character arriving, but more characters are
needed before the message being received is complete and ready for processing.

```c

void Dummy_IRQHandler( void )

{

long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */

    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a

 task with an interrupt. A task notification is used for this purpose.

 Note lHigherPriorityTaskWoken is initialised to pdFALSE. */

    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskHandle, &lHigherPriorityTaskWoken );

    /* If the notified task was blocked waiting for the notification, and the

 unblocked task has a priority higher than or equal to the currently Running

 task (the task that this interrupt interrupted), then

 lHigherPriorityTaskWoken will have been set to pdTRUE internally within

 vTaskNotifyGiveFromISR(). Passing pdTRUE into the portYIELD\_FROM\_ISR() macro

 will result in a context switch being pended to ensure this interrupt returns

 directly to the unblocked, higher priority, task. Passing pdFALSE into

 portYIELD\_FROM\_ISR() has no effect. */

    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );

}

An example interrupt handler
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_API\_CALL\_INTERRUPT\_PRIORITY
configuration constant.

#### Resources used by FreeRTOS

FreeRTOS uses the local APIC timer, and interrupt vectors 0x20 and 0x21. In
addition, the demo project uses the UART, GPIO, Legacy GPIO, I2C and HPE timers.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the Intel IA32 demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
