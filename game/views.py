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
            state = setup_game_state(word_lookup, 'com1', 'com2', post_params['debug'])

            apply_setup_values(state, word_lookup, state.players[0], int(post_params['strategy1']), int(post_params['utility1']))
            apply_setup_values(state, word_lookup, state.players[1], int(post_params['strategy2']), int(post_params['utility2']))

            request.session['game'] = state
        else:
            state = request.session['game']

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
    state = request.session['game']

    if state:
        Process(target=go, args=(state,)).start()
        return HttpResponse(json.dumps(True), mimetype="application/json")
    else:
        raise Http404

def go(state):
    state.continue_game()


