import oracledb

def seed_data(cur):
    """Inserta todos los datos de ejemplo en la base de datos."""
    print("Insertando nuevos datos...")
    
    # Datos a insertar
    usuarios = [
        ('Carlos Mendoza', 'carlos.mendoza@example.com'), ('María López', 'maria.lopez@example.com'),
        ('Juan Pérez', 'juan.perez@example.com'), ('Ana Castillo', 'ana.castillo@example.com'),
        ('Luis Hernández', 'luis.hernandez@example.com'), ('Paola Ramírez', 'paola.ramirez@example.com'),
        ('Andrés Torres', 'andres.torres@example.com'), ('Sofía Navarro', 'sofia.navarro@example.com'),
        ('Ricardo Gutiérrez', 'ricardo.gutierrez@example.com'), ('Elena Vargas', 'elena.vargas@example.com')
    ]
    
    tags = [
        ('tecnologia', 'www.blogtech.com/tecnologia'), ('ciberseguridad', 'www.seguridadonline.com/articulos'),
        ('programacion', 'www.devworld.com/tutoriales'), ('futbol', 'www.deportes.com/futbol'),
        ('videojuegos', 'www.gamershub.com/news'), ('educacion', 'www.educacionhoy.com/cursos'),
        ('noticias', 'www.mundonoticias.com/ultimas'), ('cocina', 'www.recetasychef.com/blog'),
        ('viajes', 'www.viajerosglobal.com/guias'), ('economia', 'www.finanzasfacil.com/reportes')
    ]

    categorias = [
        ('Tecnología', 'www.tecnologia.com'), ('Ciberseguridad', 'www.ciberseguridad.com'),
        ('Programación', 'www.programacion.com'), ('Ciencia', 'www.ciencia.com'),
        ('Videojuegos', 'www.videojuegos.com'), ('Educación', 'www.educacion.com'),
        ('Salud', 'www.salud.com'), ('Finanzas', 'www.finanzas.com'),
        ('Deportes', 'www.deportes.com'), ('Cocina', 'www.cocina.com')
    ]

    articulos = [
        (1, 'Introducción a la Programación en Python', 'En este artículo aprenderás las bases de Python...'),
        (2, 'Conceptos Básicos de Ciberseguridad', 'Exploramos los principios fundamentales...'),
        (3, 'Guía de Diseño de Bases de Datos Relacionales', 'Te mostramos cómo modelar y estructurar...'),
        (4, 'Patrones de Diseño en el Desarrollo de Software', 'Un recorrido por los patrones más utilizados...'),
        (5, 'Introducción al Aprendizaje Automático', 'Descubre qué es el machine learning...'),
        (6, 'Seguridad en Redes: Buenas Prácticas', 'Aprende cómo proteger tu red...'),
        (7, 'Optimización de Consultas SQL', 'Consejos para mejorar el rendimiento...'),
        (8, 'Inteligencia Artificial en Videojuegos', 'Exploramos cómo la IA mejora la experiencia...'),
        (9, 'Guía Completa sobre APIs REST', 'Aprende a diseñar, implementar y consumir APIs...'),
        (10, 'Introducción a Docker y Contenedores', 'Una guía básica para comenzar a trabajar...')
    ]

    comentarios = [
        (1, 5, 'Muy interesante el artículo, me ayudó a entender mejor el tema.'),
        (2, 3, 'Creo que podrías profundizar más en la parte de seguridad, pero en general está bien explicado.'),
        (3, 7, 'Excelente explicación, fue fácil de seguir y muy útil para principiantes.'),
        (4, 2, 'No había considerado ese enfoque, gracias por compartirlo.'),
        (5, 8, 'Estoy de acuerdo con tus conclusiones, aportan una perspectiva clara sobre el tema.'),
        (6, 1, 'La parte final del artículo me pareció especialmente útil para mi proyecto.'),
        (7, 4, 'Buen trabajo, aunque creo que podrías incluir algunos ejemplos más técnicos.'),
        (8, 6, 'Me gustó mucho la forma en que estructuraste el contenido, fue muy fácil de entender.'),
        (9, 10, 'Definitivamente este artículo aclara muchas dudas que tenía, gracias.'),
        (10, 9, 'Una lectura muy interesante, espero que sigas publicando artículos similares.'),
        (1, 2, 'Me encantó cómo abordaste el tema desde diferentes perspectivas.'),
        (2, 4, 'La explicación fue clara y directa, justo lo que necesitaba.'),
        (3, 5, 'Podrías agregar algunas referencias externas para complementar la información.'),
        (4, 6, 'Gracias por compartir, me resultó muy útil para mi trabajo universitario.'),
        (5, 7, 'Creo que podrías mejorar la redacción en algunas partes, pero el contenido es bueno.'),
        (6, 8, 'Muy buen artículo, se nota el esfuerzo en la investigación.'),
        (7, 9, 'No estaba familiarizado con este tema y ahora tengo una mejor comprensión.'),
        (8, 10, 'Interesante punto de vista, aunque difiero en algunos aspectos.'),
        (9, 1, 'Gracias por compartir esta información, la pondré en práctica.'),
        (10, 3, 'La sección de ejemplos fue mi parte favorita, muy bien explicada.'),
        (1, 6, 'Excelente contenido, ojalá publiques más artículos como este.'),
        (2, 7, 'Considero que podrías incluir gráficos o diagramas para facilitar la comprensión.'),
        (3, 8, 'Me pareció muy interesante la conclusión, muy bien argumentada.'),
        (4, 9, 'Aunque es un tema complejo, lograste explicarlo de forma sencilla.'),
        (5, 10, 'Este artículo responde muchas de las preguntas que tenía, gracias.'),
        (6, 2, 'La información es actual y relevante, muy buen trabajo.'),
        (7, 3, 'Tal vez podrías agregar más casos prácticos, pero en general es excelente.'),
        (8, 4, 'Me gustó la estructura del artículo, todo está bien organizado.'),
        (9, 5, 'Nunca había leído algo tan completo sobre el tema, felicidades.'),
        (10, 8, 'Muy informativo, definitivamente lo recomendaré a mis compañeros.')
    ]

    articulo_categorias = [
        (1, 3), (1, 1),
        (2, 2), (2, 4),
        (3, 3), (3, 6),
        (4, 1), (4, 7),
        (5, 3), (5, 4),
        (6, 2), (6, 7),
        (7, 3), (7, 8),
        (8, 5), (8, 1),
        (9, 3), (9, 2),
        (10, 1), (10, 9)
    ]

    articulo_tags = [
        (1, 3), (1, 1),
        (2, 2), (2, 7),
        (3, 3), (3, 6),
        (4, 3), (4, 1),
        (5, 1), (5, 6),
        (6, 2), (6, 7),
        (7, 3), (7, 10),
        (8, 5), (8, 7),
        (9, 3), (9, 1),
        (10, 1), (10, 6)
    ]
    
    try:
        for nombre, correo in usuarios:
            cur.callproc('INSERT_USUARIO', (nombre, correo))
        print(f"{len(usuarios)} usuarios insertados.")

        for tag, url in tags:
            cur.callproc('INSERT_TAG', (tag, url))
        print(f"{len(tags)} tags insertados.")

        for cat, url in categorias:
            cur.callproc('INSERT_CATEGORIA', (cat, url))
        print(f"{len(categorias)} categorías insertadas.")

        for IdUsr, NomArt, descripcion in articulos:
            cur.callproc('INSERT_ARTICULO', (IdUsr, NomArt, descripcion))
        print(f"{len(articulos)} artículos insertados.")
    
        for artId, usId, texto in comentarios:
            cur.callproc('INSERT_COMENTARIO', (artId, usId, texto))
        print(f"{len(comentarios)} comentarios insertados.")

        for artId, catId in articulo_categorias:
            cur.callproc('INSERT_ART_CAT', (artId, catId))
        print(f"{len(articulo_categorias)} relaciones artículo-categoría insertadas.")

        for artId, tagId in articulo_tags:
            cur.callproc('INSERT_ART_TAG', (artId, tagId))
        print(f"{len(articulo_tags)} relaciones artículo-tag insertadas.")

    except oracledb.Error as err:
        print('Error durante la inserción:', err)
        raise

# Este bloque solo se ejecuta cuando corres "python seed.py"
if __name__ == "__main__":
    try:
        conn = oracledb.connect(
            user="blog",
            password="blog",
            dsn="localhost:1521/xepdb1"
        )
        print("\nConexión a la BD exitosa para carga de datos.")
        
        with conn.cursor() as cur:
            seed_data(cur)
        
        conn.commit()
        print("\n¡Carga de datos completada exitosamente! Cambios guardados.")

    except oracledb.Error as err:
        print('\nOcurrió un error durante el proceso:', err)
        if 'conn' in locals() and conn:
            conn.rollback()
            print("Se ha hecho rollback de la transacción.")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Conexión de carga de datos cerrada.")
