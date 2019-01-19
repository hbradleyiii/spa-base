#!/bin/bash
#
# name:             create_self_signed_cert.sh
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created:          Jan 19, 2019 14:09 PM
#
# description:      This file is for creating a self-signed certificate for
#                   development environments.
#
# dependencies:     You may need to install this ssl package:
#                   $ sudo apt-get install libssl1.0.0 -y
#
# This script is derived from the very helpful instructions found here:
# https://fabianlee.org/2018/02/17/ubuntu-creating-a-trusted-ca-and-san-certificate-using-openssl-on-ubuntu/
#

prefix=localhost

if [[ -f localhost.key.pem || -f localhost.crt ]]; then
	echo 'Self-signed certificates for localhost already exist. Nothing to do.'
	exit
fi

echo 'Generating self-signed key...'
openssl genrsa -out $prefix.key.pem 2048

echo 'Generating ssl certificate request...'
openssl req -subj "/CN=$prefix" -extensions v3_req -sha256 -new -key $prefix.key.pem -out $prefix.csr -config localhost.cnf

echo 'Signing ssl certificate...'
openssl x509 -req -extensions v3_req -days 3650 -sha256 -in $prefix.csr -CA ca.pem -CAkey ca.key.pem -CAcreateserial -out $prefix.crt -extfile localhost.cnf

echo 'Bundling full chain...'
cat $prefix.crt ca.pem $prefix.key.pem > $prefix-ca-full.pem
openssl pkcs12 -export -out $prefix.pfx -inkey $prefix.key.pem -in $prefix.crt -certfile ca.pem

openssl x509 -in $prefix.crt -text -noout
echo 'Completed.'
