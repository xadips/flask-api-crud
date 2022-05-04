FROM python:3.10.4-buster

EXPOSE 5000

WORKDIR /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

COPY /server.py /server

CMD [ "python3", "server.py" ]