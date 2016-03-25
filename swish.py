import json
import os
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    print 'Pong!'
    return 'Pong!'


@app.route('/record', methods=['POST'])
def record():
    new_data = request.json
    print new_data
    return json.dumps({"response": "Got it!"})


@app.route("/download")
def download():
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run()