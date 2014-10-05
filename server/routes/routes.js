// db is already db.economic_data
var db = require('../../db/index').db;

var getData = function (request, response) {

  var collection = db.collection('economic_series_by_date');
  
  // If month and year are present use month and year
  if( request.params.month && request.params.year ){
    var queryValue = request.params.month + '_' + request.params.year;
 
    // economic_data database
    collection.findOne({month_year: queryValue}, function (error, item){
      if(error){
        throw 'Database error'
      }
      response.status(200).send(item);
    });
  } else {  // get the most recent document
    var stream = collection.find().sort({ _id: -1}).limit(1).stream();
    stream.on('data', function (item){
      response.status(200).send(item);
    });
  }

};

var getDates = function (request, response) {

  var collection = db.collection('observation_dates');
  
  // If month and year are present use month and year
  var stream = collection.find().sort({ _id: -1}).limit(1).stream();
  stream.on('data', function (item){
    response.status(200).send(item);
  });

};

module.exports = function (server) {

  server.get('/:year/:month', getData);

  server.get('/dates', getDates);
  
  server.get('/', getData);

  return server;

};