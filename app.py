from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Example route for GET request
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'

# Example route for POST request
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    # Process the data (e.g., save to database)
    response = {
        'status': 'success',
        'data': data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
