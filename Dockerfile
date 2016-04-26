# Docker image for OmNomNom Telegram Bot
#
#     Build: docker build -t ekeih/omnomnom .
#     Run: docker run -d ekeih/omnomnom ekeih/omnomnom 

FROM alpine:latest

WORKDIR /app

RUN apk update
RUN apk add bash ca-certificates python3 py-pip

COPY canteens/ canteens/
COPY main.py omnomnom.py config.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD python3 main.py
