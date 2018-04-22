'''
Created on Apr 22, 2018

@author: varunjai
'''
'''
Config
'''

import os

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO

from com.varun.game.Game import Game
from com.varun.game.PlayerData import PlayerData

# configuration
game_server = Flask(__name__)
game_server.session_key = str(os.urandom(24))
game_server.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(game_server)

game = None
players = []


@socketio.on('move_event')
def handle_message(message):
    print('received message: ' + message)


@game_server.route('/')
def index():
    return render_template('index.html')


@game_server.route('/login')
def login():
    if(session and 'user' in session):
        return __start()
    
    return render_template('login.html')
    


@game_server.route('/start', methods=['POST'])
def start_game():
    global players
    # register users
    if('user' not in session or session['user'] is not request.form['user']):    
        players.append(PlayerData(request.form['user'], 'X' if len(players) == 0 else 'O'))
        session['user'] = request.form['user']

    return __start()


def __start():

    global players
    # wait if players are inadequate
    if(len(players) != 2):
        print('Waiting for other player t o join')
        return render_template('wait.html')

    # launch game
    global game
    game = Game(players[0], players[1], 3)
    socketio.emit('start_event')
    return render_template('start.html')

'''
Join the game
'''

@game_server.route('/join')
def join_game():
    if(len(players) != 2):
        print('Waiting for other player to join')
        return render_template('wait.html')
    return render_template('start.html')


'''
Get the player who is having the current turn
'''


@game_server.route('/currentplayer')
def current_player():
    global game
    return game.get_current_player().get_player_name(), 200


@game_server.route('/move')
def move():

    global game
    # if not the player with current turn
    if(session['user'] != game.get_current_player().get_player_name()):
        return '', 201

    # check params
    x = request.args.get('x')
    y = request.args.get('y')

    if(x is None or y is None):
        return '', 400

    # make move
    result = game.move(int(x), int(y))
    # invalid move
    if(result is None or result is ''):
        return '', 201

    # valid move
    socketio.emit('move_event', data="x:" + x + " y:" + y + " style:" + result)
    return '', 201


@game_server.route('/checkgame')
def check_game():
    global game
    return game.checkGame(), 200


@game_server.route('/exitgame')
def exit_game():
    global game
    game = None
    return render_template('index.html')


'''
Shutdown code
'''


def shutdown_server():
    if(session and 'user' in session):
        session.pop('user', None)
        
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@game_server.route("/shutdown")
def shutdown():
    shutdown_server()
    return "OK", 200


'''
Start server
'''
if __name__ == '__main__':
    if(session and 'user' in session):
        session.pop('user', None)
        
    socketio.run(game_server, host='0.0.0.0', port=5000)
    # game_server.secret_key = 'some secret key'
    # game_server.run(host='0.0.0.0', port=5000, threaded=True)
