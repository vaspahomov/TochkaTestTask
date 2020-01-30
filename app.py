#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from pymongo import MongoClient

from entities.Account import Account

app = Flask(__name__)

client = MongoClient('mongodb', 27017)
db = client.tododb

accounts = {
    '0': Account('Петров Иван Сергеевич', 1700, 300, True)
}


@app.route('/api/ping', methods=['GET'])
def api_ping():
    subscriber_number = request.args.get('subscriberNumber')
    return jsonify(
        status=200,
        result=True,
        addition='Service works well',
        description={}
    )


@app.route('/api/add', methods=['POST'])
def api_add():
    account_number = request.json['accountNumber']
    addition = int(request.json['addition'])
    account = accounts[account_number]
    account.add(addition)
    return jsonify(
        status=200,
        result=True,
        addition='Transaction finished well',
        description='Transaction status'
    )


@app.route('/api/substract', methods=['POST'])
def api_substract():
    account_number = request.json['accountNumber']
    substraction = int(request.json['substraction'])
    account = accounts[account_number]
    account.substract(substraction)
    return jsonify(
        status=200,
        result=True,
        addition='Transaction finished well',
        description='Transaction status'
    )


@app.route('/api/status', methods=['GET'])
def api_status():
    account_number = request.args.get('accountNumber')
    return 'Hello world!'


# test methods
@app.route('/api/accounts', methods=['GET'])
def api_accounts():
    return jsonify(
        status=200,
        result=True,
        addition=[accounts[a].serialize() for a in accounts],
        description='Accounts listing'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
