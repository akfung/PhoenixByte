# FROM python:3.8.17
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

ARG ENVIRONMENT='runpod'

WORKDIR /code
   
COPY ./requirements.txt /code/requirements.txt

RUN apt update

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

ENV ENVIRONMENT=$ENVIRONMENT
EXPOSE 8080

CMD ["python3", "app.py"]
