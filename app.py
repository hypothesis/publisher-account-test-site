import os

from hypothesis import HypothesisClient
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'notverysecret'
hypothesis_service = os.environ.get('HYPOTHESIS_SERVICE', 'http://localhost:5000')
hyp_client = HypothesisClient(authority=os.environ['HYPOTHESIS_AUTHORITY'],
                              client_id=os.environ['HYPOTHESIS_CLIENT_ID'],
                              client_secret=os.environ['HYPOTHESIS_CLIENT_SECRET'],
                              service=hypothesis_service)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    hyp_client.create_account(username, email='{}@partner.org'.format(username))
    session['username'] = username
    return redirect(url_for('index'))


@app.route('/')
def index():
    username = session.get('username', None)
    return render_template('article.html',
                           grant_token=hyp_client.grant_token(username=username),
                           username=username,
                           service_url=hypothesis_service)
