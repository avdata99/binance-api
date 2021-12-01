# create a secret.py file with real values

api_key=""
secrete_key=""

try:
    from .secret import *
except (ModuleNotFoundError, ImportError):
    pass
