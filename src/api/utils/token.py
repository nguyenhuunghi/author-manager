from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_verification_token(email):
    '''
    the funtion generate verification token and confirm the verification token
    the verification link in the email contain a unique URL with verification token should look like
    http://host/api/users/confirm/<verification_token>
    the token here should always be unique
    '''
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_verification_token(token, expiration=3600):
    '''
    the method to validate the token and expiration
    and as long as the token is valid and not expired
    return the email and verify the user email
    '''
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception as e:
        print (e)
        return e
    return email
