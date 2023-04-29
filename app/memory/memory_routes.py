from flask import Blueprint, request, jsonify
from .memory import MemoryController
from . import memory_bp


memory_bp = Blueprint('memory', __name__)
memory_controller = MemoryController()

@memory_bp.route('/memory/store', methods=['POST'])
def store_memory():
    key = request.form.get('key')
    value = request.form.get('value')
    memory_controller.store_memory(key, value)
    return jsonify({"result": "success"})

@memory_bp.route('/memory/retrieve', methods=['GET'])
def retrieve_memory():
    key = request.args.get('key')
    value = memory_controller.retrieve_memory(key)
    return jsonify({"result": value})

@memory_bp.route('/memory/delete', methods=['DELETE'])
def delete_memory():
    key = request.form.get('key')
    memory_controller.delete_memory(key)
    return jsonify({"result": "success"})
