from transformers import pipeline

def generate_answer(context, question):
    generator = pipeline("text-generation", model="gpt2")
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    return generator(prompt, max_length=150)[0]['generated_text']
