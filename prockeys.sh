echo "Input files must be cert.p12 and key.p12. Output will be apns.pem"

openssl pkcs12 -clcerts -nokeys -out cert.pem -in cert.p12
openssl pkcs12 -nocerts -out key.pem -in key.p12
openssl rsa -in key.pem -out key-noenc.pem
cat cert.pem key-noenc.pem > apns.pem

rm key.pem
rm key-noenc.pem
rm cert.pem
