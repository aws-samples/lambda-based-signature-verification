# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: Apache-2.0
#!/bin/bash

# Using RPM as an example, download and run notation installer. 
wget https://d2hvyiie56hcat.cloudfront.net/linux/amd64/installer/rpm/latest/aws-signer-notation-cli_amd64.rpm
sudo rpm -U aws-signer-notation-cli_amd64.rpm

mkdir -p ./notation-lambda-layer/bin

# copy over notation files needed
cp -r "${XDG_CONFIG_HOME:-$HOME/.config}/notation" ./notation-lambda-layer
rm ./notation-lambda-layer/notation/trustpolicy.json # we'll later import our own trustpolicy
cp /usr/local/bin/notation ./notation-lambda-layer/bin
zip -r notation-lambda-layer.zip ./notation-lambda-layer/*