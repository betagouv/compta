from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data')
def api_data():
    return jsonify({'message': 'Hello, World!'})
