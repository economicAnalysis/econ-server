// db is already db.economic_data
var db = require('../../db/index').db;

var getData = function (request, response) {

  var queryValue = request.params.month + '_' + request.params.year;
  
  // economic_data database
  var collection = db.collection('economic_series_by_date')
  collection.findOne({date: queryValue}, function (error, item){
    if(error){
      throw 'Database error'
    }
    response.status(200).send(item);
  });

};


module.exports = function (server) {

  //
  server.get('/:year/:month', getData);
  
  server.get('/', function (request, response){
    
    response.send('economics');

  })

  return server;

};