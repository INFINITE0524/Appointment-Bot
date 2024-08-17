from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Appointment(db.Model):
    __tablename__ = 'AP00'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, date, name):
        self.date = date
        self.name = name

@app.route('/appointment')
def home():
    return render_template('appointment.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    date = data.get('date')
    name = data.get('name')

    if not date or not name:
        return jsonify({'error': 'Missing data'}), 400

    try:
        new_appointment = Appointment(date=date, name=name)
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': 'Reservation successful'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(host='0.0.0.0', port=5000)
