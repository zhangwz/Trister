# coding=utf-8

import os
from functools import wraps

from tweepy import (parsers, OAuthHandler, API, TweepError)
from flask import (Flask, request, session, g)

from twitter_oauth import (TwitterOauth, TwitterOauthError)

application = app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('config')


def jsonify(f):
    @wraps(f)
    def _wrapped(*args, **kwargs):
        from flask import jsonify as flask_jsonify
        try:
            result_dict = f(*args, **kwargs)
        except Exception as e:
            result_dict = dict(status='error')
            if app.config['DEBUG']:
                result_dict['reason'] = e.message
                from traceback import format_exc
                result_dict['exc_info'] = format_exc(e)
        return flask_jsonify(**result_dict)
    return _wrapped


def rebuild_api():
    twit = OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    twit.set_access_token(session.get('trister_access_key'), session.get('trister_access_secret'))
    return API(auth_handler=twit, parser=parsers.RawParser())


@app.before_request
def before_request():
    if session.get('trister_access_key') and session.get('trister_access_secret'):
        g.twit_api = rebuild_api()


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/is_login', methods=['GET'])
@jsonify
def is_login():
    if session.get('trister_access_key') and session.get('trister_access_secret'):
        return dict(status='ok', content=1)
    else:
        return dict(status='ok', content=0)


@app.route('/login', methods=['POST'])
@jsonify
def oauth_login():
    t = TwitterOauth(request.form['name'], request.form['password'])
    try:
        t.oauth()
    except TwitterOauthError, e:
        return dict(status='error', content=e.reason)
    else:
        session['trister_access_key'] = t.access_token
        session['trister_access_secret'] = t.access_token_secret
        return dict(status='ok', content='')


@app.route('/home', methods=['GET'])
def get_home():
    if session.get('trister_access_key') and session.get('trister_access_secret'):
        page_arg = int(request.args['page'])
        count_arg = int(request.args['count'])
        tweets = g.twit_api.home_timeline(page=page_arg, count=count_arg)
        return tweets
    else:
        return app.send_static_file('index.html')


@app.route('/mention', methods=['GET'])
def get_reply():
    if session.get('trister_access_key') and session.get('trister_access_secret'):
        page_arg = int(request.args['page'])
        count_arg = int(request.args['count'])
        replys = g.twit_api.mentions(page=page_arg, count=count_arg)
        return replys
    else:
        return app.send_static_file('index.html')


@app.route('/update', methods=['POST'])
@jsonify
def update_status():
    if session.get('trister_access_key') and session.get('trister_access_secret'):
        try:
            g.twit_api.update_status(request.form['tweet'])
        except TweepError, e:
            return dict(status='error', content='Failed to update tweet!', reason=e.message)
        else:
            return dict(status='success', content='')
    else:
        return app.send_static_file('index.html')


app.secret_key = '\xfcM\xf7\xd4\x03\x14\x1e<\xe1\xd4Sn\xed\xa5e\x96\xb7\x8aq\x82\xed\x10\xdc\x93'
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])