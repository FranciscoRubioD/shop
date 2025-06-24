from flask import Flask, jsonify,request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from db_config import db_config  # Importa la configuración desde otro archivo


app = Flask(__name__)
CORS(app)  # Permite que el frontend acceda al backend

# Configuración conexión MySQL
db_config = {
    'host': 'mysql',  # <--- Este es el nombre del servicio del contenedor MySQL
    'user': 'root',
    'password': 'root',
    'database': 'covers'
}


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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
