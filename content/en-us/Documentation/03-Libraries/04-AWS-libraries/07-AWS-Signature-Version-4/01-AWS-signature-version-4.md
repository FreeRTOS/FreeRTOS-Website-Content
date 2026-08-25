---
title: AWS Signature Version 4
created: 2018-09-20
categories:
  - libraries
description: An introduction to the AWS IoT signature version 4 library
relatedLinks:
  - title: Signature version 4 Github repository
    link: https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: AWS SigV4 Library
    link: https://aws.github.io/SigV4-for-AWS-IoT-embedded-sdk/v1.2.0/
---


## Introduction

The AWS Signature Version 4 (SigV4) Library is a standalone library for generating authentication headers
and signatures according to the specifications of
the [AWS Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
signing process. This library can be used by applications
to interact with AWS services that require SigV4 authentication using HTTP. This library has no
dependencies on any library other than the standard C library.


This library has gone through code quality checks including verification that no function has
a [GNU Complexity](https://www.gnu.org/software/complexity/manual/complexity.html) score over 8, and
checks against deviations from mandatory rules in
the [MISRA coding standard](https://www.misra.org.uk/). Deviations from the MISRA C:2012 guidelines are
documented
under [MISRA Deviations](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk/blob/main/MISRA.md).
This library has also undergone static code analysis
using [Coverity static analysis](https://scan.coverity.com/), and validation of memory safety through
the [CBMC automated reasoning tool](https://www.cprover.org/cbmc/).

This library can be freely used and is distributed under
the [MIT Open Source License](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk/blob/main/LICENSE).


**Code Size of AWS SigV4 library (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| sigv4.c | 5.2K | 4.4K |
| sigv4\_quicksort.c | 0.4K | 0.3K |
| Total estimates | 5.6K | 4.7K |
