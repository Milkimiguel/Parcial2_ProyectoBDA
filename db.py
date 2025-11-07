# import oracledb
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

# --- Módulo para gestionar la conexión a la base de datos ---

def get_db(uri, db_name):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("Conexión exitosa")
        return client[db_name]
    except ServerSelectionTimeoutError:
        print("Ocurrió un error al conectar con el servidor")
        return None
    except ConnectionFailure:
        print("Hubo un error en la red")
        return None


db = get_db("mongodb+srv://a361031:IoKRukAmh0naLRTU@proyecto2bda.pvcqdkd.mongodb.net/?appName=Proyecto2BDA", "proyecto2BDA")
if db is not None:
    try:
        collections = db.list_collection_names()
        print("Colecciones:", collections)

    except Exception as e:
        print(f"Error al acceder a la base de datos: {e}")
        
else:
    print("No se pudo establecer conexión con la base de datos")


# pool = None

# def init_db_pool():
#     """
#     Inicializa el pool de conexiones a la base de datos.
#     Esta función se llama una sola vez al iniciar la aplicación.
#     """
#     global pool
#     try:
#         pool = oracledb.create_pool(
#             user="blog", password="blog", dsn="localhost:1521/xepdb1",
#             min=2, max=5, increment=1
#         )
#         print("Pool de conexiones creado exitosamente.")
#     except oracledb.Error as e:
#         print(f"Error al crear el pool de conexiones: {e}")
#         pool = None

# def get_db_connection():
#     """
#     Obtiene una conexión del pool.
#     """
#     if not pool:
#         print("Error: El pool de conexiones no está inicializado.")
#         return None
#     try:
#         # Adquiere una conexión del pool para ser usada por un endpoint
#         return pool.acquire()
#     except oracledb.Error as e:
#         print(f"Error al obtener conexión del pool: {e}")
#         return None

# # Inicializamos el pool al cargar este módulo
# init_db_pool()
