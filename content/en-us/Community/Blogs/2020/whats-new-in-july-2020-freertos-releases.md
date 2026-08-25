---
title: What's New in July 2020 FreeRTOS Releases
created: 2020-07-17
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---
 
by [Tanmoy Sen](../author/stanmoy) on 17 Jul 2020

We are excited to share these latest updates:

1. Progress toward the [FreeRTOS LTS release](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/02-More-about-LTS):

   * Refactored MQTT library: The [200717\_LTS\_development\_snapshot.zip](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) file contains, 
     among other things, our progress toward completing the refactoring and quality checklist for the MQTT 
     library. It is now simpler to bring the MQTT library into any project – including projects that do 
     not use FreeRTOS. You can find details on the refactored MQTT library [here](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), and 
     pre-configured projects that demonstrate the library’s most basic usage 
     scenarios [here](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/01-coreMQTT-demo). Pre-configured projects that demonstrate more complex 
     usage scenarios will follow. Additional details on our upcoming Long Term Support (LTS) release can 
     be found on the [LTS Roadmap page](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/02-More-about-LTS).

   * OTA Pause and Resume: The [200717\_LTS\_development\_snapshot.zip](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) file also contains 
     enhancements to the OTA library. Now, a FreeRTOS device can suspend an in-progress OTA if it disconnects 
     from the network, and then resume the OTA when it reconnects. This helps OTA downloads to complete 
     quickly when there is intermittent network connectivity. You can find details on the OTA 
     library [here](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates).

   See [Changelog](https://github.com/FreeRTOS/FreeRTOS/blob/V200717_LTS_development_snapshot/CHANGELOG.md) 
   for a full list of enhancements.
   
2. AWS reference integrations:

   * [The 202007.00 release](https://github.com/aws/amazon-freertos/tree/202007.00) of the AWS reference 
     integrations includes a new integration for the Cypress PSoC 64 Standard Secure microcontroller. You 
     can take advantage of FreeRTOS features and benefits using the 
     Cypress [PSoC 64 Standard Secure AWS Wi-Fi Bluetooth Pioneer Kit](https://devices.amazonaws.com/detail/a3G0h0000088AgXEAU) 
     available from Cypress. See details [here.](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations)


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers 
and embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
