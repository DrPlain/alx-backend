#!/usr/bin/env python3
"""
Basic flask app
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Get locale from request """
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    return render_template('3-index.html')

# babel = Babel(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run()
