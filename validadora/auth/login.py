from ..models.users import User
import flask.ext.login as flask_login
import base64


def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    print(request.args)
    if api_key:
        user = User.objects(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.objects(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


def user_loader(user_id):
        """Given *user_id*, return the associated User object.

        :param unicode user_id: user_id (email) user to retrieve
        """
        return User.objects.get(user_id)

def initialize_login(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    login_manager.request_loader(load_user_from_request)
    login_manager.user_loader(user_loader)

    return login_manager