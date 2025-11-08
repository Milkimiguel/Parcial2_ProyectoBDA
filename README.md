<b><h2>Requerimientos antes de compilar la aplicación:</h2></b>
   <ul>
         <li>Tener instalado Python en la computadora.</li>
         <li>Contar con un DBMS para bases de datos relacionales. También se recomienda una IDE como SQL Developer para manejar los scripts con facilidad.</li>
         <li>Tener instalado un navegador web en la computadora.</li>
   </ul>

<b><h2>Cómo compilar la aplicación: </h2></b>
   <ol>
      <li>Instalar las dependencias necesarias (cx_Oracle, oracledb, flask, flask_cors usando pip install)</li>
      <li>Correr el script de la base de datos (scriptPROYECTO.sql) junto con los scripts dentro de las carpetas “IUD Procedures” y “Procedimientos de Consultas”. Se tiene que asegurar que el usuario y contraseña en el que se realiza la conexión a la base de datos coincida con el que está en db.py, o modificar db.py para que coincida con el usuario y contraseña usados.</li>
      <li>Correr el archivo seed.py (python seed.py) para agregar información a la base de datos.</li>
      <li>Correr el archivo app.py (python app.py)</li>
      <li>Abrir el archivo index.html dentro de la carpeta frontend en el navegador.</li>
   </ol>

<b><h2>Cómo funciona la aplicación: </h2></b>
El archivo app.py es una API Flask que contiene los endpoints de la aplicación. Maneja procesos relacionados a la base de datos de Oracle y manejo de errores.
El archivo db.py crea la conexión a la base de datos de Oracle y permite gestionar dicha conexión.
Dentro de la carpeta frontend se maneja toda la lógica dentro del archivo script.js; dentro de este archivo se define la URL de la API, así como mostrar mensajes y hacer peticiones al backend. Tiene funciones para mostrar, agregar y eliminar datos.
Aparte de esos tres archivos, el script de la base de datos se encuentra en el archivo scriptPROYECTO.sql; mientras que los scripts para los procedimientos para insertar, actualizar y eliminar se encuentran dentro de la carpeta “IUD Procedures”. La carpeta “Procedimientos de consultas” contiene los scripts de todos los procedimientos necesarios para la aplicación como buscar artículos o mostrar detalles.



lalo
