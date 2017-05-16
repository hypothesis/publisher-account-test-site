import os

from flask import Flask, redirect, render_template, request, session, url_for
from flask.views import MethodView
from requests.exceptions import HTTPError

from hypothesis import HypothesisClient

app = Flask(__name__)
app.secret_key = 'notverysecret'
hypothesis_service = os.environ.get('HYPOTHESIS_SERVICE', 'http://localhost:5000')
hyp_client = HypothesisClient(authority=os.environ['HYPOTHESIS_AUTHORITY'],
                              client_id=os.environ['HYPOTHESIS_CLIENT_ID'],
                              client_secret=os.environ['HYPOTHESIS_CLIENT_SECRET'],
                              service=hypothesis_service)


class LoginPage(MethodView):
    def get(self):
        username = session.get('username')
        context = {}
        if username:
            context['username'] = username

        return render_template('login.html', **context)

    def post(self):
        username = request.form['username']
        email = '{}@partner.org'.format(username)
        try:
            hyp_client.create_account(username, email=email)
        except HTTPError as ex:
            # FIXME: Make the service respond with an appropriate status code and
            # machine-readable error if the user account already exists
            email_err = 'user with email address {} already exists'.format(email)
            username_err = 'user with username {} already exists'.format(username)
            content = ex.response.content
            if email_err not in content and username_err not in content:
                raise ex

        session['username'] = username
        return redirect(url_for('login'))


app.add_url_rule('/login', view_func=LoginPage.as_view('login'))
app.add_url_rule('/signup', view_func=LoginPage.as_view('signup'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    username = session.get('username', None)
    grant_token = None

    if username:
        grant_token = hyp_client.grant_token(username=username)

    return render_template('article.html',
                           grant_token=grant_token,
                           username=username,
                           service_url=hypothesis_service)
