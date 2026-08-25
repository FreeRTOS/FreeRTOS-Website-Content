---
title: HTTP S3 Download Demo using the SigV4 Library
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

This demo uses the SigV4 Library for authenticating the S3 object download requests sent to the
AWS S3 HTTP Server. The AWS S3 HTTP server's TLS connection uses server authentication only. Follow
the steps below to configure your connection to AWS.


### Set up an Amazon Web Services (AWS) account

1. If you haven't 
   already, [create and activate an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) 
   (which includes a [free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)).

2. Accounts and permissions are set using AWS Identity and Access Management (IAM). IAM allows
   you to manage permissions for each user in your account. By default, a user doesn't have
   permissions until granted by the root owner.

   1. To add an IAM user to your AWS account, see 
      the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/).

   2. Grant permission to your AWS account to access AWS S3, and IoT by adding these policies:

      + AmazonS3FullAccess
      + AWSIoTFullAccess
      + IAMFullAccess


### Setup AWS resources for S3 Download using SigV4 authentication

1. Create a bucket in S3 by following the steps 
   in [How do I create an S3 Bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) 
   in the *Amazon Simple Storage Service Console User Guide*.

2. Upload a file to S3 by following the steps 
   in [How do I upload files and folders to an S3 bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html).

3. You must install and configure the AWS CLI in order to follow the next steps. After you have
   installed the AWS CLI, configure it by entering

   ```c
   aws configure
   ```

4. Create an AWS IoT thing: You may use an already existing AWS IoT thing or create a new one in
   the AWS IoT Core Console. You may also use the following command on the AWS CLI with to create a thing.

   ```c
   aws iot create-thing --thing-name device_thing_name
   ```

   Keep track of the name you gave your thing for use in a later step. 

5. Register a certificate:

   If your AWS IoT Thing already has a certificate attached to it, then
   that certificate's ARN can be used in the step "Attach a policy" below. Otherwise, you
   can create a certificate and attach it to the thing using AWS IoT Core Console.

   1. Optional:

      It is also possible to sign the thing's certificate using your own Certificate
      Authority (CA) certificate. You must register both certificates with AWS IoT before your device
      can authenticate to AWS IoT. If you do not already have a CA certificate, you can use OpenSSL
      to create a CA certificate, as described in
      [Use Your Own Certificate](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html). To register your CA
      certificate with AWS IoT, follow the steps in
      [Registering Your CA Certificate](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html#register-CA-cert). 
      You must then create a device certificate signed by the CA certificate and register it with AWS IoT. 
      You can do this by following the steps 
      in [Creating a Device Certificate Using Your CA Certificate](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html#create-device-cert).
      Save the certificate and the corresponding key pair; you will use them when you request a
      security token later. Also, remember the password you provide when you create the certificate.
      Run the following command in the AWS CLI to attach the device certificate to your thing so that
      you can use thing attributes in policy variables.

      ```c
      aws iot attach-thing-principal --thing-name device_thing_name --principal \<certificate-arn>
      ```

6. Configure an IAM role:

   1. Configure an IAM role in your AWS account that will be assumed by the credentials provider
      on behalf of your device. You are required to associate two policies with the role: a trust policy
      that controls who can assume the role, and an access policy that controls which actions can be
      performed on which resources by assuming the role. The following trust policy grants the credentials
      provider permission to assume the role. Put it in a text document and save the document with the
      name `trustpolicyforiot.json`.

      ```json
      {
          "Version": "2012-10-17",
          "Statement": {
              "Effect": "Allow",
              "Principal": {"Service": "credentials.iot.amazonaws.com"},
              "Action": "sts:AssumeRole"
          }
      }
      ```

   2. Run the following command in the AWS CLI to create an IAM role with the preceding trust policy.

      ```
      aws iam create-role --role-name s3-access-role --assume-role-policy-document file://trustpolicyforiot.json
      ```

   3. The following s3 access policy allows you to perform actions on S3. Put the policy in a
      text document and save it with the name `accesspolicyfors3.json`.

      ```json
      {
          "Version": "2012-10-17",
          "Statement": {
              "Effect": "Allow",
              "Action": [
                            "s3:GetObject"
                        ],
              "Resource": "arn:aws:s3:::BUCKET_NAME/*"
          }
      }
      ```

   4. Run the following command in the AWS CLI to create the access policy.

      ```c
      aws iam create-policy --policy-name accesspolicyfors3 --policy-document file://accesspolicyfors3.json
      ```

   5. Run the following command in the AWS CLI to attach the access policy to your role, substituting
      \<your\_aws\_account\_id\>:

      ```c
      aws iam attach-role-policy --role-name s3-access-role --policy-arn arn:aws:iam::\<your_aws_account_id>:policy/accesspolicyfors3
      ```

7. Configure the PassRole permissions:

   1. The IAM role that you have created must be passed to AWS IoT to create a role alias, as
      described in the previous step. The IAM user who performs the operation requires
      `iam:PassRole` permission to authorize this action. You also should add
      permission for the `iam:GetRole` action to allow the IAM user to retrieve
      information about the specified role. Create the following policy to grant
      `iam:PassRole` and `iam:GetRole` permissions, substituting
      \<your\_aws\_account\_id\>. Name this policy `passrolepermission.json`.

      ```json
      {
          "Version": "2012-10-17",
          "Statement": {
              "Effect": "Allow",
              "Action": [
                  "iam:GetRole",
                  "iam:PassRole"
              ],
              "Resource": "arn:aws:iam::<your_aws_account_id>:role/s3-access-role"
          }
      }
      ```

   2. Run the following command in the AWS CLI to create the policy in your AWS account.

      ```c
      aws iam create-policy --policy-name passrolepermission --policy-document file://passrolepermission.json
      ```

   3. Run the following command to attach the policy to the IAM user, substituting
      \<your\_aws\_account\_id\> and \<user\_name\>. (See [Set up an Amazon Web Services (AWS) account](#set-up-an-amazon-web-services-aws-account).)

      ```
      aws iam attach-user-policy --policy-arn arn:aws:iam::\<your_aws_account_id>:policy/passrolepermission --user-name \<user_name>
      ```

8. Create a role alias:

   Now that you have configured the IAM role, you will create a role alias with AWS IoT. You must
   provide the following pieces of information when creating a role alias:

   * RoleAlias: This is the primary key of the role alias data model and hence a mandatory
     attribute. It is a string; the minimum length is 1 character, and the maximum length is
     128 characters.
   * RoleArn: This is 
     the [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) 
     of the IAM role
     you have created. This is also a mandatory attribute.
   * CredentialDurationSeconds: This is an optional attribute specifying the validity (in
     seconds) of the security token. The minimum value is 900 seconds (15 minutes), and the
     maximum value is 3,600 seconds (60 minutes). If not specified, the default value is
     3,600 seconds. Run the following command in the AWS CLI to create a role alias. Use the credentials

   of the user to whom you have given the iam:PassRole permission.

   ```
   aws iot create-role-alias --role-alias name-s3-access-role-alias --role-arn arn:aws:iam::\<your_aws_account_id>:role/s3-access-role --credential-duration-seconds 3600
   ```

9. Attach a policy:

   Earlier, you created and registered a certificate with AWS IoT for successful authentication of your
   device. Now, you need to create and attach a policy to the certificate to authorize the request for
   the security token.

   1. Copy the following JSON into a text file named `thingpolicy.json`, substituting
      your \<aws\_region\_name\> and \<your\_aws\_account\_id\>:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "iot:AssumeRoleWithCertificate",
                "Resource": "arn:aws:iot:<aws_region_name>:<your_aws_account_id>:rolealias/name-s3-access-role-alias"
            }
        ]
    }
    ```
   2. Run the following command in the AWS CLI to create the policy in your AWS IoT database:

    ```
    aws iot create-policy --policy-name Thing_Policy_Name --policy-document file://thingpolicy.json
    ```

   3. Use the following command to attach the policy with the ARN of the certificate you
       registered earlier.

       ```
       aws iot attach-policy --policy-name Thing_Policy_Name --target \<certificate-arn>
       ```

10. Request a security token:

   To make an HTTPS request to the credentials provider to fetch a security token, you have to
   supply the following information:

   * Certificate and key pair: Because this is an HTTP request over TLS mutual authentication,
     you have to provide the certificate and the corresponding key pair to your client while
     making the request. Use the same certificate and key pair that you used during certificate
     registration with AWS IoT.

   * RoleAlias: Provide the role alias (in this example, `Thermostat-dynamodb-access-role-alias`)
     to be assumed in the request.

   * ThingName: Provide the thing name that you created earlier in the AWS IoT thing registry
     database. This is passed as a header with the name `x-amzn-iot-thingname`. Note
     that the thing name is mandatory only if you have thing attributes as policy variables in
     AWS IoT or IAM policies.

   * AWS account-specific endpointRun the following command in the AWS CLI to obtain your AWS 
     account-specific endpoint for the credentials provider. (See 
     the [DescribeEndpoint API documentation](https://docs.aws.amazon.com/iot/latest/apireference/API_DescribeEndpoint.html) 
     for further details.)

     ```
     aws iot describe-endpoint --endpoint-type iot:CredentialProvider
     ```

     The following is sample output of the describe-endpoint command. It contains the endpointAddress.

     ```json
     {
         "endpointAddress": "<your_aws_account_specific_prefix>.credentials.iot.us-east-1.amazonaws.com"
     }
     ```

11. Copy and paste your AWS account-specific endpoint to the file `demo_config.h` as the value of
    the macro `democonfigIOT_CREDENTIAL_PROVIDER_ENDPOINT`.

   ```c
   #define democonfigIOT_CREDENTIAL_PROVIDER_ENDPOINT    "<your_aws_account_specific_prefix>.credentials.iot.us-east-1.amazonaws.com"
   #define CLIENT_CERT_PATH "path of the client certificate downloaded when setting up the device certificate in AWS IoT Account Setup"
   #define CLIENT_PRIVATE_KEY_PATH "path of the private key downloaded when setting up the device certificate in AWS IoT Account Setup"
   ```

12. Configure the following macros in `demo_config.h`

   ```c
   #define democonfigIOT_THING_NAME                  "Name of IOT Thing that you provided in STEP 1"
   #define democonfigIOT_CREDENTIAL_PROVIDER_ROLE    "Name of ROLE ALIAS that you provided in STEP 4"
   #define democonfigS3_BUCKET_NAME                  "Name of Bucket that contains the object that needs to be downloaded"
   #define democonfigS3_BUCKET_REGION                "Region where Bucket is located"
   #define democonfigS3_OBJECT_NAME                  "Name of object that needs to be downloaded from AWS S3"
   ```


### Parameters

**device_thing_name**   
The name of the AWS IoT thing for your device registered with AWS IoT core.

**thing_name-s3-access-role-alias**   
The name for the role alias for S3.

**Thing_Policy_Name**   
The name of the policy attached to the device certificate in the step "Attach a policy".

**BUCKET_NAME**   
The name of the S3 bucket from which the demo will download.
