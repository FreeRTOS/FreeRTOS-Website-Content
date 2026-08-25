---
title: 使用 SigV4 库的 HTTP S3 下载演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

此演示使用 SigV4 库对
发送到 AWS S3 HTTP 服务器的 S3 对象下载请求进行身份验证。AWS S3 HTTP 服务器的 TLS 连接仅使用服务器身份验证。请按照
以下步骤配置您与 AWS 的连接。


### 设置 Amazon Web Services (AWS) 账户

1. 如果您还没有账户， 
   [请创建并激活 AWS 账户](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) 
   （其中包括一个[免费层级](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23iot)）。

2. 使用 AWS 身份和访问管理 (IAM) 设置账户和权限。IAM 允许
   您管理账户中每个用户的权限。默认情况下，用户只有
   获得根所有者的授权才具有权限。

   1. 要将 IAM 用户添加到您的 AWS 账户，请参阅 
      [IAM 用户指南](https://docs.aws.amazon.com/IAM/latest/UserGuide/)。

   2. 通过添加以下策略，授予您的 AWS 账户访问 AWS S3 和 IoT 的权限：

      + AmazonS3FullAccess
      + AWSIoTFullAccess
      + IAMFullAccess


### 使用 SigV4 身份验证为 S3 下载设置 AWS 资源

1. 按照 
   ["我如何创建 S3 存储桶？"](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)中的步骤在 S3 中创建一个存储桶, 
   请参阅*Amazon 简单存储服务控制台用户指南*。

2. 按照 
   ["如何将文件和文件夹上传到 S3 存储桶？"](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html)中的步骤将文件上传到 S3。

3. 须安装和配置 AWS CLI 才能执行后续步骤。在
   安装 AWS CLI 后，输入如下命令进行配置：

   ```c
   aws configure
   ```

4. 创建 AWS IoT 事物：您可以使用现有的 AWS IoT 事物，也可以在
   AWS IoT 核心控制台中创建一个新事物。您也可以在 AWS CLI 上使用以下命令来创建事物。

   ```c
   aws iot create-thing --thing-name device_thing_name
   ```

   记录您为事物指定的名称，以供后续步骤使用。 

5. 注册证书：

   如果您的 AWS IoT 事物已附加证书，则
   可以在下面的“附加策略”步骤中使用该证书的 ARN。否则，
   可使用 AWS IoT 核心控制台创建证书并将其附加到该事物。

   1. 可选：

      您也可以使用自己的证书颁发机构 (CA) 证书
      对事物的证书进行签名。必须先这两个证书注册到 AWS IoT，然后您的设备
      才可以向 AWS IoT进行身份验证。如果您还没有 CA 证书，则可以使用 OpenSSL
      创建 CA 证书，请参阅
      [创建您自己的客户端证书](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html)。要将您的 CA 证书注册
      到 AWS IoT，请按照
      [注册 CA 证书](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html#register-CA-cert)中的步骤操作。 
      必须创建由 CA 证书签名的设备证书，并将其注册到 AWS IoT。 
      您可以按照 
      [使用 CA 证书创建设备证书](https://docs.aws.amazon.com/iot/latest/developerguide/device-certs-your-own.html#create-device-cert)中的步骤操作。
      保存证书和相应的密钥对；以备稍后请求安全令牌时
      使用。此外，请记住创建证书时提供的密码。
      在 AWS CLI 中运行以下命令，将设备证书附加到您的事物，以便
      可以在策略变量中使用事物属性。

      ```c
      aws iot attach-thing-principal --thing-name device_thing_name --principal <certificate-arn>
      ```

6. 配置 IAM 角色:

   1. 在您的 AWS 账户中配置 IAM 角色，该角色由代表您设备的凭据提供程序
      使用。您需要将以下两个策略与该角色相关联：
      控制谁可以承担角色的信任策略；
      以及控制通过承担角色可以对哪些资源执行哪些操作的访问策略。以下信任策略授予凭证
      提供程序承担该角色的权限。将其放入文本文档中，并将该文档以
      `trustpolicyforiot.json` 名称保存。

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

   2. 在AWS CLI 中运行以下命令，使用上述信任策略创建 IAM 角色。

      ```
      aws iam create-role --role-name s3-access-role --assume-role-policy-document file://trustpolicyforiot.json
      ```

   3. 以下 s3 访问策略允许您对 S3 执行操作。将策略置于
      文本文档并以 `accesspolicyfors3.json` 名称保存。

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

   4. 在 AWS CLI 中运行以下命令以创建访问策略。

      ```c
      aws iam create-policy --policy-name accesspolicyfors3 --policy-document file://accesspolicyfors3.json
      ```

   5. 在 AWS CLI 中运行以下命令，将访问策略附加到您的角色，替换
      \<your_aws_account_id>：

      ```c
      aws iam attach-role-policy --role-name s3-access-role --policy-arn arn:aws:iam::<your_aws_account_id>:policy/accesspolicyfors3
      ```

7. 配置 PassRole 权限：

   1. 您创建的 IAM 角色必须传递给 AWS IoT 才能创建角色别名，
      如上一步所述。执行该操作的 IAM 用户需要
      `iam:PassRole` 权限才能授权此操作。还应
      为 `iam:GetRole` 操作添加权限，以允许 IAM 用户检索
      有关指定角色的信息。创建以下策略以授予
      `iam:PassRole` 和 `iam:GetRole` 权限，替换
      \<your_aws_account_id>。将此策略命名为 `passrolepermission.json`。

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

   2. 在 AWS CLI 中运行以下命令，以在 AWS 账户中创建策略。

      ```c
      aws iam create-policy --policy-name passrolepermission --policy-document file://passrolepermission.json
      ```

   3. 运行以下命令以将策略附加到 IAM 用户，替换
      \<your_aws_account_id> 和 \<user_name>。（请参阅 [设置 Amazon Web Services (AWS) 账户](#设置-amazon-web-services-aws-账户)。）

      ```
      aws iam attach-user-policy --policy-arn arn:aws:iam::<your_aws_account_id>:policy/passrolepermission --user-name <user_name>
      ```

8. 创建角色别名：

   现在您已经配置了 IAM 角色，可使用 AWS IoT 创建角色别名。创建角色别名时，
   须提供以下信息：

   * RoleAlias：这是角色别名数据模型的主键，因此是必需
     属性。它是一个字符串；最小长度为 1 个字符，最大长度
     为 128 个字符。
   * RoleArn：这是 
     您创建的 IAM 角色的 [Amazon 资源名称 (ARN)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) 

     。这也是一个必需属性。
   * CredentialDurationSeconds：这是一个可选属性，用于指定安全令牌的
     有效性（以秒为单位）。最小值为 900 秒（15 分钟）。
     最大值为 3,600 秒（60 分钟）。如果未指定，则默认值
     为 3600 秒。在 AWS CLI 中运行以下命令以创建角色别名。使用

   您授予 iam: PassRole 权限的用户的凭据。

   ```
   aws iot create-role-alias --role-alias name-s3-access-role-alias --role-arn arn:aws:iam::<your_aws_account_id>:role/s3-access-role --credential-duration-seconds 3600
   ```

9. 附加策略：

   此前，您创建并将证书注册到 AWS IoT，以成功验证您的
   设备。现在，您需要创建一个策略并将其附加到证书，以授权
   安全令牌的请求。

   1. 将以下 JSON 复制到名为 `thingpolicy.json` 的文本文件中，替换
      您的 \<aws_region_name> 和 \<your_aws_account_id>：

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
   2. 在 AWS CLI 中运行以下命令以在 AWS IoT 数据库中创建策略：

    ```
    aws iot create-policy --policy-name Thing_Policy_Name --policy-document file://thingpolicy.json
    ```

   3. 使用以下命令将策略附加到之前注册的
       证书的 ARN。

       ```
       aws iot attach-policy --policy-name Thing_Policy_Name --target <certificate-arn>
       ```

10. 请求安全令牌：

   要向凭据提供程序发出 HTTPS 请求以获取安全令牌，必须
   提供以下信息：

   * 证书和密钥对：由于这是使用 TLS 双向身份验证的 HTTP 请求，
     因此，您在发出请求时必须向客户端提供证书和
     相应地密钥对。使用您
     向 AWS IoT 注册您的证书时所使用的相同证书和密钥对。

   * RoleAlias：提供要在请求中使用的角色别名（在此示例中，为 `Thermostat-dynamodb-access-role-alias`）
     。

   * ThingName：请提供您之前在 AWS IoT 事物注册数据库中
     。这作为名为 `x-amzn-iot-thingname` 的标头进行传递。请注意，
     仅当您使用事物属性
     作为 AWS IoT 或 IAM 策略中的策略变量时，此值才是必需的。

   * AWS 账户特定端点 在 AWS CLI 中运行以下命令，为凭证提供程序获取您的 AWS 
     账户特定端点。（请参阅 
     [DescribeEndpoint API 文档](https://docs.aws.amazon.com/iot/latest/apireference/API_DescribeEndpoint.html) 
     以了解更多详情。

     ```
     aws iot describe-endpoint --endpoint-type iot:CredentialProvider
     ```

     以下是 describe-endpoint 命令的示例输出。该示例包含 endpointAddress。

     ```json
     {
         "endpointAddress": "<your_aws_account_specific_prefix>.credentials.iot.us-east-1.amazonaws.com"
     }
     ```

11. 将您 AWS 账户特定端点复制并粘贴到文件 `demo_config.h` 中，作为
    宏 `democonfigIOT_CREDENTIAL_PROVIDER_ENDPOINT` 的值。

   ```c
   #define democonfigIOT_CREDENTIAL_PROVIDER_ENDPOINT    "<your_aws_account_specific_prefix>.credentials.iot.us-east-1.amazonaws.com"
   #define CLIENT_CERT_PATH "path of the client certificate downloaded when setting up the device certificate in AWS IoT Account Setup"
   #define CLIENT_PRIVATE_KEY_PATH "path of the private key downloaded when setting up the device certificate in AWS IoT Account Setup"
   ```

12. 在 `demo_config.h` 中配置以下宏

   ```c
   #define democonfigIOT_THING_NAME                  "Name of IOT Thing that you provided in STEP 1"
   #define democonfigIOT_CREDENTIAL_PROVIDER_ROLE    "Name of ROLE ALIAS that you provided in STEP 4"
   #define democonfigS3_BUCKET_NAME                  "Name of Bucket that contains the object that needs to be downloaded"
   #define democonfigS3_BUCKET_REGION                "Region where Bucket is located"
   #define democonfigS3_OBJECT_NAME                  "Name of object that needs to be downloaded from AWS S3"
   ```


### 参数

**device_thing_name**   
设备注册到 AWS IoT 核心使用的 AWS IoT 事物名称。

**thing_name-s3-access-role-alias**   
S3 角色别名的名称。

**Thing_Policy_Name**   
在“附加策略”步骤中附加到设备证书的策略的名称。

**BUCKET_NAME**   
将从中下载演示的 S3 存储桶的名称。
