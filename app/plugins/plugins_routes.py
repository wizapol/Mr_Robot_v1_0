from flask import Blueprint, request, jsonify
from .plugins import PluginManager

plugins_bp = Blueprint("plugins", __name__, url_prefix="/plugins")

plugin_manager = PluginManager()

@plugins_bp.route("/load", methods=["POST"])
def load_plugins():
    response = plugin_manager.load_plugins()
    return jsonify(response)

@plugins_bp.route("/unload", methods=["POST"])
def unload_plugins():
    response = plugin_manager.unload_plugins()
    return jsonify(response)
