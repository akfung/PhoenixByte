# FROM python:3.8.17
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel

WORKDIR /code

# Get model artifacts from google cloud storage
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-cli -y
      
COPY ./requirements.txt /code/requirements.txt

RUN apt update

# RUN apt-get install -y python3 python3-pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 7860

CMD ["python3", "app.py"]
