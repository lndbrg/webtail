"""
The MIT License (MIT)

Copyright (c) <2013> <Olle Lundberg>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from gevent import monkey
monkey.patch_all()
import io
import os
import time
import gevent
from gevent.queue import Empty, JoinableQueue
from flask import Flask, Response, render_template_string

directory_list_template = """
<!doctype html>
<head>
<title>Webtail</title>
</head>
<body>
<p>
Welcome to Webtail, you can choose to tream <a href="/stream/all">all</a>
files in separate containersor stream all files
<a href="/stream/all/interleaved">interleaved</a> in the same container
</p>
<p>You can also chose to stream one file at the time:<br>
{% for file in files %}
<a href="/stream/raw/{{file}}">{{file}}</a><br>
{% endfor %}
</p>
</body>
</html>
"""

stream_all_template = """
<!doctype html>
<head>
<title>Webtail</title>
<style>
div {
width: 50%;
float: left;
}
iframe {
width: 100%;
}
</style>
</head>
<body>
<form>
{% for file in files %}
<div><label><input type="checkbox" data-target="{{file}}"
checked>Autoscroll {{file}}</label><br>
<iframe src="{{path}}{{file}}" id="{{file}}"></iframe>
</div>
{% endfor %}
</form>

<script type="text/javascript">
setInterval(function autoScroll() {
    console.log("Running");
    var checkboxes = document.querySelectorAll('input:checked');

    for(var i = 0; i < checkboxes.length; i+=1) {
        var checkbox = checkboxes[i];
        var iframe = document.getElementById(checkbox.getAttribute("data-target"));
        iframe.contentWindow.document.body.scrollTop+=20;
    }
    }, 10)
</script>
</body>
</html>
"""

app = Flask(__name__)


def tail(thefile):
    fd = io.open(thefile, 'r')
    fd.seek(0)
    while True:
        line = fd.readline()
        if not line:
            # Sleep for a short while. This allows gevent to swith to another
            # greenlet. It also won't force the cpu to spike.
            time.sleep(0.001)
            continue
        yield line


def files():
    return (item for item in os.listdir(os.curdir) if os.path.isfile(item))


@app.route('/')
def index():
    return render_template_string(directory_list_template,
                                  files=files()
                                  )


@app.route("/stream/all")
def stream_all():
    return render_template_string(stream_all_template,
                                  files=files(),
                                  path="/stream/raw/"
                                  )


@app.route("/stream/all/interleaved")
def stream_all_interleaved():
    return render_template_string(stream_all_template,
                                  files=['interleaved'],
                                  path="/stream/all/raw/"
                                  )


@app.route("/stream/raw/<thefile>")
def raw(thefile):
    return Response(tail(thefile), mimetype='text/plain')


@app.route("/stream/all/raw/interleaved")
def stream_all_raw_interleaved():
    q = JoinableQueue()

    def httpwriter():

        def filereader(thefile):
            for line in tail(thefile):
                q.put((thefile, line, ))
                #sleep in order to let gevent schedule another greenlet.
                time.sleep(0.001)

        for thefile in files():
            gevent.spawn(filereader, thefile)

        while True:
            try:
                yield "{0}: {1}".format(*q.get())
            except Empty:
                time.sleep(0.001)

    return Response(httpwriter(), mimetype='text/plain')

if __name__ == '__main__':
    from optparse import OptionParser
    from gevent.pywsgi import WSGIServer

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-D", "--debug",
                      action="store_true",
                      default=False,
                      dest="debug",
                      help="turn on debug for the flask application")
    parser.add_option("-d", "--directory",
                      action="store",
                      default='.',
                      dest="directory",
                      metavar="DIR",
                      help="read from DIR")

    (options, args) = parser.parse_args()

    app.debug = options.debug
    os.chdir(options.directory)

    # Here we go!
    http_server = WSGIServer(('', 5000), app)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
