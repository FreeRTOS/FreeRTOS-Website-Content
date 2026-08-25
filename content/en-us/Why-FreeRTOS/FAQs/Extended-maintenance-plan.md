---
title: "FreeRTOS FAQ - What is the FreeRTOS Extended Maintenance Plan (EMP)?"
created: 2018-09-20
categories:
  - kernel
description: Frequently asked questions about the FreeRTOS Extended Maintenance Plan (EMP)
---


## What is the FreeRTOS Extended Maintenance Plan (EMP)?

The FreeRTOS Extended Maintenance Plan (EMP), offered by Amazon Web Services (AWS), provides you with security 
patches and critical bug fixes on your chosen FreeRTOS Long Term Support (LTS) version for up to 10 years beyond 
the expiry of the initial LTS [period](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries). With FreeRTOS EMP, your FreeRTOS-based,
long-lived devices can rely on a version that has feature stability and receives security updates during the 
term of your subscription. You receive timely notifications of upcoming patches on FreeRTOS libraries, so you 
can plan the deployment of security patches on your Internet of Things (IoT) devices. Before the end of the 
current LTS period, you will be able to subscribe to the Extended Maintenance Plan using your AWS account, and renew 
the subscription annually to cover the product lifecycle or until you're ready to transition to a new FreeRTOS 
release. FreeRTOS EMP applies to libraries that are part of FreeRTOS LTS. 


## Why should I use FreeRTOS EMP?

The FreeRTOS EMP helps you maintain your FreeRTOS-based devices during the term of your subscription. It allows you to save 
operating system upgrade costs and reduce the risks of not being able to update devices in time. It provides 
security patches and critical bug fixes on feature-stable FreeRTOS LTS versions, so you don't need to incur 
development, testing, and QA costs to migrate to the latest FreeRTOS release. Updating devices involves 
project planning, release readiness testing, and over-the-air (OTA) update scheduling to deploy critical fixes. 
FreeRTOS EMP reduces the risk of delayed deployment by providing timely notification of upcoming patches and 
support with integration issues. 


## What are the main features of FreeRTOS EMP?

| Feature | Description | Why is it important? |
| --- | --- | --- |
| Feature stability | Get FreeRTOS libraries that maintain the same set of features for years. | Save upgrade costs by using a stable FreeRTOS codebase for your product lifecycle. |
| API stability | Get FreeRTOS libraries that have stable APIs for years. |
| Critical fixes | Receive security patches and critical bug[^1] fixes on your chosen FreeRTOS libraries. | Security patches help keep your IoT devices secure for the product lifecycle. |
| Notification of patches | Receive timely notification of upcoming patches. | Timely awareness of security patches helps you proactively plan the deployment of patches. |
| Flexible subscription plan | Extend maintenance by a year or longer. | Continue to renew your annual subscription to keep the same version for the entire device lifecycle, or for a shorter period to buy time before upgrading to the latest FreeRTOS version. |


[^1]: A critical bug is a defect determined by AWS to impact the functionality of the affected 
library and has no reasonable workaround.

AWS will provide technical support to FreeRTOS EMP customers via [AWS Support](https://aws.amazon.com/premiumsupport/). 
AWS Support is not included in FreeRTOS EMP subscriptions. You can track issues (for example, issues related 
to AWS accounts, billing, or bugs) or get access to technical experts (on issues such as patch integration) 
based on your AWS Support plan.


## Where can I find information about pricing and getting started?

Visit the [FreeRTOS webpage](https://aws.amazon.com/freertos/) on AWS for more information.
