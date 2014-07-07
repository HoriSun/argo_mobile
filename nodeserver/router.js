var common = require('./common');

function route(pathname){
    var self = route;
    self.log = common.log;
    
    self.log('About to route a request for ' + pathname);
}

exports.route = route;