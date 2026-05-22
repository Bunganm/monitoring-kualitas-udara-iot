from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():

    data = request.json

    with open(
        'sensor_data.json',
        'w'
    ) as f:

        json.dump(data, f)

    return jsonify(
        {"status":"success"}
    )

app.run(
    host='0.0.0.0',
    port=5000
)