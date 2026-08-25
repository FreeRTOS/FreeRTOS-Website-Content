---
title: "Modifying a FreeRTOS Demo to use a different compiler or run on different hardware"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### What This Page is About

[See also "[Creating a new FreeRTOS project](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)"]

FreeRTOS already includes *many* demo applications - each of which is targeted at:

1. A specific microcontroller.
2. A specific development tool (compiler, debugger, etc.).
3. A specific hardware platform (prototyping or evaluation board).

These are documented under '[Supported Devices](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)' in the menu frame on the left.

Unfortunately it is not possible to provide a demo project for every combination of microcontroller, compiler and evaluation board - so it might be that a demo
application does not exist that matches your required setup exactly. This page documents how existing demo applications can be modified or combined to
better match the setup you require.

It is generally a simple task to take an existing demo for one evaluation board and modify it to run on another - and only slightly more complex to take a demo for one compiler
and modify it to use another. This page provides instruction on these and similar porting type activities. It is not so simple however to take a FreeRTOS
port and convert it to run on a completely different, and as yet unsupported, processor core architecture. This page does not therefore cover the topic of creating
completely new RTOS ports, also [a separate page is provided](/Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-porting-guide) that gives hints on
how such a development can be approached.

---

### Converting a Demo to Use a Different Evaluation Board

This subsection documents the steps required to convert an existing demo application from one prototyping board to another, without changing either the microcontroller
or compiler being used. As an example, these instructions would be used to convert the IAR SAM7S demo targeted at the SAM7S-EK hardware to instead target the
Olimex SAM7-P64 prototyping board.

Ensure each step is completed successfully prior to moving to the next:

1. **Initial compilation**:
 An existing demo application should be used as a starting point for the conversion exercise, therefore first check you can successfully compile
 the existing demo application exactly as downloaded - before making any modifications.
 In most cases the demo application should compile without any errors or warnings.

 This website contains a [documentation page for each demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) included in the FreeRTOS
 download. Please ensure to read this in full. Build instructions are included.

2. **Modifying the LED IO**:
 LEDs provide the easiest method of getting visual feedback that the demo application is running, so it is useful to get the LEDs on the new hardware
 platform working as soon as possible.

 It is unlikely that the hardware platform to which the demo is being ported has LEDs on the same IO ports as the hardware platform on which the
 demo was developed - so some minor modification will be required.

 The function vParTestInitialise() within partest.c contains the IO port mode and direction configuration.
 The function prvSetupHardware() within main.c contains more generic hardware configuration (for example, enabling the clock to the IO peripheral)
 and may also require some modification, depending on the port being used.

 Make any changes necessary to the two functions highlighted in the paragraph above, then write a very simple program to check that the LED outputs are working. This simple program
 need not make use of FreeRTOS - all that is of interest at this stage is ensuring the LEDs work - so for now comment out the existing main() function
 and replace it with something similar to the following example:

```c

    int main( void )
    {
    volatile unsigned long ul; /* volatile so it is not optimized away. */

        /* Initialise the LED outputs - note that prvSetupHardware() might also
 have to be called! */
        vParTestInitialise();

        /* Toggle the LEDs repeatedly. */
        for( ;; )
        {
            /* We don't want to use the RTOS features yet, so just use a very
 crude delay mechanism instead. */
            for( ul = 0; ul < 0xfffff; ul++ )
            {
            }

            /* Toggle the first four LEDs (on the assumption there are at least
 4 fitted. */
            vParTestToggleLED( 0 );
            vParTestToggleLED( 1 );
            vParTestToggleLED( 2 );
            vParTestToggleLED( 3 );
        }

        return 0;
    }
```
3. **Introducing the RTOS scheduler**:
 Once the LEDs are known to be working the dummy main() function can be removed, and the original main() function restored.

 It is advisable to start with the simplest multitasking application possible. The standard 'flash test' tasks are often used initially as
 a multitasking equivalent of a 'hello world' type application.

 The standard 'flash test' tasks are a set of 3 very simple tasks - each of which toggles a single LED at a fixed frequency, with each task using a different
 frequency. These tasks are included in nearly all the demo applications, and are started within main() by a call to the function
 vStartLEDFlashTasks() (or vStartFlashCoRoutines() should the co-routine version be used instead). If the main() function of the demo you are using does not
 call vStartLEDFlashTasks() (or alternatively vStartFlashCoRoutines()) then simply add the file FreeRTOS/Demo/Common/Minimal/Flash.c to your build and
 add the call to vStartLEDFlashTasks() manually.

 Comment out every function that is used to start one or more demo tasks, other than the call to vStartLEDFlashTasks(). It is likely that main() will then only call three
 functions: prvSetupHardware(), vStartLEDFlashTasks(), and vTaskStartScheduler(). For example ([based on the typical main()
 introduced earlier](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)):

```c

int main( void )
{
   /* Setup the microcontroller hardware for the demo. */
   prvSetupHardware();

   /* Leave this function. */
   vCreateFlashTasks();

   /* All other functions that create tasks are commented out.
   vCreatePollQTasks();
   vCreateComTestTasks();
   Etc.
   xTaskCreate( vCheckTask, "check", STACK\_SIZE, NULL, TASK\_PRIORITY, NULL );
   */

   /* Start the RTOS scheduler. */
   vTaskStartScheduler();

   /* Should never get here! */
   return 0;
}
```

 This very simple application is running correctly if LEDs 0 to 2 (inclusive) are under the control of the 'flash' tasks and each is toggling at a fixed but different frequency.

4. **Finishing off**:

 Once the simple flash demo is executing you can restore the full demo
 application with all the demo tasks being created, or alternatively, start
 to create your own application tasks.

 Points to keep in mind:

	* If the demo application did not originally have a call to vTaskCreateFlashTasks(), and a call to this function was added manually, then the call
	 should be removed again. This is for two reasons, first the flash tasks may use LED outputs that are already used elsewhere within the demo, and second the
	 full demo might already use all the available RAM, meaning there is no room for additional tasks to be created.
	* The standard 'com test' tasks (if included in the demo) will utilise one of the microcontrollers UART peripherals. Check that the UART used is valid for the
	 hardware onto which you have ported the demo.
	* It is unlikely that peripherals such as LCDs will function without modification to account for any hardware or interface differences.

---

### Combining or Modifying Existing Demo Projects

This subsection highlights the details that require consideration to either modify an existing project, or combine two existing project, both with the aim of creating a project
specific to your requirements. For example, you may wish to create an STR9 demo project that uses the GCC compiler. While the FreeRTOS download may not (at the time or writing)
include a GCC STR9 demo, it does include an IAR STR9 demo, and a GCC STR75x demo. The information required to create the STR9 GCC project can be gleaned from
these two existing project. There are two ways this can be done:

1. Take an existing demo project that uses the correct compiler but targets a different microcontroller, and re-target this to the required microcontroller.
2. Create a new project using your chosen compiler. When this option is taken an existing demo project can be used as a guide to which files and settings
 are required, even if the existing project uses a different compiler.

The following notes highlight the information that requires consideration whichever method is used:

* **Identifying the FreeRTOS kernel files that are specific to the microcontroller being used**:

 The [FreeRTOS source code organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page provides all the information that is required to understand
 the FreeRTOS directory structure.

 The majority (if not all) the code that is specific to a single port is contained in a file called FreeRTOS/source/portable/[compiler]/[microcontroller]/port.c
 and an accompanying header file called FreeRTOS/source/portable/[compiler]/[microcontroller]/portmacro.h,
 where [compiler] is the name of the compiler being used, and [microcontroller] is the name of the microcontroller family being used.

 For some compilers the port.c and portmacro.h files are all that is required. For others (those with less flexible features) an assembler
 file is also required. This will be called portasm.s or portasm.asm.

 Finally, and specific to ARM7 GCC ports only, there will also be a file called portISR.c. portISR.c is used to separate out from port.c
 that code which must always be compiled to ARM mode - the code that remains in port.c can then be compiled to either ARM or THUMB mode.
* **Identifying files that are specific to the compiler being used**:
 Compilers targeting embedded systems provide certain extensions to the C language. For example, a special keyword might exist that is used to identify
 that a particular function should be compiled as an interrupt handler.

 Extensions to the C language, by definition, fall outside of the C standard so differ from compiler to compiler. The FreeRTOS files that contain such non-standard
 syntax will be those within the FreeRTOS/source/portable directory tree (as highlighted above). In addition, some demo applications will install interrupt
 handlers that are not part of FreeRTOS itself. The definition of such interrupt handlers and the method of installing the interrupt handler might also be
 compiler specific.
* **Low level files**:
 The C startup file and linker script are generally processor and compiler specific. Never try to create these files from scratch - instead look through the
 existing FreeRTOS demo projects for a file that is a suitable candidate for modification.

 Take particular care with ARM7 C startup files. These must either configure the IRQ handler to vector directly to the interrupt handler or vector to a common entry
 point. Examples are provided of both methods. In either case the first code executed after the jump must be the FreeRTOS context save code, not any compiler provided
 intermediary code. Again - use the existing files as a reference.

 Linker scripts must be adjusted to correctly describe the memory map of the microcontroller being used.
* **Project settings**:

 Every project will normally define a preprocessor macro that is specific to the port being compiled. The preprocessor macro identifies which portmacro.h file
 will be included. For example, GCC\_MEGA\_AVR must be defined when using GCC to compile the MegaAVR port. IAR\_MEGA\_AVR must be defined when using IAR to compile
 the MegaAVR port, etc. Refer to existing demo application projects and the file FreeRTOS/source/include/portable.h to find the correct definition
 for your project. If the preprocessor macro is not defined then the directory in which the relevant portmacro.h file is located must be included in the
 preprocessors include search path.

 Other compiler settings, such as optimisation options, can also be critical. Again refer to existing demo application projects for examples.

 Compilers with an IDE based interface will generally include the target microcontroller as part of the project settings - this must be adjusted to be correct for
 the new target. Likewise where a makefile is used, the options within the makefile must be updated to be correct for the new microcontroller target.
* **Configuring the tick interrupt**:
 The tick interrupt is configured by a function called prvSetupTimerInterrupt(), which can be located within FreeRTOS/source/portable/[compiler]/[microcontroller]/port.c.
* **RAM usage and ROM usage**:
 The [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section provides all the information required to understand how FreeRTOS uses RAM, and
 how this RAM is allocated to the RTOS kernel.

 If you are converting an existing demo application to run on a microcontroller that has less RAM then you may need to reduce the configTOTAL\_HEAP\_SIZE
 value - located within FreeRTOSConfig.h - and reduce the number of tasks the demo creates. Reducing the amount
 of tasks created can be achieved by simply commenting out the function calls used to create the tasks within main(), as [previously demonstrated](#combining-or-modifying-existing-demo-projects).

 If you are converting an existing demo application to run on a microcontroller that has less ROM then you may need to reduce the number of demo application
 files that are included in the build. These are the files located within the FreeRTOS/Demo/common [directory tree](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization). When you remove a demo application file from the build you will also have to remove the call within main() used to create the tasks that are no longer included.
