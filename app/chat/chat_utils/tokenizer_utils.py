from transformers import GPT2Tokenizer

def truncate_conversation(conversation, max_tokens, tokenizer):
    current_tokens = 0
    truncated_conversation = []

    for message in reversed(conversation):
        message_tokens = len(tokenizer.tokenize(message["content"]))
        if current_tokens + message_tokens > max_tokens:
            break

        truncated_conversation.insert(0, message)
        current_tokens += message_tokens

    return truncated_conversation
