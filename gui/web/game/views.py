from django.shortcuts import render

from word_lookup import WordLookup
from setup import *

def index(request):
    state = setup_game_state()
    word_lookup = WordLookup()
    for player in Game.instance.plyers:
      apply_setup_values(word_lookup, player, 0, 0)

    request.session['game'] = Game.instance

        
    return render(request, 'game/index.html')
