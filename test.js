var fs = require('fs')

var test = function(){
  fs.writeFile('test.txt', 
               'port: ' + DB_PORT + '\n' +
               ' port_27017: ' + DB_PORT_27017_TCP + '\n',
               function(err){
                console.log(err);
               });


};

test();