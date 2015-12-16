from flask import Flask
import sys
import os

sys.path.insert(0, ".")


def run():
    port = int(os.getenv('REFINADORA_PORT', 5000))
    host = os.getenv('REFINADORA_HOST', '127.0.0.1')

    app = Flask(__name__)
    try:
        app.config.from_envvar('VALIDADORA_SETTINGS')
    except:
        app.config["WTF_CSRF_ENABLED"] = True
        app.config["SECRET_KEY"] = 'f7C3{1s|0[0Whmy'

    from validadora.initializers.database import initialize_db
    initialize_db(app)

    from validadora import views
    app.register_blueprint(views.validations)

    from validadora.auth.login import initialize_login
    initialize_login(app)

    app.run(host, port, debug=True)

if __name__ == "__main__":
    run()