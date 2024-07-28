import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def api():
  return 'API is working'

if __name__ == '__main__':
    app.run(debug=True)
