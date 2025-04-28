import json
from datasets import Dataset #Import the Dataset library for pre processing ng data
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments #Utilities for training Hugging Face Models


dataset_path = "data.json"
data = json.load(open(dataset_path, "r", encoding="utf-8")) #Loads the JSON DATA


dataset = Dataset.from_list(data) #Convert JSON Data To Hugging Face Dataset
dataset = dataset.train_test_split(test_size=0.2)  # 80% train, 20% validation
#The dataset split into two which is training set(data the model sees during training);and
#Validation Which an unseen data, ginagamit para sa pag evaluate ng performance like this
###Sample Data based doon sa pag evaluation ng pagbuild ng Model AI

# {'eval_loss': 0.3388477861881256, 'eval_runtime': 1.9052, 'eval_samples_per_second': 1.575, 'eval_steps_per_second': 0.525, 'epoch': 1.0}        
# {'eval_loss': 0.2183121293783188, 'eval_runtime': 1.9045, 'eval_samples_per_second': 1.575, 'eval_steps_per_second': 0.525, 'epoch': 2.0}
# {'eval_loss': 0.14282657206058502, 'eval_runtime': 1.8794, 'eval_samples_per_second': 1.596, 'eval_steps_per_second': 0.532, 'epoch': 3.0}
# {'eval_loss': 0.08570582419633865, 'eval_runtime': 1.8083, 'eval_samples_per_second': 1.659, 'eval_steps_per_second': 0.553, 'epoch': 4.0}
# {'eval_loss': 0.058933358639478683, 'eval_runtime': 1.8761, 'eval_samples_per_second': 1.599, 'eval_steps_per_second': 0.533, 'epoch': 5.0}
# {'eval_loss': 0.05235637351870537, 'eval_runtime': 1.8481, 'eval_samples_per_second': 1.623, 'eval_steps_per_second': 0.541, 'epoch': 6.0}
# {'eval_loss': 0.04461568221449852, 'eval_runtime': 1.9157, 'eval_samples_per_second': 1.566, 'eval_steps_per_second': 0.522, 'epoch': 7.0}
# {'eval_loss': 0.03512850031256676, 'eval_runtime': 1.8204, 'eval_samples_per_second': 1.648, 'eval_steps_per_second': 0.549, 'epoch': 8.0}
# {'eval_loss': 0.031860243529081345, 'eval_runtime': 1.9029, 'eval_samples_per_second': 1.577, 'eval_steps_per_second': 0.526, 'epoch': 9.0}
# {'eval_loss': 0.02991507202386856, 'eval_runtime': 1.8971, 'eval_samples_per_second': 1.581, 'eval_steps_per_second': 0.527, 'epoch': 10.0}     
# {'eval_loss': 0.02938481606543064, 'eval_runtime': 1.9118, 'eval_samples_per_second': 1.569, 'eval_steps_per_second': 0.523, 'epoch': 11.0}
# {'eval_loss': 0.031365782022476196, 'eval_runtime': 1.9567, 'eval_samples_per_second': 1.533, 'eval_steps_per_second': 0.511, 'epoch': 12.0}
# {'eval_loss': 0.032317306846380234, 'eval_runtime': 1.9964, 'eval_samples_per_second': 1.503, 'eval_steps_per_second': 0.501, 'epoch': 13.0}
# {'eval_loss': 0.03258664160966873, 'eval_runtime': 1.9547, 'eval_samples_per_second': 1.535, 'eval_steps_per_second': 0.512, 'epoch': 14.0}
# {'eval_loss': 0.0300530344247818, 'eval_runtime': 1.9432, 'eval_samples_per_second': 1.544, 'eval_steps_per_second': 0.515, 'epoch': 15.0}
# {'eval_loss': 0.03145013377070427, 'eval_runtime': 1.9554, 'eval_samples_per_second': 1.534, 'eval_steps_per_second': 0.511, 'epoch': 16.0}
# {'eval_loss': 0.03273295611143112, 'eval_runtime': 1.9388, 'eval_samples_per_second': 1.547, 'eval_steps_per_second': 0.516, 'epoch': 17.0}
# {'eval_loss': 0.03135867416858673, 'eval_runtime': 2.0341, 'eval_samples_per_second': 1.475, 'eval_steps_per_second': 0.492, 'epoch': 18.0}
# {'eval_loss': 0.03076007403433323, 'eval_runtime': 1.9669, 'eval_samples_per_second': 1.525, 'eval_steps_per_second': 0.508, 'epoch': 19.0}
# {'eval_loss': 0.03060574270784855, 'eval_runtime': 1.989, 'eval_samples_per_second': 1.508, 'eval_steps_per_second': 0.503, 'epoch': 20.0}  


tokenizer = AutoTokenizer.from_pretrained("gpt2") #Loads GPT-2 Tokenizer
tokenizer.pad_token = tokenizer.eos_token #Padding Tokens
model = AutoModelForCausalLM.from_pretrained("gpt2") #Loads GPT-2 Model

def tokenize_function(example):
    prompt = f"Question: {example['prompt']} Answer: {example['completion']}" #Formatting ng prompt and answer 
    encoding = tokenizer(prompt, truncation=True, padding="max_length", max_length=512) 
    #I Totokenize yung nasa taas para maging machine readable dahil tokens ang ginagamit para makapagcommunicate sa AI
    return {"input_ids": encoding["input_ids"], "labels": encoding["input_ids"]} #Then return ang mga input_ids and labels


dataset = dataset.map(tokenize_function) #Imamap nya ang tokens na mangagaling sa function which is ung data ay galing doon sa data.json

train_dataset = dataset["train"] #Ni assign para gamitin sa pag train 
eval_dataset = dataset["test"] #Ni assign for validation of Model AI

training_args = TrainingArguments( 
    output_dir="gpt2-training", # Kung saan masasave ang bawat checkpoint sa pagtatrain
    per_device_train_batch_size=1,  #Parameter ito na dito dinedefine ang size ng pagtatrain for gradient_norm
    #connected ang tatlo ung train loss, eval_loss and gradient, ayon sa aking pag reresearch research kapag mababa daw ang tatlong ito ay stable daw ang learning ng Model AI
    #Kapag hindi maaari daw may overfitting or may instability, need i optimize ung training args
    num_train_epochs=20,  # Need na numbers of training
    #The smaller the data, The more it need epochs dahil ang Model ay need ng more repetitions para ma learn ang patterns ng iyong dataset
    #Kabaligtaran naman kapag large ang data
    eval_strategy="epoch", # Set to epoch para kada epoch ay lalabas ang output ng training pero need ito i pass sa trainer
    save_steps=500,  # About sa pagsasave para daw kapag may case na nag crash ay hindi daw mawawala ang progress and pwede mo daw i continue yon
    save_total_limit=1,  # Keep only the latest checkpoint
    logging_dir="./logs",
    logging_steps=10,  # Log more frequently for monitoring
    learning_rate=5e-5,  # Slightly lower learning rate for stability
    warmup_steps=10,  # Helps gradual training
    weight_decay=0.01,  # Adds regularization to prevent overfitting
    remove_unused_columns=False
)

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