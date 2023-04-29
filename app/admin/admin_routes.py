from flask import Blueprint, current_app, flash, jsonify, render_template, request
from app.chat.chat import ChatController

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.route("/admin", methods=["GET"])
def index():
    return render_template("admin/index.html")

@admin_routes.route("/admin/train", methods=["POST"])
def train():
    """Entrenar el modelo con datos proporcionados por el usuario."""
    training_data = request.form["training_data"]

    try:
        ChatController.train(training_data)
        flash("Model training successful.", "success")
    except Exception as e:
        current_app.logger.error(f"Model training failed: {e}")
        flash("Model training failed.", "error")

    return render_template("admin/index.html")

@admin_routes.route("/admin/plugins", methods=["GET"])
def list_plugins():
    """Listar todos los plugins disponibles en el sistema."""
    plugins = ChatController.plugin_manager.list_plugins()
    return jsonify(plugins)

@admin_routes.route("/admin/memory", methods=["GET"])
def view_memory():
    """Obtener el contenido actual de la memoria del bot."""
    memory = ChatController.memory_controller.view_memory()
    return jsonify(memory)

@admin_routes.route("/admin/memory", methods=["DELETE"])
def clear_memory():
    """Limpiar la memoria del bot."""
    ChatController.memory_controller.clear_memory()
    return jsonify({"message": "Memory cleared."})
