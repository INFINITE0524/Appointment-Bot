from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    person = db.Column(db.String(100), nullable=False)

    def __init__(self, date, person):
        self.date = date
        self.person = person

@app.route('/appointment')
def home():
    return render_template('appointment.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    date = data.get('date')
    person = data.get('person')

    if not date or not person:
        return jsonify({'error': 'Missing data'}), 400

    try:
        AP00 = AP00(date=date, person=person)
        db.session.add(AP00)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
