# app/training/__init__.py

from flask import Blueprint

training_bp = Blueprint("training", __name__)

from . import training_routes
