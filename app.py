from flask import Flask, request, jsonify, render_template
import sqlite3 as lite
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# SQLite database path
dbpath = 'APB.db'

# Function to fetch appointments from the database
def fetch_appointments():
    if not os.path.exists(dbpath):
        return pd.DataFrame(), {'errormsg': '找不到 APB.db'}

    try:
        with lite.connect(dbpath) as con:
            query = "SELECT * FROM AP00;"
            df = pd.read_sql_query(query, con)
        return df, {}
    except Exception as e:
        return pd.DataFrame(), {'errormsg': str(e)}

# Function to insert an appointment into the database
def insert_appointment(ap001_date, ap002_person):
    if not os.path.exists(dbpath):
        return {'errormsg': '找不到 APB.db'}

    try:
        with lite.connect(dbpath) as con:
            cur = con.cursor()
            create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO AP00 (CreateDate, AP001, AP002) VALUES (?, ?, ?);"
            cur.execute(query, (create_date, ap001_date, ap002_person))
            con.commit()
        return {'message': '預約成功'}
    except Exception as e:
        return {'errormsg': str(e)}

# Route to create an appointment
@app.route('/reserve', methods=['POST'])
def reserve_appointment():
    data = request.json
    ap001_date = data.get('date')
    ap002_person = data.get('person')

    if not ap001_date or not ap002_person:
        return jsonify({'message': 'Missing data'}), 400

    result = insert_appointment(ap001_date, ap002_person)
    if 'errormsg' in result:
        return jsonify({'message': result['errormsg']}), 400
    else:
        return jsonify({'message': result['message']}), 201

# Route to fetch all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    df, error = fetch_appointments()
    if error:
        return jsonify({'message': error['errormsg']}), 400
    else:
        return df.to_json(orient='records'), 200

# Homepage route
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # Check if the database exists before starting the app
    if not os.path.exists(dbpath):
        raise FileNotFoundError(f"Database file not found: {dbpath}")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0')
