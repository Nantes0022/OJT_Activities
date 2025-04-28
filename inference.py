from transformers import AutoTokenizer, AutoModelForCausalLM

# Load fine-tuned model and tokenizer
model_path = "gpt2-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token  # Ensure correct padding
model = AutoModelForCausalLM.from_pretrained(model_path)

# Function to generate answers
def generate_answer(question):
    prompt = f"Q: {question}\nA:"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    output = model.generate(input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id, temperature=0.3)
    answer = tokenizer.decode(output[0], skip_special_tokens=True).replace("Question:", "").strip()
    
    return answer

# Loop input for multiple queries
while True:
    question = input("Enter Question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    answer = generate_answer(question)
    print(f"Generated answer: {answer}")