FROM python:3.10.4-buster

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY /app.py /app

COPY /templates /app/templates/

COPY /todo.dbs /app

CMD [ "python3", "app.py" ]