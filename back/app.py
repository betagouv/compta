from flask import Flask, jsonify, send_file
from flask_cors import CORS
import onlinesheet
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

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
