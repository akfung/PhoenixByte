'''Set ENVIRONMENT to local for local app.py testing and spaces for running from docker image'''

import os
env  = os.environ.get('ENVIRONMENT', 'local')

if env == 'local':
    model_path = '../merged_llama2/'
    tokenizer_path = '../Llama2/7B/tokenizer.model'

elif env == 'spaces':
    model_path = 'akfung/llama_supreme'
    tokenizer_path = 'akfung/llama_supreme'

elif env == 'gcp':
    model_path = 'model/'
    tokenizer_path = 'tokenizer.model'
    bucket_name = 'phoenix-byte'
    os.environ["GCLOUD_PROJECT"] = "phoenix-byte"


max_new_tokens = os.environ.get('max_new_tokens', 100)

model_files = [
    'config.json',
    'generation_config.json',
    'pytorch_model-00001-of-00002.bin',
    'pytorch_model-00002-of-00002.bin',
    'pytorch_model.bin.index.json'
]

readme = "Provide a legal case description or click on Get Random Case to get a random case from Wikipedia's \
    pending US Supreme Court cases. Click run to generate the predicted US Supreme Court opinion."