from validadora.proxy import Proxy as proxy

db = proxy.db

class User(db.Document):
    email = db.EmailField(max_lenth=50, required=True, unique=True)
    password = db.StringField(max_length=200, required=True)
    authenticated = db.BooleanField(required=True, default=False)
    api_key = db.StringField(max_length=50, required=True)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
