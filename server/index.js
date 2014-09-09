var fs = require('fs');
var express = require('express');

var server = express();

// Automatically load handlers in handlers directory
fs.readdirSync(__dirname + '/handlers/').forEach(function (file) {
 
  require('./handlers/' + file.substr(0, file.indexOf('.')))(server);

});

// Automatically load routes in routes directory
// In this case the restify body parser is attached to the server 
// and mapParams is set to false
fs.readdirSync(__dirname + '/routes/').forEach(function (file) {


  require('./routes/' + file.substr(0, file.indexOf('.')))(server);

});

module.exports.server = server;