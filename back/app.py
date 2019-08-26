from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask, jsonify, make_response
from flask_cors import CORS
import onlinesheet


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
  resp = make_response(df.to_json(orient="records"))
  resp.headers['Content-Type'] = 'application/json'
  return resp

@app.route('/api/conventions')
def api_conventions():
  return jsonifyDF(cache['conventions'])

@app.route('/api/orders')
def api_orders():
  return jsonifyDF(cache['orders'])

@app.route('/api/teams')
def api_teams():
  return jsonifyDF(cache['teams'])
