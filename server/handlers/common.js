var express = require('express');


var headers = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, PUT, DELETE, OPTIONS",
  "access-control-allow-headers": "content-type, accept",
  "access-control-max-age": 10, // Seconds.
  'Content-Type': "application/json"
};

var allowCrossDomain = function (request, response, next){
  response.header(headers);
  next();
}

module.exports = function (server) {
  // configure the server here
  // eg. bodyParser, etc
  server.use(allowCrossDomain);

};