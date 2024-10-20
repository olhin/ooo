import traceback
from flask import Flask, request, jsonify, make_response
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Параметры подключения к первой базе данных
db_config1 = {
    'host': '192.168.56.1',
    'user': 'other',
    'password': '000000000',
    'database': 'osint',
    'port': 3306
}

# Параметры подключения ко второй базе данных
db_config2 = {
    'host': '192.168.1.103',
    'user': 'other',
    'password': '000000000',
    'database': 'osint',
    'port': 3306
}

def get_db_connection(config):
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # Используем DictCursor для получения данных в виде словарей
        return connection, cursor
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None

@app.route('/search', methods=['GET'])
def search():
    connection, cursor = get_db_connection(db_config1)
    if connection is None or cursor is None:
        return jsonify({'error': 'Database connection is not available'}), 500

    phone = request.args.get('phone')
    if not phone:
        return jsonify({'error': 'Phone parameter is required'}), 400

    search_query = """
    SELECT address, birth_date AS date_of_birth, city, email, name, phone_number
    FROM sportmaster
    WHERE phone_number = %s LIMIT 1
    """

    try:
        cursor.execute(search_query, (phone,))
        result = cursor.fetchone()
        response = make_response(jsonify(result))  # Возвращаем данные в исходном виде
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except pymysql.MySQLError as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/search2', methods=['GET'])
def search2():
    connection, cursor = get_db_connection(db_config2)
    if connection is None or cursor is None:
        return jsonify({'error': 'Database connection is not available'}), 500

    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    search_query = """
    SELECT address, birth_date AS date_of_birth, city, email, name
    FROM another_table
    WHERE email = %s LIMIT 1
    """

    try:
        cursor.execute(search_query, (email,))
        result = cursor.fetchone()
        response = make_response(jsonify(result))  # Возвращаем данные в исходном виде
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except pymysql.MySQLError as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
