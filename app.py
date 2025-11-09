from flask import Flask, jsonify  # ← Agregar jsonify aquí
from flask_cors import CORS
import os
from extensions import mongo
from bson import json_util  # ← Agregar esto
import json  # ← Agregar esto
from pymongo import MongoClient
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
MONGO_URI = ""
app.config["MONGO_URI"] = MONGO_URI

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

# --- Endpoints de Debug Mejorados ---
@app.route('/api/debug/connection')
def debug_connection():
    """Verifica la conexión y muestra información básica de la DB"""
    try:
        # Verificar conexión
        mongo.db.command('ping')
        
        # Obtener información de la base de datos
        db_name = mongo.db.name
        collections = mongo.db.list_collection_names()
        
        # Contar documentos en cada colección
        collection_counts = {}
        for collection_name in collections:
            count = mongo.db[collection_name].count_documents({})
            collection_counts[collection_name] = count
        
        return jsonify({
            "status": "success",
            "database": db_name,
            "collections": collections,
            "counts": collection_counts,
            "message": f"Conectado a la base de datos: {db_name}"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/debug/collections')
def debug_collections():
    """Muestra datos de ejemplo de cada colección"""
    try:
        collections = mongo.db.list_collection_names()
        print(f"Colecciones encontradas: {collections}")  # Log en consola
        
        if not collections:
            return jsonify({
                "status": "empty",
                "message": "No se encontraron colecciones en la base de datos"
            })
        
        sample_data = {}
        for collection in collections:
            try:
                # Obtener hasta 3 documentos de cada colección
                docs = list(mongo.db[collection].find().limit(3))
                sample_data[collection] = docs
                print(f"Colección '{collection}': {len(docs)} documentos")  # Log en consola
            except Exception as coll_error:
                sample_data[collection] = f"Error accediendo a la colección: {str(coll_error)}"
        
        # Usar json_util para manejar ObjectId y otros tipos BSON
        return json.loads(json_util.dumps({
            "status": "success",
            "data": sample_data
        }))
        
    except Exception as e:
        print(f"Error general en debug_collections: {str(e)}")  # Log en consola
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/debug/test-query')
def test_query():
    """Prueba una consulta simple a una colección específica"""
    try:
        # Probar con la colección 'users' primero
        users = list(mongo.db.users.find().limit(5))
        return json.loads(json_util.dumps({
            "status": "success",
            "collection": "users",
            "count": len(users),
            "data": users
        }))
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error en consulta: {str(e)}"
        }), 500

@app.route('/api/debug/direct-connection')
def direct_connection():
    """Prueba de conexión directa sin Flask-PyMongo"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_database()
        
        # Listar todas las bases de datos
        db_names = client.list_database_names()
        
        # Listar colecciones de la base de datos actual
        coll_names = db.list_collection_names()
        
        return jsonify({
            "status": "success",
            "available_databases": db_names,
            "current_database": db.name,
            "collections": coll_names
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/debug/categorias')
def debug_categorias():
    """Endpoint específico para debug de categorías"""
    try:
        # Verificar si la colección existe
        collections = mongo.db.list_collection_names()
        print(f"📂 Colecciones disponibles: {collections}")
        
        if 'categories' not in collections:
            return jsonify({
                "status": "error", 
                "message": "La colección 'categorias' no existe"
            }), 404
        
        # Contar documentos
        count = mongo.db.categories.count_documents({})
        print(f"📊 Número de categorías: {count}")
        
        # Obtener todas las categorías
        categorias = list(mongo.db.categories.find())
        print(f"🔍 Categorías encontradas: {categorias}")
        
        # Verificar la estructura de los documentos
        if categorias:
            primera_categoria = categorias[0]
            print(f"📝 Estructura de la primera categoría: {primera_categoria}")
        
        return json.loads(json_util.dumps({
            "status": "success",
            "count": count,
            "data": categorias,
            "collection_exists": True
        }))
        
    except Exception as e:
        print(f"❌ Error en debug_categorias: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# --- Iniciar el servidor ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)