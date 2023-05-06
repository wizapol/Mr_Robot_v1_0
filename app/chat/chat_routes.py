from flask import jsonify, request
from app.chat.chat import ChatController
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .env en la raíz del proyecto
api_key = os.getenv("OPENAI_API_KEY")  # Obtiene el valor de la variable de entorno "OPENAI_API_KEY"
model_name = os.getenv("MODEL_NAME")
chat_controller = ChatController(api_key=api_key, model=model_name)  # Inicializa el controlador de chat con la API Key cargada desde el archivo .env

print("Chat routes module loaded")  # Aviso de modulo Chat Routes Cargado

def chat_route(app):
    @app.route("/chat/message", methods=["POST", "GET"])
    def chat():
        if request.method == 'POST':
            """Responder a un mensaje enviado por el usuario."""
            print("***Chat route called***")
            message = request.json["message"]
            response = chat_controller.chat(message)
            return jsonify({"message": response})

    @app.route("/chat/edit_message", methods=["POST"])
    def edit_message():
        print("Edit message route called")
        message = request.json["message"]
        new_message = request.json["new_message"]
        chat_controller.edit_message(message, new_message)
        response = chat_controller.regenerate_response(new_message)
        return jsonify({"message": response})

    @app.route("/chat/regenerate_response", methods=["POST"])
    def regenerate_response():
        print("Regenerate response route called")
        message = request.json["message"]
        response = chat_controller.regenerate_response(message)
        return jsonify({"message": response})

    @app.route("/chat/delete_short_term_memory", methods=["POST"])
    def delete_short_term_memory():
        print("Delete short term memory route called")
        chat_controller.delete_short_term_memory()
        return jsonify({"status": "success", "message": "Short term memory deleted."})

    @app.route("/chat/delete_long_term_memory", methods=["POST"])
    def delete_long_term_memory():
        print("Delete long term memory route called")
        chat_controller.delete_long_term_memory()
        return jsonify({"status": "success", "message": "Long term memory deleted."})

    @app.route("/chat/delete_all_memory", methods=["POST"])
    def delete_all_memory():
        print("Delete all memory route called")
        chat_controller.delete_all_memory()
        return jsonify({"status": "success", "message": "All memory deleted."})
