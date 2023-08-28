import torch
import os
from threading import Thread
from google.cloud import storage
from transformers import LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig, TextIteratorStreamer, pipeline
from config import model_path, tokenizer_path, max_new_tokens, bucket_name, model_files, env

class Model:
    '''Client class for holding Llama2 model and tokenizer. Models are loaded according to 
    ENVIRONMENT environment variable
    '''
    def __init__(self, 
                 model_path:str=model_path, 
                 tokenizer_path:str=tokenizer_path,
                 max_new_tokens:int=max_new_tokens):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.max_new_tokens = max_new_tokens
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        #download files if running GCP
        if env == 'gcp':
            self.download_checkpoints(bucket_name=bucket_name)
        self.model = LlamaForCausalLM.from_pretrained(model_path, quantization_config=self.bnb_config)
        self.tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)


    def inference(self, query: str):
        '''Inference function for gradio text streaming'''
        query = "You are the US Supreme Court. What is your opinion on the following case? " + query
        batch = self.tokenizer(query, return_tensors='pt')

        generation_kwargs = dict(batch, streamer=self.streamer, max_new_tokens=self.max_new_tokens, repetition_penalty=1.1)
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        output= [[None, '']]
        
        for word in self.streamer:
            output[0][1] += word
            yield output

    def download_checkpoints(self, bucket_name: str = bucket_name):
        """Downloads model files from gcp storage if running in gcp."""
        
        if not(os.path.exists('model/')):
            os.mkdir('model')
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # get tokenizer
        blob = bucket.blob(self.tokenizer_path)
        blob.download_to_filename(self.tokenizer_path)
        
        # get model files to models/
        model_file_paths = [self.model_path + i for i in model_files]

        for object_name in model_file_paths:
            blob = bucket.blob(object_name)
            blob.download_to_filename(object_name)
        