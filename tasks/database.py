from invoke import task

from flask import Flask
from validadora.initializers.database import initialize_db
from validadora.models.users import User
from uuid import uuid4
import getpass

@task
def add_user():
    app = Flask(__name__)
    initialize_db(app)
    email = input()
    password = getpass.getpass(prompt="Password:")
    api_key = uuid4().hex

    User(email=email, password=password, authenticated=True, api_token=api_key)

