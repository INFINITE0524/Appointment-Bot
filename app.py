from flask import Flask, request, jsonify, render_template
import sqlite3
from sqlite3 import Error

# Initialize Flask application
app = Flask(__name__)

# Helper function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('APB.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create an appointment
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    date = data.get('date')
    name = data.get('name')

    if not date or not name:
        return jsonify({'message': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO AP00 (date, name) VALUES (?, ?)', (date, name))
        conn.commit()
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Appointment created'}), 201

# Homepage
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0')
