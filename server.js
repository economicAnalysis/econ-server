var server = require('./server/index').server;
var db = require('./db/index').db;
var dbObj = require('./db/index');
var express = require('express');


var port = 5000;


db.open(function (error, mongoclient){
  if(error){
    throw error;
  }
  console.log('now listening on ', port);
  server.listen(port);
})