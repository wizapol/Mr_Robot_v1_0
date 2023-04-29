# app/chat/__init__.py

from flask import Blueprint

chat_bp = Blueprint("chat_bp", __name__)

from . import chat_routes

