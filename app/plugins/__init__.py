# app/plugins/__init__.py

from flask import Blueprint

plugins_bp = Blueprint("plugins", __name__)

from . import plugins_routes
