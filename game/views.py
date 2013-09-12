from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

import json
from multiprocessing import Process
# from pusher import Pusher

from word_lookup import WordLookup
from config import ScrabbleConfig, Coordinate
from setup import *

def index(request):
    request.session['game'] = None

    length = ScrabbleConfig.board_length
    css_grid = [ [ ScrabbleConfig.board_layout( Coordinate(i, j) ) for j in xrange(0, length) ] for i in xrange(0, length) ]
        
    return render(request, 'game/index.html', {'board': css_grid, 'board_length': length})

def game(request):
    if request.method == 'POST':
        post_params = request.POST

        if request.session['game'] == None:
            word_lookup = WordLookup()
            setup_game_state(word_lookup, post_params['player1_name'], post_params['player2_name'])

            for player in Game.instance.players:
                apply_setup_values(word_lookup, player, 0, 0)

            request.session['game'] = Game.instance
        else:
            Game.instance = request.session['game']

        length = ScrabbleConfig.board_length
        css_grid = [ [ ScrabbleConfig.board_layout( Coordinate(i, j) ) for j in xrange(0, length) ] for i in xrange(0, length) ]
            
        return render(request, 'game/game.html', {'board': css_grid, 'board_length': length, 'post_params': post_params})

    elif request.method == 'GET':
        return redirect('/')

# @csrf_exempt
# def auth(request):
#     channel_name = request.POST['channel_name']
#     socket_id = request.POST['socket_id']
  
#     p = Pusher(
#         app_id='53591',
#         key='a0a56b5e372395197020',
#         secret='0f0db5e609af25a002c3'
#     )
  
#     auth = p[channel_name].authenticate(socket_id)

#     return HttpResponse(json.dumps(auth), mimetype="application/json")

def continue_game(request):
    Game.instance = request.session['game']

    if Game.instance:
        Process(target=go, args=(Game.instance,)).start()
        return HttpResponse(json.dumps(True), mimetype="application/json")
    else:
        raise Http404

def go(state):
    state.continue_game()


