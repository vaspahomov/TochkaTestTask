#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb', 27017)
db = client.tododb


@app.route('/', methods=['GET'])
def hello():
    return 'Hello world!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
