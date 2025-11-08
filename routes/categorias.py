# routes/categorias.py

from flask import Blueprint, request, jsonify
from app import mongo
import urllib.parse
from bson import json_util
import json

categorias_bp = Blueprint('categorias', __name__)

# GET /api/categorias
@categorias_bp.route('/', methods=['GET'])
def get_categorias():
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # cursor = mongo.db.categorias.find()
    # categorias = json.loads(json_util.dumps(cursor))
    # return jsonify(categorias)
    return jsonify([]) # Devolver array vacío por ahora

# POST /api/categorias
@categorias_bp.route('/', methods=['POST'])
def create_categoria():
    data = request.get_json() # { category_name, url_cat }
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.categorias.insert_one(data)
    return jsonify({"message": "Categoría creada"}), 201

# PUT /api/categorias/<originalName>
@categorias_bp.route('/<string:originalName>', methods=['PUT'])
def update_categoria(originalName):
    data = request.get_json() # { category_name, url_cat }
    # El JS usa encodeURIComponent, lo decodificamos
    decoded_name = urllib.parse.unquote(originalName)
    
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.categorias.update_one(
    #   {"category_name": decoded_name},
    #   {"$set": {
    #     "category_name": data.get('category_name'),
    #     "url_cat": data.get('url_cat')
    #   }}
    # )
    return jsonify({"message": "Categoría actualizada"})

# DELETE /api/categorias/<name>
@categorias_bp.route('/<string:name>', methods=['DELETE'])
def delete_categoria(name):
    decoded_name = urllib.parse.unquote(name)
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.categorias.delete_one({"category_name": decoded_name})
    return "", 204