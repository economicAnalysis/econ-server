var Db = require('mongodb').Db;
var MongoClient = require('mongodb').MongoClient;
var dbServer = require('mongodb').Server;


// At this point we have not connected to mongo.
// mongoclient is an object that describes the connection to mongo
var db = new Db('economic_data', new dbServer('localhost', 27017), 
                                  {'native_parser':true});


// stil have no connection to mongodb
module.exports.db = db;

