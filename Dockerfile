# FROM python:3.8.17
# FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel
FROM python:3.8.18

WORKDIR /code
   
COPY ./requirements.txt /code/requirements.txt

RUN apt update

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .
RUN mkdir /code/embedding_model/
# RUN chmod +x /code/embedding_setup.sh
RUN python setup.py

EXPOSE 7860

# CMD ["python "app.py" "--port", "7860"]
CMD python app.py --port 7860
