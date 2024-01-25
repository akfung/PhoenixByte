'''Set ENVIRONMENT to local for local app.py testing and spaces for running from docker image'''

import os

env  = os.environ.get('ENVIRONMENT', 'local')

if env == 'local':
    from dotenv import load_dotenv

    model_path = '../merged_llama2/'
    tokenizer_path = '../Llama2/7B/tokenizer.model'
    load_dotenv()

elif env == 'spaces':
    model_path = 'akfung/llama_supreme'
    tokenizer_path = 'akfung/llama_supreme'

elif env == 'gcp':
    model_path = 'model/'
    tokenizer_path = 'tokenizer.model'
    bucket_name = 'phoenix-byte'
    os.environ["GCLOUD_PROJECT"] = "phoenix-byte"

conn_s = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(user=os.environ.get('DB_USER'),
                                                                         password=os.environ.get('DB_PASSWORD'),
                                                                         host=os.environ.get('DB_HOST'),  
                                                                         port=os.environ.get('DB_PORT'), 
                                                                         db_name=os.environ.get('DB_NAME'),
                                                                         )

justice_names = {'Alito',
    'Barrett',
    'Breyer',
    'Ginsburg',
    'Gorsuch',
    'Jackson',
    'Kagan',
    'Kavanaugh',
    'Kennedy',
    'Roberts',
    'Scalia',
    'Sotomayor',
    'Thomas',}

headers = {
    "Authorization": os.environ.get('runpod_api_key'),
    "Content-Type": "application/json"
}

embedding_path = os.environ.get('EMBEDDING_PATH')
streaming_url = os.environ.get('STREAMING_URL')
job_url = os.environ.get('JOB_URL')

default_payload = { "input": {
        "prompt": "Who is the president of the United States?",
        "apply_chat_template": True,
        "sampling_params": {
            "max_tokens": os.environ.get('max_new_tokens', 400),
            "n": 1,
            "best_of": None,
            "presence_penalty": 0.6,
            "frequency_penalty": 0,
            "temperature": 0.7,
            "top_k": 6,
            "use_beam_search": False,
            "stop": ["USER"],
            "ignore_eos": False,
            "logprobs": None
        }
    } }

max_new_tokens = os.environ.get('max_new_tokens', 100)

readme = """Provide a legal case description or click on Get Random Case to get a random case from Wikipedia's
    pending US Supreme Court cases. Choose a Supreme Court Justice to generate opinions according to what that particular Justice might
    have to say about this case, or select Court to generate opinions based on what the majority opinion might be.Click run to generate the predicted US Supreme Court opinion."""

