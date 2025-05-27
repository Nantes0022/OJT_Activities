from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_path = "gpt2-model"  

tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model.eval()  # set to eval mode

def gen_answer(question):
    prompt = "Question: "+ question +"Answer: "
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    output_ids = model.generate(
        input_ids,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=2,
        early_stopping=True,
    )

    generated_text = tokenizer.decode(output_ids[0], skips_special_tokens=True)
    return generated_text

while True:
    question = input("Enter Question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    answer = gen_answer(question)
    print(answer)
