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

    # Priority 1: locale from query string
    locale = request.args.get('locale', None)
    if locale and locale in Config.LANGUAGES:
        return locale

    # Priority 2: locale from user settings
    user = get_user()
    if user:
        user_locale = user.get('locale', None)
        if user_locale and user_locale in Config.LANGUAGES:
            print(user_locale)
            return user_locale

    # Priority 3: locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    return render_template('6-index.html')


def get_user():
    """ Returns a user dict or None if the ID cannot be found
    ID ==  url value of login_as param"""
    ID = request.args.get('login_as', None)
    if ID:
        if ID.isnumeric():
            return users.get(int(ID), None)


@app.before_request
def before_request():
    """ Executes before other functions in a request
    context
    """
    user = get_user()
    print(user)
    if user:
        g.user = user

# babel = Babel(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run()
