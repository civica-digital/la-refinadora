from flask.ext.assets import Bundle, Environment
from .. import app


"""
    You can register assets for
    the application in this file.

"""

bundles = {
    'application_js': Bundle(
        'js/lib/dropzone.js',
        'js/accordion.js',
        'js/application.js',
        output='gen/application.js'),

    'application_css': Bundle(
        'stylesheets/accordion.css',
        'stylesheets/dropzone.css',
        'stylesheets/landing.css',
        'stylesheets/main.css',
        output='gen/application.css')
}

assets = Environment(app)
assets.register(bundles)
