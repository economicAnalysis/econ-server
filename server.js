var server = require('./server/index').server;
var db = require('./db/index').db;
var express = require('express');

var mytest = require('./test');

var port = 5000;


db.open(function (error, mongoclient){
  if(error){
    throw 'Error opening database';
  }
  console.log('now listening on ', port);
  server.listen(port);
})