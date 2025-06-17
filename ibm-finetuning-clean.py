from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch
import json
from datasets import Dataset

model_id = "ibm-granite/granite-3.3-2b-base"

tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True  
)

model = prepare_model_for_kbit_training(model)

#Config ng LoRA
lora_config = LoraConfig(
    r=8,                 

    lora_alpha=32,       
    target_modules=["q_proj", "v_proj"],  
    lora_dropout=0.05, 
    bias="none",
    task_type="CAUSAL_LM",
)

# Then wrap it with PEFT lora config
model = get_peft_model(model, lora_config)

model.gradient_checkpointing_enable()

# Fine-tuning Dataset
dataset_path = "/content/datasets/dataset.json"
data = json.load(open(dataset_path, "r", encoding="utf-8"))

dataset = Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.2)

def mask_labels(labels, pad_token_id=None, ignore_index=-100):
    if pad_token_id is None:
        pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id

    pad_positions = [i for i, token_id in enumerate(labels) if token_id == pad_token_id]
    if not pad_positions:
        return labels
    keep_index = pad_positions[-1]
    return [token if i == keep_index else ignore_index for i, token in enumerate(labels)]

# Tokenization function
import numpy as np

def tokenize_function(batch):
    input_ids_batch = []
    attention_mask_batch = []
    labels_batch = []
    topic_batch = []
    difficulty_batch = []

    metadata_list = batch.get("metadata", [{}] * len(batch["prompt"]))

    for i in range(len(batch["prompt"])):
        prompt = f"Question: {batch['prompt'][i]}\nAnswer:"
        completion = f" {batch['completion'][i]}{tokenizer.eos_token}"

        full_input = prompt + completion
        encoding = tokenizer(
            full_input,
            truncation=True,
            max_length=512,
            padding="max_length"
        )

        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        prompt_len = len(prompt_ids)

        labels = [-100] * prompt_len + encoding["input_ids"][prompt_len:]
        labels = labels[:512] + [-100] * (512 - len(labels))

        input_ids_batch.append(encoding["input_ids"])
        attention_mask_batch.append(encoding["attention_mask"])
        labels_batch.append(labels)

        metadata = metadata_list[i] if i < len(metadata_list) else {}

        topic_batch.append(metadata.get("topic", "unknown"))
        difficulty_batch.append(metadata.get("difficulty", "unknown"))

    return {
        "input_ids": np.array(input_ids_batch),
        "attention_mask": np.array(attention_mask_batch),
        "labels": np.array(labels_batch),
        "topic": topic_batch,
        "difficulty": difficulty_batch
    }


tokenized_dataset = dataset.map(tokenize_function, batched=True)


training_args = TrainingArguments(
    output_dir="./granite-lora-t4",
    gradient_accumulation_steps=8,  
    learning_rate=3e-4,
    fp16=True,
    logging_steps=10,
    save_steps=20,
    eval_strategy="steps",
    save_total_limit=2,
    max_steps=1000,
    warmup_steps=50,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model("./granite-base-and-adapter")
tokenizer.save_pretrained("./granite-base-and-adapter")
