from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ap001 = db.Column(db.String(50), nullable=False)  # 預約日期
    ap002 = db.Column(db.String(50), nullable=False)  # 預約者

    def __repr__(self):
        return f'<Appointment {self.id}>'

@app.route('/')
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 確保在首次運行時創建數據庫
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
