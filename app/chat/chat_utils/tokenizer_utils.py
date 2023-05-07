from transformers import GPT2TokenizerFast, AutoTokenizer, AutoConfig

def truncate_conversation(conversation, model_name, tokenizer=None, max_tokens=None, debug=False):
    if tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    if max_tokens is None:
        model_config = AutoConfig.from_pretrained(model_name)
        max_tokens = model_config.max_position_embeddings

    truncated_conversation = []
    current_tokens = 0

    for message in reversed(conversation):
        message_tokens = len(tokenizer.encode(message["content"], return_tensors='pt')[0])
        print("tokens por mensaje:", message_tokens)  # Agregue esta línea
        if current_tokens + message_tokens > max_tokens:
            break

        truncated_conversation.insert(0, message)
        current_tokens += message_tokens
        
    print("tokens actuales:", current_tokens, "max tokens:", max_tokens)

    return truncated_conversation
