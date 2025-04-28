import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
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
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained("gpt2")

dataset = QADataset(data, tokenizer)

print(dataset)









