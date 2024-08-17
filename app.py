from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ap001 = db.Column(db.String(100), nullable=False)
    ap002 = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()  # 創建所有表格

@app.route('/appointment')
def home():
    return render_template('appointment.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    date = data.get('date')
    person = data.get('person')

    if not date or not person:
        return jsonify({'error': '缺少日期或預約者信息'}), 400

    try:
        new_appointment = Appointment(ap001=date, ap002=person)
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': f'預約成功: {date}'}), 200
    except Exception as e:
        db.session.rollback()  # 在出錯時回滾事務
        return jsonify({'error': f'伺服器錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
