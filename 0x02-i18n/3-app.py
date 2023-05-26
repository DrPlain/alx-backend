#!/usr/bin/env python3
"""
Basic flask app
"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """ configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_locale():
    """ Get locale from request """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ Home route """
    return render_template('3-index.html')


babel = Babel(app, locale_selector=get_locale)

if __name__ == "__main__":
    app.run()
