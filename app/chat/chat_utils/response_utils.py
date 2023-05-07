import openai

def generate_response(model, memory_summary, truncated_conversation, max_response_length, temperature):
    if memory_summary:
        prompt = [{"role": "system", "content": f"Long-term memory:{memory_summary}, context: {truncated_conversation}"}]
    else:
        prompt = [{"role": "system", "content": f"una AI entrenada para programmar"}] + truncated_conversation

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
    print("prompt al modelo:", prompt)
    print("respuesta del modelo:", response)

    return response["choices"][0]["message"]["content"].strip()
