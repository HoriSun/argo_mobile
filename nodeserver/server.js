var http = require('http');
var url = require('url');
var common = require('./common');

var port = 8080;

function start(){
    var self = start;
    self.log = common.log;

    function onRequest(request, response){
        var self = onRequest;
        self.log = common.log;

        var pathname = url.parse(request.url).pathname;
        self.log("Request for " + pathname + " received.");

        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.write('Where would you like to go?\n' + pathname);
        response.end();
    }

    server = http.createServer(onRequest);
    server.listen(port);
    self.log("Server started.");
}

exports.start = start;