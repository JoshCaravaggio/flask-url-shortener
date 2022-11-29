import redis
import json
from flask import Flask, abort, request, redirect
import hashlib
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/shorten', methods=['GET'])
def shorten():
    args = request.args
    toShorten = args.get('url')

    if toShorten:
        toShorten = "https://" + toShorten
        #print(f' Storing URL {toShorten}')
        digest = hashlib.sha256(
            bytes(toShorten, encoding='utf-8')).hexdigest()

        shortened = f'{digest}'[-8:-1]
        r.set(shortened, toShorten)
        return json.dumps({'url': toShorten, 'hash': shortened, 'redirectUrl': f'http://127.0.0.1:5000/{shortened}'})


@app.route('/<hash>', methods=['GET'])
def index(hash: list):
    rdr = r.get(hash)
    if rdr:
        #print(f'redirecting to {rdr}')
        return redirect(rdr, code=302)
    else:
        abort(404)


app.run()
