import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

import process

app = Flask(__name__)
CORS(app)
@app.route("/", methods=["GET"])
def hello():
    message = {"message": "Welcome to SalesCast"}
    return jsonify(message)

@app.route("/process-data", methods=["POST"])
def upload_file():
    files = request.files.getlist("fileInput")
    if not files:
        return jsonify({"error": "no file uploaded"})
    print(request.values.get("periodicity"))
    print(request.values.get("periods"))

    file = files[0]
    df = pd.read_csv(file.stream, index_col='Date', parse_dates=True)
    return jsonify({"img": process.main(request.values.get("periodicity"), request.values.get("periods"), df)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")





