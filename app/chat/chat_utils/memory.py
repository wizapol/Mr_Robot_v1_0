def process_memory(conversation, message, long_term_memory_controller):
    if conversation is None:
        conversation = []
    else:
        conversation = eval(conversation)

    conversation.append({"role": "user", "content": message})

    related_memory = find_related_memory(message, long_term_memory_controller)
    if related_memory is not None:
        memory_summary = " ".join([mem["content"] for mem in related_memory])
    else:
        memory_summary = ""

    return conversation, memory_summary

def find_related_memory(message, long_term_memory_controller):
    long_term_memory = long_term_memory_controller.retrieve_memory("long_term_memory")
    if long_term_memory is not None:
        long_term_memory = eval(long_term_memory)
        related_memory = [mem for mem in long_term_memory if "content" in mem and message.lower() in mem["content"].lower()]
        return related_memory if related_memory else None
    return None
