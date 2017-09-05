from functools import wraps

from peo.blueprints import get_error_resp
from peo.blueprints import with_common_errors
from peo.models.account import Account


@with_common_errors
def handle_errors(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Account.DoesNotExist:
            return get_error_resp({"message": "Account with that ID no longer exists.", "status": 404})
        except Account.LoginAlreadyInUse:
            return get_error_resp({"message": "Account with that name already exists.", "status": 400})
        except Account.IncorrectLoginOrPassword:
            return get_error_resp({"message": "Incorrect login or password", "status": 400})
    return wrap
