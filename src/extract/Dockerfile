FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg git -y

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /output
COPY *.py /usr/src

WORKDIR /usr/src

ENTRYPOINT ["python", "extract.py"]