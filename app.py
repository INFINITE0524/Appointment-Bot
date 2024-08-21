from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
from datetime import datetime
import pytz
import pandas as pd  # 添加 pandas 的导入

app = Flask(__name__)

# PostgreSQL connection parameters using Internal Database URL
db_params = {
    'dbname': 'apb_m2t4',
    'user': 'apb_m2t4_user',
    'password': '84kTZ1La5ZzJhoQ1EuJpWWq45hQe43VO',
    'host': 'dpg-cr2jhpo8fa8c73dk3r0g-a.singapore-postgres.render.com',
    'port': '5432'
}

# Function to fetch appointments from the database
def fetch_appointments():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                query =  '''
                    SELECT 
                    TO_CHAR("CreateDate", 'YYYY-MM-DD"T"HH24:MI:SS') AS CreateDate, 
                    TO_CHAR("AP001", 'YYYY-MM-DD') AS AP001, 
                    "AP002"
                    FROM "AP00";
                 '''
                cur.execute(query)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=columns)
        return df, {}
    except Exception as e:
        return pd.DataFrame(), {'errormsg': str(e)}

# Function to insert an appointment into the database
def insert_appointment(ap001_date, ap002_person):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                create_date = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
                query = sql.SQL('INSERT INTO "AP00" ("CreateDate", "AP001", "AP002") VALUES (%s, %s, %s);')
                cur.execute(query, (create_date, ap001_date, ap002_person))
                conn.commit()
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
    # Run the application
    app.run(debug=True, host='0.0.0.0')
