from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(context, question):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # ✅ Initial request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1500,
        temperature=0.85,  # Increased for diversity
    )

    # ✅ Capture the first response
    answer = response.choices[0].message.content.strip()

    # ✅ Continuation logic with more dynamic prompting
    while response.choices[0].finish_reason != 'stop':
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Continue elaborating on this response without repeating:\n\n{answer}"}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000,
            temperature=0.85,
        )

        continuation = response.choices[0].message.content.strip()

        # ✅ Avoid appending if it's a duplicate
        if continuation in answer:
            break

        answer += " " + continuation

    return answer
