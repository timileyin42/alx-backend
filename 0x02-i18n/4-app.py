#!/usr/bin/env python3


"""Flask app"""


from flask import Flask
from flask import render_template
from flask import request
from flask_babel import Babel


class Config(object):
    """Babel Configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Best language selection and return match"""
    u = request.query_string.decode('utf-8').split('&')
    qt = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        u,
    ))
    if 'locale' in qt:
        if qt['locale'] in app.config["LANGUAGES"]:
            return qt['locale']
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """Route handler"""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
