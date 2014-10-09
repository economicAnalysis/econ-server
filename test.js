var fs = require('fs')

var makeDate = function(timestamp){
  return (timestamp.getMonth() + 1) + '/' +
    timestamp.getDay() + '/' + 
    timestamp.getFullYear() + ' ' +
    timestamp.getHours() + ':' +
    timestamp.getMinutes() + '\n';
}

// address and port are established in the db/index.js file

var test = function(address, port){


  var timestamp = new Date();
  var readableDate = makeDate(timestamp);

  fs.writeFile('test.txt', 
               'time: ' + readableDate + 
               'address variable: ' + address + '\n' +
               'port variable:' + port + '\n' +  
               'port: ' + process.env.MONGODB_PORT + '\n' +
               'port_27017: ' + process.env.MONGODB_PORT_27017_TCP + '\n',
               function(err){
                console.log(err);
               });
  console.log('test triggered');

};

module.exports.test = test;