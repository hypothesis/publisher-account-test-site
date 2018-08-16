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
                              jwt_client_id=os.environ['HYPOTHESIS_JWT_CLIENT_ID'],
                              jwt_client_secret=os.environ['HYPOTHESIS_JWT_CLIENT_SECRET'],
                              service=hypothesis_service)


class LoginPage(MethodView):
    def get(self):
        username = session.get('username')
        context = {}
        if username:
            context['username'] = username

        return render_template('login.html', **context)

    def post(self):
        display_name = request.form['display_name']
        username = request.form['username']
        email = '{}@partner.org'.format(username)
        try:
            hyp_client.create_account(username, email=email,
                                      display_name=display_name)
        except HTTPError as ex:
            if ex.response.status_code != 409:
                raise ex

            if display_name:
                hyp_client.update_account(username, display_name=display_name)

        session['username'] = username
        return redirect(url_for('login'))


app.add_url_rule('/login', view_func=LoginPage.as_view('login'))
app.add_url_rule('/signup', view_func=LoginPage.as_view('signup'))


def render_template_with_context(template):
    """Return the given template rendered with the standard context."""
    username = session.get('username', None)

    if username:
        grant_token = hyp_client.grant_token(username=username)
    else:
        grant_token = None

    hypothesis_api_url = hypothesis_service+'/api/'

    return render_template(
        template,
        grant_token=grant_token,
        hypothesis_api_url=hypothesis_api_url,
        username=username,
        service_url=hypothesis_service,
    )


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template_with_context('article.html')


@app.route('/help')
def help():
    return render_template_with_context('help.html')


@app.route('/profile')
def profile():
    return render_template_with_context('profile.html')
