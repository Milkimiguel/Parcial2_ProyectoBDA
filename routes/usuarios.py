from flask import Blueprint, request, jsonify
from extensions import mongo
import urllib.parse
from bson import json_util
import json

# El nombre del blueprint debe coincidir con el Blueprint de app.py
usuarios_bp = Blueprint('usuarios', __name__) 

# GET /api/usuarios
@usuarios_bp.route('', methods=['GET'])
def get_usuarios():
    try:
        cursor = mongo.db.users.find()
        usuarios = json.loads(json_util.dumps(cursor))
        return jsonify(usuarios)
    except Exception as e:
        return jsonify(error=str(e)), 500

# POST /api/usuarios
@usuarios_bp.route('', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json() 
        
        # Validar datos de entrada (basado en scriptbasemongo.txt)
        if 'name' not in data or 'email' not in data:
            return jsonify({"error": "Faltan los campos 'name' y 'email'"}), 400
        
        # Verificar si el email ya existe
        if mongo.db.users.find_one({"email": data['email']}):
            return jsonify({"error": "El email ya existe"}), 409 # 409 Conflict
        
        # --- LÓGICA CORREGIDA ---
        result = mongo.db.users.insert_one(data)
        
        # Devolver el usuario recién creado
        new_user = mongo.db.users.find_one({"_id": result.inserted_id})
        return jsonify(json.loads(json_util.dumps(new_user))), 201
        
    except Exception as e:
        return jsonify(error=str(e)), 500

# PUT /api/usuarios/<originalEmail>
@usuarios_bp.route('/<string:originalEmail>', methods=['PUT'])
def update_usuario(originalEmail):
    try:
        data = request.get_json()
        decoded_email = urllib.parse.unquote(originalEmail)
        
        updates = {}
        # Asumimos que el JS envía 'name' y 'email' basado en el script de la DB
        if data.get('name_bool') == 1:
            updates["name"] = data.get('name')
        if data.get('email_bool') == 1:
            updates["email"] = data.get('email')

        if not updates:
            return jsonify({"error": "No hay campos para actualizar"}), 400
            
        # --- LÓGICA CORREGIDA ---
        result = mongo.db.users.update_one(
            {"email": decoded_email},
            {"$set": updates}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        return jsonify({"message": "Usuario actualizado"})
        
    except Exception as e:
        return jsonify(error=str(e)), 500

# DELETE /api/usuarios/<email>
@usuarios_bp.route('/<string:email>', methods=['DELETE'])
def delete_usuario(email):
    try:
        decoded_email = urllib.parse.unquote(email)
        
        # --- LÓGICA CORREGIDA ---
        result = mongo.db.users.delete_one({"email": decoded_email})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        return "", 204 # 204 No Content (éxito sin respuesta)
        
    except Exception as e:
        return jsonify(error=str(e)), 500