from flask import Flask, jsonify, send_file
import onlinesheet

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Compta!'

cache = {}
def refresh():
  cache['conventions'] = onlinesheet.getconventiondata()
  cache['orders'] = onlinesheet.getorderdata()
  cache['teams'] = onlinesheet.getteamdata()
refresh()
print('READY!')

@app.route('/api/refresh')
def api_refresh():
  refresh()
  return jsonify({'status': 'OK'})

def jsonifyDF(df):
  return df.to_json(orient="records")

@app.route('/api/conventions')
def api_conventions():
  return jsonifyDF(cache['conventions'])

@app.route('/api/orders')
def api_orders():
  return jsonifyDF(cache['orders'])

@app.route('/api/teams')
def api_teams():
  return jsonifyDF(cache['teams'])
