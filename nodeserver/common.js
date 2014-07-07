String.prototype.multi = function(time){
    var res = '';
    for(i=0;i<time;i++)
        res += this;
    return res;
}

function log(message){
    var name = "log";
    var callerName = this.name;
    var subname = name;
    if(callerName)
        subname = callerName.substring(0,10);
    var len = ((10 - subname.length)/2 - 0.5).toFixed();
    var output = "[" + ' '.multi(len) + subname + ' '.multi(10-subname.length-len) + ']';
    if(message)
        output += ' ' + message;
    console.log(output);
}

exports.log = log;



//------ EXAMPLE ------\\
function tester(){
    var self = tester;

    self.log = log;
    self.log("aha");
}

