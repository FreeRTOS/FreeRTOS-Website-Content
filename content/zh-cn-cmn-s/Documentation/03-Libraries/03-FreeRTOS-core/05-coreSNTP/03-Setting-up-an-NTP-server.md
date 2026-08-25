---
title: "设置 NTP 服务器的说明"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

（支持 AES-128-CMAC 身份验证）

按照以下说明在 Linux 环境中设置 NTP 服务器
（使用 [`chrony`](https://chrony.tuxfamily.org/) 软件包），其中 128 位 **AES-CMAC**）
用作客户端-服务器通信中身份验证机制的哈希算法。


### 必须从源文件构建 Chrony，以获得 AES CMAC 支持

要使用支持 AES-CMAC 128 的 chrony，系统必须安装 4.0 或更高版本。正如
[版本说明](https://chrony.tuxfamily.org/news.html)中提到的那样，**chrony 4.0**
支持具备 Nettle 依赖项的 AES CMAC 函数。Ubuntu 18.04 或 Ubuntu 20.04 在其 LTS 版本中
均不提供支持 AES-CMAC 的 chrony 软件包版本。

### 说明

#### 1\. 在从源文件构建 chrony 之前，先安装 chrony 的依赖项

可在此查看依赖项列表：https://chrony.tuxfamily.org/doc/4.1/installation.html。下载所有依赖项。

```c
sudo apt-get install libcap2 libseccomp2 pkg-config nettle-dev
```

**nettle** 是使 chrony 支持 CMAC 所需的软件包。如果 `nettle-dev` 不
安装软件包头文件及其共享库，即 ***.so** 文件，则需要
从源文件安装 nettle。通过查找 `nettle/cmac.h` 文件
和 `hogweed.so` 以及 `nettle.so` 库文件（它们通常
位于 `/usr/` 文件夹）来验证 Nettle 的安装。如果找不到这些文件，请按照下一步的说明从源文件中安装 Nettle。
否则，跳到第 3 步。

对于 AL2 EC2 实例，

```c
sudo yum install libcap libseccomp pkg-config nettle-dev
```

可能找不到 pkg-config 和 nettle-dev。转到第 2 步。


#### 2.（可选）从源文件安装 Nettle

Nettle 的生成和安装说明如下：https://www.linuxfromscratch.org/blfs/view/svn/postlfs/nettle.html。
请遵循这些说明安装软件包。


##### 2.1 下载源文件并解压缩

```c
wget https://ftp.gnu.org/gnu/nettle/nettle-3.9.1.tar.gz
tar -xvf tar -xvf nettle-3.9.1.tar.gz
```


##### 2.2 从源文件生成和安装

```c
./configure --prefix=/usr --disable-static && make -j8
sudo make install
sudo chmod -v 755 /usr/lib/lib{hogweed,nettle}.so
```

通过在 `/usr/include/nettle` 目录中查找 `cmac.h` 文件
以及在 `/usr/lib` 目录中查找 `libogweed.so` 和 `libnettle.so` 库来验证 Nettle 的安装。找不到
libhogweed.so 也没有问题。


#### 3\. 从源文件生成 chrony

如上所述，为了支持 AES-CMAC 身份验证（带 Nettle），需要 chrony >= 4.0。以下是
关于从源文件生成和安装 chrony 的说明。


##### 3.1 克隆存储库并签出最新版本标记

在此示例中，将 `4.1` 替换为最新版本标签：

```c
git clone https://git.tuxfamily.org/chrony/chrony.git
git checkout tags/4.1
```


##### 3.2 使用 Nettle 安装的系统信息（以及所需的 chrony.conf 位置）配置生成

`./configure --help` 命令可用于查看 `configure`
脚本的使用文档。

对于我的环境，我必须通过设置
`CPPFLAGS` 和 `LDFLAGS` 环境变量指定 Nettle 包的包含和共享库文件的文件夹路径。此外，我还指定了 `chrony.conf`
和 `chrony.keys` 文件的位置（通过传递 `---sysconfdir=<DIR>` 参数）。

此外，我进行配置使之安装在 `/usr/sbin/` 和 `usr/bin` 目录下，
（用 `--prefix=/usr` 参数），以便我的环境路径能自动
获取 chrony 的二进制文件。

```c
export CPPFlAGS='-I/usr/include'
export LDFLAGS='-L/usr/lib'
./configure --prefix=/usr --sysconfdir=/etc/chrony

```

确保生成配置日志记录显示已检测到 `nettle` 以及您的系统支持 CMAC，
并且已为 `chrony` 构建启用 `SECHASH` 功能。( `SECHASH` 功能
表示对用于身份验证机制的各种哈希/密码算法的支持。）

日志记录末端应如下所示：

```c
Checking for nettle : Yes
Checking for CMAC in nettle : Yes
Checking for gnutls : No
Features : +CMDMON +NTP +REFCLOCK +RTC -PRIVDROP -SCFILTER -SIGND +ASYNCDNS -NTS -READLINE +SECHASH +IPV6 -DEBUG
Creating Makefile
Creating doc/Makefile
Creating test/unit/Makefile

```

##### 3.3 生成并安装 chrony！

在系统中生成并安装软件包。

```c
make -j 8
sudo make install
```

上述说明将在您的系统中安装 **chronyc** 和 **chronyd** 二进制文件。
（**chronyd** 是执行 NTP 客户端/服务器操作的实际守护程序，而 **chronyc**
是面向用户的客户端实用程序，用于查询守护程序的状态。）

您将看到类似于以下安装日志记录的内容。**注意：**关于文档输出安装的错误
可以忽略，因为未安装文档所需的 chrony 依赖项。

```c
─>  sudo make install

[ -d /etc/chrony ] || mkdir -p /etc/chrony
[ -d /usr/sbin ] || mkdir -p /usr/sbin
[ -d /usr/bin ] || mkdir -p /usr/bin
[ -d /var/lib/chrony ] || mkdir -p /var/lib/chrony
if [ -f /usr/sbin/chronyd ]; then rm -f /usr/sbin/chronyd ; fi
if [ -f /usr/bin/chronyc ]; then rm -f /usr/bin/chronyc ; fi
cp chronyd /usr/sbin/chronyd
chmod 755 /usr/sbin/chronyd
cp chronyc /usr/bin/chronyc
chmod 755 /usr/bin/chronyc
make -C doc install
make[1]: Entering directory '/home/ubuntu/Experiments/chrony/doc'
asciidoctor  -b manpage -o chrony.conf.man.in chrony.conf.adoc
make[1]: asciidoctor: Command not found
Makefile:44: recipe for target 'chrony.conf.man.in' failed
make[1]: *** [chrony.conf.man.in] Error 127
make[1]: Leaving directory '/home/ubuntu/Experiments/chrony/doc'
Makefile:88: recipe for target 'install' failed
make: *** [install] Error 2
```


##### 3.4 确认安装情况

确认系统中是否已安装 **chronyc** 和 **chronyd** 文件。

```c
─>  chronyc --version
chronyc (chrony) version DEVELOPMENT (-READLINE +SECHASH +IPV6 -DEBUG)
```

```c
ls -la /usr/sbin/chronyd
```

此外，使用 **chronyc** 的 **keygen** 命令确认生成 chrony 的软件包是否支持 AES-CMAC。
以下显示了支持 AES-CMAC 的命令的示例运行。

```c
─>  chronyc keygen 1 AES128 128
1 AES128 HEX:6CD5CA79D68B815093BA1DEC9DBD691C
```


#### 4\. 为 chrony 配置引用 NTP 服务器（在配置 chrony 为服务器之前）

在将 `chrony` 作为服务器运行之前，必须将其配置为客户端，以便从不同的引用服务器
获取时间。


##### 4.1 设置 chrony.conf 文件

`chrony.conf` 文件用于配置 **chrony** 守护程序。以下配置可以
放置在 `/etc/chrony/chrony.conf` 文件中，其中 NTP 池服务器和 Amazon 时间同步服务
（地址为 `169.254.169.123`）已进行配置，用于为 **chrony** 客户端获得时间。


```c
# Welcome to the chrony configuration file. See chrony.conf(5) for more
# information about usuable directives.

pool ntp.ubuntu.com        iburst maxsources 4
pool 0.ubuntu.pool.ntp.org iburst maxsources 1
pool 1.ubuntu.pool.ntp.org iburst maxsources 1
pool 2.ubuntu.pool.ntp.org iburst maxsources 2
server 169.254.169.123 prefer iburst minpoll 4 maxpoll 4

# This directive specify the location of the file containing ID/key pairs for
# NTP authentication.
keyfile /etc/chrony/chrony.keys

# This directive specify the file into which chronyd will store the rate
# information.
driftfile /var/lib/chrony/chrony.drift

# Uncomment the following line to turn logging on.
log tracking measurements statistics

# Log files location.
logdir /var/log/chrony

# Stop bad estimates upsetting machine clock.
maxupdateskew 100.0

# This directive enables kernel synchronisation (every 11 minutes) of the
# real-time clock. Note that it can’t be used along with the 'rtcfile' directive.
rtcsync

# Step the system clock instead of slewing it if the adjustment is larger than
# one second, but only in the first three clock updates.
makestep 1 3
```


##### 4.2 创建 chronyd.service 文件

`chronyd.service` 文件指定 **chronyd** 作为守护进程运行。将此文件
与以下内容放置在 `/etc/systemd/system/`：

```c
─>  sudo cat /etc/systemd/system/chronyd.service
[Unit]
Description=chrony, an NTP client/server
Documentation=man:chronyd(8) man:chronyc(1) man:chrony.conf(5)
Conflicts=systemd-timesyncd.service openntpd.service
After=network.target

[Service]
Type=forking
PIDFile=/run/chrony/chronyd.pid
EnvironmentFile=-/etc/default/chrony
ExecStart=/usr/sbin/chronyd $OPTIONS
PrivateTmp=yes
ProtectHome=yes
ProtectSystem=full

[Install]
Alias=chronyd.service
WantedBy=multi-user.target
```


##### 4.3 作为 NTP 客户端运行 chronyd 并确认

启动 **chronyd** 服务，并确认带有 **chronyc** 实用程序的 NTP 客户端的功能是否正常，
该步骤使用其 **sources** 和 **tracking** 子命令即可做到。

```c
sudo service chronyd start

```

```c
─>  chronyc sources
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^- alphyn.canonical.com          2  10   377   29m  -2864us[-2829us] +/-  105ms
^- chilipepper.canonical.com     2  10   377   22m  +2987us[+2988us] +/-  102ms
^- pugot.canonical.com           2  10   377    92  -1572us[-1571us] +/-  100ms
^- golem.canonical.com           2  10   377   479   -505us[ -509us] +/-  109ms
^- time.cloudflare.com           3  10   377   25m  +9676us[+9687us] +/-   22ms
^- a.chl.la                      2  10   377   486  +1995us[+1991us] +/-   87ms
^- ns4.asda.gr                   2  10   377   469  +7679us[+7674us] +/-  160ms
^- 0.cl.ntp.edgeuno.com          3  10   377   990  -5310us[-5326us] +/-  228ms
^* 169.254.169.123               3   4   377     2   +157ns[ +552ns] +/-  535us
```

```c
─>  chronyc tracking
Reference ID    : A9FEA97B (169.254.169.123)
Stratum         : 4
Ref time (UTC)  : Wed Jun 09 23:41:53 2021
System time     : 0.000000990 seconds fast of NTP time
Last offset     : +0.000000155 seconds
RMS offset      : 0.000001250 seconds
Frequency       : 2.439 ppm slow
Residual freq   : +0.000 ppm
Skew            : 0.023 ppm
Root delay      : 0.000512199 seconds
Root dispersion : 0.000275599 seconds
Update interval : 16.2 seconds
Leap status     : Normal
```


#### 5. 将 chrony 配置为 NTP 服务器

首先，确保 **chronyd** 作为 NTP 客户端在您的系统上运行，对此，请查看说明中的
[步骤 4.2](#42-创建-chronydservice-文件)。


##### 5.1 使用允许指令更新 chrony.conf

如果 `chronyd` 已作为 NTP 客户端运作，通过添加 `allow`
指令到 `chrony.conf` 文件中即可将其升级为 NTP 服务器。`allow` 指令允许指定网络和子网，
以接受来自的 NTP 请求。请参阅 https://chrony.tuxfamily.org/doc/devel/chrony.conf.html，获取详细信息。

[![NTP 服务器允许指令](/media/2021/setting-ntp-server-300x138.png)](/media/2021/setting-ntp-server-300x138.png)
*单击以放大*


```c
echo 'allow 0/0' >> /etc/chrony/chrony.conf

```

##### 5.2 在 NTP 服务器配置中重新运行 chronyd

使用更新的配置重新运行 `chronyd` 以启用 NTP 服务器功能。

```c
sudo service chronyd restart

```

再次使用 **chronyc tracking** 或 **chronyc sources** 命令验证 **chronyd** 是否正在运行。


##### 5.3 具有 Python 脚本的 chronyd 完整性检查服务器模式

使用以下 python 脚本确认 **chronyd** 的 NTP 服务器模式在本地运行。

```c
#!/usr/bin/env python
#
# Requirements: ntplib (easy_install ntplib)
import ntplib
from time import ctime
import argparse

parser = argparse.ArgumentParser( description="test-ntp.py - Test a set of IP addresses for NTP " )
parser.add_argument("--ip", action="append", help="IP address to check for NTP")
a = parser.parse_args()
if a.ip is not None:
    c = ntplib.NTPClient()
    for ip in a.ip:
        try:
            response = c.request(ip)
            if response:
                print (ip+" NTP Active "+ ctime(response.tx_time))
        except:
            print (ip+" NTP Deactivated")
else:
    parser.print_help()
    exit(1)
```

以 `python3 <script-name>.py --ip localhost.` 方式调用脚本。以下是一个示例输出，显示
将 chronyd 成功配置为 NTP 服务器。

```c
─>  python3 ~/Experiments/test-ntp-server.py --ip localhost
localhost NTP Active Wed Jun  9 23:59:41 2021
```


#### 6\. 在 NTP 服务器中启用基于对称密钥的身份验证

您可以通过
在 `/etc/chrony/chrony.keys` 文件中添加密钥来启用基于对称密钥的身份验证，以便与 NTP 服务器进行通信。密钥可以通过使用 `keygen` 子命令生成，
该子命令来自 `chronyc` 实用程序。


##### 6.1 生成 AES-128-CMAC 密钥进行身份验证，并在 NTP 服务器中进行配置

由 `chronyc keygen` 命令生成的密钥可以添加到 `chrony.keys` 文件中。

```c
chronyc keygen 1 AES128 128 > /etc/chrony/chrony.keys

```

可以将多个密钥添加到 `chrony.keys` 文件，通过密钥 ID 引用每个密钥。上述
命令中，`1` 是 AES-128-CMACM 密钥的密钥 ID。

通过 `sudo cat /etc/chrony/chrony.keys` 验证是否已将密钥添加到 `chrony.keys` 文件。


##### 6.2 重新运行 NTP 服务器以使用身份验证密钥

重新运行 NTP 服务器后，它将同时服务于两者：

* 在其请求有效负载中具备身份验证代码 (MAC) 的客户端，该身份验证代码用服务器已知的密钥生成；以及
* 在身份验证模式下不通信的客户端，即它们的请求有效负载中没有 MAC。

```c
sudo service chronyd restart
```
