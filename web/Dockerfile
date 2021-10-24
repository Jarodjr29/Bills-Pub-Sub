# syntax-docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /web

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install mysql-connector-python
RUN pip3 install requests
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install flask_socketio
COPY . .
ENV FLASK_APP=server.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]