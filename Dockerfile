FROM python:3

ENV endpoint=''
ENV root-cert=''
ENV cert=''
ENV key=''

ADD pahosubPubNG.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 1883
EXPOSE 8883

CMD ["sh","-c","python3 ./pahosubPubNG.py --range-start 0 --range-end 9 --endpoint ${endpoint} --root-ca ${root-cert} --cert ${cert} --key ${key}"]