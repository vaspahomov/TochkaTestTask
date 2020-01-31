#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from helpers.AccountsUpdaterDemon import AccountsUpdaterDemon
from db_collections.AccountsCollection import AccountsCollection
from entities.Account import Account
from exceptions.NotEnoughMoneyException import NotEnoughMoneyException

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

logger = app.logger

logger.setLevel(logging.INFO)

client = MongoClient('mongodb', 27017)
bank_accounts_db = client.bank_accounts_db

accounts_collection = AccountsCollection(bank_accounts_db, logger)

accounts_updater_demon = AccountsUpdaterDemon(logger, accounts_collection)


@app.route('/api/ping', methods=['GET'])
def api_ping():
    return jsonify(
        status=200,
        result=True,
        addition='Service works well.',
        description='Current service status.'
    )


@app.route('/api/add', methods=['POST'])
def api_add():
    if 'accountNumber' not in request.json or 'addition' not in request.json:
        return jsonify(
            status=400,
            result=False,
            addition='Missing required fields in request.',
            description='Transaction status.'
        ), 400
    account_number = request.json['accountNumber']
    addition = int(request.json['addition'])
    accounts_collection.increment_balance(account_number, addition)
    return jsonify(
        status=200,
        result=True,
        addition='Transaction finished well.',
        description='Transaction status.'
    )


@app.route('/api/substract', methods=['POST'])
def api_substract():
    if 'accountNumber' not in request.json or 'substraction' not in request.json:
        return jsonify(
            status=400,
            result=False,
            addition='Missing required fields in request.',
            description='Transaction status.'
        ), 400
    account_number = request.json['accountNumber']
    substraction = int(request.json['substraction'])
    try:
        accounts_collection.decrement_balance(account_number, substraction)
    except NotEnoughMoneyException:
        return jsonify(
            status=403,
            result=True,
            addition='Transaction failed. You does not have enough money for this operation.',
            description='Transaction status.'
        ), 403
    return jsonify(
        status=200,
        result=True,
        addition='Transaction finished well.',
        description='Transaction status.'
    )


@app.route('/api/status', methods=['GET'])
def api_status():
    if 'accountNumber' not in request.args:
        return jsonify(
            status=400,
            result=False,
            addition='Missing required fields in request.',
            description='Transaction status.'
        ), 400
    account_number = request.args.get('accountNumber')
    return jsonify(
        status=200,
        result=True,
        addition=accounts_collection.get_account(account_number).serialize(),
        description='Account status.'
    )


# test methods
@app.route('/api/accounts', methods=['GET'])
def api_accounts():
    return jsonify(
        status=200,
        result=True,
        addition=[a.serialize() for a in accounts_collection.get_all_accounts()],
        description='Accounts listing.'
    )


@app.route('/api/create', methods=['POST'])
def api_create():
    if 'name' not in request.json:
        return jsonify(
            status=400,
            result=False,
            addition='Missing required fields in request.',
            description='Account creation.'
        ), 400
    account = Account(request.json['name'])
    accounts_collection.create_new_account(account)
    return jsonify(
        status=200,
        result=True,
        addition='Account was successfully created.',
        description='Account creation.'
    )


if __name__ == "__main__":
    accounts_updater_demon.start()
    for a in accounts_collection.get_all_accounts():
        accounts_updater_demon.subscribe_id(a.id)
    app.run(host='0.0.0.0')
