from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 設定 SQLite 資料庫位置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫
db = SQLAlchemy(app)

# 定義資料庫模型
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    person = db.Column(db.String(100), nullable=False)

    def __init__(self, date, person):
        self.date = date
        self.person = person

# 創建資料庫表格
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/appointment')
def home():
    return render_template('appointment.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    try:
        data = request.json
        date = data.get('date')
        person = data.get('person')

        if not date or not person:
            return jsonify({'error': '缺少日期或預約者信息'}), 400

        new_appointment = Appointment(date=date, person=person)
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': f'預約成功: {date}'}), 200
    except Exception as e:
        db.session.rollback()  # 在出錯時回滾事務
        return jsonify({'error': f'伺服器錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
