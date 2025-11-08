from flask import Blueprint, request, jsonify
from app import mongo
import urllib.parse
from bson import json_util
import json

usuarios_bp = Blueprint('usuarios', __name__)

# GET /api/usuarios
@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # cursor = mongo.db.usuarios.find()
    # usuarios = json.loads(json_util.dumps(cursor))
    # return jsonify(usuarios)
    return jsonify([])

# POST /api/usuarios
@usuarios_bp.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json() # { user_name, email }
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.usuarios.insert_one(data)
    return jsonify({"message": "Usuario creado"}), 201

# PUT /api/usuarios/<originalEmail>
@usuarios_bp.route('/<string:originalEmail>', methods=['PUT'])
def update_usuario(originalEmail):
    data = request.get_json()
    # JS envía: { user_name, email, name_bool(1/0), email_bool(1/0) }
    decoded_email = urllib.parse.unquote(originalEmail)
    
    # Construir el $set dinámicamente
    updates = {}
    if data.get('name_bool') == 1:
        updates["user_name"] = data.get('user_name')
    if data.get('email_bool') == 1:
        updates["email"] = data.get('email')

    if not updates:
        return jsonify({"error": "No hay campos para actualizar"}), 400
        
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.usuarios.update_one(
    #   {"email": decoded_email},
    #   {"$set": updates}
    # )
    return jsonify({"message": "Usuario actualizado"})

# DELETE /api/usuarios/<email>
@usuarios_bp.route('/<string:email>', methods=['DELETE'])
def delete_usuario(email):
    decoded_email = urllib.parse.unquote(email)
    # --- LÓGICA DE PYMONGO AQUÍ ---
    # mongo.db.usuarios.delete_one({"email": decoded_email})
    return "", 204