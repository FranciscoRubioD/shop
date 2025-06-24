from flask import Flask, jsonify,request,send_from_directory
from flask_cors import CORS
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from db_config import db_config  # Importa la configuración desde otro archivo
import os
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)
CORS(app)  # Permite que el frontend acceda al backend


# archivos
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), '..', 'img', 'covers'))  # carpeta img/cover
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta absoluta hacia la carpeta img
IMG_FOLDER = os.path.abspath(os.path.join(os.getcwd(), '..', 'img'))



# Función para validar extensión
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración conexión MySQL
db_config = {
    'host': 'mysql',  # <--- Este es el nombre del servicio del contenedor MySQL
    'user': 'root',
    'password': 'root',
    'database': 'covers'
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)


# probar conexion a bd
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Conexión a la base de datos exitosa")
except Error as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")
# termina prueba de conexion a bd

# endpoint archivos
@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMG_FOLDER, filename)

# API

# Ruta para obtener productos tipo 'cover' con sus modelos
@app.route('/api/covers', methods=['GET'])
def get_covers():
    modelo_id = request.args.get('modelo_id')
    ocasion_id = request.args.get('ocasion_id')  # Nuevo parámetro

    if not modelo_id:
        return jsonify({'error': 'modelo_id es requerido'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT p.id, p.nombre AS producto_nombre, p.imagen, p.stock, p.precio,
                   m.id AS modelo_id, m.nombre AS modelo_nombre
            FROM producto p
            JOIN cover c ON p.id = c.id
            JOIN modelo m ON c.modelo_id = m.id
            LEFT JOIN cover_ocasion co ON c.id = co.id_cover
        """

        params = [modelo_id]

        if ocasion_id:
            query += " WHERE c.modelo_id = %s AND co.id_ocasion = %s"
            params.append(ocasion_id)
        else:
            query += " WHERE c.modelo_id = %s"

        query += " GROUP BY p.id"

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# empieza subir cover
@app.route('/api/covers', methods=['POST'])
def agregar_cover():
    nombre = request.form.get('nombre')
    stock = request.form.get('stock')
    precio = request.form.get('precio')
    modelo_id = request.form.get('modelo_id')
    ocasiones = request.form.get('ocasiones')

    if not all([nombre, stock, precio, modelo_id]):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    if 'imagen' not in request.files:
        return jsonify({'error': 'No se envió archivo de imagen'}), 400

    imagen_file = request.files['imagen']

    if imagen_file and allowed_file(imagen_file.filename):
      # Procesar y guardar la imagen
      filename = secure_filename(imagen_file.filename)
      extension = os.path.splitext(filename)[1]  # .png, .jpg, etc.

      unique_name = f"{uuid.uuid4().hex}{extension}"
      relative_path = f"covers/{unique_name}"  # Esto es lo que se guarda en la BD
      imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
      # Guardar la imagen
      imagen_file.save(imagen_path)
    else:
        return jsonify({'error': 'Archivo no permitido'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar en producto
        cursor.execute("""
            INSERT INTO producto (nombre, tipo, imagen, stock, precio)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, "cover", relative_path, stock, precio))
        producto_id = cursor.lastrowid

        # Insertar en cover
        cursor.execute("""
            INSERT INTO cover (id, modelo_id)
            VALUES (%s, %s)
        """, (producto_id, modelo_id))

        # Insertar ocasiones si vienen
        if ocasiones:
            import json
            lista_ocasiones = json.loads(ocasiones)
            for ocasion_id in lista_ocasiones:
                cursor.execute("""
                    INSERT INTO cover_ocasion (id_cover, id_ocasion)
                    VALUES (%s, %s)
                """, (producto_id, ocasion_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Cover agregado correctamente', 'id': producto_id})

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# termina agregar cover

# eliminar cover
@app.route('/api/covers/<int:id>', methods=['DELETE'])
def eliminar_cover(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Obtener la ruta de imagen antes de eliminar
        cursor.execute("SELECT imagen FROM producto WHERE id = %s AND tipo = 'cover'", (id,))
        resultado = cursor.fetchone()

        if not resultado:
            return jsonify({'error': 'Cover no encontrado'}), 404

        # Obtener la ruta relativa desde la BD (ej: 'covers/08f6abcd.png')
        imagen_relativa = resultado['imagen']

        # Extraer el nombre del archivo (ej: '08f6abcd.png')
        nombre_archivo = os.path.basename(imagen_relativa)
         # Construir la ruta absoluta final correctamente
        imagen_absoluta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)

        print(imagen_absoluta)

        # Eliminar de cover_ocasion
        cursor.execute("DELETE FROM cover_ocasion WHERE id_cover = %s", (id,))
        # Eliminar de cover
        cursor.execute("DELETE FROM cover WHERE id = %s", (id,))
        # Eliminar de producto
        cursor.execute("DELETE FROM producto WHERE id = %s AND tipo = 'cover'", (id,))
        
        conn.commit()
        cursor.close()
        conn.close()

        # Eliminar archivo de imagen del disco
        try:
            if os.path.exists(imagen_absoluta):
                print(imagen_absoluta);
                os.remove(imagen_absoluta)
        except Exception as file_err:
            print(f"Advertencia: No se pudo eliminar la imagen: {file_err}")

        return jsonify({'mensaje': 'Cover eliminado correctamente'})

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
# eliminar cover termina

# modificar campos
@app.route('/api/covers/<int:id>', methods=['PUT'])
def actualizar_cover(id):
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')

    if campo not in ['stock', 'precio']:
        return jsonify({'error': 'Campo no permitido'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE producto SET {campo} = %s WHERE id = %s AND tipo = 'cover'", (valor, id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': f'{campo} actualizado'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@app.route('/api/modelos', methods=['GET'])
def get_modelos():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, nombre FROM modelo ORDER BY id"
        cursor.execute(query)
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(resultados)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# deja de consultar modelos


# ocaciones select
@app.route('/api/ocasiones', methods=['GET'])
def get_ocasiones():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, nombre FROM ocasion ORDER BY nombre"
        cursor.execute(query)
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(resultados)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# ocaciones count
@app.route('/api/ocasiones/con-cantidad/<int:modelo_id>', methods=['GET'])
def obtener_ocasiones_con_cantidad(modelo_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT o.id, o.nombre, COUNT(c.id) as cantidad
            FROM ocasion o
            LEFT JOIN cover_ocasion co ON co.id_ocasion = o.id
            LEFT JOIN cover c ON c.id = co.id_cover AND c.modelo_id = %s
            GROUP BY o.id, o.nombre
            ORDER BY o.nombre;
        """
        cursor.execute(query, (modelo_id,))
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(resultados)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


# manejar una venta
@app.route('/api/venta', methods=['POST'])
def registrar_venta():
    data = request.json
    print(data)
    producto_id = data.get('producto_id')
    precio_venta = data.get('precio')
    cantidad = data.get('cantidad')
    metodo = data.get('metodo_pago')  # ✅ Nuevo campo

    if not all([producto_id, precio_venta, cantidad, metodo]):
        return jsonify({'error': 'Faltan datos'}), 400

    # Verificar stock suficiente
    cursor.execute("SELECT stock FROM producto WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    if producto['stock'] < cantidad:
        return jsonify({'error': 'Stock insuficiente'}), 400

    try:
        # Insertar en tabla venta con método de pago
        cursor.execute("INSERT INTO venta (fecha, metodo) VALUES (%s, %s)", (datetime.now(), metodo))
        venta_id = cursor.lastrowid

        # Insertar en venta_producto
        cursor.execute("""
            INSERT INTO venta_producto (venta_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (venta_id, producto_id, cantidad, precio_venta))

        # Actualizar stock del producto
        cursor.execute("""
            UPDATE producto SET stock = stock - %s WHERE id = %s
        """, (cantidad, producto_id))

        conn.commit()
        return jsonify({'message': 'Venta registrada correctamente'}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
