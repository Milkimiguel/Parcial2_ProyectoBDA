from flask import Blueprint, request, jsonify
from app import mongo
from bson import json_util
import json

comentarios_bp = Blueprint('comentarios', __name__)

# GET /api/comentarios
@comentarios_bp.route('/', methods=['GET'])
def get_comentarios():
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # cursor = mongo.db.comentarios.find(...) # (Probablemente con $lookups)
    # comentarios = json.loads(json_util.dumps(cursor))
    # return jsonify(comentarios)
    return jsonify([])

# POST /api/comentarios
@comentarios_bp.route('/', methods=['POST'])
def create_comentario():
    data = request.get_json()
    # El JS envía: { articulo_id: ..., user_id: 0, texto_com: "..." }
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.comentarios.insert_one({
    #     "articulo_id": data.get('articulo_id'),
    #     "user_id": data.get('user_id'),
    #     "texto_com": data.get('texto_com')
    # })
    return jsonify({"message": "Comentario creado"}), 201

# DELETE /api/comentarios/<id>
@comentarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_comentario(id):
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.comentarios.delete_one({"comentario_id": id})
    return "", 204