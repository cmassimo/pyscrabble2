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

function add_move_to_board(move) {
  for(var i in move) {
    put_tile(move[i].x, move[i].y, move[i].tile);
  }
}

function make_tile(t, can_move) {
    var t = $('<div>')
        .addClass(can_move ? 'tile movable' : 'tile')
        .html(t.letter)
        .data('letter', t.letter)
        .append($('<span>').addClass('tileScore').text(t.score));
    // return can_move ? movable(t) : t;
    return t;
}

function put_tile(x, y, tile)
{
    var element = make_tile(tile, false);
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

$(function() {
  var pusher = new Pusher('a0a56b5e372395197020');
  var channel1 = pusher.subscribe('computer_1');
  var channel2 = pusher.subscribe('computer_2');

  channel1.bind('pusher:subscription_succeeded', function() {
    console.log('--- channel1 subscription_succeeded');

    entry = $("<div class='entry first'>Game started.</div>");
    log(entry);

    $.get("http://localhost:8000/continue");
  });

  channel2.bind('pusher:subscription_succeeded', function() {
    console.log('--- channel2 subscription_succeeded');
  });

  pusher.bind('draw_turn', function(data) {
    console.log('draw_turn');
    console.log(data);

    var entry = $("<div class='entry'>"+ data.string +"</div>");
    log(entry);
    update_rack(data.player.pid-1, data.player.tiles);
    add_move_to_board(data.move);

    $('#player-'+ (data.player.pid-1) +' .playerScore').html(data.player.score)

  });

  pusher.bind('notify_turn', function(data) {
    console.log('notify_turn');
    console.log(data);
  });

  pusher.bind('game_over', function(data) {
    console.log('game_over');
    console.log(data);

    entry = $("<div class='entry'>Game has ended! Finalising scores.</div>");
    log(entry);
  });

  channel1.bind('tiles_updated', function(data) {
    console.log('ch1 tiles_updated');
    console.log(data);
  });

  channel2.bind('tiles_updated', function(data) {
    console.log('ch2 tiles_updated');
    console.log(data);
  });

});