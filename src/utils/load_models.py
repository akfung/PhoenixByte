'''Utility functions for loading Llama2-7B-chat'''
from peft import PeftModel
import os
import torch
import bitsandbytes as bnb
from transformers import LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig
os.environ["CUDA_VISIBLE_DEVICES"]="0"

def load_llama(local:bool=False, model_path:str='', quantize:bool=True):
    '''Returns a quantized llama2-7b-chat model'''

    if local and not model_path:
        model_path = 'llama2-7b-chat/'
        tokenizer_path = model_path + 'tokenizer.model'
    elif not local:
        model_path = 'meta-llama/Llama-2-7b-chat-hf'
        tokenizer_path = model_path
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )


    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
    model = LlamaForCausalLM.from_pretrained(model_path, quantization_config = bnb_config, device_map='auto')

    return tokenizer, model

def merge_unload_lora(model, lora_adapter_path:str, save_path:str=''):
    '''Merge lora adapters into a loaded model'''
    model = PeftModel.from_pretrained(model, lora_adapter_path)
    model = model.merge_and_unload() 
    if save_path:
        model.save_pretrained(save_path)
    return model
