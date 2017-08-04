FROM python:3.6-alpine

WORKDIR /app

RUN apk update && apk add poppler-utils

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

COPY warmup_cache.py warmup_cache.py
COPY stats/ stats/
COPY omnomgram/ omnomgram/
COPY backend/ backend/
COPY canteens/ canteens/
COPY frontend.py frontend.py

RUN chown nobody /app
USER nobody
ENTRYPOINT ["/app/entrypoint.sh"]