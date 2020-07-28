FROM python:3

#ENV endpoint 'axz2zuppilfv5-ats.iot.eu-west-1.amazonaws.com'
ENV endpoint '0.0.0.0'

#--root-ca 'C:\Users\carmichaelt\Documents\Tom C (002)\Tom C\Amazon Root CA1.txt.pem' --cert 'C:\Users\carmichaelt\Documents\Tom C (002)\Tom C\2cbab2e9e5-certificate.pem.crt' --key 'C:\Users\carmichaelt\Documents\Tom C (002)\Tom C\2cbab2e9e5-private.pem.key'

ADD subPubNG.py /

RUN pip install awsiotsdk

EXPOSE 1883
EXPOSE 8883

CMD ["-c"]