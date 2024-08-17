from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化 Flask 應用
app = Flask(__name__)

# 設定 SQLite 資料庫連接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy 和 Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 定義 Appointment 模型
class Appointment(db.Model):
    __tablename__ = 'AP00'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.date}>'

# 創建預約
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    date = data.get('date')
    name = data.get('name')

    if not date or not name:
        return jsonify({'message': 'Missing data'}), 400

    new_appointment = Appointment(date=date, name=name)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment created'}), 201



# 網頁首頁
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # 啟動應用
    app.run(debug=True, host='0.0.0.0')
