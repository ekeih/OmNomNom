FROM python:3.10-alpine

WORKDIR /app

RUN mkdir /app/logs && chown -R nobody /app
RUN apk update && apk add gcc musl-dev poppler-utils libffi-dev
COPY . .
RUN pip3 install .

USER nobody
ENTRYPOINT ["python3"]
