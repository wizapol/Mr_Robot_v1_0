import openai
import re
from app.memory import MemoryController
from app.plugins.plugins import PluginManager
from app.memory.redis_memory import RedisMemoryController
from transformers import GPT2Tokenizer
from app.chat.memory_patterns import check_remember_patterns

class ChatController:
    def __init__(self, api_key="", model=""):
        self.api_key = api_key
        self.model = model
        self.short_term_memory_controller = RedisMemoryController()
        self.long_term_memory_controller = MemoryController()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        openai.api_key = self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def set_model(self, model):
        self.model = model

    def _truncate_conversation(self, conversation, max_tokens):
        current_tokens = 0
        truncated_conversation = []

        for message in reversed(conversation):
            message_tokens = len(self.tokenizer.tokenize(message["content"]))
            if current_tokens + message_tokens > max_tokens:
                break

            truncated_conversation.insert(0, message)
            current_tokens += message_tokens

        return truncated_conversation

    def store_to_long_term_memory(self, message):
        long_term_memory = self.long_term_memory_controller.retrieve_memory("long_term_memory")

        if long_term_memory is None:
            long_term_memory = []
        else:
            long_term_memory = eval(long_term_memory)

        if isinstance(long_term_memory, list):
            long_term_memory.append(message)
        else:
            long_term_memory = [message]

        self.long_term_memory_controller.store_memory("long_term_memory", str(long_term_memory))

    def chat(self, message, context_length=100, max_response_length=2000, temperature=0.5):
        conversation = self.short_term_memory_controller.retrieve_memory("conversation")
        if conversation is None:
            conversation = []
        else:
            conversation = eval(conversation)

        conversation.append({"role": "user", "content": message})

        long_term_memory = self.long_term_memory_controller.retrieve_memory("long_term_memory")
        if long_term_memory is not None:
            long_term_memory = eval(long_term_memory)
            memory_summary = " ".join([mem["content"] for mem in long_term_memory])
        else:
            memory_summary = ""

        max_tokens = 4096 - max_response_length
        truncated_conversation = self._truncate_conversation(conversation, max_tokens)

        if long_term_memory is not None:
            prompt = [{"role": "system", "content": f"Your long-term memory includes the following information: {memory_summary}"}] + truncated_conversation
        else:
            prompt = [{"role": "system", "content": "You are a helpful AI assistant."}] + truncated_conversation

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            max_tokens=max_response_length,
            n=1,
            temperature=temperature,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.5
        )
        print(response)

        generated_response = response["choices"][0]["message"]["content"].strip()

        memory_content = check_remember_patterns(message)
        if memory_content:
            self.store_to_long_term_memory({"role": "memory", "content": memory_content})

        conversation.append({"role": "assistant", "content": generated_response})
        self.short_term_memory_controller.store_memory("conversation", str(conversation))
        plugin_manager = PluginManager()
        plugin_response = plugin_manager.apply_plugins(generated_response)
        processed_response = re.sub('[^0-9a-zA-ZáéíóúÁÉÍÓÚñÑ\n\.\?,!\'"()\-]+', ' ', plugin_response)
        return processed_response

    def delete_short_term_memory(self):
        self.short_term_memory_controller.delete_memory("conversation")

    def delete_long_term_memory(self):
        self.long_term_memory_controller.delete_memory("long_term_memory")

    def delete_all_memory(self):
        self.delete_short_term_memory()
        self.delete_long_term_memory()




