FROM alpine:latest

WORKDIR /app

RUN apk update
RUN apk add bash ca-certificates python3 python3-dev musl-dev gcc
RUN python3 -m ensurepip && pip3 install --upgrade pip setuptools

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY backend.py ./
COPY canteens/ canteens/

CMD python3 backend.py
