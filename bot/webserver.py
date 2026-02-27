from flask import flask
from threading import Thread

app = flask('')
@app.route('/')
def home():
    return flask.render_template('index.html')
def run():
    app.run(host='0.0.0.0', port=10000)
def keep_alive():
    t = Thread(target=run)
    t.start()