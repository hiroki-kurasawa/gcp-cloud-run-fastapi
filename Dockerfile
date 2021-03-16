FROM python:3.7-buster

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/ .
EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
