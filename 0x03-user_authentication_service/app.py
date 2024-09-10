#!/usr/bin/env python3
"""flask app basic
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def welcome() -> str:
    """ main root method"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
