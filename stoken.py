from itsdangerous import URLSafeTimedSerializer
from key import secret_key,salt,salt2
def token(data,salt):
    serialiazer=URLSafeTimedSerializer(secret_key)
    return serialiazer.dumps(data,salt=salt)
