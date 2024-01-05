from peft import prepare_model_for_kbit_training
from peft import LoraConfig, get_peft_model
import transformers

'''Dataset loading'''
from datasets import load_dataset

def process_dataset(sample, max_target_length: int = 4000):
    '''Process dataset labels if necessary''' 
    model_inputs = tokenizer(
        sample["summary"],
        truncation=True,
    )
    labels = tokenizer(
        sample["opinion"], max_length=max_target_length, truncation=True
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def load_case_dataset(dataset_path:str=''):
    '''dataset loader function, needs dataset path'''
    dataset = load_dataset('json', data_files='chunked_case_data.json', field='data')
    dataset = dataset.map(process_dataset, batched=True)
    dataset = dataset.map(lambda samples: tokenizer(samples["opinion"]), batched=True)
    return dataset


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """

    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )
def train_model(model, save_path:str=''):
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)

    config = LoraConfig(
        r=8, 
        lora_alpha=32, 
        target_modules=["q_proj", "v_proj"], 
        lora_dropout=0.05, 
        bias="none", 
        task_type="CAUSAL_LM"
    )
    
    tokenizer.pad_token = tokenizer.eos_token
    trainer = transformers.Trainer(
        model=model, 
        train_dataset=dataset['train'],
        args=transformers.TrainingArguments(
            per_device_train_batch_size=1, 
            gradient_accumulation_steps=4,
            warmup_steps=100, 
            max_steps=200, 
            learning_rate=2e-4, 
            fp16=True,
            logging_steps=1, 
            output_dir='outputs'
        ),
        data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    trainer.train()
    model = get_peft_model(model, config)
    print_trainable_parameters(model)
    if save_path:
        model.save_pretrained('./llama2_lora_4k/')
    return model
