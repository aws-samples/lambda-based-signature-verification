mkdir notation-lambda-layer
cd notation-lambda-layer
mkdir notation
mkdir bin
cd bin
wget https://github.com/notaryproject/notation/releases/download/v1.0.1/notation_1.0.1_linux_amd64.tar.gz
tar -xvf notation_1.0.1_linux_amd64.tar.gz
rm notation_1.0.1_linux_amd64.tar.gz
cd ..
wget https://d2hvyiie56hcat.cloudfront.net/linux/amd64/installer/rpm/latest/aws-signer-notation-cli_amd64.rpm
tar -xvf aws-signer-notation-cli_amd64.rpm
mkdir -p notation/plugins/com.amazonaws.signer.notation.plugin
cp opt/com.amazonaws.signer.notation.installer.rpm/notation_libexec/* notation/plugins/com.amazonaws.signer.notation.plugin/
mkdir -p notation/truststore/x509/signingAuthority/aws-signer-ts
cp opt/com.amazonaws.signer.notation.installer.rpm/notation_config/aws-signer-notation-root.crt notation/truststore/x509/signingAuthority/aws-signer-ts/
cp opt/com.amazonaws.signer.notation.installer.rpm/notation_config/LICENSE notation/
cp opt/com.amazonaws.signer.notation.installer.rpm/notation_config/THIRD_PARTY_LICENSES notation/
rm -rf opt
rm -rf usr
rm aws-signer-notation-cli_amd64.rpm
zip -r notation-cli-layer.zip *
cd ..
mv notation-lambda-layer/notation-cli-layer.zip sigverify/

