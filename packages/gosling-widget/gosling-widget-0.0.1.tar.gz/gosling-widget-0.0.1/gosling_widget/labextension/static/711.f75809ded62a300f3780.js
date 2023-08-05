(self["webpackChunkgosling_widget"] = self["webpackChunkgosling_widget"] || []).push([[711],{

/***/ 8926:
/***/ ((module) => {

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
  try {
    var info = gen[key](arg);
    var value = info.value;
  } catch (error) {
    reject(error);
    return;
  }

  if (info.done) {
    resolve(value);
  } else {
    Promise.resolve(value).then(_next, _throw);
  }
}

function _asyncToGenerator(fn) {
  return function () {
    var self = this,
        args = arguments;
    return new Promise(function (resolve, reject) {
      var gen = fn.apply(self, args);

      function _next(value) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
      }

      function _throw(err) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
      }

      _next(undefined);
    });
  };
}

module.exports = _asyncToGenerator, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 4575:
/***/ ((module) => {

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

module.exports = _classCallCheck, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 3913:
/***/ ((module) => {

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  Object.defineProperty(Constructor, "prototype", {
    writable: false
  });
  return Constructor;
}

module.exports = _createClass, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 9713:
/***/ ((module) => {

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}

module.exports = _defineProperty, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 5318:
/***/ ((module) => {

function _interopRequireDefault(obj) {
  return obj && obj.__esModule ? obj : {
    "default": obj
  };
}

module.exports = _interopRequireDefault, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 7757:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__(5666);


/***/ }),

/***/ 8191:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(5318);

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _regenerator = _interopRequireDefault(__webpack_require__(7757));

var _asyncToGenerator2 = _interopRequireDefault(__webpack_require__(8926));

var _classCallCheck2 = _interopRequireDefault(__webpack_require__(4575));

var _createClass2 = _interopRequireDefault(__webpack_require__(3913));

var _defineProperty2 = _interopRequireDefault(__webpack_require__(9713));

// Using this you can "await" the file like a normal promise
// https://blog.shovonhasan.com/using-promises-with-filereader/
function readBlobAsArrayBuffer(blob) {
  var fileReader = new FileReader();
  return new Promise(function (resolve, reject) {
    fileReader.onerror = function () {
      fileReader.abort();
      reject(new Error('problem reading blob'));
    };

    fileReader.onabort = function () {
      reject(new Error('blob reading was aborted'));
    };

    fileReader.onload = function () {
      if (fileReader.result && typeof fileReader.result !== 'string') {
        resolve(fileReader.result);
      } else {
        reject(new Error('unknown error reading blob'));
      }
    };

    fileReader.readAsArrayBuffer(blob);
  });
}

function readBlobAsText(blob) {
  var fileReader = new FileReader();
  return new Promise(function (resolve, reject) {
    fileReader.onerror = function () {
      fileReader.abort();
      reject(new Error('problem reading blob'));
    };

    fileReader.onabort = function () {
      reject(new Error('blob reading was aborted'));
    };

    fileReader.onload = function () {
      if (fileReader.result && typeof fileReader.result === 'string') {
        resolve(fileReader.result);
      } else {
        reject(new Error('unknown error reading blob'));
      }
    };

    fileReader.readAsText(blob);
  });
}
/**
 * Blob of binary data fetched from a local file (with FileReader).
 *
 * Adapted by Robert Buels and Garrett Stevens from the BlobFetchable object in
 * the Dalliance Genome Explorer, which is copyright Thomas Down 2006-2011.
 */


var BlobFile = /*#__PURE__*/function () {
  function BlobFile(blob) {
    (0, _classCallCheck2.default)(this, BlobFile);
    (0, _defineProperty2.default)(this, "blob", void 0);
    (0, _defineProperty2.default)(this, "size", void 0);
    this.blob = blob;
    this.size = blob.size;
  }

  (0, _createClass2.default)(BlobFile, [{
    key: "read",
    value: function () {
      var _read = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee(buffer) {
        var offset,
            length,
            position,
            start,
            end,
            result,
            resultBuffer,
            bytesCopied,
            _args = arguments;
        return _regenerator.default.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                offset = _args.length > 1 && _args[1] !== undefined ? _args[1] : 0;
                length = _args.length > 2 ? _args[2] : undefined;
                position = _args.length > 3 && _args[3] !== undefined ? _args[3] : 0;

                if (length) {
                  _context.next = 5;
                  break;
                }

                return _context.abrupt("return", {
                  bytesRead: 0,
                  buffer: buffer
                });

              case 5:
                start = position;
                end = start + length;
                _context.next = 9;
                return readBlobAsArrayBuffer(this.blob.slice(start, end));

              case 9:
                result = _context.sent;
                resultBuffer = Buffer.from(result);
                bytesCopied = resultBuffer.copy(buffer, offset);
                return _context.abrupt("return", {
                  bytesRead: bytesCopied,
                  buffer: resultBuffer
                });

              case 13:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, this);
      }));

      function read(_x) {
        return _read.apply(this, arguments);
      }

      return read;
    }()
  }, {
    key: "readFile",
    value: function () {
      var _readFile = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee2(options) {
        var encoding, result;
        return _regenerator.default.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                if (typeof options === 'string') {
                  encoding = options;
                } else {
                  encoding = options && options.encoding;
                }

                if (!(encoding === 'utf8')) {
                  _context2.next = 3;
                  break;
                }

                return _context2.abrupt("return", readBlobAsText(this.blob));

              case 3:
                if (!encoding) {
                  _context2.next = 5;
                  break;
                }

                throw new Error("unsupported encoding: ".concat(encoding));

              case 5:
                _context2.next = 7;
                return readBlobAsArrayBuffer(this.blob);

              case 7:
                result = _context2.sent;
                return _context2.abrupt("return", Buffer.from(result));

              case 9:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2, this);
      }));

      function readFile(_x2) {
        return _readFile.apply(this, arguments);
      }

      return readFile;
    }()
  }, {
    key: "stat",
    value: function () {
      var _stat = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee3() {
        return _regenerator.default.wrap(function _callee3$(_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                return _context3.abrupt("return", {
                  size: this.size
                });

              case 1:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3, this);
      }));

      function stat() {
        return _stat.apply(this, arguments);
      }

      return stat;
    }()
  }, {
    key: "close",
    value: function () {
      var _close = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee4() {
        return _regenerator.default.wrap(function _callee4$(_context4) {
          while (1) {
            switch (_context4.prev = _context4.next) {
              case 0:
                return _context4.abrupt("return");

              case 1:
              case "end":
                return _context4.stop();
            }
          }
        }, _callee4);
      }));

      function close() {
        return _close.apply(this, arguments);
      }

      return close;
    }()
  }]);
  return BlobFile;
}();

exports["default"] = BlobFile;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uL3NyYy9ibG9iRmlsZS50cyJdLCJuYW1lcyI6WyJyZWFkQmxvYkFzQXJyYXlCdWZmZXIiLCJibG9iIiwiZmlsZVJlYWRlciIsIkZpbGVSZWFkZXIiLCJQcm9taXNlIiwicmVzb2x2ZSIsInJlamVjdCIsIm9uZXJyb3IiLCJhYm9ydCIsIkVycm9yIiwib25hYm9ydCIsIm9ubG9hZCIsInJlc3VsdCIsInJlYWRBc0FycmF5QnVmZmVyIiwicmVhZEJsb2JBc1RleHQiLCJyZWFkQXNUZXh0IiwiQmxvYkZpbGUiLCJzaXplIiwiYnVmZmVyIiwib2Zmc2V0IiwibGVuZ3RoIiwicG9zaXRpb24iLCJieXRlc1JlYWQiLCJzdGFydCIsImVuZCIsInNsaWNlIiwicmVzdWx0QnVmZmVyIiwiQnVmZmVyIiwiZnJvbSIsImJ5dGVzQ29waWVkIiwiY29weSIsIm9wdGlvbnMiLCJlbmNvZGluZyJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUVBO0FBQ0E7QUFDQSxTQUFTQSxxQkFBVCxDQUErQkMsSUFBL0IsRUFBaUU7QUFDL0QsTUFBTUMsVUFBVSxHQUFHLElBQUlDLFVBQUosRUFBbkI7QUFFQSxTQUFPLElBQUlDLE9BQUosQ0FBWSxVQUFDQyxPQUFELEVBQVVDLE1BQVYsRUFBMkI7QUFDNUNKLElBQUFBLFVBQVUsQ0FBQ0ssT0FBWCxHQUFxQixZQUFZO0FBQy9CTCxNQUFBQSxVQUFVLENBQUNNLEtBQVg7QUFDQUYsTUFBQUEsTUFBTSxDQUFDLElBQUlHLEtBQUosQ0FBVSxzQkFBVixDQUFELENBQU47QUFDRCxLQUhEOztBQUtBUCxJQUFBQSxVQUFVLENBQUNRLE9BQVgsR0FBcUIsWUFBWTtBQUMvQkosTUFBQUEsTUFBTSxDQUFDLElBQUlHLEtBQUosQ0FBVSwwQkFBVixDQUFELENBQU47QUFDRCxLQUZEOztBQUlBUCxJQUFBQSxVQUFVLENBQUNTLE1BQVgsR0FBb0IsWUFBWTtBQUM5QixVQUFJVCxVQUFVLENBQUNVLE1BQVgsSUFBcUIsT0FBT1YsVUFB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LElBQUl2QixLQUFKLGlDQUFtQ3VCLFFBQW5DLEU7Ozs7dUJBRWFoQyxxQkFBcUIsQ0FBQyxLQUFLQyxJQUFOLEM7OztBQUFwQ1csZ0JBQUFBLE07a0RBQ0NlLE1BQU0sQ0FBQ0MsSUFBUCxDQUFZaEIsTUFBWixDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7a0RBSUE7QUFBRUssa0JBQUFBLElBQUksRUFBRSxLQUFLQTtBQUFiLGlCIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgR2VuZXJpY0ZpbGVoYW5kbGUsIEZpbGVoYW5kbGVPcHRpb25zLCBTdGF0cyB9IGZyb20gJy4vZmlsZWhhbmRsZSdcblxuLy8gVXNpbmcgdGhpcyB5b3UgY2FuIFwiYXdhaXRcIiB0aGUgZmlsZSBsaWtlIGEgbm9ybWFsIHByb21pc2Vcbi8vIGh0dHBzOi8vYmxvZy5zaG92b25oYXNhbi5jb20vdXNpbmctcHJvbWlzZXMtd2l0aC1maWxlcmVhZGVyL1xuZnVuY3Rpb24gcmVhZEJsb2JBc0FycmF5QnVmZmVyKGJsb2I6IEJsb2IpOiBQcm9taXNlPEFycmF5QnVmZmVyPiB7XG4gIGNvbnN0IGZpbGVSZWFkZXIgPSBuZXcgRmlsZVJlYWRlcigpXG5cbiAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpOiB2b2lkID0+IHtcbiAgICBmaWxlUmVhZGVyLm9uZXJyb3IgPSAoKTogdm9pZCA9PiB7XG4gICAgICBmaWxlUmVhZGVyLmFib3J0KClcbiAgICAgIHJlamVjdChuZXcgRXJyb3IoJ3Byb2JsZW0gcmVhZGluZyBibG9iJykpXG4gICAgfVxuXG4gICAgZmlsZVJlYWRlci5vbmFib3J0ID0gKCk6IHZvaWQgPT4ge1xuICAgICAgcmVqZWN0KG5ldyBFcnJvcignYmxvYiByZWFkaW5nIHdhcyBhYm9ydGVkJykpXG4gICAgfVxuXG4gICAgZmlsZVJlYWRlci5vbmxvYWQgPSAoKTogdm9pZCA9PiB7XG4gICAgICBpZiAoZmlsZVJlYWRlci5yZXN1bHQgJiYgdHlwZW9mIGZpbGVSZWFkZXIucmVzdWx0ICE9PSAnc3RyaW5nJykge1xuICAgICAgICByZXNvbHZlKGZpbGVSZWFkZXIucmVzdWx0KVxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmVqZWN0KG5ldyBFcnJvcigndW5rbm93biBlcnJvciByZWFkaW5nIGJsb2InKSlcbiAgICAgIH1cbiAgICB9XG4gICAgZmlsZVJlYWRlci5yZWFkQXNBcnJheUJ1ZmZlcihibG9iKVxuICB9KVxufVxuXG5mdW5jdGlvbiByZWFkQmxvYkFzVGV4dChibG9iOiBCbG9iKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgY29uc3QgZmlsZVJlYWRlciA9IG5ldyBGaWxlUmVhZGVyKClcblxuICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCk6IHZvaWQgPT4ge1xuICAgIGZpbGVSZWFkZXIub25lcnJvciA9ICgpOiB2b2lkID0+IHtcbiAgICAgIGZpbGVSZWFkZXIuYWJvcnQoKVxuICAgICAgcmVqZWN0KG5ldyBFcnJvcigncHJvYmxlbSByZWFkaW5nIGJsb2InKSlcbiAgICB9XG5cbiAgICBmaWxlUmVhZGVyLm9uYWJvcnQgPSAoKTogdm9pZCA9PiB7XG4gICAgICByZWplY3QobmV3IEVycm9yKCdibG9iIHJlYWRpbmcgd2FzIGFib3J0ZWQnKSlcbiAgICB9XG5cbiAgICBmaWxlUmVhZGVyLm9ubG9hZCA9ICgpOiB2b2lkID0+IHtcbiAgICAgIGlmIChmaWxlUmVhZGVyLnJlc3VsdCAmJiB0eXBlb2YgZmlsZVJlYWRlci5yZXN1bHQgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgIHJlc29sdmUoZmlsZVJlYWRlci5yZXN1bHQpXG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZWplY3QobmV3IEVycm9yKCd1bmtub3duIGVycm9yIHJlYWRpbmcgYmxvYicpKVxuICAgICAgfVxuICAgIH1cbiAgICBmaWxlUmVhZGVyLnJlYWRBc1RleHQoYmxvYilcbiAgfSlcbn1cblxuLyoqXG4gKiBCbG9iIG9mIGJpbmFyeSBkYXRhIGZldGNoZWQgZnJvbSBhIGxvY2FsIGZpbGUgKHdpdGggRmlsZVJlYWRlcikuXG4gKlxuICogQWRhcHRlZCBieSBSb2JlcnQgQnVlbHMgYW5kIEdhcnJldHQgU3RldmVucyBmcm9tIHRoZSBCbG9iRmV0Y2hhYmxlIG9iamVjdCBpblxuICogdGhlIERhbGxpYW5jZSBHZW5vbWUgRXhwbG9yZXIsIHdoaWNoIGlzIGNvcHlyaWdodCBUaG9tYXMgRG93biAyMDA2LTIwMTEuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIEJsb2JGaWxlIGltcGxlbWVudHMgR2VuZXJpY0ZpbGVoYW5kbGUge1xuICBwcml2YXRlIGJsb2I6IEJsb2JcbiAgcHJpdmF0ZSBzaXplOiBudW1iZXJcbiAgcHVibGljIGNvbnN0cnVjdG9yKGJsb2I6IEJsb2IpIHtcbiAgICB0aGlzLmJsb2IgPSBibG9iXG4gICAgdGhpcy5zaXplID0gYmxvYi5zaXplXG4gIH1cblxuICBwdWJsaWMgYXN5bmMgcmVhZChcbiAgICBidWZmZXI6IEJ1ZmZlcixcbiAgICBvZmZzZXQgPSAwLFxuICAgIGxlbmd0aDogbnVtYmVyLFxuICAgIHBvc2l0aW9uID0gMCxcbiAgKTogUHJvbWlzZTx7IGJ5dGVzUmVhZDogbnVtYmVyOyBidWZmZXI6IEJ1ZmZlciB9PiB7XG4gICAgLy8gc2hvcnQtY2lyY3VpdCBhIHJlYWQgb2YgMCBieXRlcyBoZXJlLCBiZWNhdXNlIGJyb3dzZXJzIGFjdHVhbGx5IHNvbWV0aW1lc1xuICAgIC8vIGNyYXNoIGlmIHlvdSB0cnkgdG8gcmVhZCAwIGJ5dGVzIGZyb20gYSBsb2NhbCBmaWxlIVxuICAgIGlmICghbGVuZ3RoKSB7XG4gICAgICByZXR1cm4geyBieXRlc1JlYWQ6IDAsIGJ1ZmZlciB9XG4gICAgfVxuXG4gICAgY29uc3Qgc3RhcnQgPSBwb3NpdGlvblxuICAgIGNvbnN0IGVuZCA9IHN0YXJ0ICsgbGVuZ3RoXG5cbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCByZWFkQmxvYkFzQXJyYXlCdWZmZXIodGhpcy5ibG9iLnNsaWNlKHN0YXJ0LCBlbmQpKVxuICAgIGNvbnN0IHJlc3VsdEJ1ZmZlciA9IEJ1ZmZlci5mcm9tKHJlc3VsdClcblxuICAgIGNvbnN0IGJ5dGVzQ29waWVkID0gcmVzdWx0QnVmZmVyLmNvcHkoYnVmZmVyLCBvZmZzZXQpXG5cbiAgICByZXR1cm4geyBieXRlc1JlYWQ6IGJ5dGVzQ29waWVkLCBidWZmZXI6IHJlc3VsdEJ1ZmZlciB9XG4gIH1cblxuICBwdWJsaWMgYXN5bmMgcmVhZEZpbGUob3B0aW9ucz86IEZpbGVoYW5kbGVPcHRpb25zIHwgc3RyaW5nKTogUHJvbWlzZTxCdWZmZXIgfCBzdHJpbmc+IHtcbiAgICBsZXQgZW5jb2RpbmdcbiAgICBpZiAodHlwZW9mIG9wdGlvbnMgPT09ICdzdHJpbmcnKSB7XG4gICAgICBlbmNvZGluZyA9IG9wdGlvbnNcbiAgICB9IGVsc2Uge1xuICAgICAgZW5jb2RpbmcgPSBvcHRpb25zICYmIG9wdGlvbnMuZW5jb2RpbmdcbiAgICB9XG4gICAgaWYgKGVuY29kaW5nID09PSAndXRmOCcpIHtcbiAgICAgIHJldHVybiByZWFkQmxvYkFzVGV4dCh0aGlzLmJsb2IpXG4gICAgfVxuICAgIGlmIChlbmNvZGluZykge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGB1bnN1cHBvcnRlZCBlbmNvZGluZzogJHtlbmNvZGluZ31gKVxuICAgIH1cbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCByZWFkQmxvYkFzQXJyYXlCdWZmZXIodGhpcy5ibG9iKVxuICAgIHJldHVybiBCdWZmZXIuZnJvbShyZXN1bHQpXG4gIH1cblxuICBwdWJsaWMgYXN5bmMgc3RhdCgpOiBQcm9taXNlPFN0YXRzPiB7XG4gICAgcmV0dXJuIHsgc2l6ZTogdGhpcy5zaXplIH1cbiAgfVxuXG4gIHB1YmxpYyBhc3luYyBjbG9zZSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm5cbiAgfVxufVxuIl19

/***/ }),

/***/ 3187:
/***/ (() => {

"use strict";

//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsInNvdXJjZXNDb250ZW50IjpbXX0=

/***/ }),

/***/ 2711:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(5318);

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
var _exportNames = {
  open: true,
  fromUrl: true,
  LocalFile: true,
  RemoteFile: true,
  BlobFile: true
};
exports.open = open;
exports.fromUrl = fromUrl;
Object.defineProperty(exports, "LocalFile", ({
  enumerable: true,
  get: function get() {
    return _localFile.default;
  }
}));
Object.defineProperty(exports, "RemoteFile", ({
  enumerable: true,
  get: function get() {
    return _remoteFile.default;
  }
}));
Object.defineProperty(exports, "BlobFile", ({
  enumerable: true,
  get: function get() {
    return _blobFile.default;
  }
}));

var _localFile = _interopRequireDefault(__webpack_require__(6173));

var _remoteFile = _interopRequireDefault(__webpack_require__(5594));

var _blobFile = _interopRequireDefault(__webpack_require__(8191));

var _filehandle = __webpack_require__(3187);

Object.keys(_filehandle).forEach(function (key) {
  if (key === "default" || key === "__esModule") return;
  if (Object.prototype.hasOwnProperty.call(_exportNames, key)) return;
  Object.defineProperty(exports, key, {
    enumerable: true,
    get: function get() {
      return _filehandle[key];
    }
  });
});

function fromUrl(source) {
  var opts = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
  return new _remoteFile.default(source, opts);
}

function open(maybeUrl, maybePath, maybeFilehandle) {
  var opts = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : {};

  if (maybeFilehandle !== undefined) {
    return maybeFilehandle;
  }

  if (maybeUrl !== undefined) {
    return fromUrl(maybeUrl, opts);
  }

  if (maybePath !== undefined) {
    return new _localFile.default(maybePath, opts);
  }

  throw new Error('no url, path, or filehandle provided, cannot open');
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6WyJmcm9tVXJsIiwic291cmNlIiwib3B0cyIsIlJlbW90ZUZpbGUiLCJvcGVuIiwibWF5YmVVcmwiLCJtYXliZVBhdGgiLCJtYXliZUZpbGVoYW5kbGUiLCJ1bmRlZmluZWQiLCJMb2NhbEZpbGUiLCJFcnJvciJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7QUFDQTs7QUFDQTs7QUFFQTs7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTs7QUFFQSxTQUFTQSxPQUFULENBQWlCQyxNQUFqQixFQUFrRjtBQUFBLE1BQWpEQyxJQUFpRCx1RUFBdkIsRUFBdUI7QUFDaEYsU0FBTyxJQUFJQyxtQkFBSixDQUFlRixNQUFmLEVBQXVCQyxJQUF2QixDQUFQO0FBQ0Q7O0FBQ0QsU0FBU0UsSUFBVCxDQUNFQyxRQURGLEVBRUVDLFNBRkYsRUFHRUMsZUFIRixFQUtxQjtBQUFBLE1BRG5CTCxJQUNtQix1RUFETyxFQUNQOztBQUNuQixNQUFJSyxlQUFlLEtBQUtDLFNBQXhCLEVBQW1DO0FBQ2pDLFdBQU9ELGVBQVA7QUFDRDs7QUFDRCxNQUFJRixRQUFRLEtBQUtHLFNBQWpCLEVBQTRCO0FBQzFCLFdBQU9SLE9BQU8sQ0FBQ0ssUUFBRCxFQUFXSCxJQUFYLENBQWQ7QUFDRDs7QUFDRCxNQUFJSSxTQUFTLEtBQUtFLFNBQWxCLEVBQTZCO0FBQzNCLFdBQU8sSUFBSUMsa0JBQUosQ0FBY0gsU0FBZCxFQUF5QkosSUFBekIsQ0FBUDtBQUNEOztBQUNELFFBQU0sSUFBSVEsS0FBSixDQUFVLG1EQUFWLENBQU47QUFDRCIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBMb2NhbEZpbGUgZnJvbSAnLi9sb2NhbEZpbGUnXG5pbXBvcnQgUmVtb3RlRmlsZSBmcm9tICcuL3JlbW90ZUZpbGUnXG5pbXBvcnQgQmxvYkZpbGUgZnJvbSAnLi9ibG9iRmlsZSdcbmltcG9ydCB7IEdlbmVyaWNGaWxlaGFuZGxlLCBGaWxlaGFuZGxlT3B0aW9ucyB9IGZyb20gJy4vZmlsZWhhbmRsZSdcbmV4cG9ydCAqIGZyb20gJy4vZmlsZWhhbmRsZSdcblxuZnVuY3Rpb24gZnJvbVVybChzb3VyY2U6IHN0cmluZywgb3B0czogRmlsZWhhbmRsZU9wdGlvbnMgPSB7fSk6IEdlbmVyaWNGaWxlaGFuZGxlIHtcbiAgcmV0dXJuIG5ldyBSZW1vdGVGaWxlKHNvdXJjZSwgb3B0cylcbn1cbmZ1bmN0aW9uIG9wZW4oXG4gIG1heWJlVXJsPzogc3RyaW5nLFxuICBtYXliZVBhdGg/OiBzdHJpbmcsXG4gIG1heWJlRmlsZWhhbmRsZT86IEdlbmVyaWNGaWxlaGFuZGxlLFxuICBvcHRzOiBGaWxlaGFuZGxlT3B0aW9ucyA9IHt9LFxuKTogR2VuZXJpY0ZpbGVoYW5kbGUge1xuICBpZiAobWF5YmVGaWxlaGFuZGxlICE9PSB1bmRlZmluZWQpIHtcbiAgICByZXR1cm4gbWF5YmVGaWxlaGFuZGxlXG4gIH1cbiAgaWYgKG1heWJlVXJsICE9PSB1bmRlZmluZWQpIHtcbiAgICByZXR1cm4gZnJvbVVybChtYXliZVVybCwgb3B0cylcbiAgfVxuICBpZiAobWF5YmVQYXRoICE9PSB1bmRlZmluZWQpIHtcbiAgICByZXR1cm4gbmV3IExvY2FsRmlsZShtYXliZVBhdGgsIG9wdHMpXG4gIH1cbiAgdGhyb3cgbmV3IEVycm9yKCdubyB1cmwsIHBhdGgsIG9yIGZpbGVoYW5kbGUgcHJvdmlkZWQsIGNhbm5vdCBvcGVuJylcbn1cblxuZXhwb3J0IHsgb3BlbiwgZnJvbVVybCwgUmVtb3RlRmlsZSwgTG9jYWxGaWxlLCBCbG9iRmlsZSB9XG4iXX0=

/***/ }),

/***/ 5594:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var _interopRequireDefault = __webpack_require__(5318);

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _regenerator = _interopRequireDefault(__webpack_require__(7757));

var _asyncToGenerator2 = _interopRequireDefault(__webpack_require__(8926));

var _classCallCheck2 = _interopRequireDefault(__webpack_require__(4575));

var _createClass2 = _interopRequireDefault(__webpack_require__(3913));

var _defineProperty2 = _interopRequireDefault(__webpack_require__(9713));

var _fileUriToPath = _interopRequireDefault(__webpack_require__(1631));

var _ = __webpack_require__(2711);

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2.default)(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var myGlobal = typeof window !== 'undefined' ? window : typeof self !== 'undefined' ? self : {
  fetch: undefined
};

var RemoteFile = /*#__PURE__*/function () {
  (0, _createClass2.default)(RemoteFile, [{
    key: "getBufferFromResponse",
    value: function () {
      var _getBufferFromResponse = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee(response) {
        var resp;
        return _regenerator.default.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                if (!(typeof response.buffer === 'function')) {
                  _context.next = 4;
                  break;
                }

                return _context.abrupt("return", response.buffer());

              case 4:
                if (!(typeof response.arrayBuffer === 'function')) {
                  _context.next = 11;
                  break;
                }

                _context.next = 7;
                return response.arrayBuffer();

              case 7:
                resp = _context.sent;
                return _context.abrupt("return", Buffer.from(resp));

              case 11:
                throw new TypeError('invalid HTTP response object, has no buffer method, and no arrayBuffer method');

              case 12:
              case "end":
                return _context.stop();
            }
          }
        }, _callee);
      }));

      function getBufferFromResponse(_x) {
        return _getBufferFromResponse.apply(this, arguments);
      }

      return getBufferFromResponse;
    }()
  }]);

  function RemoteFile(source) {
    var opts = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
    (0, _classCallCheck2.default)(this, RemoteFile);
    (0, _defineProperty2.default)(this, "url", void 0);
    (0, _defineProperty2.default)(this, "_stat", void 0);
    (0, _defineProperty2.default)(this, "fetchImplementation", void 0);
    (0, _defineProperty2.default)(this, "baseOverrides", {});
    this.url = source; // if it is a file URL, monkey-patch ourselves to act like a LocalFile

    if (source.startsWith('file://')) {
      var path = (0, _fileUriToPath.default)(source);

      if (!path) {
        throw new TypeError('invalid file url');
      }

      var localFile = new _.LocalFile(path);
      this.read = localFile.read.bind(localFile);
      this.readFile = localFile.readFile.bind(localFile);
      this.stat = localFile.stat.bind(localFile); // eslint-disable-next-line @typescript-eslint/ban-ts-ignore
      // @ts-ignore

      this.fetchImplementation = function () {
        /* intentionally blank */
      };

      return;
    }

    var fetch = opts.fetch || myGlobal.fetch && myGlobal.fetch.bind(myGlobal);

    if (!fetch) {
      throw new TypeError("no fetch function supplied, and none found in global environment");
    }

    if (opts.overrides) {
      this.baseOverrides = opts.overrides;
    }

    this.fetchImplementation = fetch;
  }

  (0, _createClass2.default)(RemoteFile, [{
    key: "fetch",
    value: function () {
      var _fetch = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee2(input, init) {
        var response;
        return _regenerator.default.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                _context2.prev = 0;
                _context2.next = 3;
                return this.fetchImplementation(input, init);

              case 3:
                response = _context2.sent;
                _context2.next = 16;
                break;

              case 6:
                _context2.prev = 6;
                _context2.t0 = _context2["catch"](0);

                if (!(_context2.t0.message === 'Failed to fetch')) {
                  _context2.next = 15;
                  break;
                }

                // refetch to to help work around a chrome bug (discussed in generic-filehandle issue #72) in
                // which the chrome cache returns a CORS error for content in its cache.
                // see also https://github.com/GMOD/jbrowse-components/pull/1511
                console.warn("generic-filehandle: refetching ".concat(input, " to attempt to work around chrome CORS header caching bug"));
                _context2.next = 12;
                return this.fetchImplementation(input, _objectSpread(_objectSpread({}, init), {}, {
                  cache: 'reload'
                }));

              case 12:
                response = _context2.sent;
                _context2.next = 16;
                break;

              case 15:
                throw _context2.t0;

              case 16:
                return _context2.abrupt("return", response);

              case 17:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2, this, [[0, 6]]);
      }));

      function fetch(_x2, _x3) {
        return _fetch.apply(this, arguments);
      }

      return fetch;
    }()
  }, {
    key: "read",
    value: function () {
      var _read = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee3(buffer) {
        var offset,
            length,
            position,
            opts,
            _opts$headers,
            headers,
            signal,
            _opts$overrides,
            overrides,
            args,
            response,
            responseData,
            bytesCopied,
            res,
            sizeMatch,
            _args3 = arguments;

        return _regenerator.default.wrap(function _callee3$(_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                offset = _args3.length > 1 && _args3[1] !== undefined ? _args3[1] : 0;
                length = _args3.length > 2 ? _args3[2] : undefined;
                position = _args3.length > 3 && _args3[3] !== undefined ? _args3[3] : 0;
                opts = _args3.length > 4 && _args3[4] !== undefined ? _args3[4] : {};
                _opts$headers = opts.headers, headers = _opts$headers === void 0 ? {} : _opts$headers, signal = opts.signal, _opts$overrides = opts.overrides, overrides = _opts$overrides === void 0 ? {} : _opts$overrides;

                if (length < Infinity) {
                  headers.range = "bytes=".concat(position, "-").concat(position + length);
                } else if (length === Infinity && position !== 0) {
                  headers.range = "bytes=".concat(position, "-");
                }

                args = _objectSpread(_objectSpread(_objectSpread({}, this.baseOverrides), overrides), {}, {
                  headers: _objectSpread(_objectSpread(_objectSpread({}, headers), overrides.headers), this.baseOverrides.headers),
                  method: 'GET',
                  redirect: 'follow',
                  mode: 'cors',
                  signal: signal
                });
                _context3.next = 9;
                return this.fetch(this.url, args);

              case 9:
                response = _context3.sent;

                if (response.ok) {
                  _context3.next = 12;
                  break;
                }

                throw new Error("HTTP ".concat(response.status, " ").concat(response.statusText));

              case 12:
                if (!(response.status === 200 && position === 0 || response.status === 206)) {
                  _context3.next = 21;
                  break;
                }

                _context3.next = 15;
                return this.getBufferFromResponse(response);

              case 15:
                responseData = _context3.sent;
                bytesCopied = responseData.copy(buffer, offset, 0, Math.min(length, responseData.length)); // try to parse out the size of the remote file

                res = response.headers.get('content-range');
                sizeMatch = /\/(\d+)$/.exec(res || '');

                if (sizeMatch && sizeMatch[1]) {
                  this._stat = {
                    size: parseInt(sizeMatch[1], 10)
                  };
                }

                return _context3.abrupt("return", {
                  bytesRead: bytesCopied,
                  buffer: buffer
                });

              case 21:
                if (!(response.status === 200)) {
                  _context3.next = 23;
                  break;
                }

                throw new Error('${this.url} fetch returned status 200, expected 206');

              case 23:
                throw new Error("HTTP ".concat(response.status, " fetching ").concat(this.url));

              case 24:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3, this);
      }));

      function read(_x4) {
        return _read.apply(this, arguments);
      }

      return read;
    }()
  }, {
    key: "readFile",
    value: function () {
      var _readFile = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee4() {
        var options,
            encoding,
            opts,
            _opts,
            _opts$headers2,
            headers,
            signal,
            _opts$overrides2,
            overrides,
            args,
            response,
            _args4 = arguments;

        return _regenerator.default.wrap(function _callee4$(_context4) {
          while (1) {
            switch (_context4.prev = _context4.next) {
              case 0:
                options = _args4.length > 0 && _args4[0] !== undefined ? _args4[0] : {};

                if (typeof options === 'string') {
                  encoding = options;
                  opts = {};
                } else {
                  encoding = options.encoding;
                  opts = options;
                  delete opts.encoding;
                }

                _opts = opts, _opts$headers2 = _opts.headers, headers = _opts$headers2 === void 0 ? {} : _opts$headers2, signal = _opts.signal, _opts$overrides2 = _opts.overrides, overrides = _opts$overrides2 === void 0 ? {} : _opts$overrides2;
                args = _objectSpread(_objectSpread({
                  headers: headers,
                  method: 'GET',
                  redirect: 'follow',
                  mode: 'cors',
                  signal: signal
                }, this.baseOverrides), overrides);
                _context4.next = 6;
                return this.fetch(this.url, args);

              case 6:
                response = _context4.sent;

                if (response) {
                  _context4.next = 9;
                  break;
                }

                throw new Error('generic-filehandle failed to fetch');

              case 9:
                if (!(response.status !== 200)) {
                  _context4.next = 11;
                  break;
                }

                throw Object.assign(new Error("HTTP ".concat(response.status, " fetching ").concat(this.url)), {
                  status: response.status
                });

              case 11:
                if (!(encoding === 'utf8')) {
                  _context4.next = 13;
                  break;
                }

                return _context4.abrupt("return", response.text());

              case 13:
                if (!encoding) {
                  _context4.next = 15;
                  break;
                }

                throw new Error("unsupported encoding: ".concat(encoding));

              case 15:
                return _context4.abrupt("return", this.getBufferFromResponse(response));

              case 16:
              case "end":
                return _context4.stop();
            }
          }
        }, _callee4, this);
      }));

      function readFile() {
        return _readFile.apply(this, arguments);
      }

      return readFile;
    }()
  }, {
    key: "stat",
    value: function () {
      var _stat = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee5() {
        var buf;
        return _regenerator.default.wrap(function _callee5$(_context5) {
          while (1) {
            switch (_context5.prev = _context5.next) {
              case 0:
                if (this._stat) {
                  _context5.next = 6;
                  break;
                }

                buf = Buffer.allocUnsafe(10);
                _context5.next = 4;
                return this.read(buf, 0, 10, 0);

              case 4:
                if (this._stat) {
                  _context5.next = 6;
                  break;
                }

                throw new Error("unable to determine size of file at ".concat(this.url));

              case 6:
                return _context5.abrupt("return", this._stat);

              case 7:
              case "end":
                return _context5.stop();
            }
          }
        }, _callee5, this);
      }));

      function stat() {
        return _stat.apply(this, arguments);
      }

      return stat;
    }()
  }, {
    key: "close",
    value: function () {
      var _close = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee6() {
        return _regenerator.default.wrap(function _callee6$(_context6) {
          while (1) {
            switch (_context6.prev = _context6.next) {
              case 0:
                return _context6.abrupt("return");

              case 1:
              case "end":
                return _context6.stop();
            }
          }
        }, _callee6);
      }));

      function close() {
        return _close.apply(this, arguments);
      }

      return close;
    }()
  }]);
  return RemoteFile;
}();

exports["default"] = RemoteFile;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uL3NyYy9yZW1vdGVGaWxlLnRzIl0sIm5hbWVzIjpbIm15R2xvYmFsIiwid2luZG93Iiwic2VsZiIsImZldGNoIiwidW5kZWZpbmVkIiwiUmVtb3RlRmlsZSIsInJlc3BvbnNlIiwiYnVmZmVyIiwiYXJyYXlCdWZmZXIiLCJyZXNwIiwiQnVmZmVyIiwiZnJvbSIsIlR5cGVFcnJvciIsInNvdXJjZSIsIm9wdHMiLCJ1cmwiLCJzdGFydHNXaXRoIiwicGF0aCIsImxvY2FsRmlsZSIsIkxvY2FsRmlsZSIsInJlYWQiLCJiaW5kIiwicmVhZEZpbGUiLCJzdGF0IiwiZmV0Y2hJbXBsZW1lbnRhdGlvbiIsIm92ZXJyaWRlcyIsImJhc2VPdmVycmlkZXMiLCJpbnB1dCIsImluaXQiLCJtZXNzYWdlIiwiY29uc29sZSIsIndhcm4iLCJjYWNoZSIsIm9mZnNldCIsImxlbmd0aCIsInBvc2l0aW9uIiwiaGVhZGVycyIsInNpZ25hbCIsIkluZmluaXR5IiwicmFuZ2UiLCJhcmdzIiwibWV0aG9kIiwicmVkaXJlY3QiLCJtb2RlIiwib2siLCJFcnJvciIsInN0YXR1cyIsInN0YXR1c1RleHQiLCJnZXRCdWZmZXJGcm9tUmVzcG9uc2UiLCJyZXNwb25zZURhdGEiLCJieXRlc0NvcGllZCIsImNvcHkiLCJNYXRoIiwibWluIiwicmVzIiwiZ2V0Iiwic2l6ZU1hdGNoIiwiZXhlYyIsIl9zdGF0Iiwic2l6ZSIsInBhcnNlSW50IiwiYnl0ZXNSZWFkIiwib3B0aW9ucyIsImVuY29kaW5nIiwiT2JqZWN0IiwiYXNzaWduIiwidGV4dCIsImJ1ZiIsImFsbG9jVW5zYWZlIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7O0FBUUE7Ozs7OztBQUVBLElBQU1BLFFBQVEsR0FDWixPQUFPQyxNQUFQLEtBQWtCLFdBQWxCLEdBQ0lBLE1BREosR0FFSSxPQUFPQyxJQUFQLEtBQWdCLFdBQWhCLEdBQ0FBLElBREEsR0FFQTtBQUFFQyxFQUFBQSxLQUFLLEVBQUVDO0FB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Q1ZDLGtCQUFBQSxJQUFJLEVBQUUsTTtBQUNOTixrQkFBQUEsTUFBTSxFQUFOQTttQkFDRyxLQUFLWCxhLEdBQ0xELFM7O3VCQUVrQixLQUFLdEIsS0FBTCxDQUFXLEtBQUtZLEdBQWhCLEVBQXFCeUIsSUFBckIsQzs7O0FBQWpCbEMsZ0JBQUFBLFE7O29CQUVEQSxROzs7OztzQkFDRyxJQUFJdUMsS0FBSixDQUFVLG9DQUFWLEM7OztzQkFHSnZDLFFBQVEsQ0FBQ3dDLE1BQVQsS0FBb0IsRzs7Ozs7c0JBQ2hCa0IsTUFBTSxDQUFDQyxNQUFQLENBQWMsSUFBSXBCLEtBQUosZ0JBQWtCdkMsUUFBUSxDQUFDd0MsTUFBM0IsdUJBQThDLEtBQUsvQixHQUFuRCxFQUFkLEVBQXlFO0FBQzdFK0Isa0JBQUFBLE1BQU0sRUFBRXhDLFFBQVEsQ0FBQ3dDO0FBRDRELGlCQUF6RSxDOzs7c0JBSUppQixRQUFRLEtBQUssTTs7Ozs7a0RBQ1J6RCxRQUFRLENBQUM0RCxJQUFULEU7OztxQkFFTEgsUTs7Ozs7c0JBQ0ksSUFBSWxCLEtBQUosaUNBQW1Da0IsUUFBbkMsRTs7O2tEQUVELEtBQUtmLHFCQUFMLENBQTJCMUMsUUFBM0IsQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztvQkFJRixLQUFLb0QsSzs7Ozs7QUFDRlMsZ0JBQUFBLEcsR0FBTXpELE1BQU0sQ0FBQzBELFdBQVAsQ0FBbUIsRUFBbkIsQzs7dUJBQ04sS0FBS2hELElBQUwsQ0FBVStDLEdBQVYsRUFBZSxDQUFmLEVBQWtCLEVBQWxCLEVBQXNCLENBQXRCLEM7OztvQkFDRCxLQUFLVCxLOzs7OztzQkFDRixJQUFJYixLQUFKLCtDQUFpRCxLQUFLOUIsR0FBdEQsRTs7O2tEQUdILEtBQUsyQyxLIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHVyaTJwYXRoIGZyb20gJ2ZpbGUtdXJpLXRvLXBhdGgnXG5pbXBvcnQge1xuICBHZW5lcmljRmlsZWhhbmRsZSxcbiAgRmlsZWhhbmRsZU9wdGlvbnMsXG4gIFN0YXRzLFxuICBGZXRjaGVyLFxuICBQb2x5ZmlsbGVkUmVzcG9uc2UsXG59IGZyb20gJy4vZmlsZWhhbmRsZSdcbmltcG9ydCB7IExvY2FsRmlsZSB9IGZyb20gJy4nXG5cbmNvbnN0IG15R2xvYmFsID1cbiAgdHlwZW9mIHdpbmRvdyAhPT0gJ3VuZGVmaW5lZCdcbiAgICA/IHdpbmRvd1xuICAgIDogdHlwZW9mIHNlbGYgIT09ICd1bmRlZmluZWQnXG4gICAgPyBzZWxmXG4gICAgOiB7IGZldGNoOiB1bmRlZmluZWQgfVxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBSZW1vdGVGaWxlIGltcGxlbWVudHMgR2VuZXJpY0ZpbGVoYW5kbGUge1xuICBwcm90ZWN0ZWQgdXJsOiBzdHJpbmdcbiAgcHJpdmF0ZSBfc3RhdD86IFN0YXRzXG4gIHByaXZhdGUgZmV0Y2hJbXBsZW1lbnRhdGlvbjogRmV0Y2hlclxuICBwcml2YXRlIGJhc2VPdmVycmlkZXM6IGFueSA9IHt9XG5cbiAgcHJpdmF0ZSBhc3luYyBnZXRCdWZmZXJGcm9tUmVzcG9uc2UocmVzcG9uc2U6IFBvbHlmaWxsZWRSZXNwb25zZSk6IFByb21pc2U8QnVmZmVyPiB7XG4gICAgaWYgKHR5cGVvZiByZXNwb25zZS5idWZmZXIgPT09ICdmdW5jdGlvbicpIHtcbiAgICAgIHJldHVybiByZXNwb25zZS5idWZmZXIoKVxuICAgIH0gZWxzZSBpZiAodHlwZW9mIHJlc3BvbnNlLmFycmF5QnVmZmVyID09PSAnZnVuY3Rpb24nKSB7XG4gICAgICBjb25zdCByZXNwID0gYXdhaXQgcmVzcG9uc2UuYXJyYXlCdWZmZXIoKVxuICAgICAgcmV0dXJuIEJ1ZmZlci5mcm9tKHJlc3ApXG4gICAgfSBlbHNlIHtcbiAgICAgIHRocm93IG5ldyBUeXBlRXJyb3IoXG4gICAgICAgICdpbnZhbGlkIEhUVFAgcmVzcG9uc2Ugb2JqZWN0LCBoYXMgbm8gYnVmZmVyIG1ldGhvZCwgYW5kIG5vIGFycmF5QnVmZmVyIG1ldGhvZCcsXG4gICAgICApXG4gICAgfVxuICB9XG5cbiAgcHVibGljIGNvbnN0cnVjdG9yKHNvdXJjZTogc3RyaW5nLCBvcHRzOiBGaWxlaGFuZGxlT3B0aW9ucyA9IHt9KSB7XG4gICAgdGhpcy51cmwgPSBzb3VyY2VcblxuICAgIC8vIGlmIGl0IGlzIGEgZmlsZSBVUkwsIG1vbmtleS1wYXRjaCBvdXJzZWx2ZXMgdG8gYWN0IGxpa2UgYSBMb2NhbEZpbGVcbiAgICBpZiAoc291cmNlLnN0YXJ0c1dpdGgoJ2ZpbGU6Ly8nKSkge1xuICAgICAgY29uc3QgcGF0aCA9IHVyaTJwYXRoKHNvdXJjZSlcbiAgICAgIGlmICghcGF0aCkge1xuICAgICAgICB0aHJvdyBuZXcgVHlwZUVycm9yKCdpbnZhbGlkIGZpbGUgdXJsJylcbiAgICAgIH1cbiAgICAgIGNvbnN0IGxvY2FsRmlsZSA9IG5ldyBMb2NhbEZpbGUocGF0aClcbiAgICAgIHRoaXMucmVhZCA9IGxvY2FsRmlsZS5yZWFkLmJpbmQobG9jYWxGaWxlKVxuICAgICAgdGhpcy5yZWFkRmlsZSA9IGxvY2FsRmlsZS5yZWFkRmlsZS5iaW5kKGxvY2FsRmlsZSlcbiAgICAgIHRoaXMuc3RhdCA9IGxvY2FsRmlsZS5zdGF0LmJpbmQobG9jYWxGaWxlKVxuICAgICAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIEB0eXBlc2NyaXB0LWVzbGludC9iYW4tdHMtaWdub3JlXG4gICAgICAvLyBAdHMtaWdub3JlXG4gICAgICB0aGlzLmZldGNoSW1wbGVtZW50YXRpb24gPSAoKTogdm9pZCA9PiB7XG4gICAgICAgIC8qIGludGVudGlvbmFsbHkgYmxhbmsgKi9cbiAgICAgIH1cbiAgICAgIHJldHVyblxuICAgIH1cblxuICAgIGNvbnN0IGZldGNoID0gb3B0cy5mZXRjaCB8fCAobXlHbG9iYWwuZmV0Y2ggJiYgbXlHbG9iYWwuZmV0Y2guYmluZChteUdsb2JhbCkpXG4gICAgaWYgKCFmZXRjaCkge1xuICAgICAgdGhyb3cgbmV3IFR5cGVFcnJvcihcbiAgICAgICAgYG5vIGZldGNoIGZ1bmN0aW9uIHN1cHBsaWVkLCBhbmQgbm9uZSBmb3VuZCBpbiBnbG9iYWwgZW52aXJvbm1lbnRgLFxuICAgICAgKVxuICAgIH1cbiAgICBpZiAob3B0cy5vdmVycmlkZXMpIHtcbiAgICAgIHRoaXMuYmFzZU92ZXJyaWRlcyA9IG9wdHMub3ZlcnJpZGVzXG4gICAgfVxuICAgIHRoaXMuZmV0Y2hJbXBsZW1lbnRhdGlvbiA9IGZldGNoXG4gIH1cblxuICBwdWJsaWMgYXN5bmMgZmV0Y2goXG4gICAgaW5wdXQ6IFJlcXVlc3RJbmZvLFxuICAgIGluaXQ6IFJlcXVlc3RJbml0IHwgdW5kZWZpbmVkLFxuICApOiBQcm9taXNlPFBvbHlmaWxsZWRSZXNwb25zZT4ge1xuICAgIGxldCByZXNwb25zZVxuICAgIHRyeSB7XG4gICAgICByZXNwb25zZSA9IGF3YWl0IHRoaXMuZmV0Y2hJbXBsZW1lbnRhdGlvbihpbnB1dCwgaW5pdClcbiAgICB9IGNhdGNoIChlKSB7XG4gICAgICBpZiAoZS5tZXNzYWdlID09PSAnRmFpbGVkIHRvIGZldGNoJykge1xuICAgICAgICAvLyByZWZldGNoIHRvIHRvIGhlbHAgd29yayBhcm91bmQgYSBjaHJvbWUgYnVnIChkaXNjdXNzZWQgaW4gZ2VuZXJpYy1maWxlaGFuZGxlIGlzc3VlICM3MikgaW5cbiAgICAgICAgLy8gd2hpY2ggdGhlIGNocm9tZSBjYWNoZSByZXR1cm5zIGEgQ09SUyBlcnJvciBmb3IgY29udGVudCBpbiBpdHMgY2FjaGUuXG4gICAgICAgIC8vIHNlZSBhbHNvIGh0dHBzOi8vZ2l0aHViLmNvbS9HTU9EL2picm93c2UtY29tcG9uZW50cy9wdWxsLzE1MTFcbiAgICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAgIGBnZW5lcmljLWZpbGVoYW5kbGU6IHJlZmV0Y2hpbmcgJHtpbnB1dH0gdG8gYXR0ZW1wdCB0byB3b3JrIGFyb3VuZCBjaHJvbWUgQ09SUyBoZWFkZXIgY2FjaGluZyBidWdgLFxuICAgICAgICApXG4gICAgICAgIHJlc3BvbnNlID0gYXdhaXQgdGhpcy5mZXRjaEltcGxlbWVudGF0aW9uKGlucHV0LCB7IC4uLmluaXQsIGNhY2hlOiAncmVsb2FkJyB9KVxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgdGhyb3cgZVxuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gcmVzcG9uc2VcbiAgfVxuXG4gIHB1YmxpYyBhc3luYyByZWFkKFxuICAgIGJ1ZmZlcjogQnVmZmVyLFxuICAgIG9mZnNldCA9IDAsXG4gICAgbGVuZ3RoOiBudW1iZXIsXG4gICAgcG9zaXRpb24gPSAwLFxuICAgIG9wdHM6IEZpbGVoYW5kbGVPcHRpb25zID0ge30sXG4gICk6IFByb21pc2U8eyBieXRlc1JlYWQ6IG51bWJlcjsgYnVmZmVyOiBCdWZmZXIgfT4ge1xuICAgIGNvbnN0IHsgaGVhZGVycyA9IHt9LCBzaWduYWwsIG92ZXJyaWRlcyA9IHt9IH0gPSBvcHRzXG4gICAgaWYgKGxlbmd0aCA8IEluZmluaXR5KSB7XG4gICAgICBoZWFkZXJzLnJhbmdlID0gYGJ5dGVzPSR7cG9zaXRpb259LSR7cG9zaXRpb24gKyBsZW5ndGh9YFxuICAgIH0gZWxzZSBpZiAobGVuZ3RoID09PSBJbmZpbml0eSAmJiBwb3NpdGlvbiAhPT0gMCkge1xuICAgICAgaGVhZGVycy5yYW5nZSA9IGBieXRlcz0ke3Bvc2l0aW9ufS1gXG4gICAgfVxuICAgIGNvbnN0IGFyZ3MgPSB7XG4gICAgICAuLi50aGlzLmJhc2VPdmVycmlkZXMsXG4gICAgICAuLi5vdmVycmlkZXMsXG4gICAgICBoZWFkZXJzOiB7IC4uLmhlYWRlcnMsIC4uLm92ZXJyaWRlcy5oZWFkZXJzLCAuLi50aGlzLmJhc2VPdmVycmlkZXMuaGVhZGVycyB9LFxuICAgICAgbWV0aG9kOiAnR0VUJyxcbiAgICAgIHJlZGlyZWN0OiAnZm9sbG93JyxcbiAgICAgIG1vZGU6ICdjb3JzJyxcbiAgICAgIHNpZ25hbCxcbiAgICB9XG4gICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCB0aGlzLmZldGNoKHRoaXMudXJsLCBhcmdzKVxuXG4gICAgaWYgKCFyZXNwb25zZS5vaykge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGBIVFRQICR7cmVzcG9uc2Uuc3RhdHVzfSAke3Jlc3BvbnNlLnN0YXR1c1RleHR9YClcbiAgICB9XG5cbiAgICBpZiAoKHJlc3BvbnNlLnN0YXR1cyA9PT0gMjAwICYmIHBvc2l0aW9uID09PSAwKSB8fCByZXNwb25zZS5zdGF0dXMgPT09IDIwNikge1xuICAgICAgY29uc3QgcmVzcG9uc2VEYXRhID0gYXdhaXQgdGhpcy5nZXRCdWZmZXJGcm9tUmVzcG9uc2UocmVzcG9uc2UpXG4gICAgICBjb25zdCBieXRlc0NvcGllZCA9IHJlc3BvbnNlRGF0YS5jb3B5KFxuICAgICAgICBidWZmZXIsXG4gICAgICAgIG9mZnNldCxcbiAgICAgICAgMCxcbiAgICAgICAgTWF0aC5taW4obGVuZ3RoLCByZXNwb25zZURhdGEubGVuZ3RoKSxcbiAgICAgIClcblxuICAgICAgLy8gdHJ5IHRvIHBhcnNlIG91dCB0aGUgc2l6ZSBvZiB0aGUgcmVtb3RlIGZpbGVcbiAgICAgIGNvbnN0IHJlcyA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCdjb250ZW50LXJhbmdlJylcbiAgICAgIGNvbnN0IHNpemVNYXRjaCA9IC9cXC8oXFxkKykkLy5leGVjKHJlcyB8fCAnJylcbiAgICAgIGlmIChzaXplTWF0Y2ggJiYgc2l6ZU1hdGNoWzFdKSB7XG4gICAgICAgIHRoaXMuX3N0YXQgPSB7IHNpemU6IHBhcnNlSW50KHNpemVNYXRjaFsxXSwgMTApIH1cbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHsgYnl0ZXNSZWFkOiBieXRlc0NvcGllZCwgYnVmZmVyIH1cbiAgICB9XG5cbiAgICBpZiAocmVzcG9uc2Uuc3RhdHVzID09PSAyMDApIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignJHt0aGlzLnVybH0gZmV0Y2ggcmV0dXJuZWQgc3RhdHVzIDIwMCwgZXhwZWN0ZWQgMjA2JylcbiAgICB9XG5cbiAgICAvLyBUT0RPOiB0cnkgaGFyZGVyIGhlcmUgdG8gZ2F0aGVyIG1vcmUgaW5mb3JtYXRpb24gYWJvdXQgd2hhdCB0aGUgcHJvYmxlbSBpc1xuICAgIHRocm93IG5ldyBFcnJvcihgSFRUUCAke3Jlc3BvbnNlLnN0YXR1c30gZmV0Y2hpbmcgJHt0aGlzLnVybH1gKVxuICB9XG5cbiAgcHVibGljIGFzeW5jIHJlYWRGaWxlKFxuICAgIG9wdGlvbnM6IEZpbGVoYW5kbGVPcHRpb25zIHwgc3RyaW5nID0ge30sXG4gICk6IFByb21pc2U8QnVmZmVyIHwgc3RyaW5nPiB7XG4gICAgbGV0IGVuY29kaW5nXG4gICAgbGV0IG9wdHNcbiAgICBpZiAodHlwZW9mIG9wdGlvbnMgPT09ICdzdHJpbmcnKSB7XG4gICAgICBlbmNvZGluZyA9IG9wdGlvbnNcbiAgICAgIG9wdHMgPSB7fVxuICAgIH0gZWxzZSB7XG4gICAgICBlbmNvZGluZyA9IG9wdGlvbnMuZW5jb2RpbmdcbiAgICAgIG9wdHMgPSBvcHRpb25zXG4gICAgICBkZWxldGUgb3B0cy5lbmNvZGluZ1xuICAgIH1cbiAgICBjb25zdCB7IGhlYWRlcnMgPSB7fSwgc2lnbmFsLCBvdmVycmlkZXMgPSB7fSB9ID0gb3B0c1xuICAgIGNvbnN0IGFyZ3MgPSB7XG4gICAgICBoZWFkZXJzLFxuICAgICAgbWV0aG9kOiAnR0VUJyxcbiAgICAgIHJlZGlyZWN0OiAnZm9sbG93JyxcbiAgICAgIG1vZGU6ICdjb3JzJyxcbiAgICAgIHNpZ25hbCxcbiAgICAgIC4uLnRoaXMuYmFzZU92ZXJyaWRlcyxcbiAgICAgIC4uLm92ZXJyaWRlcyxcbiAgICB9XG4gICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCB0aGlzLmZldGNoKHRoaXMudXJsLCBhcmdzKVxuXG4gICAgaWYgKCFyZXNwb25zZSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdnZW5lcmljLWZpbGVoYW5kbGUgZmFpbGVkIHRvIGZldGNoJylcbiAgICB9XG5cbiAgICBpZiAocmVzcG9uc2Uuc3RhdHVzICE9PSAyMDApIHtcbiAgICAgIHRocm93IE9iamVjdC5hc3NpZ24obmV3IEVycm9yKGBIVFRQICR7cmVzcG9uc2Uuc3RhdHVzfSBmZXRjaGluZyAke3RoaXMudXJsfWApLCB7XG4gICAgICAgIHN0YXR1czogcmVzcG9uc2Uuc3RhdHVzLFxuICAgICAgfSlcbiAgICB9XG4gICAgaWYgKGVuY29kaW5nID09PSAndXRmOCcpIHtcbiAgICAgIHJldHVybiByZXNwb25zZS50ZXh0KClcbiAgICB9XG4gICAgaWYgKGVuY29kaW5nKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYHVuc3VwcG9ydGVkIGVuY29kaW5nOiAke2VuY29kaW5nfWApXG4gICAgfVxuICAgIHJldHVybiB0aGlzLmdldEJ1ZmZlckZyb21SZXNwb25zZShyZXNwb25zZSlcbiAgfVxuXG4gIHB1YmxpYyBhc3luYyBzdGF0KCk6IFByb21pc2U8U3RhdHM+IHtcbiAgICBpZiAoIXRoaXMuX3N0YXQpIHtcbiAgICAgIGNvbnN0IGJ1ZiA9IEJ1ZmZlci5hbGxvY1Vuc2FmZSgxMClcbiAgICAgIGF3YWl0IHRoaXMucmVhZChidWYsIDAsIDEwLCAwKVxuICAgICAgaWYgKCF0aGlzLl9zdGF0KSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihgdW5hYmxlIHRvIGRldGVybWluZSBzaXplIG9mIGZpbGUgYXQgJHt0aGlzLnVybH1gKVxuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fc3RhdFxuICB9XG5cbiAgcHVibGljIGFzeW5jIGNsb3NlKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVyblxuICB9XG59XG4iXX0=

/***/ }),

/***/ 5666:
/***/ ((module) => {

/**
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

var runtime = (function (exports) {
  "use strict";

  var Op = Object.prototype;
  var hasOwn = Op.hasOwnProperty;
  var undefined; // More compressible than void 0.
  var $Symbol = typeof Symbol === "function" ? Symbol : {};
  var iteratorSymbol = $Symbol.iterator || "@@iterator";
  var asyncIteratorSymbol = $Symbol.asyncIterator || "@@asyncIterator";
  var toStringTagSymbol = $Symbol.toStringTag || "@@toStringTag";

  function define(obj, key, value) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
    return obj[key];
  }
  try {
    // IE 8 has a broken Object.defineProperty that only works on DOM objects.
    define({}, "");
  } catch (err) {
    define = function(obj, key, value) {
      return obj[key] = value;
    };
  }

  function wrap(innerFn, outerFn, self, tryLocsList) {
    // If outerFn provided and outerFn.prototype is a Generator, then outerFn.prototype instanceof Generator.
    var protoGenerator = outerFn && outerFn.prototype instanceof Generator ? outerFn : Generator;
    var generator = Object.create(protoGenerator.prototype);
    var context = new Context(tryLocsList || []);

    // The ._invoke method unifies the implementations of the .next,
    // .throw, and .return methods.
    generator._invoke = makeInvokeMethod(innerFn, self, context);

    return generator;
  }
  exports.wrap = wrap;

  // Try/catch helper to minimize deoptimizations. Returns a completion
  // record like context.tryEntries[i].completion. This interface could
  // have been (and was previously) designed to take a closure to be
  // invoked without arguments, but in all the cases we care about we
  // already have an existing method we want to call, so there's no need
  // to create a new function object. We can even get away with assuming
  // the method takes exactly one argument, since that happens to be true
  // in every case, so we don't have to touch the arguments object. The
  // only additional allocation required is the completion record, which
  // has a stable shape and so hopefully should be cheap to allocate.
  function tryCatch(fn, obj, arg) {
    try {
      return { type: "normal", arg: fn.call(obj, arg) };
    } catch (err) {
      return { type: "throw", arg: err };
    }
  }

  var GenStateSuspendedStart = "suspendedStart";
  var GenStateSuspendedYield = "suspendedYield";
  var GenStateExecuting = "executing";
  var GenStateCompleted = "completed";

  // Returning this object from the innerFn has the same effect as
  // breaking out of the dispatch switch statement.
  var ContinueSentinel = {};

  // Dummy constructor functions that we use as the .constructor and
  // .constructor.prototype properties for functions that return Generator
  // objects. For full spec compliance, you may wish to configure your
  // minifier not to mangle the names of these two functions.
  function Generator() {}
  function GeneratorFunction() {}
  function GeneratorFunctionPrototype() {}

  // This is a polyfill for %IteratorPrototype% for environments that
  // don't natively support it.
  var IteratorPrototype = {};
  define(IteratorPrototype, iteratorSymbol, function () {
    return this;
  });

  var getProto = Object.getPrototypeOf;
  var NativeIteratorPrototype = getProto && getProto(getProto(values([])));
  if (NativeIteratorPrototype &&
      NativeIteratorPrototype !== Op &&
      hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
    // This environment has a native %IteratorPrototype%; use it instead
    // of the polyfill.
    IteratorPrototype = NativeIteratorPrototype;
  }

  var Gp = GeneratorFunctionPrototype.prototype =
    Generator.prototype = Object.create(IteratorPrototype);
  GeneratorFunction.prototype = GeneratorFunctionPrototype;
  define(Gp, "constructor", GeneratorFunctionPrototype);
  define(GeneratorFunctionPrototype, "constructor", GeneratorFunction);
  GeneratorFunction.displayName = define(
    GeneratorFunctionPrototype,
    toStringTagSymbol,
    "GeneratorFunction"
  );

  // Helper for defining the .next, .throw, and .return methods of the
  // Iterator interface in terms of a single ._invoke method.
  function defineIteratorMethods(prototype) {
    ["next", "throw", "return"].forEach(function(method) {
      define(prototype, method, function(arg) {
        return this._invoke(method, arg);
      });
    });
  }

  exports.isGeneratorFunction = function(genFun) {
    var ctor = typeof genFun === "function" && genFun.constructor;
    return ctor
      ? ctor === GeneratorFunction ||
        // For the native GeneratorFunction constructor, the best we can
        // do is to check its .name property.
        (ctor.displayName || ctor.name) === "GeneratorFunction"
      : false;
  };

  exports.mark = function(genFun) {
    if (Object.setPrototypeOf) {
      Object.setPrototypeOf(genFun, GeneratorFunctionPrototype);
    } else {
      genFun.__proto__ = GeneratorFunctionPrototype;
      define(genFun, toStringTagSymbol, "GeneratorFunction");
    }
    genFun.prototype = Object.create(Gp);
    return genFun;
  };

  // Within the body of any async function, `await x` is transformed to
  // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
  // `hasOwn.call(value, "__await")` to determine if the yielded value is
  // meant to be awaited.
  exports.awrap = function(arg) {
    return { __await: arg };
  };

  function AsyncIterator(generator, PromiseImpl) {
    function invoke(method, arg, resolve, reject) {
      var record = tryCatch(generator[method], generator, arg);
      if (record.type === "throw") {
        reject(record.arg);
      } else {
        var result = record.arg;
        var value = result.value;
        if (value &&
            typeof value === "object" &&
            hasOwn.call(value, "__await")) {
          return PromiseImpl.resolve(value.__await).then(function(value) {
            invoke("next", value, resolve, reject);
          }, function(err) {
            invoke("throw", err, resolve, reject);
          });
        }

        return PromiseImpl.resolve(value).then(function(unwrapped) {
          // When a yielded Promise is resolved, its final value becomes
          // the .value of the Promise<{value,done}> result for the
          // current iteration.
          result.value = unwrapped;
          resolve(result);
        }, function(error) {
          // If a rejected Promise was yielded, throw the rejection back
          // into the async generator function so it can be handled there.
          return invoke("throw", error, resolve, reject);
        });
      }
    }

    var previousPromise;

    function enqueue(method, arg) {
      function callInvokeWithMethodAndArg() {
        return new PromiseImpl(function(resolve, reject) {
          invoke(method, arg, resolve, reject);
        });
      }

      return previousPromise =
        // If enqueue has been called before, then we want to wait until
        // all previous Promises have been resolved before calling invoke,
        // so that results are always delivered in the correct order. If
        // enqueue has not been called before, then it is important to
        // call invoke immediately, without waiting on a callback to fire,
        // so that the async generator function has the opportunity to do
        // any necessary setup in a predictable way. This predictability
        // is why the Promise constructor synchronously invokes its
        // executor callback, and why async functions synchronously
        // execute code before the first await. Since we implement simple
        // async functions in terms of async generators, it is especially
        // important to get this right, even though it requires care.
        previousPromise ? previousPromise.then(
          callInvokeWithMethodAndArg,
          // Avoid propagating failures to Promises returned by later
          // invocations of the iterator.
          callInvokeWithMethodAndArg
        ) : callInvokeWithMethodAndArg();
    }

    // Define the unified helper method that is used to implement .next,
    // .throw, and .return (see defineIteratorMethods).
    this._invoke = enqueue;
  }

  defineIteratorMethods(AsyncIterator.prototype);
  define(AsyncIterator.prototype, asyncIteratorSymbol, function () {
    return this;
  });
  exports.AsyncIterator = AsyncIterator;

  // Note that simple async functions are implemented on top of
  // AsyncIterator objects; they just return a Promise for the value of
  // the final result produced by the iterator.
  exports.async = function(innerFn, outerFn, self, tryLocsList, PromiseImpl) {
    if (PromiseImpl === void 0) PromiseImpl = Promise;

    var iter = new AsyncIterator(
      wrap(innerFn, outerFn, self, tryLocsList),
      PromiseImpl
    );

    return exports.isGeneratorFunction(outerFn)
      ? iter // If outerFn is a generator, return the full iterator.
      : iter.next().then(function(result) {
          return result.done ? result.value : iter.next();
        });
  };

  function makeInvokeMethod(innerFn, self, context) {
    var state = GenStateSuspendedStart;

    return function invoke(method, arg) {
      if (state === GenStateExecuting) {
        throw new Error("Generator is already running");
      }

      if (state === GenStateCompleted) {
        if (method === "throw") {
          throw arg;
        }

        // Be forgiving, per 25.3.3.3.3 of the spec:
        // https://people.mozilla.org/~jorendorff/es6-draft.html#sec-generatorresume
        return doneResult();
      }

      context.method = method;
      context.arg = arg;

      while (true) {
        var delegate = context.delegate;
        if (delegate) {
          var delegateResult = maybeInvokeDelegate(delegate, context);
          if (delegateResult) {
            if (delegateResult === ContinueSentinel) continue;
            return delegateResult;
          }
        }

        if (context.method === "next") {
          // Setting context._sent for legacy support of Babel's
          // function.sent implementation.
          context.sent = context._sent = context.arg;

        } else if (context.method === "throw") {
          if (state === GenStateSuspendedStart) {
            state = GenStateCompleted;
            throw context.arg;
          }

          context.dispatchException(context.arg);

        } else if (context.method === "return") {
          context.abrupt("return", context.arg);
        }

        state = GenStateExecuting;

        var record = tryCatch(innerFn, self, context);
        if (record.type === "normal") {
          // If an exception is thrown from innerFn, we leave state ===
          // GenStateExecuting and loop back for another invocation.
          state = context.done
            ? GenStateCompleted
            : GenStateSuspendedYield;

          if (record.arg === ContinueSentinel) {
            continue;
          }

          return {
            value: record.arg,
            done: context.done
          };

        } else if (record.type === "throw") {
          state = GenStateCompleted;
          // Dispatch the exception by looping back around to the
          // context.dispatchException(context.arg) call above.
          context.method = "throw";
          context.arg = record.arg;
        }
      }
    };
  }

  // Call delegate.iterator[context.method](context.arg) and handle the
  // result, either by returning a { value, done } result from the
  // delegate iterator, or by modifying context.method and context.arg,
  // setting context.delegate to null, and returning the ContinueSentinel.
  function maybeInvokeDelegate(delegate, context) {
    var method = delegate.iterator[context.method];
    if (method === undefined) {
      // A .throw or .return when the delegate iterator has no .throw
      // method always terminates the yield* loop.
      context.delegate = null;

      if (context.method === "throw") {
        // Note: ["return"] must be used for ES3 parsing compatibility.
        if (delegate.iterator["return"]) {
          // If the delegate iterator has a return method, give it a
          // chance to clean up.
          context.method = "return";
          context.arg = undefined;
          maybeInvokeDelegate(delegate, context);

          if (context.method === "throw") {
            // If maybeInvokeDelegate(context) changed context.method from
            // "return" to "throw", let that override the TypeError below.
            return ContinueSentinel;
          }
        }

        context.method = "throw";
        context.arg = new TypeError(
          "The iterator does not provide a 'throw' method");
      }

      return ContinueSentinel;
    }

    var record = tryCatch(method, delegate.iterator, context.arg);

    if (record.type === "throw") {
      context.method = "throw";
      context.arg = record.arg;
      context.delegate = null;
      return ContinueSentinel;
    }

    var info = record.arg;

    if (! info) {
      context.method = "throw";
      context.arg = new TypeError("iterator result is not an object");
      context.delegate = null;
      return ContinueSentinel;
    }

    if (info.done) {
      // Assign the result of the finished delegate to the temporary
      // variable specified by delegate.resultName (see delegateYield).
      context[delegate.resultName] = info.value;

      // Resume execution at the desired location (see delegateYield).
      context.next = delegate.nextLoc;

      // If context.method was "throw" but the delegate handled the
      // exception, let the outer generator proceed normally. If
      // context.method was "next", forget context.arg since it has been
      // "consumed" by the delegate iterator. If context.method was
      // "return", allow the original .return call to continue in the
      // outer generator.
      if (context.method !== "return") {
        context.method = "next";
        context.arg = undefined;
      }

    } else {
      // Re-yield the result returned by the delegate method.
      return info;
    }

    // The delegate iterator is finished, so forget it and continue with
    // the outer generator.
    context.delegate = null;
    return ContinueSentinel;
  }

  // Define Generator.prototype.{next,throw,return} in terms of the
  // unified ._invoke helper method.
  defineIteratorMethods(Gp);

  define(Gp, toStringTagSymbol, "Generator");

  // A Generator should always return itself as the iterator object when the
  // @@iterator function is called on it. Some browsers' implementations of the
  // iterator prototype chain incorrectly implement this, causing the Generator
  // object to not be returned from this call. This ensures that doesn't happen.
  // See https://github.com/facebook/regenerator/issues/274 for more details.
  define(Gp, iteratorSymbol, function() {
    return this;
  });

  define(Gp, "toString", function() {
    return "[object Generator]";
  });

  function pushTryEntry(locs) {
    var entry = { tryLoc: locs[0] };

    if (1 in locs) {
      entry.catchLoc = locs[1];
    }

    if (2 in locs) {
      entry.finallyLoc = locs[2];
      entry.afterLoc = locs[3];
    }

    this.tryEntries.push(entry);
  }

  function resetTryEntry(entry) {
    var record = entry.completion || {};
    record.type = "normal";
    delete record.arg;
    entry.completion = record;
  }

  function Context(tryLocsList) {
    // The root entry object (effectively a try statement without a catch
    // or a finally block) gives us a place to store values thrown from
    // locations where there is no enclosing try statement.
    this.tryEntries = [{ tryLoc: "root" }];
    tryLocsList.forEach(pushTryEntry, this);
    this.reset(true);
  }

  exports.keys = function(object) {
    var keys = [];
    for (var key in object) {
      keys.push(key);
    }
    keys.reverse();

    // Rather than returning an object with a next method, we keep
    // things simple and return the next function itself.
    return function next() {
      while (keys.length) {
        var key = keys.pop();
        if (key in object) {
          next.value = key;
          next.done = false;
          return next;
        }
      }

      // To avoid creating an additional object, we just hang the .value
      // and .done properties off the next function object itself. This
      // also ensures that the minifier will not anonymize the function.
      next.done = true;
      return next;
    };
  };

  function values(iterable) {
    if (iterable) {
      var iteratorMethod = iterable[iteratorSymbol];
      if (iteratorMethod) {
        return iteratorMethod.call(iterable);
      }

      if (typeof iterable.next === "function") {
        return iterable;
      }

      if (!isNaN(iterable.length)) {
        var i = -1, next = function next() {
          while (++i < iterable.length) {
            if (hasOwn.call(iterable, i)) {
              next.value = iterable[i];
              next.done = false;
              return next;
            }
          }

          next.value = undefined;
          next.done = true;

          return next;
        };

        return next.next = next;
      }
    }

    // Return an iterator with no values.
    return { next: doneResult };
  }
  exports.values = values;

  function doneResult() {
    return { value: undefined, done: true };
  }

  Context.prototype = {
    constructor: Context,

    reset: function(skipTempReset) {
      this.prev = 0;
      this.next = 0;
      // Resetting context._sent for legacy support of Babel's
      // function.sent implementation.
      this.sent = this._sent = undefined;
      this.done = false;
      this.delegate = null;

      this.method = "next";
      this.arg = undefined;

      this.tryEntries.forEach(resetTryEntry);

      if (!skipTempReset) {
        for (var name in this) {
          // Not sure about the optimal order of these conditions:
          if (name.charAt(0) === "t" &&
              hasOwn.call(this, name) &&
              !isNaN(+name.slice(1))) {
            this[name] = undefined;
          }
        }
      }
    },

    stop: function() {
      this.done = true;

      var rootEntry = this.tryEntries[0];
      var rootRecord = rootEntry.completion;
      if (rootRecord.type === "throw") {
        throw rootRecord.arg;
      }

      return this.rval;
    },

    dispatchException: function(exception) {
      if (this.done) {
        throw exception;
      }

      var context = this;
      function handle(loc, caught) {
        record.type = "throw";
        record.arg = exception;
        context.next = loc;

        if (caught) {
          // If the dispatched exception was caught by a catch block,
          // then let that catch block handle the exception normally.
          context.method = "next";
          context.arg = undefined;
        }

        return !! caught;
      }

      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        var record = entry.completion;

        if (entry.tryLoc === "root") {
          // Exception thrown outside of any try block that could handle
          // it, so set the completion value of the entire function to
          // throw the exception.
          return handle("end");
        }

        if (entry.tryLoc <= this.prev) {
          var hasCatch = hasOwn.call(entry, "catchLoc");
          var hasFinally = hasOwn.call(entry, "finallyLoc");

          if (hasCatch && hasFinally) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            } else if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else if (hasCatch) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            }

          } else if (hasFinally) {
            if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else {
            throw new Error("try statement without catch or finally");
          }
        }
      }
    },

    abrupt: function(type, arg) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc <= this.prev &&
            hasOwn.call(entry, "finallyLoc") &&
            this.prev < entry.finallyLoc) {
          var finallyEntry = entry;
          break;
        }
      }

      if (finallyEntry &&
          (type === "break" ||
           type === "continue") &&
          finallyEntry.tryLoc <= arg &&
          arg <= finallyEntry.finallyLoc) {
        // Ignore the finally entry if control is not jumping to a
        // location outside the try/catch block.
        finallyEntry = null;
      }

      var record = finallyEntry ? finallyEntry.completion : {};
      record.type = type;
      record.arg = arg;

      if (finallyEntry) {
        this.method = "next";
        this.next = finallyEntry.finallyLoc;
        return ContinueSentinel;
      }

      return this.complete(record);
    },

    complete: function(record, afterLoc) {
      if (record.type === "throw") {
        throw record.arg;
      }

      if (record.type === "break" ||
          record.type === "continue") {
        this.next = record.arg;
      } else if (record.type === "return") {
        this.rval = this.arg = record.arg;
        this.method = "return";
        this.next = "end";
      } else if (record.type === "normal" && afterLoc) {
        this.next = afterLoc;
      }

      return ContinueSentinel;
    },

    finish: function(finallyLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.finallyLoc === finallyLoc) {
          this.complete(entry.completion, entry.afterLoc);
          resetTryEntry(entry);
          return ContinueSentinel;
        }
      }
    },

    "catch": function(tryLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc === tryLoc) {
          var record = entry.completion;
          if (record.type === "throw") {
            var thrown = record.arg;
            resetTryEntry(entry);
          }
          return thrown;
        }
      }

      // The context.catch method must only be called with a location
      // argument that corresponds to a known catch block.
      throw new Error("illegal catch attempt");
    },

    delegateYield: function(iterable, resultName, nextLoc) {
      this.delegate = {
        iterator: values(iterable),
        resultName: resultName,
        nextLoc: nextLoc
      };

      if (this.method === "next") {
        // Deliberately forget the last sent value so that we don't
        // accidentally pass it on to the delegate.
        this.arg = undefined;
      }

      return ContinueSentinel;
    }
  };

  // Regardless of whether this script is executing as a CommonJS module
  // or not, return the runtime object so that we can declare the variable
  // regeneratorRuntime in the outer scope, which allows this module to be
  // injected easily by `bin/regenerator --include-runtime script.js`.
  return exports;

}(
  // If this script is executing as a CommonJS module, use module.exports
  // as the regeneratorRuntime namespace. Otherwise create a new empty
  // object. Either way, the resulting object will be used to initialize
  // the regeneratorRuntime variable at the top of this file.
   true ? module.exports : 0
));

try {
  regeneratorRuntime = runtime;
} catch (accidentalStrictMode) {
  // This module should not be running in strict mode, so the above
  // assignment should always work unless something is misconfigured. Just
  // in case runtime.js accidentally runs in strict mode, in modern engines
  // we can explicitly access globalThis. In older engines we can escape
  // strict mode using a global Function call. This could conceivably fail
  // if a Content Security Policy forbids using Function, but in that case
  // the proper solution is to fix the accidental strict mode problem. If
  // you've misconfigured your bundler to force strict mode and applied a
  // CSP to forbid Function, and you're not willing to fix either of those
  // problems, please detail your unique predicament in a GitHub issue.
  if (typeof globalThis === "object") {
    globalThis.regeneratorRuntime = runtime;
  } else {
    Function("r", "regeneratorRuntime = r")(runtime);
  }
}


/***/ })

}]);