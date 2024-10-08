FROM python:3.13-alpine

WORKDIR /app

RUN mkdir /app/logs && chown -R nobody /app
RUN apk update && apk upgrade --no-cache && apk add --update --no-cache gcc musl-dev poppler-utils libffi-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN pip3 install .

USER nobody
ENTRYPOINT ["python3"]
