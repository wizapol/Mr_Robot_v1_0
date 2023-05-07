import json
import openai
import spacy
from app.memory import MemoryController
from app.plugins.plugins import PluginManager
from app.memory.redis_memory import RedisMemoryController
from transformers import GPT2TokenizerFast
from app.chat.chat_utils.tokenizer_utils import truncate_conversation
from app.chat.chat_utils.response_utils import generate_response
from app.chat.memory_patterns import check_remember_patterns

nlp = spacy.load("es_core_news_md")


class ChatController:
    def __init__(self, api_key="", model=""):
        if not api_key:
            raise ValueError("API key is required.")
        if not model:
            raise ValueError("Model name is required.")
        self.api_key = api_key
        self.model = model
        self.st_memory_ctrl = RedisMemoryController()
        self.lt_memory_ctrl = MemoryController()
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        openai.api_key = self.api_key

    def set_api_key(self, api_key):
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key
        openai.api_key = self.api_key

    def set_model(self, model):
        if not model:
            raise ValueError("Model name is required.")
        self.model = model

    def store_memory(self, message, memory_type):
        try:
            memory = self.lt_memory_ctrl.retrieve_memory(memory_type)
            memory = json.loads(memory) if memory else []
            memory.append({"role": message["role"], "content": message["content"].replace('\r\n', '\n')})
            self.lt_memory_ctrl.store_memory(memory_type, json.dumps(memory))
            print("Memory stored:", memory)
        except Exception as e:
            print(f"Error storing memory: {e}")

    def find_related_memory(self, message):
        try:
            memory = self.lt_memory_ctrl.retrieve_memory("long_term_memory")
            if memory:
                memory = json.loads(memory)
                return [mem for mem in memory if nlp(message.lower()).similarity(nlp(mem["content"].lower())) > 0.5]
            return None
        except Exception as e:
            print(f"Error finding related memory: {e}")

    def process_response(self, response):
        plugin_manager = PluginManager()
        return plugin_manager.apply_plugins(response)

    def chat(self, message, max_response_length=3000, temperature=0.5, edited_message=None):
        conversation = json.loads(self.st_memory_ctrl.retrieve_memory("conversation") or "[]")
        message = edited_message or message
        conversation.append({"role": "user", "content": message})
        print("Mensaje del usuario:", message)
        print("Conversación completa:", conversation)


        memory_summary = " ".join([mem["content"] for mem in self.find_related_memory(message) or []])
        #print the memory comparation
        print("Memoria comparada:", memory_summary)
        truncated_conversation = truncate_conversation(conversation, self.model, self.tokenizer, 4096 - max_response_length)
        print("Conversación truncada:", truncated_conversation)

        response = generate_response(self.model, memory_summary, truncated_conversation, max_response_length, temperature)

        conversation.append({"role": "system", "content": response})
        self.st_memory_ctrl.store_memory("conversation", json.dumps(conversation))

        memory_content = check_remember_patterns(message)
        if memory_content:
            self.store_memory({"role": "system", "content": memory_content.replace('\r\n', '\n')}, "long_term_memory")
        return self.process_response(response)


    def delete_short_term_memory(self):
        self.st_memory_ctrl.delete_memory("conversation")

    def delete_long_term_memory(self):
        self.lt_memory_ctrl.delete_memory("long_term_memory")

    def delete_all_memory(self):
        self.delete_short_term_memory()
        self.delete_long_term_memory()

