# app/training/training_routes.py

from flask import render_template
from . import training_bp

@training_bp.route("/training")
def training_index():
    """Renderizar la página de entrenamiento del modelo."""
    return render_template("training/index.html")
