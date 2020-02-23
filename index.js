var express = require('express');
var router = express.Router();
var app=express();
// var aiml = require('aiml')

// aiml.parseFile('sample.aiml', function(err, topics){
//   var engine = new aiml.AiEngine('Default', topics, {name: 'Jonny'});
//   var responce = engine.reply({name: 'Billy'}, "Hi, dude", function(err, responce){
//     console.log(responce);
//   });
// });

var home=require('./home.js')
app.use('/', home);


app.listen(3000);
