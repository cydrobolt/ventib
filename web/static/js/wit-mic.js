var Microphone, VERSION, WEBSOCKET_HOST, WitError, log, states;

VERSION = "0.8.0";

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

window.AudioContext = window.AudioContext || window.webkitAudioContext || window.mozAudioContext || window.msAudioContext;

(function() {
  var browserRaf, canceled, j, len, ref, targetTime, vendor, w;
  w = window;
  ref = ['ms', 'moz', 'webkit', 'o'];
  for (j = 0, len = ref.length; j < len; j++) {
    vendor = ref[j];
    if (w.requestAnimationFrame) {
      break;
    }
    w.requestAnimationFrame = w[vendor + "RequestAnimationFrame"];
    w.cancelAnimationFrame = w[vendor + "CancelAnimationFrame"] || w[vendor + "CancelRequestAnimationFrame"];
  }
  if (w.requestAnimationFrame) {
    if (w.cancelAnimationFrame) {
      return;
    }
    browserRaf = w.requestAnimationFrame;
    canceled = {};
    w.requestAnimationFrame = function(callback) {
      var id;
      return id = browserRaf(function(time) {
        if (id in canceled) {
          return delete canceled[id];
        } else {
          return callback(time);
        }
      });
    };
    return w.cancelAnimationFrame = function(id) {
      return canceled[id] = true;
    };
  } else {
    targetTime = 0;
    w.requestAnimationFrame = function(callback) {
      var currentTime;
      targetTime = Math.max(targetTime + 16, currentTime = +(new Date));
      return w.setTimeout((function() {
        return callback(+(new Date));
      }), targetTime - currentTime);
    };
    return w.cancelAnimationFrame = function(id) {
      return clearTimeout(id);
    };
  }
})();

log = (typeof localStorage !== "undefined" && localStorage !== null ? localStorage.getItem : void 0) && localStorage.getItem('wit_debug') ? (function() {
  return console.log.apply(console, arguments);
}) : function() {};

WitError = function(message, infos) {
  this.name = "WitError";
  this.message = message || "";
  this.infos = infos;
  return this;
};

WitError.prototype = Error.prototype;

WEBSOCKET_HOST = 'wss://api.wit.ai/speech_ws';

Microphone = function(elem) {
  var ns, svg;
  this.conn = null;
  this.ctx = new AudioContext();
  this.state = 'disconnected';
  this.rec = false;
  this.handleError = function(e) {
    var err, f;
    if (_.isFunction(f = this.onerror)) {
      err = _.isString(e) ? e : _.isString(e.message) ? e.message : "Something went wrong!";
      return f.call(window, err, e);
    }
  };
  this.handleResult = function(res) {
    var entities, f, fullText, intent;
    if (_.isFunction(f = this.onresult)) {
      intent = res.outcome.intent;
      entities = res.outcome.entities;
      fullText = res.msg_body;
      return f.call(window, intent, entities, fullText, res);
    }
  };
  if (elem) {
    this.elem = elem;
    elem.innerHTML = "<div class='mic mic-box icon-wit-mic'>\n</div>\n<svg class='mic-svg mic-box'>\n</svg>";
    elem.className += ' wit-microphone';
    elem.addEventListener('click', (function(_this) {
      return function(e) {
        return _this.fsm('toggle_record');
      };
    })(this));
    svg = this.elem.children[1];
    ns = "http://www.w3.org/2000/svg";
    this.path = document.createElementNS(ns, 'path');
    this.path.setAttribute('stroke', '#eee');
    this.path.setAttribute('stroke-width', '5');
    this.path.setAttribute('fill', 'none');
    svg.appendChild(this.path);
  }
  this.rmactive = function() {
    if (this.elem) {
      return this.elem.classList.remove('active');
    }
  };
  this.mkactive = function() {
    if (this.elem) {
      return this.elem.classList.add('active');
    }
  };
  this.mkthinking = function() {
    var T, b, from_x, from_y, h, r, ref, start, style, swf, tick, w, xrotate;
    this.thinking = true;
    if (this.elem) {
      style = getComputedStyle(svg);
      this.elem.classList.add('thinking');
      w = parseInt(style.width, 10);
      h = parseInt(style.height, 10);
      b = style.boxSizing === 'border-box' ? parseInt(style.borderTopWidth, 10) : 0;
      r = w / 2 - b - 5;
      T = 1000;
      from_x = w / 2 - b;
      from_y = h / 2 - b - r;
      xrotate = 0;
      swf = 1;
      start = ((ref = window.performance) != null ? ref.now() : void 0) || new Date;
      tick = (function(_this) {
        return function(time) {
          var laf, rads, to_x, to_y;
          rads = (((time - start) % T) / T) * 2 * Math.PI - Math.PI / 2;
          to_x = Math.cos(rads) * r + w / 2 - b;
          to_y = Math.sin(rads) * r + h / 2 - b;
          laf = +((1.5 * Math.PI > rads && rads > Math.PI / 2));
          _this.path.setAttribute('d', "M" + from_x + "," + from_y + "A" + r + "," + r + "," + xrotate + "," + laf + "," + swf + "," + to_x + "," + to_y);
          if (_this.thinking) {
            return requestAnimationFrame(tick);
          } else {
            _this.elem.classList.remove('thinking');
            return _this.path.setAttribute('d', 'M0,0');
          }
        };
      })(this);
      return requestAnimationFrame(tick);
    }
  };
  this.rmthinking = function() {
    return this.thinking = false;
  };
  return this;
};

states = {
  disconnected: {
    connect: function(token) {
      var conn, on_stream;
      if (!token) {
        this.handleError('No token provided');
      }
      conn = new WebSocket(WEBSOCKET_HOST);
      conn.onopen = (function(_this) {
        return function(e) {
          var opts;
          log("connection opened", e);
          opts = {
            token: token,
            bps: 16,
            encoding: 'signed-integer'
          };
          return conn.send(JSON.stringify(["auth", opts]));
        };
      })(this);
      conn.onclose = (function(_this) {
        return function(e) {
          return _this.fsm('socket_closed');
        };
      })(this);
      conn.onmessage = (function(_this) {
        return function(e) {
          var data, ref, type;
          ref = JSON.parse(e.data), type = ref[0], data = ref[1];
          if (data) {
            return _this.fsm.call(_this, type, data);
          } else {
            return _this.fsm.call(_this, type);
          }
        };
      })(this);
      this.conn = conn;
      on_stream = (function(_this) {
        return function(stream) {
          var ctx, proc, src;
          ctx = _this.ctx;
          src = ctx.createMediaStreamSource(stream);
          proc = (ctx.createScriptProcessor || ctx.createJavascriptNode).call(ctx, 4096, 1, 1);
          proc.onaudioprocess = function(e) {
            var buffer, float32s, i, int16s, j, n_samples, ref, x, y;
            if (!_this.rec) {
              return;
            }
            buffer = e.inputBuffer;
            float32s = buffer.getChannelData(0);
            n_samples = float32s.length;
            int16s = new Int16Array(n_samples);
            for (i = j = 0, ref = n_samples; 0 <= ref ? j <= ref : j >= ref; i = 0 <= ref ? ++j : --j) {
              x = float32s[i];
              y = x < 0 ? x * 0x8000 : x * 0x7fff;
              int16s[i] = y;
            }
            log("[audiobuffer] rate=" + buffer.sampleRate + ", samples=" + n_samples + ", bytes=" + int16s.byteLength);
            return _this.conn.send(int16s);
          };
          src.connect(proc);
          proc.connect(ctx.destination);
          _this.stream = stream;
          _this.proc = proc;
          _this.src = src;
          return _this.fsm('got_stream');
        };
      })(this);
      navigator.getUserMedia({
        audio: true
      }, on_stream, this.handleError);
      return 'connecting';
    }
  },
  connecting: {
    'auth-ok': function() {
      return 'waiting_for_stream';
    },
    got_stream: function() {
      return 'waiting_for_auth';
    },
    error: function(err) {
      this.handleError(err);
      return 'connecting';
    },
    socket_closed: function() {
      return 'disconnected';
    }
  },
  waiting_for_auth: {
    'auth-ok': function() {
      return 'ready';
    }
  },
  waiting_for_stream: {
    got_stream: function() {
      return 'ready';
    }
  },
  ready: {
    socket_closed: function() {
      return 'disconnected';
    },
    timeout: function() {
      return 'ready';
    },
    start: function() {
      return this.fsm('toggle_record');
    },
    toggle_record: function() {
      this.conn.send(JSON.stringify(["start", this.context || {}]));
      this.rec = true;
      if (!this.ctx) {
        console.error("No context");
      }
      if (!this.stream) {
        console.error("No stream");
      }
      if (!this.src) {
        console.error("No source");
      }
      if (!this.proc) {
        console.error("No processor");
      }
      return 'audiostart';
    }
  },
  audiostart: {
    error: function(data) {
      this.rec = false;
      this.handleError(new WitError("Error during recording", {
        code: 'RECORD',
        data: data
      }));
      return 'ready';
    },
    socket_closed: function() {
      this.rec = false;
      return 'disconnected';
    },
    stop: function() {
      return this.fsm('toggle_record');
    },
    toggle_record: function() {
      this.rec = false;
      this.conn.send(JSON.stringify(["stop"]));
      this.timer = setTimeout(((function(_this) {
        return function() {
          return _this.fsm('timeout');
        };
      })(this)), 60000);
      return 'audioend';
    }
  },
  audioend: {
    socket_closed: function() {
      if (this.timer) {
        clearTimeout(this.timer);
      }
      return 'disconnected';
    },
    timeout: function() {
      this.handleError(new WitError('Wit timed out', {
        code: 'TIMEOUT'
      }));
      return 'ready';
    },
    error: function(data) {
      if (this.timer) {
        clearTimeout(this.timer);
      }
      this.handleError(new WitError('Wit did not recognize intent', {
        code: 'RESULT',
        data: data
      }));
      return 'ready';
    },
    result: function(data) {
      if (this.timer) {
        clearTimeout(this.timer);
      }
      this.handleResult(data);
      return 'ready';
    }
  }
};

Microphone.prototype.fsm = function(event) {
  var ary, f, ref, s;
  f = (ref = states[this.state]) != null ? ref[event] : void 0;
  ary = Array.prototype.slice.call(arguments, 1);
  if (_.isFunction(f)) {
    s = f.apply(this, ary);
    log("fsm: " + this.state + " + " + event + " -> " + s, ary);
    this.state = s;
    if (s === 'audiostart' || s === 'audioend' || s === 'ready' || s === 'connecting' || s === 'disconnected') {
      if (_.isFunction(f = this['on' + s])) {
        f.call(window);
      }
    }
    switch (s) {
      case 'disconnected':
        this.rmthinking();
        this.rmactive();
        break;
      case 'ready':
        this.rmthinking();
        this.rmactive();
        break;
      case 'audiostart':
        this.mkactive();
        break;
      case 'audioend':
        this.mkthinking();
        this.rmactive();
    }
  } else {
    log("fsm error: " + this.state + " + " + event, ary);
  }
  return s;
};

Microphone.prototype.connect = function(token) {
  return this.fsm('connect', token);
};

Microphone.prototype.start = function() {
  return this.fsm('start');
};

Microphone.prototype.stop = function() {
  return this.fsm('stop');
};

Microphone.prototype.setContext = function(context) {
  var k, v;
  this.context || (this.context = {});
  for (k in context) {
    v = context[k];
    this.context[k] = context[k];
  }
  log('context: ', this.context);
  return null;
};

window._ || (window._ = {});

_.isFunction || (_.isFunction = function(x) {
  return (typeof x) === 'function';
});

_.isString || (_.isString = function(obj) {
  return toString.call(obj) === '[object String]';
});

window.Wit || (window.Wit = {});

Wit.Microphone = Microphone;
