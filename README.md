## Introduction 

In the leadup to many US Supreme Court cases, there is often rampant speculation and forecasting by legal experts, the media, and the general public as to what the outcome will be. There is sometimes consensus on the expected rulings, which seem to be based on the existing rulings made by the court and its Justices. Predictions based on existing publicly accessible text? Sounds like a deep learning project! This project makes a rudimentary attempt at predicting the Supreme Court’s ruling on a case when provided a brief overview of the case.

## Training Data

Training data for this project was gathered from Justia using the basic requests library. It consists of case summaries and court opinions dating back to 2013, consisting of 762 cases and over 10M tokens. I collected both court opinions and the opinions of individual justices, but at the current time only the court opinions were used for fine tuning.

## Model
The base model is Meta’s Llama2 7B, chosen because it can be trained on an 8GB consumer GPU with quantization. The model finetuning was performed on a laptop RTX 4060 using 4bit normal float quantization and Low-Rank adapters through the Hugging Face transformers and PEFT libraries. LoRA updates were merged with the model following training completion.

## Deployment
This app runs as a gradio app inside a docker container deployed to Google Cloud Run on a T4 instance. The model weights themselves are stored on Google Cloud storage.
