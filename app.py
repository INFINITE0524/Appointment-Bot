from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 設置 SQLite 資料庫 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 定義 Appointment 資料模型
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)

    def __init__(self, date):
        self.date = date

# 初始化資料庫
with app.app_context():
    db.create_all()



# 路由：處理預約請求
@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    date = data.get('date')

    # 創建新的預約記錄並保存到資料庫
    new_appointment = Appointment(date)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': f'已預約 {date}'}), 201

if __name__ == '__main__':
    app.run(debug=True)
