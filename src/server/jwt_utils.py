import jwt
import datetime
import config

def encode(data: dict) -> str:
    """
    Encodes the data into a JWT token.
    """
    # Set the expiration time for the token (e.g., 1 hour from now)
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    
    data.update({
        'exp': expiration_time,
        'iat': datetime.datetime.now()
    })
    # Create the JWT token
    token = jwt.encode(data, config.JWT_SECRET, algorithm='HS256')
    
    return token

def decode(token: str) -> dict:
    """
    Decodes the JWT token and returns the payload.
    """

    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    if not token:
        return {'error': 'Token is required'}
    try:
        # Decode the token
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

def decode_without_verify(token: str) -> dict:
    """
    Decodes the JWT token without verifying the signature.
    """
    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    if not token:
        return {'error': 'Token is required'}
    try:
        # Decode the token without verifying the signature
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.DecodeError:
        return {'error': 'Invalid token'}
