FROM python:3.7-buster

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/ .
EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
