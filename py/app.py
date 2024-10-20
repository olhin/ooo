import traceback
from flask import Flask, request, jsonify, make_response
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Параметры подключения к базе данных
db_config = {
    'host': '192.168.1.100',
    'user': 'other',
    'password': '000000000',
    'database': 'osint',
    'port': 3306
}

def get_db_connection():
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None

@app.route('/search', methods=['GET'])
def search():
    connection, cursor = get_db_connection()
    if connection is None or cursor is None:
        return jsonify({'error': 'Database connection is not available'}), 500

    phone = request.args.get('phone')
    if not phone:
        return jsonify({'error': 'Phone parameter is required'}), 400

    # Замените на правильные имена столбцов в вашей таблице
    search_query = """
    SELECT address, birth_date AS date_of_birth, city, email, name, phone_number
    FROM sportmaster
    WHERE phone_number = %s LIMIT 1
    """
    

    try:
        cursor.execute(search_query, (phone,))
        result = cursor.fetchone()

        if result:
            columns = ['address', 'date_of_birth', 'city', 'email', 'name', 'phone_number']
            data = dict(zip(columns, result))
        else:
            data = {}

        response = make_response(jsonify(data))
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
