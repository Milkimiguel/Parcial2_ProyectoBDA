from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb
from db import get_db_connection, pool # Importamos desde nuestro módulo db

app = Flask(__name__)
CORS(app)

# --- FUNCIÓN AUXILIAR PARA LLAMAR AL PROCEDIMIENTO GENÉRICO ---
def _call_sp_get_data(table_name):
    # Función genérica que llama al procedimiento sp_datos_tablas
    # y devuelve las filas obtenidas.
    
    conn = get_db_connection()
    if not conn:
        raise Exception("Error de conexión a la base de datos")
    
    try:
        with conn.cursor() as cur:
            out_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
            cur.callproc('sp_datos_tablas', [table_name, out_cursor])
            result_cursor = out_cursor.getvalue()
            return result_cursor.fetchall()
    finally:
        if conn:
            pool.release(conn)

# --- Endpoints para Usuarios (Usa el procedimiento genérico) ---
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    try:
        rows = _call_sp_get_data('usuarios')
        usuarios = [{'user_id': r[0], 'user_name': r[1], 'email': r[2]} for r in rows]
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoints para Artículos (AHORA USA SU PROCEDIMIENTO ESPECÍFICO) ---
@app.route('/api/articulos', methods=['GET'])
def get_articulos():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            # Llama al nuevo procedimiento específico para artículos
            out_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
            cur.callproc('sp_get_articulos_detalle', [out_cursor])
            
            # Obtiene el cursor de resultado y lee las filas
            result_cursor = out_cursor.getvalue()
            rows = result_cursor.fetchall()
            
            articulos = []
            for row in rows:
                article_text_lob = row[3]
                article_text_str = article_text_lob.read() if article_text_lob else ""
                articulos.append({
                    'articulo_id': row[0], 'user_id': row[1], 'titulo': row[2],
                    'article_text': article_text_str, 'user_name': row[4]
                })
            return jsonify(articulos)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

# --- Endpoints para Categorías (Usa el procedimiento genérico) ---
@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    try:
        rows = _call_sp_get_data('categorias')
        categorias = [{'category_name': r[1], 'url_cat': r[2]} for r in rows]
        return jsonify(categorias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoints para Comentarios (AHORA USA SU PROCEDIMIENTO ESPECÍFICO) ---
@app.route('/api/comentarios', methods=['GET'])
def get_comentarios():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            # Llama al nuevo procedimiento específico para comentarios
            out_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
            cur.callproc('sp_get_comentarios_detalle', [out_cursor])

            # Obtiene el cursor de resultado y lee las filas
            result_cursor = out_cursor.getvalue()
            rows = result_cursor.fetchall()

            comentarios = []
            for row in rows:
                texto_com_lob = row[3]
                texto_com_str = texto_com_lob.read() if texto_com_lob else ""
                comentarios.append({
                    'comentario_id': row[0], 'articulo_id': row[1], 'user_id': row[2],
                    'texto_com': texto_com_str, 'titulo_articulo': row[4], 'user_name': row[5]
                })
            return jsonify(comentarios)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

# --- Endpoints para Tags (Usa el procedimiento genérico) ---
@app.route('/api/tags', methods=['GET'])
def get_tags():
    try:
        rows = _call_sp_get_data('tags')
        tags = [{'tag_name': r[1], 'url_tag': r[2]} for r in rows]
        return jsonify(tags)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- EL RESTO DE ENDPOINTS (POST, PUT, DELETE) NO CAMBIAN ---
# (El código es el mismo que ya tenías)

@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('INSERT_USUARIO', [data['user_name'], data['email']])
            conn.commit()
            return jsonify({"message": "Usuario creado correctamente"}), 201
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/usuarios/<email>', methods=['PUT'])
def update_usuario(email):
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('UPDATE_USUARIO', [email, data['user_name'], data['email'], data.get('name_bool', 1), data.get('email_bool', 1)])
            conn.commit()
            return jsonify({"message": "Usuario actualizado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/usuarios/<email>', methods=['DELETE'])
def delete_usuario(email):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('DELETE_USUARIO', [email])
            conn.commit()
            return jsonify({"message": "Usuario eliminado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/articulos', methods=['POST'])
def create_articulo():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('INSERT_ARTICULO', [0, data['titulo'], data['article_text']])
            conn.commit()
            return jsonify({"message": "Artículo creado correctamente"}), 201
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/articulos/<int:articulo_id>', methods=['PUT'])
def update_articulo(articulo_id):
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('UPDATE_ARTICULO', [
                articulo_id, data['titulo'], data['article_text'],
                data.get('titulo_bool', 1), data.get('text_bool', 1)
            ])
            conn.commit()
            return jsonify({"message": "Artículo actualizado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/articulos/<int:articulo_id>', methods=['DELETE'])
def delete_articulo(articulo_id):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('DELETE_ARTICULOS', [articulo_id])
            conn.commit()
            return jsonify({"message": "Artículo eliminado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/categorias', methods=['POST'])
def create_categoria():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('INSERT_CATEGORIA', [data['category_name'], data['url_cat']])
            conn.commit()
            return jsonify({"message": "Categoría creada correctamente"}), 201
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/categorias/<category_name>', methods=['PUT'])
def update_categoria(category_name):
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('UPDATE_CATEGORIA', [category_name, data['category_name'], data['url_cat']])
            conn.commit()
            return jsonify({"message": "Categoría actualizada correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/categorias/<category_name>', methods=['DELETE'])
def delete_categoria(category_name):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('DELETE_CATEGORIA', [category_name])
            conn.commit()
            return jsonify({"message": "Categoría eliminada correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/comentarios', methods=['POST'])
def create_comentario():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('INSERT_COMENTARIO', [data['articulo_id'], 0, data['texto_com']])
            conn.commit()
            return jsonify({"message": "Comentario creado correctamente"}), 201
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/comentarios/<int:comentario_id>', methods=['PUT'])
def update_comentario(comentario_id):
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('UPDATE_COMENTARIO', [comentario_id, data['texto_com']])
            conn.commit()
            return jsonify({"message": "Comentario actualizado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/comentarios/<int:comentario_id>', methods=['DELETE'])
def delete_comentario(comentario_id):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('DELETE_COMENTARIO', [comentario_id])
            conn.commit()
            return jsonify({"message": "Comentario eliminado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/tags', methods=['POST'])
def create_tag():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('INSERT_TAG', [data['tag_name'], data['url_tag']])
            conn.commit()
            return jsonify({"message": "Tag creado correctamente"}), 201
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/tags/<tag_name>', methods=['PUT'])
def update_tag(tag_name):
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('UPDATE_TAG', [tag_name, data['tag_name'], data['url_tag']])
            conn.commit()
            return jsonify({"message": "Tag actualizado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)

@app.route('/api/tags/<tag_name>', methods=['DELETE'])
def delete_tag(tag_name):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de conexión"}), 500
    try:
        with conn.cursor() as cur:
            cur.callproc('DELETE_TAG', [tag_name])
            conn.commit()
            return jsonify({"message": "Tag eliminado correctamente"})
    except oracledb.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: pool.release(conn)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

