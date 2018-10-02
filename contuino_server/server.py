# -*- coding: utf-8 -*-

from contuino_core import Board, Action, Events, Sensors
from flask import Flask, request, redirect, jsonify, render_template
from flaskrun import flaskrun
import argparse
import json
import sys

boards = []

app = Flask(__name__)


@app.route('/')
def projects():
    return render_template("index.html")


@app.route("/contuino/api/boards", methods=['GET'])
def boards_api():
    return get_boards()


@app.route("/contuino/api/boards", methods=['POST'])
def post_board():
    board_data = request.json
    board_username = board_data.get('username')
    print(board_username)
    board_id = find_board_index(board_username)
    board = make_board(board_data)
    if board_id == -1:
        boards.append(board)
    else:
        boards[board_id] = board
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


def get_boards():
    tmp_boards = []
    for board in boards:
        tmp_boards.append(str(board))
    return jsonify({'boards': tmp_boards})


def main():
    flaskrun(app, True, '0.0.0.0')
