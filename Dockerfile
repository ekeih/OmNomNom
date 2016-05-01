# Docker image for OmNomNom Telegram Bot
#
#     Build: docker build -t ekeih/omnomnom .
#     Run: docker run -d --name omnomnom ekeih/omnomnom:latest

FROM alpine:latest

WORKDIR /app

RUN apk update
RUN apk add bash ca-certificates  python3 && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip setuptools

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY canteens/ canteens/
COPY main.py omnomnom.py ./

CMD python3 main.py
