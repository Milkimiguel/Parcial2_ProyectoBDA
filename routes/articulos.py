from flask import Blueprint, request, jsonify
from extensions import mongo
from bson import json_util
import json
import datetime

articulos_bp = Blueprint('articulos', __name__)

# GET /api/articulos
@articulos_bp.route('', methods=['GET'])
def get_articulos():
    try:
        # --- LÓGICA CORREGIDA: Implementar $lookups ---
        pipeline = [
            {
                '$lookup': {
                    'from': 'users', # Colección de usuarios
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': '$author_info' # Convertir array en objeto
            },
            # (Se podrían añadir $lookups para tags y categorias si se necesita)
            {
                '$project': {
                    # Mapear los campos de la DB a lo que espera el JS
                    'articulo_id': '$_id', # JS espera 'articulo_id'
                    'user_id': '$author_id', # JS espera 'user_id'
                    'user_name': '$author_info.name', # JS espera 'user_name'
                    'titulo': '$title' # JS espera 'titulo'
                    # (Añadir 'content', 'tags', etc. si el JS los necesita)
                }
            }
        ]
        
        cursor = mongo.db.articles.aggregate(pipeline)
        articulos_serializados = json.loads(json_util.dumps(cursor))
        return jsonify(articulos_serializados)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /api/articulos
@articulos_bp.route('', methods=['POST']) # <-- CORREGIDO: de '/' a ''
def create_articulo():
    data = request.get_json()
    # JS envía: { user_id: 0, titulo: "...", article_text: "..." }
    try:
        # --- LÓGICA CORREGIDA ---
        
        # 1. Encontrar el ID más alto actual, ya que son manuales (de scriptbasemongo.txt)
        last_article = mongo.db.articulos.find_one(sort=[("_id", -1)])
        new_id = (last_article["_id"] + 1) if last_article else 1

        # 2. Mapear campos de JS a campos de la DB (de scriptbasemongo.txt)
        new_article = {
            "_id": new_id,
            "title": data.get('titulo'), # JS usa 'titulo', DB usa 'title'
            "content": data.get('article_text'), # JS usa 'article_text', DB usa 'content'
            "author_id": data.get('user_id'), # JS usa 'user_id', DB usa 'author_id'
            "tags": data.get('tags', []), # Asumir vacío si no se envía
            "categories": data.get('categories', []), # Asumir vacío si no se envía
            "created_at": datetime.datetime.utcnow()
        }
        
        result = mongo.db.articulos.insert_one(new_article)
        
        new_doc = mongo.db.articulos.find_one({"_id": result.inserted_id})
        return jsonify(json.loads(json_util.dumps(new_doc))), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE /api/articulos/<id>
@articulos_bp.route('/<int:id>', methods=['DELETE'])
def delete_articulo(id):
    try:
        # --- LÓGICA CORREGIDA ---
        # El ID es un Int, no un ObjectId (de scriptbasemongo.txt)
        result = mongo.db.articulos.delete_one({"_id": id})

        if result.deleted_count == 0:
            return jsonify({"error": "Artículo no encontrado"}), 404
            
        return "", 204 # Respuesta vacía, como espera el JS
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500