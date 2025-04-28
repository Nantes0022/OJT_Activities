import json
from datasets import Dataset 
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments


dataset_path = "data.json"
data = json.load(open(dataset_path, "r", encoding="utf-8"))


dataset = Dataset.from_list(data) 
dataset = dataset.train_test_split(test_size=0.2)  


tokenizer = AutoTokenizer.from_pretrained("gpt2") 
tokenizer.pad_token = tokenizer.eos_token 
model = AutoModelForCausalLM.from_pretrained("gpt2") 

def tokenize_function(example):
    prompt = f"Question: {example['prompt']} Answer: {example['completion']}" 
    encoding = tokenizer(prompt, truncation=True, padding="max_length", max_length=512) 
    return {"input_ids": encoding["input_ids"], "labels": encoding["input_ids"]}


dataset = dataset.map(tokenize_function) 

train_dataset = dataset["train"]
eval_dataset = dataset["test"]
training_args = TrainingArguments( 
    output_dir="gpt2-training",
    per_device_train_batch_size=1,  
    num_train_epochs=20,  
    eval_strategy="epoch",
    save_steps=500,  
    save_total_limit=1,  
    logging_dir="./logs",
    logging_steps=10,  
    learning_rate=5e-5,  
    warmup_steps=10, 
    weight_decay=0.01, 
    remove_unused_columns=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# Train model
trainer.train()

# Save model
model.save_pretrained("gpt2-model")
tokenizer.save_pretrained("gpt2-model")

print("Fine-tuning complete!")