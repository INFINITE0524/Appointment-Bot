from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
db = SQLAlchemy(app)

class AP00(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    AP001 = db.Column(db.String(50), nullable=False)
    AP002 = db.Column(db.String(50), nullable=False)

@app.route('/appointment')
def index():
    return render_template('appointment.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    ap001 = data.get('date')
    ap002 = data.get('person')
    
    if not ap001 or not ap002:
        return jsonify({'error': '缺少日期或人員資訊'}), 400

    new_reservation = AP00(AP001=ap001, AP002=ap002)
    db.session.add(new_reservation)
    db.session.commit()
    
    return jsonify({'message': '預約成功'}), 200

if __name__ == '__main__':
    app.run(debug=True)
