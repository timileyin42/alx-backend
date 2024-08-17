#!/usr/bin/env python3


"""Flask app"""


from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask_babel import Babel
from typing import Dict
from typing import Union


class Config(object):
    """Babel Configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """If ID can't be found return a user dict or None"""
    id = request.args.get('login_as', None)
    if id and int(id) in users.keys():
        return users.get(int(id))
    return None


@app.before_request
def before_request():
    """If user is not found add to flask.g"""
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Best language selection and return match"""
    u = request.args.get('locale')
    if u in app.config['LANGUAGES']:
        return u
    if g.user:
        u = g.user.get('locale')
        if u and u in app.config['LANGUAGES']:
            return u
    u = request.headers.get('locale', None)
    if u in app.config['LANGUAGES']:
        return u
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Route handler"""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
