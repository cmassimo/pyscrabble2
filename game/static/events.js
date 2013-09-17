/* BEGIN utils */
function log(entry) {
  if ($('.inner div').size() % 2 == 0)
    entry.addClass('alt')

  $('#console .inner').prepend(entry);
}

function update_rack(player_id, tiles) {
  var rack = $('#player-'+ player_id +' .rack');
  rack.html('');

  for(var i in tiles) {
    rack.append($("<div class='tile' data-letter='" + tiles[i].letter + "'>" + tiles[i].letter + "<span class='tileScore'>" + tiles[i].score + "</span></div>"));
  }

}

function add_move_to_board(move, cls) {
  if (cls == undefined)
    cls = ''
  
  for(var i in move) {
    put_tile(move[i].x, move[i].y, move[i].tile, cls);
  }
}

function make_tile(t, can_move, cls) {
    var classes = can_move ? ('tile movable ' + cls) : ('tile ' + cls);
    var t = $('<div>')
        .addClass(classes)
        .html(t.letter)
        .data('letter', t.letter)
        .append($('<span>').addClass('tileScore').text(t.score));
    // return can_move ? movable(t) : t;
    return t;
}

function put_tile(x, y, tile, cls)
{
    var element = make_tile(tile, false, cls);
    var square = find_square(x, y);
    append_to_square(element, square);
    square.addClass('occupied');
    return square;
}

function find_square(x, y)
{
    return $('#board tr:eq(' + y + ') td:eq(' + x + ')');
}

function append_to_square(e, square)
{
    square.children().first().html($(e));
}

/* END utils */

$(function() {
  var pusher = new Pusher('a0a56b5e372395197020');

  var channel1 = pusher.subscribe('computer_' + $('#player-0').data('pid'));
  var channel2 = pusher.subscribe('computer_' + $('#player-1').data('pid'));

  channel1.bind('pusher:subscription_succeeded', function() {
    console.log('--- channel1 subscription_succeeded');

    entry = $("<div class='entry first'>Game started.</div>");
    log(entry);

    $.get("/continue");
  });

  channel2.bind('pusher:subscription_succeeded', function() {
    console.log('--- channel2 subscription_succeeded');
  });

  channel1.bind('draw_turn', function(data) {
    console.log('draw_turn');
    console.log(data);

    var entry = $("<div class='entry'>"+ data.string +"</div>");
    log(entry);
    update_rack(0, data.player.tiles);
    // $('.tile.debug').remove();
    add_move_to_board(data.move);
    $('.tile.debug').remove();

    $('#player-0 .playerScore').html(data.player.score)

  });

  channel1.bind('notify_turn', function(data) {
    console.log('notify_turn');
    console.log(data);
  });

  channel1.bind('game_over', function(data) {
    console.log('game_over');
    console.log(data);

    entry = $("<div class='entry'>Game has ended! Finalising scores.</div>");
    log(entry);
  });

  channel1.bind('tiles_updated', function(data) {
    console.log('ch1 tiles_updated');
    console.log(data);
    update_rack(0, data.tiles);
  });

  channel2.bind('draw_turn', function(data) {
    console.log('draw_turn');
    console.log(data);

    var entry = $("<div class='entry'>"+ data.string +"</div>");
    log(entry);
    update_rack(1, data.player.tiles);
    // $('.tile.debug').remove();
    add_move_to_board(data.move);
    $('.tile.debug').remove();

    $('#player-1 .playerScore').html(data.player.score)

  });

  channel2.bind('notify_turn', function(data) {
    console.log('notify_turn');
    console.log(data);
  });

  channel2.bind('game_over', function(data) {
    console.log('game_over');
    console.log(data);

    entry = $("<div class='entry'>Game has ended! Finalising scores.</div>");
    log(entry);
  });

  channel2.bind('tiles_updated', function(data) {
    console.log('ch2 tiles_updated');
    console.log(data);
    update_rack(1, data.tiles);
  });


  channel1.bind('debug', function(data) {
    console.log('debug');
    console.log(data);

    for(var i in data) {
      add_move_to_board(data, 'debug');
    }
  });

  channel1.bind('clear_debug', function(data) {
    $('.tile.debug').remove();
  });

});