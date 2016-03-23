from flask import Flask, request

app = Flask(__name__)
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