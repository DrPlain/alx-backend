#!/usr/bin/env python3
"""
Basic flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """ configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Get locale from request """
    locale = request.args.get('locale', None)
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    return render_template('5-index.html')


def get_user():
    """ Returns a user dict or None if the ID cannot be found
    ID ==  url value of login_as param"""
    ID = request.args.get('login_as', None)
    if ID:
        if ID.isnumeric():
            return users.get(int(ID), None)


@app.before_request
def before_request():
    """ Executed before any other function in a request
    context
    """
    user = get_user()
    g.user = user
