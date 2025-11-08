from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

# Importar los Blueprints (los archivos de rutas)
from routes.articulos import articulos_bp
from routes.categorias import categorias_bp
from routes.comentarios import comentarios_bp
from routes.tags import tags_bp
from routes.usuarios import usuarios_bp

# Crear la aplicación Flask
app = Flask(__name__)

# --- Configuración ---

# 1. Habilitar CORS: Permite que tu JS (frontend) se comunique con este backend
CORS(app)

# 2. Configurar MongoDB Atlas
# (Reemplaza con tu cadena de conexión)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb+srv://<usuario>:<password>@<tu-cluster>.mongodb.net/<tu-db>?retryWrites=true&w=majority")

# 3. Inicializar PyMongo
# Esta variable 'mongo' estará disponible en todas tus rutas
try:
    mongo = PyMongo(app)
    print("Conexión a MongoDB Atlas exitosa.")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")

# --- Registrar los Blueprints (Endpoints) ---
# Le decimos a Flask que todas estas rutas empiezan con /api
app.register_blueprint(articulos_bp, url_prefix='/api/articulos')
app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')
app.register_blueprint(tags_bp, url_prefix='/api/tags')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

# --- Iniciar el servidor ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)