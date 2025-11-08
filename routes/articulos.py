# routes/articulos.py

from flask import Blueprint, request, jsonify
from app import mongo # Importamos la conexión de PyMongo
from bson.objectid import ObjectId # Para buscar por _id si es necesario
import json
from bson import json_util # Para serializar correctamente la data de Mongo

articulos_bp = Blueprint('articulos', __name__)

# GET /api/articulos
@articulos_bp.route('/', methods=['GET'])
def get_articulos():
    try:
        # --- LÓGICA DE PYMONGO AQUÍ ---
        # cursor = mongo.db.articulos.find(...) 
        # (Asegúrate de hacer los 'joins' o 'lookups' necesarios si los datos están en colecciones separadas)
        
        # Datos de ejemplo si aún no tienes la consulta:
        articulos = [
            {"articulo_id": 1, "user_name": "Admin", "user_id": 0, "titulo": "Título de prueba"}
        ]
        
        # Si usas un cursor de PyMongo, serialízalo:
        # articulos_serializados = json.loads(json_util.dumps(cursor))
        # return jsonify(articulos_serializados)
        
        return jsonify(articulos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /api/articulos
@articulos_bp.route('/', methods=['POST'])
def create_articulo():
    data = request.get_json()
    # El JS envía: { user_id: 0, titulo: "...", article_text: "..." }
    try:
        # --- LÓGICA DE PYMONGO AQUÍ ---
        # mongo.db.articulos.insert_one({
        #     "user_id": data.get('user_id'),
        #     "titulo": data.get('titulo'),
        #     "article_text": data.get('article_text')
        #     # ... otros campos ...
        # })
        return jsonify({"message": "Artículo creado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE /api/articulos/<id>
@articulos_bp.route('/<int:id>', methods=['DELETE']) # Asumo que el ID es un int
def delete_articulo(id):
    try:
        # --- LÓGICA DE PYMONGO AQUÍ ---
        # (Ojo: si tu 'articulo_id' no es el _id de Mongo, usa este campo)
        # result = mongo.db.articulos.delete_one({"articulo_id": id})
        
        # Si 'id' es el _id de Mongo (que es un string):
        # @articulos_bp.route('/<string:id>', methods=['DELETE'])
        # result = mongo.db.articulos.delete_one({"_id": ObjectId(id)})

        # if result.deleted_count == 0:
        #    return jsonify({"error": "Artículo no encontrado"}), 404
            
        return "", 204 # Respuesta vacía, como espera el JS
    except Exception as e:
        return jsonify({"error": str(e)}), 500