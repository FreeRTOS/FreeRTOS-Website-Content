---
title: FreeRTOS FAQ - AWS IoT Reference Integrations
created: 2018-09-20
description: Frequently asked questions about AWS IoT Reference Integrations for FreeRTOS
---

## How can I add my microcontroller-based board to the FreeRTOS.org  [IoT Reference Integrations](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations) page?

To list your board in the AWS IoT Reference Integrations page, follow the qualification process listed 
in the [AWS Device Qualification Program](https://aws.amazon.com/partners/dqp/). In this program, you 
will need to validate your FreeRTOS port, submit the validation results, and list your board in 
the [AWS Partner Device Catalog.](https://devices.amazonaws.com/) Once qualified, your board will be 
listed in the FreeRTOS.org IoT Reference Integrations page.


## How do I get started with FreeRTOS LTS libraries, if I want to use AWS IoT features?

You can build your project from scratch by cloning GitHub repositories of individual libraries, or start 
from IoT reference integrations in FreeRTOS.org and update individual libraries to FreeRTOS LTS libraries. 
Some IoT reference integrations have been pre-integrated with FreeRTOS LTS libraries, and you can identify 
them by the tag, “Uses FreeRTOS YYYYMM.XX LTS libraries”. Once you make a selection, it will take you to 
the AWS Partner Device Catalog, where you can review a list of LTS libraries used in the reference 
integration, and a getting started guide for specific MCU-based boards.
