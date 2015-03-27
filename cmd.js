'use strict';
var util = require('util');
var stream = require('stream');

var esformatter = require('esformatter');
esformatter.register(require('esformatter-jsx'));

var stdinStr = '';
var buffers = [];

function BufferStream(source) {
  if (!Buffer.isBuffer(source)) {
    throw (new Error('Source must be a buffer.'));
  }
  stream.Readable.call(this);
  this._source = source;
  this._offset = 0;
  this._length = source.length;
  this.on('end', this._destroy);
}
util.inherits(BufferStream, stream.Readable);
BufferStream.prototype._destroy = function() {
  this._source = null;
  this._offset = null;
  this._length = null;
};
BufferStream.prototype._read = function(size) {
  if (this._offset < this._length) {
    this.push(
      this._source.slice(this._offset, this._offset + size)
    );
    this._offset += size;
  }
  if (this._offset >= this._length) {
    this.push(null);
  }
};


process.stdin.on('data', function(trunk) {
  buffers.push(trunk);
});

var endhandle = function() {
  stdinStr = Buffer.concat(buffers).toString();
  var output = esformatter.format(stdinStr);
  // console.log(output);
  new BufferStream(new Buffer(output))
    .pipe(process.stdout)
    .on('end', function() {
      process.exit(0);
    });
};
process.stdin.on('end', endhandle);

process.stdin.on('error', function(err) {
  console.error('ERROR:', err.message);
  process.abort();
});