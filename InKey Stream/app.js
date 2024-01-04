var express = require("express");
var app = new express();
var http = require("http").Server(app);
var io = require("socket.io")(http);

var port = process.env.PORT || 3000;

app.use(express.static(__dirname + "/test_audio_Stream"));

app.get('/', function(req, res) {
    res.redirect('index.html');
});

io.on('connection', function(socket) {
    socket.on('enter', function(roomName){
        socket.join(roomName);
        socket.on('stream', function(blob) {
            socket.to(roomName).emit('stream', blob);
        });
        
        socket.on('sendMessage', function(res) {
            console.log(res);
            io.in(roomName).emit('receiveMessage', res);
        });
    });
});
io.on("disconnect", function(socket){

})



http.listen(port, function() {
});