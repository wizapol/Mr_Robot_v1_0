from transformers import GPT2Tokenizer

import openai

def generate_response(model, memory_summary, truncated_conversation, max_response_length, temperature):
    if memory_summary:
        prompt = [{"role": "system", "content": "Una AI ayudante"}] + [{"role": "system", "content": f"Long-term memory: {memory_summary}"}] + truncated_conversation
    else:
        prompt = [{"role": "system", "content": "Una AI ayudante"}] + truncated_conversation
    temperature = 0.5
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        max_tokens=max_response_length,
        n=1,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    print("respuesta del modelo:", response)
    return response["choices"][0]["message"]["content"].strip()
