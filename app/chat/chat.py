import openai
import spacy
from app.memory import MemoryController
from app.plugins.plugins import PluginManager
from app.memory.redis_memory import RedisMemoryController
from transformers import GPT2Tokenizer
from app.chat.chat_utils.tokenizer_utils import truncate_conversation
from app.chat.chat_utils.response_utils import generate_response
from app.chat.memory_patterns import check_remember_patterns

nlp = spacy.load("es_core_news_md")

class ChatController:
    def __init__(self, api_key="", model=""):
        self.api_key = api_key
        self.model = model
        self.st_memory_ctrl = RedisMemoryController()
        self.lt_memory_ctrl = MemoryController()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        openai.api_key = self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def set_model(self, model):
        self.model = model

    def store_memory(self, message, memory_type):
        memory = self.lt_memory_ctrl.retrieve_memory(memory_type)

        if memory is None:
            memory = []
        else:
            memory = eval(memory)

        memory.append({"role": message["role"], "content": message["content"].replace('\r\n', '\n')})

        print(f"***Almacenando en {memory_type}: {message}")
        self.lt_memory_ctrl.store_memory(memory_type, str(memory))

    def find_related_memory(self, message):
        memory = self.lt_memory_ctrl.retrieve_memory("long_term_memory")
        if memory is not None:
            memory = eval(memory)
            related_memory = []

            message_doc = nlp(message.lower())
            for mem in memory:
                if "content" in mem and isinstance(mem["content"], str):
                    mem_doc = nlp(mem["content"].lower())
                    similarity = message_doc.similarity(mem_doc)
                    print(f"***Comparando '{message}' con '{mem['content']}': similitud = {similarity}")
                    if similarity > 0.5:
                        related_memory.append(mem)
            print(f"***Memoria a largo plazo: {memory}")
            print(f"***Memoria relacionada: {related_memory}")
            return related_memory if related_memory else None
        return None

    def process_response(self, response):
        plugin_manager = PluginManager()
        plugin_response = plugin_manager.apply_plugins(response)

        cleaned_response = plugin_response

        return cleaned_response

    def chat(self, message, context_length=100, max_response_length=2000, temperature=0.5):
        conversation = eval(self.st_memory_ctrl.retrieve_memory("conversation") or "[]")
        conversation.append({"role": "user", "content": message})

        memory_summary = " ".join([mem["content"] for mem in self.find_related_memory(message) or []])

        max_tokens = 4096 - max_response_length
        truncated_conversation = truncate_conversation(conversation, max_tokens, self.tokenizer)

        print(f"***Resumen de memoria: {memory_summary}")
        response = f"""{generate_response(self.model, memory_summary, truncated_conversation, max_response_length, temperature)}"""

        conversation.append({"role": "system", "content": response})
        self.st_memory_ctrl.store_memory("conversation", str(conversation))

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

