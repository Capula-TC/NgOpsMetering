FROM python:3

ADD subPubNG.py /

RUN pip install awsiotsdk

EXPOSE 1883
EXPOSE 8883

CMD ["-c"]