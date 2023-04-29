from .memory import MemoryController

__all__ = [
    "MemoryController"
]
from flask import Blueprint

memory_bp = Blueprint("memory", __name__, url_prefix="/memory")

from . import memory_routes
