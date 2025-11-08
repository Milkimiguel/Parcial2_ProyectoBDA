from flask import Blueprint, request, jsonify
from app import mongo
import urllib.parse
from bson import json_util
import json

tags_bp = Blueprint('tags', __name__)

# GET /api/tags
@tags_bp.route('/', methods=['GET'])
def get_tags():
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # cursor = mongo.db.tags.find()
    # tags = json.loads(json_util.dumps(cursor))
    # return jsonify(tags)
    return jsonify([])

# POST /api/tags
@tags_bp.route('/', methods=['POST'])
def create_tag():
    data = request.get_json() # { tag_name, url_tag }
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.tags.insert_one(data)
    return jsonify({"message": "Tag creado"}), 201

# PUT /api/tags/<originalName>
@tags_bp.route('/<string:originalName>', methods=['PUT'])
def update_tag(originalName):
    data = request.get_json() # { tag_name, url_tag }
    decoded_name = urllib.parse.unquote(originalName)
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.tags.update_one(
    #   {"tag_name": decoded_name},
    #   {"$set": data}
    # )
    return jsonify({"message": "Tag actualizado"})

# DELETE /api/tags/<name>
@tags_bp.route('/<string:name>', methods=['DELETE'])
def delete_tag(name):
    decoded_name = urllib.parse.unquote(name)
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.tags.delete_one({"tag_name": decoded_name})
    return "", 204