FROM python:3.8

ENV PYTHONUNBUFFERD 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install binutils libproj-dev gdal-bin
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN apt-get -y update
RUN apt-get -y install cron

WORKDIR /ai_django

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .