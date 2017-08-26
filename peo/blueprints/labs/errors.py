from functools import wraps

from peo.blueprints import get_error_resp
from peo.models.lab import Lab


def handle_errors(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Lab.DoesNotExist:
            return get_error_resp({"message": "A lab with that ID no longer exists.", "status": 404})
        except Lab.NameAlreadyInUse:
            return get_error_resp({"message": "A lab with that name already exists.", "status": 400})
    return wrap
