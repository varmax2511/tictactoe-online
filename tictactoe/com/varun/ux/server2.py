'''
Created on Apr 22, 2018

@author: varunjai
'''
from com.varun.player.AIPlayer import AIPlayer
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
mp_players_data = []
sp_players_data = []
aiplayer = None


@socketio.on('move_event')
def handle_message(message):
    print('received message: ' + message)


@game_server.route('/')
def index():
    return render_template('index.html')


@game_server.route('/login')
def login():
    mode = request.args.get('mode')
    if(session and 'user' in session):
        if(mode == 'single-player'):
            return start_sp_game()
        else:
            return __start(mp_players_data, 'startmp.html')

    return render_template('login.html')


@game_server.route('/startmp', methods=['POST'])
def start_game():
    global mp_players_data
    # register users
    if('user' not in session or session['user'] is not request.form['user']):
        mp_players_data.append(PlayerData(request.form['user'], 'X' if len(mp_players_data) == 0 else 'O'))
        session['user'] = request.form['user']

    return __start(mp_players_data, 'startmp.html')


'''
Start a single player game.
This creates an instance of AI player as the second instance of the player


See if the game is set to none then it means that even if the users are present
the game has been reset. This is an instance where a user is playing another game
'''


@game_server.route('/startsp', methods=['POST'])
def start_sp_game():
    global sp_players_data
    global aiplayer
    global game

    # if two players already added
    if(len(sp_players_data) == 2):
        # if its not a new game
        if(game is not None and aiplayer is not None):
            return __start(sp_players_data, 'startsp.html')
        else:
            result = __start(sp_players_data, 'startsp.html')
            aiplayer = AIPlayer('AI', 'O', game)
            return result

    # register users
    if('user' not in session or session['user'] is not request.form['user']):
        sp_players_data.append(PlayerData(request.form['user'], 'X'))
        session['user'] = request.form['user']
        sp_players_data.append(PlayerData('AI', 'O'))
        result = __start(sp_players_data, 'startsp.html')
        aiplayer = AIPlayer('AI', 'O', game)
        return result

    return __start(sp_players_data, 'startsp.html')


def __start(players_data, template):

    # wait if mp_players_data are inadequate
    if(len(players_data) != 2):
        print('Waiting for other player to join')
        return render_template('wait.html')

    # launch game
    global game
    game = Game(players_data[0], players_data[1], 3)
    socketio.emit('start_event')
    return render_template(template)


'''
Join the game
'''


@game_server.route('/join')
def join_game():
    if(len(mp_players_data) != 2):
        print('Waiting for other player to join')
        return render_template('wait.html')
    return render_template('startmp.html')


'''
Get the player who is having the current turn
'''


@game_server.route('/currentplayer')
def current_player():
    global game
    if(game is None):
        return '', 401
    return game.get_current_player().get_player_name(), 200


@game_server.route('/move')
def move_mp():
    global game
    # if not the player with current turn
    if(session['user'] != game.get_current_player().get_player_name()):
        return '', 201

    # check params
    x = request.args.get('x')
    y = request.args.get('y')

    return __move(int(x), int(y))


'''
Make the move on the board
'''


def __move(x: int, y: int):

    if(x is None or y is None):
        return '', 400

    # make move
    global game
    result = game.move(x, y)
    # invalid move
    if(result is None or result is ''):
        return '', 201

    # valid move
    socketio.emit('move_event', data="x:" + str(x) + " y:" + str(y) + " style:" + result)
    return '', 201


@game_server.route('/movesp')
def move_sp():

    if(game is None):
        return '', 401
    
    if(game.get_current_player().get_player_name() == 'AI'):
        # AI player move
        global aiplayer
        move_param = aiplayer.move()

        if(move_param is None):
            return '', 201
        return __move(move_param.getXval(), move_param.getYval())

    # if not the player with current turn and not AI
    if(session['user'] != game.get_current_player().get_player_name()):
        return '', 201

    # if not the player with current turn
    # check params
    x = request.args.get('x')
    y = request.args.get('y')
    return __move(int(x), int(y))


@game_server.route('/checkgame')
def check_game():
    global game
    return game.checkGame(), 200


@game_server.route('/exitgame')
def exit_game():
    print("exiting game session")
    global game
    global aiplayer
    game = None
    aiplayer = None
    return render_template('index.html')


'''
Shutdown code
'''


def shutdown_server():
    if(session and 'user' in session):
        session.pop('user', None)
    
    exit_game()
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
