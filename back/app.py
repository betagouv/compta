from flask import Flask, jsonify, send_file
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/conventions')
def api_conventions():
    return send_file('../tmp/onlinesheet.convention.json')

@app.route('/api/orders')
def api_orders():
    return send_file('../tmp/onlinesheet.order.json')

@app.route('/api/teams')
def api_teams():
    return send_file('../tmp/onlinesheet.team.json')
