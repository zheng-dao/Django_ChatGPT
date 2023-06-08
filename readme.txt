SSH UPGRADE ON UBUNTU 20
https://askubuntu.com/questions/1189747/is-possible-to-upgrade-openssh-server-openssh-7-6p1-to-openssh-8-0p1
ssh -V

sudo su ?
sudo apt update
sudo apt install build-essential zlib1g-dev libssl-dev
sudo mkdir /var/lib/sshd
sudo chmod -R 700 /var/lib/sshd/
sudo chown -R root:sys /var/lib/sshd/
wget -c https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.8p1.tar.gz

tar -xzf openssh-8.8p1.tar.gz
cd openssh-8.8p1/
sudo apt install libpam0g-dev libselinux1-dev libkrb5-dev
./configure --with-kerberos5 --with-pam --with-selinux --with-privsep-path=/var/lib/sshd/ --sysconfdir=/etc/ssh
make
sudo make install

If it still shows the old version then copy the new version as below.

cd /usr/sbin
sudo mv sshd sshd.bak                 # Back up existing
sudo cp /usr/local/sbin/sshd sshd

sudo reboot

Test is ssh is right version from https requests (on Windows):
Nmap -v -A finalyticsdata.com --script vuln

DO NOT NEED THE BELOW ANYMORE:
----------------------------------------------------------------------------
CREATE NEW ED25519 KEY AND PUT IT IN ~/.ssh/authorized_keys!!!!

Create key pair:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html

Add/remove keys from your instance:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/replacing-key-pair.html

See Method 4 here and Edit User Data:
https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-resolve-ssh-connection-errors/

Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type:
    text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
iptables -F
service sshd restart
--//