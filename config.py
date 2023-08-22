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

max_new_tokens = os.environ.get('max_new_tokens', 100)