from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql
from datetime import datetime
import pytz
import pandas as pd  # 添加 pandas 的導入

app = Flask(__name__)

# PostgreSQL connection parameters using Internal Database URL
db_params = {
    'dbname': 'apb_m2t4',
    'user': 'apb_m2t4_user',
    'password': '84kTZ1La5ZzJhoQ1EuJpWWq45hQe43VO',
    'host': 'dpg-cr2jhpo8fa8c73dk3r0g-a.singapore-postgres.render.com',
    'port': '5432'
}

@app.route('/getAppointment', methods=['GET'])
def get_appointments():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                query = '''
                    SELECT 
                    TO_CHAR(ap."AP001", 'YYYY-MM-DD') AS "AP001",
                    COALESCE(mb."MB002", '未知') AS "MB002"
                    FROM "AP00" ap
                    LEFT JOIN "MB00" mb ON ap."AP002" = mb."MB001"
                '''
                cur.execute(query)
                rows = cur.fetchall()

                # 将数据转换为 FullCalendar 的事件格式
                appointments = [{"title": row[1], "start": row[0]} for row in rows]

                return jsonify({"appointments": appointments})
    except Exception as e:
        return jsonify({"error": str(e)})
        
# Function to fetch appointments from the database
def fetch_record(ap002_person):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                query =  '''
                    SELECT 
                    TO_CHAR(ap."AP001", 'YYYY-MM-DD') AS "AP001",
                    COALESCE(mb."MB002", '未知') AS "MB002"
                    FROM "AP00" ap
                    LEFT JOIN "MB00" mb ON ap."AP002" = mb."MB001"
                    WHERE ap."AP002" = %s;
                 '''
                cur.execute(query, (ap002_person,))
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
                create_date = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S.%f')
                # 插入預約記錄
                query_insert = sql.SQL('INSERT INTO "AP00" ("CreateDate", "AP001", "AP002") VALUES (%s, %s, %s);')
                cur.execute(query_insert, (create_date, ap001_date, ap002_person))
                conn.commit()
                
                # 查詢MB002
                query_select = sql.SQL('SELECT "MB002" FROM "MB00" WHERE "MB001" = %s;')
                cur.execute(query_select, (ap002_person,))
                result = cur.fetchone()
                
        return {'message': '預約成功', 'name': result[0]}
    except Exception as e:
        return {'errormsg': str(e)}

# Route to create an appointment
@app.route('/sentAppointment', methods=['POST'])
def reserve_appointment():
    data = request.json
    ap001_date = data.get('date')
    ap002_person = data.get('person')

    if not ap001_date or not ap002_person:
        return jsonify({'message': '缺少資料'}), 400

    result = insert_appointment(ap001_date, ap002_person)
    if 'errormsg' in result:
        return jsonify({'message': result['errormsg']}), 400
    else:
        return jsonify(result), 201

# Route to fetch all appointments
@app.route('/getRecord', methods=['POST'])
def get_record():
    data = request.json
    ap002_person = data.get('person')
    
    df, error = fetch_record(ap002_person)
    if error:
        return jsonify({'message': error['errormsg']}), 400
    else:
        return df.to_json(orient='records'), 200

# appointment route
@app.route('/appointment')
def appointmentHTML():
    return render_template('appointment.html')

# record route
@app.route('/record')
def recordHTML():
    return render_template('record.html')

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0')
