from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 連接到 SQLite 數據庫
def get_db_connection():
    conn = sqlite3.connect('APB.db')
    conn.row_factory = sqlite3.Row
    return conn

# 創建一個預約
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    date = data.get('date')
    name = data.get('name')

    if not date or not name:
        return jsonify({'message': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO AP00 (date, name) VALUES (?, ?)", (date, name))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Appointment created'}), 201

# 主頁
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # 運行應用
    app.run(debug=True, host='0.0.0.0')
