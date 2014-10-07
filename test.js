var fs = require('fs')
var moment = require('moment');

var makeDate = function(timestamp){
  return (timestamp.getMonth() + 1) + '/' +
    timestamp.getDay() + '/' + 
    timestamp.getFullYear() + ' ' +
    timestamp.getHours() + ':' +
    timestamp.getMinutes();
}

var test = function(){

  var timestamp = new Date();
  var readableDate = makeDate(timestamp);

  fs.writeFile('test.txt', 
               'time: ' + readableDate + 
               'port: ' + process.env.DB_PORT + '\n' +
               ' port_27017: ' + process.env.DB_PORT_27017_TCP + '\n',
               function(err){
                console.log(err);
               });


};

module.exports.test = test;