import json
import os
from flask import Flask, request, Response

app = Flask(__name__)
cache = []


@app.route('/ping', methods=['GET'])
def ping():
    print 'Pong!'
    return 'Pong!'


@app.route('/record', methods=['POST'])
def record():
    global cache
    cache.extend(parse_shot(request.json))
    return json.dumps({"response": "Got it!"})


@app.route("/download")
def download():
    return Response(
        '\n'.join([','.join(entry) for entry in cache]),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=shots.csv"})


@app.route("/clear")
def clear():
    global cache
    cache = []
    return json.dumps({"response": "Cache cleared"})


def parse_shot(raw_shot):
    shot_name = raw_shot.keys()[0]
    return [map(str, [reading['time'], reading['x'], reading['y'], reading['z'], shot_name])
            for reading in raw_shot[shot_name]]


if __name__ == '__main__':
    # Bind to PORT env var if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)