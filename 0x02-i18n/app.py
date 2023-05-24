#!/usr/bin/env python3
"""
Basic flask app
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Dict, Union
import pytz


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


def get_locale():
    """ Get locale from request """

    # Priority 1: locale from query string
    locale = request.args.get('locale', None)
    if locale and locale in Config.LANGUAGES:
        return locale

    # Priority 2: locale from user settings
    user = g.user
    if user:
        user_locale = user.get('locale', None)
        if user_locale and user_locale in Config.LANGUAGES:
            return user_locale

    # Priority 3: locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_timezone():
    """ Infer appropriate time zone """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone('timezone').zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    #
    user = g.user
    if user:
        timezone = user.get('timezone')
        try:
            return pytz.timezone('timezone').zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # get timezone for default config
    return Config.BABEL_DEFAULT_TIMEZONE


def get_user() -> Union[Dict, None]:
    """ Returns a user dict or None if the ID cannot be found
    ID ==  url value of login_as param"""
    ID = request.args.get('login_as', None)
    if ID:
        if ID.isnumeric():
            return users.get(int(ID), None)


@app.before_request
def before_request():
    user = get_user()
    print(user)
    if user:
        g.user = user


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    datetime_formatted = format_datetime()
    return render_template('index.html', datetime_format=datetime_formatted)


babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

if __name__ == "__main__":
    app.run()
