// This program is failed to forwarding data

var net = require('net');

var HOST = '127.0.0.1';
var PORT = 8680;

var ziyou = net.createServer();
ziyou.listen(HOST, 8580);


net.createServer(function(sock) {

    console.log('Connected: ' + sock.remoteAddress + ':' + sock.remotePort);

    sock.on('data', function(data) {
        ziyou.on('connection', function(ziyou) {
            ziyou.on('data', function(dataz) {
                sock.read(data);
                ziyou.write(data);

                ziyou.read(dataz);
                sock.write(dataz);
            });
        });

    });

}).listen(HOST, PORT);

