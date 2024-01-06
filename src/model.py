import os
import requests
import time
# from google.cloud import storage
from sentence_transformers import SentenceTransformer

from .config import max_new_tokens, streaming_url, job_url, default_payload, headers
from .db.db_utilities import query_db

class Model:
    '''Client class for holding Llama2 model and tokenizer. Models are loaded according to 
    ENVIRONMENT environment variable
    '''
    def __init__(self, 
                 max_new_tokens:int=max_new_tokens):
        self.max_new_tokens = max_new_tokens
        # self.embedding_model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
        self.embedding_model = SentenceTransformer('/embedding_model/')


    def inference(self, query:str, table:str):
        '''Inference function for gradio text streaming'''
        # set in the case that None
        if table == 'Court' or table is None:
            table= 'court_opinion'
        output= [[None, '']]

        for i in self.query_model(query, table):
            output[0][1] += i
            yield output

    def get_context(self, query:str, table:str='court_opinion')-> str:
        """Query vectordb for additional context and compiles a new query string with added context"""
        matches = query_db(query, self.embedding_model, table=table)
        if len(matches) > 0:
            match = '"""' + matches[0][0] + '"""'

            context = "Use the following historical opinion delimited by tripple quotes to give your ruling on a court case description. " + match + " Description: "
        else:
            context = 'Give your ruling on a court case description. Description:'

        return context + query + " Answer in less than 400 words and without a self introduction."

    def query_model(self, query:str, table:str, default_payload:dict=default_payload, timeout:int=60, **kwargs) -> str:
        """Query the model api on runpod. Runs for 60s by default. Generator response until job is complete"""

        augmented_prompt = self.get_context(query=query, table=table)
        for k,v in kwargs:
            default_payload['input']['sampling_params'][k] = v
        default_payload["input"]["prompt"] = augmented_prompt
        job_id = requests.post(job_url, json=default_payload, headers=headers).json()['id']
        for i in range(timeout):
            time.sleep(1)
            stream_response = requests.get(streaming_url+ job_id, headers=headers).json()
            if stream_response['status'] == 'COMPLETED':
                break
            for i in stream_response['stream']:
                for j in i['output']['text']:
                    yield j


    # def download_checkpoints(self, bucket_name: str = bucket_name):
    #     """Downloads model files from gcp storage if running in gcp."""
        
    #     if not(os.path.exists('model/')):
    #         os.mkdir('model')
    #     storage_client = storage.Client()
    #     bucket = storage_client.bucket(bucket_name)

    #     # get tokenizer
    #     blob = bucket.blob(self.tokenizer_path)
    #     blob.download_to_filename(self.tokenizer_path)
        
    #     # get model files to models/
    #     model_file_paths = [self.model_path + i for i in model_files]

    #     for object_name in model_file_paths:
    #         blob = bucket.blob(object_name)
    #         blob.download_to_filename(object_name)
        