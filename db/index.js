var Db = require('mongodb').Db;
var MongoClient = require('mongodb').MongoClient;
var dbServer = require('mongodb').Server;

var address = process.env.MONGODB_PORT_27017_TCP_ADDR;
var port = process.env.MONGODB_PORT_27017_TCP_PORT;
// At this point we have not connected to mongo.
// mongoclient is an object that describes the connection to mongo
var db = new Db('economic_data', new dbServer(address, port), 
                                  {'native_parser':true,
                                    w:1});


// stil have no connection to mongodb
module.exports.db = db;
module.exports.address = address;
module.exports.port = port;
