import json
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, EarlyStoppingCallback,
    DataCollatorForLanguageModeling
)

# Load your data
dataset_path = "dataset.json"
data = json.load(open(dataset_path, "r", encoding="utf-8"))

dataset = Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.2)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("gpt2")

def mask_labels(labels, pad_token_id=50256, ignore_index=-100):
    # Find all positions of pad_token_id
    pad_positions = [i for i, token_id in enumerate(labels) if token_id == pad_token_id]

    if not pad_positions:
        # No pad token found, just return labels unchanged
        return labels

    # Keep one pad_token_id - for example, the last one
    keep_index = pad_positions[-1]

    # Create a copy of labels
    new_labels = list(labels)

    # Replace all pad_token_id except the one at keep_index with -100
    for i in pad_positions:
        if i != keep_index:
            new_labels[i] = ignore_index

    return new_labels

# Tokenization function
def tokenize_function(example):
    prompt = f"Question: {example['prompt']} Answer: {example['completion']}{tokenizer.eos_token}"
    encoding = tokenizer(
        prompt,
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    input_ids = encoding["input_ids"]

    labels = mask_labels(input_ids, pad_token_id=tokenizer.pad_token_id, ignore_index=-100)

    return {
        "input_ids": input_ids,
        "attention_mask": encoding["attention_mask"],
        "labels": labels,
    }


# Apply tokenization
dataset = dataset.map(tokenize_function, batched=False)
token_id = dataset["train"]["labels"][0]
filtered_token_ids = [tid for tid in token_id if tid != -100]
decoded_text = tokenizer.decode(filtered_token_ids, clean_up_tokenization_spaces=True)

print(decoded_text)


# Use a data collator for causal language modeling (no masking)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # GPT-2 is causal LM, so no masking
)

# Training arguments
training_args = TrainingArguments(
    output_dir="/content/gpt2-finetuned",
    overwrite_output_dir=True,
    eval_strategy="steps",
    eval_steps=500,
    logging_steps=500,
    save_steps=500,
    save_total_limit=2,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    warmup_steps=500,
    weight_decay=0.01,
    learning_rate=5e-5,
    logging_dir="./logs",
    load_best_model_at_end=True,
    fp16=True,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)

trainer.train(resume_from_checkpoint="/content/gpt2-finetuned/checkpoint-2500")


# Save the model (including config, weights) and tokenizer from the Trainer object
trainer.save_model("./gpt2-finetuned-final")

# Save the tokenizer explicitly from the trainer
trainer.tokenizer.save_pretrained("./gpt2-finetuned-final")



