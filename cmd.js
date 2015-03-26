'use strict';

var esformatter = require('esformatter');
esformatter.register(require('esformatter-jsx'));

var stdinStr = '';
var buffers = [];


process.stdin.on('data', function(trunk) {
  buffers.push(trunk);
});



process.stdin.on('end', function() {
  stdinStr = Buffer.concat(buffers).toString();
  var output = esformatter.format(stdinStr);
  process.stdout.write(output);
  process.exit(0);

});

process.stdin.on('error', function(err) {
  console.error('ERROR:', err.message);
  process.abort();
});