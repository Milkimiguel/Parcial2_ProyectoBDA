from flask import Blueprint, request, jsonify
from extensions import mongo
import urllib.parse
from bson import json_util
import json

categorias_bp = Blueprint('categorias', __name__)

# GET /api/categorias
@categorias_bp.route('', methods=['GET']) # <-- CORREGIDO: de '/' a ''
def get_categorias():
    try:
        # --- LÓGICA CORREGIDA ---
        cursor = mongo.db.categorias.find()
        categorias = json.loads(json_util.dumps(cursor))
        return jsonify(categorias)
    except Exception as e:
        return jsonify(error=str(e)), 500

# POST /api/categorias
@categorias_bp.route('', methods=['POST']) # <-- CORREGIDO: de '/' a ''
def create_categoria():
    try:
        data = request.get_json() # Espera: { category_name, url_cat }
        
        # --- LÓGICA CORREGIDA ---
        # Validar campos (basado en tus comentarios)
        if 'category_name' not in data or 'url_cat' not in data:
            return jsonify({"error": "Faltan los campos 'category_name' y 'url_cat'"}), 400
        
        # Verificar duplicados
        if mongo.db.categorias.find_one({"category_name": data['category_name']}):
            return jsonify({"error": "Ese nombre de categoría ya existe"}), 409

        result = mongo.db.categorias.insert_one(data)
        
        new_cat = mongo.db.categorias.find_one({"_id": result.inserted_id})
        return jsonify(json.loads(json_util.dumps(new_cat))), 201
        
    except Exception as e:
        return jsonify(error=str(e)), 500

# PUT /api/categorias/<originalName>
@categorias_bp.route('/<string:originalName>', methods=['PUT'])
def update_categoria(originalName):
    try:
        data = request.get_json() # Espera: { category_name, url_cat }
        decoded_name = urllib.parse.unquote(originalName)
        
        # Validar campos
        if 'category_name' not in data or 'url_cat' not in data:
            return jsonify({"error": "Faltan los campos 'category_name' y 'url_cat'"}), 400

        # --- LÓGICA CORREGIDA ---
        result = mongo.db.categorias.update_one(
            {"category_name": decoded_name},
            {"$set": {
                "category_name": data.get('category_name'),
                "url_cat": data.get('url_cat')
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "Categoría no encontrada"}), 404
            
        return jsonify({"message": "Categoría actualizada"})
        
    except Exception as e:
        return jsonify(error=str(e)), 500

# DELETE /api/categorias/<name>
@categorias_bp.route('/<string:name>', methods=['DELETE'])
def delete_categoria(name):
    try:
        decoded_name = urllib.parse.unquote(name)
        
        # --- LÓGICA CORREGIDA ---
        result = mongo.db.categorias.delete_one({"category_name": decoded_name})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Categoría no encontrada"}), 404
            
        return "", 204 # Éxito sin contenido
        
    except Exception as e:
        return jsonify(error=str(e)), 500