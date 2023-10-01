FROM python:3
COPY . /work
WORKDIR /work

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD gunicorn --workers 2 --bind 127.0.0.1:5000 api:api

