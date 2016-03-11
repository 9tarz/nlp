var MailParser = require("mailparser").MailParser;
var mailparser = new MailParser();
var fs = require('fs');

var email = fs.readFileSync('/dev/stdin').toString();

mailparser.on("end", function(mail_object){
  console.log(JSON.stringify(mail_object)); 
});

mailparser.write(email);
mailparser.end();
