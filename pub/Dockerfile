# syntax-docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /pub


RUN pip3 install requests
RUN pip3 install apscheduler
RUN pip3 install flask_apscheduler
RUN pip3 install nfl_data_py
RUN pip3 install numpy
RUN pip3 install pandas
COPY . .
ENV FLASK_APP=publish.py

CMD [ "python3", "publish.py"]