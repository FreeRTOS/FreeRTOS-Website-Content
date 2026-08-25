---
title: "Zilog eZ80 Acclaim! Port for the ZDS II Development Tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

The Zilog eZ80 Acclaim! port was created by Marcos A. Pereira.

I am not able to test the port due to a lack of the necessary development tools and hardware. This means it is **unsupported**
and provided separately from the main FreeRTOS source code download. Work on a supported port will
commence shortly.

Notes from Z80### port author

See a supported port documentation page for more information on the directory structure, how to use FreeRTOS, etc.

*"The port was created on an eZ80F91
 development kit using the [ZDS II eZ80Acclaim! development tools](http://www.zilog.com/software/zds2.asp)
 (V4.9.1).*

To added the port to an existing FreeRTOS download you need to define a new constant to be used in the portable.h header file. 
I used ZDSII\_EZ80\_PORT. The same constant (ZDSII\_EZ80\_PORT) needs to be defined
in the project -> settings -> C -> Preprocessor -> Preprocessor definitions. The portable.h file and demo project file
included in the Z80 download already contain these setting.

The heap\_3.c file is used because the kit has a large amount of RAM.

I need also to change the tasks.c source file because the ZDSII C compiler doesn't understand the #if clauses without a 
space between the #if and the parenthesis. For example:

#if( INCLUDE\_vTaskDelete == 1 )

 gives the errors 
"ERROR (7) Illegal directive and ERROR (31) Extra "#endif" found". You need to change all #if clauses putting 
a space between the #if and the parenthesis. Again the files in the Z80 download have these modifications.

[Download for FreeRTOS eZ80 source code.](http://www.realtimeengineers.com/FreeRTOS_eZ80.zip)
