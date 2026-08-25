---
title: AWS IoT Fleet Provisioning
created: 2018-09-20
categories:
  - libraries
description: An introduction to the AWS IoT fleet provisioning library
relatedLinks: 
  - title: Fleet provisioning Github repository
    link: https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk
externalLinks: 
  - title: AWS IoT Fleet Provisioning Library
    link: https://aws.github.io/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/v1.1.0/ 
---

## Introduction

The AWS Fleet Provisioning library enables you to provision a fleet of IoT devices with unique certificates 
and register them with AWS IoT Core using 
the [Fleet Provisioning feature of AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html). 
There are two ways to use fleet 
provisioning, [Provisioning by Claim](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#claim-based) 
and [Provisioning by Trusted User](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#trusted-user), 
which enable you to utilize manufactured device credentials or newly-generated credentials. This library 
has no dependencies on any additional libraries other than the standard C library, and therefore can 
be used with any MQTT library. 

This library has gone through code quality checks including verification that no function has 
a [GNU Complexity](https://www.gnu.org/software/complexity/manual/complexity.html) score over 8, and 
checks against deviations from mandatory rules in 
the [MISRA coding standard](https://www.misra.org.uk/). Deviations from the MISRA C:2012 guidelines 
are documented under [MISRA Deviations](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/blob/main/MISRA.md). 
This library has also undergone static code analysis 
using [Coverity static analysis](https://scan.coverity.com/), and validation of memory safety through 
the [CBMC automated reasoning tool](https://www.cprover.org/cbmc/).


This library is distributed under 
the [MIT Open Source License](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk/blob/main/LICENSE).

**Code Size of AWS IoT Fleet Provisioning (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| fleet\_provisioning.c | 1.0K | 0.9K |
| Total estimates | 1.0K | 0.9K |
