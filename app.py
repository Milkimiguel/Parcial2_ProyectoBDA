from flask import Flask
from flask_cors import CORS
import os
from extensions import mongo  # <--- Importa 'mongo' desde el nuevo archivo

# Importar los Blueprints (los archivos de rutas)
from routes.articulos import articulos_bp
from routes.categorias import categorias_bp
from routes.comentarios import comentarios_bp
from routes.tags import tags_bp
from routes.usuarios import usuarios_bp

# Crear la aplicación Flask
app = Flask(__name__)

# --- Configuración ---
CORS(app)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "")

# 3. Inicializar PyMongo
#    Usa .init_app() para conectar la extensión con la app
try:
    mongo.init_app(app) 
    print("Conexión a MongoDB Atlas exitosa.")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")

# --- Registrar los Blueprints (Endpoints) ---
# (Esto se queda igual)
app.register_blueprint(articulos_bp, url_prefix='/api/articulos')
app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')
app.register_blueprint(tags_bp, url_prefix='/api/tags')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

# --- Iniciar el servidor ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)