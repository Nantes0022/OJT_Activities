from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from peft import PeftModel
import torch

adapter_path = "/content/granite-lora-t4-adapter"

tokenizer = AutoTokenizer.from_pretrained(adapter_path, use_fast=True)

model = AutoModelForCausalLM.from_pretrained(
    adapter_path,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

model = PeftModel.from_pretrained(
    model,
    adapter_path,
    use_safetensors=True  
)

model.eval()


streamer = TextStreamer(tokenizer)

# Inference function
def generate_answer(question, max_new_tokens=256, temperature=0.7, top_p=0.9):
    prompt = f"Question: {question}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=top_p,
            temperature=temperature,
            eos_token_id=tokenizer.eos_token_id,
            streamer=streamer
        )

    full_output = tokenizer.decode(output[0], skip_special_tokens=True)
    answer = full_output.split("Answer:")[-1].strip()
    return answer

if __name__ == "__main__":
    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = generate_answer(question)
        print("\n---\nGenerated Answer:\n", answer)
