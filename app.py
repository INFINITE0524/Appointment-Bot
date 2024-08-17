from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///APB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Appointment model
class Appointment(db.Model):
    __tablename__ = 'AP00'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.date}>'

# Create an appointment
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

# List all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'date': a.date,
        'name': a.name
    } for a in appointments])

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0')
