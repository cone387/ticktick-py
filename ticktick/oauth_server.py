import time
from flask import Flask, request

app = Flask(__name__)


_redirected_url = None
_is_got_redirected_url = False


def stop_server():
    import os
    pid = os.getpid()
    os.kill(pid, 9)


@app.route("/")
def auth():
    global _redirected_url
    if "code" in request.args:
        _redirected_url = request.url
        return "redirected url is %s" % _redirected_url
    else:
        return "code not found in %s" % request.url


@app.route('/get_redirected_url')
def get_redirected_url():
    global _is_got_redirected_url, _redirected_url
    while _redirected_url is None:
        time.sleep(1)
    _is_got_redirected_url = True
    return _redirected_url


def is_got_redirected_url():
    while not _is_got_redirected_url:
        time.sleep(1)
    stop_server()


# threading.Thread(target=is_got_redirected_url, daemon=True).start()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument("-p", '--port', type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)
