# app/admin/admin.py

from flask import current_app, flash, render_template, request
from . import admin_bp
from app.chat import ChatController

# Crear una instancia de ChatController sin argumentos
chat_controller = ChatController()

@admin_bp.route("/admin/train", methods=["POST"])
def train():
    """Entrenar el modelo con datos proporcionados por el usuario."""
    training_data = request.form["training_data"]

    try:
        chat_controller.train(training_data)
        flash("Model training successful.", "success")
    except Exception as e:
        current_app.logger.error(f"Model training failed: {e}")
        flash("Model training failed.", "error")

    return render_template("admin/index.html")

@admin_bp.route("/admin/set-api-key", methods=["POST"])
def set_api_key():
    """Establecer la clave API de OpenAI."""
    api_key = request.form["api_key"]

    try:
        chat_controller.set_api_key(api_key)
        flash("API key set successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Failed to set API key: {e}")
        flash("Failed to set API key.", "error")

    return render_template("admin/index.html")

@admin_bp.route("/admin/set-model", methods=["POST"])
def set_model():
    """Establecer el modelo de OpenAI."""
    model = request.form["model"]

    try:
        chat_controller.set_model(model)
        flash("Model set successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Failed to set model: {e}")
        flash("Failed to set model.", "error")

    return render_template("admin/index.html")
