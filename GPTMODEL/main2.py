import json
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch

# Load dataset from JSON file
def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

class QADataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = [f"Question: {item['question']} Answer: {item['answer']}" for item in data]
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        encoding = self.tokenizer(self.data[idx], truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt")
        input_ids = encoding["input_ids"].squeeze()
        return {"input_ids": input_ids, "labels": input_ids}

# Load dataset from file
dataset_path = "data.json"
data = load_dataset(dataset_path)

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.3-2b-base")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("ibm-granite/granite-3.3-2b-base")

dataset = QADataset(data, tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir="granite_finetuned",
    per_device_train_batch_size=1,  # Smaller batch size due to limited data
    num_train_epochs=20,  # Increase epochs since data is minimal
    save_steps=500,  # Reduce save frequency
    save_total_limit=1,  # Keep only the latest checkpoint
    logging_dir="./logs",
    logging_steps=10,  # Log more frequently for monitoring
    learning_rate=5e-5,  # Slightly lower learning rate for stability
    warmup_steps=10,  # Helps gradual training
    weight_decay=0.01,  # Adds regularization to prevent overfitting
)


# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Train model
trainer.train()

# Save model
model.save_pretrained("granite_finetuned")
tokenizer.save_pretrained("granite_finetuned")

print("Fine-tuning complete!")