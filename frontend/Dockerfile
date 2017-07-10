FROM python:3.6-alpine3.6

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY frontend.py ./

USER nobody
CMD python3 frontend.py
