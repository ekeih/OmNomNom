FROM python:3.6-alpine

WORKDIR /app

RUN apk update && apk add gcc musl-dev poppler-utils
RUN pip3 install omnbot

RUN mkdir /app/logs
RUN chown nobody /app
RUN chown nobody /app/logs
USER nobody
ENTRYPOINT ["python3"]
