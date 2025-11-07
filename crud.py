from db import get_db

db = get_db()
users = db["users"]

def create_user(name, email):
    """Crea un nuevo usuario"""
    user = {"name": name, "email": email}
    result = users.insert_one(user)
    print(f"Usuario creado con id: {result.inserted_id}")

def read_users():
    """Lee y muestra todos los usuarios"""
    print("\n📋 Lista de usuarios:")
    for u in users.find():
        print(f"- {u['name']} ({u['email']})")

def update_user(email, new_name=None, new_email=None):
    """Actualiza los datos de un usuario por email"""
    update_data = {}
    if new_name:
        update_data["name"] = new_name
    if new_email:
        update_data["email"] = new_email

    result = users.update_one({"email": email}, {"$set": update_data})
    if result.modified_count:
        print("✅ Usuario actualizado correctamente.")
    else:
        print("⚠️ No se encontró el usuario o no hubo cambios.")

def delete_user(email):
    """Elimina un usuario por su email"""
    result = users.delete_one({"email": email})
    if result.deleted_count:
        print("🗑️ Usuario eliminado.")
    else:
        print("⚠️ Usuario no encontrado.")

def search_user(name):
    """Busca usuarios por nombre"""
    print(f"\n🔍 Resultados de búsqueda para '{name}':")
    results = users.find({"name": {"$regex": name, "$options": "i"}})
    found = False
    for u in results:
        print(f"- {u['name']} ({u['email']})")
        found = True
    if not found:
        print("No se encontraron coincidencias.")

def count_users():
    """Cuenta la cantidad de usuarios"""
    total = users.count_documents({})
    print(f"\n👥 Total de usuarios: {total}")
