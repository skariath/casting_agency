import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
    get the header from the request
        raise an AuthError if no header is present
    split bearer and the token
        raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or not header_parts:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be in the format'
            ' Bearer token'}, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'}, 401)

    return header_parts[1]


'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    raise an AuthError if permissions are not included in the payload
    raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload: 
        abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 401)
    return True

'''
    @INPUTS
        token: a json web token (string)

    Auth0 token with key id (kid)
    verify the token using Auth0 /.well-known/jwks.json
    decode the payload from the token
    validate the claims
    return the decoded payload
    
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Auth0 token should have a key id
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    rsa_key = {}

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break

    # verify the token
    if rsa_key:
        try:
            # Validate the token using the rsa_key
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:

            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:

            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, '
                'check the audience and issuer.'
            }, 401)

        except Exception:

            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    use the get_token_auth_header method to get the token
    use the verify_decode_jwt method to decode the jwt
    use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print("Token")
            print(token)
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
