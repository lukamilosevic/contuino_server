# -*- coding: utf-8 -*-

from contuino_core import Board, Action, Events, Sensors
from flask import Flask, request, redirect, jsonify, render_template
from flaskrun import flaskrun
from flask_pymongo import PyMongo
from bson.json_util import dumps
import argparse
import json
import sys

boards = []

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/contuino"
mongo = PyMongo(app)


@app.route('/')
def projects():
    return render_template("index.html")


@app.route("/contuino/api/boards", methods=['GET'])
def boards_api():
    tmp_boards = []
    boards = mongo.db.boards
    return dumps(boards.find({}))


@app.route("/contuino/api/boards", methods=['POST'])
def post_board():
    board_data = request.json
    board_username = board_data.get('username')
    boards = mongo.db.boards
    query = {'username': board_username}
    board = mongo.db.boards.find_one(query)
    if not board:
        boards.insert(json.loads(str(make_board(board_data))))
    else:
        boards.update(query, json.loads(str(make_board(board_data))))
    return str(board)


def make_board(board_data):
    board = Board()
    board.username = board_data.get('username')
    board.name = str(board_data.get('name'))
    board.message = str(board_data.get('message'))
    board.actions = []
    for action in board_data.get('actions'):
        tmp_action = Action(action['event'], action['value'], action[
            'sensor'], action['sensor_code'])
        board.add_action(tmp_action)
    return board


def find_board_index(username):
    for i, board in enumerate(boards):
        if board.username == username:
            return i
    return -1


def main():
    flaskrun(app, True, '0.0.0.0')
