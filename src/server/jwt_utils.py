import jwt
import datetime
import config

def encode(data: dict) -> str:
    """
    Encodes the data into a JWT token.
    """
    # Set the expiration time for the token (e.g., 1 hour from now)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    data.update({
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow()
    })
    # Create the JWT token
    token = jwt.encode(data, config.JWT_SECRET, algorithm='HS256')
    
    return token

def decode(token: str) -> dict:
    """
    Decodes the JWT token and returns the payload.
    """
    try:
        # Decode the token
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}