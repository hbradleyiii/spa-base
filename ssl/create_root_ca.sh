#!/bin/bash
#
# name:             create_root_ca.sh
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created:          Jan 19, 2019 14:05 PM
#
# description:      This file is for creating a root ca for self-signed
#                   certificates.
#
# dependencies:     You may need to install this ssl package:
#                   $ sudo apt-get install libssl1.0.0 -y
#
# This script is derived from the very helpful instructions found here:
# https://fabianlee.org/2018/02/17/ubuntu-creating-a-trusted-ca-and-san-certificate-using-openssl-on-ubuntu/
#

if [[ -f ca.key.pem || -f ca.pem ]]; then
	echo 'Root certificates already exist. Nothing to do.'
else
	echo 'Generating root ca key...'
	openssl genrsa -aes256 -out ca.key.pem 2048

	chmod 400 ca.key.pem

	echo 'Creating ca pem...'
	openssl req -new -x509 -subj "/CN=bradleystudioca" -extensions v3_ca -days 3650 -key ca.key.pem -sha256 -out ca.pem -config localhost.cnf

	openssl x509 -in ca.pem -text -noout
	echo 'Completed.'
fi


echo -e "\n"
echo -e "\n"
echo 'In order to install the ca into your browser, do the following:'
echo '    1. Navigate to chrome://settings/certificates'
echo '    2. Click the "Authorities" tab'
echo '    3. Click "import"'
echo '    4. Upload the "ca.pem" file.'
echo '    5. Select "Trust this certificate for identifying websites."'
echo '    6. Click "OK"'
echo -e "\n"
read -n 1 -s -r -p "Press any key to continue"
echo -e "\n"
