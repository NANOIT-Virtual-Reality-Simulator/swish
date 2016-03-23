from flask import Flask, request
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
data = []


@app.route('/ping', methods=['GET'])
def ping():
    print 'Pong!'
    return 'Pong!'

@app.route('/collect', methods=['POST'])
def collect():
    new_data = request.json
    print new_data
    return 'Got it!'



if __name__ == '__main__':
    app.run()