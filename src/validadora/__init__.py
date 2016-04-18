from flask import Flask

app = Flask(__name__)
try:
    app.config.from_envvar('VALIDADORA_SETTINGS')
except:
    app.config["WTF_CSRF_ENABLED"] = True
    app.config["SECRET_KEY"] = 'f7C3{1s|0[0Whmy'

from . import views

def run():
    import os
    port = int(os.getenv('REFINADORA_PORT', 5000))
    host = os.getenv('REFINADORA_HOST', '127.0.0.1')

    app.run(host, port, debug=True)

if __name__ == "__main__":
    run()