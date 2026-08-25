---
title: SigV4 Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Security Token*   
Temporary, limited-privelege credentials provided by the AWS Security Token Service (AWS STS) to authenticate 
IAM users.


*Credentials Provider*   
AWS IoT Core has a credentials provider that allows you to use the 
built-in [X.509 certificate](https://docs.aws.amazon.com/iot/latest/developerguide/x509-client-certs.html) 
as the unique device identity to authenticate AWS requests. This eliminates the need to store an access 
key ID and a secret access key on your device.
