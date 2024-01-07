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

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

RUN pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

EXPOSE 7860
CMD python app.py
