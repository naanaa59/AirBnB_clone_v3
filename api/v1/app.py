#!/usr/bin/python3
""" This script creates an api flask for hbnb project"""
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception=None):
    return storage.close()


@app.errorhandler(404)
def error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        host = os.environ.get("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if "HBNB_API_PORT" in os.environ:
        port = os.environ.get("HBNB_API_PORT")
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)
