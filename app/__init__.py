from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from .chat import chat_bp
from .memory import memory_bp
from .plugins import plugins_bp
from . import db
from app.chat.chat_routes import chat_route


# Crear una instancia de SocketIO aquí
socketio = None

def create_app():
    global socketio
    app = Flask(__name__)
    
    chat_route(app)
    
    # Configurar a partir del archivo .env
    app.config.from_pyfile('../.env')

    # Inicializar la base de datos
    db.init_app(app)

    # Inicializar SocketIO
    socketio = SocketIO(app)

    # Registrar blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(memory_bp)
    app.register_blueprint(plugins_bp)

    # Agregar ruta para servir el archivo HTML
    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")
    return app, socketio
