$(function() {
  var pusher = new Pusher('a0a56b5e372395197020');
  var channel = pusher.subscribe('human');

  channel.bind('hello_world', function(data) {
    console.log("HELLO WORLD")
  });
});