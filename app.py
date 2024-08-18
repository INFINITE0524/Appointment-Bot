from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize Flask application
app = Flask(__name__)

# Configure the PostgreSQL database using the DATABASE_URL environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apb_user:7jYbxtT3DGMgIydfWLI5zINimel5jGZ1@dpg-cr0l6mrtq21c73ci36c0-a/apb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Appointment model
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.date}>'

# Create an appointment
@app.route('/reserve', methods=['POST'])
def reserve_appointment():
    data = request.json
    date = data.get('date')
    name = data.get('name')

    if not date or not name:
        return jsonify({'message': 'Missing data'}), 400

    existing_appointment = Appointment.query.filter_by(date=date, name=name).first()
    if existing_appointment:
        return jsonify({'message': 'Appointment already exists'}), 400

    new_appointment = Appointment(date=date, name=name)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Reservation successful'}), 201

# Homepage
@app.route('/appointment')
def index():
    return render_template('appointment.html')

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0')
