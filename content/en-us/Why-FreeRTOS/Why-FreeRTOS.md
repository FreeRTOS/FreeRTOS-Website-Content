---
title: Why use FreeRTOS?
created: 2023-05-16
categories:
  - get started
description: An introduction to the history and current features of FreeRTOS.
feature: blog
featuredImage: /media/2023/why_freertos.png
relatedLinks: 
  - title: What is FreeRTOS?
    link: /Why-FreeRTOS/What-is-FreeRTOS
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS
next: 
  title: RTOS fundamentals
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
---

## Why choose FreeRTOS?

<blockquote>
    <span className="content">
"It's probably safe to say at this point that FreeRTOS goes through more 'peer-review' than any other RTOS available
on the planet. I have used it in several projects - one of which was a multiprocessor environment that used more than
64 processors and needed to run for months reliably. The RTOS core performed well. Take FreeRTOS for a spin."
    </span>
<span className="attribution">John Westmoreland</span>
</blockquote>


**FreeRTOS provides the best of all worlds:** FreeRTOS is truly free and [supported](https://forums.freertos.org), even
when used in commercial applications.
The [FreeRTOS open source MIT license](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing)
does not require you to expose your proprietary IP. You can take a product to market using FreeRTOS without even talking
to us, let alone paying any fees, and thousands of people do just that. If, at any time, you would like to receive
additional backup, or if your legal team requires additional written guarantees or indemnification, then there
is [a simple low cost commercial upgrade path](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing#optional-freertos-commercial-licensing).
Your peace of mind comes with the knowledge that you can opt to take the commercial route at any time you choose.

Here are some reasons why FreeRTOS is a good choice for your next application - FreeRTOS...

- Provides a single and independent solution for many different architectures and development tools.
- Is known to be reliable. Confidence is assured by the activities undertaken by the SAFERTOS sister project.
- Is [feature rich](/Why-FreeRTOS/highlighted-features) and still undergoing continuous active development.
- Has a minimal ROM, RAM and processing overhead. Typically an RTOS kernel binary image will be in the region
  of 6K to 12K bytes.
- Is very simple - the core of the RTOS kernel is contained
  in [only 3 C files](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization). The majority
  of the many files included in the .zip file download relate only to the numerous demonstration applications.
- Is truly free for use in commercial
  applications (see [license conditions](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing)
  for details).
- Has commercial licensing, professional support and porting services available in the form of OPEN**RTOS** from our
  partner [WITTENSTEIN high integrity systems](https://www.highintegritysystems.com).
- Has a migration path to [SAFE**RTOS**](https://www.highintegritysystems.com), which includes certifications for the
  medical, automotive and industrial sectors.
- Is well established with a large and ever growing user base.
- Contains a pre-configured example for each port. No need to figure out how to setup a project - just download and compile!
- Has an excellent, monitored, and active free [support forum](https://forums.freertos.org).
- Has the assurance that commercial support is available should it be required.
- Provides ample documentation.
- Is very scalable, simple and easy to use.
- FreeRTOS offers a smaller and easier real time processing alternative for applications where eCOS, embedded Linux
  (or Real Time Linux) and even uCLinux won't fit, are not appropriate, or are not available.


## Did you know?

- FreeRTOS is downloaded every 170 seconds (on average, during 2019).

- **FreeRTOS came top in class in every [EETimes Embedded Market](https://www.embedded.com/electronics-blogs/embedded-market-surveys/4458724/2017-Embedded-Market-Survey)
  Survey since 2011**, which was the first year it was included.

- FreeRTOS offers _**lower project risks**_ and a _**lower total cost of ownership**_ than commercial alternatives because:

  - It is [fully supported](https://forums.freertos.org) and documented.
  - Most people take products to market without ever contacting us, but with the complete peace of mind that they could opt
    to switch to a [fully indemnified commercial license](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing#optional-freertos-commercial-licensing) (with dedicated support) at any time.

- Some FreeRTOS ports [never completely disable interrupts](/Documentation/02-Kernel/03-Supported-devices/02-Customization#kernel_priority).

- For strict quality control purposes, and to remove all IP ownership
  ambiguity, [official FreeRTOS code is separated from community contributions.](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)

- FreeRTOS has a tick-less mode to [directly support low power applications](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support).

- FreeRTOS is designed to be simple and easy to use: Only 3 source files that are common to all RTOS ports, and
  one microcontroller specific source file are required, and its API is designed to be simple and intuitive.

- The RL78 port can create 13 tasks, 2 queues and 4 software timers in under 4K bytes of RAM!

